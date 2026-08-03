#!/usr/bin/env python3
"""
rev 264 follow-up — two Eldieme records sit in the page's Notorious Monsters
table but carry NO `nm` flag, so they render as ordinary mobs.

  lich c magnus   nmlv "58", nm absent  -> the audit §6 "nmlv but no nm" class
  gasha           Voidwatch NM, nm absent

Page-backed correction only (the NM table is a membership statement); nothing
else on either record is touched.
"""
import json, os, sys

A = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '..', 'app', 'src', 'main', 'assets', 'mobs.json')
d = json.load(open(A, encoding='utf-8'))
mobs = d['mobs']

for k in ('lich c magnus', 'gasha'):
    before = mobs[k].get('nm')
    mobs[k]['nm'] = True
    print(f"  {k:16s} nm {before!r} -> True")

assert not [k for m in mobs.values() for k, v in m.items() if v is None], "null poison"

if '--write' in sys.argv:
    json.dump(d, open(A, 'w', encoding='utf-8'), ensure_ascii=False)
    print("WRITTEN.")
else:
    print("(dry run — pass --write)")
