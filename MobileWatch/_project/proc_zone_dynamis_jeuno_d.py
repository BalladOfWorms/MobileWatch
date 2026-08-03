import json, os
BASE=os.path.join(os.path.dirname(__file__),'..','app','src','main','assets')
MOBS=os.path.join(BASE,'mobs.json')
d=json.load(open(MOBS)); mobs=d['mobs']
Z="Dynamis-Jeuno [D]"; CT="Dynamis D: Dynamis-Jeuno [D]"
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
    ct=[c for c in (m.get('content') or []) if 'Jeuno' not in c]
    ct.append(f"{CT}: {role}" if role else CT); m['content']=ct
created=[]; tagged=[]; moved=[]
bases={'Berserker':'WAR / DRK','Fistfighter':'MNK / PUP','Vandal':'THF / DNC','Arcanomancer':'BLM / GEO',
'Defiler':'RDM / RUN','Banneret':'PLD / DRG','Animist':'BST / RNG','Vivifier':'WHM / SMN',
'Flautist':'BRD / SAM','Operative':'NIN / BLU','Buccaneer':'COR / SCH'}
def jj(p): return [j.strip() for j in p.split('/')]
def mk(name,lv,job,drops):
    m={'n':name,'fam':'Goblin','lv':[lv,lv],'agg':True,'lnk':True,'det':['Sight','Scent'],'crys':'Fire','job':job,'drops':drops}
    mobs[key(name)]=m; created.append(name); return m
for base,job in bases.items():
    j1,j2=jj(job)
    m=mk(f"Squadron {base}",127,job,f"Legshard: {j1}, Legshard: {j2}, Rusted I. Card"); add_zone(m,127); add_content_plain(m)
    m=mk(f"Regiment {base}",134,job,f"Voidleg: {j1}, Voidleg: {j2}, Black. I. Card"); add_zone(m,134); add_content_plain(m)
    m=mk(f"{base} Leader",129,job,f"Legshard: {j1}, Legshard: {j2}, Beastmen's Medal, Rusted I. Card"); add_zone(m,129); add_content_plain(m)
    m=mk(f"{base} Commander",137,job,f"Voidleg: {j1}, Voidleg: {j2}, Kindred's Medal, Black. I. Card"); add_zone(m,137); add_content_plain(m)
# statue
m={'n':'Impish Statue','fam':'Replica','lv':[127,127],'agg':True,'lnk':True,'det':['Sight']}
mobs[key('Impish Statue')]=m; created.append('Impish Statue'); add_zone(m,127); add_content_plain(m)
# new pets — NOTE: "Bird" is not a family in the file -> Squadron's Crow filed as Lesser Bird
for name,fam,lv in [("Squadron's Crow","Lesser Bird",127),("Regiment's Bats","Flock Bat",134),
                    ("Leader's Hippogryph","Hippogryph",129),("Commander's Hippogryph","Hippogryph",137)]:
    m={'n':name,'fam':fam,'lv':[lv,lv],'agg':True,'lnk':True,'det':['Sight']}
    mobs[key(name)]=m; created.append(name); add_zone(m,lv); add_content_plain(m)
# existing shared
z=json.load(open(os.path.join(BASE,'zoneinfo.json')))['dynamis_jeuno_d']
rl={r['n']:r['lv'] for r in z['nms']+z['mobs']}
BOSSES={"Impish Golem","Obstatrix","Disjoined Mithra","Disjoined Mithra ???"}
for name,lv in rl.items():
    if name in BOSSES or name in created: continue
    m=mobs.get(key(name))
    if m is None: continue
    add_zone(m,lv); add_content_plain(m); tagged.append(name)
a=mobs[key('Aurix')]; add_zone(a,''); add_content_plain(a); tagged.append('Aurix')
# bosses
ig=mobs[key('Impish Golem')]; ig['zones']=[[Z,'132']]; set_content_role(ig,'Midboss'); moved.append('Impish Golem')
ob=mobs[key('Obstatrix')]
ob.update({'fam':'Goblin','lv':[139,139],'agg':True,'lnk':True,'det':['Sight','Scent'],'crys':'Fire','job':'MNK',
  'spawn':'Zone Boss (defeat Impish Golem)',
  'drops':"Direct: Kindred's Medal, Black. I. Card, Volte Cap, Volte Jupon, Volte Bracers, Volte Hose, Volte Boots; Personal: Kindred's Medal, Black. I. Card"})
ob['zones']=[[Z,'139']]; set_content_role(ob,'Boss')
dm=mobs[key('Disjoined Mithra')]
dm.update({'fam':'Fomor','lv':[149,149],'agg':True,'lnk':True,'det':['Sound','Blood','JA'],'crys':'Dark',
  'spawn':'Disjoined Boss (defeat Obstatrix)',
  'drops':"Direct: Old I. Card, Demon's Medal; Personal: Old I. Card, Demon's Medal"})
dm['zones']=[[Z,'149']]; set_content_role(dm,'Disjoined')
dq=mobs[key('Disjoined Mithra ???')]; dq['fam']='Fomor'; add_zone(dq,''); set_content_role(dq,None)
if 'notes' not in dq: dq['notes']=['Spawns from any elemental "circle" fetters in wave 3.']
bad=[k for m in mobs.values() for k,v in m.items() if v is None]
assert not bad, f"NULL {bad}"
json.dump(d,open(MOBS,'w'),separators=(', ',': '),ensure_ascii=False)
print("CREATED",len(created),"| TAGGED",len(tagged),"| MOVED",moved,"| total mobs",len(mobs))
