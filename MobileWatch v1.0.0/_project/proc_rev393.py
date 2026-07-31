#!/usr/bin/env python3
"""
REV 393 — three decision items answered off ten panels.

ITEM 1 CONFIRMED. "xuan wu, genbu type". The Qilin summon list spells all four
out: Xuan Wu (Genbu), Bai Hu (Byakko), Qing Long (Seiryu), Zhu Que (Suzaku) —
exactly the mapping the fold was built on, so `xuan wu` stays Adamantoise. The
same paragraph carries each one's aura and spell line, all four now merged in.

ITEM 2 CONFIRMED, INDIRECTLY AND CLEANLY. `The Briars (Galka)` and
`The Briars (Elvaan)` are two SEPARATE pages, each noting "In battle, he is
simply named The Briars". The untitled Battle Info panel names BOTH of them as
things it is stronger than — so it is neither, and `the keeper` was the right
read. **Open question raised in the doc: both Briars variants are real Rala
Waterways [U] mission bosses and the file now has neither.**

ITEM 3 ANSWERED BY THE SIXTH QUADAV'S OWN PAGE. Aa'Bho Slashburner prints
"Weak to: Lightning", which is the Quadav family table's biggest weakness
(+50%) and is absent from the contradicted grid it was wearing. Family grid
stamped, matching the five from rev 391. Its page also names all six as one
spawn set, so the shared mechanic goes on all six.

ITEM 5 ANSWERED BY FOUR ABILITY TABLES. The dangling sentences are TRIMMED TO
COMPLETE ONES rather than deleted — the fact each states is true and useful even
without the table the scrape lost.
"""
import json, os

P = 'app/src/main/assets/mobs.json'
if not os.path.exists(P):
    P = 'android/' + P
d = json.load(open(P))
M = d['mobs']; A = d['abilities']

def add_notes(m, lines):
    n = m.setdefault('notes', [])
    for b in lines:
        if b not in n:
            n.append(b)

def add_sp(m, spells):
    sp = m.setdefault('sp', [])
    added = [s for s in spells if s not in sp]
    sp.extend(added)
    return added

# ==================================================== 1. the four Qilin summons
SHARED = ("The summoned helpers have a lot of HP and are as strong as Qilin itself, "
          "so it is usually easier to keep fighting Qilin and have someone pull each "
          "summon away from the group as it spawns.")
GUARD = {
    'xuan wu':   ('Genbu',  'Poison aura',   'water',
                  ['Flood', 'Water V', 'Waterja', 'Waterga IV', 'Poisonga II']),
    'bai hu':    ('Byakko', 'Flash aura',    'light',
                  ['Holy', 'Banish IV', 'Banishga IV', 'Diaga III']),
    'qing long': ('Seiryu', 'Silence aura',  'wind',
                  ['Tornado', 'Aero V', 'Aeroja', 'Aeroga IV']),
    'zhu que':   ('Suzaku', 'Paralyze aura', 'fire',
                  ['Flare', 'Fire V', 'Firaja', 'Firaga IV']),
}
print('=== THE FOUR QILIN SUMMONS ===')
assert M['xuan wu']['fam'] == 'Adamantoise'   # item 1, confirmed by the user
for k, (alias, aura, elem, spells) in GUARD.items():
    m = M[k]
    added = add_sp(m, spells)
    add_notes(m, ["Also known as %s. Occasionally puts up a %s and casts %s-based spells."
                  % (alias, aura, elem), SHARED])
    print('  %-10s fam=%-13s alias=%-7s +sp %s' % (k, m['fam'], alias, added))
add_notes(M['zhu que'],
          ["Its melee attacks carry an additional amnesia effect."])
add_notes(M['bai hu'], ["Has high evasion."])

# ==================================================== 2. Aa'Bho + the other five
QUADAV_WK = [['Wind', '+30%'], ['Lightning', '+50%'], ['Light', '+30%'],
             ['Ice', '+30%'], ['Earth', '+30%'], ['Dark', '+30%']]
SIX = ["aa'bho slashburner", "bo'gha winterkill", "du'vha grimewind",
       "ea'zhu tremorcrag", "gi'rho wrathstorm", "he'dho spatesurge"]
SET_NOTES = [
    "One of six Quadav that spawn together for the quest Succor to the Sidhe: "
    "Aa'Bho Slashburner, Bo'Gha Winterkill, Du'Vha Grimewind, Ea'Zhu Tremorcrag, "
    "Gi'Rho Wrathstorm and He'Dho Spatesurge.",
    "Each of the six casts magic tied to one specific element.",
    "Casts progressively stronger spells as the others die — starting at the Tier IV "
    "spells, then Ancient Magic II, then -aga III, then an enfeebling or enhancing -ga.",
]
print('\n=== THE SIX ROLANBERRY QUADAV ===')
print("  Aa'Bho's page prints 'Weak to: Lightning' — the family table's +50%, and a row")
print("  the contradicted grid did not have. That is what settles decision item 3.")
for k in SIX:
    m = M[k]
    m['wk'] = [r[:] for r in QUADAV_WK]
    m['st'] = []
    m['agg'] = True
    m['lnk'] = True
    m.setdefault('zones', [["Rolanberry Fields [S]"]])
    m['spawn'] = 'Quest (Succor to the Sidhe)'
    add_notes(m, SET_NOTES)
    was_nm = m.get('nm')
    m['nm'] = True
    print('  %-22s grid=family  nm %s' % (k, 'kept' if was_nm else 'SET (see below)'))
add_notes(M["aa'bho slashburner"],
          ["Aa'Bho uses Fire magic.", "Casts Dispelga as its enfeebling -ga."])
M["aa'bho slashburner"]['job'] = 'Black Mage'
print("  NM FLAG: only Aa'Bho's page has been seen and it carries the Notorious Monster")
print("  banner. The other five had no flag; set to match, since the page names all six")
print("  as one spawn set and every other Succor to the Sidhe spawn in the file is")
print("  nm-flagged. One line reverses it.")

# ==================================================== 3. the truncated ability notes
print('\n=== FOUR TRUNCATED ABILITY NOTES ===')
BST = ("When performed by a Beastmaster with Ready, it carries skillchain attributes.")
for k in ('Lamb Chop', 'Sheep Charge'):
    print('  %-13s notes: %r' % (k, A[k]['notes']))
    A[k]['notes'] = BST

print('  %-13s notes: %r' % ('Horrid Roar', A['Horrid Roar']['notes']))
A['Horrid Roar']['notes'] = "The effect varies slightly depending on which wyrm uses it."
# table: Area 1p, Type = Magical, "Dispels positive statuses and removes Enmity.
# Wipes shadows." `t` was `Enfeebling`, which is not one of BG's four categories.
A['Horrid Roar']['d'] = ("Dispels a single target's beneficial effects, removes its "
                         "enmity and wipes its shadows.")
A['Horrid Roar']['t'] = 'Magical'
A['Horrid Roar']['fx'] = ['Dispel', 'Enmity Reset']
# The Type cell has a second, dark icon. No labelled gems on the shot to match it
# against, so `el` stays UNSET rather than guessed.

print('  %-13s notes: %r' % ('Dust Cloud', A['Dust Cloud']['notes']))
A['Dust Cloud'].pop('notes')        # the whole value was a bare ":"
# table: Y' 10', Area AoE (NOT Conal — the legend lists Conal as a separate value),
# Target Player, Type = Magical + the gold element icon, effect "Damage and Blind".
A['Dust Cloud']['d'] = 'Deals damage in an area of effect. Additional effect: Blind.'
A['Dust Cloud']['r'] = "10'"
A['Dust Cloud']['tgt'] = 'AoE'
A['Dust Cloud']['fx'] = ['Damage', 'Blindness']
print("  Dust Cloud also CORRECTED: it was stored as a 10' CONE. The table's Area column")
print("  reads AoE, and the legend lists Conal as a separate value it could have used.")

# ==================================================== guards
assert not [k for m in M.values() for k, v in m.items() if v is None], 'NULL POISON'
assert not [k for a in A.values() for k, v in a.items() if v is None], 'NULL POISON (ab)'
assert not [k for k, m in M.items() if k != m['n'].lower()]
trunc = [k for k, v in A.items() if isinstance(v, dict)
         and str(v.get('notes', '')).rstrip().endswith(':')]
print('\nability notes still ending on a colon: %d %s' % (len(trunc), trunc))
assert not trunc
sets = {s['label']: s for s in d['family_resist_sets']['Elemental']}
for key, label in [('shadowfang void', 'Dark'), ('touched gefyrst', 'Gefyrst')]:
    assert M[key]['wk'] == sets[label]['wk'] and M[key]['st'] == sets[label]['st'], key
GRID_OK = {'Physical', 'Magical', 'Breath', 'Slashing', 'Impact', 'Blunt', 'H2H',
           'Piercing', 'Ranged', 'Fire', 'Wind', 'Lightning', 'Light', 'Ice',
           'Earth', 'Water', 'Dark', 'Varies'}
assert not {e[0] for m in M.values() for f in ('wk', 'st')
            for e in (m.get(f) or []) if e[0] not in GRID_OK}

json.dump(d, open(P, 'w'), separators=(', ', ': '), ensure_ascii=False)
print('\nmobs %d, abilities %d, orphans %d' %
      (len(M), len(A), sum(1 for m in M.values() if not m.get('fam'))))
