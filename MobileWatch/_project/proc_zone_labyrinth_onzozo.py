#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Labyrinth of Onzozo (rev 168). Engine = zonepass.py

Rule 57 clean — one Onzozo string. Rule 65 applied; all 33 names resolved first try.

Sources: 4 shots — (1) info box, (2) Notorious Monsters, (3)+(4) Adversaries.

35 page rows -> 33 distinct records, 26 already exactly right.

`Goblin's Leech` appears TWICE, both as Pet rows — 33-35 and 53-55 -> merged 33-55
(rule 2). Its stored value was **48-50, which matches NEITHER page block AND neither
of its other two zones** (Sanctuary of Zi'Tah 35-40, Gustav Tunnel 53-55) — a
rule-3-shaped error with no traceable source at all. See rule 78.

The info box's `Requires` cell is an expansion icon again (a blue disc), same as
Bibiki Bay and Purgonorgo Isle. Not legible enough to name -> nothing written,
rule 1 applied to an unreadable cell exactly as to a blank one.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Labyrinth of Onzozo"
SLUG = "labyrinth_of_onzozo"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("mysticmaker profblix", "50-52", "NM  Timed 2-2.5 hr"),
    ("ubume",                "60-65", "NM  Quest: Yomi Okuri  (0 zones before)"),
    ("peg powler",           "61",    "NM  Lottery(Flying Manta)  (stored 59-61)"),
    ("hellion",              "66",    "NM  Lottery(Tainted Flesh)"),
    ("soulstealer skullnix", "69-71", "NM  Lottery(Goblin Bandit)"),
    ("ose",                  "74-76", "NM  Lottery(Torama)"),
    ("lord of onzozo",       "74-77", "NM  Lottery(Flying Manta)"),
    ("narasimha",            "75-77", "NM  Lottery(Labyrinth Manticore)"),
    ("megapod megalops",     "80",    "NM  Quest: Bugi Soden"),
    ("voso",                 "122",   "NM  UNM 1,800 accolades"),
    # --- Adversaries -----------------------------------------------------
    ("goblin's leech",     "33-55", "ADV Pet 33-35 + Pet 53-55 -> merged (rule 2); stored 48-50"),
    ("labyrinth leech",    "45-48", "ADV 45-48"),
    ("goblin poacher",     "46-49", "ADV 46-49"),
    ("goblin reaper",      "46-49", "ADV 46-49"),
    ("goblin robber",      "46-49", "ADV 46-49"),
    ("goblin trader",      "46-49", "ADV 46-49"),
    ("cockatrice",         "50-53", "ADV 50-53  (drops Onzozo Chest Key)"),
    ("mushussu",           "51-57", "ADV 51-57  (drops Onzozo Chest Key)"),
    ("goblin bouncer",     "51-58", "ADV 51-58  (drops Onzozo Chest Key)"),
    ("goblin enchanter",   "51-58", "ADV 51-58  (drops Onzozo Chest Key)"),
    ("goblin hunter",      "51-58", "ADV 51-58  (drops Onzozo Chest Key)"),
    ("goblin miner",       "51-58", "ADV 51-58  (drops Onzozo Chest Key)"),
    ("flying manta",       "55-59", "ADV 55-59  (drops Onzozo Chest Key)"),
    ("air elemental",      "60-62", "ADV 60-62 weather-spawned  (0 entries here)"),
    ("water elemental",    "60-62", "ADV 60-62 weather-spawned  (0 entries here)"),
    ("tainted flesh",      "60-63", "ADV 60-63"),
    ("goblin alchemist",   "66-69", "ADV 66-69"),
    ("goblin bandit",      "66-69", "ADV 66-69"),
    ("goblin mercenary",   "66-69", "ADV 66-69"),
    ("goblin shepherd",    "66-69", "ADV 66-69"),
    ("torama",             "70-73", "ADV 70-73"),
    ("labyrinth manticore","71-74", "ADV 71-74"),
    ("wyvern",             "72-75", "ADV 72-75  (0 zones before)"),
]

# rule 9 — the merged Pet span reaches below the stored band.
# NOTE the `peg powler` side effect: single-zone mob, so narrowing 59-61 -> 61 strands
# its lv min of 59 (rule 76's shape again). Rule 1 forbids shrinking -> (kz).
LV_EXTEND = {
    "goblin's leech": (33, 55),   # was [35,55]
}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # No Goblin Footprint row on the page and zoneinfo's `footprint` is "" — consistent.
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
