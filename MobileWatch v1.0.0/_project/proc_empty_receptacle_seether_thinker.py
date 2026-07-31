import json, copy
P='android/app/src/main/assets/mobs.json'
d=json.load(open(P))
mobs=d['mobs']; ab=d['abilities']; frs=d['family_resist_sets']; fe=d['family_eco']; fn=d['family_notes']

def byn(n):
    for v in mobs.values():
        if v.get('n')==n: return v
    return None
def clr(v,*keys):
    for k in keys:
        if k in v: del v[k]
def stamp_kit(v, kit):
    v['ab']=list(kit)

# ===== 1. ecos =====
for f in ['Receptacle','Seether','Thinker']: fe[f]='Empty'

# ===== 2. resist sets: Seether & Thinker == Craver =====
frs['Seether']=copy.deepcopy(frs['Craver'])
frs['Thinker']=copy.deepcopy(frs['Craver'])
assert frs['Seether']==frs['Craver'] and frs['Thinker']==frs['Craver']

# ===== 3. new ability defs =====
newdefs={
 'Empty Seed': {'d':"Deals physical damage to targets in a 20' area of effect. Additional effect: Knockback.",'t':'Physical','tgt':'AoE','fx':['Knockback']},
 'Lamentation': {'d':'Deals damage to targets in an area of effect and inflicts Dia (Defense Down, roughly 8 HP per tick).','t':'Magical','tgt':'AoE','fx':['Dia','Defense Down']},
 'Occultation': {'d':'The user gains the Blink status.','t':'Enhancing','tgt':'Self','fx':['Blink']},
 'Vanity Strike': {'d':'Deals physical damage to a single target. Additional effect: Stun.','t':'Physical','tgt':'Single','fx':['Stun']},
 'Wanion': {'d':"Transfers the user's negative status effects onto targets in an area of effect.",'t':'Magical','tgt':'AoE'},
 'Binary Absorption': {'d':'Drains 200 HP from a single target.','t':'Magical','tgt':'Single'},
 'Binary Tap': {'d':'Absorbs two positive status effects from a single target, or otherwise drains HP.','t':'Magical','tgt':'Single'},
 'Pain Sync': {'d':"Deals breath damage equal to 40% of the damage inflicted to the user while it readies this move, in a 20' area of effect.",'t':'Breath','tgt':'AoE'},
 'Spirit Tap': {'d':'Absorbs one positive status effect from a single target, or otherwise drains HP.','t':'Magical','tgt':'Single'},
 'Trinary Absorption': {'d':'Drains 300 HP from a single target.','t':'Magical','tgt':'Single'},
 'Winds of Promyvion': {'d':'Erases a negative status effect from the user.','t':'Enhancing','tgt':'Self','notes':'Used when the user has an active status ailment.'},
}
created=[]
for n,defn in newdefs.items():
    if n not in ab: ab[n]=defn; created.append(n)

# enrich Empty Cutter (Thinker-exclusive) + soften Trinary Tap note (Thinker-exclusive)
ab['Empty Cutter']={'d':'Deals physical damage to a single target. Can land a critical hit.','t':'Physical','r':'Melee','tgt':'Single'}
ab['Trinary Tap']['notes']="Absorbs up to three buffs (including food); drains up to 300 HP if it cannot take enough buffs. Goes through shadows."

# ============================================================
# RECEPTACLE (6) — stationary Memory Receptacle portals; single unknown grid (NOT a Core family)
# ============================================================
RKIT=['Empty Seed']
for k,v in list(mobs.items()):
    if v.get('fam')!='Receptacle': continue
    v['det']=['Sound']
    clr(v,'crys')            # object gives no crystal (box shows "N")
    v['job']=None; clr(v,'job')
    stamp_kit(v,RKIT)
mr=byn('Memory Receptacle')
mr['nm']=True; mr['lv']=[30,50]
mr['zones']=[['Promyvion-Dem'],['Promyvion-Mea'],['Promyvion-Holla'],['Promyvion-Vahzl']]
mr['notes']=['Spawns at various locations around the zone.','The correct receptacle opens a portal to the next level when defeated.']
# keep Memory Receptacle's existing per-mob grid (all-physical weak / all-element resist)
for col in ['Blue','Green','Red','Yellow']:
    cv=byn(f'Memory Receptacle ({col})')
    cv['zones']=[['Spire of Vahzl']]
    cv['notes']=['Colored puzzle variant encountered during Pulling the Plug (Spire of Vahzl).']
rc=byn('Recollector')
clr(rc,'wk','st')           # strip junk ['Piercing Damage', None] marker
fn['Receptacle']=['Stationary Memory Receptacle objects in Promyvion; destroying the correct one opens the portal to the next level.','Published family resistances are unconfirmed (the bestiary lists every cell as unknown).']

# ============================================================
# SEETHER (4) — Empty Core family (swipe); Def +20% trait
# ============================================================
SKIT=['Lamentation','Occultation','Vanity Strike','Wanion']
DET3=['Sight','Sound','Scent']
for k,v in list(mobs.items()):
    if v.get('fam')!='Seether': continue
    v['det']=list(DET3); v['crys']='Varies'; clr(v,'wk','st')
    stamp_kit(v,SKIT)
se=byn('Seether'); se['job']='Warrior'; se['lv']=[31,58]
se['zones']=[['Promyvion-Holla','31-38'],['Promyvion-Dem','31-38'],['Promyvion-Mea','31-38'],['Promyvion-Vahzl','51-58'],['Spire of Mea']]
pv=byn('Provoker'); pv['job']='Red Mage'; pv['lv']=[58,60]
pv['zones']=[['Promyvion-Vahzl']]
pv['notes']=['Forced spawn: trade a Satiator Remnant to the ??? at (E-7) on the fifth level of Promyvion-Vahzl.','Drops the Recollection of Anxiety and White Memosphere key items.']
me=byn('Meditator'); me['job']='Warrior'; me['lv']=[80,80]
me['zones']=[['Abyssea-La Theine']]
me['notes']=['Fast respawn; appears among Angler Tigers and Great Wasps, among other places.','Gives 10 Pearlescent light 100% of the time when killed appropriately.','Trading nearby can upgrade a Clear demilune abyssite to Colorful demilune abyssite (100% while holding Rhapsody in Mauve).']
al=byn('Apex Livid Rager'); al['job']='Warrior / Red Mage'
al['zones']=[['Promyvion-Holla'],['Promyvion-Dem'],['Promyvion-Mea'],['Promyvion-Vahzl']]
fn['Seether']=['Family has an innate defense boost of 20%.',
 "Empty 'Core' family: each Seether has an elemental Core that fixes its resistances \u2014 swipe the resist grid to see all eight Core alignments.",
 'Standard Seethers appear in Promyvion; Apex Livid Ragers are the high-tier version in the same zones.']

# ============================================================
# THINKER (12) — Empty Core family (swipe)
# ============================================================
TBASE=['Binary Absorption','Binary Tap','Empty Cutter','Negative Whirl','Pain Sync','Spirit Absorption','Spirit Tap','Stygian Vapor','Trinary Absorption','Trinary Tap','Winds of Promyvion']
TNM=TBASE+['Shadow Spread']
NM_NAMES={'Brooder','Cerebrator','Ponderer','Ruminator','Agonizer','Warder of Dignity'}
for k,v in list(mobs.items()):
    if v.get('fam')!='Thinker': continue
    n=v.get('n')
    if n=='Glassy Thinker': continue   # handled separately (own grid + own kit)
    v['det']=list(DET3); v['crys']='Varies'; clr(v,'wk','st')
    if v.get('job') in (None,'','WAR'): v['job']='Warrior'
    elif v.get('job')=='WAR': v['job']='Warrior'
    stamp_kit(v, TNM if (v.get('nm') or n in NM_NAMES) else TBASE)
# standard Thinker
th=byn('Thinker'); th['job']='Warrior'; th['lv']=[28,60]
th['zones']=[['Promyvion-Holla','29-40'],['Promyvion-Vahzl','54-60']]
# NMs
ce=byn('Cerebrator'); ce['lv']=[38,38]; ce['zones']=[['Promyvion-Holla']]
ce['notes']=['Spawns on the third level.','Drops the Cerebrator Remnant and Teal Memosphere key items.']
br=byn('Brooder'); br['job']='Warrior'; br['lv']=[85,85]; br['zones']=[['Abyssea-La Theine']]
br['drops']='Serpentes Sabots, Libeccio Mantle'
br['notes']=['Tends to spawn around Veridical Conflux #02, #03, and #08.','Respawn time is 10-15 minutes.','Uses its "Tap" TP moves in order, using more as its HP drops.','Can upgrade a key item to Scarlet demilune abyssite (100% while holding Rhapsody in Mauve).']
wd=byn('Warder of Dignity'); wd['lv']=[124,124]; wd['zones']=[['Escha RuAun']]
wd['drops']='Impassive Mantle, Thereoid Greaves, Henic Torque, Eschalixir'
wd['sp']=['Fire VI','Blizzard VI','Aero VI']
wd['notes']=['Lottery pop on the Eschan Limule island (portal #4).','Uses Binary Tap and Trinary Tap to absorb 2 and 3 buffs respectively \u2014 dispels are recommended.','Drops the Octanary nazar key item.']
rm=byn('Ruminator'); rm['job']='Warrior'; rm['lv']=[90,90]
po=byn('Ponderer'); po['lv']=[56,58]; po['zones']=[['Promyvion-Vahzl']]
ag=byn('Agonizer'); ag['lv']=[53,54]; ag['zones']=[['Spire of Vahzl']]
# event mobs
byn('Cogitator')['zones']=[['Spire of Holla']]
byn('Wreaker')['zones']=[['Spire of Holla']]
ct=byn('Contemplator (ENM)'); ct['zones']=[['Spire of Vahzl']]
byn('Futile Thinker')  # already cleared markers + base kit above
# Glassy Thinker: own grid (Slashing +50 only, rest unknown) -> generic guard shows ResistGrid
gt=byn('Glassy Thinker')
gt['nm']=True; gt['det']=list(DET3); gt['crys']='Varies'
gt['wk']=[['Slashing','+50%']]; clr(gt,'st')
gt['ab']=['Empty Cutter','Negative Whirl','Pain Sync','Shadow Spread','Stygian Vapor','Trinary Tap','Winds of Promyvion']
gt['zones']=[['Reisenjima Henge']]
gt['drops']='Adad Amulet, Knobkierrie, Adapa Shield'
gt['notes']=['Random spawn on floor 3 as one of three possible mini-bosses.','TP-move frequency rises as its HP falls, eventually spamming moves near ~10% HP.','Estimated ~1400 evasion; hits fairly hard (300-800 to non-tanks).','Trades for a Thought Crystal.']
fn['Thinker']=["Empty 'Core' family: each Thinker has an elemental Core that fixes its resistances \u2014 swipe the resist grid to see all eight Core alignments.",
 'Uses tiered drain/absorb moves (Binary/Spirit/Trinary) plus status moves; Shadow Spread is used only by notorious monsters.',
 'Glassy Thinker is a Reisenjima mini-boss with its own fixed resistance profile.']

# ===== guards =====
assert not [k for m in mobs.values() for k,v2 in m.items() if v2 is None], 'NULL LEAK'
und=[a for v in mobs.values() for a in (v.get('ab') or []) if a not in ab]
und=[a for a in und if byn]  # keep list
undset={a for v in mobs.values() if v.get('fam') in ('Receptacle','Seether','Thinker') for a in (v.get('ab') or []) if a not in ab}
assert not undset, f'UNDEFINED in new fams: {undset}'

json.dump(d, open(P,'w'), separators=(', ', ': '), ensure_ascii=False)
print('created defs:', created)
print('eco:', {f:fe[f] for f in ['Receptacle','Seether','Thinker']})
print('resist_sets keys:', list(frs.keys()))
print('family_eco count:', len(fe), '| family_notes count:', len(fn), '| abilities:', len(ab))
print('file-wide undefined refs:', len(set(a for v in mobs.values() for a in (v.get('ab') or []) if a not in ab)))
