#!/usr/bin/env python3
"""Dynamis-Jeuno pass (rev 199): 57 records, levels published as tildes.
USER: "next"

The NM table publishes `~80` / `~90` / `~100` and the Vanguard block `90-95`; the tilde is
kept verbatim in the zone entry (the `konjac ~78` precedent) while `lv` takes the number.
`goblin statue` drops Time Extension and is on the TE roster -> `: TE`.
`arch goblin golem` -> `: Boss`, following the pattern the user set for the other three city
zones (Arch Overlord / Arch Tzee Xicu / Arch Gu'Dha). Flagged in the handoff as inferred.
`Members of the Goblin Vanguard` is a COLLECTIVE page row (job column reads "All"), not a mob
name — no record exists and none was created.
"""
import json, os, re
from zonepass import ASSETS

ZONE = "Dynamis-Jeuno"
TAG, BOSS_TAG, TE_TAG = f"Dynamis: {ZONE}", f"Dynamis: {ZONE}: Boss", f"Dynamis: {ZONE}: TE"
BOSS, TE = "arch goblin golem", "goblin statue"

NM80 = ["bandrix rockjaw", "blazox boneybod", "bootrix jaggedelbow", "buffrix eargone",
        "cloktix longnail", "distilix stickytoes", "elixmix hooknose", "eremix snottynostril",
        "gabblox magpietongue", "hermitrix toothrot", "humnox drumbelly", "jabbrox grannyguise",
        "jabkix pigeonpecs", "karashix swollenskull", "kikklix longlegs", "lurklox dhalmelneck",
        "mobpix mucousmouth", "morgmox moldnoggin", "mortilox wartpaws", "prowlox barrelbelly",
        "rutrix hamgams", "scruffix shaggychest", "slystix megapeepers", "smeltix thickhide",
        "snypestix eaglebeak", "sparkspox sweatbrow", "ticktox beadyeyes", "trailblix goatmug",
        "tufflix loglimbs", "tymexox ninefingers", "wasabix callusdigit", "wyrmwix snakespecs",
        "anvilix sootwrists"]
VANGUARD = ["vanguard necromancer", "vanguard tinkerer", "vanguard ambusher", "vanguard enchanter",
            "vanguard armorer", "vanguard dragontamer", "vanguard welldigger", "vanguard shaman",
            "vanguard alchemist", "vanguard hitman", "vanguard maestro", "vanguard ronin",
            "vanguard smithy", "vanguard pathfinder", "vanguard pitfighter"]
ROWS = ([(k, "~80") for k in NM80] +
        [("goblin statue", "~80"), ("goblin golem", "~90"), ("quicktrix hexhands", "~100"),
         ("feralox honeylips", "~100"), ("scourquix scaleskin", "~100"),
         ("wilywox tenderpalm", "~100"), ("arch goblin golem", "~100"),
         ("feralox's slime", None), ("scourquix's wyvern", None)] +
        [(k, "90-95") for k in VANGUARD])

p = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(p, encoding='utf-8')); mobs = d['mobs']
zoned, filled, changed, unions = [], [], [], []
for k, band in ROWS:
    m = mobs[k]
    zs = m.setdefault('zones', [])
    hit = next((e for e in zs if (e[0] if isinstance(e, list) else e) == ZONE), None)
    if hit is None:
        zs.append([ZONE, band] if band else [ZONE]); zoned.append(f"{k} {band or ''}".strip())
    elif band:
        if not isinstance(hit, list):
            i = zs.index(hit); zs[i] = [ZONE, band]; filled.append(k)
        elif len(hit) == 1:
            hit.append(band); filled.append(k)
        elif hit[1] != band:
            changed.append(f"{k} {hit[1]} -> {band}"); hit[1] = band
    if band:                                    # rule 9 — lv from the published number(s)
        nums = [int(x) for x in re.findall(r'\d+', band)]
        lo, hi = min(nums), max(nums)
        lv = m.get('lv')
        if lv is None:
            m['lv'] = [lo, hi]; unions.append(f"{k} -> [{lo},{hi}] (created)")
        elif lo < lv[0] or hi > lv[1]:
            new = [min(lo, lv[0]), max(hi, lv[1])]; unions.append(f"{k} {lv} -> {new}"); m['lv'] = new
    want = BOSS_TAG if k == BOSS else TE_TAG if k == TE else TAG
    tags = [t for t in (m.get('content') or []) if t != TAG or want == TAG]
    if want not in tags: tags.append(want)
    m['content'] = tags

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print(f"zone ADDED ({len(zoned)}): {', '.join(zoned)}")
print(f"zone level FILLED ({len(filled)})")
print(f"zone level CHANGED ({len(changed)}): {', '.join(changed) or '(none)'}")
print(f"lv touched ({len(unions)}): {', '.join(unions[:6])}{' ...' if len(unions) > 6 else ''}")
print("boss:", mobs[BOSS]['content'], "| TE:", mobs[TE]['content'])
