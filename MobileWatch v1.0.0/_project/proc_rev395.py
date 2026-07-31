#!/usr/bin/env python3
"""
REV 395 — decision items 2 and 3 answered. Bestiary closed.

ADD the two Briars variants on the `mistdagger` template — same battlefield,
same spawn line, same Humanoid family, same A / L / T(S).

DELETE `will-o'the-wisp`, the hyphen-less duplicate.

TWO THINGS CARRIED OVER FROM THE DELETED SINGLE `the briars` RECORD, both worth
knowing because they are the only reason these two are not bare stubs:
  - lv 108. The deleted record carried it, and `mistdagger` — the other
    Behind the Sluices boss the file kept — is also 108.
  - the six-spell list (Diaga II, Protect V, Shell V, Haste, Slow II,
    Paralyze II). It was measured on the single record, so THERE IS NO WAY TO
    TELL which variant it came from, or whether both share it. Written to both
    and flagged rather than thrown away.
Neither page states a job, a level or a resist grid, so those stay unset.
"""
import json, os

P = 'app/src/main/assets/mobs.json'
if not os.path.exists(P):
    P = 'android/' + P
d = json.load(open(P))
M = d['mobs']; A = d['abilities']
before = len(M)

BRIARS_SP = ['Diaga II', 'Protect V', 'Shell V', 'Haste', 'Slow II', 'Paralyze II']

def briars(race):
    return {
        'n': 'The Briars (%s)' % race,
        'fam': 'Humanoid',
        'lv': [108, 108],
        'agg': True,
        'lnk': True,
        'nm': True,
        'det': ['True Sight'],
        'sp': list(BRIARS_SP),
        'zones': [['Rala Waterways [U]', '108']],
        'spawn': 'One spawn in the Behind the Sluices battlefield.',
        'notes': [
            'A mission boss, fought in Behind the Sluices in Rala Waterways [U].',
            'In battle he is simply named The Briars.',
            'One of two race variants; The Keeper is stronger than both of them '
            'and than Mistdagger.',
        ],
    }

print('=== ADDING THE TWO BRIARS VARIANTS ===')
for race in ('Galka', 'Elvaan'):
    rec = briars(race)
    key = rec['n'].lower()
    assert key not in M, key
    M[key] = rec
    print('  %-22s fam=%-9s lv=%s  nm=%s' % (key, rec['fam'], rec['lv'], rec['nm']))
print('  Level and spell list carried from the single `the briars` record deleted at')
print('  rev 390 — the spells cannot be attributed to one variant, so both carry them.')

print('\n=== DELETING THE MISSPELLED DUPLICATE ===')
DUP = "will-o'the-wisp"
KEEP = "will-o'-the-wisp"
dup, keep = M[DUP], M[KEEP]
# everything the duplicate holds must already exist on the survivor, or be
# reported as a loss. Nothing is lost here except the bare job string.
for f in ('fam', 'crys', 'det', 'wk', 'st', 'ab'):
    same = dup.get(f) == keep.get(f)
    print('  %-6s identical: %-5s  %s' % (f, same, dup.get(f) if not same else ''))
print('  ONLY DIFFERENCE: job %r (dup) vs %r (survivor). The survivor also has lv %s,'
      % (dup.get('job'), keep.get('job'), keep.get('lv')))
print('  resp %s and %d zones that the duplicate does not.' % (keep.get('resp'), len(keep['zones'])))
REF = ('notes', 'spawn', 'drops')
blob = json.dumps([{f: v.get(f) for f in REF} for k, v in M.items() if k != DUP],
                  ensure_ascii=False)
assert blob.count(dup['n']) == 0, 'cross-referenced'
del M[DUP]
print('  deleted. no surviving record references it.')

# ---------------------------------------------------------------- guards
assert not [k for m in M.values() for k, v in m.items() if v is None], 'NULL POISON'
assert not [k for a in A.values() for k, v in a.items() if v is None], 'NULL POISON (ab)'
assert not [k for k, m in M.items() if k != m['n'].lower()]
assert not [k for k, m in M.items() if m.get('lv') and (m['lv'][0] < 1 or m['lv'][0] > m['lv'][1])]
assert not [1 for m in M.values() for z in (m.get('zones') or []) if not isinstance(z, list)]
OKC = {'Fire', 'Ice', 'Wind', 'Earth', 'Lightning', 'Water', 'Light', 'Dark', 'Varies', 'None'}
assert not [m['crys'] for m in M.values() if m.get('crys') and m['crys'] not in OKC]
assert not [k for k, m in M.items() if m.get('eco') and m.get('fam')
            and m['eco'] != d['family_eco'].get(m['fam'])]
assert not [1 for m in M.values() if not m.get('fam')], 'ORPHANS'
sets = {s['label']: s for s in d['family_resist_sets']['Elemental']}
for key, label in [('shadowfang void', 'Dark'), ('touched gefyrst', 'Gefyrst')]:
    assert M[key]['wk'] == sets[label]['wk'] and M[key]['st'] == sets[label]['st'], key

json.dump(d, open(P, 'w'), separators=(', ', ': '), ensure_ascii=False)
print('\nmobs %d -> %d, abilities %d, orphans 0' % (before, len(M), len(A)))
print('Behind the Sluices roster now: %s'
      % sorted(k for k, m in M.items()
               if 'Behind the Sluices' in str(m.get('spawn', ''))))
