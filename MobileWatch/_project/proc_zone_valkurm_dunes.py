#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Valkurm Dunes (rev 175). Engine = zonepass.py
Mobs only (rule 84/87) — no zoneinfo_edit is passed, so zoneinfo cannot be touched.

Rule 57 clean — `Valkurm Dunes` and `Dynamis-Valkurm` are BOTH zones.json names
(the Bibiki/Purgonorgo shape: two genuinely different zones, not two spellings).
Rule 65 applied — all 36 names resolved against the FILE first try.

39 page rows -> 36 distinct records, 0 missing.
THREE rule-2 merges, and zoneinfo independently publishes all three merged spans:
  Ghoul       WAR 18-22 + BLM 20-24        -> 18-24
  Snipper     ground 18-22 + Fished-Up 20-22 -> 18-22
  Beach Pugil ground 23-26 + Fished-Up 23-25 -> 23-26

SEAMS: the Damselfly row splits shots 3/4 and Beach Pugil splits 4/5; both are
overlaps, not gaps — zoneinfo's own 9 nms[] + 27 mobs[] rows match the read
roster exactly (rule 91).
"""
from zonepass import run, wants_write, SKIP

ZONE = "Valkurm Dunes"
SLUG = "valkurm_dunes"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("metal shears",       SKIP,    "NM  TODO: spawn cell — Lv BLANK (0 zones before)"),
    ("golden bat",         "26-27", "NM  Lottery(Giant Bat)"),
    ("valkurm emperor",    "29-30", "NM  Lottery(Damselfly)"),
    ("hippomaritimus",     SKIP,    "NM  Timed (no interval) — Lv BLANK (keeps ~38)"),
    ("doman",              "52",    "NM  Quest(Yomi Okuri)  (0 zones before)"),
    ("marchelute",         "50-53", "NM  Quest(Messenger from Beyond) — lv [41,41] disjoint"),
    ("onryo",              "52",    "NM  Quest(Yomi Okuri)  — zone stored level-less"),
    ("valkurm imperator",  "119",   "NM  UNM 1,500 Unity Accolades"),
    ("ig-alima",           SKIP,    "NM  Voidwatch — Lv BLANK"),
    # --- Adversaries ------------------------------------------------------
    ("night bats",         "12-15", "ADV 12-15 nighttime"),
    ("sand bats",          "12-15", "ADV 12-15"),
    ("hill lizard",        "15-18", "ADV 15-18"),
    ("sand hare",          "15-18", "ADV 15-18"),
    ("goblin ambusher",    "17-20", "ADV 17-20 RNG"),
    ("goblin butcher",     "17-20", "ADV 17-20 WAR"),
    ("goblin tinkerer",    "17-20", "ADV 17-20 DRK"),
    ("star bat",           "17-20", "ADV 17-20 nighttime"),
    ("goblin bounty hunter","17-25","ADV 17-25 WAR"),
    ("ghoul",              "18-24", "ADV rule 2: WAR 18-22 + BLM 20-24"),
    ("snipper",            "18-22", "ADV rule 2: ground 18-22 + Fished-Up 20-22"),
    ("goblin digger",      "19-21", "ADV 19-21"),
    ("giant bat",          "20-22", "ADV 20-22"),
    ("brutal sheep",       "20-23", "ADV 20-23"),
    ("damselfly",          "20-23", "ADV 20-23"),
    ("thread leech",       "21-25", "ADV 21-25"),
    ("goblin gambler",     "22-25", "ADV 22-25 BLM"),
    ("goblin leecher",     "22-25", "ADV 22-25 WHM"),
    ("goblin mugger",      "22-25", "ADV 22-25 THF"),
    ("beach pugil",        "23-26", "ADV rule 2: ground 23-26 + Fished-Up 23-25"),
    ("will-o'-the-wisp",   "25-27", "ADV 25-27 fog weather"),
    ("bogy",               "28-30", "ADV 28-30 undead"),
    ("earth elemental",    "28-30", "ADV 28-30 weather-spawned  (rule 79 — 6th zone)"),
    ("fire elemental",     "28-30", "ADV 28-30 weather-spawned  (rule 79 — 6th zone)"),
    ("puffer pugil",       "15-17", "ADV Fished-Up 15-17"),
    ("stag crab",          "15-17", "ADV Fished-Up 15-17"),
    ("cutter",             "28-30", "ADV Fished-Up 28-30"),
]

# rule 9 — the one page level outside its record's band. `marchelute` stores
# lv [41,41] with ZERO zones, so nothing sourced the 41; the page's 50-53 is the
# only evidence there is. Union rather than replace (rule 1 forbids shrinking).
LV_EXTEND = {
    "marchelute": (50, 53),       # [41,41] -> [41,53]
}

run(ZONE, SLUG, ROWS, LV_EXTEND, write=wants_write())
