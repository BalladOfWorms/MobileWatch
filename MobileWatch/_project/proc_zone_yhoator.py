#!/usr/bin/env python3
"""
proc_zone_yhoator.py — refining-phase zone pass: Yhoator Jungle (rev 300).

Source: BG-wiki Yhoator Jungle page (Info box + Notorious Monsters + 3 Adversaries shots).
Zone string is `Yhoator Jungle` (exact in zones.json, no apostrophe/spacing gotcha).

Rule 15 is enforced by the writer: a page cell that publishes NO level is encoded as the SKIP
sentinel, which can ensure the zone exists but CANNOT touch a stored level.

Buckets reported separately: added / changed / filled / kept-because-blank / removed.

Author: BalladOfWorms
"""
import json, os, sys

ZONE = "Yhoator Jungle"
SKIP = object()

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
PATH = os.path.join(ASSETS, "mobs.json")

# name -> level string for this zone, or SKIP when the page publishes no level.
# Rule 2 merged spans noted inline.
ROWS = {
    # --- Notorious Monsters (11) ---
    "bisque-heeled sunberry": "58",
    "bright-handed kunberry": "55-56",
    "edacious opo-opo": "60",
    "woodland sage": "60-61",
    "acolnahuacatl": "67-68",
    "hoar-knuckled rimberry": "73",
    "powderer penny": SKIP,          # Lv cell blank -> rule 1, record keeps 49
    "kappa akuso": "63",
    "kappa biwa": "61",
    "kappa bonze": "60",
    "woodland mender": "122",
    # --- Adversaries (34) ---
    "goblin's bee": "28-30",
    "yhoator mandragora": "35-37",
    "goblin pathfinder": "35-39",
    "goblin shaman": "35-39",
    "goblin smithy": "35-39",
    "white lizard": "36-39",
    "yhoator wasp": "37-40",
    "tonberry's elemental": "38-40",
    "young opo-opo": "40-44",
    "goblin digger": "41-44",
    "goblin reaper": "41-45",
    "big jaw": "36-47",              # rule 2: Fished Up 36-38 U ground 43-47
    "worker crawler": "43-46",
    "goblin poacher": "45-49",
    "goblin robber": "45-49",
    "goblin trader": "45-49",
    "tonberry creeper": "45-49",
    "tonberry harasser": "45-49",
    "tonberry hexer": "45-49",
    "master coeurl": "47-50",
    "anemone": "51-54",
    "puroboros": "51-54",
    "goblin bouncer": "51-55",
    "goblin hunter": "51-55",
    "fire elemental": "53-55",
    "water elemental": "53-55",
    "tonberry chopper": "61-63",
    "tonberry jinxer": "61-63",
    "tonberry shadower": "61-63",
    "vepar": SKIP,                   # Lv cell reads `?-?` -> rule 10, no data
    "clipper": "30-33",
    "greater pugil": "30-33",
    "makara": "43-45",
    "razorjaw pugil": "50-53",
}

# Rev 286 wrote: "the Yhoator entry NOT removed — Yhoator's own page settles it in one line when
# it comes up." The page has come up; its 11-row NM table does not name Meww. Settled.
REMOVE = {"meww the turtlerider": "not on this page; its real home is Yuhtunga Jungle (rev 286, rule 133)"}


def zname(e):
    return e[0] if isinstance(e, list) else e


def main():
    d = json.load(open(PATH, encoding="utf-8"))
    mobs = d["mobs"]

    missing, added, changed, filled, kept, removed = [], [], [], [], [], []

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
            if lvl is SKIP:
                zs.append([ZONE])
                added.append((key, None))
            else:
                zs.append([ZONE, lvl])
                added.append((key, lvl))
            r["zones"] = zs
            continue

        ent = zs[idx]
        cur = ent[1] if isinstance(ent, list) and len(ent) > 1 else None
        if lvl is SKIP:
            kept.append((key, cur))          # rule 15: blank NEVER clears
            continue
        if cur is None:
            zs[idx] = [ZONE, lvl]
            filled.append((key, lvl))
        elif cur != lvl:
            zs[idx] = [ZONE, lvl]
            changed.append((key, cur, lvl))

    for key, why in REMOVE.items():
        r = mobs.get(key)
        if r is None:
            continue
        zs = r.get("zones") or []
        new = [e for e in zs if zname(e) != ZONE]
        if len(new) != len(zs):
            r["zones"] = new
            removed.append((key, why, new))

    # guard: never write JSON null into a mob record
    bad = [k for m in mobs.values() for k, v in m.items() if v is None]
    assert not bad, f"null-valued keys written: {bad[:5]}"

    json.dump(d, open(PATH, "w", encoding="utf-8"),
              separators=(", ", ": "), ensure_ascii=False)

    print(f"=== {ZONE} — {len(ROWS)} page records")
    print(f"MISSING ({len(missing)}): {missing}")
    print(f"\nZONE ADDED ({len(added)}):")
    for k, v in added:
        print(f"   {k:28s} {v}")
    print(f"\nLEVEL FILLED, zone held a null level ({len(filled)}):")
    for k, v in filled:
        print(f"   {k:28s} -> {v}")
    print(f"\nLEVEL CHANGED ({len(changed)}):")
    for k, a, b in changed:
        print(f"   {k:28s} {a} -> {b}")
    print(f"\nKEPT because the page cell is blank / no-data ({len(kept)}):")
    for k, v in kept:
        print(f"   {k:28s} stored {v}")
    print(f"\nZONE REMOVED ({len(removed)}):")
    for k, why, new in removed:
        print(f"   {k:28s} {why}\n{'':32s}now {new}")
    n_ok = len(ROWS) - len(added) - len(filled) - len(changed) - len(missing)
    print(f"\nAlready right (incl. blank-cell keeps): {n_ok} of {len(ROWS)}")


if __name__ == "__main__":
    main()
