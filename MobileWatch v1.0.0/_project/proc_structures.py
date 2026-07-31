import json
d=json.load(open('mobs.json'))
m=d['mobs']; ab=d['abilities']; fe=d['family_eco']; fn=d['family_notes']; frs=d['family_resist_sets']

def clr(mob,*keys):
    for k in keys:
        if k in mob: del mob[k]

# ---------- ECO ----------
fe['Gyve']='Structures'
fe['Structure']='Structures'

# ---------- FAMILY NOTES ----------
fn['Gyve']=[
  "Immobile structures. Resistance to elemental offensive magic depends on the element of the Gyve/Fetter.",
  "Has a 20' enfeebling aura; the enfeebling effect is based on the element of the Gyve/Fetter.",
  "Trait \u2014 Affinity Resistance: resistance to elemental offensive magic depends on the elemental's element. Includes movement speed and gimmicks (e.g. Silence prevents TP moves).",
]
fn['Structure']=[
  "Immobile structures, related to the Gyves.",
]

# ---------- GYVE BASE GRID (family box: weapons Resist, all 8 elements Susceptible; Magical/Breath unknown) ----------
GYVE_ST=[["Physical",None],["Slashing",None],["Impact",None],["H2H",None],["Piercing",None],["Ranged",None]]
GYVE_WK=[["Fire",None],["Wind",None],["Lightning",None],["Light",None],["Ice",None],["Earth",None],["Water",None],["Dark",None]]

GYVE=['crystal fetter','elemental circle','elemental gyves','varanus','zisurru']
for k in GYVE:
    v=m[k]
    v['fam']='Gyve'
    v['wk']=[list(x) for x in GYVE_WK]
    v['st']=[list(x) for x in GYVE_ST]
    # crys None (explicit) / job blank -> leave unset; det: box blank -> keep existing per-member det

# ---------- STRUCTURE FAMILY (all-'?' box = NO grid) ----------
STRUCT_CAT=['astral box','confederate belfry','confederate mantelet','exoplate','fortification','protective ward','zvahl fortalice']
STRUCT_FOLD=['archaic mirror','goblin mine']
for k in STRUCT_CAT:
    m[k]['fam']='Structure'
# fortification carried a junk uniform -50% element grid; the Structure box is all-'?' -> clear it (assert nothing)
clr(m['fortification'],'wk','st')
# folds
for k in STRUCT_FOLD:
    m[k]['fam']='Structure'

# ---------- NM FLAGS ----------
m['zisurru']['nm']=True              # Class = Notorious Monster (own page)
m['archaic mirror']['nm']=True       # Structure's Notorious Monster table ("Archaic Mirror (Monster)")
# crystal fetter / elemental gyves / varanus / zvahl fortalice already nm=True

# ---------- ZONES ----------
def zset(k,pairs):
    m[k]['zones']=[[z,lv] for z,lv in pairs]
zset('crystal fetter',[["Provenance",None]])                                  # Provenance Watcher BC, 9 spawns -> note
zset('elemental gyves',[["Walk of Echoes",None]])                             # WotG Mission 51 - Maiden of the Dusk
zset('varanus',[["Walk of Echoes",None],["Maquette Abdhaljs-Legion",None]])   # Seventh Walk / Hall of An
zset('zisurru',[["Sheol - Gaol",None]])                                       # Odyssey (free text)
zset('archaic mirror',[["Arrapago Reef",None],["Halvung",None],["Mamook",None]])
# elemental circle -> event zone is category "Dynamis" (not a real zone) -> unzoned
# goblin mine / fortification / other Structure adversaries -> no zone in shots -> unzoned

# ---------- DROPS ----------
m['archaic mirror']['drops']="Archaic Mirror"   # validated in ffxi_items.json

# ---------- NOTES ----------
m['crystal fetter']['notes']=[
  "Approximately 5000 HP. Immobile; Provenance Watcher summons one after casting a spell, and the Fetter's element matches that spell (shown by its colour).",
  "Carries a two-debuff aura keyed to its element: Fire = Burn + Attack Down; Ice = Frost + Magic Attack Down; Wind = Choke + Evasion Down; Earth = Rasp + Defense Down; Thunder = Shock + Accuracy Down; Water = Drown + Magic Defense Down; Light = Dia + prevents HP recovery; Dark = Bio + 5-count Doom.",
  "While Fetters stand, damage to Provenance Watcher is cut sharply \u2014 about 99% with three present, 80% with two, 50% with one.",
  "Each Fetter takes only one damage type by element: Ice/Earth/Water/Dark Fetters take physical only; Light/Fire/Wind/Thunder Fetters take magical only. Twilight Scythe (melee), Requiescat, and Quick Draw damage either type.",
]
m['zisurru']['notes']=["Summoned by Odyssey NMs."]

# ---------- HYGIENE: strip any explicit top-level None values (null-poison guard) ----------
for v in m.values():
    for k in [k for k,val in list(v.items()) if val is None]:
        del v[k]

json.dump(d,open('mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print("written")

# ---------- VERIFY ----------
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']
print("mobs",len(m),"abilities",len(ab),"family_eco",len(d['family_eco']),"family_notes",len(d['family_notes']),"family_resist_sets",len(d['family_resist_sets']),"subtypes",len(d['family_subtypes']))
print("Gyve members:",[k for k,v in m.items() if v.get('fam')=='Gyve'])
print("Structure members:",[k for k,v in m.items() if v.get('fam')=='Structure'])
# null-poison guard
bad=[(k,kk) for k,v in m.items() for kk,vv in v.items() if vv is None]
print("top-level None values:",len(bad))
# undefined refs for these families
fams=('Gyve','Structure')
und=[a for k,v in m.items() if v.get('fam') in fams for a in (v.get('ab') or []) if a not in ab]
print("Gyve/Structure undefined refs:",und)
undall=[a for v in m.values() for a in (v.get('ab') or []) if a not in ab]
print("file-wide undefined refs:",len(undall))
# spot check
for k in ['crystal fetter','zisurru','fortification','archaic mirror','varanus']:
    v=m[k]; print(f"  {k}: fam={v.get('fam')} nm={v.get('nm')} zones={v.get('zones')} wk={'set' if v.get('wk') else None} st={'set' if v.get('st') else None} drops={v.get('drops')!r}")
