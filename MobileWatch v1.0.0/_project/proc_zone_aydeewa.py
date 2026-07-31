#!/usr/bin/env python3
"""
proc_zone_aydeewa.py — refining-phase zone pass: Aydeewa Subterrane (rev 307).

RULE 188 RUN FIRST. The twin check fired once: the page's `Chigre` row belongs to
`chigre (monster)`, which ALREADY holds this zone at 82 — exactly the page value — so the bare
`chigre` record is deliberately absent from ROWS. Third distinct twin pair blocked before the
write (giant orobon r305/r306, antares r305, chigre here).

NEW Lv FORM: `Slime Eater` publishes **`87+`**, an open-ended lower bound. Stored verbatim, the
same treatment as `~60` (rule 11) and `<52` (rev 285). Add it to the rule-10 variant list.

Author: BalladOfWorms
"""
import json, os, re, sys
from collections import defaultdict

SKIP = object()
ZONE = "Aydeewa Subterrane"

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
MOBS = os.path.join(ASSETS, "mobs.json")

ROWS = {
    # --- Notorious Monsters (8; `chigre` handled by its twin, see docstring) ---
    "bluestreak gyugyuroon": "82",
    "crystal eater": SKIP,             # Lv cell reads `?` (rule 10)
    "lizardtrap": "74-75",             # zero zones
    "nosferatu": "80-90",
    "pandemonium warden": SKIP,        # Lv cell reads `?`
    "tumult curator": "145",
    "morta": SKIP,                     # Voidwatch, Lv blank
    # --- Adversaries (23) ---
    "air elemental": "70",             # page prints 70-70 -> collapses to a point
    "anautogenous slug": "65-66",
    "aydeewa crab": "68-70",
    "aydeewa diremite": "70-75",
    "cave mold": "66-69",
    "cave pugil": "68-69",
    "cave tiger": "73-76",
    "defoliator": "68-73",
    "deforester": "87-89",
    "fossorial flea": "66-68",
    "great ameretat": "73-74",
    "mold eater": "69-71",
    "mycohopper": "68-71",
    "mycoskulker": "89-98",            # zero zones
    "phlebotomic slug": "67-70",
    "puktrap": "67-69",
    "qiqirn archaeologist": "73-75",
    "qiqirn enterpriser": "68-70",
    "qiqirn lieuter": "68-70",
    "qiqirn mosstrooper": "73-75",
    "slime eater": "87+",              # zero zones; NEW Lv form, verbatim
    "slime mold": "67-70",
    "treant sapling": "66-69",
}

# Rule 9. SUSPENDED on `lizardtrap`: lv [72,72] vs the page's 74-75 are disjoint, so a union
# would invent 72-75. (kz) debt, same class as nunyunuwi / agas / locus imp / nergal.
LV_UNION = {
    "nosferatu": [80, 90],     # was [87,88]; its own nmlv already read 80-90
    "mycoskulker": [89, 98],   # was [89,90]
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

    byn = defaultdict(list)
    for k in mobs:
        byn[re.sub(r"[^a-z0-9]", "", k)].append(k)
    dupes = [g for g in byn.values() if len(g) > 1 and
             sum(any(zname(e) == ZONE for e in (mobs[k].get("zones") or [])) for k in g) > 1]
    assert not dupes, f"twin pair both holding {ZONE}: {dupes}"

    bad = [k for m in mobs.values() for k, v in m.items() if v is None]
    assert not bad, f"null-valued keys written: {bad[:5]}"
    json.dump(d, open(MOBS, "w", encoding="utf-8"),
              separators=(", ", ": "), ensure_ascii=False)

    print(f"=== {ZONE} — {len(ROWS)} rows written (page publishes 31; Chigre is its twin's)")
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
    print(f"\nKEPT, page cell blank / `?` ({len(kept)}):")
    for k, v in kept:
        print(f"    {k:24s} stored {v}")
    print(f"\nRULE-9 lv UNIONS ({len(unions)}):")
    for k, a, b in unions:
        print(f"    {k:24s} {a} -> {b}")
    print("\nTWIN-DUPLICATE GUARD: 0")


if __name__ == "__main__":
    main()
