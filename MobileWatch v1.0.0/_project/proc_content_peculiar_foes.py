#!/usr/bin/env python3
"""FIRST CONTENT TAGS (rev 186) — "Peculiar Foes".
USER: "lets add our first 'content' view mobs. 'peculiar foes' mobs get a entry in the content view"

Source = the Records of Eminence "Peculiar Foes I-XV (M)" objective table: each names an
Awoken fiend at the Peculiar Footprints in one zone. XV names three.
Writes `content: ["Peculiar Foes"]` (the new List<String> field, MobDb.kt) and, where the
record had no zone at all, the zone the objective names — zones/levels remain the remit.
"""
import json, os
from zonepass import ASSETS

FOES = {  # key -> zone named by the RoE objective
    "awoken hildesvini":    "Wajaom Woodlands",
    "awoken mokkuralfi":    "Mount Zhayolm",
    "awoken vampyr jarl":   "Caedarva Mire",
    "awoken gorgimera":     "Beaucedine Glacier",
    "awoken ariri samariri":"Palborough Mines",
    "awoken hrungnir":      "Aydeewa Subterrane",
    "awoken morbol emperor":"Arrapago Reef",
    "awoken stoorworm":     "Reisenjima",
    "awoken dendainsonne":  "Western Altepa Desert",
    "awoken freke":         "Batallia Downs",
    "awoken tanngrisnir":   "Qufim Island",
    "awoken nihhus":        "Kamihr Drifts",
    "awoken hakenmann":     "Rala Waterways",
    "awoken andhrimnir":    "Newton Movalpolos",
    "awoken angantyr":      "Xarcabard",
    "awoken hjorvarth":     "Xarcabard",
    "awoken hrani":         "Xarcabard",
}
TAG = "Peculiar Foes"

p = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(p, encoding='utf-8')); mobs = d['mobs']
zj = {z['name'] for z in json.load(open(os.path.join(ASSETS,'zones.json'), encoding='utf-8'))['zones']}

tagged, zoned, fixed, missing = [], [], [], []
for k, zone in FOES.items():
    m = mobs.get(k)
    if m is None:
        missing.append(k); continue
    tags = m.get('content') or []
    if TAG not in tags:
        m['content'] = tags + [TAG]; tagged.append(k)
    zs = m.setdefault('zones', [])
    names = [(e[0] if isinstance(e, list) else e) for e in zs]
    if zone not in names:
        if zone not in zj:
            print(f"  !! {zone!r} not a zones.json name — zone NOT added for {k}")
        else:
            zs.append([zone]); zoned.append(f"{k} -> {zone}")
    # empty-string level is documented noise (optString "" == absent)
    for i, e in enumerate(zs):
        if isinstance(e, list) and len(e) > 1 and e[1] == "":
            zs[i] = [e[0]]; fixed.append(f"{k}: {e[0]} ['',] -> level-less")

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print(f"content='{TAG}' set on {len(tagged)}: {', '.join(sorted(tagged))}")
print(f"zone added to {len(zoned)}: {', '.join(zoned) or '(none)'}")
print(f"empty-level cleanups: {', '.join(fixed) or '(none)'}")
print(f"missing records: {missing or '(none)'}")
