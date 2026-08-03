#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: La Theine Plateau (rev 172). Engine = zonepass.py
Mobs only (rule 84) — no zoneinfo_edit is passed, so zoneinfo cannot be touched.

Rule 57 clean — `La Theine Plateau` and `Abyssea-La Theine` are both zones.json names.
Rule 65 applied; all 50 page names resolved first try.

52 page rows -> 50 distinct records, 41 already exactly right. `Poltergeist` is two
rows (WAR + RDM, both 18-20) -> one record.

The page's `Grenade` row is matched to **`grenade (monster)`**, which holds all three
of that mob's zones and the full kit; the bare `grenade` key is a 6-field record with
none. NOTE this is the pairing the user's new naming rule inverts — see the handoff.
"""
from zonepass import run, wants_write, SKIP

ZONE = "La Theine Plateau"
SLUG = "la_theine_plateau"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("tumbling truffle",     "19-20", "NM  Lottery(Poison Funguar)"),
    ("lumbering lambert",    "27-28", "NM  Lottery(Battering Ram)"),
    ("goblin archaeologist", "30-75", "NM  Forced (various items)"),
    ("bloodtear baldurf",    "55-56", "NM  Lottery(Lumbering Lambert)"),
    ("ironhorn baldurno",    "99",    "NM  UNM 400 accolades"),
    ("nihniknoovi",          SKIP,    "NM  Forced (Fallen Egg) — Lv BLANK (keeps 14)"),
    ("slumbering samwell",   SKIP,    "NM  Timed — Lv BLANK (0 zones before)"),
    ("stachysaurus",         SKIP,    "NM  Voidwatch — Lv BLANK (0 zones before)"),
    ("prickly sheep",        SKIP,    "NM  Voidwalker — Lv BLANK (not zoned here)"),
    ("void hare",            SKIP,    "NM  Voidwalker — Lv BLANK (not zoned here)"),
    ("chesma",               SKIP,    "NM  Voidwalker — Lv BLANK"),
    ("tammuz",               SKIP,    "NM  Voidwalker — Lv BLANK"),
    ("dawon",                SKIP,    "NM  Voidwalker — Lv BLANK (not zoned here)"),
    ("yilbegan",             SKIP,    "NM  Voidwalker — Lv BLANK (keeps 90-92)"),
    # --- Adversaries -----------------------------------------------------
    ("gale bats",          "6-8",   "ADV 6-8 nighttime"),
    ("steppe hare",        "7-10",  "ADV 7-10"),
    ("strolling sapling",  "7-10",  "ADV 7-10"),
    ("rock eater",         "7-11",  "ADV 7-11"),
    ("acro bat",           "8-10",  "ADV 8-10 nighttime"),
    ("goblin fisher",      "8-10",  "ADV 8-10"),
    ("goblin thug",        "8-10",  "ADV 8-10"),
    ("goblin weaver",      "8-10",  "ADV 8-10"),
    ("orcish fodder",      "8-10",  "ADV 8-10"),
    ("orcish grappler",    "8-10",  "ADV 8-10"),
    ("orcish mesmerizer",  "8-10",  "ADV 8-10"),
    ("huge wasp",          "8-12",  "ADV 8-12"),
    ("plague bats",        "9-11",  "ADV 9-11 nighttime"),
    ("akbaba",             "9-13",  "ADV 9-13"),
    ("skeleton warrior",   "10-12", "ADV 10-12 undead"),
    ("grass funguar",      "11-13", "ADV 11-13"),
    ("mad sheep",          "11-13", "ADV 11-13"),
    ("skeleton sorcerer",  "11-13", "ADV 11-13 undead"),
    ("goblin digger",      "11-14", "ADV 11-14"),
    ("poison bat",         "11-14", "ADV 11-14"),
    ("thickshell",         "12-14", "ADV 12-14"),
    ("goblin ambusher",    "12-16", "ADV 12-16"),
    ("goblin butcher",     "12-16", "ADV 12-16"),
    ("goblin tinkerer",    "12-16", "ADV 12-16"),
    ("orcish grunt",       "12-16", "ADV 12-16"),
    ("orcish neckchopper", "12-16", "ADV 12-16"),
    ("orcish stonechucker","12-16", "ADV 12-16"),
    ("puffer pugil",       "14-16", "ADV Fished-Up 14-16"),
    ("poison funguar",     "14-16", "ADV 14-16"),
    ("ghost",              "15-17", "ADV 15-17 undead"),
    ("grenade (monster)",  "15-17", "ADV 15-17 fog weather"),
    ("land pugil",         "15-17", "ADV Fished-Up 15-17"),
    ("air elemental",      "18-20", "ADV 18-20 weather-spawned  (rule 79)"),
    ("water elemental",    "18-20", "ADV 18-20 weather-spawned  (rule 79)"),
    ("poltergeist",        "18-20", "ADV WAR + RDM rows, both 18-20"),
    ("battering ram",      "21-23", "ADV 21-23"),
]

# rule 9 — nothing to extend; every added range sits inside its record's band.
LV_EXTEND = {}

run(ZONE, SLUG, ROWS, LV_EXTEND, write=wants_write())
