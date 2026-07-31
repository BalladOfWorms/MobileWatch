#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Tahrongi Canyon (rev 171). Engine = zonepass.py

FIRST PASS UNDER THE NARROWED REMIT (rule 84): mobs only. The info box was read
solely to identify the zone — no `weather`, no `notes`, no zoneinfo field harvested
from it. `zoneinfo_edit` is not passed at all, so the engine cannot touch zoneinfo.

Rule 57 clean — `Tahrongi Canyon` and `Abyssea-Tahrongi` are both zones.json names.
Rule 65 applied; all 40 page names resolved first try.

44 page rows -> 40 distinct records. `Goblin Weaver` is two rows (RDM + THF, both
8-10) and `Poltergeist` is two rows (WAR + RDM, both 18-20) -> one record each.

Rule 79 again: `air elemental` AND `earth elemental` both missing, plus
`yagudo's elemental` — three elementals on one page, none of them zoned here.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Tahrongi Canyon"
SLUG = "tahrongi_canyon"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("yara ma yha who",      "15-20", "NM  Forced (trade Distilled Water to ???)"),
    ("serpopard ishtar",     "19-20", "NM  Lottery(Wild Dhalmel)"),
    ("herbage hunter",       "28",    "NM  Lottery(Canyon Crawler)  (stored 28-29)"),
    ("goblin archaeologist", "30-75", "NM  Forced (trade various items to ???)"),
    ("serpopard ninlil",     "99",    "NM  UNM 400 accolades"),
    ("habrok",               SKIP,    "NM  wind weather — Lv BLANK (keeps 16-18)"),
    ("smierc",               SKIP,    "NM  Voidwatch — Lv BLANK (0 zones before)"),
    ("prickly sheep",        SKIP,    "NM  Voidwalker — Lv BLANK (0 zones before)"),
    ("void hare",            SKIP,    "NM  Voidwalker — Lv BLANK (0 zones before)"),
    ("chesma",               SKIP,    "NM  Voidwalker — Lv BLANK"),
    ("tammuz",               SKIP,    "NM  Voidwalker — Lv BLANK"),
    ("dawon",                SKIP,    "NM  Voidwalker — Lv BLANK (0 zones before)"),
    ("yilbegan",             SKIP,    "NM  Voidwalker — Lv BLANK (keeps 90-92)"),
    # --- Adversaries -----------------------------------------------------
    ("yagudo's elemental", "5-7",   "ADV 5-7  (rule 79; not zoned here)"),
    ("canyon rarab",       "7-10",  "ADV 7-10"),
    ("strolling sapling",  "7-10",  "ADV 7-10"),
    ("pygmaioi",           "7-11",  "ADV 7-11"),
    ("barghest",           "8-10",  "ADV 8-10"),
    ("goblin weaver",      "8-10",  "ADV RDM + THF rows, both 8-10"),
    ("killer bee",         "8-10",  "ADV 8-10"),
    ("yagudo acolyte",     "8-10",  "ADV 8-10"),
    ("yagudo initiate",    "8-10",  "ADV 8-10"),
    ("yagudo scribe",      "8-10",  "ADV 8-10"),
    ("akbaba",             "9-13",  "ADV 9-13"),
    ("skeleton warrior",   "10-12", "ADV 10-12"),
    ("canyon crawler",     "11-13", "ADV 11-13"),
    ("skeleton sorcerer",  "11-13", "ADV 11-13"),
    ("goblin digger",      "11-14", "ADV 11-14"),
    ("goblin ambusher",    "12-16", "ADV 12-16"),
    ("goblin butcher",     "12-16", "ADV 12-16"),
    ("goblin tinkerer",    "12-16", "ADV 12-16"),
    ("yagudo mendicant",   "12-16", "ADV 12-16"),
    ("yagudo persecutor",  "12-16", "ADV 12-16"),
    ("yagudo piper",       "12-16", "ADV 12-16"),
    ("wild dhalmel",       "14-16", "ADV 14-16"),
    ("ghost",              "15-17", "ADV 15-17"),
    # the page's `Grenade` row is `grenade (monster)`, which already carries this zone;
    # the bare `grenade` key is a 7-field stub with no zones — see (mq)
    ("grenade (monster)",  "15-17", "ADV 15-17"),
    ("air elemental",      "18-20", "ADV 18-20 weather-spawned  (rule 79)"),
    ("earth elemental",    "18-20", "ADV 18-20 weather-spawned  (rule 79)"),
    ("poltergeist",        "18-20", "ADV WAR + RDM rows, both 18-20"),
]

# rule 9 — nothing to extend. NOTE `herbage hunter` is single-zone, so narrowing
# 28-29 -> 28 strands its lv max of 29 (rule 76's shape); rule 1 forbids shrinking.
LV_EXTEND = {}

# NO zoneinfo_edit — rule 84.
run(ZONE, SLUG, ROWS, LV_EXTEND, write=wants_write())
