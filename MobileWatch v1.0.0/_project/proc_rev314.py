#!/usr/bin/env python3
"""
proc_rev314.py — three jobs (rev 314):

  1. USER RULING: "blossom can be a genus under the family of structures>environment."
     -> `numbing blossom` gets `fam="Environment"`, which sits under eco `Structures`.
     This SUPERSEDES rev 313's withdrawal: `Blossom` is the wiki's Genus label, but in our
     taxonomy it belongs to the existing Environment family rather than becoming a new `fam`.

  2. YORCIA WEALD (U) — the 11 rows of the page's "Notorious Monsters Found Here" table.
     All 11 records already exist and are well built out (ab / crys / det / fam / job / st / wk,
     and the correct `spawn` strings INCLUDING the Faithful's-Torso-II tier gate on three of them).
     What they lack is the zone (10 of 11) and the `nm` flag (all 11).
     **Zone string is the BRACKETED `Yorcia Weald [U]`** — the file's convention, 18 records deep,
     even though zones.json spells it `Yorcia Weald U`; the app's normalizer strips the brackets.

  3. MORIMAR BASALT FIELDS — an ordinary zone pass. `Steam Spout` is on BOTH tables (rule 201,
     6th instance); zoneinfo files it under `nms` only.

Author: BalladOfWorms
"""
import json, os, re, sys
from collections import defaultdict

SKIP = object()

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
MOBS = os.path.join(ASSETS, "mobs.json")

YU = "Yorcia Weald [U]"
MB = "Morimar Basalt Fields"

FAM_SET = {"numbing blossom": "Environment"}      # job 1, user-authorised

YORCIA_U = [                                       # job 2 — all level-less, page Level is "?"
    "flustered funguar", "frothing snapweed", "inflamed flytrap", "mulcher beetle",
    "unblinking panopt", "windblown treant", "woodlot luckybug", "dithering heartwing",
    "feverish ameretat", "sly opo-opo", "highhop lapinion",
]

ROWS = {                                           # job 3
    MB: {
        # --- Notorious Monsters (8) ---
        "burgeoning flames": SKIP,      # zero zones, fam=None
        "steam spout": SKIP,            # zero zones, fam=Environment; on BOTH tables
        "volatile matamata": "110",     # zero zones
        "perdurable raptor": SKIP,      # zero zones
        "shimmering tarichuk": SKIP,
        "tutewehiwehi": SKIP,
        "kurma": SKIP,
        "achuka": SKIP,                 # zero zones
        # --- Adversaries (31; Steam Spout above) ---
        "acerbic jagil": "102-104",
        "alpine eft": SKIP,             # zero zones
        "animosiraptor": "102-103",
        "anthousai": "107-109",
        "basalt lizard": SKIP,
        "bedrock crag": SKIP,           # zero zones, fam=Obstacle
        "befuddled twitherym": "107-109",
        "bumbling leafkin": SKIP,
        "felsic eruca": "102-103",      # zero zones
        "frosty twitherym": "102-104",
        "grimy boulders": SKIP,         # zero zones, fam=Lair
        "hoarfrost gefyrst": "102-104", # zero zones
        "lavawalker raptor": "107-109", # zero zones
        "maca maca": SKIP,
        "mafic spider": "102-104",
        "matamata": SKIP,
        "minacious matamata": SKIP,     # zero zones
        "mountain peiste": "102-104",
        "outlands peiste": SKIP,
        "petrous lizard": SKIP,
        "qohanyk": "102-104",
        "sinewy matamata": "102-104",
        "snaggletooth raptor": SKIP,
        "snowcap umbril": "102-104",
        "steamed jagil": "100",         # zero zones; page prints 100-100
        "tephra lizard": "102-103",
        "tundra eft": "102-103",
        "twirling heartwing": "104",    # zero zones; page prints 104-104
        "volcanic wivre": "103-105",
        "wivre cragdweller": SKIP,      # zero zones
    },
}

LV_UNION = {"snowcap umbril": [102, 104]}          # was [103,104]; page gives 102-104


def zname(e):
    return e[0] if isinstance(e, list) else e


def main():
    d = json.load(open(MOBS, encoding="utf-8"))
    mobs = d["mobs"]

    # ---- job 1: the Blossom ruling ----
    fam_done = []
    for k, fam in FAM_SET.items():
        before = mobs[k].get("fam")
        mobs[k]["fam"] = fam
        fam_done.append((k, before, fam))

    # ---- job 2: Yorcia Weald (U) ----
    yu_added, yu_flagged, yu_had = [], [], []
    for k in YORCIA_U:
        r = mobs[k]
        zs = r.get("zones")
        if not isinstance(zs, list):
            zs = []
        if any(zname(e) == YU for e in zs):
            yu_had.append(k)
        else:
            zs.append([YU])
            r["zones"] = zs
            yu_added.append(k)
        if not r.get("nm"):
            r["nm"] = True
            yu_flagged.append(k)

    # ---- job 3: Morimar ----
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
    for ZONE in list(ROWS) + [YU]:
        dupes = [sorted(g) for g in groups.values()
                 if sum(any(zname(e) == ZONE for e in (mobs[k].get("zones") or [])) for k in g) > 1]
        assert not dupes, f"twin pair both holding {ZONE}: {dupes}"

    bad = [k for m in mobs.values() for k, v in m.items() if v is None]
    assert not bad, f"null-valued keys written: {bad[:5]}"
    json.dump(d, open(MOBS, "w", encoding="utf-8"),
              separators=(", ", ": "), ensure_ascii=False)

    print("=== 1. USER RULING — Blossom")
    for k, a, b in fam_done:
        print(f"    {k:22s} fam {a!r} -> {b!r}   (eco Structures)")
    print(f"\n=== 2. YORCIA WEALD (U) — {len(YORCIA_U)} page rows, zone string {YU!r}")
    print(f"    zone added ({len(yu_added)}): {yu_added}")
    print(f"    already held ({len(yu_had)}): {yu_had}")
    print(f"    nm flag set ({len(yu_flagged)}): {yu_flagged}")
    for ZONE, (rows, missing, added, changed, filled, kept) in report.items():
        print(f"\n=== 3. {ZONE} — {len(rows)} rows")
        print(f"    MISSING ({len(missing)}): {missing}")
        print(f"    ZONE ADDED ({len(added)}):")
        for k, v in added:
            print(f"        {k:24s} {v}")
        print(f"    LEVEL FILLED ({len(filled)}):")
        for k, v in filled:
            print(f"        {k:24s} -> {v}")
        print(f"    LEVEL CHANGED ({len(changed)}):")
        for k, a, b in changed:
            print(f"        {k:24s} {a} -> {b}")
        print(f"    KEPT, page cell blank ({len(kept)})")
    print(f"\nRULE-9 lv UNIONS ({len(unions)}):")
    for k, a, b in unions:
        print(f"    {k:24s} {a} -> {b}")
    print("TWIN-DUPLICATE GUARD: 0 on both zones")


if __name__ == "__main__":
    main()
