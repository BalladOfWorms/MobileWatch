import json, io
P='mobs.json'
d=json.load(open(P)); m=d['mobs']; ab=d['abilities']
before={'mobs':len(m),'ab':len(ab),'fe':len(d['family_eco']),'nm':sum(1 for v in m.values() if v.get('nm'))}

def setk(mob,**kw):
    for k,v in kw.items(): mob[k]=v

# ---------- NEW ABILITIES ----------
NEW={
 # Gessho (Yagudo Ninja NM)
 'Hane Fubuki':{'d':'Single-target physical damage with an additional Poison effect.','t':'Physical','tgt':'Single','fx':['Poison']},
 'Happobarai':{'d':'AoE physical damage with an additional Stun effect.','t':'Physical','tgt':'AoE','fx':['Stun']},
 'Hiden Sokyaku':{'d':'Single-target physical damage with an additional Stun effect.','t':'Physical','tgt':'Single','fx':['Stun']},
 'Rinpyotosha':{'d':'Boosts the user\u2019s attack.','t':'Enhancing','tgt':'Self','fx':['Attack Boost']},
 'Shibaraku':{'d':'AoE physical damage with additional Knockback and Stun.','t':'Physical','tgt':'AoE','fx':['Knockback','Stun']},
 'Shiko no Mitate':{'d':'Boosts the user\u2019s defense.','t':'Enhancing','tgt':'Self','fx':['Defense Boost']},
 'Kagedourou':{'d':'Summons multiple clones of the user. The clones depop once enough damage is dealt to the caster and can also be defeated individually. Used above 50% HP.','tgt':'Self'},
 'Karakuridourou':{'d':'Summons multiple clones below 50% HP. Every clone (and the caster) is masked and invulnerable except one \u201ccorrect\u201d clone; deal enough damage to the correct clone and the rest depop, resuming the fight.','tgt':'Self'},
 'Tsujikaze':{'d':'AoE magical damage (~14.9\u2032) with Silence, Defense Down, and Magic Defense Down. Used below 50% HP.','t':'Magical','tgt':'AoE','fx':['Silence','Defense Down','Magic Defense Down']},
 'Kamaitachi':{'d':'AoE physical damage with major Knockback and a full Dispel. The dispel can be avoided by a shield block or Utsusemi. Used below 50% HP.','t':'Physical','tgt':'AoE','fx':['Knockback','Dispel']},
 # Lilith - Lady Lilith form
 'Dark Thorn':{'d':'The user gains Dread Spikes and Stoneskin.','t':'Enhancing','tgt':'Self','fx':['Dread Spikes','Stoneskin']},
 'Durance Whip':{'d':'Cone physical damage with additional Bio, Bind, and Amnesia.','t':'Physical','tgt':'Cone AoE','fx':['Bio','Bind','Amnesia']},
 'Moonlight Veil':{'d':'AoE dark magic damage with Terror. Spawns a Dark Gyve. On the \u2605 battlefield it also inflicts Magic Defense Down.','t':'Magical','el':'Dark','tgt':'AoE','fx':['Terror']},
 'Petaline Tempest':{'d':'AoE magic damage that lowers Max HP, MP, and TP (up to 1,000).','t':'Magical','tgt':'AoE','fx':['Max HP Down','MP Down','TP Down']},
 'Subjugating Slash':{'d':'Cone damage with Knockback that dispels up to 3 enhancements. On the \u2605 battlefield it instead resets enmity and deals a large % of Max HP.','t':'Physical','tgt':'Cone AoE','fx':['Knockback','Dispel']},
 'Fatal Allure':{'d':'Cone gaze that Charms and inflicts a 60-second Poison. The charm can be avoided by facing away from the caster. Used while under Trance.','r':'Gaze','tgt':'Cone AoE','fx':['Charm','Poison']},
 # Lilith - Lilith Ascendant form (each summons a matching element Gyve)
 'Dark Burst':{'d':'Cone lightning magic damage with Stun that resets all of the user\u2019s ability timers, and summons a Thunder Gyve.','t':'Magical','el':'Lightning','tgt':'Cone AoE','fx':['Stun']},
 'Dark Flare':{'d':'Cone fire magic damage with TP reset and Enmity reduction, and summons a Fire Gyve.','t':'Magical','el':'Fire','tgt':'Cone AoE','fx':['TP Reset','Enmity Down']},
 'Dark Flood':{'d':'Cone water magic damage with Encumbrance and Knockback, and summons a Water Gyve.','t':'Magical','el':'Water','tgt':'Cone AoE','fx':['Encumbrance','Knockback']},
 'Dark Freeze':{'d':'Cone ice magic damage with Terror and Enmity reduction, and summons an Ice Gyve.','t':'Magical','el':'Ice','tgt':'Cone AoE','fx':['Terror','Enmity Down']},
 'Dark Quake':{'d':'AoE earth magic damage with Bind and Amnesia, and summons an Earth Gyve.','t':'Magical','el':'Earth','tgt':'AoE','fx':['Bind','Amnesia']},
 'Dark Tornado':{'d':'AoE wind magic damage with a full Dispel and Knockback, and summons a Wind Gyve.','t':'Magical','el':'Wind','tgt':'AoE','fx':['Dispel','Knockback']},
 'Dark Moon':{'d':'AoE dark magic damage with Weakness, summoning two Dark Gyves. Used below 50% HP.','t':'Magical','el':'Dark','tgt':'AoE','fx':['Weakness']},
 'Dark Sun':{'d':'AoE light magic damage with a chance of Death, summoning two Light Gyves. Used below 50% HP.','t':'Magical','el':'Light','tgt':'AoE','fx':['Death']},
}
created=[]
for k,v in NEW.items():
    if k not in ab: ab[k]=v; created.append(k)

# ---------- PROMATHIA (render only) ----------
prom=m['promathia']
prom['img']='mobimages/promathia.png'

# ---------- LANCELORD GAHEEL JA ----------
lanc=m['lancelord gaheel ja']
lanc['wk']=[['Magical','+50%'],['Ice','+15%']]
lanc['drops']='Bestas Bane, Savas Jawshan, Sifahir Slacks, Sahip Helm, Pratik Earring, Seraphicaller'
lanc['img']='mobimages/lancelord gaheel ja.png'
lanc['notes']=[
 'Puppet in Peril II \u2014 fought in the Jade Sepulcher with a Puppet In Peril phantom gem (Aht Urhgan Mission 29). The fight opens with several low-HP Mamool Ja (Polemicist/BLM, Isangoma/WHM, Flamerearer/DRG, Unseen/NIN, Profligate/THF), all susceptible to Sleep; the Flamerearer can Call Wyvern even while slept or petrified. Lancelord Gaheel Ja spawns once every add is dead.',
 'Casts Protect IV and Shell IV on itself; once those are dispelled it prioritizes Cure and Flash. It has very high defense \u2014 rely on magic damage (Formless Strikes is ineffective; Runes are effective). It also has a normal ranged attack for out-of-range targets.',
 'At 50% HP it gains Cure V / Protect V / Shell V / Banishga III / Diaga III and swaps Fire Angon for Blazing Angon. At 25% it swaps to Burning Memories, which it favors \u2014 that TP move is fairly easy to Stun.',
]
# enrich shared Angon / cone defs (broaden the "Wivres only" scoping; add ignores-shadows / absorbable-by-shadows)
for a in ['Fire Angon','Blazing Angon','Burning Memories']:
    dfn=ab[a]
    if 'Ignores shadows' not in dfn['d']: dfn['d']=dfn['d'].rstrip('.')+'. Ignores shadows but does not remove them; centered around the target.'
    dfn['notes']='Used by Mamool Rider Wivres and Lancelord Gaheel Ja.'
for a in ['Batterhorn','Clobber']:
    dfn=ab[a]
    if 'Absorbable' not in dfn['d']: dfn['d']=dfn['d'].rstrip('.')+'. Absorbable by 2-3 shadows.'

# ---------- GESSHO ----------
g=m['gessho']
setk(g, fam='Yagudo', job='Ninja', nm=True, crys='Wind', det=['Sound'],
     zones=[['Talacca Cove', None]], img='mobimages/gessho.png')
g['ab']=['Hane Fubuki','Happobarai','Hiden Sokyaku','Rinpyotosha','Shibaraku','Shiko no Mitate',
         'Kagedourou','Karakuridourou','Tsujikaze','Kamaitachi','Mijin Gakure']
g['notes']=[
 '\u2605Legacy of the Lost \u2014 spawned by Aht Urhgan Mission 35 in Talacca Cove. Mixes ranged and melee attacks.',
 'Above 50% HP it casts Utsusemi: Ni, elemental ninjutsu at the :ni tier, and :ichi debuffs. Below 50% it upgrades to Utsusemi: San, :san elemental ninjutsu, and :ni debuffs, and begins using Mijin Gakure.',
 'Kagedourou (above 50%) and Karakuridourou (below 50%) summon multiple clones. Below 50%, every clone \u2014 Gessho included \u2014 is masked and invulnerable except the one \u201ccorrect\u201d clone; deal enough damage to it and the rest depop so the fight resumes. This happens more often under 25%.',
 'Below 50% it also gains Tsujikaze (AoE magic + Silence / Defense Down / Magic Defense Down, ~14.9\u2032) and Kamaitachi (AoE physical + major Knockback + Dispel all; the dispel can be avoided by a shield block or Utsusemi).',
]

# ---------- LILITH (two forms) ----------
# Lady Lilith (first form, DNC/BLM)
ll=m['lady lilith']
setk(ll, fam='Humanoid', job='Dancer / Black Mage', nm=True,
     st=[['Breath','-25%'],['Light','-30%'],['Dark','-50%']], wk=[],
     zones=[['Walk of Echoes','81-82']], img='mobimages/lady lilith.png')
ll['ab']=['Dark Thorn','Durance Whip','Moonlight Veil','Petaline Tempest','Subjugating Slash','Fatal Allure']
ll['sp']=['Breakga','Dispelga','Silencega','Graviga','Bindga','Slowga','Comet','Meteor']
ll['notes']=[
 'Maiden of the Dusk (Wings of the Goddess Mission 51, Walk of Echoes) \u2014 released at the level 90 cap. Lady Lilith is the first form: DNC/BLM, ~9,800 HP. Immune to Silence and Sleep, resistant to Stun. Auto-attacks are AoE dark damage that remove shadows and knock back.',
 'Uses Dark Thorn (self Dread Spikes + Stoneskin), Durance Whip (cone + Bio/Bind/Amnesia), Moonlight Veil (AoE + Terror, spawns a Dark Gyve), Petaline Tempest (AoE + Max HP/MP/TP down), and Subjugating Slash (cone Knockback that dispels 3 buffs). Enters Trance at 50% (then freely), gaining the gaze-Charm Fatal Allure \u2014 avoid it by facing away from her. Also casts Breakga/Dispelga/Silencega/Graviga/Bindga/Slowga/Comet, and Meteor at low HP.',
 'A ring of Gyves encircles the arena: they absorb all magic and attack anyone within 6\u2032, and players outside the ring cannot damage Lilith. TP moves summon element-themed Gyves that persist. On defeat she is replaced by Lilith Ascendant.',
 'High-Tier \u2605 (Maiden phantom gem, Walk of Echoes [P], title Lilith Liquidator): her grid shifts to Breath -50% / Fire-Wind-Lightning -50% / Light -80% / Ice-Earth-Water -60% and she ABSORBS Dark. After being struck by a Blood Pact she takes 90% less damage from Blood Pacts for 10s, so avoid them. ~200k HP on Very Easy.',
]
# Lilith Ascendant (second form, WHM/BLM) - already fam=Humanoid, nm, big sp list, det [Sight,True Sight]
la=m['lilith ascendant']
setk(la, job='White Mage / Black Mage',
     st=[['Breath','-50%'],['Fire','-40%'],['Wind','-40%'],['Lightning','-40%'],['Light','-80%'],
         ['Ice','-40%'],['Earth','-40%'],['Water','-40%'],['Dark','-80%']], wk=[],
     zones=[['Walk of Echoes','83-84']])
la['ab']=['Dark Burst','Dark Flare','Dark Flood','Dark Freeze','Dark Quake','Dark Tornado','Dark Moon','Dark Sun']
la['notes']=[
 'Maiden of the Dusk \u2014 Lilith Ascendant is the second form, spawning after Lady Lilith falls (Walk of Echoes, WotG Mission 51). WHM/BLM, ~17,000 HP. Immune to Silence and Sleep, resistant to Stun.',
 'Its Dark-element conal/AoE moves each summon a matching element Gyve: Dark Burst (Lightning, Stun + resets its ability timers \u2192 Thunder Gyve), Dark Flare (Fire, TP reset + enmity down \u2192 Fire Gyve), Dark Flood (Water, Encumbrance + knockback \u2192 Water Gyve), Dark Freeze (Ice, Terror + enmity down \u2192 Ice Gyve), Dark Quake (Earth, Bind + Amnesia \u2192 Earth Gyve), Dark Tornado (Wind, full Dispel + knockback \u2192 Wind Gyve).',
 'Below 50% it adds Dark Moon (AoE Dark + Weakness \u2192 two Dark Gyves) and Dark Sun (AoE Light + chance of Death \u2192 two Light Gyves). Each Light Gyve present cuts the damage it takes; once five are up it is immune to damage, so clear Gyves between its TP moves.',
 'High-Tier \u2605: its grid shifts to Breath -50% / Fire-Wind-Lightning -80% / Ice-Earth-Water -50% / Dark -80% and it ABSORBS Light. \u2605 rewards: Daybreak, Malignance Pole/Sword/Earring (the Malignance Box container drops here too but is not tracked as gear).',
]
la['drops']='Daybreak, Malignance Pole, Malignance Sword, Malignance Earring'

# ---------- DELETE junk 'lilith' stub ----------
deleted=None
if 'lilith' in m:
    stub=m['lilith']
    # safety: only delete if it's the malformed no-data stub
    if not (stub.get('ab') or stub.get('sp') or stub.get('notes') or stub.get('wk') or stub.get('st') or stub.get('zones')):
        del m['lilith']; deleted='lilith'

# ---------- write ----------
# null guard
bad=[ (k,kk) for k,v in m.items() for kk,vv in v.items() if vv is None and kk not in ('wk','st') ]
# wk/st can hold [x,None] pairs but not be None themselves; our sets never write None scalars
assert not [k for v in m.values() for kk,vv in v.items() if vv is None and kk in ('n','fam','eco','job','crys','spawn','drops','nmlv','sub','img')], 'null scalar!'
with io.open(P,'w',encoding='utf-8') as f:
    json.dump(d,f,separators=(', ',': '),ensure_ascii=False)

after={'mobs':len(m),'ab':len(ab),'fe':len(d['family_eco']),'nm':sum(1 for v in m.values() if v.get('nm'))}
print('created abilities (%d):'%len(created), created)
print('deleted stub:', deleted)
print('BEFORE',before)
print('AFTER ',after)
