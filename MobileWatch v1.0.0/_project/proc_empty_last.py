import json, copy
P='app/src/main/assets/mobs.json'
d=json.load(open(P)); mobs=d['mobs']; AB=d['abilities']; FRS=d['family_resist_sets']

# ---------- RESIST SETS ----------
# Weeper == Craver (pixel-verified identical, incl. 2-weak Wind)
FRS['Weeper']=copy.deepcopy(FRS['Craver'])
# Wanderer == Craver EXCEPT Wind has only ONE weakness (Ice); Water is 100% not 150%
wander_sets=copy.deepcopy(FRS['Craver'])
for s in wander_sets:
    if s['label']=='Wind Core':
        s['wk']=[["Ice","+50%"]]        # drop Water; st (Wind,Earth) unchanged
FRS['Wanderer']=wander_sets

d['family_eco']['Weeper']='Empty'; d['family_eco']['Wanderer']='Empty'

# ---------- ABILITIES ----------
newab={
 # Wanderer
 "Aura of Persistance":{"d":"Gains a +22% Defense Bonus.","t":"Enhancing","tgt":"Self","r":"Self"},
 "Empty Beleaguer":{"d":"Area-of-effect physical damage.","t":"Physical","tgt":"AoE","r":"AoE"},
 "Mirage":{"d":"Gains a +40 Evasion Bonus.","t":"Enhancing","tgt":"Self","r":"Self"},
 # Weeper
 "Auroral Drape":{"d":"Area-of-effect Blind (-50) and Silence.","t":"Enfeebling","tgt":"AoE","r":"10'","fx":["Blind","Silence"]},
 "Vacuous Osculation":{"d":"Single-target physical damage; inflicts Poison and Plague.","t":"Physical","tgt":"Single","r":"Melee","fx":["Poison","Plague"]},
 "Hexagon Belt":{"d":"Gains a +22% Defense Bonus.","t":"Enhancing","tgt":"Self","r":"Self"},
}
for k,v in newab.items():
    if k not in AB: AB[k]=v
# enrich the Vanity Dive stub (distinct from Gorger's Vanity Drive/Conal)
AB['Vanity Dive']={"d":"Single-target physical damage.","t":"Physical","tgt":"Single","r":"7 Yalms"}
# Empty Cutter already exists (good desc) -> reuse for Weeper

# ---------- FAMILY NOTES ----------
d['family_notes']['Weeper']=[
 "Empty-type. Each Weeper has an elemental \"Core\" that fixes its resistances \u2014 swipe the resist grid to the Core you are facing. Each Core resists its own element and the one it beats on the wheel, and is weak to the element that beats it.",
 "Innate -10% Defense penalty. Possess the Magic Defense Bonus trait and are aspirable. Weepers in the original three Promyvions likely have +10 MDB; those in Promyvion-Vahzl have +12 MDB; Apex Woeful Lamenters have +14 MDB.",
 "Each Weeper also has Memory of [its element] \u2014 a 10' AoE nuke matching its Core element (e.g. a Fire-Core Weeper uses Memory of Fire)."
]
d['family_notes']['Wanderer']=[
 "Empty-type. Each Wanderer has an elemental \"Core\" that fixes its resistances \u2014 swipe the resist grid to the Core you are facing. NOTE the Wind Core differs from other Empty families: it is weak to Ice only (not Ice + Water).",
 "Possess MP and the Magic Defense Bonus trait. Family has an innate Evasion Bonus and a -10% Defense penalty (e.g. Apex Idle Drifters have +40 evasion)."
]

# ---------- MEMBER STAMPS ----------
WEEPER_KIT=["Auroral Drape","Empty Cutter","Vacuous Osculation","Hexagon Belt"]
WANDER_KIT=["Aura of Persistance","Empty Beleaguer","Mirage","Vanity Dive"]

def clear_varies(m):
    for f in ('wk','st'):
        if m.get(f)==[["Varies",None]]: del m[f]

# WEEPER
for k in [k for k,v in mobs.items() if v.get('fam')=='Weeper']:
    m=mobs[k]; clear_varies(m)
    m['det']=["Sight","Sound","Scent"]      # family box: 3 icons
    if not m.get('crys'): m['crys']='Varies'
    m['job']='Warrior'                        # Typical Job Warrior (RDM sub)
    m['ab']=list(WEEPER_KIT)
# WANDERER
for k in [k for k,v in mobs.items() if v.get('fam')=='Wanderer']:
    m=mobs[k]; clear_varies(m)
    m['det']=["Sight","True Sight","Sound","Scent"]   # family box: 4 icons (extra True Sight)
    if not m.get('crys'): m['crys']='Varies'
    m.pop('job',None)                          # Wanderer box has NO Typical Job
    m['ab']=list(WANDER_KIT)

# ---- per-mob refinements ----
# WEEPER std
we=mobs['weeper']; we['lv']=[25,57]
we['zones']=[["Promyvion-Holla","25-37"],["Promyvion-Dem","25-37"],["Promyvion-Mea","25-37"],["Promyvion-Vahzl","50-57"],["Spire of Holla"]]
# Apex Woeful Lamenter
awl=mobs['apex woeful lamenter']; awl['zones']=[["Promyvion-Holla"],["Promyvion-Dem"],["Promyvion-Mea"],["Promyvion-Vahzl"]]
# Wailer (NM)
wa=mobs['wailer']; wa['zones']=[["Promyvion-Vahzl"]]
wa['notes']=["Forced spawn by trading a Coveter Remnant to the ??? at (L-6), fourth level.","Drops the Recollection of Animosity and White Memosphere key items."]
wa.pop('drops',None)
# Lachrymater (NM)
la=mobs['lachrymater']; la['zones']=[["Abyssea-Tahrongi"]]; la['crys']='None'; la['drops']="Witchstone"
la['notes']=["Pop: trade a Moaning Vestige to the ??? at (G-10) in Abyssea-Tahrongi.","Drag onto the (G-10) spawn point to spawn Myrmecoleon."]
# Lamenter (Monster, drops the Moaning Vestige pop item)
lm=mobs['lamenter']; lm['lv']=[75,90]; lm['zones']=[["Abyssea-Tahrongi","75-90"]]; lm['crys']='None'
lm['det']=["Sight","Sound","Scent"]; lm['drops']="Moaning Vestige"
lm['notes']=["Spawns around (G-10). Its Moaning Vestige is the pop item for Lachrymater."]

# WANDERER std
wd=mobs['wanderer']; wd['lv']=[22,56]
wd['zones']=[["Promyvion-Dem","22-36"],["Promyvion-Holla","22-36"],["Promyvion-Mea","22-36"],["Promyvion-Vahzl","49-56"],["Spire of Dem"]]
# Stray (Wanderer-family regular)
st=mobs['stray']; st['lv']=[29,51]
st['zones']=[["Promyvion-Dem","29-31"],["Promyvion-Holla","29-31"],["Promyvion-Mea","29-31"],["Promyvion-Vahzl","39-51"]]
# Apex Idle Drifter
aid=mobs['apex idle drifter']; aid['zones']=[["Promyvion-Dem"],["Promyvion-Holla"],["Promyvion-Mea"],["Promyvion-Vahzl"]]
# Deviator (NM)
dv=mobs['deviator']; dv['zones']=[["Promyvion-Vahzl"]]
dv['notes']=["Forced spawn by trading a Cerebrator Remnant to the ??? at (L-10), third level.","Drops the Recollection of Suffering and White Memosphere key items."]
dv.pop('drops',None)
# Meanderer (Abyssea, class Monster)
me=mobs['meanderer']; me['zones']=[["Abyssea-Konschtat"]]; me['det']=["Sight","True Sight","Sound","Scent"]
me['notes']=["Found frequently around Veridical Conflux #04 in Abyssea-Konschtat, but also elsewhere in the zone."]

# ---------- GUARDS ----------
assert not [1 for mm in mobs.values() for v in mm.values() if v is None], "NULL POISON"
refs=set(WEEPER_KIT+WANDER_KIT)
gu=[a for a in refs if a not in AB]; assert not gu,("UNDEF ABILITY",gu)
left=[mobs[k]['n'] for k,v in mobs.items() if v.get('fam') in ('Weeper','Wanderer') and any(mobs[k].get(f)==[["Varies",None]] for f in ('wk','st'))]
assert not left,("LEFTOVER VARIES",left)

json.dump(d, open(P,'w'), separators=(', ', ': '), ensure_ascii=False)
print("OK.")
print("resist_sets keys:", list(FRS.keys()))
print("Wanderer Wind set:", [s for s in FRS['Wanderer'] if s['label']=='Wind Core'][0])
print("Weeper==Craver:", FRS['Weeper']==FRS['Craver'], "| Wanderer==Craver:", FRS['Wanderer']==FRS['Craver'])
print("eco:", d['family_eco']['Weeper'], d['family_eco']['Wanderer'])
print("abilities now:", len(AB))
for k in ['weeper','wanderer','lachrymater','lamenter','deviator','meanderer']:
    print(" ",k,"->",json.dumps(mobs[k],ensure_ascii=False)[:180])
