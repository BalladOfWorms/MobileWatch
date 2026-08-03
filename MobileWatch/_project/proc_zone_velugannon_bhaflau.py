#!/usr/bin/env python3
"""
proc_zone_velugannon_bhaflau.py — refining-phase zone pass (rev 302):
Ve'Lugannon Palace + Bhaflau Thickets.

Zone strings per zones.json: `VeLugannon Palace` (apostrophe-free), `Bhaflau Thickets`.

Rule 15 enforced by the writer: SKIP = the page publishes no level, so the entry may be created
but a stored level can never be touched.
Rule 9 unions are declared explicitly (LV_UNION) rather than derived, so each one is a decision
on the record, not a side effect.

Author: BalladOfWorms
"""
import json, os, sys

SKIP = object()

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
MOBS = os.path.join(ASSETS, "mobs.json")
ZINFO = os.path.join(ASSETS, "zoneinfo.json")

VL = "VeLugannon Palace"
BT = "Bhaflau Thickets"

ROWS = {
    VL: {
        # --- Notorious Monsters (4) ---
        "brigandish blade": SKIP,        # Lv cell blank
        "steam cleaner": "82",
        "zipacna": "83-85",
        "uptala": SKIP,                  # Voidwatch, Lv cell blank
        # --- Adversaries (12) ---
        "detector": "72-74",
        "ornamental weapon": "74-76",
        "mystic weapon": "74-77",
        "dustbuster": "75-78",
        "caretaker": "76-79",
        "enkidu": "77-80",
        # SIX elements only — no light, no dark. All Timed 16 min, not weather-driven.
        "air elemental": "79-80",
        "earth elemental": "79-80",
        "fire elemental": "79-80",
        "ice elemental": "79-80",
        "thunder elemental": "79-80",
        "water elemental": "79-80",
    },
    BT: {
        # --- Notorious Monsters (12) ---
        "berried chigoe": "60",
        "chigoe's nit": SKIP,
        "dea": SKIP,                     # Lv cell reads `?` (rule 10)
        "emergent elm": "77-78",
        "harvestman": "72",
        "lividroot amooshah": "87",
        "mahishasura": "80",
        "nis puk": "77",
        "plague chigoe": "75",
        "dark rider": SKIP,
        "dark esquire": SKIP,
        "dark bugler": SKIP,
        # --- Adversaries (42) ---
        "aht urhgan attercop": "63-65",
        "air elemental": "75",
        "ameretat": "65-66",
        "azoth apsaras": "66-67",
        "chigoe": "71-73",
        "colibri": "71-73",
        "colorful treant": "75-76",
        "date eruca": "72-74",
        "fomor bard": "63-65",
        "fomor beastmaster": "63-65",
        "fomor paladin": "63-65",
        "fomor thief": "63-65",
        "fomor's bats": "58",
        "grand marid": "80",
        "haunt": "65-66",
        "incubus bats": "64-67",
        "kissing leech": "68-69",
        "lesser colibri": "63-65",
        "mamool ja blusterer": "81-83",
        "mamool ja infiltrator": "81-83",
        "mamool ja lurker": "81-83",
        "mamool ja mimer": "81-83",
        "mamool ja philosopher": "81-83",
        "mamool ja pikeman": "81-83",
        "mamool ja stabler": "81-83",
        "mamool ja's raptor": "77",
        "mamool ja's wyvern": "77",
        "marid": "78-79",
        "olden treant": "72-74",
        "red kisser": "67-69",
        "red osculator": "66-67",
        "red smoocher": "65-66",
        "sea puk": "77-78",
        "skoffin": "82-83",
        "treant sapling": "65-68",
        "troll sabreur": "71-73",
        "troll shieldbearer": "71-73",
        "troll surveillant": "71-73",
        "troll's automaton": "70-71",
        "wajaom tiger": "65-68",
        "locus colibri": "133-135",
        "locus wivre": "135-137",
    },
}

# Rule 9 — extend `lv` to the union where a level correction landed outside the stored band.
LV_UNION = {
    "caretaker": [76, 79],        # was [78,79]; zone corrected 78-79 -> 76-79, only zone
    "grand marid": [78, 80],      # was [78,79]; zone corrected 78-79 -> 80
}

ZONE_NOTE = ("velugannon_palace",
             "Travel through the palace depends on the coloured gates and Monoliths, the same "
             "system as The Shrine of Ru'Avitau: yellow monoliths open yellow gates and blue "
             "monoliths open blue gates.")


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
        r = mobs[key]
        old = r.get("lv")
        r["lv"] = new
        unions.append((key, old, new))

    bad = [k for m in mobs.values() for k, v in m.items() if v is None]
    assert not bad, f"null-valued keys written: {bad[:5]}"
    json.dump(d, open(MOBS, "w", encoding="utf-8"),
              separators=(", ", ": "), ensure_ascii=False)

    zi = json.load(open(ZINFO, encoding="utf-8"))
    zkey, note = ZONE_NOTE
    notes = zi[zkey].get("notes") or []
    written = note not in notes
    if written:
        notes.append(note)
        zi[zkey]["notes"] = notes
        json.dump(zi, open(ZINFO, "w", encoding="utf-8"),
                  separators=(", ", ": "), ensure_ascii=False)

    for ZONE, (rows, missing, added, changed, filled, kept) in report.items():
        print("=" * 76)
        print(f"{ZONE} — {len(rows)} page records")
        print(f"  MISSING ({len(missing)}): {missing}")
        print(f"  ZONE ADDED ({len(added)}):")
        for k, v in added:
            print(f"      {k:24s} {v}")
        print(f"  LEVEL FILLED, zone held a null level ({len(filled)}):")
        for k, v in filled:
            print(f"      {k:24s} -> {v}")
        print(f"  LEVEL CHANGED ({len(changed)}):")
        for k, a, b in changed:
            print(f"      {k:24s} {a} -> {b}")
        print(f"  KEPT, page cell blank / no-data ({len(kept)}):")
        for k, v in kept:
            print(f"      {k:24s} stored {v}")
        n_ok = len(rows) - len(added) - len(filled) - len(changed) - len(missing)
        print(f"  Already right (incl. keeps): {n_ok} of {len(rows)}")

    print("=" * 76)
    print(f"RULE-9 lv UNIONS ({len(unions)}):")
    for k, a, b in unions:
        print(f"      {k:24s} {a} -> {b}")
    print(f"zoneinfo note written to {zkey}: {written}")


if __name__ == "__main__":
    main()
