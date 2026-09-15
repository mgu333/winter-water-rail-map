import json, re, urllib.request, urllib.parse, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
ROOT=Path(__file__).parent
old=ROOT.joinpath('index.html').read_text()
D=json.loads(old.split('const DATA=',1)[1].split(';\nconst svg=',1)[0]) if 'const DATA=' in old else json.loads(ROOT.joinpath('map-data.json').read_text())
for a in D['activities']:
    if a['id']==12:a.update(lat=36.6107663,lon=-121.8971465,place='Backscatter · 225 Cannery Row')
overrides={a['id']:a for a in json.loads(ROOT.joinpath('activity-picks.json').read_text())}
for a in D['activities']:
    a.update(overrides[a['id']])
assert len({a['kind'] for a in D['activities']}) == 100
def get(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url,timeout=60) as r:return json.load(r)
        except Exception:
            if attempt==2:raise
            time.sleep(2)
def decode(s):
    out=[];i=0;lat=lon=0
    while i<len(s):
        values=[]
        for _ in range(2):
            result=shift=0
            while True:
                b=ord(s[i])-63;i+=1;result|=(b&31)<<shift;shift+=5
                if b<32:break
            values.append(~(result>>1) if result&1 else result>>1)
        lat+=values[0];lon+=values[1];out.append([lat/1e6,lon/1e6])
    return out
home=[36.6149,-121.9049]; emy=[37.8405,-122.2917];truck=[39.328,-120.1833]
cache=ROOT/'route-cache.json'; C=json.loads(cache.read_text()) if cache.exists() else {}
def route(a,b,mode):
    key=json.dumps([a,b,mode])
    if key in C:return C[key]
    query={'locations':[{'lat':a[0],'lon':a[1]},{'lat':b[0],'lon':b[1]}],'costing':{'walk':'pedestrian','bike':'bicycle','drive':'auto'}[mode],'units':'miles'}
    raw=get('https://valhalla1.openstreetmap.de/route?json='+urllib.parse.quote(json.dumps(query)))
    trip=raw['trip'];r={'miles':trip['summary']['length'],'minutes':trip['summary']['time']/60,'coords':decode(trip['legs'][0]['shape']),'steps':[m['instruction'] for m in trip['legs'][0]['maneuvers']]}; C[key]=r;return r
jobs=[]
for a in D['activities']:
    if a.get('unlocated'):continue
    a['travel']={}
    for mode in ['walk','bike','drive']:jobs.append((a,mode,home,[a['lat'],a['lon']]))
regional=[]
for name,start,end in [('Home → Emeryville',home,emy),('Emeryville → Home',emy,home),('Emeryville → Truckee',emy,truck),('Truckee → Emeryville',truck,emy),('Home → Truckee · direct drive',home,truck),('Truckee → Home · direct drive',truck,home)]:
    r={'name':name,'travel':{}};regional.append(r);jobs.append((r,'drive',start,end))
with ThreadPoolExecutor(max_workers=2) as pool:
    futures={pool.submit(route,start,end,mode):(obj,mode) for obj,mode,start,end in jobs}
    for n,f in enumerate(as_completed(futures),1):
        obj,mode=futures[f]
        try:obj['travel'][mode]=f.result()
        except Exception as e:obj['travel'][mode]={'error':str(e)}
        cache.write_text(json.dumps(C));print(n,'/',len(jobs),obj['name'],mode,flush=True)
if D.get('rail'):
    D['regional']=regional
    ROOT.joinpath('map-data.json').write_text(json.dumps(D,separators=(',',':')))
    print('DONE: preserved previously verified railway, refreshed activity routes',flush=True)
    raise SystemExit(0)
base='https://services.arcgis.com/xOi1kZaI0eWDREZv/arcgis/rest/services/NTAD_Amtrak_Routes/FeatureServer/0/query?'
raw=get(base+urllib.parse.urlencode({'where':"name = 'California Zephyr'",'outFields':'*','outSR':4326,'f':'geojson'}))
lines=[]
for f in raw['features']:
    geo=f['geometry']; lines.extend(geo['coordinates'] if geo['type']=='MultiLineString' else [geo['coordinates']])
rail=[]
for line in lines:
    if not any(-122.5<p[0]<-120.17 and 37.7<p[1]<39.5 for p in line):continue
    # Trim the route at the closest vertices to the two stations.
    near=lambda p:min(range(len(line)),key=lambda i:(line[i][0]-p[1])**2+(line[i][1]-p[0])**2)
    i,j=near(emy),near(truck)
    if i!=j:
        seg=line[min(i,j):max(i,j)+1]
        if len(seg)>1:rail.append([[p[1],p[0]] for p in seg])
D['regional']=regional;D['rail']=rail
D['railSource']='https://data-usdot.opendata.arcgis.com/datasets/usdot::amtrak-routes/about'
D['railStops']=[['Emeryville',37.8405,-122.2917],['Richmond',37.9368,-122.3531],['Martinez',38.0193,-122.1387],['Davis',38.5429,-121.7377],['Sacramento',38.584,-121.5007],['Roseville',38.7501,-121.286],['Colfax',39.0994,-120.9533],['Truckee',39.328,-120.1833]]
ROOT.joinpath('map-data.json').write_text(json.dumps(D,separators=(',',':')))
print('DONE',len(rail),sum(len(x) for x in rail),'rail vertices',flush=True)
