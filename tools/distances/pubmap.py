import json, math, re, unicodedata
from load import PORTS, COORDS
P=json.load(open('pub151.json')); H=P['heads']; T=P['table']
ALIAS={"Piraeus":"Piraievs","Genoa":"Genova","Naples":"Napoli","Patras":"Patrai","Heraklion":"Iraklion","Lisbon":"Lisboa",
"Gothenburg":"Goteborg","Copenhagen":"Kobenhavn","Dunkirk":"Dunkerque","Venice":"Venezia","Latakia":"Al Latakia",
"Tripoli":"Tarabulus","Jeddah":"Jiddah","Chennai":"Madras","Mumbai (JNPT)":"Bombay","Nhava Sheva":"Bombay",
"Visakhapatnam":"Vishakhapatnam","St. Petersburg":"Sankt-Peterburg","Arkhangelsk":"Arkhangel'sk","Kolkata":"Calcutta",
"Hai Phong":"Haiphong","Keelung":"Chi-lung","Kaohsiung":"Kao-hsiung","Port Klang":"Port Kelang","Sokhna":"Ayn Sukhnah",
"Dammam":"Ad Damman","Ras Tanura":"Ra's Tannurah","Skikda":"Skikid","Vlore":"Vlores","Saint-Nazaire":"St. Nazaire",
"Fujairah":"Fujayrah","Salalah":"Mina Raysut","Chabahar":"Chah Bahar","Al Ahmadi":"Mina Al Ahmadi","Kuwait (Shuaiba)":"Mina Al Ahmadi",
"Ho Chi Minh (Cat Lai)":"Ho Chi Minh","Jakarta (Tanjung Priok)":"Jakarta","Busan":"Pusan","Yarimca":"Derince","Ceyhan":"Yumurtalik",
"Chornomorsk":"Il'ichevsk","Gemlik":"Gemlick","Fos-sur-Mer":"Port St. Louis Du Rhone","Houston (Bayport)":"Houston",
"Jeddah (Islamic Port)":"Jiddah","Jebel Ali (Dubai Port)":"Mina Jabal Ali","Jebel Ali":"Mina Jabal Ali","Dubai":"Dubayy",
"Felixstowe":"Felixstowe","Kwangyang":"Kwangyang","Tianjin":"Xingang","Rades":"Rades","Teesport":"Tees River","Immingham":"Immingham",
"Durres":"Durres","Tanjung Pelepas":"Tanjung Pelepas","Long Beach":"Long Beach","Oakland":"Oakland","Abu Dhabi":"Abu Dhabi",
"Damietta":"Dumyat","Bandar Abbas":"Bandar Abbas","Yuzhny":"Yuzhnyy","Port Elizabeth":"Port Elizabeth","Ust-Luga":"Ust'-Luga"}
def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r"[^a-z]","",s)
def city(p): return p.split(',')[0].strip()
names=set(H)|{n for v in T.values() for n in v}
bykey={}
for n in names: bykey.setdefault(norm(n.split(',')[0]),set()).add(n)
def hav(a,b):
    R=3440.065; p1,p2=map(math.radians,(a[0],b[0])); dl=math.radians(b[1]-a[1])
    x=math.sin((p2-p1)/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2; return 2*R*math.asin(math.sqrt(x))
PM={}; DEP={}
for p in PORTS:
    key=norm(ALIAS.get(city(p),city(p)))
    country=p.split(',')[-1].strip().lower()
    cands=[n for n in bykey.get(key,()) if not (len(n.split(','))>1 and n.split(',')[-1].strip().lower() in ('libya',) and country!='libya')]
    if cands: PM[p]=cands
    DEP[p]=[n for n in cands if n in H and hav(COORDS[p],H[n])<25]
def pub_dist(a,b):
    best=None
    for na in PM.get(a,()):
        for nb in PM.get(b,()):
            for x,y,dep in ((na,nb,a),(nb,na,b)):
                if x not in DEP.get(dep,()): continue
                d=T.get(x,{}).get(y)
                if d is not None: best=d if best is None else min(best,d)
    return best
if __name__=='__main__':
    miss=[p for p in PORTS if p not in PM]; print('unmapped',len(miss),miss)
