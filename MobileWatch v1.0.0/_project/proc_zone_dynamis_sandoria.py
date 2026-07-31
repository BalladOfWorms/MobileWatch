#!/usr/bin/env python3
"""Dynamis-San d'Oria zone pass + zone boss (rev 196).
USER: "dynamis san doria, arch overlord is zone boss"

The page's Lv column is blank on every NM row and "-" on every adversary row, so nothing
here carries a level: the zone is added level-less. 33 page rows -> 33 records, 0 missing;
11 of them had NO zones at all. Content tags follow the zone (rev 192's projection), and
`arch overlord tombstone` takes the `: Boss` role so it heads the section.
"""
import json, os
from zonepass import ASSETS

ZONE = "Dynamis-San d'Oria"
TAG, BOSS_TAG = f"Dynamis: {ZONE}", f"Dynamis: {ZONE}: Boss"
BOSS = "arch overlord tombstone"

PAGE = ["reapertongue gadgquok", "soulsender fugbrag", "voidstreaker butchnotch", "wyrmgnasher bjakdek",
        "battlechoir gitchfotch", "overlord's tombstone", "bladeburner rokgevok", "steelshank kratzvatz",
        "bloodfist voshgrosh", "spellspear djokvukk", "arch overlord tombstone",
        "djokvukk's wyvern", "kratzvatz's hecteyes", "serjeant tombstone", "vanguard amputator",
        "vanguard backstabber", "vanguard bugler", "vanguard dollmaster", "vanguard footsoldier",
        "vanguard grappler", "vanguard gutslasher", "vanguard hawker", "vanguard impaler",
        "vanguard mesmerizer", "vanguard neckchopper", "vanguard pillager", "vanguard predator",
        "vanguard trooper", "vanguard vexer", "vanguard's avatar", "vanguard's hecteyes",
        "vanguard's wyvern", "warchief tombstone"]

p = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(p, encoding='utf-8')); mobs = d['mobs']
zoned, tagged, promoted = [], [], []
for k in PAGE:
    m = mobs[k]
    zs = m.setdefault('zones', [])
    if not any((e[0] if isinstance(e, list) else e) == ZONE for e in zs):
        zs.append([ZONE]); zoned.append(k)
    want = BOSS_TAG if k == BOSS else TAG
    tags = [t for t in (m.get('content') or []) if t != TAG or k != BOSS]
    if k == BOSS and TAG in tags:
        tags.remove(TAG); promoted.append(k)
    if want not in tags:
        tags.append(want)
        if k != BOSS: tagged.append(k)
    m['content'] = tags

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print(f"zone added (level-less) to {len(zoned)}: {', '.join(zoned)}")
print(f"content tag added to {len(tagged)}")
print(f"boss: {BOSS} -> {BOSS_TAG}  (promoted from plain tag: {bool(promoted)})")
print("arch overlord tombstone now:", mobs[BOSS].get('content'), mobs[BOSS].get('zones'))
