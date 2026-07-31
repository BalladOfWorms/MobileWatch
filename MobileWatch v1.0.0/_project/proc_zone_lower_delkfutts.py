#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Lower Delkfutt's Tower (rev 274). Engine = zonepass.py
MOBS ONLY. Zone string is `Lower Delkfutts Tower` per zones.json.

30 page records (9 NM + 21 Adversaries), 0 missing, bucket E empty.

`gigas's bats` stored **25-27 here — the band of `Seeker Bats`, the row above it on
the same page** (rule-135 shape). Its Middle and Upper Delkfutt entries are both
27-29, which is what the page gives for Lower too.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Lower Delkfutts Tower"
SLUG = "lower_delkfutts_tower"

ROWS = [
    ("epialtes",        "28-32", "NM  Lottery(Gigas), WAR, 1st Floor"),
    ("eurymedon",       "30-34", "NM  Lottery(Giant Sentry), BST, 3rd Floor"),
    ("hippolytos",      "28-32", "NM  Lottery(Gigas), MNK, 2nd Floor"),
    ("tyrant",          SKIP,    "NM  Timed (no interval published), PLD, Doll — Lv BLANK, 0 zones before"),
    ("disaster idol",   "75",    "NM  Mission(Promathia 5-3 Three Paths), BLM/RDM/WHM — 0 zones before"),
    ("fomorian spear",  SKIP,    "NM  Quest(Hyper Active), WAR — Lv BLANK (keeps 32)"),
    ("orna",            SKIP,    "NM  Quest(Hyper Active), RDM — Lv BLANK"),
    ("illusory pot",    SKIP,    "NM  Quest(Chameleon Capers), RDM — Lv BLANK (keeps 45-50)"),
    ("akvan",           SKIP,    "NM  Voidwatch (White stratum abyssite III), Ahriman — Lv BLANK"),
    ("gigas's bat",     "21-23", "ADV Bat — pet, assists Giant Sentry"),
    ("seeker bats",     "25-27", "ADV Flock Bat"),
    ("gigas's bats",    "27-29", "ADV Flock Bat — pet, assists Gigas Butcher; stored 25-27 = Seeker Bats' band"),
    ("ancient bat",     "27-29", "ADV Bat"),
    ("goblin leecher",  "27-30", "ADV Goblin WHM"),
    ("goblin gambler",  "27-30", "ADV Goblin BLM"),
    ("goblin mugger",   "27-30", "ADV Goblin THF"),
    ("magic pot",       "28-29", "ADV Magic Pot"),
    ("giant gatekeeper","28-30", "ADV Gigas WAR"),
    ("giant guard",     "28-30", "ADV Gigas MNK"),
    ("giant lobber",    "28-30", "ADV Gigas RNG"),
    ("chaos idol",      "28-30", "ADV Doll"),
    ("giant sentry",    "28-30", "ADV Gigas BST (Eurymedon PH)"),
    ("bogy",            "30-32", "ADV Ghost, undead 20:00-4:00"),
    ("gigas punisher",  "34-35", "ADV Gigas MNK, Delkfutt Chest Key"),
    ("gigas hallwatcher","34-35","ADV Gigas WAR, Delkfutt Chest Key"),
    ("gigas sculptor",  "34-35", "ADV Gigas RNG, Delkfutt Chest Key"),
    ("gigas butcher",   "34-35", "ADV Gigas BST, Delkfutt Chest Key"),
    ("magic urn",       "34-35", "ADV Magic Pot, Delkfutt Chest Key"),
    ("thunder elemental","35-36","ADV Elemental, thunder weather, Chest Key — 0 entry here before"),
    ("light elemental", "35-36", "ADV Elemental, light weather, Chest Key — 0 entry here before"),
]

run(ZONE, SLUG, ROWS, write=wants_write())
