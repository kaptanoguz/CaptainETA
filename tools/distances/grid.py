import json, math, numpy as np
from PIL import Image, ImageDraw
RES_DEG = 1/60  # 1 arc-minute at equator, Mercator
def merc_y(lat): return math.log(math.tan(math.pi/4 + math.radians(lat)/2))
def inv_merc(y): return math.degrees(2*math.atan(math.exp(y)) - math.pi/2)
_land=None
def land_polys():
    global _land
    if _land is None:
        polys=[]
        for f in ['ne_10m_land.geojson','ne_10m_minor_islands.geojson']:
            for ft in json.load(open(f))['features']:
                g=ft['geometry']
                parts=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
                for p in parts: polys.append(np.array(p[0]))
        _land=polys
    return _land
class Grid:
    def __init__(s, lon0, lon1, lat0, lat1, res=RES_DEG):
        s.lon0,s.lon1,s.lat0,s.lat1,s.res=lon0,lon1,lat0,lat1,res
        s.r=math.radians(res)
        s.ytop=merc_y(lat1); s.ybot=merc_y(lat0)
        s.W=int(round((lon1-lon0)/res)); s.H=int(round((s.ytop-s.ybot)/s.r))
    def to_px(s, lon, lat):
        return ((lon-s.lon0)/s.res, (s.ytop-merc_y(lat))/s.r)
    def to_px_arr(s, lon, lat):
        lat=np.clip(lat,-85,85)
        return ((lon-s.lon0)/s.res, (s.ytop-np.log(np.tan(np.pi/4+np.radians(lat)/2)))/s.r)
    def to_ll(s, col, row):
        return (s.lon0+(col+0.5)*s.res, inv_merc(s.ytop-(row+0.5)*s.r))
    def rasterize(s, channels=()):
        img=Image.new('L',(s.W,s.H),0); d=ImageDraw.Draw(img)
        for p in land_polys():
            if p[:,0].max()<s.lon0-1 or p[:,0].min()>s.lon1+1 or p[:,1].max()<s.lat0-1 or p[:,1].min()>s.lat1+1: continue
            x,y=s.to_px_arr(p[:,0],p[:,1])
            d.polygon(list(zip(x.tolist(),y.tolist())),fill=1)
        for pts,wid in channels:
            xy=[s.to_px(lo,la) for lo,la in pts]
            d.line(xy,fill=0,width=wid)
            for x,y in xy: d.ellipse([x-wid/2,y-wid/2,x+wid/2,y+wid/2],fill=0)
        s.land=np.array(img,dtype=bool)
        return s.land
