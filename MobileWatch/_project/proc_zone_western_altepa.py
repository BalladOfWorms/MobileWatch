#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Western Altepa Desert (rev 281). Engine = zonepass.py
MOBS ONLY.

RULE 2: `Bigclaw` is TWO Fished-Up blocks, 45-47 and 50-52 -> **45-52**. zoneinfo
stores only the first block, so this is one of the few places the page beats zoneinfo.

39 page records (12 NM + 27 Adversaries), 0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Western Altepa Desert"
SLUG = "western_altepa_desert"

ROWS = [
    ("cactuar cantautor",  "56-59", "NM  Lottery(Cactuar), WAR — stored 56; its own nmlv already read 56-59"),
    ("celphie",            "47-48", "NM  Lottery(Desert Dhalmel), WAR"),
    ("king vinegarroon",   "80-85", "NM  Timed 21-24 hr during earth weather, WAR"),
    ("calchas",            SKIP,    "NM  Lottery(Tulwar Scorpion), WAR — Lv BLANK, 0 zones before"),
    ("dahu",               SKIP,    "NM  Timed 1 hr during earth weather, WAR, Manticore — Lv BLANK, 0 zones before"),
    ("picolaton",          SKIP,    "NM  Lottery(Phorusrhacos), WAR — Lv BLANK (keeps 60-61)"),
    ("eastern sphinx",     "62",    "NM  Mission(Bastok 6-1), WAR, Manticore — 0 zones before"),
    ("maharaja",           SKIP,    "NM  Quest(Inheritance), WAR, Tiger — Lv BLANK, 0 zones before"),
    ("sabotender enamorado","63",   "NM  Mission(San d'Oria 6-1), WAR — zone level-less; nmlv already 63"),
    ("western sphinx",     "62",    "NM  Mission(Bastok 6-1), WAR, Manticore — 0 zones before"),
    ("king uropygid",      "125",   "NM  UNM 2,100 accolades, Scorpion"),
    ("sabotender campeador", SKIP,  "NM  Voidwatch (Ashen stratum abyssite) — Lv BLANK (record has no lv at all)"),
    ("desert spider",      "40-44", "ADV Spider, 30 spawns"),
    ("antican essedarius", "41-45", "ADV Antica RNG, 8 spawns"),
    ("desert worm",        "43-47", "ADV Worm, nighttime, 24 spawns"),
    ("desert dhalmel",     "44-48", "ADV Dhalmel, 23 spawns (Celphie PH)"),
    ("antican eques",      "45-49", "ADV Antica PLD, 5 spawns"),
    ("antican retiarius",  "45-49", "ADV Antica BLM, 12 spawns"),
    ("desert beetle",      "47-51", "ADV Beetle, 100 spawns"),
    ("cactuar",            "48-53", "ADV Sabotender, 37 spawns (Cactuar Cantautor PH)"),
    ("lich",               "49-53", "ADV Skeleton BLM, undead, 6 spawns"),
    ("fallen knight",      "50-54", "ADV Skeleton WAR, undead, 9 spawns"),
    ("goblin digger",      "51-54", "ADV Goblin, 1 spawn"),
    ("goblin bouncer",     "51-55", "ADV Goblin WAR, 2 spawns"),
    ("goblin hunter",      "51-55", "ADV Goblin RNG, 2 spawns"),
    ("goblin welldigger",  "51-55", "ADV Goblin THF, 2 spawns"),
    ("goblin enchanter",   "52-55", "ADV Goblin RDM, 2 spawns — stored 51-55, the band of the three above it"),
    ("tulwar scorpion",    "53-56", "ADV Scorpion, 31 spawns (Calchas PH)"),
    ("desert manticore",   "53-57", "ADV Manticore, 16 spawns"),
    ("antican hoplomachus","54-58", "ADV Antica PLD, 29 spawns"),
    ("antican lanista",    "54-58", "ADV Antica BLM, 40 spawns"),
    ("antican secutor",    "54-58", "ADV Antica WAR, 25 spawns"),
    ("earth elemental",    "56-58", "ADV Elemental, earth weather — 0 W. Altepa entry before"),
    ("fire elemental",     "56-58", "ADV Elemental, fire weather — 0 W. Altepa entry before"),
    ("phorusrhacos",       "57-60", "ADV Greater Bird, 9 spawns (Picolaton PH)"),
    ("ironshell",          "40-42", "ADV Crab, Fished Up"),
    ("apsaras",            "40-42", "ADV Pugil, Fished Up"),
    ("bigclaw",            "45-52", "ADV Crab, Fished Up — RULE 2: 45-47 + 50-52 (zoneinfo has only the first)"),
    ("razorjaw pugil",     "56-58", "ADV Pugil, Fished Up"),
]

LV_EXTEND = {
    "cactuar cantautor":    (56, 59),   # [56,56] -> [56,59]
    "sabotender enamorado": (63, 63),   # [62,62] -> [62,63]
}

run(ZONE, SLUG, ROWS, lv_extend=LV_EXTEND, write=wants_write())
