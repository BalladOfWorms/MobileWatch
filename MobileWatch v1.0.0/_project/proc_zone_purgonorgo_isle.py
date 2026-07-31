#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Bibiki Bay - Purgonorgo Isle (rev 166). Engine = zonepass.py

Rule 57 clean — this and `Bibiki Bay` are both zones.json names (confirmed last rev).
Rule 65 applied: all 19 page names resolved against the file first try.

Sources: 3 shots — (1) info box, (2) Notorious Monsters, (3) Adversaries.

20 page rows -> 19 distinct records, and 15 were already exactly right. `Kraken`
appears twice — ground 37-40 and Fished-Up 44-46 -> merged 37-46 (rule 2), and the
record ALREADY stored the merge correctly.

The info box's `Requires` cell is an EXPANSION ICON with no text. There is precedent
for recording an expansion gate as a note (zeruhn_mines' Rise of the Zilart gate),
but the icon is not legible enough to name the expansion, so nothing was written —
rule 1 applied to an unreadable cell exactly like a blank one.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Bibiki Bay - Purgonorgo Isle"
SLUG = "bibiki_bay_purgonorgo_isle"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("lancet jagil",    "42-43", "NM  Fished Up"),
    ("peerifool",       "48",    "NM  Quest: One Good Deed?  (0 zones before)"),
    ("serra",           "50",    "NM  Lottery(Jagil)  (stored 49-50)"),
    ("rohemolipaud",    "55",    "NM  Quest: The Search for Goldmane  (0 zones before)"),
    ("shen",            "84-86", "NM  Forced (trade Shrimp Lantern to ???)"),
    ("shen's filtrate", SKIP,    "NM  Pet, assists Shen — Lv BLANK (0 zones before)"),
    ("shankha",         SKIP,    "NM  Timed 1.5-2 hr — Lv BLANK (keeps stored 52-53)"),
    ("bismarck",        SKIP,    "NM  Voidwatch — Lv BLANK"),
    # --- Adversaries -----------------------------------------------------
    ("ghost crab",         "30-34", "ADV Fished-Up 30-34"),
    ("grindylow",          "30-34", "ADV Fished-Up 30-34"),
    ("coralline uragnite", "32-35", "ADV 32-35"),
    ("ignis fatuus",       "35-37", "ADV 35-37"),
    ("jagil",              "35-38", "ADV 35-38"),
    ("greater pugil",      "35-39", "ADV Fished-Up 35-39"),
    ("coastal opo-opo",    "36-39", "ADV 36-39"),
    ("alraune",            "37-40", "ADV 37-40"),
    ("kraken",             "37-46", "ADV ground 37-40 + Fished-Up 44-46 (rule 2)"),
    ("toucan",             "38-40", "ADV 38-40"),
    ("viscous clot",       "38-40", "ADV 38-40"),
]

# rule 9 — nothing to extend. NOTE the side effect of the `serra` correction: it is a
# single-zone mob, so narrowing 49-50 -> 50 strands its lv min of 49 with no support.
# Rule 1 forbids shrinking `lv`, so it joins (kz) rather than being quietly rewritten —
# the nunyenunc shape from rev 159 exactly.
LV_EXTEND = {}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # The page publishes no Goblin Footprint row and zoneinfo's `footprint` is already
    # "" — consistent, not a gap. No footnote to record.
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
