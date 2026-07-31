#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Crawlers' Nest (rev 180). Engine = zonepass.py
Mobs only (rule 84/87) — no zoneinfo_edit is passed.

RULE 7 AGAIN: the page banner reads **Crawlers' Nest** (apostrophe); zones.json
stores **`Crawlers Nest`**. Second banner-vs-canon apostrophe case this session
after Ordelle's Caves.
RULE 98 AGAIN, ONE ZONE LATER: `Crawlers Nest` is a prefix of `Crawlers Nest [S]`,
and **`wespe` carries BOTH** (this zone 48-57, the [S] entry 63-65). Exact-match
location keeps them apart; the [S] band is re-checked after the write.
Rule 65 applied — all 39 names resolved first try.
Rule 91 — zoneinfo publishes 11 nms[] + 28 mobs[]; the shots read 13 + 29 rows,
which is 11 + 28 after the three rule-2 pairs below. Reconciles exactly.

42 page rows -> 39 distinct records, 0 missing.
THREE rule-2 merges, and zoneinfo records all three as two-block strings:
  Guardian Crawler  45  + 50     -> 45-50   ("45, 50")
  Drone Crawler     50  + 55     -> 50-55   ("50, 55")
  Wespe             48-50 + 55-57 -> 48-57  ("48-50, 55-57")
"""
from zonepass import run, wants_write, SKIP

ZONE = "Crawlers Nest"
SLUG = "crawlers_nest"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("guardian crawler", "45-50", "NM  rule 2: two Forced(30%) rows, 45 + 50"),
    ("drone crawler",    "50-55", "NM  rule 2: two Forced(50%) rows, 50 + 55"),
    ("mimic",            "55-60", "NM  Failed lockpicking attempt"),
    ("demonic tiphia",   "60",    "NM  Lottery"),
    ("matron crawler",   "64",    "NM  Forced(50%) Rolanberry 874"),
    ("queen crawler",    "64",    "NM  Forced(50%) Rolanberry 874"),
    ("awd goggie",       "68",    "NM  Forced(50%) Rolanberry 864"),
    ("aqrabuamelu",      "70-74", "NM  (stored 70 — the page publishes a band)"),
    ("dynast beetle",    SKIP,    "NM  Timed 1.5-2 hr, PLD — Lv BLANK (0 zones before)"),
    ("dreadbug",         "52",    "NM  Quest(A Boy's Dream), WAR — zone stored level-less"),
    ("mellonia",         SKIP,    "NM  Voidwatch — Lv BLANK (keeps 94-95)"),
    # --- Adversaries ------------------------------------------------------
    ("death jacket",     "40-42", "ADV 40-42"),
    ("worker crawler",   "40-44", "ADV 40-44"),
    ("maze lizard",      "41-43", "ADV 41-43"),
    ("caveberry",        "42-44", "ADV 42-44"),
    ("puroboros",        "45",    "ADV 45-45 -> 45, DRK, 2 spawns"),
    ("doom scorpion",    "45-47", "ADV 45-47"),
    ("killer mushroom",  "45-47", "ADV 45-47"),
    ("nest beetle",      "45-47", "ADV 45-47  (stored 44-47, below its own lv min)"),
    ("soldier crawler",  "47-49", "ADV 47-49"),
    ("soul stinger",     "48-50", "ADV 48-50"),
    ("wespe",            "48-57", "ADV rule 2: 48-50 + 55-57  (stored only the 2nd block)"),
    ("labyrinth lizard", "49-51", "ADV 49-51"),
    ("witch hazel",      "50-52", "ADV 50-52"),
    ("hornfly",          "50-53", "ADV 50-53"),
    ("exoray",           "51-54", "ADV 51-54"),
    ("blazer beetle",    "52-54", "ADV 52-54"),
    ("fire elemental",   "52-54", "ADV 52-54 weather-spawned  (rule 79 — 10th zone)"),
    ("water elemental",  "52-54", "ADV 52-54 weather-spawned  (rule 79 — 10th zone)"),
    ("mushussu",         "53-55", "ADV 53-55"),
    ("rumble crawler",   "53-55", "ADV 53-55  (stored 53-56)"),
    ("dragonfly",        "55-58", "ADV 55-58"),
    ("helm beetle",      "59-62", "ADV 59-62"),
    ("crawler hunter",   "60-62", "ADV 60-62"),
    ("knight crawler",   "60-63", "ADV 60-63"),
    ("king crawler",     "91-96", "ADV 91-96 high tier — zone stored level-less"),
    ("dancing jewel",    "93-96", "ADV 93-96 high tier  (0 zones before)"),
    ("olid funguar",     "93-96", "ADV 93-96 high tier  (0 zones before)"),
    ("vespo",            "93-96", "ADV 93-96 high tier"),
]

# rule 9 — four unions, three of them created by the rule-2 merges (the record had
# only one of the two published blocks) and one by aqrabuamelu's single-value store.
LV_EXTEND = {
    "guardian crawler": (45, 50),   # [45,45] -> [45,50]
    "drone crawler":    (50, 55),   # [50,50] -> [50,55]
    "aqrabuamelu":      (70, 74),   # [70,70] -> [70,74]
    "wespe":            (48, 57),   # [52,66] -> [48,66]
}

run(ZONE, SLUG, ROWS, LV_EXTEND, write=wants_write())
