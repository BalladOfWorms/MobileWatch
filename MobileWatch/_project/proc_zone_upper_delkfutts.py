#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Upper Delkfutt's Tower (rev 277). Engine = zonepass.py
MOBS ONLY. Zone string `Upper Delkfutts Tower`.

!! THE `Ixtab` ROW TARGETS `ixtab (monster)`, NOT THE BARE `ixtab`. The two records
are EXACT DUPLICATES — same lv [71,71], same nm, same nmlv "71", same
spawn "Lottery (Phasma)" — except the (monster) one has **fam Ghost and the zone**
and the bare one has neither. That is the cleanest example yet of the rev-269 class-A
pairs, and it is why the bare stub was NOT given the zone: two Ixtabs in the zone view
would be a regression. **Its fam is also deliberately left blank** — the standing
family rule fills a GAP, and the family is not missing here, it is on the twin.

25 page records (7 NM + 18 Adversaries), 0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Upper Delkfutts Tower"
SLUG = "upper_delkfutts_tower"

ROWS = [
    ("alkyoneus",        "75",    "NM  Forced (trade Moldy Buckler to ???), WAR, 12th Floor"),
    ("autarch",          "83-85", "NM  Timed 30 min - 3 hr, THF, Doll"),
    ("enkelados",        "55-58", "NM  Lottery(Gigas Bonecutter), BST, 10th Floor"),
    ("ixtab (monster)",  "71",    "NM  Lottery(Phasma), WAR, Ghost — zone stored level-less; the bare `ixtab` is its duplicate stub"),
    ("mimas",            "36",    "NM  Timed 15 min, MNK, 10th Floor"),
    ("pallas",           SKIP,    "NM  Forced (trade Hoary Battle Horn to ???), BST, 11th Floor — Lv BLANK (keeps 72)"),
    ("porphyrion",       "36",    "NM  Timed 5-10 min, RNG, 10th Floor — drops the Delkfutt Key"),
    ("gigas's bats",     "27-29", "ADV Flock Bat — pet, assists Gigas Bonecutter"),
    ("gigas bonecutter", "34-35", "ADV Gigas BST, Delkfutt Chest Key (Enkelados PH)"),
    ("gigas torturer",   "34-35", "ADV Gigas MNK, Delkfutt Chest Key"),
    ("gigas stonemason", "34-35", "ADV Gigas RNG, Delkfutt Chest Key"),
    ("magic urn",        "34-35", "ADV Magic Pot, Delkfutt Chest Key"),
    ("gigas spirekeeper","34-35", "ADV Gigas WAR, Delkfutt Chest Key"),
    ("light elemental",  "35-36", "ADV Elemental, light weather, Chest Key — 0 entry here before"),
    ("thunder elemental","35-36", "ADV Elemental, thunder weather, Chest Key — 0 entry here before"),
    ("gigas's bat",      "53-55", "ADV Bat — pet, assists Jotunn Wildkeeper"),
    ("incubus bats",     "62-64", "ADV Flock Bat"),
    ("dire bat",         "64-66", "ADV Bat — stored 63-65 = its NEWTON MOVALPOLOS entry exactly (cross-zone copy)"),
    ("jotunn hallkeeper","65-69", "ADV Gigas MNK"),
    ("jotunn wallkeeper","65-69", "ADV Gigas RNG"),
    ("jotunn wildkeeper","65-69", "ADV Gigas BST"),
    ("jotunn gatekeeper","65-69", "ADV Gigas WAR"),
    ("phasma",           "67-69", "ADV Ghost (Ixtab PH)"),
    ("magic pot",        "68-70", "ADV Magic Pot"),
    ("demonic doll",     "68-70", "ADV Doll"),
]

run(ZONE, SLUG, ROWS, write=wants_write())
