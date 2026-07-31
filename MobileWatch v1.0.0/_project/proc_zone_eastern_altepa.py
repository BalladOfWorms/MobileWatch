#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Eastern Altepa Desert (rev 279). Engine = zonepass.py
MOBS ONLY.

RULE 2: `Lost Soul` is a WAR + BLM job pair, both 44-48, both 13 spawns -> one entry.

`centurio xii-i` stored **56-57** against the page's **56** — and the record's own
`nmlv` reads **56**. That is rule 107's test run the other way: there the file's range
CONTAINED the page's point value AND its `nmlv` backed the range, so the range stood;
here the `nmlv` backs the PAGE, so the page wins (rule 116 — a wider stored range is
a claim, not precision). `lv` [56,57] keeps an unsupported 57 as (kz) debt.

39 page records (9 NM + 30 Adversaries), 0 missing, bucket E empty.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Eastern Altepa Desert"
SLUG = "eastern_altepa_desert"

ROWS = [
    ("cactrot rapido",     "80-81", "NM  Timed 21-24 hr, WAR, Sabotender, roaming"),
    ("centurio xii-i",     "56",    "NM  Timed 21 hr, RNG, Antica — stored 56-57; its own nmlv says 56"),
    ("decurio i-iii",      "55",    "NM  Quest(A Craftsman's Work), PLD — zone stored level-less"),
    ("dune widow",         "45-47", "NM  Lottery(Giant Spider), WAR, Spider"),
    ("nandi",              "48-49", "NM  Timed, WAR, Dhalmel — 0 zones before"),
    ("sabotender corrido", "72",    "NM  Timed 2 hr, MNK, Sabotender — 0 zones before"),
    ("donnergugi",         SKIP,    "NM  Lottery(Sand Beetle), BLM, Beetle — Lv BLANK (keeps 60)"),
    ("tsuchigumo",         "42",    "NM  Quest(20 in Pirate Years), WAR, Spider"),
    ("cactrot veloz",      "122",   "NM  UNM 1,800 accolades, Sabotender"),
    ("antican auxiliarius","35-39", "ADV Antica WAR, 8 spawns"),
    ("antican centurio",   "50-52", "ADV Antica PLD, 3 spawns"),
    ("antican decurio",    "44-49", "ADV Antica PLD, 18 spawns"),
    ("antican faber",      "35-39", "ADV Antica BLM, 5 spawns"),
    ("antican funditor",   "35-39", "ADV Antica RNG, 7 spawns"),
    ("antican sagittarius","44-49", "ADV Antica RNG, 6 spawns — held only Western Altepa before"),
    ("antican speculator", "44-49", "ADV Antica RNG, 6 spawns"),
    ("antican veles",      "50-52", "ADV Antica WAR, 3 spawns"),
    ("bigclaw",            "48-51", "ADV Crab, Fished Up"),
    ("cutter",             "30-33", "ADV Crab, Fished Up"),
    ("desert dhalmel",     "39-44", "ADV Dhalmel, 35 spawns"),
    ("diatryma",           "47-50", "ADV Greater Bird, 7 spawns"),
    ("doom scorpion",      "44-47", "ADV Scorpion, 5 spawns"),
    ("earth elemental",    "47-49", "ADV Elemental, earth weather — 0 E. Altepa entry before"),
    ("fire elemental",     "47-49", "ADV Elemental, fire weather — 0 E. Altepa entry before"),
    ("flesh eater",        "37-42", "ADV Worm, nighttime 18:00-6:00, 28 spawns"),
    ("giant spider",       "30-34", "ADV Spider, 51 spawns (Dune Widow PH)"),
    ("goblin digger",      "45-49", "ADV Goblin, 1 spawn"),
    ("goblin poacher",     "45-49", "ADV Goblin RNG, 9 spawns"),
    ("goblin reaper",      "45-49", "ADV Goblin DRK, 6 spawns"),
    ("goblin robber",      "45-49", "ADV Goblin THF, 10 spawns"),
    ("goblin trader",      "45-49", "ADV Goblin BST, 6 spawns"),
    ("goblin's spider",    "38-40", "ADV Spider — pet, assists Goblin Trader, 6 spawns"),
    ("greater pugil",      "30-33", "ADV Pugil, Fished Up"),
    ("ironshell",          "36-39", "ADV Crab, Fished Up"),
    ("lesser manticore",   "47-49", "ADV Manticore, 10 spawns"),
    ("lost soul",          "44-48", "ADV Skeleton — WAR + BLM rows, both 44-48, 13 spawns each"),
    ("makara",             "42-45", "ADV Pugil, Fished Up"),
    ("sabotender",         "42-46", "ADV Sabotender, 16 spawns"),
    ("sand beetle",        "36-40", "ADV Beetle, 65 spawns (Donnergugi PH)"),
]

LV_EXTEND = {
    "antican sagittarius": (44, 49),   # [45,49] -> [44,49]
}

run(ZONE, SLUG, ROWS, lv_extend=LV_EXTEND, write=wants_write())
