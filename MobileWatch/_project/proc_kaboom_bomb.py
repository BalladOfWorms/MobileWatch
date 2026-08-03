#!/usr/bin/env python3
"""
rev 272 — USER: "yes if it says the family in the screenshots, resolve it if we have
nothing". A standing rule now: when a zone page's Genus column names a family and our
record has NO `fam`, take the page's.

Swept all EIGHT zone rosters processed this session (Eldieme, Jugner, Monastic Cavern,
Altar Room, Attohwa Chasm, Castle Oztroja, Garlaige Citadel, Meriphataud Mountains) —
277 distinct records — and exactly ONE still has fam=None: `kaboom`, Garlaige Citadel,
Genus **Bomb**. (The other two, hellbound warlock/warrior, were closed at rev 265.)

STAMPED (blanks only), by the rule-101 measurement over the 59 Bomb records:
  fam   'Bomb'      the page's Genus column
  crys  'Fire'      55 of 59 agree (the 4 exceptions are empty shells)
  ab    Berserk / Self-Destruct / Heat Wave / Vulcanian Impact / Hellstorm   55 of 59
  job   'Warrior'   from the PAGE (the row prints WAR), not the family

NOT STAMPED — `im` (52 of 59 carry nothing at all) and `lnk` (51 of 59 unset). No
consensus, no guess. The record already has agg/det/resp/wk/st.
"""
import json, os, sys
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'src', 'main', 'assets', 'mobs.json')
d = json.load(open(A, encoding='utf-8'))
rec = d['mobs']['kaboom']

STAMP = {'fam': 'Bomb', 'crys': 'Fire',
         'ab': ['Berserk', 'Self-Destruct', 'Heat Wave', 'Vulcanian Impact', 'Hellstorm'],
         'job': 'Warrior'}
for f, v in STAMP.items():
    if rec.get(f):
        print(f"  kaboom {f:5s} KEPT {rec[f]!r}")
    else:
        rec[f] = v
        print(f"  kaboom {f:5s} <- {v!r}")

assert not [k for m in d['mobs'].values() for k, v in m.items() if v is None], "null poison"

if '--write' in sys.argv:
    json.dump(d, open(A, 'w', encoding='utf-8'), ensure_ascii=False)
    print("WRITTEN.")
else:
    print("(dry run)")
