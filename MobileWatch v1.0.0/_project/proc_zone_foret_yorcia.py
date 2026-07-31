#!/usr/bin/env python3
"""
proc_zone_foret_yorcia.py — refining-phase zone pass (rev 313):
Foret de Hennetiel + Yorcia Weald.

RULE 188 run first on both. Twin check clean; bucket E returned two rows on Foret and one on Yorcia.

`Numbing Blossom` appears on BOTH tables in BOTH zones (NM row with Genus **Blossom**, plus an
Adversaries row with a blank Genus) — the rule-201 shape, 4th and 5th instances, and the first time
it is the SAME mob in two different zones. zoneinfo files it under `nms` only in both.

Author: BalladOfWorms
"""
import json, os, re, sys
from collections import defaultdict

SKIP = object()

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
MOBS = os.path.join(ASSETS, "mobs.json")

FH = "Foret de Hennetiel"
YW = "Yorcia Weald"

ROWS = {
    FH: {
        # --- Notorious Monsters (9) ---
        "cunning craklaw": "~105",
        "numbing blossom": SKIP,
        "pungent patricia": SKIP,
        "faded craklaw": SKIP,
        "aberrant uragnite": SKIP,          # zero zones
        "divagating jagil": SKIP,           # zero zones
        "nerrivik": SKIP,
        "krabakarpo": SKIP,
        "tchakka": SKIP,
        # --- Adversaries (29) ---
        "bashful heartwing": "103-104",     # zero zones
        "bellicose tarichuk": "102-103",
        "blood toad": SKIP,
        "broadleaf palm": SKIP,             # zero zones, fam=Obstacle
        "careening twitherym": "102-103",
        "cinder crab": SKIP,
        "craklaw": SKIP,
        "epigean leafkin": "102-103",
        "famished jagil": "100",            # zero zones
        "glutinous clot": "103-104",
        "gurgling crab": "100",             # zero zones
        "hoary craklaw": "103-104",
        "perfidious crab": "102-103",
        "phantasmagoric umbril": "103-104",
        "primordial orobon": "103-104",
        "primrose jagil": SKIP,
        "riverwashed toad": "102-103",
        "scummy slug": "102-103",
        "sere stump": SKIP,                 # zero zones, fam=Lair
        "shrouded obdella": "102-103",
        "skinsipper chigoe": "102-103",     # zero zones
        "treefrost gefyrst": "103-104",
        "vampire leech": "102-103",
        "velkk destructeur": "104-106",
        "velkk sage": "104-106",
        "vorst gnat": "103-104",
        "wetlands orobon": SKIP,
        "zoldeff jagil": "102-103",
    },
    YW: {
        # --- Notorious Monsters (7) ---
        "numbing blossom": SKIP,
        "xag'nar": SKIP,
        "laevvid": SKIP,
        "morseiu": SKIP,
        "ircinraq": SKIP,
        "hyoscya": SKIP,
        "yumcax": SKIP,
        # --- Adversaries (36); 32 of the 36 Lv cells are blank ---
        "abashed heartwing": SKIP,          # zero zones
        "arboreal bastion": SKIP,           # zero zones, fam=Lair
        "bronzecap": SKIP,
        "cheeky opo-opo": "107-109",
        "corpse flower": "107-109",
        "crabapple treant": SKIP,           # zero zones
        "crusty crab": SKIP,
        "droughted treant": "107-109",
        "fervid funguar": SKIP,             # zero zones
        "furfluff lapinion": SKIP,          # zero zones
        "furibund rafflesia": SKIP,         # zero zones
        "gnarled rampart": SKIP,            # zero zones, fam=Obstacle
        "grove wasp": "107-108",
        "gully toad": SKIP,
        "irksome leafkin": SKIP,            # zero zones
        "larkish opo-opo": SKIP,            # zero zones
        "leaflick lapinion": "107-109",
        "loyal snapweed": SKIP,             # zero zones
        "luckybug": "107-109",
        "nascent sapling": "107-109",
        "rustled panopt": SKIP,             # zero zones
        "saptrap": "107-109",
        "shade-speckled spider": SKIP,
        "shadowscourge umbril": SKIP,
        "sloshmouth snapweed": SKIP,        # zero zones
        "snapweed": "107-109",
        "soiled funguar": SKIP,             # zero zones
        "stolid byrgen": SKIP,              # zero zones
        "swollen chigoe": SKIP,
        "tenacious panopt": SKIP,           # zero zones
        "tight-lipped flytrap": SKIP,       # zero zones
        "twitherym": "107-109",
        "twitherym windstorm": SKIP,        # zero zones
        "underwood eruca": "107-109",
        "uprooted sapling": SKIP,           # zero zones
    },
}

LV_UNION = {
    "treefrost gefyrst": [103, 104],        # was [104,104]; page gives 103-104
}


def zname(e):
    return e[0] if isinstance(e, list) else e


def main():
    d = json.load(open(MOBS, encoding="utf-8"))
    mobs = d["mobs"]
    report = {}

    for ZONE, rows in ROWS.items():
        missing, added, changed, filled, kept = [], [], [], [], []
        for key, lvl in rows.items():
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
        report[ZONE] = (rows, missing, added, changed, filled, kept)

    unions = []
    for key, new in LV_UNION.items():
        old = mobs[key].get("lv")
        mobs[key]["lv"] = new
        unions.append((key, old, new))

    groups = defaultdict(set)
    for k in mobs:
        groups[re.sub(r"[^a-z0-9]", "", k)].add(k)
        base = re.sub(r"\s*\([^)]*\)$", "", k)
        if base != k and base in mobs:
            groups[f"~{base}"] |= {base, k}
    for ZONE in ROWS:
        dupes = [sorted(g) for g in groups.values()
                 if sum(any(zname(e) == ZONE for e in (mobs[k].get("zones") or [])) for k in g) > 1]
        assert not dupes, f"twin pair both holding {ZONE}: {dupes}"

    bad = [k for m in mobs.values() for k, v in m.items() if v is None]
    assert not bad, f"null-valued keys written: {bad[:5]}"
    json.dump(d, open(MOBS, "w", encoding="utf-8"),
              separators=(", ", ": "), ensure_ascii=False)

    for ZONE, (rows, missing, added, changed, filled, kept) in report.items():
        print("=" * 74)
        print(f"{ZONE} — {len(rows)} rows")
        print(f"  MISSING ({len(missing)}): {missing}")
        print(f"  ZONE ADDED ({len(added)}):")
        for k, v in added:
            print(f"      {k:26s} {v}")
        print(f"  LEVEL FILLED ({len(filled)}):")
        for k, v in filled:
            print(f"      {k:26s} -> {v}")
        print(f"  LEVEL CHANGED ({len(changed)}):")
        for k, a, b in changed:
            print(f"      {k:26s} {a} -> {b}")
        print(f"  KEPT, page cell blank ({len(kept)})")
    print("=" * 74)
    print(f"RULE-9 lv UNIONS ({len(unions)}):")
    for k, a, b in unions:
        print(f"      {k:26s} {a} -> {b}")
    print("TWIN-DUPLICATE GUARD: 0 on both zones")


if __name__ == "__main__":
    main()
