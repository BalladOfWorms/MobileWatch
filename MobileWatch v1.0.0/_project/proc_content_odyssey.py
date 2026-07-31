import json, os
BASE=os.path.join(os.path.dirname(__file__),'..','app','src','main','assets')
MOBS=os.path.join(BASE,'mobs.json')
d=json.load(open(MOBS)); mobs=d['mobs']
def key(n): return n.lower()
def zname(x): return x[0] if isinstance(x,list) else x

sheolA=["Aegypius","Ailuros","Brachys","Cynara","Damysus","Dione","Eurytus","Gloios","Harpe","Kusarikku","Leucippe","Megaera","Physis","Ptelea","Salmandra","Tipuli"]
sheolB=["Akidu","Allergorhai","Apollinaris VII-II","Azdaha","Bendigeidfran","Bes","Chelamma","Chnubis","Count Malefis","Fleet-footed Lokberry","Fornax","Gandji","Gravehaunter","Ishum","Kuk","Langmeidong","Man-kheper-re","Maverick Maude","Nerites","Ptesan Wi","Shara","Simir","Spyrrsyon","Tabitjet","Taniwha","Tripix","Zacatzontli"]
sheolC=["Asena","Bygul","Chaos Steward","Dabbat al-Ard","Kurmajara","Lotanu","Wayra Tata"]
gaol={1:["Dealan-dhe","Sgili","U Bnai","Gogmagog"],
      2:["Aristaeus","Raskovniche","Marmorkrebs","Gigelorum","Procne","Henwen"],
      3:["Xevioso","Ngai","Kalunga","Ongo","Mboze","Arebati"],
      4:["Bumba"]}
# (name, family, level-range) for the 6 missing to CREATE
create={"Harpe":("Evil Weapon",[122,134],"Sheol A","Odyssey: Sheol A"),
        "Spyrrsyon":("Fomor",[127,137],"Sheol B","Odyssey: Sheol B"),
        "Asena":("Cerberus",[132,138],"Sheol C","Odyssey: Sheol C"),
        "Bygul":("Khimaira",[132,138],"Sheol C","Odyssey: Sheol C"),
        "Chaos Steward":("Dvergr",[132,138],"Sheol C","Odyssey: Sheol C"),
        "Wayra Tata":("Hydra",[132,138],"Sheol C","Odyssey: Sheol C")}
from collections import Counter
def famdet(fam):
    ms=[m for m in mobs.values() if m.get('fam')==fam]
    c=Counter(tuple(m['det']) for m in ms if isinstance(m.get('det'),list))
    return list(c.most_common(1)[0][0]) if c else []
def uniq(seq):
    out=[]
    for x in seq:
        if x not in out: out.append(x)
    return out

def add_zone(m,zone,lv=None):
    zs=m.setdefault('zones',[])
    if any(zname(x)==zone for x in zs): return
    zs.append([zone,str(lv)] if lv else zone)
def add_content(m,tag):
    ct=m.setdefault('content',[])
    if tag not in ct: ct.append(tag)
def apply_aggro(m):           # user rule: all Odyssey mobs aggro by family sense + Sight
    m['agg']=True
    det=m.get('det')
    if not isinstance(det,list): det=[] if det is None else [det]
    if 'Sight' not in det: det=det+['Sight']
    m['det']=uniq(det)

created=[]; tagged=[]
# create the 6 missing
for name,(fam,lv,zone,ct) in create.items():
    det=uniq(famdet(fam)+['Sight'])
    m={'n':name,'fam':fam,'lv':lv,'nm':True,'agg':True,'lnk':False,'det':det}
    mobs[key(name)]=m; created.append(name)
    add_zone(m,zone,lv[0]); add_content(m,ct)

def tag(names,zone,ct):
    for n in names:
        m=mobs.get(key(n))
        if m is None: continue     # created ones handled above
        if n in created: continue
        m['nm']=True
        apply_aggro(m)
        add_zone(m,zone); add_content(m,ct)
        tagged.append(n)

tag(sheolA,"Sheol A","Odyssey: Sheol A")
tag(sheolB,"Sheol B","Odyssey: Sheol B")
tag(sheolC,"Sheol C","Odyssey: Sheol C")
for atk,names in gaol.items():
    tag(names,"Sheol - Gaol",f"Odyssey: Sheol Gaol: Atonement {atk}")

bad=[k for m in mobs.values() for k,v in m.items() if v is None]
assert not bad, f"NULL {bad}"
json.dump(d,open(MOBS,'w'),separators=(', ',': '),ensure_ascii=False)
print("CREATED",created)
print("TAGGED",len(tagged),"existing NMs | total mobs",len(mobs))
odc=sum(1 for m in mobs.values() if any('Odyssey' in c for c in (m.get('content') or [])))
print("records now tagged Odyssey:",odc)
