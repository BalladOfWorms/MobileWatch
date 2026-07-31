import json
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']
ELEMS=["Fire","Wind","Lightning","Light","Ice","Earth","Water","Dark"]
def absorb_grid(own,weak):
    return [own], [[weak,"+50%"]], [[e,"-95%"] for e in ELEMS if e not in (own,weak)]

# ---------- CORRECT the rev-107 wheel-weakness error (avatars are weak to the element that BEATS them) ----------
# ifrit=Fire wk Water; garuda=Wind wk Ice; ramuh=Lightning wk Earth  (shiva/titan/leviathan were already right)
for k,(own,weak) in {'ifrit prime':('Fire','Water'),'garuda prime':('Wind','Ice'),'ramuh prime':('Lightning','Earth')}.items():
    ae,wk,st=absorb_grid(own,weak); m[k]['ab_el']=ae; m[k]['wk']=wk; m[k]['st']=st

# ---------- CREATE the 4 signature blood pacts (iconic ultimates -> element certain) ----------
ab['Aerial Blast']={"d":"Blood Pact: Rage. Garuda's ultimate wind attack, dealing heavy damage to enemies in an area of effect.","t":"Magical","el":"Wind","tgt":"AoE","notes":"Partial hate reset on all targets hit."}
ab['Wind Blade']={"d":"Blood Pact: Rage. A wind-based ranged attack that ignores shadows.","el":"Wind","tgt":"Single","notes":"Ignores Utsusemi shadows."}
ab['Inferno']={"d":"Blood Pact: Rage. Ifrit's ultimate fire attack, dealing heavy damage to enemies in an area of effect.","t":"Magical","el":"Fire","tgt":"AoE","notes":"Partial hate reset on all targets hit."}
ab['Meteor Strike']={"d":"Blood Pact: Rage. A fire-based attack that ignores shadows.","el":"Fire","tgt":"Single","notes":"Ignores Utsusemi shadows."}

# ---------- GARUDA PRIME ----------
g=m['garuda prime']; g['nm']=True; g['lv']=[20,85]
g['ab']=["Aerial Blast","Wind Blade"]
g['sp']=["Silencega","Tornado II","Aero V","Aeroja"]
g['zones']=[["Cloister of Gales","20-60"],["Full Moon Fountain","85"]]
g['img']="mobimages/garuda prime.png"
g['notes']=[
 "Battlefield NM with a very large magic-aggro detection range; level depends on the spawning quest \u2014 20 (Trial-Size Trial by Wind), 60 (Trial by Wind, Cloister of Gales), 85 (Waking the Beast, Full Moon Fountain).",
 "Uses Aerial Blast 10 minutes into Trial by Wind, or at ~50% HP in Waking the Beast (partial hate reset on everyone it hits \u2014 save Provoke/Flash for right after). Wind Blade ignores shadows and is a ranged attack.",
 "\u2605 version (Trial by Wind \u2605): casts Silencega/Tornado II/Aero V/Aeroja; resistances shift to -30% physical/magical/breath and ~-70% off-elements.",
]

# ---------- IFRIT PRIME ----------
i=m['ifrit prime']; i['nm']=True; i['lv']=[20,85]
i['ab']=["Inferno","Meteor Strike"]
i['sp']=["Flare II","Fire V","Firaja"]
i['zones']=[["Cloister of Flames","20-60"],["Full Moon Fountain","85"]]
i['img']="mobimages/ifrit prime.png"
i['notes']=[
 "Battlefield NM with a very large magic-aggro detection range; level depends on the spawning quest \u2014 20 (Trial-Size Trial by Fire), 60 (Trial by Fire, Cloister of Flames), 85 (Waking the Beast, Full Moon Fountain).",
 "Uses Inferno 10 minutes into Trial by Fire, or at ~50% HP in Waking the Beast (partial hate reset \u2014 save Provoke/Flash for right after). Meteor Strike ignores shadows.",
 "\u2605 version (Trial by Fire \u2605): casts Flare II/Fire V/Firaja; resistances shift to -30% physical/magical/breath and ~-70% off-elements.",
]

for v in m.values():
    for k in [k for k,val in list(v.items()) if val is None]:
        del v[k]
json.dump(d,open('mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print("written; abilities",len(ab))
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']
bad=[(k,kk) for k,v in m.items() for kk,vv in v.items() if vv is None]; print("None:",len(bad))
und=[a for k in ['garuda prime','ifrit prime'] for a in (m[k].get('ab') or []) if a not in ab]; print("undefined refs:",und)
for k in ['ifrit prime','garuda prime','ramuh prime']:
    v=m[k]; print(f"  {k}: ab_el={v.get('ab_el')} wk={v.get('wk')} img={v.get('img')!r} zones={v.get('zones')} sp={v.get('sp')}")
