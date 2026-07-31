#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Meriphataud Mountains (rev 271). Engine = zonepass.py
MOBS ONLY.

RULE 2 merges: `Zombie` (WAR + BLM, both 16-26) and `Boggart` (WAR + RDM, both
25-27) are two job rows each -> one record, one zone entry.

RULE 98: prefix of `Meriphataud Mountains [S]`; 11 of these records carry both.

!! HELD, NOT WRITTEN — `coo keja the unseen`. I read the page's Lv cell as **57**;
the record says **37** in THREE places (`lv` [37,40], `nmlv` "37", the zone entry)
and zoneinfo says 37. Decisive corroboration: its only drop, **Ajase Beads, is a
LEVEL 30 item** — a ~21-hour timed NM dropping level-30 gear fits 37, not 57. Digit
template-matching at this resolution was inconclusive (the Lv glyphs are 5px tall),
and my transcription has already been wrong twice this session (Frogmander, the Dark
gem). So the file stands and the user gets asked.

45 page records (14 NM + 31 Adversaries), 0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Meriphataud Mountains"
SLUG = "meriphataud_mountains"

ROWS = [
    # --- Notorious Monsters ------------------------------------------------
    ("coo keja the unseen", SKIP,  "NM  Timed ~21 hr, NIN — page cell read as 57; HELD at 37, see docstring"),
    ("daggerclaw dracos",  "27-28", "NM  Lottery(Raptor)"),
    ("waraxe beak",        "55-56", "NM  Timed 21-24 hr, Cockatrice"),
    ("patripatan",         SKIP,    "NM  spawn cell is literally 'TODO:' on the page, Coeurl — Lv BLANK, 0 zones before"),
    ("chonchon",           "60",    "NM  Timed 1.5-2 hr, WAR, Cockatrice"),
    ("naa zeku the unwaiting", SKIP,"NM  spawn cell is literally 'TODO:', Yagudo — Lv BLANK, 0 zones before"),
    ("warblade beak",      "122",   "NM  UNM 1,800 accolades, Cockatrice"),
    ("lord asag",          SKIP,    "NM  Voidwatch (Jade stratum abyssite III), Vampyr — Lv BLANK (keeps 94-95)"),
    ("rummager beetle",    SKIP,    "NM  Voidwalker (Clear abyssite) — Lv BLANK (rule 42)"),
    ("raker bee",          SKIP,    "NM  Voidwalker (Clear abyssite) — Lv BLANK (rule 42)"),
    ("farruca fly",        SKIP,    "NM  Voidwalker (Colorful abyssite) — Lv BLANK (rule 42)"),
    ("jyeshtha",           SKIP,    "NM  Voidwalker (Colorful abyssite), WAR — Lv BLANK (keeps 82)"),
    ("orcus",              SKIP,    "NM  Voidwalker (Brown abyssite), Antlion — Lv BLANK (rule 42)"),
    ("yilbegan",           SKIP,    "NM  Voidwalker (Black abyssite) — Lv BLANK (keeps 90-92); 27th zone"),
    # --- Adversaries --------------------------------------------------------
    ("yagudo's elemental", "9-11",  "ADV Elemental — pet, assists Yagudo Mendicant; 0 Meriphataud entry before"),
    ("night bats",         "13-16", "ADV Flock Bat, nighttime 18:00-6:00"),
    ("wandering sapling",  "13-16", "ADV Sapling"),
    ("black bat",          "15-18", "ADV Bat, nighttime 18:00-6:00"),
    ("jubjub",             "15-18", "ADV Lesser Bird"),
    ("goblin ambusher",    "16-20", "ADV Goblin RNG"),
    ("goblin butcher",     "16-20", "ADV Goblin WAR"),
    ("goblin tinkerer",    "16-20", "ADV Goblin DRK"),
    ("yagudo mendicant",   "16-20", "ADV Yagudo SMN"),
    ("yagudo persecutor",  "16-20", "ADV Yagudo SAM"),
    ("yagudo piper",       "16-20", "ADV Yagudo BRD"),
    ("zombie",             "16-26", "ADV Skeleton — WAR + BLM rows, both 16-26"),
    ("crane fly",          "18-21", "ADV Fly"),
    ("goblin digger",      "18-21", "ADV Goblin"),
    ("scavenging hound",   "18-25", "ADV Hound"),
    ("hill lizard",        "19-22", "ADV Lizard"),
    ("stag beetle",        "20-23", "ADV Beetle"),
    ("goblin gambler",     "21-25", "ADV Goblin BLM"),
    ("goblin leecher",     "21-25", "ADV Goblin WHM"),
    ("goblin mugger",      "21-25", "ADV Goblin THF"),
    ("raptor",             "21-25", "ADV Raptor (Daggerclaw Dracos PH) — stored 21-24"),
    ("yagudo priest",      "21-25", "ADV Yagudo WHM"),
    ("yagudo theologist",  "21-25", "ADV Yagudo BLM"),
    ("yagudo votary",      "21-25", "ADV Yagudo MNK"),
    ("coeurl",             "22-25", "ADV Coeurl (Patripatan PH per zoneinfo)"),
    ("will-o'-the-wisp",   "24-25", "ADV Bomb, fog weather, 4 spawns"),
    ("boggart",            "25-27", "ADV Evil Weapon — WAR + RDM rows, both 25-27"),
    ("axe beak",           "25-28", "ADV Cockatrice"),
    ("bogy",               "25-29", "ADV Ghost, undead 20:00-4:00 — stored 23-25"),
    ("earth elemental",    "27-29", "ADV Elemental, earth weather — 0 Meriphataud entry before"),
    ("fire elemental",     "27-29", "ADV Elemental, fire weather — 0 Meriphataud entry before"),
]

run(ZONE, SLUG, ROWS, write=wants_write())
