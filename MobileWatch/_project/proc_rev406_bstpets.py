#!/usr/bin/env python3
"""
REV 406 — THE BEASTMASTER FAMILIAR PASS IS COMPLETE. 97 of 97.
Runs after 398-405. jobs.json only.

THREE THINGS, ALL FROM THE USER.

1. `Brave Hero Glenn` — the last unfilled familiar, and it is the SECOND KNOWN
   `ready: []`. Its page prints the words **"No Ready Moves"** in the Ready block,
   which is the empty-list discipline's whole reason for existing: an explicit []
   means the page says it HAS none, an absent key means we never recorded it.
   Kotlin tells them apart with `po.has("ready")`. Slippery Silas was the first.

2. **`Scissor Guard` IS 2 CHARGES** (user, closing rule 485). Six pages said 2 and
   rev 402 recorded 1 for `Herald Henry`. It was a transcription slip, exactly as
   the 6-vs-1 split suggested. THE LESSON: when one reading stands alone against
   several, it is the lone reading that is wrong — but confirm rather than let a
   majority vote rewrite data on its own.

3. **`Hippogryph Familiar` DOES NOT EXIST** (user: "there is no hippogryph
   familiar, just named hippogryphs"). The record is DELETED, not blanked.
   This also retires the disputed `Turpid Broth` jug string, which is what the
   user's earlier "you had turbid broth as hippo familiar" note was about — the
   whole row was phantom. Daring Roland and Faithful Falcorr remain as the two
   real Hippogryph familiars, both named, both filled.
   => the roster is 97, not 98.
"""
import json, os

BASE = 'app/src/main/assets'
if not os.path.exists(BASE):
    BASE = 'android/' + BASE
P = os.path.join(BASE, 'jobs.json')
d = json.load(open(P, encoding='utf-8'))
pets = d['pets']['9']
by_name = {p['n']: p for p in pets}

# ------------------------------------------------- 1. the last familiar
GLENN = dict(fam='Frog', eco='Aquan', job='Warrior', tp='65', cap='119',
             atk='-30%', deff='-30%',
             stats={'hp': '4,212', 'acc': '863', 'atk': '556', 'eva': '712', 'def': '661'},
             ready=[])
GLENN['def'] = GLENN.pop('deff')
p = by_name['Brave Hero Glenn']
stored = p.get('cap')
for k, v in GLENN.items():
    p[k] = v
print('=== THE LAST FAMILIAR ===')
print('  Brave Hero Glenn   Frog/Aquan, Warrior, cap %s (%s), TP/hit 65, atk -30%%, def -30%%'
      % (GLENN['cap'], 'matches the jug string' if stored == GLENN['cap'] else 'CHANGED from %s' % stored))
print('  page prints "No Ready Moves" -> ready = []  (explicit empty, the 2nd known after Slippery Silas)')
print('  ready recorded as EMPTY not ABSENT: %r, po.has("ready") will read true' % (p['ready'],))

# ------------------------------------------------- 2. Scissor Guard (rule 485 closed)
print('\n=== `Scissor Guard` = 2 CHARGES (user ruling, rule 485 CLOSED) ===')
fixed = 0
for q in pets:
    for r in (q.get('ready') or []):
        if r['n'] == 'Scissor Guard' and r['c'] != '2 charges':
            print('  %-20s %s -> 2 charges' % (q['n'], r['c']))
            r['c'] = '2 charges'
            fixed += 1
print('  %d corrected' % fixed)
costs = {r['c'] for q in pets for r in (q.get('ready') or []) if r['n'] == 'Scissor Guard'}
assert costs == {'2 charges'}, costs
print('  every Scissor Guard now reads: %s' % ', '.join(costs))

# ------------------------------------------------- 3. delete the phantom
print('\n=== `Hippogryph Familiar` DELETED (user: "there is no hippogryph familiar") ===')
ghost = by_name['Hippogryph Familiar']
print('  removing: %r  (jug %r — the disputed Turpid/Turbid Broth row goes with it)'
      % (ghost['n'], ghost.get('sub')))
d['pets']['9'] = [q for q in pets if q['n'] != 'Hippogryph Familiar']
pets = d['pets']['9']
assert 'Hippogryph Familiar' not in {q['n'] for q in pets}
hippo = [q['n'] for q in pets if q.get('fam') == 'Hippogryph']
print('  real Hippogryph familiars left (%d): %s' % (len(hippo), ', '.join(hippo)))
subs = [q.get('sub') for q in pets if q.get('sub')]
assert len(subs) == len(set(subs)), 'a jug string is now shared by two familiars'
print('  jug strings still unique across the roster: %d/%d' % (len(set(subs)), len(pets)))

# ------------------------------------------------- guards
ABIL = json.load(open(os.path.join(BASE, 'mobs.json'), encoding='utf-8'))['abilities']
unmatched = sorted({it['n'] for q in pets for sec in (q.get('sections') or []) for it in sec['items']
                    if it['n'] not in ABIL} |
                   {r['n'] for q in pets for r in (q.get('ready') or []) if r['n'] not in ABIL})
print('\npet ability names with no bestiary definition: %d %s' % (len(unmatched), unmatched))
assert not unmatched
assert not [k for q in pets for k, v in q.items() if v is None], 'NULL POISON'
import re
assert all(re.fullmatch(r'\d+', q['tp']) for q in pets if q.get('tp'))
for q in pets:
    st = q.get('stats')
    if st:
        assert set(st) <= {'hp', 'acc', 'atk', 'eva', 'def'} and all(isinstance(v, str) for v in st.values())
BST_ONLY = {'fam', 'job', 'lvl', 'cap', 'hp', 'dmg', 'tp', 'dur', 'traits', 'notes', 'ready',
            'eco', 'atk', 'def', 'stats'}
assert not [q['n'] for q in d['pets']['15'] if BST_ONLY & set(q)], 'a Summoner avatar was modified'

# ------------------------------------------------- the finish line
todo = [q['n'] for q in pets if 'ready' not in q]
empty = [q['n'] for q in pets if q.get('ready') == []]
print('\n=== BEASTMASTER FAMILIAR PASS ===')
print('  familiars with a Ready list recorded: %d of %d' % (len(pets) - len(todo), len(pets)))
print('  still to do: %s' % (', '.join(todo) if todo else 'NOTHING — THE PASS IS COMPLETE'))
assert not todo
print('  explicitly "no Ready moves" (ready == []): %s' % ', '.join(empty))
print('  ready moves total: %d, carrying a skillchain: %d'
      % (sum(len(q['ready']) for q in pets),
         sum(1 for q in pets for r in q['ready'] if r.get('sc'))))
print('  familiars with a stat block: %d   with a fam: %d   with a job: %d'
      % (sum(1 for q in pets if q.get('stats')),
         sum(1 for q in pets if q.get('fam')), sum(1 for q in pets if q.get('job'))))
print('  no `fam` recorded: %s' % ', '.join(q['n'] for q in pets if not q.get('fam')))

json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('\nwritten: %s' % P)
