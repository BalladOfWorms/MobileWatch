#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Qufim Island (rev 276). Engine = zonepass.py
MOBS ONLY.

RULE 2 merges: `Dancing Weapon` (WAR + RDM, 28-30) and `Wight` (BLM + WAR, 28-30) are
job pairs; `Greater Pugil` is a ground block 28-30 PLUS a Fished Up block 25-27 ->
**25-30** (zoneinfo already stores exactly that).

**`Kraken` is the FIFTH cross-table mob of the sweep** (after King Ranperre's Spook,
Toraimarai's Hinge Oil, Bibiki's pattern and Batallia's Sobbing Sapling): it is an NM
row (39-40, Fished Up) AND two Adversaries rows (37-38 Timed, 39-40 Fished Up).
One record, one merged entry -> **37-40**. The stored 35-40 claims a 35-36 block the
page does not list anywhere, so it is narrowed, not kept (the opposite of rule 107 —
there the FILE was more precise; here the file is merely wider).

32 page records (10 NM + 23 Adversaries -> 22 after Kraken folds into the NM row),
0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Qufim Island"
SLUG = "qufim_island"

ROWS = [
    ("dosetsu tree",      "38-40", "NM  Timed ~21 hr during thunder weather, WAR, Treant"),
    ("trickster kinetix", "35-36", "NM  Lottery(Dancing Weapon), WAR"),
    ("kraken",            "37-40", "NM + ADV x2 — cross-table; stored 35-40 claims a block the page lacks"),
    ("slippery sucker",   SKIP,    "NM  Lottery(the four Giant jobs), Leech — Lv BLANK, 0 zones before"),
    ("atkorkamuy",        "73-74", "NM  Timed 30 min, Sea Monk"),
    ("qoofim",            SKIP,    "NM  Timed (no interval published), WAR, Pugil — Lv BLANK (keeps ~48)"),
    ("ingaevon",          "53-55", "NM  Quest(Regaining Trust), RNG, Gigas — zone stored level-less"),
    ("seed mandragora",   SKIP,    "NM  Mission(A Crystalline Prophecy 4), MNK — Lv BLANK, 0 zones before"),
    ("jester malatrix",   "119",   "NM  UNM 1,500 accolades, WAR, Evil Weapon"),
    ("kaggen",            SKIP,    "NM  Voidwatch (White stratum abyssite III), Mantid — Lv BLANK"),
    ("gigas's leech",     "21-30", "ADV Leech — pet, assists Giant Trapper"),
    ("dark bats",         "25-27", "ADV Flock Bat, nighttime 18:00-6:00"),
    ("land worm",         "25-27", "ADV Worm"),
    ("seeker bats",       "25-27", "ADV Flock Bat, nighttime 18:00-6:00"),
    ("qufim pugil",       "25-27", "ADV Pugil, Fished Up"),
    ("clipper",           "25-29", "ADV Crab"),
    ("ancient bat",       "27-29", "ADV Bat, nighttime"),
    ("glow bat",          "27-29", "ADV Bat, nighttime"),
    ("dancing weapon",    "28-30", "ADV Evil Weapon — WAR + RDM rows (Trickster Kinetix PH)"),
    ("greater pugil",     "25-30", "ADV Pugil — RULE 2: ground 28-30 + Fished Up 25-27"),
    ("wight",             "28-30", "ADV Skeleton — BLM + WAR rows, both 28-30"),
    ("giant ascetic",     "28-31", "ADV Gigas MNK (Slippery Sucker PH)"),
    ("giant hunter",      "28-31", "ADV Gigas RNG (Slippery Sucker PH)"),
    ("giant ranger",      "28-31", "ADV Gigas WAR (Slippery Sucker PH)"),
    ("giant trapper",     "28-31", "ADV Gigas BST (Slippery Sucker PH)"),
    ("sea bishop",        "30-32", "ADV Sea Monk, Fished Up"),
    ("banshee",           "31-33", "ADV Ghost, undead 20:00-4:00"),
    ("goblin bounty hunter", "32", "ADV Goblin WAR — page reads 32-32; stored 15-32 spans four zones' worth"),
    ("acrophies",         "32-34", "ADV Leech"),
    ("light elemental",   "35-36", "ADV Elemental, light weather — 0 Qufim entry before"),
    ("thunder elemental", "35-36", "ADV Elemental, thunder weather — 0 Qufim entry before"),
    ("vepar",             "35-36", "ADV Pugil, Fished Up"),
]

run(ZONE, SLUG, ROWS, write=wants_write())
