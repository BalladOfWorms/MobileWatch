#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Sauromugue Champaign (rev 273). Engine = zonepass.py
MOBS ONLY.

RULE 2 merges: `Wight` (WAR + BLM, both 26-36) and `Evil Weapon` (WAR + RDM, both
36-38) are two job rows each -> one record, one zone entry.

RULE 98: prefix of `Sauromugue Champaign [S]`; 8 of these records carry both.

The NM table is dominated by the rule-42 void cluster — 13 of 22 rows are Voidwalker
or Voidwatch and publish no level at all, including the FULL EIGHT-ELEMENTAL
Voidwalker set (Aither/Deorc/Eorthe/Puretos/Pruina/Beorht/Thunor/Lacus), none of
which had a Sauromugue entry.

59 page records (22 NM + 37 Adversaries), 0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Sauromugue Champaign"
SLUG = "sauromugue_champaign"

ROWS = [
    # --- Notorious Monsters ------------------------------------------------
    ("bashe",              SKIP, "NM  Lottery(Hill Lizard) — Lv BLANK (keeps 45-47)"),
    ("deadly dodo",       "39-40", "NM  Lottery(Tabar Beak), Cockatrice"),
    ("roc",               "55",  "NM  Timed 21-24 hr, WHM, Greater Bird"),
    ("thunderclaw thuban", SKIP, "NM  Timed 1.5-2 hr, Raptor — Lv BLANK (keeps 47-48)"),
    ("blighting brand",    SKIP, "NM  Lottery(RDM-type Evil Weapon) — Lv BLANK, 0 zones before"),
    ("climbpix highrise", "55",  "NM  Quest(As Thick as Thieves), THF, Goblin — zone stored level-less"),
    ("dribblix greasemaw", SKIP, "NM  Mission(A Crystalline Prophecy 3), RNG — Lv BLANK, 0 zones before"),
    ("old sabertooth",    "20",  "NM  Quest(The Fanged One), WAR, Tiger — 0 zones before"),
    ("arke",              "125", "NM  UNM 2,100 accolades, WHM/BRD, Greater Bird"),
    ("goji",               SKIP, "NM  Voidwatch (White stratum abyssite II), Gargouille — Lv BLANK (keeps 92-94)"),
    ("aither",             SKIP, "NM  Voidwalker Elemental (Clear abyssite) — Lv BLANK, no Sauromugue entry before"),
    ("deorc",              SKIP, "NM  Voidwalker Elemental (Clear abyssite) — Lv BLANK, no Sauromugue entry before"),
    ("eorthe",             SKIP, "NM  Voidwalker Elemental (Clear abyssite) — Lv BLANK, no Sauromugue entry before"),
    ("puretos",            SKIP, "NM  Voidwalker Elemental (Clear abyssite) — Lv BLANK, no Sauromugue entry before"),
    ("pruina",             SKIP, "NM  Voidwalker Elemental (Clear abyssite) — Lv BLANK, no Sauromugue entry before"),
    ("beorht",             SKIP, "NM  Voidwalker Elemental (Clear abyssite) — Lv BLANK, no Sauromugue entry before"),
    ("thunor",             SKIP, "NM  Voidwalker Elemental (Clear abyssite) — Lv BLANK, no Sauromugue entry before"),
    ("lacus",              SKIP, "NM  Voidwalker Elemental (Clear abyssite) — Lv BLANK, no Sauromugue entry before"),
    ("urd",                SKIP, "NM  Voidwalker Pixie (Colorful abyssite), DNC — Lv BLANK"),
    ("skuld",              SKIP, "NM  Voidwalker Pixie (Colorful abyssite) — Lv BLANK"),
    ("verthandi",          SKIP, "NM  Voidwalker Pixie (Yellow abyssite) — Lv BLANK"),
    ("yilbegan",           SKIP, "NM  Voidwalker (Black abyssite) — Lv BLANK (keeps 90-92); 28th zone"),
    # --- Adversaries --------------------------------------------------------
    ("midnight wings",    "20-23", "ADV Flock Bat, nighttime 18:00-6:00"),
    ("hill lizard",       "22-26", "ADV Lizard (Bashe PH)"),
    ("goblin's beetle",   "23-25", "ADV Beetle — pet"),
    ("yagudo's elemental","23-25", "ADV Elemental — pet, assists Yagudo Oracle; 0 Sauromugue entry before"),
    ("moon bat",          "23-26", "ADV Bat, nighttime 18:00-6:00"),
    ("diving beetle",     "25-28", "ADV Beetle"),
    ("goblin gambler",    "26-30", "ADV Goblin BLM"),
    ("goblin leecher",    "26-30", "ADV Goblin WHM"),
    ("goblin mugger",     "26-30", "ADV Goblin THF"),
    ("yagudo priest",     "26-30", "ADV Yagudo WHM"),
    ("yagudo theologist", "26-30", "ADV Yagudo BLM"),
    ("yagudo votary",     "26-30", "ADV Yagudo MNK"),
    ("wight",             "26-36", "ADV Skeleton — WAR + BLM rows, both 26-36"),
    ("goblin digger",     "28-32", "ADV Goblin"),
    ("sabertooth tiger",  "28-32", "ADV Tiger"),
    ("sauromugue skink",  "28-32", "ADV Raptor"),
    ("champaign coeurl",  "30-34", "ADV Coeurl"),
    ("goblin furrier",    "30-36", "ADV Goblin RNG"),
    ("goblin pathfinder", "30-36", "ADV Goblin BST"),
    ("goblin shaman",     "30-36", "ADV Goblin BLM"),
    ("goblin smithy",     "30-36", "ADV Goblin WAR"),
    ("yagudo drummer",    "30-36", "ADV Yagudo BRD"),
    ("yagudo herald",     "30-36", "ADV Yagudo NIN"),
    ("yagudo interrogator","30-36","ADV Yagudo SAM"),
    ("yagudo oracle",     "30-36", "ADV Yagudo SMN"),
    ("will-o'-the-wisp",  "34-36", "ADV Bomb, fog weather — 0 Sauromugue entry before; its highest band anywhere"),
    ("tabar beak",        "34-37", "ADV Cockatrice, Timed 5 min (Deadly Dodo PH)"),
    ("evil spirit",       "35-38", "ADV Ghost, undead 20:00-4:00"),
    ("evil weapon",       "36-38", "ADV Evil Weapon — WAR + RDM rows, both 36-38 (Blighting Brand PH)"),
    ("earth elemental",   "38-40", "ADV Elemental, earth weather — 0 Sauromugue entry before"),
    ("thunder elemental", "38-40", "ADV Elemental, thunder weather — 0 Sauromugue entry before"),
    ("big jaw",           "20-23", "ADV Pugil, Fished Up"),
    ("land pugil",        "20-23", "ADV Pugil, Fished Up"),
    ("snipper",           "20-23", "ADV Crab, Fished Up"),
    ("cutter",            "28-30", "ADV Crab, Fished Up"),
    ("greater pugil",     "28-30", "ADV Pugil, Fished Up"),
    ("kraken",            "38-40", "ADV Sea Monk, Fished Up"),
]

LV_EXTEND = {
    "will-o'-the-wisp": (34, 36),   # [22,27] -> [22,36]
}

run(ZONE, SLUG, ROWS, lv_extend=LV_EXTEND, write=wants_write())
