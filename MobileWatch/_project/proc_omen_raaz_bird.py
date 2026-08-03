#!/usr/bin/env python3
"""Omen — the last two families (rev 196).
USER: "faaz is raaz, and the birds are lesser birds"
Same shape as rev 195: Sweetwater 119 (regular) + Transcendent 125-128 (nm), Sight, no link.
"""
import json, os
from zonepass import ASSETS

FAMS = ["Raaz", "Lesser Bird"]
ZONE, TAG = "Reisenjima Henge", "Omen: Sweetwater Mobs"
p = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(p, encoding='utf-8')); mobs = d['mobs']
known, icons = set(d['families']), d.get('family_icons', {})
import collections
members = collections.Counter(v['fam'] for v in mobs.values() if v.get('fam'))
made = []
for fam in FAMS:
    assert fam in known, fam
    print(f"  {fam}: {members[fam]} existing members, eco={d['family_eco'].get(fam)!r}, icon={fam in icons}")
    for prefix, lv, band, nm in (("Sweetwater", [119, 119], "119", False),
                                 ("Transcendent", [125, 128], "125-128", True)):
        name, key = f"{prefix} {fam}", f"{prefix} {fam}".lower()
        if key in mobs: continue
        rec = {"n": name, "fam": fam, "lv": lv, "agg": True, "lnk": False,
               "det": ["Sight"], "zones": [[ZONE, band]], "content": [TAG]}
        if nm: rec["nm"] = True
        mobs[key] = rec; made.append(key)
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print("created:", ", ".join(made), f"| mobs -> {len(mobs)}")
