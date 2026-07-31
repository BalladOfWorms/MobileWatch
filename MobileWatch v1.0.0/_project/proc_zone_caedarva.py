#!/usr/bin/env python3
"""
proc_zone_caedarva.py — refining-phase zone pass: Caedarva Mire (rev 303).

Also reverts a rev-302 mistake of mine: I zoned the BARE `chigoe` record at Bhaflau Thickets
71-73 because that page writes plain "Chigoe", but `chigoe (monster)` ALREADY held Bhaflau
71-73 — so Bhaflau ended up with the mob twice. This page writes "Chigoe (Monster)" and
zoneinfo carries the suffix, which settles which record the Aht Urhgan Chigoe is.

NOTE ON `lamia no.27`: the page writes "Lamia No.27" (dot) and the DOT-spelled record has zero
zones — but the SPACE-spelled twin `lamia no 27` already holds Caedarva Mire. They are a
split-duplicate pair (see the file-wide sweep in the rev notes). Nothing added; zoning the dot
form would put two Lamia No.27s in the Zone view.

Author: BalladOfWorms
"""
import json, os, sys

SKIP = object()
ZONE = "Caedarva Mire"

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
MOBS = os.path.join(ASSETS, "mobs.json")

ROWS = {
    # --- Notorious Monsters (19) ---
    "experimental lamia": "80-90",
    "khimaira": SKIP,                 # Lv blank -> keeps stored 85
    "mahjlaef the paintorn": "80-90",
    "peallaidh": SKIP,                # Lv blank -> keeps stored 73-75
    "tyger": "85-90",
    "verdelet": "80-90",
    "zikko": "80",
    "aynu-kaysey": SKIP,
    "vidhuwa the wrathborn": SKIP,    # zero zones AND no lv anywhere
    "caedarva toad": SKIP,
    "dark rider": SKIP,
    "dark esquire": SKIP,
    "dark bugler": SKIP,
    "lamia deathdancer": SKIP,
    # "lamia no.27" deliberately absent — see module docstring
    "moshdahn": SKIP,
    "ravin raven": SKIP,
    "shedu": "135",
    "brekekekex": SKIP,
    # --- Adversaries (36) ---
    "caedarva leech": "63-65",
    "caedarva marshscum": "66-67",
    "caedarva pondscum": "64-66",
    "chigoe (monster)": "62-66",
    "dark elemental": SKIP,           # weather-gated, Lv cell blank
    "draugar servant": "79",
    "draugar's wyvern": "74",
    "elder treant": "79-82",
    "ephramadian shade": "75-77",
    "guard bhoot": "81-83",
    "guard skeleton": "66-69",
    "heraldic imp": "80-81",
    "jnun": "72-77",
    "lamia chaukidar": "82-83",
    "lamia fatedealer": "73-75",
    "lamia idolater": "79-81",
    "lamia necromancer": "81-83",
    "lamia toxophilite": "77-80",
    "llamhigyn y dwr": "75-76",
    "locus imp": "120-132",
    "marsh murre": "64-67",
    "mature treant": "71-72",
    "mosshorn": "80-81",
    "oil slick": "65-67",
    "orderly imp": "63-68",
    "puktrap": "67-69",
    "qiqirn mireguide": "67-69",
    "qiqirn rock hound": "67-69",
    "reserve draugar": "73-74",
    "soulflayer": "79-82",
    "spongilla fly": "78-79",
    "thunder elemental": SKIP,        # weather-gated, Lv cell blank
    "treant sapling": "61-64",
    "water elemental": SKIP,          # weather-gated, Lv cell blank
    "wild karakul": "68-70",
    "slough skua": "88-89",
}

# Rule 9 — union where a correction/fill landed outside the stored band.
# SUSPENDED on `locus imp`: lv [134,136] vs page 120-132 are DISJOINT, so a union would
# invent 120-136. (kz) debt, same class as nunyunuwi / agas / rancor torch.
LV_UNION = {
    "experimental lamia": [80, 90],   # was [82,84]; nmlv already read 80-90
    "verdelet": [80, 90],             # was [85,86]; nmlv already read 80-90
    "lamia toxophilite": [77, 83],    # was [81,83]; both its zones now read 77-80
}

# rev-302 revert
REVERT = [("chigoe", "Bhaflau Thickets")]


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

    reverted = []
    for key, z in REVERT:
        r = mobs[key]
        zs = r.get("zones") or []
        new = [e for e in zs if zname(e) != z]
        if len(new) != len(zs):
            if new:
                r["zones"] = new
            else:
                r.pop("zones", None)      # never write an empty list where none existed
            reverted.append((key, z, new))

    bad = [k for m in mobs.values() for k, v in m.items() if v is None]
    assert not bad, f"null-valued keys written: {bad[:5]}"
    json.dump(d, open(MOBS, "w", encoding="utf-8"),
              separators=(", ", ": "), ensure_ascii=False)

    print(f"=== {ZONE} — {len(ROWS)} page records processed (54 of the page's 55; see docstring)")
    print(f"MISSING ({len(missing)}): {missing}")
    print(f"\nZONE ADDED ({len(added)}):")
    for k, v in added:
        print(f"    {k:24s} {v}")
    print(f"\nLEVEL FILLED ({len(filled)}):")
    for k, v in filled:
        print(f"    {k:24s} -> {v}")
    print(f"\nLEVEL CHANGED ({len(changed)}):")
    for k, a, b in changed:
        print(f"    {k:24s} {a} -> {b}")
    print(f"\nKEPT, page cell blank ({len(kept)}):")
    for k, v in kept:
        print(f"    {k:24s} stored {v}")
    print(f"\nRULE-9 lv UNIONS ({len(unions)}):")
    for k, a, b in unions:
        print(f"    {k:24s} {a} -> {b}")
    print(f"\nREV-302 REVERT ({len(reverted)}):")
    for k, z, new in reverted:
        print(f"    {k:24s} dropped {z!r}; now {new}")


if __name__ == "__main__":
    main()
