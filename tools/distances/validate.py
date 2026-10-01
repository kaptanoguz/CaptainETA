import pickle, statistics
from load import PORTS, COORDS
from pubmap import PM, DEP, T, hav
import sys
V=pickle.load(open('variants.pkl','rb')); D,SRC=V[sys.argv[1] if len(sys.argv)>1 else 'base']
def one(x_port,y_port):
    best=None
    for na in DEP.get(x_port,()):
        for nb in PM.get(y_port,()):
            d=T.get(na,{}).get(nb)
            if d: best=d if best is None else min(best,d)
    return best
rows=[]
for k,d in D.items():
    a,b=k; p1=one(a,b); p2=one(b,a)
    if p1 and p2 and abs(p1-p2)<=max(3,0.03*p1):
        p=(p1+p2)/2
        if p>=hav(COORDS[a],COORDS[b])*0.98: rows.append((k,d,p,(d-p)/p,SRC[k]))
def stats(rs,label):
    if not rs: print(label,'none'); return
    e=[r[3] for r in rs]; ae=sorted(abs(x) for x in e); an=sorted(abs(r[1]-r[2]) for r in rs)
    print(f"{label:20} n={len(rs):4}  bias {statistics.median(e)*100:+.1f}%  median |err| {statistics.median(ae)*100:.1f}% ({statistics.median(an):.0f} nm)  p90 {ae[int(len(ae)*.9)]*100:.1f}%  max {ae[-1]*100:.0f}%  within 5%: {sum(x<.05 for x in ae)/len(ae)*100:.0f}%")
stats(rows,'all trusted pairs')
stats([r for r in rows if r[4]=='grid'],'grid (regional)')
stats([r for r in rows if r[4]=='searoute'],'searoute (cross)')
stats([r for r in rows if r[4]=='gateway'],'gateway (EUR-ocean)')
stats([r for r in rows if r[2]<200],'legs < 200 nm')
stats([r for r in rows if 200<=r[2]<1000],'legs 200-1000 nm')
stats([r for r in rows if r[2]>=1000],'legs > 1000 nm')
print()
for k,d,p,e,s in sorted(rows,key=lambda r:-abs(r[3]))[:25]:
    print(f"  {k[0][:24]:24} {k[1][:24]:24} calc {d:6.0f}  pub {p:6.0f}  {e*100:+5.1f}%  {s}")
