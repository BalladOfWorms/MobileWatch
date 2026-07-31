import json
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']; fe=d['family_eco']

# ---------- CREATE Shiva's 2 missing defs (Diamond Dust + Frost Armor already exist) ----------
ab['Rush']={"d":"A fivefold physical attack.","t":"Physical","tgt":"Single"}
ab['Heavenly Strike']={"d":"Deals ice damage in an area of effect. Ignores shadows.","t":"Magical","el":"Ice","tgt":"AoE","notes":"Ignores Utsusemi shadows."}

# ---------- SHIVA PRIME (grid already correct: A Ice / wk Fire / rest -95) ----------
s=m['shiva prime']; s['nm']=True; s['lv']=[20,85]
# ab already = [Rush, Heavenly Strike, Diamond Dust, Frost Armor]; sp add Freeze II (Trial by Ice star)
s['sp']=["Freeze II","Blizzard V","Blizzaja","Paralyga"]
s['zones']=[["Cloister of Frost","20-60"],["Full Moon Fountain","85"]]
s['img']="mobimages/shiva prime.png"
s['drops']="Calved Claws, Frazil Staff, Rimeice Earring, Nilas Gloves, Floestone"
s['notes']=[
 "Battlefield NM with a very large magic-aggro detection range; level depends on the spawning quest \u2014 20 (Trial-Size Trial by Ice), 60 (Trial by Ice, Cloister of Frost), 85 (Waking the Beast, Full Moon Fountain). Title: Penitentes Blaster (VD only).",
 "Uses Diamond Dust 10 minutes into Trial by Ice, or at ~50% HP in Waking the Beast (now a normal TP move, not Astral-Flow-only; partial hate reset \u2014 save Provoke/Flash for right after). Heavenly Strike ignores shadows; melee has an added Ice-damage effect.",
 "Ice damage from spells, additional effects, and skillchains (INCLUDING Darkness) HEALS her \u2014 avoid it. Four Ice Elementals assist her in the Waking the Beast (lv85) fight.",
 "\u2605 version (Trial by Ice \u2605): casts Freeze II/Blizzard V/Blizzaja; resistances shift to -30% physical/magical/breath.",
]

# ---------- SIREN PRIME (fam=Siren; Type=Avatar per its page) ----------
fe['Siren']='Avatar'   # Siren Prime page: Type=Avatar, Family=Siren (its own family/eco; elemental Primes stay Unclassified)
# create the 6 abilities (Tornado II is a SPELL per Image 11, not an ability def)
ab['Hysteric Assault']={"d":"A fivefold physical attack that also drains HP proportional to the damage dealt.","t":"Physical","tgt":"Single"}
ab['Lunatic Voice']={"d":"Inflicts Silence on nearby enemies.","tgt":"AoE","fx":["Silence"],"r":"6-8' radial"}
ab['Sonic Buffet']={"d":"Wind-based conal attack that dispels 2-3 beneficial effects.","t":"Magical","el":"Wind","tgt":"Conal","fx":["Dispel"]}
ab['Entice']={"d":"Charms a single target.","tgt":"Conal","fx":["Charm"],"notes":"Will not charm Trusts."}
ab['Bitter Elegy']={"d":"A single-target wind-based Slow (50%), applied as a song debuff (removed by Erase).","el":"Wind","tgt":"Single","fx":["Slow"]}
ab['Clarsach Call']={"d":"High wind damage in a wide radius; grants the Siren Attack/Defense/Evasion/Magic Attack/Magic Accuracy/Magic Evasion/Magic Defense bonuses for 3 minutes (each individually dispellable).","t":"Magical","el":"Wind","tgt":"AoE","notes":"Used once at 50% HP."}

sp_=m['siren prime']; sp_['nm']=True; sp_['job']='Summoner'
sp_['ab_el']=["Wind","Light"]
sp_['wk']=[["Ice",None],["Dark",None]]
sp_['st']=[["Slashing","-75%"],["Impact","-62.5%"],["H2H","-62.5%"],["Piercing","-50%"],["Ranged","-50%"]]
sp_['ab']=["Hysteric Assault","Lunatic Voice","Sonic Buffet","Entice","Bitter Elegy","Clarsach Call"]
sp_['sp']=["Tornado II"]
sp_['zones']=[["Yorcia Weald [U]",None]]
sp_['img']="mobimages/siren prime.png"
sp_['notes']=[
 "Quest NM \u2014 Winds of Eternity battlefield (Yorcia Weald [U]); a variant of the Siren fought at the end of Rhapsodies of Vana'diel Chapter 1. 30-minute time limit; up to 6 players (Trusts allowed). Title: Eternal Communer.",
 "Absorbs Wind and Light; weak to Dark and Ice; susceptible to Stun; immune to Silence. Because it absorbs wind MAGIC damage, its SDT reads lowest to Wind \u2014 so wind nukes (and Automatons/Trusts that target the lowest resist) plus Fragmentation/Light skillchains will HEAL it. Job is Summoner (no longer Bard); does not apply Requiem.",
 "Clarsach Call (once, at 50% HP) grants a large multi-stat buff for 3 min (each buff individually dispellable). Lunatic Voice is an AoE Silence; Entice charms a single target (not Trusts); Bitter Elegy is a 50% wind Slow applied as a song.",
]

# ---------- small enrichment: Fenrir's Lunar Roar removes up to 10 (Image 12), not 6 ----------
if 'Lunar Roar' in ab:
    ab['Lunar Roar']['d']="Removes up to ten beneficial effects from targets in a 30' area of effect."
    ab['Lunar Roar']['tgt']="AoE"; ab['Lunar Roar']['r']="30' radial"

for v in m.values():
    for k in [k for k,val in list(v.items()) if val is None]:
        del v[k]
json.dump(d,open('mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print("written; abilities",len(ab),"| family_eco Siren=",fe.get('Siren'))
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']
bad=[(k,kk) for k,v in m.items() for kk,vv in v.items() if vv is None]; print("None:",len(bad))
und=[a for k in ['shiva prime','siren prime'] for a in (m[k].get('ab') or []) if a not in ab]; print("undefined refs:",und)
for k in ['shiva prime','siren prime']:
    v=m[k]; print(f"  {k}: fam={v.get('fam')} nm={v.get('nm')} img={v.get('img')!r} ab_el={v.get('ab_el')} wk={v.get('wk')} st={[e[0] for e in (v.get('st') or [])]} ab={v.get('ab')} sp={v.get('sp')} zones={v.get('zones')}")
