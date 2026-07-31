#!/usr/bin/env python3
"""
rev 279 — CASING, MEASURED FIRST. `cactrot rapido` stores `Arco De Velocidad` and
`Arete Del Sol`; the item DB writes the Spanish articles lowercase — `Arco de
Velocidad`, `Arete del Sol`. Swept file-wide: only **3 tokens across 2 records**
differ from the DB by case alone (the third is `Danzo Sune-ate` -> `Danzo Sune-Ate`).

Case-only, verified by exact match against the DB after the change. The rev-248
"+8 casing fixes" pass is the precedent.
"""
import json, os, sys
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'src', 'main', 'assets')
d = json.load(open(os.path.join(A, 'mobs.json'), encoding='utf-8'))
items = json.load(open(os.path.join(A, 'ffxi_items.json'), encoding='utf-8'))
byl = {}
for v in items.values():
    if isinstance(v, dict) and 'n' in v:
        byl.setdefault(v['n'].lower(), v['n'])

n = 0
for k, v in d['mobs'].items():
    s = v.get('drops')
    if not isinstance(s, str):
        continue
    parts = [p.strip() for p in s.split(',')]
    fixed = [byl.get(p.lower(), p) for p in parts]
    if fixed != parts:
        v['drops'] = ', '.join(fixed)
        for a, b in zip(parts, fixed):
            if a != b:
                print(f"  {k:20s} {a!r} -> {b!r}")
        n += 1
print(f"\n{n} records touched")

if '--write' in sys.argv:
    json.dump(d, open(os.path.join(A, 'mobs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print("WRITTEN.")
else:
    print("(dry run)")
