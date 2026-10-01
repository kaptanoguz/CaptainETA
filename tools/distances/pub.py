import re, json
L=[l.strip() for l in open('raw.txt',encoding='utf-8')]
coord=re.compile(r'^\((\d+)˚(\d+)\'(\d+)"([NS])\.,\s*(\d+)˚(\d+)\'(\d+)"([EW])\.\)\s*to:')
def dms(d,m,s,h): v=int(d)+int(m)/60+int(s)/3600; return -v if h in 'SW' else v
heads={}; table={}; cur=None; buf=''
for i,l in enumerate(L):
    m=coord.match(l)
    if m and i>0 and L[i-1].isupper():
        k=i-1; parts=[]
        while k>=0 and L[k] and L[k].isupper() and len(parts)<3 and L[k] not in ('PORTS',):
            parts.insert(0,L[k]); k-=1
        cur=' '.join(parts).replace('*','').title().replace(' ,',','); heads[cur]=(dms(*m.group(1,2,3,4)),dms(*m.group(5,6,7,8))); table.setdefault(cur,{}); buf=''; continue
    if cur is None or not l or l in('Ports','Junction Points*') or l.isupper(): 
        if l.isupper(): buf=''
        continue
    buf=(buf+' '+l).strip()
    mm=re.match(r'^(.*?),\s*([\d,]+)$',buf)
    if mm:
        name=mm.group(1); d=int(mm.group(2).replace(',',''))
        if 'Corinth' not in name:
            base=re.sub(r'\s*\(.*\)\s*$','',name).strip()
            table[cur][base]=min(d,table[cur].get(base,1e9))
        buf=''
    elif len(buf)>120: buf=''
json.dump(dict(heads=heads,table=table),open('pub151.json','w'))
print(len(heads), sum(len(v) for v in table.values()))
print(table.get('Istanbul, Turkey',{}).get('Piraievs, Greece'), list(heads.items())[:3])
