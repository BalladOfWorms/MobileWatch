import json, os
BASE=os.path.join(os.path.dirname(__file__),'..','app','src','main','assets')
MOBS=os.path.join(BASE,'mobs.json')
d=json.load(open(MOBS))
mobs=d['mobs']
Z="Dynamis-Bastok [D]"
CT="Dynamis D: Dynamis-Bastok [D]"

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
    # drop any Dynamis-Bastok content (classic or D) then set the roled tag
    ct=[c for c in (m.get('content') or []) if 'Bastok' not in c]
    ct.append(f"{CT}: {role}" if role else CT)
    m['content']=ct

created=[]; tagged=[]; moved=[]

# ---- job pairs (Quadav) ----
squad={'Weaponmaster':'WAR / DRK','Combatant':'MNK / PUP','Trickster':'THF / DNC','Magister':'BLM / GEO',
'Magician':'RDM / RUN','Cavalier':'PLD / DRG','Harnesser':'BST / RNG','Mender':'WHM / SMN',
'Balladeer':'BRD / SAM','Shadowstalker':'NIN / BLU','Scallywag':'COR / SCH'}
lead={'Fighter':'WAR / DRK','Brother':'MNK / PUP','Pickpocket':'THF / DNC','Magus':'BLM / GEO',
'Shaman':'RDM / RUN','Chevalier':'PLD / DRG','Domesticator':'BST / RNG','Healer':'WHM / SMN',
'Joculator':'BRD / SAM','Assassin':'NIN / BLU','Freebooter':'COR / SCH'}
def jj(pair): return [j.strip() for j in pair.split('/')]

def mk_quadav(name,lv,job,drops):
    m={'n':name,'fam':'Quadav','lv':[lv,lv],'agg':True,'lnk':True,'det':['Sound'],
       'crys':'Water','job':job,'drops':drops}
    mobs[key(name)]=m; created.append(name); return m

# Squadron(127)/Regiment(134)
for base,job in squad.items():
    j1,j2=jj(job)
    m=mk_quadav(f"Squadron {base}",127,job,f"Handshard: {j1}, Handshard: {j2}, Rusted I. Card")
    add_zone(m,127); add_content_plain(m)
    m=mk_quadav(f"Regiment {base}",134,job,f"Voidhand: {j1}, Voidhand: {j2}, Black. I. Card")
    add_zone(m,134); add_content_plain(m)
# Leader(129)/Commander(137)
for base,job in lead.items():
    j1,j2=jj(job)
    m=mk_quadav(f"{base} Leader",129,job,f"Handshard: {j1}, Handshard: {j2}, Beastmen's Medal, Rusted I. Card")
    add_zone(m,129); add_content_plain(m)
    m=mk_quadav(f"{base} Commander",137,job,f"Voidhand: {j1}, Voidhand: {j2}, Kindred's Medal, Black. I. Card")
    add_zone(m,137); add_content_plain(m)

# ---- statue ----
if key('Lithicthrower Image') not in mobs:
    m={'n':'Lithicthrower Image','fam':'Replica','lv':[127,127],'agg':True,'lnk':True,'det':['Sight']}
    mobs[key('Lithicthrower Image')]=m; created.append('Lithicthrower Image')
    add_zone(m,127); add_content_plain(m)

# ---- new pets (Bastok-specific) ----
newpets=[("Squadron's Wasp","Bee",127),("Regiment's Fly","Fly",134),
         ("Leader's Gnat","Gnat",129),("Commander's Gnat","Gnat",137),("Volte's Bomb","Bomb",142)]
for name,fam,lv in newpets:
    m={'n':name,'fam':fam,'lv':[lv,lv],'agg':True,'lnk':True,'det':['Sight']}
    mobs[key(name)]=m; created.append(name)
    add_zone(m,lv); add_content_plain(m)

# ---- existing shared pets + Volte block: add zone+content (plain) ----
z=json.load(open(os.path.join(BASE,'zoneinfo.json')))['dynamis_bastok_d']
roster_lv={r['n']:r['lv'] for r in z['nms']+z['mobs']}
BOSSES={"Mu'Sha Effigy","Ka'Rho Fearsinger","Disjoined Galka","Disjoined Galka ???"}
for name,lv in roster_lv.items():
    if name in BOSSES: continue
    k=key(name); m=mobs.get(k)
    if m is None: continue           # was created above (already zoned)
    if name in created: continue
    add_zone(m,lv); add_content_plain(m); tagged.append(name)

# ---- Aurix (shared NM, level-less) ----
a=mobs[key('Aurix')]; add_zone(a,''); add_content_plain(a); tagged.append('Aurix')
# Elemental Circle (level-less) already handled by loop (lv='')

# ---- bosses ----
# Mu'Sha Effigy: MOVE from classic Dynamis-Bastok -> Bastok [D] Midboss
me=mobs[key("Mu'Sha Effigy")]
me['zones']=[[Z,'132']]
set_content_role(me,'Midboss'); moved.append("Mu'Sha Effigy")
# Ka'Rho Fearsinger: zone boss (mirror Halphas: nm absent)
kr=mobs[key("Ka'Rho Fearsinger")]
kr.update({'fam':'Quadav','lv':[139,139],'agg':True,'lnk':True,'det':['Sound'],'crys':'Water','job':'MNK',
   'spawn':"Zone Boss (defeat Mu'Sha Effigy)",
   'drops':"Direct: Kindred's Medal, Black. I. Card, Volte Tiara, Volte Harness, Volte Mittens, Volte Tights, Volte Spats; Personal: Kindred's Medal, Black. I. Card"})
kr['zones']=[[Z,'139']]; set_content_role(kr,'Boss')
# Disjoined Galka: disjoined boss (mirror Disjoined Elvaan)
dg=mobs[key('Disjoined Galka')]
dg.update({'fam':'Fomor','lv':[149,149],'agg':True,'lnk':True,'det':['Sound','Blood','JA'],'crys':'Dark',
   'spawn':"Disjoined Boss (defeat Ka'Rho Fearsinger)",
   'drops':"Direct: Old I. Card, Demon's Medal; Personal: Old I. Card, Demon's Medal"})
dg['zones']=[[Z,'149']]; set_content_role(dg,'Disjoined')
# Disjoined Galka ??? : fetter-spawn variant (mirror Disjoined Elvaan ??? : plain, level-less, nm absent)
dq=mobs[key('Disjoined Galka ???')]
dq['fam']='Fomor'; add_zone(dq,''); set_content_role(dq,None)
if 'notes' not in dq: dq['notes']=['Spawns from any elemental "circle" fetters in wave 3.']

# ---- guard: no None values ----
bad=[k for m in mobs.values() for k,v in m.items() if v is None]
assert not bad, f"NULL VALUES: {bad}"

json.dump(d,open(MOBS,'w'),separators=(', ',': '),ensure_ascii=False)
print("CREATED",len(created)); print("TAGGED (existing shared)",len(tagged)); print("MOVED",moved)
print("total mobs now",len(mobs))
