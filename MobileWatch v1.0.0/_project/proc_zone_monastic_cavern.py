#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Monastic Cavern (rev 267). Engine = zonepass.py
MOBS ONLY — no zoneinfo_edit (rev-171 ruling). The info box publishes no Goblin
Footprint row and zoneinfo's `footprint` is "" — consistent, not a gap.

**THIS ZONE IS ONE OF THE TWO NAMED D3 CONFLICT CLUSTERS** from the rev-151
file-wide cross-check ("Monastic Cavern 4 — orcish farkiller/dreadnought/champion/
dragoon, zoneinfo spans far wider"). The page settles all four in zoneinfo's favour.

24 page records (11 NM + 13 Adversaries), 0 missing, bucket E empty.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Monastic Cavern"
SLUG = "monastic_cavern"

ROWS = [
    # --- Notorious Monsters ------------------------------------------------
    ("orcish hexspinner",  "72-74", "NM  Timed 20 min (J-7) — zone stored level-less; lv held its Vunkerl [S] band"),
    ("orcish overlord",    "75",    "NM  Timed 21-24 hr (J-7) — zone stored level-less"),
    ("orcish warlord",     "72-74", "NM  Timed 20 min (I-8)/(J-7) — zone stored level-less; lv held its La Vaule [S] band"),
    ("overlord bakgodek",  "85",    "NM  Lottery(Orcish Overlord) (J-7) — zone stored level-less"),
    ("bugaboo",            "63",    "NM  Quest(The Circle of Time), BLM, Ghost — zone stored level-less"),
    ("chillgaze foddrud",  SKIP,    "NM  Quest(An Understanding Overlord?), BLM — Lv BLANK"),
    ("grimbolt onkzok",    SKIP,    "NM  Quest(An Understanding Overlord?), RNG — Lv BLANK"),
    ("rictusgrin prakpok", SKIP,    "NM  Quest(An Understanding Overlord?), DRK — Lv BLANK"),
    ("sevenskewer krugglug", SKIP,  "NM  Quest(An Understanding Overlord?), DRG — Lv BLANK"),
    ("shatterskull mippdapp", SKIP, "NM  Quest(An Understanding Overlord?), MNK — Lv BLANK; ONLY La Vaule [S] before"),
    ("siegebreaker wujroj", SKIP,   "NM  Quest(An Understanding Overlord?), WAR — Lv BLANK"),
    # --- Adversaries --------------------------------------------------------
    ("orcish bowshooter",  "42-46", "ADV RNG, Davoi Chest Key"),
    ("orcish footsoldier", "43-47", "ADV WAR, Davoi Chest Key — stored 43-49 = Davoi 43-47 U Zvahl 47-49"),
    ("orcish gladiator",   "44-48", "ADV MNK, Davoi Chest Key"),
    ("orcish trooper",     "45-49", "ADV PLD, Davoi Chest Key"),
    ("orcish veteran",     "52-56", "ADV WAR"),
    ("orcish predator",    "53-57", "ADV RNG"),
    ("orcish zerker",      "54-58", "ADV DRK"),
    ("orcish warchief",    "55-59", "ADV PLD"),
    ("orcish farkiller",   "62-72", "ADV RNG, Davoi Coffer Key — D3 cluster, stored 69-71"),
    ("orcish dreadnought", "63-72", "ADV WAR, Davoi Coffer Key — D3 cluster, stored 69-72"),
    ("orcish champion",    "64-72", "ADV MNK, Davoi Coffer Key — D3 cluster, stored 69-72"),
    ("orcish dragoon",     "65-72", "ADV DRG, Davoi Coffer Key — D3 cluster, stored 69-72"),
    ("orcish protector",   "70-72", "ADV PLD"),
]

# rule 9 — the two NM fills land outside a `lv` that was holding another zone's band
LV_EXTEND = {
    "orcish hexspinner": (72, 74),   # [71,73] -> [71,74]
    "orcish warlord":    (72, 74),   # [79,81] -> [72,81]
}

run(ZONE, SLUG, ROWS, lv_extend=LV_EXTEND, write=wants_write())
