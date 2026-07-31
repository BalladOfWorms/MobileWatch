#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Middle Delkfutt's Tower (rev 275). Engine = zonepass.py
MOBS ONLY. Zone string is `Middle Delkfutts Tower` per zones.json.

35 page records (8 NM + 27 Adversaries), 0 missing, bucket E empty.

!! `gigas's bats` — THE REV-274 DIAGNOSIS WAS WRONG AND THIS PAGE CORRECTS IT.
Lower Delkfutt read 27-29 and the record held 25-27; I called that a copy of Seeker
Bats' band. It was not: **the Lower and Middle entries were TRANSPOSED.** Middle's
page says 25-27 and the record holds 27-29 — the exact mirror. With both fixed,
Lower/Upper = 27-29 and Middle = 25-27, and `lv` [25,29] becomes exactly supported at
both ends for the first time.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Middle Delkfutts Tower"
SLUG = "middle_delkfutts_tower"

ROWS = [
    ("eurytos",          "32",    "NM  Lottery(Gigas), RNG, 4th Floor"),
    ("ogygos",           SKIP,    "NM  Lottery(Gigas Wallwatcher), WAR, 9th Floor — Lv BLANK"),
    ("ophion",           SKIP,    "NM  Lottery(Gigas Kettlemaster), BST, 7th Floor — Lv BLANK"),
    ("polybotes",        SKIP,    "NM  Lottery(Gigas), WAR, 5th Floor — Lv BLANK"),
    ("rhoikos",          "34",    "NM  Lottery(Gigas Quarrier), RNG, 8th Floor"),
    ("rhoitos",          "33-38", "NM  Lottery(Gigas), MNK, 6th Floor"),
    ("gerwitz's scythe", "60",    "NM  Quest(Blade of Evil), RDM, Evil Weapon"),
    ("scythe victim",    "58",    "NM  Quest(Blade of Evil), BLM/WAR, Skeleton — zone stored level-less"),
    ("gigas's bat",      "23-25", "ADV Bat — pet, assists Giant Sentry"),
    ("goblin's bat",     "23-25", "ADV Bat — pet, assists Goblin Pathfinder"),
    ("mold bats",        "25-27", "ADV Flock Bat"),
    ("gigas's bats",     "25-27", "ADV Flock Bat — stored 27-29; TRANSPOSED with its Lower Delkfutt entry"),
    ("tower bats",       "27-29", "ADV Flock Bat"),
    ("stirge",           "27-29", "ADV Bat"),
    ("magic pot",        "28-29", "ADV Magic Pot"),
    ("big bat",          "29-31", "ADV Bat"),
    ("giant gatekeeper", "30-32", "ADV Gigas WAR"),
    ("giant sentry",     "30-32", "ADV Gigas BST"),
    ("giant guard",      "30-32", "ADV Gigas MNK"),
    ("giant lobber",     "30-32", "ADV Gigas RNG"),
    ("goblin smithy",    "30-34", "ADV Goblin WAR"),
    ("goblin shaman",    "30-34", "ADV Goblin BLM"),
    ("goblin furrier",   "30-34", "ADV Goblin RNG"),
    ("goblin pathfinder","30-34", "ADV Goblin BST"),
    ("panzer doll",      "31-32", "ADV Doll"),
    ("magic jar",        "31-32", "ADV Magic Pot — stored 31-33, one past its own lv max"),
    ("banshee",          "32-33", "ADV Ghost"),
    ("gigas quarrier",   "32-34", "ADV Gigas RNG (Rhoikos PH)"),
    ("gigas kettlemaster","32-34","ADV Gigas BST, Delkfutt Chest Key (Ophion PH)"),
    ("gigas wallwatcher","32-34", "ADV Gigas WAR, Delkfutt Chest Key (Ogygos PH)"),
    ("gigas jailer",     "32-34", "ADV Gigas MNK"),
    ("jagd doll",        "33-34", "ADV Doll"),
    ("evil spirit",      "34-35", "ADV Ghost, Delkfutt Chest Key"),
    ("light elemental",  "35-36", "ADV Elemental, light weather, Chest Key — 0 entry here before"),
    ("thunder elemental","35-36", "ADV Elemental, thunder weather, Chest Key — 0 entry here before"),
]

run(ZONE, SLUG, ROWS, write=wants_write())
