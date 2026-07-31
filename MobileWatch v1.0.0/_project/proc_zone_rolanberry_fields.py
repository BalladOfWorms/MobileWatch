#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Rolanberry Fields (rev 183). Engine = zonepass.py
Mobs only (rule 84/87) — no zoneinfo_edit is passed.

RULE 98 for the fourth time in five zones: `Rolanberry Fields` is a prefix of
`Rolanberry Fields [S]`, and **21 records carry BOTH**. [S] entries re-checked
after the write.
Rule 65 applied — all 56 names resolved first try. The page's `Ochu` row is
matched to **`ochu (monster)`** (fam Morbol, 12 fields, holds BOTH Rolanberry
entries); bare `ochu` is the 7-field fam=None stub of the (mq)-class pair, and
the user's pending naming rule would swap the two names.
Rule 91 — zoneinfo publishes 21 nms[] + 35 mobs[]; the shots read 21 + 37, which
is 21 + 35 after the two job pairs (Wight WAR/BLM both 26-36, Evil Weapon
RDM/WAR both 36-38). Reconciles exactly.

58 page rows -> 56 distinct records, 0 missing.

THE VOIDWALKER ELEMENTAL SET IS THE STORY: eight one-name Elemental NMs — aither,
deorc, eorthe, puretos, pruina, beorht, thunor, lacus — every one with ZERO zones
anywhere in the file, all published here with a blank Lv. Rule 42's class at its
largest.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Rolanberry Fields"
SLUG = "rolanberry_fields"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("black triple stars", "26-27", "NM  Lottery(Midnight Wings) 18:00-6:00"),
    ("drooling daisy",     "40",    "NM  Lottery(Ochu) every 20 min, WAR"),
    ("silk caterpillar",   "28-30", "NM  Special: airship overhead — zone stored level-less"),
    ("simurgh",            "58",    "NM  Timed 1-2 hr, WAR"),
    ("ravenous crawler",   SKIP,    "NM  TODO: spawn cell — Lv BLANK (0 zones before)"),
    ("eldritch edge",      SKIP,    "NM  Lottery(Evil Weapon) — Lv BLANK (0 zones before)"),
    ("chuglix berrypaws",  SKIP,    "NM  Mission(Crystalline 3), THF — Lv BLANK (0 zones)"),
    ("strix",              "125",   "NM  UNM 2,100 accolades  (stored 99)"),
    ("yatagarasu",         SKIP,    "NM  Voidwatch — Lv BLANK"),
    ("aither",             SKIP,    "NM  Voidwalker Elemental — Lv BLANK (0 zones)"),
    ("deorc",              SKIP,    "NM  Voidwalker Elemental — Lv BLANK (0 zones)"),
    ("eorthe",             SKIP,    "NM  Voidwalker Elemental — Lv BLANK (0 zones)"),
    ("puretos",            SKIP,    "NM  Voidwalker Elemental — Lv BLANK (0 zones)"),
    ("pruina",             SKIP,    "NM  Voidwalker Elemental — Lv BLANK (0 zones)"),
    ("beorht",             SKIP,    "NM  Voidwalker Elemental — Lv BLANK (0 zones)"),
    ("thunor",             SKIP,    "NM  Voidwalker Elemental — Lv BLANK (0 zones)"),
    ("lacus",              SKIP,    "NM  Voidwalker Elemental — Lv BLANK (0 zones)"),
    ("urd",                SKIP,    "NM  Voidwalker Pixie, DNC — Lv BLANK"),
    ("skuld",              SKIP,    "NM  Voidwalker Pixie — Lv BLANK"),
    ("verthandi",          SKIP,    "NM  Voidwalker Pixie — Lv BLANK"),
    ("yilbegan",           SKIP,    "NM  Voidwalker — Lv BLANK (keeps 90-92)"),
    # --- Adversaries ------------------------------------------------------
    ("midnight wings",     "20-23", "ADV 20-23 nighttime"),
    ("death wasp",         "22-26", "ADV 22-26"),
    ("clipper",            "23-25", "ADV 23-25"),
    ("goblin's bee",       "23-25", "ADV 23-25"),
    ("moon bat",           "23-26", "ADV 23-26 nighttime"),
    ("poison leech",       "24-26", "ADV 24-26"),
    ("berry grub",         "25-28", "ADV 25-28"),
    ("brass quadav",       "26-30", "ADV 26-30 DRK"),
    ("copper quadav",      "26-30", "ADV 26-30 THF"),
    ("goblin gambler",     "26-30", "ADV 26-30 BLM"),
    ("goblin leecher",     "26-30", "ADV 26-30 WHM"),
    ("goblin mugger",      "26-30", "ADV 26-30 THF"),
    ("old quadav",         "26-30", "ADV 26-30 WAR"),
    ("wight",              "26-36", "ADV WAR + BLM rows, both 26-36"),
    ("goblin digger",      "28-32", "ADV 28-32"),
    ("goobbue farmer",     "28-32", "ADV 28-32"),
    ("bronze quadav",      "30-36", "ADV 30-36 PLD"),
    ("garnet quadav",      "30-36", "ADV 30-36 WHM"),
    ("goblin furrier",     "30-36", "ADV 30-36 RNG"),
    ("goblin pathfinder",  "30-36", "ADV 30-36 BST"),
    ("goblin shaman",      "30-36", "ADV 30-36 BLM"),
    ("goblin smithy",      "30-36", "ADV 30-36 WAR"),
    ("silver quadav",      "30-36", "ADV 30-36 THF"),
    ("zircon quadav",      "30-36", "ADV 30-36 BLM"),
    ("ignis fatuus",       "34-36", "ADV 34-36 DRK, fog weather, 3 spawns"),
    ("ochu (monster)",     "34-37", "ADV 34-37 WAR, 30 spawns — see rule 65 note"),
    ("evil spirit",        "35-38", "ADV 35-38 undead"),
    ("evil weapon",        "36-38", "ADV RDM + WAR rows, both 36-38"),
    ("fire elemental",     "38-40", "ADV 38-40 weather-spawned  (rule 79 — 12th zone)"),
    ("water elemental",    "38-40", "ADV 38-40 weather-spawned  (rule 79 — 12th zone)"),
    ("big jaw",            "20-23", "ADV Fished-Up 20-23"),
    ("snipper",            "20-23", "ADV Fished-Up 20-23"),
    ("horrid fluke",       "28-30", "ADV Fished-Up 28-30"),
    ("greater pugil",      "31-33", "ADV Fished-Up 31-33"),
    ("big leech",          "34-36", "ADV Fished-Up 34-36  (0 zones before)"),
]

# rule 9 — `strix` is a UNM: the page publishes 125 against a stored 99, and the
# other UNMs of this sweep sit the same way (Joyous Green 122, Valkurm Imperator 119).
LV_EXTEND = {
    "strix": (125, 125),          # [99,99] -> [99,125]
}

run(ZONE, SLUG, ROWS, LV_EXTEND, write=wants_write())
