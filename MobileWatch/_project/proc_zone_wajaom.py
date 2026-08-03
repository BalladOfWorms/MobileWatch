#!/usr/bin/env python3
"""
proc_zone_wajaom.py — refining-phase zone pass: Wajaom Woodlands (rev 309).

RULE 188 RUN FIRST, and the twin check fired TWICE — both page rows belong to the suffixed record:
  * `Hydra (Notorious Monster)` -> `hydra (nm)`, already holding the zone at 80 (the page value).
  * `Chigoe`                    -> `chigoe (monster)`, already holding 71-73 (the page value).
The bare `hydra` and `chigoe` records are deliberately absent from ROWS. **`chigoe` is the exact
pair I got wrong at rev 302 and had to revert at rev 304 — the guard now catches it automatically.**

Author: BalladOfWorms
"""
import json, os, re, sys
from collections import defaultdict

SKIP = object()
ZONE = "Wajaom Woodlands"

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
MOBS = os.path.join(ASSETS, "mobs.json")

ROWS = {
    # --- Notorious Monsters (17; `hydra` handled by its twin) ---
    "chelicerata": "78",                # zero zones, fam=None
    "gharial": SKIP,                    # zero zones; Lv cell reads `?` (rule 10)
    "gotoh zha the redolent": "80-90",
    "jaded jody": "80",
    "iriz ima": "87-88",
    "tinnin": "85-90",
    "vulpangue": "75-80",               # zero zones
    "zoraal ja's pkuucha": "73",
    "percipient zoraal ja": SKIP,
    "dark rider": SKIP,
    "dark esquire": SKIP,
    "dark bugler": SKIP,
    "berried chigoe": "60",
    "chigoe's nit": SKIP,
    "kubool ja's mhuufya": "125",
    "thu'ban": "135",
    # --- Adversaries (37; `chigoe` handled by its twin) ---
    "aht urhgan attercop": "63-65",
    "air elemental": "75",
    "ameretat": "65-66",
    "azoth apsaras": "66-67",
    "carmine eruca": "70",              # page prints 70-70
    "colorful treant": "74-76",
    "defoliate treant": "75-76",
    "fomor bard": "63-65",
    "fomor beastmaster": "63-65",
    "fomor paladin": "63-65",
    "fomor thief": "63-65",
    "fomor's bats": "58",               # page prints 58-58
    "grand marid": "80",                # page prints 80-80
    "great ameretat": "73-74",
    "haunt": "65-66",
    "kissing leech": "68-69",
    "lesser colibri": "63-65",
    "mamool ja bounder": "72-73",
    "mamool ja mimicker": "72-73",
    "mamool ja savant": "72-73",
    "mamool ja sophist": "72-73",
    "mamool ja zenist": "72-73",
    "marid": "78-79",
    "puk": "68-70",
    "red kisser": "67-69",
    "red osculator": "66-67",
    "red smoocher": "65-67",
    "soldier pephredo": "64-65",
    "treant sapling": "66-68",
    "wajaom tiger": "65-68",
    "woodland runner": "71-72",
    "woodtroll dark knight": "72-73",
    "woodtroll monk": "72-73",
    "woodtroll ranger": "72-73",
    "woodtroll warrior": "72-73",
    "worker pephredo": "62-63",
}

# Rule 9. SUSPENDED on `defoliate treant`: its lv [71,73] and the page's 75-76 are DISJOINT, so a
# union would invent 74. (kz) debt — and note BOTH its lv and its zone entry read 71-73, so the
# record was internally consistent and internally wrong.
LV_UNION = {
    "gotoh zha the redolent": [80, 90],   # was [83,85]; its own nmlv already read 80-90
    "vulpangue": [75, 80],                # was [78,80]; its own nmlv already read 75-80
    "red smoocher": [65, 67],             # was [65,66]
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

    # no twin pair may both hold this zone (normalized key AND suffix variants)
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

    print(f"=== {ZONE} — {len(ROWS)} rows written (page publishes 54; Hydra + Chigoe are their twins')")
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
    print(f"\nRULE-9 lv UNIONS ({len(unions)}):")
    for k, a, b in unions:
        print(f"    {k:26s} {a} -> {b}")
    print("\nTWIN-DUPLICATE GUARD: 0")


if __name__ == "__main__":
    main()
