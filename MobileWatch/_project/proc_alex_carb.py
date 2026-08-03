import json
d=json.load(open('mobs.json'))
m=d['mobs']; ab=d['abilities']
def clr(o,*ks):
    for k in ks:
        if k in o: del o[k]

# ---------- CREATE Alexander's 7 abilities ----------
ab['Divine Judgment']={"d":"Deals damage, then applies a full dispel and full MP removal.","t":"Magical","tgt":"AoE","r":"20' radial","fx":["Dispel"]}
ab['Divine Spear']={"d":"Deals damage with Petrify, Attack Down (-50%), and Magic Attack Down.","t":"Magical","tgt":"Conal","fx":["Petrify","Attack Down","Magic Attack Down"]}
ab['Gospel of the Lost']={"d":"Recovers HP, removes all debuffs, and grants a powerful, unremovable Stoneskin.","t":"Buff","tgt":"Self","notes":"Used in response to any debuff being applied."}
ab['Perfect Defense']={"d":"Grants complete damage immunity for 30 seconds.","t":"Buff","tgt":"Self","notes":"Triggered by receiving five skillchains; may also follow every third Gospel of the Lost."}
ab['Mega Holy']={"d":"Deals damage to both HP and MP in an area of effect.","t":"Magical","tgt":"AoE"}
ab['Radiant Sacrament']={"d":"Deals damage with Silence, Defense Down (-50%), and Magic Defense Down.","t":"Physical","tgt":"AoE","fx":["Silence","Defense Down","Magic Defense Down"]}
ab['Void of Repentance']={"d":"Inflicts Stun, Accuracy Down (-100), and Magic Accuracy Down.","t":"Magical","tgt":"AoE","fx":["Stun","Accuracy Down","Magic Accuracy Down"],"notes":"Used after any skillchain is performed."}
# ---------- CREATE Carbuncle's 2 missing blood pacts ----------
ab['Meteorite']={"d":"Blood Pact: Rage. Deals area damage.","tgt":"AoE"}
ab['Holy Mist']={"d":"Blood Pact: Rage. A light-based attack that also lowers the target's Defense.","el":"Light","tgt":"Single","fx":["Defense Down"],"notes":"Carbuncle Prime \u2605 uses an AoE version."}

# ---------- ALEXANDER PRIME (Divine Interference \u2605, Walk of Echoes) ----------
a=m['alexander prime']
a['nm']=True
a['st']=[["Light","-95%"],["Fire","-60%"],["Wind","-60%"],["Lightning","-60%"],["Ice","-60%"],["Earth","-60%"],["Water","-60%"],["Dark","-60%"]]
clr(a,'wk','ab_el')
a['ab']=["Divine Judgment","Divine Spear","Gospel of the Lost","Perfect Defense","Mega Holy","Radiant Sacrament","Void of Repentance"]
a['sp']=[]                              # explicit: "Alexander casts no spells"
a['zones']=[["Walk of Echoes",None]]
a['img']="mobimages/alexander prime.png"
a['drops']="Sacro Breastplate, Sacro Gorget, Sacro Cord, Sacro Mantle, Sacro Bulwark"
a['notes']=[
 "Divine Interference \u2605 battlefield NM (Walk of Echoes); the Divine phantom gem drops after the quest Waking the Colossus. Casts no spells and takes no damage from behind. Title: Alexander Annihilator (HP ~750k N / ~900k D / ~1.4M VD).",
 "Gospel of the Lost fires in response to ANY debuff \u2014 including Samba, Bully, Angon, and weaponskill effects like Stardiver/Rudra's Storm. At higher difficulty it is also used at set HP% (90% and 30%, sometimes 70% on slow kills) alongside Divine Judgement.",
 "Skillchain damage triggers Void of Repentance; repeated skillchains trigger Perfect Defense (30s damage immunity).",
]

# ---------- CARBUNCLE PRIME (Waking the Beast, Full Moon Fountain) ----------
c=m['carbuncle prime']
# base grid: Light resist -95, Dark weak; other elements "?" (not recorded). Base RESISTS Light (not absorb).
c['st']=[["Light","-95%"]]
c['wk']=[["Dark",None]]
clr(c,'ab_el')                          # base resists Light; the \u2605 absorb is captured in notes
c['zones']=[["Full Moon Fountain","80"]]
c['img']="mobimages/carbuncle prime.png"
c['drops']="Shiva's Shotel, Titan's Baselarde, Leviathan's Couse, Ifrit's Bow, Garuda's Sickle, Ramuh's Mace, Carbuncle's Cuffs, Marquetry Staff, Engraved Belt, Lapidary Tunic, Satlada Necklace"
c['notes']=[
 "Waking the Beast battlefield NM (Full Moon Fountain). At 75%/50%/25% HP it despawns and 1/2/3 random avatars take its place; defeating them returns Carbuncle Prime at that HP. When all avatars are beaten, five Carbuncle Primes spawn at 25% HP, each using Searing Light at ~1% HP.",
 "\u2605 version (lv ~113-119, while holding the Waking the Beast phantom gem): does not despawn, possesses all Carbuncle blood pacts, uses an AoE Holy Mist and occasional Searing Light (partial hate reset on everyone it hits), trait Auto Regen. Its resistances shift to ABSORB Light, resist all other elements ~70%, and take -30% physical/magical/breath.",
]
# ab already = the 7 Carbuncle blood pacts (kept)

# ---------- null-poison guard ----------
for v in m.values():
    for k in [k for k,val in list(v.items()) if val is None]:
        del v[k]

json.dump(d,open('mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print("written")
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']
print("abilities",len(ab),"family_eco",len(d['family_eco']))
bad=[(k,kk) for k,v in m.items() for kk,vv in v.items() if vv is None]; print("None values:",len(bad))
und=[a for k in ['alexander prime','carbuncle prime'] for a in (m[k].get('ab') or []) if a not in ab]; print("alex/carb undefined refs:",und)
for k in ['alexander prime','carbuncle prime']:
    v=m[k]; print(f"  {k}: nm={v.get('nm')} img={v.get('img')!r} st={v.get('st')} wk={v.get('wk')} ab_el={v.get('ab_el')} zones={v.get('zones')} ab={len(v.get('ab') or [])}moves drops={(v.get('drops') or '')[:45]!r}")
