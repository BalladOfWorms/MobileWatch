#!/usr/bin/env python3
"""rev 388 — the Vampyr duplicate resolved and the three held pets released.

USER: the Vampyr Dog panel + "vampyr dog is real, wolf not so much, and these in the screenshot can
be removed, no info found"

TWO GUARD OVERRIDES, both deliberate and both explicitly authorised:
  (1) `vampyr wolf` HAS a family (Hound), which rule 389's guard normally refuses. It is a confirmed
      DUPLICATE, the same class as `hydra` at r366 — the user has the real record's page in hand.
  (2) `assassin's apprentice`, `commander's pet`, `volte's pet` all have `zones`, which the guard also
      refuses. I held them at r383 and again at r386, and put their zones, levels and Dynamis-D
      content tags into decision item 4 so the call would be an informed one. This is the third
      explicit instruction. Releasing them.
The zone/cross-reference reporting still runs on every target so anything lost is named.
"""
import json, collections, re

P = 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M, AB = d['mobs'], d['abilities']

# ------------------------------------------------------- 1. VAMPYR DOG, FROM ITS PAGE
v = M['vampyr dog']
assert v['fam'] == 'Hound'
before = json.dumps([v.get('wk'), v.get('st')], ensure_ascii=False)
v['det'] = ['True Sound', 'Blood']              # page Notes column: A, L, T(H), HP
v['im'] = ['Sleep', 'Lullaby', 'Repose']        # "Immune to all forms of Sleep, including..."
v['zones'] = [["Ortlinde's Chamber"], ["Gerhilde's Chamber"], ["Brunhilde's Chamber"]]
v['spawn'] = 'Twelve spawn in each of Ortlinde\u2019s, Gerhilde\u2019s and Brunhilde\u2019s Chamber.'
v['notes'] = [
    'A transformation of the Vampyr Jarl.',
    'They have to be killed in a random, sequential order.',
    'If all of them \u2014 or most of them \u2014 are slain, they converge back into the Vampyr Jarl '
    'with reduced HP.',
    'Immune to every form of Sleep, including Lullaby and Repose.',
    'They can also pop as normal waves, usually when the boss is the Vampyr.',
]
# The page's Weak to (Fire, Light, Slashing) and Strong to (Dark, Ice) all already match the stored
# grid; the grid additionally carries Wind/Lightning/Water weaknesses the page does not list.
# Omission is not contradiction (the Simorg precedent), so the grid is left alone.
after = json.dumps([v.get('wk'), v.get('st')], ensure_ascii=False)
assert before == after, 'grid must not change'
for e in v['wk']:
    assert e[0] not in ('Dark', 'Ice'), e
print('vampyr dog updated: det=%s im=%s zones=%d  grid UNCHANGED and consistent with the page'
      % (v['det'], v['im'], len(v['zones'])))

# ------------------------------------------------------------------- 2. DELETES
ASKED = ['vampyr wolf', "assassin's apprentice", "commander's pet", "volte's pet"]
print('\n=== DELETE REPORT (guards overridden, see header) ===')
for k in ASKED:
    r = M.get(k)
    assert r is not None, k
    print('  %-24s fam=%-8s lv=%-10s zones=%s content=%s nm=%s' % (
        k, r.get('fam'), r.get('lv'), r.get('zones'), r.get('content'), r.get('nm')))

print('\n=== CROSS-REFERENCES FROM SURVIVING RECORDS (word-boundary) ===')
disp = {k: M[k]['n'] for k in ASKED}
hits = 0
for mk, mv in M.items():
    if mk in ASKED:
        continue
    blob = json.dumps(mv, ensure_ascii=False)
    for k, name in disp.items():
        if re.search(r"(?<![\w'-])%s(?![\w'-])" % re.escape(name), blob):
            print('  %-26s mentions %s' % (mk, name)); hits += 1
if not hits:
    print('  (none)')

# what the two Dynamis-D pets take with them off the Content-tab rosters
for k in ("commander's pet", "volte's pet"):
    for tag in (M[k].get('content') or []):
        n = sum(1 for x in M.values() if tag in (x.get('content') or []))
        print('  content tag %-40s loses 1 of %d rows' % (tag, n))

for k in ASKED:
    del M[k]
print('  deleted %d' % len(ASKED))

# ------------------------------------------------------------------- 3. GUARDS
bad = [(k, f) for k, mm in M.items() for f, val in mm.items() if val is None]
assert not bad, bad[:10]
FREE = {"ortlindes chamber", "gerhildes chamber", "brunhildes chamber"}
zn = {x['name'] for x in json.load(open('app/src/main/assets/zones.json', encoding='utf-8'))['zones']}
def norm(s): return s.replace('\u2019', "'").replace("'", '').lower()
zi = {norm(z) for z in zn} | FREE
for z in M['vampyr dog']['zones']:
    assert norm(z[0]) in zi, z

GOOD = {'Physical', 'Magical', 'Breath', 'Slashing', 'Blunt', 'Impact', 'H2H', 'Piercing', 'Ranged',
        'Fire', 'Wind', 'Lightning', 'Light', 'Ice', 'Earth', 'Water', 'Dark', 'Varies'}
bogus = collections.Counter(e[0] for x in M.values()
                            for e in (x.get('wk') or []) + (x.get('st') or []) if e[0] not in GOOD)
print('\nnon-standard resist labels: %d entries' % sum(bogus.values()))
imv = collections.Counter(x for mv in M.values() for x in (mv.get('im') or []))
junk = [k for k in imv if k != k.strip() or '{' in k or (k.istitle() is False and k.islower())
        or re.search(r'[a-z][A-Z]', k)]
print('malformed `im` values: %s' % {k: imv[k] for k in junk})

json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('\nmobs %d | abilities %d | bucket %d' % (
    len(M), len(AB), sum(1 for x in M.values() if not x.get('fam'))))
