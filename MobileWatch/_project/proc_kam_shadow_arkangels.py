#!/usr/bin/env python3
"""
proc_kam_shadow_arkangels.py — Rev 118: Kam'lanaut, Shadow Lord, and the five
Ark Angels (HM/TT/MR/EV/GK). Enriches jobs, NM flags, resistances, drops, zones,
notes, renders; defines 20 abilities; un-orphans Humanoid into the Unclassified
eco and sets Shadow Lord -> Demon.

Author: BalladOfWorms
"""
import json
P='mobs.json'
d=json.load(open(P))
M=d['mobs']; A=d['abilities']; FE=d['family_eco']; FI=d['family_icons']

# ---------- 1. NEW ABILITY DEFINITIONS (18) ----------
NEW={
 # Kam'lanaut
 "Light Blade":{"d":"Three-hit sword strike dealing severe physical damage to a single target.","t":"Physical","tgt":"Single","notes":"Damage scales with distance closed; can be mitigated by kiting."},
 "Great Wheel":{"d":"Area attack that resets enmity on those it hits.","t":"Physical","tgt":"AoE","fx":["Hate Reset"]},
 # Shadow Lord (star-only signals + form-2)
 "Damning Edict":{"tgt":"Self","notes":"Signals a period of physical immunity on the Very Difficult (\u2605) battlefield."},
 "Swath of Silence":{"tgt":"Self","notes":"Signals a period of magic immunity on the Very Difficult (\u2605) battlefield."},
 "Bowels of Agony":{"t":"Magical","tgt":"AoE","r":"Limited radius","notes":"Limited-range second-form attack seen on the Very Difficult (\u2605) battlefield."},
 # Ark Angel HM
 "Cross Reaver":{"d":"Cone attack dealing heavy physical damage (~500-900).","t":"Physical","tgt":"Cone AoE","fx":["Stun"]},
 "Swift Blade":{"d":"Single-target sword weapon skill.","t":"Physical","tgt":"Single"},
 "Chant du Cygne":{"d":"Three-hit sword weapon skill with a high critical-hit rate.","t":"Physical","tgt":"Single"},
 # Ark Angel TT
 "Amon Drive":{"d":"Unique scythe weapon skill dealing area damage (~100-300).","t":"Physical","tgt":"AoE","fx":["Paralysis","Petrification"],"notes":"Absorbable by Utsusemi."},
 # Ark Angel MR
 "Havoc Spiral":{"d":"Unique weapon skill dealing area damage (~100-300).","t":"Physical","tgt":"AoE","fx":["Sleep"],"notes":"Absorbable by Utsusemi."},
 "Larceny":{"tgt":"Single","notes":"Steals a beneficial effect from the target; used to counter SP-ability use."},
 "Cloudsplitter":{"d":"Weapon skill dealing damage to a single target.","t":"Physical","tgt":"Single","notes":"Favored below 25% HP, alongside Darkness skillchains."},
 # Ark Angel EV
 "Dominion Slash":{"d":"Unique weapon skill dealing area damage (~100-300).","t":"Physical","tgt":"AoE","fx":["Silence","Dispel"],"notes":"Absorbable by Utsusemi; can also dispel buffs."},
 "Shield Strike":{"d":"Cone attack dealing ~100 damage with a knockback.","t":"Physical","tgt":"Cone AoE","fx":["Stun"],"notes":"Knockback may be absorbed by shadows; reduced by Repulse Mantle."},
 "Arrogance Incarnate":{"d":"A modified Spirits Within that strikes targets within ~5 yalms.","t":"Physical","tgt":"AoE"},
 "Intervene":{"d":"Conal area attack (Paladin special ability).","t":"Physical","tgt":"Cone AoE"},
 # Ark Angel GK
 "Dragonfall":{"d":"Unique weapon skill dealing area damage (~100-300).","t":"Physical","tgt":"AoE","fx":["Bind"],"notes":"Absorbable by Utsusemi."},
 "Tachi: Fudo":{"d":"Katana weapon skill dealing damage to a single target.","t":"Physical","tgt":"Single","notes":"Gained below 25% HP; enables self-light-skillchaining."},
 "Spirits Within":{"d":"Sword weapon skill dealing damage based on the user\u2019s remaining HP to a single target.","t":"Physical","tgt":"Single"},
 "Vicious Kick":{"d":"A kick attack dealing physical damage to a single target.","t":"Physical","tgt":"Single"},
}
created=0
for k,v in NEW.items():
    if k not in A: A[k]=v; created+=1
    else: print('  (already existed, left as-is):',k)

# ---------- 2. ENRICH SHADOW-LORD-EXCLUSIVE ABILITIES ----------
def append_note(name,extra):
    a=A[name]; n=a.get('notes')
    if not n: a['notes']=extra
    elif extra.strip() not in n: a['notes']=n.rstrip()+' '+extra
A['Dark Nova']['el']='Dark'
A['Implosion']['el']='Dark'; append_note('Implosion','Removes Utsusemi.')
for nm in ['Giga Slash','Kick Back','Umbra Smash']:
    append_note(nm,'Absorbable by Utsusemi.')

# ---------- helpers ----------
def st(*pairs): return [[e,p] for e,p in pairs]
ALL8_40=st(('Fire','-40%'),('Wind','-40%'),('Lightning','-40%'),('Light','-40%'),('Ice','-40%'),('Earth','-40%'),('Water','-40%'),('Dark','-40%'))
AA_ZONES=[["LaLoff Amphitheater","75-124"],["Escha RuAun","75-124"]]

def upd(key,**kv):
    m=M[key]
    for k,v in kv.items():
        if v is None: m.pop(k,None)
        else: m[k]=v

# ---------- 3. MOB EDITS ----------
# Kam'lanaut
upd("kam'lanaut",
    job="Red Mage", nm=True, det=None,
    ab=["Light Blade","Great Wheel"],
    st=ALL8_40, wk=[],
    drops="Mes'yohi Sword, Mes'yohi Rod, Mes. Haubergeon, Mes'yohi Slacks",
    zones=[["Stellar Fulcrum","75-78"],["Empyreal Paradox","75-78"]],
    img="mobimages/kam'lanaut.png",
    notes=[
     "Endgame battlefield boss (Zilart / CoP final fights).",
     "Heals himself when struck by magic matching his active en-spell element \u2014 avoid nuking into a matching En-spell.",
     "Gravity is difficult to land without Elemental Seal.",
     "Title: Quieter of Ancient Thoughts (VD only)."])

# Shadow Lord (Mission 5-2 version)
upd("shadow lord",
    fam="Shadow Lord", job="Dark Knight", nm=True,
    ab=["Giga Slash","Kick Back","Umbra Smash","Dark Nova","Implosion","Damning Edict","Swath of Silence","Bowels of Agony"],
    st=st(('Fire','-60%'),('Wind','-60%'),('Lightning','-60%'),('Ice','-60%'),('Earth','-60%'),('Water','-60%'),('Dark','-90%')),
    wk=[],
    drops="Lightreaver, Onimusha-no-Kote, Dread Jupon, Perdition Slops, Trepidity Mantle",
    zones=[["Throne Room","60"]],
    img="mobimages/shadow lord.png",
    notes=[
     "Final boss of Zilart Mission 5-2.",
     "Fights in two forms (~10k HP, then ~4k HP).",
     "Alternates between a physical-immune and a magic-immune stance \u2014 match your damage type to the currently vulnerable stance.",
     "Second form uses only Implosion and Bowels of Agony.",
     "Engage carefully near 1% HP to avoid a premature despawn.",
     "Titles: Shadow Banisher / Brilliance Manifest."])
FE["Shadow Lord"]="Demon"
FI["Shadow Lord"]="Shadow Lord.jpg"

# Shadow Lord (S) sibling -> mark NM
upd("shadow lord (s)", nm=True)

# Ark Angel HM
upd("ark angel hm",
    job="Warrior / Ninja", nm=True,
    ab=["Mijin Gakure","Mighty Strikes","Brazen Rush","Cross Reaver","Swift Blade","Chant du Cygne"],
    st=st(('Fire','-30%'),('Wind','-15%'),('Lightning','-15%'),('Ice','-15%'),('Earth','-15%'),('Water','-15%'),('Dark','-30%')),
    wk=[],
    drops="Deacon Saber, Kerygma Belt, Bloodrain Strap, Lithelimb Cap",
    zones=AA_ZONES, img="mobimages/ark angel hm.png",
    notes=[
     "Battlefield boss (Divine Might / Zilart Mission 14); also a High-Tier Mission Battlefield and Escha - Ru'Aun NM.",
     "Uses Mijin Gakure near 1% HP \u2014 a near-certain wipe if he is at high HP, so keep him low before it fires.",
     "Opens the fight with Mighty Strikes.",
     "Cross Reaver is a ~500-900 cone that also Stuns; also uses Swift Blade, Chant du Cygne and various Ninjutsu.",
     "Entry via Phantom Gem of Apathy at Home Point 1, Ru'Aun Gardens.",
     "Titles: Ark Hume Humiliator / Vanquisher of Apathy."])

# Ark Angel TT
tt_sp=list(M['ark angel tt'].get('sp') or [])
if 'Meteor' not in tt_sp: tt_sp.append('Meteor')
upd("ark angel tt",
    job="Black Mage / Dark Knight", nm=True, sp=tt_sp,
    ab=["Amon Drive","Manafont","Blood Weapon","Soul Enslavement"],
    st=st(('Fire','-15%'),('Wind','-15%'),('Lightning','-15%'),('Ice','-30%'),('Earth','-15%'),('Water','-30%'),('Dark','-30%')),
    wk=[],
    drops="Deacon Scythe, Rahab Ring, Fravashi Mantle",
    zones=AA_ZONES, img="mobimages/ark angel tt.png",
    notes=[
     "Battlefield boss (Divine Might); also a High-Tier Mission Battlefield and Escha - Ru'Aun NM.",
     "Teleports around the arena and uses AoE Petrify.",
     "Amon Drive is an AoE (~100-300) with Paralysis and Petrification, absorbable by Utsusemi.",
     "Uses Blood Weapon first, then Manafont, spamming Meteor under Manafont \u2014 a Thief can Larceny the Manafont to stop it.",
     "In Escha, opens with Sleepga + Meteor and uses Soul Enslavement (an amnesia aura).",
     "Entry via Phantom Gem of Cowardice at Home Point 2, Ru'Aun Gardens.",
     "Titles: Ark Tarutaru Trouncer / Vanquisher of Cowardice."])

# Ark Angel MR
upd("ark angel mr",
    job="Beastmaster / Thief", nm=True,
    ab=["Havoc Spiral","Familiar","Charm","Perfect Dodge","Larceny","Cloudsplitter"],
    st=st(('Fire','-15%'),('Wind','-15%'),('Lightning','-15%'),('Ice','-15%'),('Earth','-15%'),('Water','-15%'),('Dark','-30%')),
    wk=[],
    drops="Deacon Tabar, Enuma Mantle, Felistris Mask",
    zones=AA_ZONES, img="mobimages/ark angel mr.png",
    notes=[
     "Battlefield boss (Divine Might); also a High-Tier Mission Battlefield and Escha - Ru'Aun NM.",
     "Can Charm players regardless of whether her pet is alive.",
     "Summons a pet \u2014 usually Ark Angel's Tiger (fairly harmless) or Ark Angel's Mandragora (dangerous, can Dream Flower); sleep the pet and ignore it.",
     "Havoc Spiral is an AoE (~100-300) with Sleep, absorbable by Utsusemi.",
     "Uses Perfect Dodge once, Charm below 50% once, and Larceny if a 2-hour is used.",
     "In Escha, opens with Perfect Dodge, summons Karakul or Gnat (sleepable, huge regain), Charms around 75%, favors Havoc Spiral above 30%, then spams Cloudsplitter with Darkness skillchains.",
     "Entry via Phantom Gem of Envy at Home Point 3, Ru'Aun Gardens.",
     "Titles: Ark Mithra Maligner / Vanquisher of Envy."])

# Ark Angel EV
upd("ark angel ev",
    job="Paladin / White Mage", nm=True,
    ab=["Dominion Slash","Shield Strike","Spirits Within","Vorpal Blade","Arrogance Incarnate","Chant du Cygne","Intervene","Invincible","Benediction"],
    st=st(('Fire','-15%'),('Wind','-15%'),('Lightning','-30%'),('Ice','-15%'),('Earth','-15%'),('Water','-15%'),('Dark','-30%')),
    wk=[],
    drops="Deacon Sword, Cagliostro's Rod, Elis Tome, Dynasty Mitts",
    zones=AA_ZONES, img="mobimages/ark angel ev.png",
    notes=[
     "Battlefield boss (Divine Might / Zilart Mission 14); also a High-Tier Mission Battlefield and Escha - Ru'Aun NM.",
     "Dominion Slash is an AoE (~100-300) that Silences and can dispel buffs, absorbable by Utsusemi.",
     "Shield Strike is a conal ~100-damage Stun with knockback (reduced by Repulse Mantle, may be absorbed by shadows).",
     "Spirits Within can destroy a tank \u2014 Gravity + Bind and kiting is the usual strategy.",
     "Arrogance Incarnate is a modified Spirits Within that hits targets within ~5'.",
     "At 30% and under she uses Chant du Cygne twice to make a Light skillchain.",
     "Uses Invincible multiple times and Benediction once (triggered when the tank is cured for ~800+ HP).",
     "Casts Aquaveil, Blink, Haste plus offensive divine magic (Diaga II, Banishga III, Holy II).",
     "Entry via Phantom Gem of Arrogance at Home Point 4, Ru'Aun Gardens.",
     "Titles: Ark Elvaan Eviscerator / Vanquisher of Arrogance."])

# Ark Angel GK
upd("ark angel gk",
    job="Samurai / Dragoon", nm=True,
    ab=["Dragonfall","Meikyo Shisui","Call Wyvern","Tachi: Fudo"],
    st=st(('Fire','-15%'),('Wind','-15%'),('Lightning','-15%'),('Ice','-15%'),('Earth','-30%'),('Water','-15%'),('Dark','-30%')),
    wk=[],
    drops="Deacon Blade, Seki Sh. Pouch, Daihanshi Habaki",
    zones=AA_ZONES, img="mobimages/ark angel gk.png",
    notes=[
     "Battlefield boss (Divine Might / Zilart Mission 14); also a High-Tier Mission Battlefield and Escha - Ru'Aun NM.",
     "Uses Call Wyvern to summon Ark Angel's Wyvern (can re-summon it if killed) and Meikyo Shisui repeatedly.",
     "Dragonfall is an AoE (~100-300) with Bind, absorbable by Utsusemi; on Difficult/Very Difficult it can one-shot.",
     "At 25% HP and under he gains Tachi: Fudo and will self-skillchain into Light \u2014 a Ninja tank with Utsusemi is recommended.",
     "Entry via Phantom Gem of Rage at Home Point 5, Ru'Aun Gardens.",
     "Titles: Ark Galka Gouger / Vanquisher of Rage."])

# ---------- 4. FAMILY ECO: un-orphan Humanoid ----------
FE["Humanoid"]="Unclassified"

# ---------- 5. GUARDS ----------
bad_none=[(k,f) for k,m in M.items() for f,v in m.items() if v is None]
assert not bad_none, ('NULL values present: %r'%bad_none[:10])
TOUCHED=["kam'lanaut",'shadow lord','shadow lord (s)','ark angel hm','ark angel tt','ark angel mr','ark angel ev','ark angel gk']
undef=sorted({a for k in TOUCHED for a in (M[k].get('ab') or []) if a not in A})
assert not undef, ('UNDEFINED ability refs in edited mobs: %r'%undef)

json.dump(d,open(P,'w'),separators=(', ', ': '),ensure_ascii=False)
print('created abilities:',created,'| total abilities:',len(A))
print('mobs:',len(M),'| family_eco:',len(FE),'| family_icons:',len(FI))
print('Humanoid eco:',FE['Humanoid'],'| Shadow Lord eco:',FE['Shadow Lord'])
print('GUARDS PASSED (no nulls, no undefined ab refs)')
