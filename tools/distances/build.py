import sys, math, json, time, pickle, multiprocessing as mp
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw
from skimage.graph import MCP_Geometric
from grid import Grid
from geo import REGIONS, CHANNELS, APPROACH, DEPTH_MIN, KIEL, ORESUND, SUEZ_BARRIER, ORESUND_BARRIER, BARRIERS, SHALLOW_PENALTY, GATEWAYS
from scipy.io import netcdf_file
from load import PORTS, COORDS
SUEZ_PTS = [(32.32,31.30),(32.32,30.95),(32.30,30.60),(32.35,30.40),(32.45,30.25),(32.56,29.95),(32.56,29.88)]

def hav(lon1, lat1, lon2, lat2):
    R = 3440.065
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2-p1)/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(math.radians(lon2-lon1)/2)**2
    return 2*R*math.asin(math.sqrt(min(1, a)))

def depth_mask(g, name):
    f = netcdf_file(f'etopo_{name}.nc', 'r', mmap=False)
    alt = f.variables['altitude'].data.astype(np.int16)
    lat = f.variables['latitude'].data; lon = f.variables['longitude'].data
    rows = np.array([g.to_ll(0, r)[1] for r in range(g.H)])
    cols = np.array([g.to_ll(c, 0)[0] for c in range(g.W)])
    ri = np.clip(np.rint((rows - lat[0]) / (lat[1]-lat[0])).astype(int), 0, len(lat)-1)
    ci = np.clip(np.rint((cols - lon[0]) / (lon[1]-lon[0])).astype(int), 0, len(lon)-1)
    return alt[np.ix_(ri, ci)] > -DEPTH_MIN

def build_region(name, lon0, lon1, lat0, lat1, kiel=False, suez=True):
    g = Grid(lon0, lon1, lat0, lat1)
    land = g.rasterize()
    shallow = depth_mask(g, name)
    # remove diagonal-only land/water contacts so 8-connected moves cannot slip through land corners
    for _ in range(2):
        a, b, c, d = land[:-1,:-1], land[:-1,1:], land[1:,:-1], land[1:,1:]
        fix1 = a & d & ~b & ~c
        fix2 = b & c & ~a & ~d
        land[:-1,1:] |= fix1
        land[:-1,:-1] |= fix2
    img = Image.fromarray(land.astype('uint8')); dr = ImageDraw.Draw(img)
    chans = CHANNELS + (KIEL + ORESUND if kiel else []) + ([("Suez Canal", SUEZ_PTS)] if suez else [])
    for _, pts in chans:
        if not any(lon0 < lo < lon1 and lat0 < la < lat1 for lo, la in pts): continue
        xy = [g.to_px(lo, la) for lo, la in pts]
        dr.line(xy, fill=0, width=3)
        for x, y in xy: dr.ellipse([x-1.5, y-1.5, x+1.5, y+1.5], fill=0)
    if not suez and lon0 < 32.3 < lon1 and lat0 < 30.5 < lat1:
        dr.line([g.to_px(*p) for p in SUEZ_BARRIER], fill=1, width=5)
    if not kiel and lon0 < 12.8 < lon1 and lat0 < 55.6 < lat1:
        dr.line([g.to_px(*p) for p in ORESUND_BARRIER], fill=1, width=3)
    for _, pts in BARRIERS:
        if any(lon0 < lo < lon1 and lat0 < la < lat1 for lo, la in pts):
            dr.line([g.to_px(*p) for p in pts], fill=1, width=3)
    land = np.array(img, dtype=bool)
    # carved cells count as deep water: mark them by re-drawing channels on a separate layer
    cimg = Image.new('L', (g.W, g.H), 0); cd = ImageDraw.Draw(cimg)
    for _, pts in chans:
        if not any(lon0 < lo < lon1 and lat0 < la < lat1 for lo, la in pts): continue
        cd.line([g.to_px(lo, la) for lo, la in pts], fill=1, width=3)
    carved = np.array(cimg, dtype=bool)
    lab, n = ndimage.label(~land)
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n+1))
    water = lab == (1 + int(np.argmax(sizes)))
    g.water = water
    g.deep = water & (~shallow | carved)
    _, idx = ndimage.distance_transform_edt(~water, return_indices=True)
    g.near = idx
    return g

def port_points(g, name, suez=True):
    out = {}
    gws = {k: v for k, v in GATEWAYS.get(name, {}).items() if suez or k != 'GW:RedSea'}
    for p in list(PORTS) + list(gws):
        lo, la = gws[p] if p in gws else (APPROACH[p][0] if p in APPROACH else (COORDS[p][1], COORDS[p][0]))
        extra = APPROACH[p][1] if p in APPROACH else 0
        if not (g.lon0+0.3 < lo < g.lon1-0.3 and g.lat0+0.3 < la < g.lat1-0.3): continue
        x, y = g.to_px(lo, la)
        r, c = int(round(y-0.5)), int(round(x-0.5))
        r = min(max(r,0), g.H-1); c = min(max(c,0), g.W-1)
        rr, cc = int(g.near[0][r,c]), int(g.near[1][r,c])
        slo, sla = g.to_ll(cc, rr)
        snap = hav(lo, la, slo, sla)
        out[p] = dict(cell=(rr,cc), snap=snap, extra=extra, sea=(slo, sla))
    return out

# ---------- path smoothing ----------
G = None
def visible(a, b, mask=None):
    mask = G.water if mask is None else mask
    n = int(math.ceil(max(abs(b[0]-a[0]), abs(b[1]-a[1]))*3)) + 1
    t = np.linspace(0, 1, n)
    r = np.rint(a[0] + t*(b[0]-a[0])).astype(int)
    c = np.rint(a[1] + t*(b[1]-a[1])).astype(int)
    return bool(mask[r, c].all())

def pull_run(path, mask):
    n = len(path); out = [path[0]]; i = 0
    while i < n-1:
        lo, step = i+1, 1
        while lo+step < n and visible(path[i], path[lo+step], mask):
            lo += step; step *= 2
        hi = min(lo+step, n-1)
        if hi > lo and visible(path[i], path[hi], mask): lo = hi
        else:
            while hi - lo > 1:
                m = (lo+hi)//2
                if visible(path[i], path[m], mask): lo = m
                else: hi = m
        out.append(path[lo]); i = lo
    return out

def pull(path):
    # smooth deep-water stretches against the deep mask, shallow stretches against all water
    path = [tuple(p) for p in path]
    isdeep = [bool(G.deep[r, c]) for r, c in path]
    out = [path[0]]; s = 0
    while s < len(path) - 1:
        e = s
        while e + 1 < len(path) and isdeep[e + 1] == isdeep[s]: e += 1
        e = min(e + 1, len(path) - 1)          # include the first cell of the next run
        seg = pull_run(path[s:e+1], G.deep if isdeep[s] else G.water)
        out.extend(seg[1:]); s = e
    return out

def length(cells):
    ll = [G.to_ll(c, r) for r, c in cells]
    return sum(hav(*ll[k], *ll[k+1]) for k in range(len(ll)-1))

MCP = None; PTS = None
def work(i):
    global MCP
    if MCP is None:
        cosl = np.cos(np.radians([G.to_ll(0, r)[1] for r in range(G.H)]))[:, None]
        cost = np.where(G.water, cosl * np.where(G.deep, 1.0, float(SHALLOW_PENALTY)), np.inf)
        MCP = MCP_Geometric(cost, fully_connected=True)
    names = list(PTS)
    src = names[i]
    ends = [PTS[n]['cell'] for n in names[i+1:]]
    if not ends: return {}
    MCP.find_costs([PTS[src]['cell']], ends, find_all_ends=True)
    res = {}
    for n in names[i+1:]:
        a, b = PTS[src], PTS[n]
        if a['cell'] == b['cell']:
            d = hav(*a['sea'], *b['sea'])
        else:
            path = MCP.traceback(b['cell'])
            d = length(pull(path))
        res[(src, n)] = d + a['snap'] + a['extra'] + b['snap'] + b['extra']
    return res

if __name__ == '__main__':
    only = sys.argv[1:] or [r[0] for r in REGIONS]
    for reg in REGIONS:
      if reg[0] not in only: continue
      kiels = [False, True] if reg[0] == 'EUR' else [False]
      suezs = [True, False] if reg[0] in ('EUR', 'MEA', 'IND') else [True]
      for kiel in kiels:
       for suez in suezs:
        t = time.time()
        tag = f"{reg[0]}_k{int(kiel)}s{int(suez)}"
        G = build_region(*reg, kiel=kiel, suez=suez)
        PTS = port_points(G, reg[0], suez)
        MCP = None
        print(f"{tag}: {G.W}x{G.H}, {len(PTS)} points, built {time.time()-t:.0f}s", flush=True)
        for p, v in PTS.items():
            if v['snap'] > 2.5: print(f"   snap {v['snap']:5.1f} nm  {p}")
        with mp.get_context('fork').Pool(6) as pool:
            out = {}
            for r in pool.imap_unordered(work, range(len(PTS))): out.update(r)
        pickle.dump(dict(dist=out, pts={k: dict(v) for k, v in PTS.items()}), open(f"reg_{tag}.pkl", "wb"))
        print(f"   {len(out)} pairs in {time.time()-t:.0f}s", flush=True)
