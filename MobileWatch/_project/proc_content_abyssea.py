#!/usr/bin/env python3
"""Abyssea content tags (rev 193) — DERIVED FROM THE ZONE DATA, like Dynamis.
USER: "Abyssea next, zones then zone boss, nms and mobs"

Every `Abyssea-*` zone is content-exclusive, so the roster is projected from each
record's existing zone entries as `Abyssea: <zone>`. Bosses are NOT guessed: `nm`
already lifts NMs above regular mobs inside a section, and the zone boss gets an
explicit `: Boss` role on the user's word.
"""
import json, os
from zonepass import ASSETS

p = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(p, encoding='utf-8')); mobs = d['mobs']

added, per_zone = 0, {}
for k, v in mobs.items():
    for e in (v.get('zones') or []):
        z = e[0] if isinstance(e, list) else e
        if not z.startswith('Abyssea-'):
            continue
        tag = f"Abyssea: {z}"
        tags = v.get('content') or []
        if tag not in tags:
            v['content'] = tags + [tag]
            added += 1
            per_zone[z] = per_zone.get(z, 0) + 1

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print(f"tags added: {added}")
for z, n in sorted(per_zone.items()):
    print(f"  {z:26s} {n}")
print("records carrying any content tag:", sum(1 for v in mobs.values() if v.get('content')))
