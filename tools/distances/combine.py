import glob, pickle, multiprocessing as mp, re
from load import PORTS
from geo import REGIONS

VARIANTS = {'base': (0, 1), 'kiel': (1, 1), 'cape': (0, 0), 'kiel_cape': (1, 0)}   # (kiel, suez open)

def load_region(name, kiel, suez):
    for tag in (f"{name}_k{kiel}s{suez}", f"{name}_k0s{suez}", f"{name}_k0s1"):
        try: return pickle.load(open(f"reg_{tag}.pkl", 'rb'))
        except FileNotFoundError: pass

SEA = {}
for f in glob.glob('reg_*_k0s1.pkl'):
    for p, v in pickle.load(open(f, 'rb'))['pts'].items():
        if not p.startswith('GW:') and (p not in SEA or v['snap'] < SEA[p]['snap']): SEA[p] = v

# Gulf of Suez ports: when Suez is closed, join the long-haul network at the mouth of the gulf
GULF_OF_SUEZ_MOUTH = (33.75, 27.75)
def sea_of(p, suez):
    v = dict(SEA[p])
    if not suez and v['sea'][1] > 27.8 and 32.0 < v['sea'][0] < 33.0:
        from build import hav
        v['extra'] = v['extra'] + hav(*v['sea'], *GULF_OF_SUEZ_MOUTH)
        v['sea'] = GULF_OF_SUEZ_MOUTH
    return v

def sr(job):
    import searoute
    a_pt, b_pt, suez = job
    restr = ['northwest'] + ([] if suez else ['suez'])
    return job, searoute.searoute(list(a_pt), list(b_pt), units='naut', restrictions=restr).properties['length']

def key(a, b): return tuple(sorted((a, b)))

def build_variant(kiel, suez, pool):
    D = {}; regs = {}
    for r in REGIONS:
        R = load_region(r[0], kiel, suez)
        # a port that only reaches this region's main water body by jumping over land is not in it
        R['pts'] = {p: v for p, v in R['pts'].items() if v['snap'] <= 20}
        R['dist'] = {k: d for k, d in R['dist'].items() if k[0] in R['pts'] and k[1] in R['pts']}
        regs[r[0]] = R
        for (a, b), d in R['dist'].items():
            k = key(a, b); D[k] = min(d, D.get(k, 1e18))
    eur = regs['EUR']; eur_pts = eur['pts']
    gws = [g for g in eur_pts if g.startswith('GW:')]
    eur_ports = [p for p in eur_pts if not p.startswith('GW:')]
    def g_to(a, g): return eur['dist'].get((a, g), eur['dist'].get((g, a)))
    missing = [key(a, b) for i, a in enumerate(PORTS) for b in PORTS[i+1:] if key(a, b) not in D]
    jobs = set()
    for a, b in missing:
        if a in eur_pts or b in eur_pts:
            far = b if a in eur_pts else a
            for g in gws: jobs.add((eur_pts[g]['sea'], sea_of(far, suez)['sea'], suez))
        else:
            jobs.add((sea_of(a, suez)['sea'], sea_of(b, suez)['sea'], suez))
    res = dict(pool.imap_unordered(sr, list(jobs), chunksize=40))
    src = {k: 'grid' for k in D}
    for a, b in missing:
        if a in eur_pts or b in eur_pts:
            near, far = (a, b) if a in eur_pts else (b, a)
            F = sea_of(far, suez)
            best = min(g_to(near, g) + res[(eur_pts[g]['sea'], F['sea'], suez)] for g in gws if g_to(near, g) is not None)
            D[(a, b)] = best + F['snap'] + F['extra']; src[(a, b)] = 'gateway'
        else:
            A, B = sea_of(a, suez), sea_of(b, suez)
            D[(a, b)] = res[(A['sea'], B['sea'], suez)] + A['snap'] + A['extra'] + B['snap'] + B['extra']; src[(a, b)] = 'searoute'
    return D, src

if __name__ == '__main__':
    out = {}
    with mp.get_context('fork').Pool(8) as pool:
        for name, (k, s) in VARIANTS.items():
            out[name] = build_variant(k, s, pool)
            print(name, len(out[name][0]), flush=True)
    pickle.dump(out, open('variants.pkl', 'wb'))
