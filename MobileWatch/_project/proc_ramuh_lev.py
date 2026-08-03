import json
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']

# ---------- CREATE the 4 blood pacts (iconic ultimates -> element certain) ----------
ab['Judgment Bolt']={"d":"Blood Pact: Rage. Ramuh's ultimate lightning attack, dealing heavy damage to enemies in an area of effect.","t":"Magical","el":"Lightning","tgt":"AoE","notes":"Partial hate reset on all targets hit."}
ab['Thunderstorm']={"d":"Blood Pact: Rage. A lightning-based attack that ignores shadows.","el":"Lightning","tgt":"AoE","notes":"Ignores Utsusemi shadows."}
ab['Tidal Wave']={"d":"Blood Pact: Rage. Leviathan's ultimate water attack, dealing heavy damage to enemies in an area of effect.","t":"Magical","el":"Water","tgt":"AoE","notes":"Partial hate reset on all targets hit."}
ab['Grand Fall']={"d":"Blood Pact: Rage. A water-based attack that ignores shadows.","el":"Water","tgt":"Single","notes":"Ignores Utsusemi shadows."}

# ---------- RAMUH PRIME (grid already correct: A Lightning / wk Earth / rest -95, page-validated) ----------
r=m['ramuh prime']; r['nm']=True; r['lv']=[20,85]
r['ab']=["Judgment Bolt","Thunderstorm"]
r['sp']=["Burst II","Thunder V","Thundaja"]
r['zones']=[["Cloister of Storms","20-60"],["Full Moon Fountain","85"]]
r['img']="mobimages/ramuh prime.png"
r['notes']=[
 "Battlefield NM with a very large magic-aggro detection range; level depends on the spawning quest \u2014 20 (Trial-Size Trial by Lightning), 60 (Trial by Lightning, Cloister of Storms), 85 (Waking the Beast, Full Moon Fountain).",
 "Uses Judgment Bolt 10 minutes into Trial by Lightning, or at ~50% HP in Waking the Beast (partial hate reset on everyone it hits \u2014 save Provoke/Flash for right after). Thunderstorm ignores shadows.",
 "\u2605 version (Trial by Lightning \u2605): casts Burst II/Thunder V/Thundaja; resistances shift to -30% physical/magical/breath.",
]

# ---------- LEVIATHAN PRIME (grid already correct: A Water / wk Lightning / rest -95, page-validated) ----------
l=m['leviathan prime']; l['nm']=True; l['lv']=[20,85]
l['ab']=["Tidal Wave","Grand Fall"]
l['sp']=["Flood II","Water V","Waterja"]
l['zones']=[["Cloister of Tides","20-60"],["Full Moon Fountain","85"]]
l['img']="mobimages/leviathan prime.png"
l['notes']=[
 "Battlefield NM with a very large magic-aggro detection range; level depends on the spawning quest \u2014 20 (Trial-Size Trial by Water), 60 (Trial by Water, Cloister of Tides), 85 (Waking the Beast, Full Moon Fountain).",
 "Uses Tidal Wave 10 minutes into Trial by Water, or at ~50% HP in Waking the Beast (partial hate reset on everyone it hits \u2014 save Provoke/Flash for right after). Grand Fall ignores shadows.",
 "\u2605 version (Trial by Water \u2605): casts Flood II/Water V/Waterja; resistances shift to -30% physical/magical/breath.",
]

for v in m.values():
    for k in [k for k,val in list(v.items()) if val is None]:
        del v[k]
json.dump(d,open('mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print("written; abilities",len(ab))
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']
bad=[(k,kk) for k,v in m.items() for kk,vv in v.items() if vv is None]; print("None:",len(bad))
und=[a for k in ['ramuh prime','leviathan prime'] for a in (m[k].get('ab') or []) if a not in ab]; print("undefined refs:",und)
for k in ['ramuh prime','leviathan prime']:
    v=m[k]; print(f"  {k}: nm={v.get('nm')} img={v.get('img')!r} ab_el={v.get('ab_el')} wk={v.get('wk')} zones={v.get('zones')} sp={v.get('sp')}")
