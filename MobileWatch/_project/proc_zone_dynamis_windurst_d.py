import json, os
BASE=os.path.join(os.path.dirname(__file__),'..','app','src','main','assets')
MOBS=os.path.join(BASE,'mobs.json')
d=json.load(open(MOBS)); mobs=d['mobs']
Z="Dynamis-Windurst [D]"; CT="Dynamis D: Dynamis-Windurst [D]"
def key(n): return n.lower()
def zname(x): return x[0] if isinstance(x,list) else x
def add_zone(m,lv):
    zs=m.setdefault('zones',[])
    if any(zname(x)==Z for x in zs): return
    zs.append([Z,str(lv)] if lv else Z)
def add_content_plain(m):
    ct=m.setdefault('content',[])
    if CT not in ct: ct.append(CT)
def set_content_role(m,role):
    ct=[c for c in (m.get('content') or []) if 'Windurst' not in c]
    ct.append(f"{CT}: {role}" if role else CT); m['content']=ct
created=[]; tagged=[]; moved=[]
squad={'Hoplite':'WAR / DRK','Ascetic':'MNK / PUP','Ruffian':'THF / DNC','Magian':'BLM / GEO',
'Prognosticator':'RDM / RUN','Champion':'PLD / DRG','Empath':'BST / RNG','Orisha':'WHM / SMN',
'Minnesinger':'BRD / SAM','Spy':'NIN / BLU','Privateer':'COR / SCH'}
lead=dict(squad)  # Windurst Leader/Commander share the same base names as Squadron/Regiment
def jj(p): return [j.strip() for j in p.split('/')]
def mk(name,lv,job,drops):
    m={'n':name,'fam':'Yagudo','lv':[lv,lv],'agg':True,'lnk':True,'det':['Sight'],'crys':'Wind','job':job,'drops':drops}
    mobs[key(name)]=m; created.append(name); return m
for base,job in squad.items():
    j1,j2=jj(job)
    m=mk(f"Squadron {base}",127,job,f"Headshard: {j1}, Headshard: {j2}, Rusted I. Card"); add_zone(m,127); add_content_plain(m)
    m=mk(f"Regiment {base}",134,job,f"Voidhead: {j1}, Voidhead: {j2}, Black. I. Card"); add_zone(m,134); add_content_plain(m)
for base,job in lead.items():
    j1,j2=jj(job)
    m=mk(f"{base} Leader",129,job,f"Headshard: {j1}, Headshard: {j2}, Beastmen's Medal, Rusted I. Card"); add_zone(m,129); add_content_plain(m)
    m=mk(f"{base} Commander",137,job,f"Voidhead: {j1}, Voidhead: {j2}, Kindred's Medal, Black. I. Card"); add_zone(m,137); add_content_plain(m)
# statue
m={'n':'Incarnation Icon','fam':'Replica','lv':[127,127],'agg':True,'lnk':True,'det':['Sight']}
mobs[key('Incarnation Icon')]=m; created.append('Incarnation Icon'); add_zone(m,127); add_content_plain(m)
# new pets
for name,fam,lv in [("Squadron's Jagil","Pugil",127),("Regiment's Crab","Crab",134),("Leader's Kraken","Sea Monk",129),("Commander's Kraken","Sea Monk",137)]:
    m={'n':name,'fam':fam,'lv':[lv,lv],'agg':True,'lnk':True,'det':['Sight']}
    mobs[key(name)]=m; created.append(name); add_zone(m,lv); add_content_plain(m)
# existing shared: add zone+content
z=json.load(open(os.path.join(BASE,'zoneinfo.json')))['dynamis_windurst_d']
rl={r['n']:r['lv'] for r in z['nms']+z['mobs']}
BOSSES={"Evincing Idol","Fii Pexu the Eternal","Disjoined Tarutaru","Disjoined Tarutaru ???"}
for name,lv in rl.items():
    if name in BOSSES or name in created: continue
    m=mobs.get(key(name))
    if m is None: continue
    add_zone(m,lv); add_content_plain(m); tagged.append(name)
a=mobs[key('Aurix')]; add_zone(a,''); add_content_plain(a); tagged.append('Aurix')
# bosses
ev=mobs[key('Evincing Idol')]; ev['zones']=[[Z,'132']]; set_content_role(ev,'Midboss'); moved.append('Evincing Idol')
fp=mobs[key('Fii Pexu the Eternal')]
fp.update({'fam':'Yagudo','lv':[139,139],'agg':True,'lnk':True,'det':['Sight'],'crys':'Wind','job':'THF',
  'spawn':'Zone Boss (defeat Evincing Idol)',
  'drops':"Direct: Kindred's Medal, Black. I. Card, Volte Salade, Volte Haubert, Volte Moufles, Volte Brayettes, Volte Sollerets; Personal: Kindred's Medal, Black. I. Card"})
fp['zones']=[[Z,'139']]; set_content_role(fp,'Boss')
dt=mobs[key('Disjoined Tarutaru')]
dt.update({'fam':'Fomor','lv':[149,149],'agg':True,'lnk':True,'det':['Sound','Blood','JA'],'crys':'Dark',
  'spawn':'Disjoined Boss (defeat Fii Pexu the Eternal)',
  'drops':"Direct: Old I. Card, Demon's Medal; Personal: Old I. Card, Demon's Medal"})
dt['zones']=[[Z,'149']]; set_content_role(dt,'Disjoined')
dq=mobs[key('Disjoined Tarutaru ???')]; dq['fam']='Fomor'; add_zone(dq,''); set_content_role(dq,None)
if 'notes' not in dq: dq['notes']=['Spawns from any elemental "circle" fetters in wave 3.']
bad=[k for m in mobs.values() for k,v in m.items() if v is None]
assert not bad, f"NULL {bad}"
json.dump(d,open(MOBS,'w'),separators=(', ',': '),ensure_ascii=False)
print("CREATED",len(created),"| TAGGED",len(tagged),"| MOVED",moved,"| total mobs",len(mobs))
