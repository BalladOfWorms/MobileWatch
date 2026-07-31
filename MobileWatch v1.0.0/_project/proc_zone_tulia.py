#!/usr/bin/env python3
"""
proc_zone_tulia.py — refining-phase zone pass: Ru'Aun Gardens + The Shrine of Ru'Avitau (rev 301).

Source: BG-wiki zone pages (Info boxes + NM tables + Adversaries tables).

ZONE STRINGS ARE APOSTROPHE-FREE per zones.json: `RuAun Gardens`, `The Shrine of RuAvitau`.
(Rule 7. Note the ITEM `Ru'Aun Coffer Key` KEEPS its apostrophe in ffxi_items.json — the
stripping is a zones.json convention, not a file-wide one.)

Rule 15 enforced by the writer: a page cell publishing NO level uses the SKIP sentinel, which can
create the zone entry but can never touch a stored level.

Also: one rule-41 ledger correction (`suzaku`) and one zoneinfo note.

Author: BalladOfWorms
"""
import json, os, sys

SKIP = object()

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
MOBS = os.path.join(ASSETS, "mobs.json")
ZINFO = os.path.join(ASSETS, "zoneinfo.json")

RUAUN = "RuAun Gardens"
SHRINE = "The Shrine of RuAvitau"

ROWS = {
    RUAUN: {
        # --- Notorious Monsters (6) ---
        "byakko": "88-90",
        "despot": "80-82",
        "genbu": "88-90",
        "seiryu": "88-90",
        "suzaku": "88-90",
        "aello": SKIP,               # Voidwatch, Lv cell blank -> rule 1 keeps stored 110
        # --- Adversaries (11) ---
        "flamingo": "72-74",
        "sprinkler": "73-76",
        "groundskeeper": "75-78",
        # the full eight-element set, all at one band
        "thunder elemental": "78-79",
        "earth elemental": "78-79",
        "water elemental": "78-79",
        "light elemental": "78-79",
        "dark elemental": "78-79",
        "ice elemental": "78-79",
        "air elemental": "78-79",
        "fire elemental": "78-79",
    },
    SHRINE: {
        # --- Notorious Monsters (6) ---
        "faust": "83-85",
        "kirin": None,               # None = HOLD: page point 92 vs stored 90-92, nmlv backs the range
        "mother globe": "83-85",
        "olla grande": "85",
        "ullikummi": "85-87",
        "qilin": SKIP,               # Voidwatch, Lv cell blank
        # --- Adversaries (15) --- the eight elements on a THREE-TIER ladder
        "earth elemental": "71-72",
        "air elemental": "71-72",
        "defender": "71-76",
        "thunder elemental": "72-73",
        "water elemental": "72-73",
        "dark elemental": "73-74",
        "fire elemental": "73-74",
        "ice elemental": "73-74",
        "light elemental": "73-74",
        "aura pot": "75-80",
        "aura gear": "76-81",
        "aura butler": "77-82",
        "decorative weapon": "79-81",
        "aura weapon": "80-82",
        "aura statue": "81-84",
    },
}

# Rule 41 / rule 129: ffxi_items.json writes the metal three ways (Orichalcum / Orichalc. / Ocl.).
# The ingot is `Ocl. Ingot`; three other records already store it that way.
DROP_FIX = {"suzaku": [("Orichalcum Ingot", "Ocl. Ingot")]}

# The page footnote (blue text UNDER the info box, not an info-box row) explains the roster above.
ZONE_NOTE = ("ruaun_gardens",
             "All elementals in the area are always present regardless of the overall zone "
             "weather conditions.")


def zname(e):
    return e[0] if isinstance(e, list) else e


def main():
    d = json.load(open(MOBS, encoding="utf-8"))
    mobs = d["mobs"]
    report = {}

    for ZONE, rows in ROWS.items():
        missing, added, changed, filled, kept, held = [], [], [], [], [], []
        for key, lvl in rows.items():
            r = mobs.get(key)
            if r is None:
                missing.append(key)
                continue
            zs = r.get("zones")
            if not isinstance(zs, list):
                zs = []
            idx = next((i for i, e in enumerate(zs) if zname(e) == ZONE), None)

            if lvl is None:                      # explicit HOLD, never write
                ent = zs[idx] if idx is not None else None
                held.append((key, ent))
                continue

            if idx is None:
                zs.append([ZONE] if lvl is SKIP else [ZONE, lvl])
                added.append((key, None if lvl is SKIP else lvl))
                r["zones"] = zs
                continue

            ent = zs[idx]
            cur = ent[1] if isinstance(ent, list) and len(ent) > 1 else None
            if lvl is SKIP:
                kept.append((key, cur))          # rule 15: blank NEVER clears
            elif cur is None:
                zs[idx] = [ZONE, lvl]
                filled.append((key, lvl))
            elif cur != lvl:
                zs[idx] = [ZONE, lvl]
                changed.append((key, cur, lvl))
        report[ZONE] = (rows, missing, added, changed, filled, kept, held)

    # rule 41 corrections
    fixed = []
    for key, pairs in DROP_FIX.items():
        r = mobs.get(key)
        if not r or not r.get("drops"):
            continue
        s = r["drops"]
        for old, new in pairs:
            if old in s:
                s = s.replace(old, new)
                fixed.append((key, old, new))
        r["drops"] = s

    bad = [k for m in mobs.values() for k, v in m.items() if v is None]
    assert not bad, f"null-valued keys written: {bad[:5]}"
    json.dump(d, open(MOBS, "w", encoding="utf-8"),
              separators=(", ", ": "), ensure_ascii=False)

    # zoneinfo note (field added rev 131; optJSONArray path, parse-safe)
    zi = json.load(open(ZINFO, encoding="utf-8"))
    zkey, note = ZONE_NOTE
    notes = zi[zkey].get("notes") or []
    if note not in notes:
        notes.append(note)
        zi[zkey]["notes"] = notes
        json.dump(zi, open(ZINFO, "w", encoding="utf-8"),
                  separators=(", ", ": "), ensure_ascii=False)
        note_written = True
    else:
        note_written = False

    for ZONE, (rows, missing, added, changed, filled, kept, held) in report.items():
        print("=" * 74)
        print(f"{ZONE} — {len(rows)} page records")
        print(f"  MISSING ({len(missing)}): {missing}")
        print(f"  ZONE ADDED ({len(added)}):")
        for k, v in added:
            print(f"      {k:22s} {v}")
        print(f"  LEVEL FILLED, zone held a null level ({len(filled)}):")
        for k, v in filled:
            print(f"      {k:22s} -> {v}")
        print(f"  LEVEL CHANGED ({len(changed)}):")
        for k, a, b in changed:
            print(f"      {k:22s} {a} -> {b}")
        print(f"  KEPT, page cell blank ({len(kept)}):")
        for k, v in kept:
            print(f"      {k:22s} stored {v}")
        print(f"  HELD against the page, deliberate ({len(held)}):")
        for k, e in held:
            print(f"      {k:22s} {e}")
        n_ok = len(rows) - len(added) - len(filled) - len(changed) - len(missing)
        print(f"  Already right (incl. keeps/holds): {n_ok} of {len(rows)}")

    print("=" * 74)
    print(f"DROPS FIXED ({len(fixed)}):")
    for k, a, b in fixed:
        print(f"      {k:22s} {a!r} -> {b!r}")
    print(f"zoneinfo note written to {zkey}: {note_written}")


if __name__ == "__main__":
    main()
