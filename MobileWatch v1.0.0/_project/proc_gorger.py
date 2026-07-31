import json, copy
P='app/src/main/assets/mobs.json'
d=json.load(open(P)); mobs=d['mobs']; AB=d['abilities']

# 1) resist sets: Gorger == Craver (pixel-verified identical, all 8 Cores)
d['family_resist_sets']['Gorger']=copy.deepcopy(d['family_resist_sets']['Craver'])
# 2) eco
d['family_eco']['Gorger']='Empty'
# 3) family notes
d['family_notes']['Gorger']=[
 "Empty-type. Each Gorger has an elemental \"Core\" that fixes its resistances \u2014 swipe the resist grid to the Core you are facing. Each Core resists its own element and the one it beats on the wheel, and is weak to the element that beats it.",
 "Possess the Magic Defense Bonus trait and are aspirable. Gorgers in the original three Promyvions likely have +10 MDB; those in Promyvion-Vahzl have +12 MDB.",
 "Blessing Sync (NM only) copies status enhancements from nearby players, including normally non-dispellable buffs (e.g. Dematerialize, Aftermath). Copying many effects grants a strong Damage Taken reduction \u2014 up to full immunity; dispel the stolen buffs to remove it. Enfeebling effects on the Gorger also count toward the reduction.",
 "Fission (NM only) summons an Offspring."
]
# 4) abilities (create missing; enrich Stygian Flatus with its ice element icon)
new_ab={
 "Promyvion Barrier":{"d":"Gains a +20% Defense Bonus.","t":"Enhancing","tgt":"Self","r":"Self"},
 "Quadratic Continuum":{"d":"Four-hit physical attack; inflicts a -20% Attack penalty on itself afterward.","t":"Physical","tgt":"Single","r":"Melee"},
 "Vanity Drive":{"d":"Conal physical damage.","t":"Physical","tgt":"Cone","r":"Cone"},
 "Blessing Sync":{"d":"Copies status enhancements from players within ~10'.","t":"Enhancing","tgt":"AoE","r":"10'",
   "notes":"NM only. Copies even normally non-dispellable buffs (e.g. Dematerialize, Aftermath). Copying many effects grants a strong Damage Taken reduction, up to full immunity; dispel the stolen buffs to remove it. Enfeebling effects on it also count toward the reduction."},
 "Fission":{"d":"Summons an Offspring.","t":"Special","tgt":"Self","notes":"NM only."},
}
for k,v in new_ab.items():
    if k not in AB: AB[k]=v
# enrich existing Stygian Flatus: add ice element (blue gem in Type column)
if 'Stygian Flatus' in AB and not AB['Stygian Flatus'].get('el'):
    AB['Stygian Flatus']['el']='Ice'

# 5) per-mob stamp
BASE=["Promyvion Barrier","Quadratic Continuum","Spirit Absorption","Stygian Flatus","Vanity Drive"]
NMKIT=BASE+["Blessing Sync","Fission"]
NM_MEMBERS={'Hadal Mirror','Hadal Satiator','Neoingurgitator','Procreator','Propagator','Satiator','Warder of Loyalty','Depths Digester','Glassy Gorger'}
custom_kit={
 'Depths Digester':["Stygian Flatus","Promyvion Barrier"],                                   # page: only these two
 'Glassy Gorger':["Blessing Sync","Spirit Absorption","Stygian Flatus","Vanity Drive","Quadratic Continuum"],
}
zones={
 'Gorger':[["Promyvion-Dem","29-40"],["Promyvion-Vahzl","54-60"]],
 'Satiator':[["Promyvion-Dem","38"]],
 'Depths Digester':[["Abyssea-Konschtat"]],
 'Glassy Gorger':[["Reisenjima Henge"]],
 'Warder of Loyalty':[["Escha RuAun"]],
 'Ingester':[["Spire of Dem"]],'Neoingester':[["Spire of Dem"]],'Neogorger':[["Spire of Dem"]],
 'Neosatiator':[["Spire of Dem"]],'Progenerator':[["Spire of Dem"]],
 'Procreator':[["Spire of Vahzl"]],'Ingurgitator':[["Spire of Vahzl"]],'Neoingurgitator':[["Spire of Vahzl"]],
 'Propagator':[["Promyvion-Vahzl"]],
}
gorger_keys=[k for k,v in mobs.items() if v.get('fam')=='Gorger']
for k in gorger_keys:
    m=mobs[k]; nm=m.get('n')
    m['det']=["Sight","Sound","Scent"]              # family box: 3 red icons; strips bad True-Sight stamps
    if not m.get('crys'): m['crys']='Varies'         # Empty core -> crystal varies per individual
    m['job']='Warrior'                               # Typical Job (RDM sub -> notes)
    # kit
    if nm in custom_kit: m['ab']=custom_kit[nm]
    elif nm in NM_MEMBERS: m['ab']=list(NMKIT)
    else: m['ab']=list(BASE)
    # clear obsolete 'Varies' wk/st markers (Satiator etc.)
    for f in ('wk','st'):
        if f in m and m[f]==[["Varies",None]]: del m[f]
    # zones
    if nm in zones: m['zones']=zones[nm]

# base Gorger level
mobs['gorger']['lv']=[29,60]; mobs['gorger']['nm']=None if not mobs['gorger'].get('nm') else mobs['gorger'].get('nm')
if mobs['gorger'].get('nm') is None: mobs['gorger'].pop('nm',None)

# per-mob refinements
# Glassy Gorger: own grid (Slashing 150% weak; all else '?'=unknown -> not recorded), nm, drops, job already Warrior
gg=mobs['glassy gorger']; gg['nm']=True; gg['wk']=[["Slashing","+50%"]]
gg['drops']="Kishar Ring, Enki Strap, Erra Pendant"
# Depths Digester: drops already good; add spawn coord note is n/a (roaming). keep existing drops/spawn.
# Satiator: move KIs to notes, clear drops; spawn coord
sa=mobs['satiator']; sa['drops'] and None
sa['notes']=["Spawns around (G-11/12) in Promyvion-Dem.","Drops the Satiator Remnant and Beryl Memosphere key items."]
sa.pop('drops',None)
# Warder of Loyalty: remove KI from drops -> notes, add spawn note
wl=mobs['warder of loyalty']
wl['drops']="Vatic Byrnie, Deceiver's Torque, Lissome Necklace"
wl['notes']=["Occasionally spawns from defeating Eschan Clionids on Clionid island (portal 13).","Drops the Nonary nazar key item."]

# 7) Usurper (Craver family) — Image 8 adds the Abyssea-Tahrongi zone + coords + title; clean the Atma from drops
us=mobs['usurper']
us['zones']=[["Abyssea-Tahrongi","95-96"]]
us['drops']="Ocelot Trousers, Entois Trousers, Hako Hachimaki, Balance Jewel, Balance Stone"
us['notes']=["Title: Usurper Deposer.","Can spawn around (I-6), (G-4), or (G-6).","Grants the Atma of the Siren Shadow."]

# ---- GUARDS ----
assert not [k for mm in mobs.values() for k,v in mm.items() if v is None], "NULL POISON"
gu=[a for a in (list(gg['ab'])+BASE+NMKIT+custom_kit['Depths Digester']) if a not in AB]
assert not gu, ("UNDEFINED GORGER ABILITY REFS", gu)
# no [Varies,null] markers left on Gorger
leftover=[mobs[k]['n'] for k in gorger_keys if any(mobs[k].get(f)==[["Varies",None]] for f in ('wk','st'))]
assert not leftover, ("LEFTOVER VARIES MARKERS", leftover)

json.dump(d, open(P,'w'), separators=(', ', ': '), ensure_ascii=False)
print("OK. Gorger members:",len(gorger_keys))
print("family_resist_sets keys:", list(d['family_resist_sets'].keys()))
print("family_eco Gorger:", d['family_eco']['Gorger'])
print("new/updated abilities present:", all(x in AB for x in new_ab))
print("Glassy Gorger:", json.dumps(mobs['glassy gorger'],ensure_ascii=False))
print("Depths Digester ab:", mobs['depths digester']['ab'])
print("Satiator:", json.dumps(mobs['satiator'],ensure_ascii=False))
print("Usurper zones:", mobs['usurper'].get('zones'))
