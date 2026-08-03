#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Buburimu Peninsula (rev 167). Engine = zonepass.py

Rule 57 clean — `Buburimu Peninsula` and `Dynamis-Buburimu` are both zones.json
names (the Bibiki/Purgonorgo shape again: two real zones, not two spellings).
Rule 65 applied: all 31 page names resolved against the file first try.

Sources: 4 shots — (1) info box, (2) Notorious Monsters, (3)+(4) Adversaries.

33 page rows -> 31 distinct records, 27 of them already exactly right.

TWO rule-2 merges, and BOTH were already stored correctly:
  snipper     ground 18-22 + Fished-Up 20-23 -> 18-23
  shoal pugil ground 24-28 + Fished-Up 24-26 -> 24-28  (the Fished block sits inside)
...except mobs.json had shoal pugil at the FISHED value 24-26 rather than the merge.

`Goblin Bounty Hunter`'s Lv cell reads `?-?` — rule 10's second spelling of no data.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Buburimu Peninsula"
SLUG = "buburimu_peninsula"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("helldiver",          "29-30", "NM  Lottery(Zu)"),
    ("buburimboo",         "30-31", "NM  Lottery(Shoal Pugil)"),
    ("abyssdiver",         "119",   "NM  UNM 1,500 accolades"),
    ("backoo",             SKIP,    "NM  Timed 50-60 min, daytime only — Lv BLANK (keeps 37)"),
    ("wake warder wanda",  SKIP,    "NM  Timed 1 hr — Lv BLANK (keeps 22-23)"),
    ("botulus rex",        SKIP,    "NM  Voidwatch — Lv BLANK"),
    # --- Adversaries (ground) --------------------------------------------
    ("goblin bounty hunter", SKIP,  "ADV Lv cell '?-?' (rule 10)"),
    ("mighty rarab",       "15-18", "ADV 15-18"),
    ("sylvestre",          "15-18", "ADV 15-18"),
    ("goblin ambusher",    "17-20", "ADV 17-20"),
    ("goblin butcher",     "17-20", "ADV 17-20"),
    ("goblin tinkerer",    "17-20", "ADV 17-20"),
    ("snipper",            "18-23", "ADV ground 18-22 + Fished-Up 20-23 (rule 2)"),
    ("zombie",             "18-22", "ADV 18-22 undead"),
    ("goblin digger",      "19-21", "ADV 19-21"),
    ("bull dhalmel",       "20-23", "ADV 20-23"),
    ("carnivorous crawler","20-23", "ADV 20-23"),
    ("zu",                 "20-23", "ADV 20-23"),
    ("ghoul",              "20-24", "ADV 20-24 undead"),
    ("poison leech",       "21-25", "ADV 21-25"),
    ("goblin gambler",     "22-25", "ADV 22-25"),
    ("goblin leecher",     "22-25", "ADV 22-25"),
    ("goblin mugger",      "22-25", "ADV 22-25"),
    ("bogy",               "23-25", "ADV 23-25 undead"),
    ("shoal pugil",        "24-28", "ADV ground 24-28 + Fished-Up 24-26 (rule 2; stored 24-26)"),
    ("will-o'-the-wisp",   "25-27", "ADV 25-27 fog weather"),
    ("air elemental",      "28-30", "ADV 28-30 weather-spawned"),
    ("water elemental",    "28-30", "ADV 28-30 weather-spawned"),
    # --- Adversaries (Fished Up) -----------------------------------------
    ("puffer pugil",       "15-18", "ADV Fished-Up 15-18"),
    ("stag crab",          "15-18", "ADV Fished-Up 15-18"),
    ("cutter",             "28-30", "ADV Fished-Up 28-30"),
]

# rule 9 — nothing to extend; every value sits inside its record's existing band.
LV_EXTEND = {}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # rule 12 — a traversal fact about reaching the Dynamis entrance, not a travel row
    note = ("The fastest way to reach the Dynamis-Buburimu entrance at (I-9) is to "
            "exit from Mhaura.")
    e.setdefault('notes', [])
    if note not in e['notes']:
        e['notes'].append(note)
        out.append("notes += fastest route to the Dynamis entrance (exit from Mhaura)")
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
