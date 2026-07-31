#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Yughott Grotto (rev 156). Data only; engine = zonepass.py

Sources: 3 uploaded shots — (1) info box, (2) the single-row NM table + most of
Adversaries, (3) the last two Adversaries rows.

10 page rows -> 10 distinct records. No Fished-Up block, no row merges.
NINE of the ten were already exactly right; only the NM lacked a level.

!! THE NM RECORD IS A CONFLATION OF TWO DIFFERENT MOBS — see the handoff (ly).
`ashmaker gotblut` carries lv [17,83] and BOTH zones (Yughott Grotto + La Vaule [S]),
but its spawn/drops/sp all belong to the La Vaule [S] version:
    spawn "Lottery (Orcish Augur)"  vs this page's "Orcish Stonechucker or Orcish Grunt"
    drops "Marabout Sandals" (a lv 71 Rare) vs this page's "Hermit's Wand, Priest's Robe"
    sp    a 40-spell endgame kit (Flare/Freeze/Tornado/Quake/Aspir II/Sleepga II)
zoneinfo keeps the two apart correctly in yughott_grotto.nms and la_vaule_s.nms.
ONLY the zone level is written here — splitting the record is a create-records
decision and belongs to the user.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Yughott Grotto"
SLUG = "yughott_grotto"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("ashmaker gotblut",    "17-18", "NM  Lottery(Orcish Stonechucker/Orcish Grunt)"),
    # --- Adversaries -----------------------------------------------------
    ("grotto bats",         "8-11",  "ADV 8-11"),
    ("riding lizard",       "12-15", "ADV 12-15 (passive)"),
    ("orcish grunt",        "14-18", "ADV 14-18"),
    ("orcish neckchopper",  "14-18", "ADV 14-18"),
    ("orcish stonechucker", "14-18", "ADV 14-18"),
    ("stealth bat",         "15-18", "ADV 15-18"),
    ("orcish cursemaker",   "21-23", "ADV 21-23  (drops Ghelsba Chest Key)"),
    ("orcish fighter",      "21-23", "ADV 21-23  (drops Ghelsba Chest Key)"),
    ("orcish serjeant",     "21-23", "ADV 21-23  (drops Ghelsba Chest Key)"),
]

# rule 9 — nothing to extend. The fill makes lv's MIN of 17 supported for the first
# time; the MAX of 83 belongs to the La Vaule [S] mob and stays unsupported (kz debt),
# which is a symptom of the conflation, not of this write.
LV_EXTEND = {}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # type Dungeon, footprint D-9 and both travel rows already match the info box;
    # the page publishes no footnote, so there is nothing for notes.
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
