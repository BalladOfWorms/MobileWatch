#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Pashhow Marshlands (rev 181). Engine = zonepass.py
Mobs only (rule 84/87) — no zoneinfo_edit is passed.

RULE 98, THIRD CONSECUTIVE ZONE, AND THE DENSEST YET: `Pashhow Marshlands` is a
prefix of `Pashhow Marshlands [S]`, and **21 records on this page carry BOTH**.
A prefix/substring match would have corrupted 21 rows in one run. Exact-match
location (rule 8) is what makes the pass safe; the [S] entries are re-checked
after the write.
Rule 65 applied — all 49 names resolved first try.
Rule 91 — zoneinfo publishes 13 nms[] + 36 mobs[]; the shots read 13 + 37, which
is 13 + 36 after the Thread Leech pair. Reconciles exactly.

50 page rows -> 49 distinct records, 0 missing, 43 already exactly right.
ONE rule-2 merge: Thread Leech ground 19-22 + Fished-Up 20-23 -> 19-23 (zoneinfo
already publishes the merged span).
"""
from zonepass import run, wants_write, SKIP

ZONE = "Pashhow Marshlands"
SLUG = "pashhow_marshlands"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("bo'who warmonger",      "37",    "NM  Timed 21 hr, PLD"),
    ("bloodpool vorax",       "24-25", "NM  Lottery(Thread Leech)"),
    ("jolly green",           "27-28", "NM  Lottery(Goobbue), WAR"),
    ("toxic tamlyn",          SKIP,    "NM  Timed (no interval) — Lv BLANK (keeps 44-45)"),
    ("ni'zho bladebender",    SKIP,    "NM  Lottery(Veteran Quadav), WAR — Lv BLANK (0 zones)"),
    ("joyous green",          "122",   "NM  UNM 1,800 Unity Accolades"),
    ("murk-veined baneberry", SKIP,    "NM  Voidwatch — Lv BLANK (0 zones before)"),
    ("ground guzzler",        SKIP,    "NM  Voidwalker — Lv BLANK"),
    ("globster",              SKIP,    "NM  Voidwalker — Lv BLANK"),
    ("shoggoth",              SKIP,    "NM  Voidwalker — Lv BLANK"),
    ("lamprey lord",          SKIP,    "NM  Voidwalker — Lv BLANK"),
    ("blobdingnag",           SKIP,    "NM  Voidwalker — Lv BLANK"),
    ("yilbegan",              SKIP,    "NM  Voidwalker — Lv BLANK (keeps 90-92)"),
    # --- Adversaries ------------------------------------------------------
    ("bog bunny",             "13-16", "ADV 13-16"),
    ("night bats",            "13-16", "ADV 13-16 nighttime"),
    ("black bat",             "15-18", "ADV 15-18 nighttime"),
    ("water wasp",            "15-18", "ADV 15-18"),
    ("goblin ambusher",       "16-20", "ADV 16-20 RNG"),
    ("goblin butcher",        "16-20", "ADV 16-20 WAR"),
    ("goblin tinkerer",       "16-20", "ADV 16-20 DRK"),
    ("greater quadav",        "16-20", "ADV 16-20 DRK"),
    ("onyx quadav",           "16-20", "ADV 16-20 RDM"),
    ("veteran quadav",        "16-20", "ADV 16-20 PLD"),
    ("zombie",                "16-26", "ADV 16-26 BLM undead"),
    ("land pugil",            "17-20", "ADV 17-20"),
    ("snipper",               "17-20", "ADV 17-20"),
    ("gadfly",                "18-21", "ADV 18-21"),
    ("goblin digger",         "18-21", "ADV 18-21"),
    ("bog dog",               "18-25", "ADV 18-25 undead"),
    ("ghoul",                 "18-25", "ADV 18-25 WAR undead"),
    ("thread leech",          "19-23", "ADV rule 2: ground 19-22 + Fished-Up 20-23"),
    ("carnivorous crawler",   "20-23", "ADV 20-23"),
    ("brass quadav",          "20-26", "ADV 20-26 DRK"),
    ("copper quadav",         "20-26", "ADV 20-26 THF"),
    ("old quadav",            "20-26", "ADV 20-26 WAR"),
    ("goblin gambler",        "21-25", "ADV 21-25 BLM"),
    ("goblin leecher",        "21-25", "ADV 21-25 WHM"),
    ("goblin mugger",         "21-25", "ADV 21-25 THF"),
    ("marsh funguar",         "21-25", "ADV 21-25"),
    ("goobbue",               "22-25", "ADV 22-25"),
    ("fox fire",              "24-25", "ADV 24-25 fog weather"),
    ("malboro",               "25-28", "ADV 25-28"),
    ("bogy",                  "25-29", "ADV 25-29 undead  (stored 23-25 = its Buburimu/Meriphataud value)"),
    ("thunder elemental",     "27-29", "ADV 27-29 weather-spawned  (rule 79 — 11th zone)"),
    ("water elemental",       "27-29", "ADV 27-29 weather-spawned  (rule 79 — 11th zone)"),
    ("stag crab",             "13-15", "ADV Fished-Up 13-15"),
    ("swamp leech",           "13-15", "ADV Fished-Up 13-15"),
    ("swamp pugil",           "17-20", "ADV Fished-Up 17-20"),
    ("clipper",               "25-27", "ADV Fished-Up 25-27"),
]

# rule 9 — nothing to extend; both corrected ranges sit inside their record's band
# (bogy [23,73], thread leech [18,68]).
LV_EXTEND = {}

run(ZONE, SLUG, ROWS, LV_EXTEND, write=wants_write())
