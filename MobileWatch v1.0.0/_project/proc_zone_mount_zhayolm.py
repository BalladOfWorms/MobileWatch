#!/usr/bin/env python3
"""
proc_zone_mount_zhayolm.py — refining-phase zone pass: Mount Zhayolm (rev 306).

RULE 188 WAS RUN FIRST: bucket E and the alternate-spelling twin check both executed BEFORE any
write. The twin check fired once — the page's `Giant Orobon` row belongs to
`giant orobon (fished)`, which ALREADY holds this zone; the bare `giant orobon` record is
deliberately absent from ROWS so no duplicate is created. Third zone running for that pair
(Arrapago r303, Talacca r305, here).

Author: BalladOfWorms
"""
import json, os, sys

SKIP = object()
ZONE = "Mount Zhayolm"

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
MOBS = os.path.join(ASSETS, "mobs.json")

ROWS = {
    # --- Notorious Monsters (22; `giant orobon` handled by its twin, see docstring) ---
    "anantaboga": "80-90",
    "brass borer": "82-83",
    "cerberus": "85",
    "claret": SKIP,                     # Lv blank -> keeps stored 82-83
    "energetic eruca": "80",
    "garfurlar the rabid": "80",
    "garharlor the unruly": "80",
    "garhorlur the brutal": "80",
    "khromasoul bhurborlor": SKIP,
    "sarameya": "85-90",
    "chary apkallu": SKIP,              # zero zones
    "fahrafahr the bloodied": "~80",    # zero zones; tilde stored verbatim (rule 11)
    "ignamoth": SKIP,                   # zero zones, fam=None
    "ancient bombs": SKIP,
    "troll speculator": SKIP,
    "dark rider": SKIP,
    "dark esquire": SKIP,
    "dark bugler": SKIP,
    "grand grenade": "128",
    "sarama": "135",
    "vanasarvik": SKIP,
    # --- Adversaries (27) ---
    "assassin fly": "71-74",
    "dahak": "82-83",
    "earth elemental": SKIP,            # weather-gated, Lv cell blank
    "ebony pudding": "75-80",
    "fire elemental": SKIP,             # weather-gated, Lv cell blank
    "hilltroll dark knight": "79-83",
    "hilltroll monk": "79-82",
    "hilltroll paladin": "79-83",
    "hilltroll puppetmaster": "79-83",
    "hilltroll ranger": "79-83",
    "hilltroll red mage": "79-82",
    "hilltroll warrior": "80-82",
    "king apkallu": "70-80",
    "magmatic eruca": "71-75",
    "mountain clot": "72-75",
    "phasma": "73-76",
    "sicklemoon crab": "71-73",
    "sicklemoon jagil": "73-76",
    "volcanic leech": "72-75",
    "vozold clot": "74-75",
    "vozold jagil": "75-76",
    "wamoura": "80",                    # page prints 80-80 -> collapses to a point
    "wamoura prince": "79-81",
    "wootzshell": "70-71",              # rev 303's rule-182 correction, confirmed by this page
    "zazalda clot": "71-73",
    "zazalda jagil": "74-75",
    "zhayolm apkallu": "70-74",
}

# Rule 9 — union where a correction/add landed outside the stored band.
LV_UNION = {
    "anantaboga": [80, 90],     # was [85,87]; nmlv already read 80-90
    "king apkallu": [70, 80],   # was [78,80]
    "ebony pudding": [75, 80],  # was [76,80]
}


def zname(e):
    return e[0] if isinstance(e, list) else e


def main():
    d = json.load(open(MOBS, encoding="utf-8"))
    mobs = d["mobs"]
    missing, added, changed, filled, kept = [], [], [], [], []

    for key, lvl in ROWS.items():
        r = mobs.get(key)
        if r is None:
            missing.append(key)
            continue
        zs = r.get("zones")
        if not isinstance(zs, list):
            zs = []
        idx = next((i for i, e in enumerate(zs) if zname(e) == ZONE), None)
        if idx is None:
            zs.append([ZONE] if lvl is SKIP else [ZONE, lvl])
            added.append((key, None if lvl is SKIP else lvl))
            r["zones"] = zs
            continue
        ent = zs[idx]
        cur = ent[1] if isinstance(ent, list) and len(ent) > 1 else None
        if lvl is SKIP:
            kept.append((key, cur))
        elif cur is None:
            zs[idx] = [ZONE, lvl]
            filled.append((key, lvl))
        elif cur != lvl:
            zs[idx] = [ZONE, lvl]
            changed.append((key, cur, lvl))

    unions = []
    for key, new in LV_UNION.items():
        old = mobs[key].get("lv")
        mobs[key]["lv"] = new
        unions.append((key, old, new))

    # duplicate guard: no zone may be held twice by a normalized-name twin pair
    from collections import defaultdict
    import re
    byn = defaultdict(list)
    for k in mobs:
        byn[re.sub(r"[^a-z0-9]", "", k)].append(k)
    dupes = []
    for group in byn.values():
        if len(group) < 2:
            continue
        holders = [k for k in group
                   if any(zname(e) == ZONE for e in (mobs[k].get("zones") or []))]
        if len(holders) > 1:
            dupes.append(holders)
    assert not dupes, f"twin pair both holding {ZONE}: {dupes}"

    bad = [k for m in mobs.values() for k, v in m.items() if v is None]
    assert not bad, f"null-valued keys written: {bad[:5]}"
    json.dump(d, open(MOBS, "w", encoding="utf-8"),
              separators=(", ", ": "), ensure_ascii=False)

    print(f"=== {ZONE} — {len(ROWS)} rows written (page publishes 49; Giant Orobon is its twin's)")
    print(f"MISSING ({len(missing)}): {missing}")
    print(f"\nZONE ADDED ({len(added)}):")
    for k, v in added:
        print(f"    {k:26s} {v}")
    print(f"\nLEVEL FILLED ({len(filled)}):")
    for k, v in filled:
        print(f"    {k:26s} -> {v}")
    print(f"\nLEVEL CHANGED ({len(changed)}):")
    for k, a, b in changed:
        print(f"    {k:26s} {a} -> {b}")
    print(f"\nKEPT, page cell blank ({len(kept)}):")
    for k, v in kept:
        print(f"    {k:26s} stored {v}")
    print(f"\nRULE-9 lv UNIONS ({len(unions)}):")
    for k, a, b in unions:
        print(f"    {k:26s} {a} -> {b}")
    print("\nTWIN-DUPLICATE GUARD: 0")


if __name__ == "__main__":
    main()
