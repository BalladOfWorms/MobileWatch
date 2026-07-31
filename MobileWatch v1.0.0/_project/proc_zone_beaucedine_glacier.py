#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Beaucedine Glacier (rev 281). Engine = zonepass.py
MOBS ONLY.

RULE 2: `Goblin's Tiger` is two pet blocks — 28-30 (assists Goblin Pathfinder) and
33-35 (assists Goblin Trader) -> **28-35**; `Ghast` is a WAR 35-38 + BLM 37-40 pair
-> 35-40 (already stored merged).

The NM table is half Voidwalker: SIX of the twelve rows are the Clear/Colorful/Purple/
Black abyssite ladder, all with blank Lv cells (rule 42).

39 page records (12 NM + 27 Adversaries), 0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Beaucedine Glacier"
SLUG = "beaucedine_glacier"

ROWS = [
    ("calcabrina",     SKIP,    "NM  Timed (no interval published), DRK, Doll — Lv BLANK (keeps 52-55)"),
    ("gargantua",      "47-48", "NM  Lottery(Stone Golem) every 20 min — zone stored level-less"),
    ("humbaba",        SKIP,    "NM  spawn cell reads 'TODO', WAR, Gigas — Lv BLANK (keeps 62)"),
    ("kirata",         "41",    "NM  Lottery(Tundra Tiger) every 20 min, WAR"),
    ("nue",            "41-42", "NM  Lottery(Tundra Tiger) every 1 hr, WAR"),
    ("largantua",      "125",   "NM  UNM 2,100 accolades, Golem"),
    ("gjenganger",     SKIP,    "NM  Voidwalker (Clear abyssite), Ghost — Lv BLANK"),
    ("gorehound",      SKIP,    "NM  Voidwalker (Clear abyssite), Hound — Lv BLANK"),
    ("erebus",         SKIP,    "NM  Voidwalker (Colorful abyssite), DRK, Skeleton — Lv BLANK"),
    ("feuerunke",      SKIP,    "NM  Voidwalker (Colorful abyssite), MNK/RDM, Doomed — Lv BLANK"),
    ("lord ruthven",   SKIP,    "NM  Voidwalker (Purple abyssite), Vampyr — Lv BLANK (keeps 85)"),
    ("yilbegan",       SKIP,    "NM  Voidwalker (Black abyssite) — Lv BLANK (keeps 90-92); 29th zone"),
    ("goblin's tiger", "28-35", "ADV Tiger — RULE 2: 28-30 (assists Goblin Pathfinder) + 33-35 (assists Goblin Trader)"),
    ("gigas's tiger",  "33-40", "ADV Tiger — pet, assists Rime Gigas"),
    ("tundra tiger",   "34-37", "ADV Tiger (Kirata + Nue PH)"),
    ("ghast",          "35-40", "ADV Skeleton — WAR 35-38 + BLM 37-40, already stored merged"),
    ("goblin furrier", "35-38", "ADV Goblin RNG"),
    ("goblin pathfinder","35-38","ADV Goblin BST"),
    ("goblin shaman",  "35-38", "ADV Goblin BLM"),
    ("goblin smithy",  "35-38", "ADV Goblin WAR"),
    ("living statue",  "37-39", "ADV Doll"),
    ("lugat",          "39-42", "ADV Ghost, undead"),
    ("bat eye",        "40-42", "ADV Ahriman"),
    ("stone golem",    "40-42", "ADV Golem — zone stored level-less (Gargantua PH)"),
    ("cold gigas",     "40-43", "ADV Gigas WAR"),
    ("goblin poacher", "40-43", "ADV Goblin RNG"),
    ("goblin reaper",  "40-43", "ADV Goblin DRK"),
    ("goblin robber",  "40-43", "ADV Goblin THF"),
    ("goblin trader",  "40-43", "ADV Goblin BST"),
    ("rime gigas",     "40-43", "ADV Gigas BST"),
    ("sleet gigas",    "40-43", "ADV Gigas RNG"),
    ("snow gigas",     "40-43", "ADV Gigas MNK"),
    ("dark elemental", "44-46", "ADV Elemental, dark weather — 0 Beaucedine entry before"),
    ("ice elemental",  "44-46", "ADV Elemental, ice weather — 0 Beaucedine entry before"),
    ("greater pugil",  "32-34", "ADV Pugil, Fished Up"),
    ("vepar",          "32-34", "ADV Pugil, Fished Up"),
    ("kraken",         "38-40", "ADV Sea Monk, Fished Up"),
    ("apsaras",        "41-42", "ADV Pugil, Fished Up"),
    ("morgawr",        "44-45", "ADV Sea Monk, Fished Up"),
]

LV_EXTEND = {
    "goblin's tiger": (28, 35),   # [33,35] -> [28,35]
}

run(ZONE, SLUG, ROWS, lv_extend=LV_EXTEND, write=wants_write())
