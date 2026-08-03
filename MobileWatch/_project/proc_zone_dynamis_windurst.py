#!/usr/bin/env python3
"""Dynamis-Windurst zone pass + boss + Time Extension flags (rev 197).
USER: "dynamis windhurst, zone boss is arch tzee. flag the time extension mobs in these zones as well,
maybe put them at the top of regular mob list with a "(T.E.)" after the name"

Lv is blank on every row, so the zone goes on level-less. 33 rows -> 33 records, 0 missing
(zoneinfo publishes the same 12 + 21). `arch tzee xicu idol` takes the `: Boss` role.
Time Extension mobs take the `: TE` role, which sorts them above the regular block and
renders "(T.E.)" after the name.
"""
import json, os
from zonepass import ASSETS

ZONE = "Dynamis-Windurst"
TAG, BOSS_TAG = f"Dynamis: {ZONE}", f"Dynamis: {ZONE}: Boss"
BOSS = "arch tzee xicu idol"
PAGE = ["loo hepe the eyepiercer", "wuu qoho the razorclaw", "xoo kaza the solemn",
        "haa pevi the stentorian", "maa febi the steadfast", "muu febi the steadfast", "tzee xicu idol",
        "xuu bhoqa the enigma", "fuu tzapo the blessed", "naa yixo the stillrage",
        "tee zaksa the ceaseless", "arch tzee xicu idol", "avatar icon", "avatar idol",
        "vanguard assassin", "vanguard chanter", "vanguard exemplar", "vanguard inciter",
        "vanguard liberator", "vanguard ogresoother", "vanguard oracle", "vanguard partisan",
        "vanguard persecutor", "vanguard prelate", "vanguard priest", "vanguard salvager",
        "vanguard sentinel", "vanguard skirmisher", "vanguard visionary", "vanguard's avatar",
        "vanguard's crow", "vanguard's wyvern", "xuu bhoqa's avatar"]

# The Time Extension roster from the page's info row. Only the zones these records ALREADY
# carry are flagged — the six with no zone at all cannot be placed from this page.
TE_MOBS = ["adamantking effigy", "effigy prototype", "avatar icon", "icon prototype",
           "warchief tombstone", "tombstone prototype", "goblin statue", "statue prototype",
           "rearguard eye", "prototype eye"]

p = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(p, encoding='utf-8')); mobs = d['mobs']

zoned = []
for k in PAGE:
    m = mobs[k]
    zs = m.setdefault('zones', [])
    if not any((e[0] if isinstance(e, list) else e) == ZONE for e in zs):
        zs.append([ZONE]); zoned.append(k)
    want = BOSS_TAG if k == BOSS else TAG
    tags = m.get('content') or []
    if k == BOSS and TAG in tags: tags.remove(TAG)
    if want not in tags: tags.append(want)
    m['content'] = tags

te_set, te_none = [], []
for k in TE_MOBS:
    m = mobs[k]
    zs = [(e[0] if isinstance(e, list) else e) for e in (m.get('zones') or [])]
    dz = [z for z in zs if z.startswith('Dynamis-')]
    if not dz:
        te_none.append(k); continue
    tags = m.get('content') or []
    for z in dz:
        plain, te = f"Dynamis: {z}", f"Dynamis: {z}: TE"
        if plain in tags: tags.remove(plain)
        if te not in tags: tags.append(te); te_set.append(f"{k} @ {z}")
    m['content'] = tags

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print(f"zone added (level-less) to {len(zoned)}: {', '.join(zoned)}")
print(f"boss: {BOSS} -> {mobs[BOSS]['content']}")
print(f"TE flagged ({len(te_set)}): {', '.join(te_set)}")
print(f"TE mobs with NO Dynamis zone yet ({len(te_none)}): {', '.join(te_none)}")
