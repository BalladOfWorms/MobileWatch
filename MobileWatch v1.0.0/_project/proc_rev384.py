#!/usr/bin/env python3
"""rev 384 — the 14 ability-name diffs between mobs.json and ability_info.xml, closed.

USER uploaded ability_info.xml: "before we continue mobs, update the abilities we found in here".

The 14 names below were RECOVERED FROM THE DATA, not guessed: every mobs.json ability key absent
from the XML was tested for normalized equality (strip non-alphanumerics, lowercase) against the
1,740 res-verified XML names. Exactly 14 matched, and the XML spelling wins by the established
policy (Windower's res files are authority for the name the game reports).

Rule 398 discipline — a rename is FOUR edits: the `abilities` key (rebuilt in insertion order),
every mob `ab` reference, prose inside other defs' d/notes, and family_notes bullets.
"""
import json, collections, re

P = 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
AB, M, FN = d['abilities'], d['mobs'], d['family_notes']

# ---- 12 pure renames: the target name does NOT already exist as a key
RENAME = {
    'Dead Eye': 'Deadeye',
    'Cryo Jet': 'Cryojet',
    'Start From Scratch': 'Start from Scratch',
    'Armblock': 'Arm Block',
    'Into The Light': 'Into the Light',
    'Plague Breath': 'Plaguebreath',
    '1000 Needles': '1,000 Needles',
    '2000 Needles': '2,000 Needles',
    '4000 Needles': '4,000 Needles',
    '10000 Needles': '10,000 Needles',
    'Petrogaze': 'Petro Gaze',
    'Blindside Barrage': 'Blind Side Barrage',
}
# ---- 2 MERGES: the target already exists, so this is not a rename.
#   'Frigid shuffle'  0 refs, thin def          -> drop, keep 'Frigid Shuffle' (16 refs, rich def)
#   'Draw-In'        27 refs, RICHER def        -> keep that def UNDER the res name 'Draw In'
MERGE = {'Frigid shuffle': 'Frigid Shuffle', 'Draw-In': 'Draw In'}
KEEP_DEF_FROM_OLD = {'Draw-In'}      # the loser's def is the better one

for o, n in RENAME.items():
    assert o in AB, o
    assert n not in AB, 'collision, would clobber a real def: ' + n
for o, n in MERGE.items():
    assert o in AB and n in AB, (o, n)

refs = collections.Counter(a for v in M.values() for a in (v.get('ab') or []))
print('=== plan ===')
for o, n in list(RENAME.items()) + list(MERGE.items()):
    print('  %-20s -> %-20s refs %d%s' % (
        o, n, refs.get(o, 0), '   [MERGE]' if o in MERGE else ''))

ALL = dict(RENAME); ALL.update(MERGE)

# (1) the abilities dict, rebuilt in insertion order so the diff stays readable
new_ab = {}
for k, v in AB.items():
    if k in MERGE:
        tgt = MERGE[k]
        if k in KEEP_DEF_FROM_OLD:
            new_ab[tgt] = v                       # richer def wins, under the res name
        continue                                   # otherwise just drop the duplicate key
    new_ab[ALL.get(k, k)] = v
for o, n in MERGE.items():
    assert n in new_ab, n
d['abilities'] = AB = new_ab

# (2) every mob `ab` reference
nref = 0
for v in M.values():
    kit = v.get('ab')
    if not kit:
        continue
    out, seen = [], set()
    for a in kit:
        b = ALL.get(a, a)
        if b != a:
            nref += 1
        if b not in seen:                          # a merge can create a duplicate in one kit
            seen.add(b); out.append(b)
    v['ab'] = out
print('\n  mob ab references repointed: %d' % nref)

# (3)+(4) prose mentions inside ability d/notes and in family_notes bullets
def fix_prose(s):
    for o, n in ALL.items():
        s = re.sub(r'\b%s\b' % re.escape(o), n, s)
    return s

nprose = 0
for a in AB.values():
    for f in ('d', 'notes'):
        if isinstance(a.get(f), str):
            s = fix_prose(a[f])
            if s != a[f]:
                a[f] = s; nprose += 1
for fam, bullets in FN.items():
    for i, b in enumerate(bullets):
        s = fix_prose(b)
        if s != b:
            bullets[i] = s; nprose += 1
for v in M.values():
    for i, b in enumerate(v.get('notes') or []):
        s = fix_prose(b)
        if s != b:
            v['notes'][i] = s; nprose += 1
print('  prose mentions fixed: %d' % nprose)

# ---- guards
bad = [(k, f) for k, m in M.items() for f, val in m.items() if val is None]
assert not bad, bad[:10]
bad = [(k, f) for k, a in AB.items() for f, val in a.items() if val is None]
assert not bad, bad[:10]
for o in ALL:
    assert o not in AB, 'old key survived: ' + o
    assert not [1 for v in M.values() for a in (v.get('ab') or []) if a == o], 'ref survived: ' + o

json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
undef = collections.Counter(a for v in M.values() for a in (v.get('ab') or []) if a not in AB)
print('\nabilities %d | undefined refs %d across %d names' % (
    len(AB), sum(undef.values()), len(undef)))
