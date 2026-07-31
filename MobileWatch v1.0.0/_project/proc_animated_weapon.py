import json
d=json.load(open('mobs.json'))
m=d['mobs']; ab=d['abilities']; fe=d['family_eco']; fn=d['family_notes']

def clr(mob,*keys):
    for k in keys:
        if k in mob: del mob[k]

# ---------- ECO (USER: "unclassified family"; family box Type=Unclassified) ----------
fe['Animated Weapon']='Unclassified'

# ---------- FAMILY NOTES ----------
fn['Animated Weapon']=[
  "Immune to Sleep, Silence, and Stun, but susceptible to Lullaby.",
  "Satellite and Animated Weapons have a Magic Defense of 160.",
  "Members mimic various jobs \u2014 each Animated/Satellite weapon type behaves as a specific job.",
]

# ---------- TWO GRIDS by name (per-member; NOT a swipe) ----------
SAT_WK=[["Fire","+30%"],["Wind","+15%"],["Lightning","+15%"],["Light","+30%"],["Earth","+15%"],["Water","+15%"]]
SAT_ST=[["Magical","-12.5%"],["Ice","-15%"],["Dark","-15%"]]
ANI_WK=[["Fire","+15%"],["Light","+15%"]]
ANI_ST=[["Magical","-12.5%"],["Ice","-30%"],["Dark","-30%"]]

JOBMAP={'THF':'Thief','WAR':'Warrior','RNG':'Ranger','WHM':'White Mage','BRD':'Bard','MNK':'Monk',
        'NIN':'Ninja','PLD':'Paladin','DRK':'Dark Knight','DRG':'Dragoon','BLM':'Black Mage','SAM':'Samurai'}

members=[k for k,v in m.items() if v.get('fam')=='Animated Weapon']
for k in members:
    v=m[k]
    v['det']=['Sound']                      # family box = lone red speaker; strip [Sight,Sound,True Sight] on animated*
    if v.get('job') in JOBMAP:              # long-form published abbreviations
        v['job']=JOBMAP[v['job']]
    if k.startswith('satellite '):
        v['wk']=[list(x) for x in SAT_WK]; v['st']=[list(x) for x in SAT_ST]
    else:                                   # animated* + arcus blades
        v['wk']=[list(x) for x in ANI_WK]; v['st']=[list(x) for x in ANI_ST]
    # crys: family box blank -> KEEP existing (Dark on animated*, None on satellite*/arcus)

# ---------- ZONES ----------
for k in members:
    if k.startswith('animated '):
        m[k]['zones']=[["Dynamis-Xarcabard","82"]]     # Event Appearances (all 16)
# satellite* left unzoned (no zone data in shots)
m['arcus blades']['zones']=[["King Ranperre's Tomb","109"],["Fei'Yin","125"],["Ranguemont Pass","135"]]
m['arcus blades']['lv']=[109,135]

# ---------- ARCUS BLADES kit + spell cleanup + notes ----------
# Dire Whorl def exists but was scoped to another user + missing the Stun/10' from Image 5 -> enrich
dw=ab['Dire Whorl']
dw['d']="Spins around, dealing physical damage to targets in a 10' area of effect. Additional effect: Stun."
dw['t']="Physical"; dw['tgt']="AoE"; dw['r']="10' radial"; dw['fx']=["Stun"]
clr(dw,'notes')   # drop the now-false "Used only by King Goldemar's merchandise." exclusive claim
# remove the junk descriptor 'Tier IV-VI Elemental Magic' from arcus sp (not a castable spell name)
m['arcus blades']['sp']=[s for s in (m['arcus blades'].get('sp') or []) if s!='Tier IV-VI Elemental Magic']
m['arcus blades']['notes']=[
  "~17,000 HP. Spawned during Epiphany at the Hazy Rune behind the Strange Apparatus.",
  "Casts single-target tier IV-VI elemental magic, Comet, and Holy II by day of the week: starts on the day's element and escalates in tier (IV\u2192VI) the longer it stays before moving to the next element. Absorbs magic damage of its current element.",
  "Most defensive buffs (Blink, Utsusemi, Shell, Phalanx, Protect, etc.) make it respond with Dispelga (removes two buffs) and enrage it \u2014 significantly higher power and higher-tier nukes; Rune Fencer buffs (Valiance, Vallation, One for All) do NOT trigger this.",
  "Melee and Dire Whorl damage are low relative to its magic damage. Trait: Fast Cast.",
]

# ---------- FIX 31 int-pair zone-levels file-wide (render as literal "[a,b]") -> string "a-b" ----------
fixed=0
for v in m.values():
    for p in (v.get('zones') or []):
        if isinstance(p,list) and len(p)>1 and isinstance(p[1],list):
            a=p[1]
            p[1]=str(a[0]) if len(a)>=1 and (len(a)<2 or a[0]==a[1]) else f"{a[0]}-{a[1]}"
            fixed+=1

# ---------- null-poison guard ----------
for v in m.values():
    for k in [k for k,val in list(v.items()) if val is None]:
        del v[k]

json.dump(d,open('mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print("written; int-pair zone-levels fixed:",fixed)

# ---------- VERIFY ----------
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']
print("mobs",len(m),"abilities",len(ab),"family_eco",len(d['family_eco']),"family_notes",len(d['family_notes']),"resist_sets",len(d['family_resist_sets']),"subtypes",len(d['family_subtypes']))
print("Animated Weapon members:",len([k for k,v in m.items() if v.get('fam')=='Animated Weapon']),"| eco:",d['family_eco'].get('Animated Weapon'))
bad=[(k,kk) for k,v in m.items() for kk,vv in v.items() if vv is None]; print("top-level None values:",len(bad))
und=[a for k,v in m.items() if v.get('fam')=='Animated Weapon' for a in (v.get('ab') or []) if a not in ab]; print("family undefined refs:",und)
print("remaining int-pair zone-levels:",sum(1 for v in m.values() for p in (v.get('zones') or []) if isinstance(p,list) and len(p)>1 and isinstance(p[1],list)))
for k in ['satellite guns','animated hammer','arcus blades']:
    v=m[k]; print(f"  {k}: eco={v.get('eco')} det={v.get('det')} job={v.get('job')!r} crys={v.get('crys')!r} wk={v.get('wk')} st={v.get('st')} zones={v.get('zones')}")
print("  Dire Whorl def:",ab['Dire Whorl'])
"" 
