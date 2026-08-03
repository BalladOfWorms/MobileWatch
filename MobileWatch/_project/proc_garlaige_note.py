#!/usr/bin/env python3
"""
rev 270 — ZONEINFO NOTE, user-authorised: "pouch of weighted stones, if there isnt a
note in the zone section, please add". `garlaige_citadel` has no `notes` key at all,
so one is created from the info box's gate mechanic. Same shape as the rev-266
Eldieme astrolabe note: an ACCESS requirement the zone cannot be navigated without.
"""
import json, os, sys
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'src', 'main', 'assets')
p = os.path.join(A, 'zoneinfo.json')
zi = json.load(open(p, encoding='utf-8'))
e = zi['garlaige_citadel']
assert 'notes' not in e, "notes already present — the user's condition was 'if there isnt a note'"
e['notes'] = [
    "Three Banishing Gates must be opened to reach parts of the zone: either four players stand on the pressure switches together, or one player carries a Pouch of Weighted Stones.",
    "A Pouch of Weighted Stones is obtained by selecting the ??? at (G-8) on Map 1; a gate is then opened by targeting it and selecting it.",
]
for n in e['notes']:
    print('  +', n)
if '--write' in sys.argv:
    json.dump(zi, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    print("WRITTEN.")
else:
    print("(dry run)")
