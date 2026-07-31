#!/usr/bin/env python3
"""
proc_zone_ceizak.py — refining-phase zone pass: Ceizak Battlegrounds (rev 311).

RULE 188 run first: bucket E returned three level-less Wildskeeper-adjacent NMs and the twin check
found nothing.

`unfettered twitherym` sits in the NM table with `nm` unset — page-backed flag, the rev-264 /
rev-310 `armed gears` precedent.

Author: BalladOfWorms
"""
import json, os, re, sys
from collections import defaultdict

SKIP = object()
ZONE = "Ceizak Battlegrounds"

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
MOBS = os.path.join(ASSETS, "mobs.json")

ROWS = {
    # --- Notorious Monsters (6). Every Lv cell is blank except Colkhab's. ---
    "unfettered twitherym": SKIP,       # zero zones
    "supernal chapuli": SKIP,
    "transcendent scorpion": SKIP,      # zero zones
    "mastop": SKIP,
    "tax'et": SKIP,
    "colkhab": "105-110",
    # --- Adversaries (25). Thirteen more blank cells. ---
    "appetent umbril": SKIP,
    "barnacled orobon": SKIP,           # zero zones
    "belaboring wasp": "100-101",
    "bight uragnite": "100-101",
    "blanched mandragora": "100",
    "careening twitherym": "100-101",
    "colossal spider": SKIP,
    "cornered heartwing": SKIP,
    "crusty crab": SKIP,                # zero zones
    "deathmaw orobon": "101-102",
    "downy emerald": SKIP,
    "fernfelling chapuli": SKIP,
    "fluffy sheep": SKIP,
    "frenzied mantis": SKIP,
    "irascible baelfyr": SKIP,
    "knobby treant": "100-102",
    "longclaw raptor": SKIP,
    "mischievous leafkin": SKIP,
    "rapier hornet": SKIP,              # zero zones
    "resplendent luckybug": SKIP,
    "sedge scorpion": SKIP,             # zero zones
    "twigtrip lapinion": "100",
    "unbridled ungeweder": SKIP,
    "undergrowth hornet": "100-101",
    "velkk torturer": SKIP,
}

NM_FLAG = ["unfettered twitherym"]      # page-backed: it is an NM-table row


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

    flagged = []
    for key in NM_FLAG:
        if not mobs[key].get("nm"):
            mobs[key]["nm"] = True
            flagged.append(key)

    groups = defaultdict(set)
    for k in mobs:
        groups[re.sub(r"[^a-z0-9]", "", k)].add(k)
        base = re.sub(r"\s*\([^)]*\)$", "", k)
        if base != k and base in mobs:
            groups[f"~{base}"] |= {base, k}
    dupes = [sorted(g) for g in groups.values()
             if sum(any(zname(e) == ZONE for e in (mobs[k].get("zones") or [])) for k in g) > 1]
    assert not dupes, f"twin pair both holding {ZONE}: {dupes}"

    bad = [k for m in mobs.values() for k, v in m.items() if v is None]
    assert not bad, f"null-valued keys written: {bad[:5]}"
    json.dump(d, open(MOBS, "w", encoding="utf-8"),
              separators=(", ", ": "), ensure_ascii=False)

    print(f"=== {ZONE} — {len(ROWS)} rows")
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
    print(f"\nNM FLAGS SET ({len(flagged)}): {flagged}")
    print("TWIN-DUPLICATE GUARD: 0")


if __name__ == "__main__":
    main()
