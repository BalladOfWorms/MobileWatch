#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Attohwa Chasm (rev 268). Engine = zonepass.py
MOBS ONLY — no zoneinfo_edit, so the info box's `One Good Deed?` map source and the
Requires key-item row are read and not harvested.

RULE 2 merges (two page blocks -> one zone entry): `Earth Elemental` 40-42 + 75-76
-> 40-76 and `Air Elemental` 41-43 + 75-76 -> 41-76.

!! `Tracer Antlion` (38-40) and `Tracker Antlion` (70-73) are TWO DIFFERENT MOBS,
not one mob in two blocks. Confirmed three ways: zoneinfo lists both spellings
separately, mobs.json already holds both records at exactly those bands, and the
70-73 row's name cell measures 65px of ink against the 38-40 row's 61px — one
character wider. **A near-homograph pair in the same table is a merge trap.**

51 page records (11 NM + 40 Adversaries), 0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Attohwa Chasm"
SLUG = "attohwa_chasm"

ROWS = [
    # --- Notorious Monsters ------------------------------------------------
    ("alastor antlion",   "83",    "NM  Special (Feeler Antlion uses Sandblast), WAR"),
    ("ambusher antlion",  "75-77", "NM  Lottery(Trench Antlion), WAR — stored 68-70 while its own nmlv read 75-77"),
    ("citipati",          "67-70", "NM  Lottery(Corse), BLM"),
    ("feeler antlion",    "73-75", "NM  Forced (trade Antlion Trap to ???), WAR"),
    ("tiamat",            "95",    "NM  Timed 3-5 Earth days, Wyrm — zone stored level-less"),
    ("xolotl",            "80-81", "NM  Timed 21-24 hr during 20:00-4:00, BLM"),
    ("sargas",            "77-78", "NM  Timed 90-120 min, WAR, Scorpion"),
    ("sekhmet",           "52-53", "NM  Timed 60-90 min, RDM/WAR, Coeurl — 0 zones before"),
    ("lioumere",          SKIP,    "NM  Mission(Promathia 3-3), WAR — Lv BLANK (keeps 50-52)"),
    ("muut",              "125",   "NM  UNM 2,100 accolades, Corse"),
    ("fjalar",            SKIP,    "NM  Voidwatch (Hyacinth stratum abyssite), Dvergr — Lv BLANK (rule 42; record has no lv at all)"),
    # --- Adversaries --------------------------------------------------------
    ("goblin's gallinipper", "31-34", "ADV Fly — pet, assists Goblin Pathfinder"),
    ("flesh eater",       "34-37", "ADV Worm"),
    ("goblin furrier",    "35-38", "ADV Goblin RNG"),
    ("goblin shaman",     "35-38", "ADV Goblin BLM"),
    ("hecteyes",          "35-38", "ADV Hecteyes"),
    ("gallinipper",       "36-39", "ADV Fly"),
    ("goblin pathfinder", "36-39", "ADV Goblin BST — stored 35-38, the Furrier/Shaman band"),
    ("goblin smithy",     "36-39", "ADV Goblin WAR — stored 35-38, the Furrier/Shaman band"),
    ("attohwa coeurl",    "37-39", "ADV Coeurl"),
    ("goblin's ogrefly",  "38-39", "ADV Fly — pet, assists Goblin Trader"),
    ("tracer antlion",    "38-40", "ADV Antlion — stored 37-40 (NOT Tracker Antlion)"),
    ("chasm lizard",      "40-42", "ADV Hill Lizard"),
    ("earth elemental",   "40-76", "ADV Elemental, earth weather — RULE 2: 40-42 + 75-76; 0 Attohwa entry before"),
    ("will-o'-the-wykes", "40-43", "ADV Bomb, fog weather (usually 2:00-7:00), 6 spawns"),
    ("air elemental",     "41-76", "ADV Elemental, wind weather — RULE 2: 41-43 + 75-76; 0 Attohwa entry before"),
    ("burrow antlion",    "41-44", "ADV Antlion — stored 40-44"),
    ("doom scorpion",     "41-44", "ADV Scorpion"),
    ("goblin poacher",    "42-44", "ADV Goblin RNG"),
    ("goblin reaper",     "42-44", "ADV Goblin DRK"),
    ("goblin robber",     "42-44", "ADV Goblin THF"),
    ("goblin trader",     "43-44", "ADV Goblin BST"),
    ("ogrefly",           "44-47", "ADV Fly"),
    ("hunter antlion",    "45-46", "ADV Antlion — stored 45-47"),
    ("master coeurl",     "46-48", "ADV Coeurl"),
    ("bane lizard",       "47-49", "ADV Hill Lizard"),
    ("pit antlion",       "49-51", "ADV Antlion — stored 49-52"),
    ("tulwar scorpion",   "58-59", "ADV Scorpion"),
    ("lich",              "62-64", "ADV Skeleton BLM, undead 20:00-4:00"),
    ("mummy",             "62-64", "ADV Skeleton WAR, undead 20:00-4:00"),
    ("monarch ogrefly",   "65-67", "ADV Fly"),
    ("sand lizard",       "65-67", "ADV Hill Lizard"),
    ("corse",             "66-67", "ADV Corse, undead 20:00-4:00"),
    ("cutlass scorpion",  "67-69", "ADV Scorpion — stored 66-68"),
    ("trench antlion",    "70-71", "ADV Antlion (Ambusher Antlion PH) — stored 70-72"),
    ("tomb mage",         "70-73", "ADV Skeleton BLM"),
    ("tomb warrior",      "70-73", "ADV Skeleton WAR"),
    ("tracker antlion",   "70-73", "ADV Antlion — the OTHER antlion (see docstring)"),
    ("bifrons",           "74-76", "ADV Bomb"),
    ("arch corse",        "75-81", "ADV Corse, undead 20:00-4:00"),
    ("cave antlion",      "77-79", "ADV Antlion"),
]

# rule 9 — the only correction that lands OUTSIDE the record's stored lv
LV_EXTEND = {
    "ambusher antlion": (75, 77),   # [68,70] -> [68,77]
}

run(ZONE, SLUG, ROWS, lv_extend=LV_EXTEND, write=wants_write())
