#!/usr/bin/env python3
"""
proc_zone_mamook.py — refining-phase zone pass: Mamook (rev 308).

RULE 188 RUN FIRST. The twin check fired, and for the first time it found a duplicate that was
ALREADY IN THE FILE rather than one I was about to create: `poroggo` and `poroggo (nm)` BOTH hold
`Mamook 75-77` **and** `Mamool Ja Training Grounds`. `poroggo (nm)` is a strict subset of `poroggo`
(same ab/agg/crys/det/fam/job/lnk/st/wk/zones; it just lacks `lv`, `resp` and the 32-spell `sp`
list, and its `nm` flag is not even set). The right fix is deleting the whole record, which is a
merge = the user's call (rev 283 Gargoyle precedent) — so NOTHING is touched here and the pair is
allow-listed below so the guard still catches anything NEW.

`Mamool Ja Conservator` appears on BOTH tables (an NM row "Assists: Archaic Mirror" with a blank Lv,
and an Adversaries row at 81-83). zoneinfo files it under `nms` and takes the level from the
ADVERSARIES row — the same shape as Halvung's two Mirror Guards (rev 305) and Arrapago's Lamia
Palace Guard (rev 303). One record, level filled from the ADV row.

Author: BalladOfWorms
"""
import json, os, re, sys
from collections import defaultdict

SKIP = object()
ZONE = "Mamook"

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
MOBS = os.path.join(ASSETS, "mobs.json")

# pre-existing duplicates, deliberately untouched (see docstring)
KNOWN_DUP = {frozenset({"poroggo", "poroggo (nm)"})}

ROWS = {
    # --- Notorious Monsters (15) ---
    "chamrosh": "77-82",
    "darting kachaal ja": "83",
    "devout radol ja": "83",
    "dragonscaled bugaal ja": "83",
    "gulool ja ja": SKIP,               # Lv cell reads `?` (rule 10)
    "hundredfaced hapool ja": "83",
    "iriri samariri": SKIP,             # Lv blank -> keeps stored 84
    "zizzy zillah": SKIP,
    "firedance magmaal ja": SKIP,       # zero zones
    "venomfang": SKIP,                  # zero zones
    "carpophagous puk": SKIP,           # zero zones
    "mamool ja conservator": "81-83",   # both tables; level from the ADV row
    "mamool ja treasurer": SKIP,        # NM row only, blank Lv
    "mamool ja (nm)": SKIP,
    "yalungur": SKIP,                   # Voidwatch, blank Lv
    # --- Adversaries (39; `poroggo` already exact, see docstring) ---
    "air elemental": "75-80",
    "archaic mirror": SKIP,
    "battle bugard": "77-78",
    "brei": "77-78",
    "carriage lizard": "72-74",
    "colibri": "70-71",
    "hunting raptor": "73-74",
    "mamook crab": "75-76",
    "mamook mush": SKIP,                # Fished Up, blank Lv, zero zones
    "mamool ja bloodsucker": "69-70",
    "mamool ja blusterer": "81-83",
    "mamool ja bounder": "73-75",
    "mamool ja diver": "75-77",
    "mamool ja frogman": "75-77",
    "mamool ja infiltrator": "81-83",
    "mamool ja lurker": "81-83",
    "mamool ja mimer": "81-83",
    "mamool ja mimicker": "73-75",
    "mamool ja philosopher": "81-83",
    "mamool ja pikeman": "81-83",
    "mamool ja savant": "73-75",
    "mamool ja sophist": "73-75",
    "mamool ja spearman": "73-75",
    "mamool ja stabler": "81-83",
    "mamool ja strapper": "73-75",
    "mamool ja zenist": "73-75",
    "mamool ja's lizard": "68",
    "mamool ja's raptor": SKIP,         # Lv cell blank
    "mamool ja's wyvern": "67-78",
    "nipper": "76-77",
    "poroggo": "75-77",
    "puk": "70-72",                     # zero zones
    "qiqirn goldsmith": "77",
    "qiqirn poulterer": "77",
    "sea puk": "76-78",
    "spinner": "79-81",
    "suhur mas": "68-71",
    "watch wyvern": "82-83",            # zero zones
    "ziz": "76-78",
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

    byn = defaultdict(list)
    for k in mobs:
        byn[re.sub(r"[^a-z0-9]", "", k)].append(k)
    # also group suffixed variants: "x (nm)" / "x (monster)" / "x (fished)" with bare "x"
    for k in list(mobs):
        base = re.sub(r"\s*\([^)]*\)$", "", k)
        if base != k and base in mobs:
            byn[f"~{base}"] = sorted({base, k} | set(byn.get(f"~{base}", [])))
    dupes = []
    for group in byn.values():
        holders = [k for k in group
                   if any(zname(e) == ZONE for e in (mobs[k].get("zones") or []))]
        if len(holders) > 1 and frozenset(holders) not in KNOWN_DUP:
            dupes.append(holders)
    assert not dupes, f"NEW twin pair both holding {ZONE}: {dupes}"

    bad = [k for m in mobs.values() for k, v in m.items() if v is None]
    assert not bad, f"null-valued keys written: {bad[:5]}"
    json.dump(d, open(MOBS, "w", encoding="utf-8"),
              separators=(", ", ": "), ensure_ascii=False)

    print(f"=== {ZONE} — {len(ROWS)} rows (page publishes 15 NM + 39 ADV; Conservator is on both)")
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
    print(f"\nKEPT, page cell blank / `?` ({len(kept)}):")
    for k, v in kept:
        print(f"    {k:26s} stored {v}")
    print(f"\nNEW twin duplicates: 0 | pre-existing, flagged not touched: "
          f"{[sorted(s) for s in KNOWN_DUP]}")
    n_ok = len(ROWS) - len(added) - len(filled) - len(changed) - len(missing)
    print(f"Already right (incl. keeps): {n_ok} of {len(ROWS)}")


if __name__ == "__main__":
    main()
