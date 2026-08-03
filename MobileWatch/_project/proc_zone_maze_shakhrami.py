#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Maze of Shakhrami (rev 169). Engine = zonepass.py

Rule 57 clean — one Shakhrami string. Rule 65 applied; all 42 names resolved.

Sources: 5 shots — (1) info box, (2)+(3) Notorious Monsters, (3)-(5) Adversaries.

44 page rows -> 42 distinct records, 34 already exactly right. `Wight` is two rows
(BLM + WAR, both 32-35) -> one record.

!! THE WEATHER CELL IS **NOT** "None" ON THIS PAGE — it shows element icons, and
zones.json backs that with ["Sunshine","Clouds","Dust Storm","Wind"]. So the rule-40
override is deliberately NOT written here. First zone of the sweep where the page
publishes real weather; the guard firing only on a literal "None" is what makes that
distinction survive.

!! `lost soul` vs `lost soul (nm)` is an (lx) pair pointing the WRONG WAY — see (mp).
The zone goes on the BASE record, which is the one zoneinfo resolves to and the one
carrying the page's own spawn string.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Maze of Shakhrami"
SLUG = "maze_of_shakhrami"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("ichorous ire",      "35-36", "NM  Quest: Blast from the Past"),
    ("leech king",        "35-36", "NM  Timed 1-2 hr, shared with Argus"),
    ("argus",             "36-37", "NM  Timed 1-2 hr, shared with Leech King"),
    ("aroma crawler",     "44-48", "NM  Forced (??? during your race's RSE week)"),
    ("ogbunabali",        "94-95", "NM  Voidwatch"),
    ("gloombound lurker", SKIP,    "NM  Lv BLANK (0 zones before)"),
    ("lesath",            SKIP,    "NM  Lv BLANK (keeps stored 44)"),
    ("trembler tabitha",  SKIP,    "NM  Lottery(Maze Maker) — Lv BLANK"),
    ("dark elemental",    SKIP,    "NM  failed Strange Apparatus — Lv BLANK (0 entries here)"),
    ("lost soul",         SKIP,    "NM  Quest: Equipped for All Occasions — Lv BLANK; see (mp)"),
    ("wyrmfly",           SKIP,    "NM  Quest: Eco-Warrior (Windurst) — Lv BLANK"),
    # --- Adversaries -----------------------------------------------------
    ("stink bats",        "15-18", "ADV 15-18"),
    ("goblin ambusher",   "16-18", "ADV 16-18"),
    ("goblin butcher",    "16-18", "ADV 16-18"),
    ("goblin tinkerer",   "16-18", "ADV 16-18"),
    ("maze maker",        "18-21", "ADV 18-21"),
    ("combat",            "20-23", "ADV 20-23"),
    ("carnivorous crawler","22-25","ADV 22-25"),
    ("ghoul",             "22-26", "ADV 22-26"),
    ("goblin gambler",    "22-26", "ADV 22-26"),
    ("goblin leecher",    "22-26", "ADV 22-26"),
    ("goblin mugger",     "22-26", "ADV 22-26"),
    ("seeker bats",       "23-26", "ADV 23-26"),
    ("goblin's bat",      "24-26", "ADV Pet, assists Goblin Pathfinder"),
    ("poison leech",      "24-28", "ADV 24-28"),
    ("wendigo",           "24-28", "ADV 24-28"),
    ("maze scorpion",     "25-28", "ADV 25-28"),
    ("jelly",             "26-28", "ADV 26-28"),
    ("ancient bat",       "26-29", "ADV 26-29"),
    ("abyss worm",        "27-30", "ADV 27-30  (drops Shk. Chest Key)"),
    ("caterchipillar",    "29-31", "ADV 29-31  (drops Shk. Chest Key)"),
    ("protozoan",         "29-31", "ADV 29-31  (drops Shk. Chest Key)"),
    ("labyrinth scorpion","30-33", "ADV 30-33  (drops Shk. Chest Key)"),
    ("goblin shaman",     "30-34", "ADV 30-34  (drops Shk. Chest Key)"),
    ("goblin furrier",    "31-34", "ADV 31-34  (drops Shk. Chest Key)"),
    ("goblin pathfinder", "31-34", "ADV 31-34  (drops Shk. Chest Key)"),
    ("goblin smithy",     "31-34", "ADV 31-34  (drops Shk. Chest Key)"),
    ("wight",             "32-35", "ADV BLM + WAR rows, both 32-35"),
    ("air elemental",     "33-36", "ADV 33-36 weather-spawned  (rule 79; 0 entries here)"),
    ("earth elemental",   "33-36", "ADV 33-36 weather-spawned  (rule 79; 0 zones at all)"),
    ("chaser bats",       "83-85", "ADV high tier  (0 zones before)"),
    ("crypterpillar",     "86-88", "ADV high tier"),
]

# rule 9 — nothing to extend; every added range sits inside its record's band.
LV_EXTEND = {}


def zoneinfo_edit(e):
    out = []
    # !! NO rule-40 weather override here. The page's Weather cell shows ELEMENT ICONS,
    # not "None", and zones.json backs it with ["Sunshine","Clouds","Dust Storm","Wind"].
    # Writing "None" would override a correct base with a wrong one — rule 40 in reverse.
    if e.get('weather'):
        out.append(f"weather override left as {e['weather']!r} (page does NOT say None)")
    # rule 12 / 43 — a SIXTH distinct abyssite value: Jade stratum, Tier II or above
    # (West Sarutabaruta is Jade Tier I+, so even the same stratum differs by zone).
    notes = [
        "Possession of Jade stratum abyssite (Tier II or above) is required to unlock "
        "the Voidwatch Warp for this area.",
        "The Voidwatch Warp does not place you inside the area — it brings you to the "
        "entrance.",
    ]
    e.setdefault('notes', [])
    added = [n for n in notes if n not in e['notes']]
    e['notes'].extend(added)
    if added:
        out.append(f"notes += {len(added)} (Jade stratum abyssite Tier II+; warp lands at the entrance)")
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
