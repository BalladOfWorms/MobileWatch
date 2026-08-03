#!/usr/bin/env python3
"""
rev 264 — RULE-98 DROPPED-SUFFIX FIX.

The bucket-E check (records carrying `The Eldieme Necropolis` that the zone page's
two tables never name) returned exactly four rows:

    goblin blastmaster / corpsman / freesword / pioneer   62-64

Three independent proofs they belong to the [S] twin, not the present-day zone:
  1. zoneinfo `the_eldieme_necropolis_s.mobs[]` lists all four AT 62-64
  2. the present-day Adversaries table (user's shots) runs 40-43 -> 91-95 with no
     Goblin row anywhere in it
  3. EVERY OTHER ZONE on all four records is an [S] zone — Batallia Downs [S],
     Fort Karugo-Narugo [S], Grauberg [S]

So the entry lost its ` [S]` suffix in an early intake, and rule 98's prefix
collision is what hid it: the string still matched a real zone, so it filed
silently into the wrong bucket of the Zone view.

Retarget only — the level string is unchanged and no zone is removed.
"""
import json, os, sys

A = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '..', 'app', 'src', 'main', 'assets', 'mobs.json')
d = json.load(open(A, encoding='utf-8'))
mobs = d['mobs']

OLD = "The Eldieme Necropolis"
NEW = "The Eldieme Necropolis [S]"
KEYS = ['goblin blastmaster', 'goblin corpsman', 'goblin freesword', 'goblin pioneer']

for k in KEYS:
    zs = mobs[k]['zones']
    assert not any((e[0] if isinstance(e, list) else e) == NEW for e in zs), f"{k} already has {NEW}"
    for e in zs:
        if (e[0] if isinstance(e, list) else e) == OLD:
            if isinstance(e, list):
                e[0] = NEW
            else:
                zs[zs.index(e)] = NEW
            print(f"  {k:20s} -> {zs}")

assert not [k for m in mobs.values() for k, v in m.items() if v is None], "null poison"

if '--write' in sys.argv:
    json.dump(d, open(A, 'w', encoding='utf-8'), ensure_ascii=False)
    print("WRITTEN.")
else:
    print("(dry run — pass --write)")
