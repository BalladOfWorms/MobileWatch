#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: West Ronfaure (rev 151). Data only; engine = zonepass.py

Sources: 4 uploaded shots — (1) info box, (2) NM table + start of Adversaries,
(3)+(4) the rest of the Adversaries table.

31 page rows -> 30 distinct records: `Enchanted Bones` is TWO rows (WAR 5-8 and
DRK 5-8) -> one record. All five Fished-Up rows are Crabs; there is no ground
Pugil in this zone.

TWO RULE-3 COPY ERRORS, both copied from EAST RONFAURE (the adjacent same-region
zone — the South/North Gustaberg shape exactly):
  enchanted bones    stored 4-8 == its East Ronfaure entry   -> page says 5-8
  orcish mesmerizer  stored 3-8 == its East Ronfaure entry   -> page says 4-8
Both were ALREADY CORRECT in zoneinfo.json's mobs[] — see (lo).
"""
from zonepass import run, wants_write, SKIP

ZONE = "West Ronfaure"
SLUG = "west_ronfaure"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("amanita",            "5-6",   "NM  Timed 60-70 min"),
    ("fungus beetle",      "10-11", "NM  Lottery(Scarab Beetle)"),
    ("jaggedy-eared jack", "9-10",  "NM  Lottery(Forest Hare)"),
    ("marauder dvogzog",   "67",    "NM  Mission — Prestige of the Papsque"),
    ("lancing lamorak",    SKIP,    "NM  Voidwatch — Lv cell BLANK"),
    # --- Adversaries (ground) --------------------------------------------
    ("tunnel worm",        "1",     "ADV 1-1 -> '1'"),
    ("wild rabbit",        "1",     "ADV 1-1 -> '1'"),
    ("carrion worm",       "1-5",   "ADV 1-5"),
    ("ding bats",          "1-5",   "ADV 1-5 nighttime"),
    ("forest hare",        "1-5",   "ADV 1-5"),
    ("forest funguar",     "3-6",   "ADV 3-6"),
    ("mouse bat",          "3-6",   "ADV 3-6 nighttime"),
    ("river crab",         "3-6",   "ADV 3-6"),
    ("scarab beetle",      "3-6",   "ADV 3-6"),
    ("orcish fodder",      "3-8",   "ADV 3-8"),
    ("orcish grappler",    "3-8",   "ADV 3-8"),
    ("goblin thug",        "4-8",   "ADV 4-8"),
    ("goblin weaver",      "4-8",   "ADV 4-8"),
    ("orcish mesmerizer",  "4-8",   "ADV 4-8  (rule-3 copy of East Ronfaure 3-8)"),
    ("enchanted bones",    "5-8",   "ADV 5-8  (WAR + DRK rows; rule-3 copy of East Ronfaure 4-8)"),
    ("goblin digger",      "5-8",   "ADV 5-8"),
    ("goblin fisher",      "5-8",   "ADV 5-8"),
    ("tainted hound",      "5-8",   "ADV 5-8 undead"),
    ("wild sheep",         "5-8",   "ADV 5-8"),
    ("bomb",               "8-10",  "ADV 8-10 fog weather"),
    # --- Adversaries (Fished Up) -----------------------------------------
    ("limicoline crab",    "2-4",   "ADV Fished-Up 2-4"),
    ("tree crab",          "2-4",   "ADV Fished-Up 2-4"),
    ("land crab",          "5-6",   "ADV Fished-Up 5-6"),
    ("vermivorous crab",   "7-8",   "ADV Fished-Up 7-8"),
    ("passage crab",       "9-10",  "ADV Fished-Up 9-10"),
]

# rule 9 — no unions needed: enchanted bones' lv min 4 is still backed by its
# East Ronfaure 4-8 entry, and orcish mesmerizer's lv min 3 by East Ronfaure 3-8.
LV_EXTEND = {}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # rule 12 — a traversal fact about the existing Survival Guide travel row
    note = ("The Survival Guide here is the closest teleport to the Cavernous Maw "
            "in La Theine Plateau for Abyssea - La Theine.")
    e.setdefault('notes', [])
    if note not in e['notes']:
        e['notes'].append(note)
        out.append("notes += Survival Guide / Cavernous Maw (Abyssea - La Theine) hop")
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
