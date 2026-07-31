#!/usr/bin/env python3
"""
proc_zone_alzadaal_rala.py — refining-phase zone pass (rev 310):
Alzadaal Undersea Ruins + Rala Waterways.

RULE 188 RUN FIRST on both zones. The twin check found nothing; **bucket E found the interesting
pair**: `apex archaic cog` (singular) and `apex archaic cogs` (plural) each hold this zone, at
143-145 and 146-147. The page publishes TWO rows and BOTH name cells are the same string
(pixel-measured, 82px vs 81px — sub-character, where rule 105's Tracer/Tracker differed by a whole
letter blob), at 142-145 and 146-147. zoneinfo merged them to a single `142-147`.

NOT MERGED. The two records carry DIFFERENT accuracy figures in `notes` (1,591 vs 1,668), so they
were built from two genuinely distinct source rows, and `archaic gear`/`archaic gears` shows the
singular/plural split is a real distinction in this family (rule 105's warning). Instead each
record is aligned to the page row it obviously belongs to: the singular takes **142-145**.

`armed gears` sits in the NM table and carries `nmlv` 88 with **no `nm` flag** — one of the audit's
40 "nmlv but no nm" rows. Set page-backed, the rev-264 precedent.

Rala Waterways publishes NO Notorious Monsters table and zoneinfo agrees (0 NMs) — the absence is
real, not a capture gap.

Author: BalladOfWorms
"""
import json, os, re, sys
from collections import defaultdict

SKIP = object()

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
MOBS = os.path.join(ASSETS, "mobs.json")
ZINFO = os.path.join(ASSETS, "zoneinfo.json")

AZ = "Alzadaal Undersea Ruins"
RW = "Rala Waterways"

ROWS = {
    AZ: {
        # --- Notorious Monsters (9) ---
        "armed gears": "88",
        "boompadu": "82-83",
        "cookieduster lipiroon": SKIP,      # Lv blank -> keeps stored 80-82
        "cheese hoarder gigiroon": SKIP,
        "ob": SKIP,
        "oupire": "88",
        "vidmapire": "128",
        "wulgaru": "88",
        "nepionic soulflayer": SKIP,
        # --- Adversaries (3 distinct; Apex Archaic Cogs is published on two rows) ---
        "qiqirn goldsmith": "76-78",
        "qiqirn poulterer": "76-78",
        "apex archaic cog": "142-145",      # the page's FIRST Apex row
        "apex archaic cogs": "146-147",     # the page's SECOND Apex row
    },
    RW: {
        # --- Adversaries (18). THIRTEEN of the 18 Lv cells are blank. ---
        "baleful tarichuk": SKIP,
        "barnacle crab": "102-103",
        "chalybeous slime": "101-103",
        "depthswalker crab": "101-102",
        "duskbringer bat": SKIP,
        "duskjaw obdella": SKIP,
        "flavescent slime": "101-103",
        "new moon bats": SKIP,
        "pewter diremite": SKIP,
        "plantpassage slug": SKIP,
        "rustwater toad": SKIP,
        "sawtooth pugil": "100",            # zero zones AND no lv
        "skittering spider": "100-102",
        "spoutdrenched toad": SKIP,
        "stillwater funguar": SKIP,
        "unrelenting eft": SKIP,
        "waterway pugil": SKIP,
        "weatherworn leech": SKIP,
    },
}

# Rule 9. SUSPENDED on `oupire`: lv [85,85] vs the page's 88 are disjoint points, so a union would
# invent 85-88. (kz) debt, the nunyunuwi / locus imp / lizardtrap class.
LV_UNION = {
    "boompadu": [82, 83],          # was [82,82]; its own nmlv already read 82-83
    "apex archaic cog": [142, 145],  # was [143,145]
}

NM_FLAG = ["armed gears"]          # page-backed: it is in the NM table and already has nmlv 88

ZONE_NOTE = ("rala_waterways",
             "The zone has various Sluice Gates that are accessible or locked depending on the "
             "day and time.")


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
        old = mobs[key].get("lv")
        mobs[key]["lv"] = new
        unions.append((key, old, new))

    flagged = []
    for key in NM_FLAG:
        if not mobs[key].get("nm"):
            mobs[key]["nm"] = True
            flagged.append(key)

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
        print(f"  KEPT, page cell blank ({len(kept)}):")
        for k, v in kept:
            print(f"      {k:26s} stored {v}")
    print("=" * 74)
    print(f"RULE-9 lv UNIONS ({len(unions)}):")
    for k, a, b in unions:
        print(f"      {k:26s} {a} -> {b}")
    print(f"NM FLAGS SET ({len(flagged)}): {flagged}")
    print(f"zoneinfo note written to {zkey}: {written}")


if __name__ == "__main__":
    main()
