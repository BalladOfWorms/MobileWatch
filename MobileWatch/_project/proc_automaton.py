import json
d=json.load(open('mobs.json'))
m=d['mobs']; ab=d['abilities']; fe=d['family_eco']

def clr(mob,*keys):
    for k in keys:
        if k in mob: del mob[k]

# ---------- ECO (USER: "automaton" / family box Type=Unclassified) ----------
fe['Automaton']='Unclassified'

# ---------- REAL MOBS ONLY (weaponskill category entries are NOT mobs — not in data, not created) ----------
FOLD=['elvaan automaton','galkan automaton','hume automaton','mithran automaton','tarutaru automaton',
      'carmine sentinel','cobalt sentinel','hazel sentinel','white sentinel','fantoccini automaton']
for k in FOLD:
    m[k]['fam']='Automaton'

members=[k for k,v in m.items() if v.get('fam')=='Automaton']
assert len(members)==14, members

# ---------- FAMILY GRID (Image 1: physical all 100 -> neutral; elements all 115 -> wk +15) ----------
GRID_WK=[["Fire","+15%"],["Wind","+15%"],["Lightning","+15%"],["Light","+15%"],["Ice","+15%"],["Earth","+15%"],["Water","+15%"],["Dark","+15%"]]
for k in members:
    v=m[k]
    v['wk']=[list(x) for x in GRID_WK]   # replaces galkan's +12.5 placeholder
    clr(v,'st')                          # clears tarutaru's junk physical -25 (box shows physical neutral)

# ---------- DETECTS: strip the bad [Sight,Sound,True Sight] import triple where pages show "?" ----------
for k in ['ob','valkeng','fantoccini automaton']:
    clr(m[k],'det')     # Ob/Valkeng pages show Detects "?"; family box blank -> leave unset
# troll's automaton [Sound] (page-confirmed), sentinels [Sound], osschaart's [Sound], race automatons [Sight] KEPT

# ---------- CRYS/JOB: family box blank -> no stamp (ob/valkeng keep crys 'N') ----------

# ---------- ZONES ----------
def zset(k,pairs): m[k]['zones']=[[z,lv] for z,lv in pairs]
zset('ob',[["Alzadaal Undersea Ruins","78-80"]])
zset("osschaart's automaton",[["Waughroon Shrine","60"]])
zset('valkeng',[["Talacca Cove","60"],["Navukgo Execution Chamber","60"]])
zset("troll's automaton",[["Al Zahbi","69-79"],["Bhaflau Thickets","69-79"],["Halvung","69-79"],["Mount Zhayolm","69-79"]])
for k in ['elvaan automaton','galkan automaton','hume automaton','mithran automaton','tarutaru automaton']:
    zset(k,[["Mine Shaft 2716","60"]])
for k in ['carmine sentinel','cobalt sentinel','hazel sentinel','white sentinel']:
    zset(k,[["Al Zahbi","68-84"]])
zset('fantoccini automaton',[["Mine Shaft 2716","49"]])

# ---------- NOTES ----------
m['ob']['notes']=["Trade a Cog Lubricant to the ??? at (G-7) in Alzadaal Undersea Ruins to spawn (teleporter at H-9)."]
m["osschaart's automaton"]['notes']=["Assists Osschaart, who is spawned by the KSNM Copycat."]
m['valkeng']['notes']=["Battlefield NM: Puppetmaster Blues (Talacca Cove) and Achieving True Power (Navukgo Execution Chamber)."]
m["troll's automaton"]['notes']=["Summoned by Trolls. Steal: Automaton Oil +2."]
# Ob drops already validated (all 16 exact in item DB) -> unchanged. No family kit (enemy pages show no
# abilities; the family "abilities" table lists frame-gated PLAYER-automaton weaponskills, not mob TP moves).

# ---------- null-poison guard ----------
for v in m.values():
    for k in [k for k,val in list(v.items()) if val is None]:
        del v[k]

json.dump(d,open('mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print("written")

# ---------- VERIFY ----------
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']
print("mobs",len(m),"abilities",len(ab),"family_eco",len(d['family_eco']),"family_notes",len(d['family_notes']),"resist_sets",len(d['family_resist_sets']),"subtypes",len(d['family_subtypes']))
mem=[k for k,v in m.items() if v.get('fam')=='Automaton']
print("Automaton members (%d):"%len(mem),"| eco:",d['family_eco'].get('Automaton'))
bad=[(k,kk) for k,v in m.items() for kk,vv in v.items() if vv is None]; print("top-level None values:",len(bad))
und=[a for k,v in m.items() if v.get('fam')=='Automaton' for a in (v.get('ab') or []) if a not in ab]; print("family undefined refs:",und)
for k in ['ob','valkeng',"troll's automaton",'tarutaru automaton','galkan automaton','carmine sentinel','fantoccini automaton']:
    v=m[k]; print(f"  {k}: nm={v.get('nm')} det={v.get('det')} crys={v.get('crys')!r} wk={'set' if v.get('wk') else None} st={v.get('st')} zones={v.get('zones')}")
