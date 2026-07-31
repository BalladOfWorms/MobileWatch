#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Bibiki Bay (rev 165). Engine = zonepass.py

Rule 57 clean — `Bibiki Bay` and `Bibiki Bay - Purgonorgo Isle` are BOTH zones.json
names, so the two buckets are correct, not a split. Rule 65 applied: all 39 page
names resolved against the file first try.

Sources: 5 shots — (1) info box, (2) NM table + start of Adversaries, (3)-(5) the rest.

44 page rows -> 39 distinct records. `Goblin's Rarab` appears TWICE with a huge gap
between the blocks — 29-31 (wild) and 67-69 (Pet) -> merged span **29-69** (rule 2,
the Misareaux Fomor precedent). `Hobgoblin Angler` reads 80-80 -> "80".

!! EIGHT RECORDS ON THIS PAGE HAVE NO `lv` KEY AT ALL and the page publishes one for
each. That is a direct dent in (mi)'s 972 — the band is CREATED from the page here,
which is purely additive (rule 1) and is what LV_EXTEND already does for an absent lv.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Bibiki Bay"
SLUG = "bibiki_bay"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("intulo",             "46-47",   "NM  Lottery(Eft)"),
    ("intuila",            "119",     "NM  UNM 1,500 accolades"),
    ("locus fiddler crab", "137-139", "NM  Lottery(Locus Ghost Crab)  (0 zones, NO lv)"),
    ("splacknuck",         SKIP,      "NM  spawn cell reads 'TODO:' — Lv BLANK (0 zones)"),
    ("dalham",             SKIP,      "NM  Promathia 7-4 — Lv BLANK"),
    # --- Adversaries, the 29-46 tier -------------------------------------
    ("goblin's rarab",     "29-69",   "ADV wild 29-31 + Pet 67-69 -> merged (rule 2)"),
    ("ghost crab",         "30-34",   "ADV Fished-Up 30-34"),
    ("grindylow",          "30-34",   "ADV Fished-Up 30-34"),
    ("eft",                "33-36",   "ADV 33-36"),
    ("goblin furrier",     "33-36",   "ADV 33-36"),
    ("goblin pathfinder",  "33-36",   "ADV 33-36"),
    ("goblin shaman",      "33-36",   "ADV 33-36"),
    ("goblin smithy",      "33-36",   "ADV 33-36"),
    ("marine dhalmel",     "34-37",   "ADV 34-37  (stored 33-37)"),
    ("island rarab",       "34-38",   "ADV 34-38"),
    ("ignis fatuus",       "35-37",   "ADV 35-37 fog weather"),
    ("greater pugil",      "35-39",   "ADV Fished-Up 35-39"),
    ("raven",              "36-38",   "ADV 36-38"),
    ("apsaras",            "40-42",   "ADV Fished-Up 40-42"),
    ("kraken",             "44-46",   "ADV Fished-Up 44-46"),
    # --- Adversaries, the 71-85 tier -------------------------------------
    ("tragopan",           "71-73",   "ADV 71-73"),
    ("hobgoblin martialist", "72-75", "ADV 72-75"),
    ("hobgoblin animalier",  "73-75", "ADV 73-75  (stored 72-75)"),
    ("hobgoblin fascinator", "73-75", "ADV 73-75  (stored 72-75)"),
    ("hobgoblin venerer",    "73-76", "ADV 73-76  (stored 72-76)"),
    ("tropical rarab",     "73-76",   "ADV 73-76"),
    ("teine sith",         "75-77",   "ADV 75-77 fog weather"),
    ("hobgoblin physician","76-78",   "ADV 76-78  (stored 76-79; NO lv)"),
    ("tartarus eft",       "76-78",   "ADV 76-78"),
    ("hobgoblin alastor",  "76-79",   "ADV 76-79  (NO lv)"),
    ("hobgoblin toreador", "76-79",   "ADV 76-79  (NO lv)"),
    ("catoblepas",         "76-80",   "ADV 76-80"),
    ("hobgoblin blagger",  "77-79",   "ADV 77-79  (NO lv)"),
    ("hobgoblin angler",   "80",      "ADV 80-80 -> '80'  (NO lv)"),
    ("bight rarab",        "80-83",   "ADV 80-83  (0 zones, NO lv)"),
    ("camelopard",         "80-85",   "ADV 80-85  (NO lv)"),
    # --- Adversaries, the 137-139 Locus tier ------------------------------
    ("locus ghost crab",   "137-139", "ADV Locus tier"),
    ("locus bight rarab",  "137-139", "ADV Locus tier  (stored 135-137)"),
    ("locus camelopard",   "137-139", "ADV Locus tier  (0 zones)"),
]

# rule 9 — unions, plus eight records where `lv` is ABSENT and the page publishes a
# band (LV_EXTEND creates it: `min(old[0], lo) if old else lo`). Creating a missing
# `lv` from a published value is additive, so rule 1 permits it.
LV_EXTEND = {
    "goblin's rarab":       (29, 69),    # was [29,54]; the Pet block reaches 69
    "hobgoblin martialist": (72, 75),    # was [72,74]
    "hobgoblin animalier":  (72, 75),    # was [72,74]
    "hobgoblin fascinator": (72, 75),    # was [72,74]
    "hobgoblin venerer":    (72, 76),    # was [72,74]
    "locus bight rarab":    (135, 139),  # was [135,137]
    "locus camelopard":     (135, 139),  # was [135,137]
    # --- created from the page (record had NO lv) -------------------------
    "locus fiddler crab":   (137, 139),
    "hobgoblin physician":  (76, 78),
    "hobgoblin alastor":    (76, 79),
    "hobgoblin toreador":   (76, 79),
    "hobgoblin blagger":    (77, 79),
    "hobgoblin angler":     (80, 80),
    "bight rarab":          (80, 83),
    "camelopard":           (80, 85),
}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # rule 4/12 — a ticketed boat service IS the access route to Purgonorgo Isle, but
    # the page gives the SELLER, not a boarding point, so it reads as a note rather
    # than a `travel` row (the rev-153 Domenic call).
    note = ("Tswe Panipahr at (H-7) sells tickets for the Manaclipper.")
    e.setdefault('notes', [])
    if note not in e['notes']:
        e['notes'].append(note)
        out.append("notes += Manaclipper ticket vendor (H-7)")
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
