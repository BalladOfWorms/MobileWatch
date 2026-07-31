#!/usr/bin/env python3
"""rev 383 — the TUBES family is born; spirit + get folded; the 3 tubes I wrongly deleted come back.

USER: Bhogbigg's Grenade + Bhogbigg's Vial panels, the Tubes CATEGORY page, an Eschan Il'aern's
Spirit blurb, the Kutkha's Get page, and a 3-line screenshot:
  "tube is new family, image included. i guess it goes in unclassified. and do we have these
   abilities already documented? the spirit goes with other spirits like fire spirit. get is
   lesser bird. mobs in last screenshot can be removed completely"

!! THE TUBES CATEGORY PAGE'S NM TABLE NAMES `Binding Tube (Mob)`, `Paralyzing Tube (Mob)` and
`Silencing Tube (Mob)` — the three records I classified as STRUCTURES and deleted at r374. They are
real mobs. Restored here with the family stamp; their original rows were bare fam=None stubs, so
nothing but the key was ever lost.

Guards: null-poison assert before dump; delete targets must exist; refuse any delete target that
has a `fam` or `zones` (rule 389); print cross-references from surviving records.
"""
import json, collections

P = 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M, AB = d['mobs'], d['abilities']

# ============================================================ 1. THE TUBES FAMILY
FAM = 'Tubes'
assert FAM not in d['families'], 'family already exists'
d['families'] = sorted(d['families'] + [FAM])
d['family_eco'][FAM] = 'Unclassified'          # page: Type = Unclassified
d['family_icons'][FAM] = 'Tubes.jpg'
d['family_notes'][FAM] = [
    'Crystal War smart bombs designed by Adelheid Sturm to cripple the forces of the Beastmen '
    'Confederate. These levitating bombs detonate after a set time once a target is close, and '
    'each releases an area-of-effect blast that inflicts a status ailment.',
    'A large number were stolen from Bastok by the Quadav during the raids on Grauberg. The Quadav '
    'shared them with the Goblins, who reverse-engineered them into very potent poison-inducing '
    'vials and flasks and sold those on to the Orcish Hosts.',
    'Immobile, and despawns after using an ability.',
    'Cannot be charmed and cannot be used in Pankration. Aspir and Drain both work.',
    'Each blast is locked to its own type: Silencing Blast to Silencing Tubes, Binding Blast to '
    'Binding Tubes, Paralyzing Blast to Paralyzing Tubes. Noxious Spray carries no such '
    'restriction. All four appear in Wings of the Goddess areas.',
]

# Family standard from the category page's Family Information box.
TUBE_STAMP = dict(fam=FAM, agg=True, det=['True Sound'])   # Common Behavior: A, T(H)

# ------------------------------------------------- 2. NEW ABILITY DEFINITIONS
# The category page's Special Abilities table is TEXT — it gives no Type icon, so `t` stays UNSET
# rather than guessed (the Quake Blast / Gravitic Horn precedent).
NEW_AB = {
    'Silencing Blast': {'d': 'Area-of-effect Silence.', 'tgt': 'AoE', 'fx': ['Silence'],
                        'notes': 'Only used by Silencing Tubes.'},
    'Binding Blast': {'d': 'Area-of-effect Bind.', 'tgt': 'AoE', 'fx': ['Bind'],
                      'notes': 'Only used by Binding Tubes.'},
    'Paralyzing Blast': {'d': 'Area-of-effect Paralysis.', 'tgt': 'AoE', 'fx': ['Paralysis'],
                         'notes': 'Only used by Paralyzing Tubes.'},
    'Noxious Spray': {'d': 'Area-of-effect Poison.', 'tgt': 'AoE', 'fx': ['Poison']},
}
for n, v in NEW_AB.items():
    if n in AB:
        print('  ability already defined, skipped:', n)
    else:
        AB[n] = v
print('=== abilities: Helldive already defined ->', 'Helldive' in AB)

# ---------------------------------------------- 3. STAMP THE TWO BHOGBIGG ADDS
for k, kit, move_note in [
    ("bhogbigg's grenade",
     ['Silencing Blast', 'Paralyzing Blast', 'Binding Blast'],
     'Uses either Silencing Blast, Paralyzing Blast or Binding Blast, then despawns.'),
    ("bhogbigg's vial", ['Noxious Spray'], 'Uses Noxious Spray, then despawns.'),
]:
    v = M[k]
    assert not v.get('fam'), k
    v.update(TUBE_STAMP)
    v['nm'] = True
    v['ab'] = kit
    v['zones'] = [['La Vaule [S]']]
    v['spawn'] = 'One spawn in La Vaule [S], summoned by Feebleschemer Bhogbigg.'
    v['notes'] = ['Summoned by Feebleschemer Bhogbigg.', move_note, 'Roughly 100-150 HP.']
    print('  stamped', k)

# --------------------------------- 4. RESTORE THE 3 TUBES WRONGLY DELETED AT r374
RESTORE = {
    'silencing tube': ('Silencing Tube', ['Silencing Blast']),
    'binding tube': ('Binding Tube', ['Binding Blast']),
    'paralyzing tube': ('Paralyzing Tube', ['Paralyzing Blast']),
}
for k, (name, kit) in RESTORE.items():
    assert k not in M, 'already present: ' + k
    rec = dict(n=name)
    rec.update(TUBE_STAMP)
    rec['ab'] = kit
    rec['notes'] = ['Found in Wings of the Goddess areas.']
    M[k] = rec
    print('  RESTORED', k, '->', name)

# ==================================================== 5. TWO SINGLE FOLDS
# `eschan il'aern's spirit` — USER: "the spirit goes with other spirits like fire spirit".
# The file's home for mob-summoned spirits/elementals/avatars is `Adversary Avatar` (eco Avatar,
# 30 members, family note "Avatars and elementals summoned by enemy mobs rather than by players").
# Decisive corroboration: the SAME owner's `aern's elemental` and `aern's avatar` are both filed
# there. Its own grid/spells are kept — Adversary Avatar has no uniform grid.
sp = M["eschan il'aern's spirit"]
assert not sp.get('fam')
sp['fam'] = 'Adversary Avatar'
sp['zones'] = [["Escha - Ru'Aun"]]
sp['notes'] = ['Summoned by Eschan Il\u2019aern on the Escha - Ru\u2019Aun islands reached through '
               'portals 3, 6 and 9.']
print('  folded eschan spirit -> Adversary Avatar')

# `kutkha's get` — USER: "get is lesser bird". Page says Family: Birds; the file splits Birds into
# Greater Bird / Lesser Bird, and the user picked Lesser.
LB = [v for v in M.values() if v.get('fam') == 'Lesser Bird']
crys = collections.Counter(v.get('crys') for v in LB).most_common(1)[0]
job = collections.Counter(v.get('job') for v in LB).most_common(1)[0]
print('  Lesser Bird standard: crys %r (%d/%d)  job %r (%d/%d)' % (
    crys[0], crys[1], len(LB), job[0], job[1], len(LB)))
g = M["kutkha's get"]
assert not g.get('fam')
g['fam'] = 'Lesser Bird'
g['nm'] = True
g['agg'] = True
g['lnk'] = True
g['det'] = ['True Sight']          # page Notes column: A, T(S), L
g.setdefault('crys', crys[0])
g.setdefault('job', job[0])
# Page states a SMALLER kit outright, so trim rather than stamp the family kit:
g['ab'] = ['Helldive']
g['zones'] = [['Balgas Dais']]
g['spawn'] = 'Six spawn in Balgas Dais for the KCNM The V Formation.'
g['notes'] = ['Appears in the Kindred\u2019s Crest NM battle The V Formation, assisting Kutkha.',
              'Does not melee. It ceaselessly uses Helldive in sync with its companions.']
# The page's lone "Weak against" gem measures (140,136,202) = Ice at distance 18.7 (next best
# 68.7), which CONFIRMS the Ice weakness already stored. Grid left untouched.
print('  folded kutkha\'s get -> Lesser Bird, grid untouched (Ice confirmed)')

# =============================== 6. THE 3 PETS THE USER ASKED TO DELETE — GUARD CHECK
ASKED = ["assassin's apprentice", "commander's pet", "volte's pet"]
print('\n=== DELETE GUARD (rule 389) ===')
refused = []
for k in ASKED:
    v = M.get(k)
    if v is None:
        refused.append((k, 'missing'))
    elif v.get('fam'):
        refused.append((k, 'has fam %r' % v['fam']))
    elif v.get('zones'):
        refused.append((k, 'has zones %s  content=%s  lv=%s' % (
            v['zones'], v.get('content'), v.get('lv'))))
for k, why in refused:
    print('  REFUSED  %-24s %s' % (k, why))
print('  deleting %d of %d — HELD FOR CONFIRMATION, see the reply' % (len(ASKED) - len(refused), len(ASKED)))

# ================================================================ 7. GUARDS + WRITE
bad = [(k, f) for k, m in M.items() for f, val in m.items() if val is None]
assert not bad, bad[:10]
bad = [(k, f) for k, a in AB.items() for f, val in a.items() if val is None]
assert not bad, bad[:10]
zn = {x['name'] for x in json.load(open('app/src/main/assets/zones.json', encoding='utf-8'))['zones']}
def norm(s): return s.replace('\u2019', "'").replace("'", '').lower()
zi = {norm(z) for z in zn} | {norm('Escha - Ru\u2019Aun')}
for k in ["bhogbigg's grenade", "bhogbigg's vial", "kutkha's get", "eschan il'aern's spirit"]:
    for z in (M[k].get('zones') or []):
        assert norm(z[0]) in zi, (k, z[0])
assert FAM in d['family_eco'] and FAM in d['family_icons']
# NOTE: 16 pre-existing PHANTOM families (Beasts, Chaos, Elementals, ...) are in `families` with
# no `family_eco` entry and 0 members — that is decision item 2, not something this rev introduced.
noeco = [f for f in d['families'] if f not in d['family_eco']]
print('  pre-existing families with no eco entry: %d %s' % (len(noeco), noeco))

json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('\nmobs %d | abilities %d | families %d | bucket %d' % (
    len(M), len(AB), len(d['families']), sum(1 for v in M.values() if not v.get('fam'))))
