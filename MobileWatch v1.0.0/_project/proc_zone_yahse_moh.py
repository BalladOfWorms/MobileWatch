#!/usr/bin/env python3
"""
proc_zone_yahse_moh.py — refining-phase zone pass (rev 312):
Yahse Hunting Grounds + Moh Gates.

RULE 188 run first on both: the twin check found nothing, bucket E returned one row each.

These are Adoulin-era pages and they publish almost no levels — Yahse fills 8 of 26 Lv cells and
**Moh Gates fills only 5 of 29**, so nearly every write here is a bare zone add under rule 1.

Author: BalladOfWorms
"""
import json, os, re, sys
from collections import defaultdict

SKIP = object()

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
MOBS = os.path.join(ASSETS, "mobs.json")

YH = "Yahse Hunting Grounds"
MG = "Moh Gates"

ROWS = {
    YH: {
        # --- Notorious Monsters (2) ---
        "bothersome chapuli": SKIP,
        "startled uragnite": SKIP,          # zero zones
        # --- Adversaries (24); 18 of the 24 Lv cells are blank ---
        "beady panopt": SKIP,
        "bight uragnite": "100-101",
        "broad scarlet": SKIP,
        "burning mantis": SKIP,
        "calfcleaving chapuli": SKIP,
        "canopycrusher beetle": "100-101",
        "crusty crab": SKIP,
        "edacious orobon": "101-102",
        "fiery wasp": "100-101",
        "frondescent leafkin": SKIP,
        "hinterland peiste": SKIP,
        "jungle baelfyr": SKIP,             # zero zones
        "luckybug hoarder": SKIP,
        "monstrosiraptor": SKIP,
        "nettled wasp": "100-101",
        "numbing blossom": SKIP,            # zero zones, fam=None, blank Genus (see rev notes)
        "pinetorum": "100",
        "shy heartwing": SKIP,              # zero zones
        "twitherym infestation": "100",     # page prints 100-100
        "ulbukan sheep": SKIP,
        "umbril": SKIP,
        "velkk marauder": SKIP,
        "verdant treant": "100-102",
        "wooded ungeweder": SKIP,
    },
    MG: {
        # --- Notorious Monsters (2) ---
        "staumarth": SKIP,                  # zero zones
        "stinkskin": SKIP,
        # --- Adversaries (27); 24 of the 27 Lv cells are blank ---
        "apex eft": "125-127",
        "apex eruca": "125-127",
        "apex matamata": "125-127",
        "apex raptor": "125-127",
        "blustering twitherym": SKIP,       # zero zones
        "boiling obdella": SKIP,            # zero zones
        "cave panopt": SKIP,
        "conflagrant eruca": "101-102",
        "consecrated baelfyr": SKIP,        # zero zones
        "crestfallen baelfyr": SKIP,        # zero zones
        "cthonic chapuli": SKIP,
        "disturbed matamata": SKIP,
        "erupting geyser": SKIP,            # zero zones, fam=Environment
        "erythemic eft": SKIP,
        "ferocious funguar": SKIP,
        "gleeful ungeweder": SKIP,          # zero zones
        "knotted root": SKIP,               # zero zones, fam=Obstacle
        "menacing mantis": SKIP,
        "nachtschatten": SKIP,              # zero zones
        "pepper hare": SKIP,
        "pungent fungus": SKIP,             # zero zones, fam=Environment
        "repugnant twitherym": SKIP,
        "ruby raptor": SKIP,
        "scoriaceous clot": SKIP,           # zero zones
        "submerged slime": SKIP,            # zero zones
        "writhing leech": SKIP,
        "writhing obdella": SKIP,
    },
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
    print("TWIN-DUPLICATE GUARD: 0 on both zones")


if __name__ == "__main__":
    main()
