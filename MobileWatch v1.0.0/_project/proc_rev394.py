#!/usr/bin/env python3
"""
REV 394 — a file-wide sweep for the Lamiae class of problem: a value that is not
wrong about the mob, but is wrong for THIS FILE'S vocabulary, so it renders badly.

THE HEADLINE IS A NEGATIVE RESULT AND IT IS WORTH MORE THAN THE FIXES.
A detector for "the mob's NAME names a family, but `fam` says something else"
returns 79 records once the 16 empty families and substring matches are excluded
(`harpeia (nm)` filed Khimaira, `seed goblin` filed Orc, `phlebotomic slug` filed
Leech, `belladonna (nm)` filed Rafflesia, `bat eye` filed Ahriman ...). Every
single one was then checked against an INDEPENDENT witness — the record's own
ability kit — and in all 79 the kit matches the family it is filed under and NOT
the family its name suggests. `harpeia (nm)` really carries the Khimaira kit;
`seed goblin` really carries the Orc kit. **There is no second Lamiae. The
family column is sound.**

What the sweep did find is four vocabulary/shape problems, all of them cosmetic
in the data and visible on the card:
  1. 63 `crys` values that are not the file's own crystal vocabulary
  2. 2 records whose level range starts at 0
  3. 1 stray zone spelling
  4. 35 `zones` entries stored as bare strings instead of one-element lists
plus one probable typo-duplicate that is NOT touched here because deleting a
record needs your word: `will-o'the-wisp` (missing a hyphen) beside the properly
spelled `will-o'-the-wisp`.
"""
import json, os, collections

P = 'app/src/main/assets/mobs.json'
if not os.path.exists(P):
    P = 'android/' + P
d = json.load(open(P))
M = d['mobs']; A = d['abilities']
before = len(M)

# ============================================================ 1. crys vocabulary
# The file's crystal vocabulary is the eight bare element names, plus two
# deliberate words: "Varies" (118 records, the Aern/Ghrah/Craver classes whose
# crystal follows the mob's own element) and "None" (6).
OKC = {'Fire', 'Ice', 'Wind', 'Earth', 'Lightning', 'Water', 'Light', 'Dark',
       'Varies', 'None'}
CRYS_FIX = {
    'Fire Crystal': 'Fire',      # the word "Crystal" leaked in from the page
    'Earth Crystal': 'Earth',
    'Light Crystal': 'Light',
    'Thunder': 'Lightning',      # this file calls that element Lightning
    'N': 'None',                 # truncated; nothing else starts with N
    'Element': 'Varies',         # JUDGEMENT CALL — see the note below
}
print('=== 1. NON-VOCABULARY `crys` VALUES ===')
counts = collections.Counter()
for k, m in M.items():
    c = m.get('crys')
    if c in CRYS_FIX:
        counts[(c, CRYS_FIX[c])] += 1
        m['crys'] = CRYS_FIX[c]
for (o, n), c in sorted(counts.items(), key=lambda x: -x[1]):
    print('  %4d  %-14r -> %r' % (c, o, n))
print('  total %d records' % sum(counts.values()))
print("  JUDGEMENT CALL: `reactionary rampart` alone said 'Element'. Its family's other")
print("  members carry real crystals (Light x4, Lightning, Wind), so 'Element' reads as a")
print("  placeholder for 'its own element' — mapped to 'Varies', the file's word for that.")
left = sorted({m['crys'] for m in M.values() if m.get('crys') and m['crys'] not in OKC})
print('  non-vocabulary values remaining: %s' % (left or 'none'))
assert not left

# ============================================================ 2. level 0
print('\n=== 2. LEVEL RANGES STARTING AT 0 ===')
for k, m in M.items():
    lv = m.get('lv')
    if lv and lv[0] == 0:
        print('  %-14s %s -> [%d, %d]   (level 0 does not exist; the upper bound is the'
              ' measured value)' % (k, lv, lv[1], lv[1]))
        m['lv'] = [lv[1], lv[1]]
assert not [k for k, m in M.items() if m.get('lv') and m['lv'][0] < 1]

# ============================================================ 3. stray zone name
print('\n=== 3. STRAY ZONE SPELLING ===')
n = 0
for m in M.values():
    for z in (m.get('zones') or []):
        if isinstance(z, list) and z and z[0] == "Escha - Ru'Aun":
            z[0] = 'Escha RuAun'; n += 1
        elif isinstance(z, str) and z == "Escha - Ru'Aun":
            n += 1
print("  Escha - Ru'Aun -> Escha RuAun  x%d  (77 records already used the second form)" % n)

# ============================================================ 4. flat zone entries
# MobDb.kt:183-188 handles both shapes (`else e.toString() to null`), so this was
# never a crash risk — but the shape is documented as a [zone, levels] PAIR, and
# `elemental circle` had BOTH shapes inside one record's list.
print('\n=== 4. `zones` ENTRIES STORED AS BARE STRINGS ===')
recs = flat = 0
for k, m in M.items():
    zs = m.get('zones')
    if not zs:
        continue
    if any(not isinstance(z, list) for z in zs):
        recs += 1
        flat += sum(1 for z in zs if not isinstance(z, list))
        m['zones'] = [z if isinstance(z, list) else [z] for z in zs]
print('  normalised %d entries across %d records' % (flat, recs))
assert not [1 for m in M.values() for z in (m.get('zones') or []) if not isinstance(z, list)]

# ============================================================ 5. glued spell list
# `guimauve` stored eight spells run together as ONE string. The split
# reconstructs the original byte for byte, and every one of the eight is an
# established name in this file (used by 43-501 other mobs), so it is mechanical.
print('\n=== 5. GLUED SPELL LIST ===')
GLUED = 'Blizzaga IIICure VGravigaParalygaSilencegaSleepgaSlowgaStonega III'
PARTS = ['Blizzaga III', 'Cure V', 'Graviga', 'Paralyga', 'Silencega', 'Sleepga',
         'Slowga', 'Stonega III']
assert ''.join(PARTS) == GLUED
for k, m in M.items():
    sp = m.get('sp') or []
    if GLUED in sp:
        rest = [x for x in sp if x != GLUED]
        m['sp'] = rest + [x for x in PARTS if x not in rest]
        print('  %s: 1 glued string -> %d spells (%d were already in its list)'
              % (k, len(PARTS), sum(1 for x in PARTS if x in rest)))
print("  LEFT ALONE: 'Addle (AoE)', 'Stun (AoE)', 'Stun / Stun (AoE)' on mastop / tojil /")
print("  tutewehiwehi. Those are not glued — the '(AoE)' is real information about which")
print("  version the mob casts, and it reads correctly on the card.")

# ============================================================ report-only
print('\n=== REPORTED, NOT TOUCHED ===')
w1, w2 = "will-o'-the-wisp", "will-o'the-wisp"
if w1 in M and w2 in M:
    print("  PROBABLE TYPO-DUPLICATE — deleting a record needs your word, so both stand:")
    for w in (w1, w2):
        m = M[w]
        print('    %-18s lv=%-10s job=%-12s resp=%-5s ab=%d notes=%d zones=%d' %
              (w, m.get('lv'), m.get('job'), m.get('resp'),
               len(m.get('ab') or []), len(m.get('notes') or []), len(m.get('zones') or [])))
bad_det = sum(1 for m in M.values()
              if ('Sight' in (m.get('det') or []) and 'True Sight' in (m.get('det') or []))
              or ('Sound' in (m.get('det') or []) and 'True Sound' in (m.get('det') or [])))
print('  %d records still carry a Sight+True Sight style det stamp — you ruled '
      '"toro is fine", so untouched.' % bad_det)
z = json.load(open(os.path.join(os.path.dirname(P), 'zones.json')))
known = {x['name'] for x in z['zones']}
unk = collections.Counter()
for m in M.values():
    for zz in (m.get('zones') or []):
        if zz[0] not in known:
            unk[zz[0]] += 1
print('  %d zone names are free text (not in zones.json). Almost all are the established '
      'Sheol / Temenos / Apollyon / Einherjar-chamber / [U] forms; the one that looks like '
      'a name rather than a convention is %r x%d.'
      % (len(unk), 'Ferry - Mhaura/Selbina', unk.get('Ferry - Mhaura/Selbina', 0)))

# ============================================================ guards
assert not [k for m in M.values() for k, v in m.items() if v is None], 'NULL POISON'
assert not [k for a in A.values() for k, v in a.items() if v is None], 'NULL POISON (ab)'
assert not [k for k, m in M.items() if k != m['n'].lower()]
assert len(M) == before
sets = {s['label']: s for s in d['family_resist_sets']['Elemental']}
for key, label in [('shadowfang void', 'Dark'), ('touched gefyrst', 'Gefyrst')]:
    assert M[key]['wk'] == sets[label]['wk'] and M[key]['st'] == sets[label]['st'], key

json.dump(d, open(P, 'w'), separators=(', ', ': '), ensure_ascii=False)
print('\nmobs %d, abilities %d, orphans %d' %
      (len(M), len(A), sum(1 for m in M.values() if not m.get('fam'))))
