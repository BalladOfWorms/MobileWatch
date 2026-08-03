#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Giddeus (rev 162). Engine = zonepass.py

Rule 57 clean — one Giddeus string, matching zones.json.
Rule 65 applied: every page name was looked up against the FILE, not built from
page text. All 27 resolved on the first pass, no false misses.

Sources: 4 shots — (1) info box, (2) Notorious Monsters, (3)+(4) Adversaries.
The shot boundary between (3) and (4) splits the `Yagudo Priest` row across two
images but loses nothing — unlike Outer Horutoto last rev, no row is missing.

27 page rows -> 27 distinct records, and 24 were already exactly right. The three
gaps are all "record exists, this zone absent", not level errors.

NOTE for the Yagudo NM ladder: `Zhuu Buxu the Silent` appears here at 16 and its
record already carries the rev-157 merge (Giddeus 16 + Castle Oztroja [S], drops
Parana Shield + Sangoma Lappa) — the one-entry rule holding up a zone later.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Giddeus"
SLUG = "giddeus"

ROWS = [
    # --- Notorious Monsters (all Yagudo) ---------------------------------
    ("juu duzu the whirlwind",  "13",    "NM  Lottery(various Yagudo)"),
    ("eyy mon the ironbreaker", "16",    "NM  Timed 5 min"),
    ("zhuu buxu the silent",    "16",    "NM  Timed 5 min (rev-157 one-entry merge)"),
    ("hoo mjuu the torrent",    "16-17", "NM  Lottery(Yagudo Mendicant)"),
    ("vuu puqu the beguiler",   "21-22", "NM  Lottery(Yagudo Piper)"),
    ("vaa huja the erudite",    "45",    "NM  Quest: Dark Legacy  (0 zones before)"),
    ("quu xijo the illusory",   SKIP,    "NM  spawn cell reads 'TODO: ?' — Lv BLANK (0 zones before)"),
    # --- Adversaries (ground) --------------------------------------------
    ("giddeus bee",             "2-5",   "ADV 2-5"),
    ("giddeus pugil",           "2-5",   "ADV 2-5"),
    ("dirt eater",              "3-5",   "ADV 3-5"),
    ("yagudo acolyte",          "3-10",  "ADV 3-10"),
    ("yagudo initiate",         "3-10",  "ADV 3-10"),
    ("yagudo scribe",           "3-10",  "ADV 3-10"),
    ("yagudo's elemental",      "4-6",   "ADV 4-6  (0 zones before)"),
    ("giant pugil",             "9-11",  "ADV 9-11"),
    ("earth eater",             "10-12", "ADV 10-12"),
    ("digger wasp",             "11-13", "ADV 11-13"),
    ("yagudo mendicant",        "11-18", "ADV 11-18"),
    ("yagudo persecutor",       "11-18", "ADV 11-18"),
    ("yagudo piper",            "11-18", "ADV 11-18"),
    ("yagudo votary",           "22-26", "ADV 22-26  (drops Gds. Chest Key)"),
    ("yagudo priest",           "22-28", "ADV 22-28  (drops Gds. Chest Key)"),
    ("yagudo theologist",       "23-27", "ADV 23-27  (drops Gds. Chest Key)"),
    # --- Adversaries (Fished Up) -----------------------------------------
    ("pugil",                   "3-5",   "ADV Fished-Up 3-5"),
    ("pug pugil",               "8-10",  "ADV Fished-Up 8-10"),
    ("puffer pugil",            "13-15", "ADV Fished-Up 13-15"),
    ("land pugil",              "18-20", "ADV Fished-Up 18-20"),
]

# rule 9 — nothing to extend. Every added zone range sits inside its record's
# existing lv band (yagudo's elemental [4,79] vs 4-6; vaa huja [45,45] vs 45).
LV_EXTEND = {}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # The info box shows NO Goblin Footprint row and zoneinfo's `footprint` is already
    # "" — consistent (the rev-150 East Ronfaure precedent). No footnote to record.
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
