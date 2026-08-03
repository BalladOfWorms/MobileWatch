import json
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']; fe=d['family_eco']
def clr(o,*ks):
    for k in ks:
        if k in o: del o[k]

# ---------- FLIP eco: 4/4 individual avatar pages (Alexander/Carbuncle/Diabolos/Fenrir) say Type=Unclassified ----------
fe['Avatar']='Unclassified'

# ---------- CREATE the 3 named blood pacts (pages name them but don't show type/element -> leave t/el unset) ----------
ab['Ruinous Omen']={"d":"Blood Pact: Rage. Halves the current HP of enemies in an area of effect.","tgt":"AoE","notes":"Partial hate reset on all targets hit."}
ab['Howling Moon']={"d":"Blood Pact: Rage. A dark-based area attack.","tgt":"AoE","notes":"Partial hate reset on all targets hit (used by the \u2605 version)."}
ab['Lunar Roar']={"d":"Removes up to six beneficial effects from the target.","tgt":"AoE","fx":["Dispel"]}

# ---------- DIABOLOS PRIME (The Shrouded Maw, Waking Dreams) ----------
dp=m['diabolos prime']; dp['nm']=True
dp['st']=[["Fire","-15%"],["Wind","-15%"],["Lightning","-15%"],["Ice","-15%"],["Earth","-15%"],["Water","-15%"],["Dark","-50%"]]  # Light 100 neutral (not recorded)
clr(dp,'wk','ab_el')
dp['ab']=["Ruinous Omen"]
dp['zones']=[["The Shrouded Maw",None]]
dp['img']="mobimages/diabolos prime.png"
dp['notes']=[
 "Waking Dreams battlefield NM (The Shrouded Maw); much higher level here than in Promathia Mission 4-1. Resists Stun. Occasionally uses Ruinous Omen (partial hate reset on everyone it hits). Title: Devil's Demise (VD only).",
 "\u2605 version: resistances shift to ABSORB Dark, resist all other elements ~70% (Light neutral), and take -30% physical/magical/breath.",
]

# ---------- FENRIR PRIME (Full Moon Fountain, The Moonlit Path) ----------
fp=m['fenrir prime']; fp['nm']=True
fp['st']=[["Fire","-40%"],["Wind","-40%"],["Lightning","-40%"],["Ice","-40%"],["Earth","-40%"],["Water","-40%"],["Dark","-95%"]]
fp['wk']=[["Light","+30%"]]
clr(fp,'ab_el')
fp['ab']=["Howling Moon","Lunar Roar"]
fp['zones']=[["Full Moon Fountain","80"]]
fp['img']="mobimages/fenrir prime.png"
fp['notes']=[
 "The Moonlit Path battlefield NM (Full Moon Fountain). Uses Howling Moon at ~50% HP; Lunar Roar removes up to six player buffs. Title: Lupine Liquidator (VD only).",
 "\u2605 version: occasionally uses Howling Moon (partial hate reset on everyone it hits); resistances shift to ABSORB Dark, resist all other elements ~70% (Light neutral), and take -30% physical/magical/breath.",
]

for v in m.values():
    for k in [k for k,val in list(v.items()) if val is None]:
        del v[k]
json.dump(d,open('mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print("written")
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']
print("abilities",len(ab),"| family_eco[Avatar]=",d['family_eco']['Avatar'])
bad=[(k,kk) for k,v in m.items() for kk,vv in v.items() if vv is None]; print("None values:",len(bad))
und=[a for k in ['diabolos prime','fenrir prime'] for a in (m[k].get('ab') or []) if a not in ab]; print("undefined refs:",und)
for k in ['diabolos prime','fenrir prime']:
    v=m[k]; print(f"  {k}: nm={v.get('nm')} img={v.get('img')!r} wk={v.get('wk')} st={v.get('st')} ab={v.get('ab')} zones={v.get('zones')}")
