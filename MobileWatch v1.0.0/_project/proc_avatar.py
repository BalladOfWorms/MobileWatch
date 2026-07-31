import json
d=json.load(open('mobs.json'))
m=d['mobs']; ab=d['abilities']; fe=d['family_eco']; fn=d['family_notes']

def clr(mob,*keys):
    for k in keys:
        if k in mob: del mob[k]

ELEMS=["Fire","Wind","Lightning","Light","Ice","Earth","Water","Dark"]

# ---------- ECO (Bestiary Type "Elementals" -> stored "Elemental" to match the existing Elemental eco) ----------
fe['Avatar']='Elemental'

# ---------- FAMILY NOTES (General Notes + Prime weakness system, Image 1) ----------
fn['Avatar']=[
  "Powerful beings of Vana'diel lore \u2014 evoked by Summoners and central to many storylines.",
  "High-Tier Mission Battlefield Prime Avatars (\u2605) have an innate \u221230% damage reduction to magic, physical, and ranged, plus a potent en-spell of their element. They have four weaknesses \u2014 triggered by Weaponskills, Abilities (e.g. Provoke), offensive Magic, and offensive Pet abilities (Ready/Blood Pact/Wyvern breath/Automaton attachments). Triggering one removes the damage penalty or weakens the en-spell; the effect varies per Prime and per trigger.",
  "A proc'd weakness stuns the current action and keeps the Prime weakened until it uses Astral Flow, after which it must be re-proc'd.",
]

# ---------- 6 CELESTIAL ELEMENTAL PRIMES: absorb own element / weak opposite +50% / resist rest -95% ----------
# (confirmed by reading Ifrit + Shiva + Garuda/Titan/Ramuh/Leviathan Prime grids; A/150/5 pattern)
PAIRS={'ifrit prime':('Fire','Ice'),'shiva prime':('Ice','Fire'),'garuda prime':('Wind','Earth'),
       'titan prime':('Earth','Wind'),'ramuh prime':('Lightning','Water'),'leviathan prime':('Water','Lightning')}
for k,(own,opp) in PAIRS.items():
    v=m[k]
    v['ab_el']=[own]                                   # absorb (list of strings)
    v['wk']=[[opp,'+50%']]
    v['st']=[[e,'-95%'] for e in ELEMS if e not in (own,opp)]

# ---------- clean obvious junk placeholder tokens on non-celestial records ----------
# baa's avatar carried wk/st = ['Varies',None] placeholder -> clear (unknown grid)
clr(m["baa's avatar"],'wk','st')

# ---------- long-form job abbreviations family-wide (box: Black Mage / White Mage / Dark Knight) ----------
JOB={'BLM':'Black Mage','WHM':'White Mage','DRK':'Dark Knight','RDM':'Red Mage','BLM / RDM':'Black Mage / Red Mage'}
for k,v in m.items():
    if v.get('fam')=='Avatar' and v.get('job') in JOB:
        v['job']=JOB[v['job']]
# crys: box None -> no stamp (per-mob crys like bahamut Fire / akash Water kept). det: box "Varies" -> kept per-mob.

# ---------- null-poison guard ----------
for v in m.values():
    for k in [k for k,val in list(v.items()) if val is None]:
        del v[k]

json.dump(d,open('mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print("written")

# ---------- VERIFY ----------
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']
print("mobs",len(m),"abilities",len(ab),"family_eco",len(d['family_eco']),"family_notes",len(d['family_notes']),"resist_sets",len(d['family_resist_sets']),"subtypes",len(d['family_subtypes']))
print("Avatar members:",sum(1 for v in m.values() if v.get('fam')=='Avatar'),"| eco:",d['family_eco'].get('Avatar'))
bad=[(k,kk) for k,v in m.items() for kk,vv in v.items() if vv is None]; print("top-level None values:",len(bad))
for k in ['ifrit prime','shiva prime','garuda prime','titan prime','ramuh prime','leviathan prime',"baa's avatar",'fenrir prime','carbuncle prime']:
    v=m[k]; print(f"  {k}: job={v.get('job')!r} ab_el={v.get('ab_el')} wk={v.get('wk')} st={v.get('st')}")
