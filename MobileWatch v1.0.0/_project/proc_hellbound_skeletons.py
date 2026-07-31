#!/usr/bin/env python3
"""
rev 265 — USER: "helbound mobs are skeletons".

`hellbound warlock` and `hellbound warrior` were two of the 561 fam=None orphans.
The Eldieme page's Genus column says Skeleton for both and the user confirms it.

STAMPED (blanks only — nothing existing is overwritten):
  fam   'Skeleton'
  crys  'Earth'                                   113 of 118 Skeleton records agree
                                                  (the 5 exceptions are empty shells)
  ab    Black Cloud / Blood Saber / Hell Slash /  113 of 118 agree
        Horror Cloud
  job   from the PAGE, not the family — the shots print BLM under Hellbound Warlock
        and WAR under Hellbound Warrior

NOT STAMPED — `im`. The Skeleton family does NOT agree on it: Drain/Aspir/Dark Sleep
69, Dark Sleep 30, +Sleep 7, Dark+Dark Sleep 6. No consensus, so no guess.
Both records already carry det/wk/st/resp and the Warlock its own `sp` list.
"""
import json, os, sys

A = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '..', 'app', 'src', 'main', 'assets', 'mobs.json')
d = json.load(open(A, encoding='utf-8'))
mobs = d['mobs']

AB = ['Black Cloud', 'Blood Saber', 'Hell Slash', 'Horror Cloud']
STAMP = {
    'hellbound warlock': {'fam': 'Skeleton', 'crys': 'Earth', 'ab': AB, 'job': 'Black Mage'},
    'hellbound warrior': {'fam': 'Skeleton', 'crys': 'Earth', 'ab': AB, 'job': 'Warrior'},
}

for k, fields in STAMP.items():
    rec = mobs[k]
    for f, v in fields.items():
        if rec.get(f):
            print(f"  {k:18s} {f:5s} KEPT {rec[f]!r}")
        else:
            rec[f] = v
            print(f"  {k:18s} {f:5s} <- {v!r}")

assert not [k for m in mobs.values() for k, v in m.items() if v is None], "null poison"

if '--write' in sys.argv:
    json.dump(d, open(A, 'w', encoding='utf-8'), ensure_ascii=False)
    print("WRITTEN.")
else:
    print("(dry run — pass --write)")
