#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Outer Horutoto Ruins (rev 161). Engine = zonepass.py

Rule 57 clean — only the two canonical Horutoto strings.

Sources: 8 shots — (1) info box, (2)+(3) Notorious Monsters, (3)-(8) Adversaries.
The largest page of the sweep: ~70 rows, 36 of them Cardians.

!! THE CARDIANS ARE STORED WITHOUT THE PAGE'S "(Monster)" SUFFIX.
The page names every numbered Cardian `Two of Batons (Monster)` — the suffix
disambiguates the mob from the card ITEM — but mobs.json keys them plainly
(`two of batons`), and zoneinfo's mobs[] rows do too. Building the lookup keys
from the page text reported all 36 as MISSING; they all exist and all already
carry this zone. Recorded so the next reader does not repeat it (rule 65).

ONE ADVERSARIES ROW IS UNREADABLE — it straddles the boundary between shots 7 and
8 (between `Fetor Bats` 81-83 and `Fuligo` 84-85; only its behaviour icons survive
in shot 8). It is NOT in this table and nothing was inferred for it.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Outer Horutoto Ruins"
SLUG = "outer_horutoto_ruins"

SUITS = ("batons", "coins", "cups", "swords")
# rank -> the page's level band for all four suits of that rank
CARDIAN_TIERS = [("two", "1-5"), ("three", "5-9"), ("four", "10-14"), ("five", "15-19"),
                 ("six", "20-24"), ("seven", "25-29"), ("eight", "30-34"),
                 ("nine", "35-39"), ("ten", "40-44")]

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("bomb king",         "16-18", "NM  Timed 8 min, shared spawn with both Doppelgangers"),
    ("doppelganger dio",  "23-25", "NM  shared spawn  (0 zones before)"),
    ("doppelganger gog",  "23-25", "NM  shared spawn  (0 zones before)"),
    ("desmodont",         "26-27", "NM  Lottery(Stink Bats)"),
    ("legalox heftyhind", "33",    "NM  Timed 10 min"),
    ("ah puch",           SKIP,    "NM  Lottery(BLM Ghoul) — Lv BLANK"),
    ("jack of batons",    SKIP,    "NM  Windurst Mission 6-1 — Lv BLANK (keeps 62)"),
    ("jack of coins",     SKIP,    "NM  Windurst Mission 6-1 — Lv BLANK (keeps 62)"),
    ("jack of cups",      SKIP,    "NM  Windurst Mission 6-1 — Lv BLANK (keeps 62)"),
    ("jack of swords",    SKIP,    "NM  Windurst Mission 6-1 — Lv BLANK (keeps 62)"),
    ("queen of coins",    SKIP,    "NM  Windurst Mission 8-2 — Lv BLANK (keeps 72)"),
    ("queen of swords",   SKIP,    "NM  Windurst Mission 8-2 — Lv BLANK (keeps 72)"),
    ("custom cardian",    SKIP,    "NM  Kupo Mission 6 — Lv BLANK (0 zones before)"),
    ("voidwrought",       SKIP,    "NM  Voidwatch — Lv BLANK (record has NO lv at all)"),
    # --- Adversaries, non-Cardian ----------------------------------------
    ("battue bats",       "1-5",   "ADV 1-5"),
    ("goblin thug",       "1-7",   "ADV 1-7"),
    ("goblin weaver",     "1-7",   "ADV 1-7"),
    ("blade bat",         "4-7",   "ADV 4-7"),
    ("balloon",           "8-10",  "ADV 8-10"),
    ("goblin ambusher",   "10-14", "ADV 10-14"),
    ("goblin butcher",    "10-14", "ADV 10-14"),
    ("goblin tinkerer",   "10-14", "ADV 10-14"),
    ("rotten jam",        "12-15", "ADV 12-15  (drops Hrt. Chest Key)"),
    ("stink bats",        "15-18", "ADV 15-18  (drops Hrt. Chest Key)"),
    ("combat",            "20-23", "ADV 20-23  (drops Hrt. Chest Key)"),
    ("black slime",       "23-25", "ADV 23-25"),
    ("ghoul",             "23-26", "ADV BLM + WAR rows, both 23-26"),
    ("dancing weapon",    "28-30", "ADV RDM + WAR rows, both 28-30"),
    ("thunder elemental", SKIP,    "ADV Strange Apparatus — Lv cell '?-?' (rule 10)"),
    ("fetor bats",        "81-83", "ADV high tier  (0 zones before)"),
    ("thorn bat",         "82-85", "ADV high tier  (0 zones before)"),
    ("fuligo",            "84-85", "ADV high tier"),
]
# the 36 numbered Cardians — four suits per rank, one band per rank
ROWS += [(f"{rank} of {suit}", lvl, f"ADV Cardian tier {rank} ({lvl})")
         for rank, lvl in CARDIAN_TIERS for suit in SUITS]

# rule 9 — the four `two of X` records store lv [1,4] to match their old 1-4 zone
# entry; the page (and zoneinfo) publish 1-5, so the band widens with the fix.
LV_EXTEND = {f"two of {suit}": (1, 5) for suit in SUITS}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # type Dungeon and footprint "H-5 (Map 1)" already match the info box; no footnote.
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
