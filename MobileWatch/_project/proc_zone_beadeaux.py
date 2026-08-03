#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Beadeaux (rev 179). Engine = zonepass.py
Mobs only (rule 84/87) — no zoneinfo_edit is passed.

Rule 57: `Beadeaux` AND `Beadeaux [S]` are both zones.json names — two genuinely
different zones (the Bibiki/Purgonorgo shape), and `magnes quadav` carries BOTH,
so the [S] entry (77-79) must not be touched by this pass.
Rule 65 applied — all 39 names resolved against the FILE first try.
Rule 91 — zoneinfo publishes 10 nms[] + 29 mobs[]; the shots read 10 + 29. The
three seams (Zircon / Spinel / Ancient Quadav) are all overlaps, not gaps.

39 page rows -> 39 distinct records, 0 missing, 32 already exactly right. No job
pairs and no Fished-Up block on this page — one row per record throughout.

THE QUADAV LADDER: Bronze 32-36 / Silver 33-37 / Zircon 34-38 / Garnet 35-39 step
by exactly +1. Three of the four were stored right; `garnet quadav` alone read
32-39 — its min pinned to the BOTTOM of the ladder rather than its own rung.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Beadeaux"
SLUG = "beadeaux"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("bi'gho headtaker",    "25",    "NM  Lottery(Brass Quadav), DRK"),
    ("da'dha hundredmask",  "30",    "NM  Lottery(Copper Quadav), THF"),
    ("ge'dha evileye",      "30",    "NM  Lottery(Old Quadav), WHM"),
    ("zo'khu blackcloud",   "36-38", "NM  Lottery(Zircon Quadav), BLM"),
    ("go'bhu gascon",       "41-42", "NM  Timed 20 min, WAR"),
    ("de'vyu headhunter",   "45",    "NM  Timed 15 min, WAR"),
    ("ga'bhu unvanquished", "47-48", "NM  Lottery(Emerald Quadav), RDM"),
    ("mimic",               "55-60", "NM  Failed lockpicking attempt  (0 zones before)"),
    ("magnes quadav",       "43-45", "NM  Quest(For the Birds), BLM — zone stored level-less"),
    ("nickel quadav",       "43-45", "NM  Quest(For the Birds), PLD — zone stored level-less"),
    # --- Adversaries ------------------------------------------------------
    ("land pugil",          "20-23", "ADV 20-23  (20 spawns)"),
    ("caterpillar",         "22-25", "ADV 22-25"),
    ("old quadav",          "22-26", "ADV 22-26 WAR"),
    ("copper quadav",       "22-27", "ADV 22-27 THF"),
    ("brass quadav",        "24-28", "ADV 24-28 DRK"),
    ("charging sheep",      "28-30", "ADV 28-30"),
    ("ooze",                "28-30", "ADV 28-30"),
    ("bronze quadav",       "32-36", "ADV 32-36 PLD  (ladder rung 1)"),
    ("silver quadav",       "33-37", "ADV 33-37 THF  (ladder rung 2)"),
    ("zircon quadav",       "34-38", "ADV 34-38 BLM  (ladder rung 3)"),
    ("larva",               "35-38", "ADV 35-38"),
    ("garnet quadav",       "35-39", "ADV 35-39 WHM  (ladder rung 4 — stored 32-39)"),
    ("big jaw",             "37-39", "ADV 37-39 WAR"),
    ("gloop",               "38-40", "ADV 38-40 WAR"),
    ("broo",                "39-41", "ADV 39-41 WAR"),
    ("elder quadav",        "42-46", "ADV 42-46 WAR"),
    ("iron quadav",         "43-47", "ADV 43-47 PLD"),
    ("spinel quadav",       "44-48", "ADV 44-48 BLM"),
    ("emerald quadav",      "45-49", "ADV 45-49 RDM"),
    ("thunder elemental",   "47-49", "ADV 47-49 weather-spawned  (rule 79 — 9th zone)"),
    ("water elemental",     "47-49", "ADV 47-49 weather-spawned  (rule 79 — 9th zone)"),
    ("steel quadav",        "52-56", "ADV 52-56 PLD"),
    ("mythril quadav",      "53-57", "ADV 53-57 DRK"),
    ("gold quadav",         "54-58", "ADV 54-58 THF"),
    ("topaz quadav",        "55-59", "ADV 55-59 WHM"),
    ("ancient quadav",      "62-66", "ADV 62-66 WAR"),
    ("darksteel quadav",    "63-67", "ADV 63-67 PLD"),
    ("platinum quadav",     "64-68", "ADV 64-68 THF"),
    ("sapphire quadav",     "65-68", "ADV 65-68 BLM  (stored 65-69)"),
]

# rule 9 — `mimic` had ZERO zones and lv [56,79]; the page's 55 sits one below it.
LV_EXTEND = {
    "mimic": (55, 60),            # [56,79] -> [55,79]
}

run(ZONE, SLUG, ROWS, LV_EXTEND, write=wants_write())
