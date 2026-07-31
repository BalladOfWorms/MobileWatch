import json
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']; fe=d['family_eco']
items={v.get('n') for v in json.load(open('ffxi_items.json')).values() if isinstance(v,dict) and v.get('n')}
def clr(o,*ks):
    for k in ks:
        if k in o: del o[k]

# ---------- ECO: classify ALL avatars as Avatar (USER) — revert the rev-109 Unclassified flip ----------
fe['Avatar']='Avatar'
fe['Siren']='Avatar'   # keep

# ---------- FOLD Odin + Cait Sith records into fam=Avatar ----------
for k in ['odin','odin (nm)','odin prime','cait sith','cait sith prime']:
    if k in m: m[k]['fam']='Avatar'   # cait sith ceithir already Avatar

# ---------- TITAN PRIME (grid already correct: A Earth / wk Wind / rest -95) ----------
ab['Earthen Fury']={"d":"Blood Pact: Rage. Titan's ultimate earth attack, dealing heavy damage in an area of effect.","t":"Magical","el":"Earth","tgt":"AoE","notes":"Once per battle. Partial hate reset on all targets hit."}
ab['Rock Throw']={"d":"Blood Pact: Rage. A ranged attack with an additional Slow effect.","tgt":"Single","fx":["Slow"]}
ab['Rock Buster']={"d":"Blood Pact: Rage. Blunt damage that inflicts Bind.","tgt":"Single","fx":["Bind"]}
ab['Megalith Throw']={"d":"Blood Pact: Rage. A stronger ranged attack with an additional Slow effect.","tgt":"Single","fx":["Slow"]}
ab['Earthen Ward']={"d":"Blood Pact: Ward. Grants a Stoneskin effect.","tgt":"Self","fx":["Stoneskin"]}
ab['Mountain Buster']={"d":"Blood Pact: Rage. Stronger blunt damage that inflicts Bind.","tgt":"Single","fx":["Bind"]}
ab['Geocrush']={"d":"Blood Pact: Rage. Earth damage that inflicts Stun and ignores shadows.","el":"Earth","tgt":"AoE","fx":["Stun"],"notes":"Ignores Utsusemi shadows."}
t=m['titan prime']; t['nm']=True; t['lv']=[20,85]
t['ab']=["Earthen Fury","Rock Throw","Rock Buster","Megalith Throw","Earthen Ward","Mountain Buster","Geocrush"]
t['sp']=["Quake II","Stone V","Stoneja"]
t['zones']=[["Cloister of Tremors","20-60"],["Full Moon Fountain","85"]]
t['notes']=[
 "Battlefield NM with a very large magic-aggro detection range and very high defense; level depends on the spawning quest \u2014 20 (Trial-Size Trial by Earth), 60 (Trial by Earth, Cloister of Tremors), 85 (Waking the Beast, Full Moon Fountain).",
 "Uses Earthen Fury once per battle (10 min into Trial by Earth, or ~50% HP in Waking the Beast; partial hate reset \u2014 save Provoke/Flash for right after). Geocrush ignores shadows. Has a natural Enstone effect that can out-damage his normal hits. Four Earth Elementals assist at lv85.",
]
# (no Titan portrait provided this pass -> img falls back to family icon)

# ---------- ODIN PRIME (Walk of Echoes, A Stygian Pact star) ----------
ab['Ofnir']={"d":"Deals damage with Defense Down and Magic Defense Down.","t":"Magical","el":"Dark","tgt":"AoE","fx":["Defense Down","Magic Defense Down"]}
ab['Valfodr']={"d":"Deals damage with Curse and Silence.","t":"Magical","el":"Dark","tgt":"AoE","fx":["Curse","Silence"]}
ab['Gagnrath']={"d":"Conal physical damage that inflicts Terror.","t":"Physical","tgt":"Conal","fx":["Terror"]}
ab['Geirrothr']={"d":"Area damage scaled by difficulty and divided among the players in range. Additional effect: Bind.","t":"Physical","tgt":"AoE","fx":["Bind"],"r":"20' radial"}
ab['Sanngetall']={"d":"Dispels all songs and rolls from targets in a 15' area of effect.","t":"Magical","el":"Dark","tgt":"AoE","fx":["Dispel"],"r":"15' radial"}
ab['Yggr']={"d":"Grants Odin an intimidation and attack boost effect.","t":"Buff","tgt":"Self"}
ab['Zantetsuken X']={"d":"Instantly K.O.s any target in a 20' area when Odin's attack exceeds a set ratio over their defense.","t":"Magical","el":"Dark","tgt":"AoE","r":"20' radial","notes":"Used at under 50% HP."}
ab['Zantetsuken Kai']={"d":"Conal critical damage of -95% HP.","t":"Magical","el":"Dark","tgt":"Conal","notes":"Difficult and Very Difficult only."}
o=m['odin prime']; o['nm']=True; o['job']='Black Mage / Dark Knight'   # lv[124,129] kept
o['st']=[["Breath","-50%"],["Ranged","-75%"],["Fire","-30%"],["Wind","-30%"],["Lightning","-30%"],["Light","-30%"],["Ice","-50%"],["Earth","-50%"],["Water","-50%"],["Dark","-50%"]]
clr(o,'wk','ab_el')
o['ab']=["Manafont","Ofnir","Valfodr","Gagnrath","Geirrothr","Sanngetall","Yggr","Zantetsuken Kai","Zantetsuken X"]
o['sp']=["Aspir","Absorb-Attri","Absorb-TP","Drain","Dread Spikes","Endark","Kaustra","Silencega"]
o['zones']=[["Walk of Echoes",None]]
o['img']="mobimages/odin prime.png"
odrops=[x for x in ["Geirrothr","Zantetsuken","Zantetsuken X","Hjarrandi Helm","Hjarrandi Breastplate","Freke Ring","Gere Ring"] if x in items]
o['drops']=", ".join(odrops)
o['notes']=[
 "Walk of Echoes battlefield NM (A Stygian Pact \u2605); the Stygian Pact phantom gem needs the quest The Rider Cometh. Job Black Mage / Dark Knight; susceptible to Silence (resistance grows steeply after 1-2 applications; trait Resist Silence). Uses Manafont.",
 "Carries the Divergence repeat-skill damage reduction: -10% \u2192 -25% \u2192 -60% \u2192 caps -85% when the SAME skill is used seven times (per skill, not reduced over time). Use five other abilities \u2014 or debuffs like slow/silence/dispel \u2014 to reset it.",
 "Zantetsuken X (under 50% HP) will K.O. players whose defense is far below Odin's attack: dispel the Yggr attack boost, apply Bio/Attack Down, and boost defense to survive. Zantetsuken Kai (Difficult/Very Difficult) deals -95% HP critical damage. Geirrothr damage is split among players in range; Geomancy effects are reduced by the chosen difficulty.",
]

# ---------- CAIT SITH (Champion of the Dawn, Walk of Echoes) ----------
ab['Divine Favor']={"d":"Removes status ailments from the caster.","tgt":"Self"}
c=m['cait sith']; c['nm']=True; c['job']='White Mage'; c['lv']=[75,75]
c['det']=["True Sound"]     # Image 6: A, T(H) = aggressive, True-hearing
c['ab']=["Divine Favor"]
c['sp']=["Holy"]
c['zones']=[["Walk of Echoes",None]]
c['img']="mobimages/cait sith.png"
c['notes']=[
 "Walk of Echoes NM, summoned during Champion of the Dawn. Aggressive; detects by sound (true-hearing). High magic defense, low physical defense; susceptible to Stun.",
 "Casts Tier V, -ja, and -ga IV elemental magic plus enfeebles (Blind, Slow, Sleep II); its Level ? Holy can be deadly. Uses Divine Favor to recover from status ailments.",
]

for v in m.values():
    for k in [k for k,val in list(v.items()) if val is None]:
        del v[k]
json.dump(d,open('mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print("written; abilities",len(ab),"| family_eco Avatar=",fe['Avatar'],"Siren=",fe['Siren'],"| Odin drops:",o.get('drops'))
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']
bad=[(k,kk) for k,v in m.items() for kk,vv in v.items() if vv is None]; print("None:",len(bad))
und=[a for k in ['titan prime','odin prime','cait sith'] for a in (m[k].get('ab') or []) if a not in ab]; print("undefined refs:",und)
print("Avatar members now:",sum(1 for v in m.values() if v.get('fam')=='Avatar'))
