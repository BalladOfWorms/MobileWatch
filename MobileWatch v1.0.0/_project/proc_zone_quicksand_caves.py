#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Quicksand Caves (rev 280). Engine = zonepass.py
MOBS ONLY — the info box is pure lore (the Galka/Antica history), no mechanics.

**The best-covered page of the whole sweep: 34 of 42 records were already exact**,
and 26 of the 42 are NMs — the largest NM table seen. Every one of the 17 world-spawn
NMs was already right, `nmlv` and the zone entry agreeing throughout.

42 page records (26 NM + 16 Adversaries), 0 missing, bucket E empty.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Quicksand Caves"
SLUG = "quicksand_caves"

ROWS = [
    ("antican consul",      "75",    "NM  Timed 21-24 hr, WAR"),
    ("antican legatus",     "72-74", "NM  Timed 20 min, PLD"),
    ("antican magister",    "66",    "NM  Lottery(Antican Hastatus), WAR"),
    ("antican praefectus",  "65",    "NM  Lottery(Antican Princeps), PLD — drops Save the Queen"),
    ("antican praetor",     "72-74", "NM  Timed 20 min, BLM"),
    ("antican proconsul",   "65",    "NM  Lottery(Antican Signifer), BLM"),
    ("antican tribunus",    "72-74", "NM  Lottery(Antican Aedilis), RNG"),
    ("centurio x-i",        "56-58", "NM  Lottery(Antican Signifer), BLM"),
    ("diamond daig",        "70",    "NM  Lottery(Helm Beetle) during DOUBLE earth weather, PLD"),
    ("hastatus xi-xii",     "65-68", "NM  Lottery(Antican Triarius), WAR"),
    ("nussknacker",         "60",    "NM  Lottery(Sand Lizard) during DOUBLE earth weather, WAR"),
    ("proconsul xii",       "72",    "NM  Timed 2 hr, PLD — drops Dainslaif"),
    ("sabotender bailarin", "68-70", "NM  Lottery(Sabotender Bailaor), WAR"),
    ("sabotender bailarina","80-82", "NM  Lottery(Spelunking Sabotender), WAR"),
    ("sagittarius x-xiii",  "57-58", "NM  Lottery(Antican Princeps), RNG"),
    ("triarius x-xv",       "72-74", "NM  Lottery(Antican Triarius), WAR"),
    ("tribunus vii-i",      "60-62", "NM  Forced (trade Antican Tag to ???), WAR"),
    ("ancient vessel",      "72",    "NM  Mission(Zilart 12), RDM, Magic Pot"),
    ("centurio iv-vii",     "70",    "NM  Mission(Bastok 8-1), WAR — zone stored level-less"),
    ("girtablulu",          SKIP,    "NM  Quest(Old Wounds), WAR, Scorpion — Lv BLANK"),
    ("honor",               SKIP,    "NM  Mission(San d'Oria 8-1), Sea Monk — Lv BLANK"),
    ("princeps iv-xlv",     "70",    "NM  Mission(Bastok 8-1), PLD — zone stored level-less"),
    ("triarius iv-xiv",     "70",    "NM  Mission(Bastok 8-1), BLM — zone stored level-less"),
    ("valor",               SKIP,    "NM  Mission(San d'Oria 8-1), MNK, Sea Monk — Lv BLANK"),
    ("centurio xx-i",       "125",   "NM  UNM 2,100 accolades, BLM/WHM"),
    ("malleator maurok",    SKIP,    "NM  Voidwatch (Ashen stratum abyssite), Scorpion — Lv BLANK, 0 zones before"),
    ("antican aedilis",     "62-75", "ADV Antica RNG, 25 spawns — stored 62-72 (Antican Tribunus PH)"),
    ("antican antesignanus","62-72", "ADV Antica PLD, 28 spawns"),
    ("antican hastatus",    "52-59", "ADV Antica WAR, Quicksand Coffer Key, 46 spawns"),
    ("antican princeps",    "52-59", "ADV Antica PLD, Quicksand Coffer Key, 51 spawns"),
    ("antican quaestor",    "62-72", "ADV Antica BLM, 29 spawns"),
    ("antican signifer",    "52-59", "ADV Antica BLM, Quicksand Coffer Key, 47 spawns"),
    ("antican triarius",    "62-72", "ADV Antica WAR, 28 spawns"),
    ("girtab",              "62-65", "ADV Scorpion, 19 spawns"),
    ("helm beetle",         "51-58", "ADV Beetle, Quicksand Coffer Key, 35 spawns (Diamond Daig PH)"),
    ("sabotender bailaor",  "52-59", "ADV Sabotender, Quicksand Coffer Key, 25 spawns"),
    ("sand digger",         "62-65", "ADV Worm, 4 spawns"),
    ("sand eater",          "51-59", "ADV Worm, Quicksand Coffer Key, 32 spawns"),
    ("sand lizard",         "56-59", "ADV Lizard, Quicksand Coffer Key, 27 spawns (Nussknacker PH)"),
    ("sand spider",         "51-55", "ADV Spider, Quicksand Coffer Key, 16 spawns"),
    ("sand tarantula",      "65-68", "ADV Spider, 12 spawns"),
    ("spelunking sabotender","62-68","ADV Sabotender, 11 spawns (Sabotender Bailarina PH)"),
]

LV_EXTEND = {
    "antican aedilis": (62, 75),   # [62,72] -> [62,75]
}

run(ZONE, SLUG, ROWS, lv_extend=LV_EXTEND, write=wants_write())
