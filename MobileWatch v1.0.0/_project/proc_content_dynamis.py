#!/usr/bin/env python3
"""Dynamis content tags (rev 192) — DERIVED FROM THE ZONE DATA ALREADY IN THE FILE.
USER: "Dynamis and Dynamis D. Each get zone > bosses and regular mobs"

A mob standing in `Dynamis-Bastok` IS Dynamis content — the zone is not reachable
outside it — so the roster needs no screenshots: project each mob's existing Dynamis
zone entries into `content` as `Dynamis: <zone>`.

Bosses are NOT guessed. `nm` already sorts NMs above regular mobs inside a section;
the explicit `: Boss` role gets added later, per zone, on the user's word.
`Dynamis D` ([D] zones) is left alone — no record carries a [D] zone yet.
"""
import json, os
from zonepass import ASSETS

p = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(p, encoding='utf-8')); mobs = d['mobs']

added, per_zone = 0, {}
for k, v in mobs.items():
    znames = [(e[0] if isinstance(e, list) else e) for e in (v.get('zones') or [])]
    for z in znames:
        if not z.startswith('Dynamis-') or z.endswith('[D]'):
            continue
        tag = f"Dynamis: {z}"
        tags = v.get('content') or []
        if tag not in tags:
            v['content'] = tags + [tag]
            added += 1
            per_zone[z] = per_zone.get(z, 0) + 1

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print(f"tags added: {added}")
for z, n in sorted(per_zone.items()):
    print(f"  {z:26s} {n}")
tagged = sum(1 for v in mobs.values() if v.get('content'))
print(f"records now carrying any content tag: {tagged}")
