#!/usr/bin/env python3
"""
proc_zone_talacca_halvung.py — rev 305. Two zones: Talacca Cove + Halvung.

Zone strings `Talacca Cove` and `Halvung` — both exact in zones.json, no gotcha.

RULE 179 APPLIED UP FRONT THIS TIME: before writing, every prospective add was checked for an
alternate-spelling twin already holding the zone, using BOTH a normalized-key collision test and a
full bucket-E scan. The normalized test found nothing; **bucket E found two** —
`giant orobon` (twin `giant orobon (fished)` holds Talacca Cove) and `antares` (twin
`antares (monster)` holds Halvung 76-78, already at the page value). Neither is written. That is the
rev-303 lesson working as intended: run bucket E BEFORE the write, not after.

Rule 15 SKIP sentinel: a blank page cell can create a zone entry but never touch a stored level.
Rule 9 unions are declared explicitly rather than computed, so each one is a reviewed decision.

Author: BalladOfWorms
"""
import json, os, sys

SKIP = object()
ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
PATH = os.path.join(ASSETS, "mobs.json")

TAL = "Talacca Cove"
HAL = "Halvung"

ROWS = {
    TAL: {
        "giant orobon": None,          # HOLD: `giant orobon (fished)` already holds this zone
        "arrapago leech": "73-74",
        "lahama": "77-78",
        "llamhigyn y dwr": "77-79",
        "talacca clot": "76-77",
        "wootzshell": "73-74",
    },
    HAL: {
        # --- Notorious Monsters (13) ---
        "achamoth": "80-90", "big bomb": "81-84", "copper borer": "81", "dextrose": "80-90",
        "dorgerwor the astute": "80", "farlarder the shrewd": SKIP,
        "flammeri": SKIP,              # Lv cell reads `?` -> rule 10
        "gurfurlur the menacing": SKIP, "kirlirger the abhorrent": SKIP,
        "mythril mouth monamaq": SKIP, "reacton": "80-90",
        # both Mirror Guards appear on BOTH tables; the ADV table publishes the level
        "hilltroll mirror guard": "82-83", "woodtroll mirror guard": "82-83",
        # --- Adversaries (36) ---
        "antares": None,               # HOLD: `antares (monster)` already holds Halvung 76-78
        "archaic mirror": SKIP, "black pudding": "73-75", "dahak": "78-81",
        "earth elemental": "74-75", "ebony pudding": "77-79", "fire elemental": "74-75",
        "friar's lantern": "72-74", "hilltroll elite guard": SKIP, "magmatic eruca": "71-75",
        "moblin billionaire": "76-77", "moblin millionaire": "76-77", "purgatory bat": "70-72",
        "qiqirn diamantaire": "72-73", "qiqirn mercenary": "71-73", "troll artilleryman": "78-82",
        "troll cameist": "71-75", "troll combatant": "78-80", "troll cuirasser": "78-80",
        "troll engraver": "71-75", "troll gemologist": "71-75", "troll grenadier": "78-81",
        "troll ironworker": "71-75", "troll lapidarist": "71-75", "troll machinist": "78-81",
        "troll scrimer": "78-80", "troll smelter": "71-75", "troll stoneworker": "71-75",
        "troll targeteer": "78-82", "troll's automaton": SKIP, "volcanic bats": "69-71",
        "wamoura": "77-80", "wamouracampa": "73-75", "woodtroll elite guard": SKIP,
    },
}

# rule 9 — extend `lv`, never shrink. Each declared, not computed.
LV_UNION = {
    "copper borer": [81, 82],   # was [82,82]; page + nmlv say 81, adjacent so no gap invented
    "dextrose": [80, 90],       # was [80,82]; nmlv already read 80-90
    "black pudding": [66, 75],  # was [66,74]
    "reacton": [80, 90],        # was [81,83]; nmlv already read 80-90
    "talacca clot": [75, 77],   # was [75,75]
}


def zname(e):
    return e[0] if isinstance(e, list) else e


def main():
    d = json.load(open(PATH, encoding="utf-8"))
    mobs = d["mobs"]
    report = {}

    for ZONE, rows in ROWS.items():
        missing, added, changed, filled, kept, held = [], [], [], [], [], []
        for key, lvl in rows.items():
            r = mobs.get(key)
            if r is None:
                missing.append(key)
                continue
            if lvl is None:                     # explicit HOLD — twin already carries the zone
                held.append(key)
                continue
            zs = r.get("zones")
            if not isinstance(zs, list):
                zs = []
            idx = next((i for i, e in enumerate(zs) if zname(e) == ZONE), None)
            if idx is None:
                zs.append([ZONE] if lvl is SKIP else [ZONE, lvl])
                added.append((key, None if lvl is SKIP else lvl, len(zs) == 1))
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
        report[ZONE] = (rows, missing, added, changed, filled, kept, held)

    unions = []
    for key, new in LV_UNION.items():
        r = mobs[key]
        old = r.get("lv")
        if old != new:
            r["lv"] = new
            unions.append((key, old, new))

    bad = [k for mm in mobs.values() for k, v in mm.items() if v is None]
    assert not bad, f"null-valued keys written: {bad[:5]}"
    json.dump(d, open(PATH, "w", encoding="utf-8"),
              separators=(", ", ": "), ensure_ascii=False)

    for ZONE, (rows, missing, added, changed, filled, kept, held) in report.items():
        print("=" * 74)
        print(f"{ZONE} — {len(rows)} page records")
        print(f"  MISSING ({len(missing)}): {missing}")
        print(f"  ZONE ADDED ({len(added)})  [*] = record had NO zones at all before:")
        for k, v, first in added:
            print(f"     {'*' if first else ' '} {k:24s} {v}")
        print(f"  LEVEL FILLED ({len(filled)}):")
        for k, v in filled:
            print(f"       {k:24s} -> {v}")
        print(f"  LEVEL CHANGED ({len(changed)}):")
        for k, a, b in changed:
            print(f"       {k:24s} {a} -> {b}")
        print(f"  KEPT, page cell blank ({len(kept)}): {[k for k, _ in kept]}")
        print(f"  HELD — twin already holds the zone ({len(held)}): {held}")
        n_ok = len(rows) - len(added) - len(filled) - len(changed) - len(missing) - len(held)
        print(f"  Already right (incl. blank keeps): {n_ok} of {len(rows)}")

    print("=" * 74)
    print(f"RULE 9 `lv` UNIONS ({len(unions)}):")
    for k, a, b in unions:
        print(f"     {k:20s} {a} -> {b}")


if __name__ == "__main__":
    main()
