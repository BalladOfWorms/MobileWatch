#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Gusgen Mines (rev 178). Engine = zonepass.py
Mobs only (rule 84/87) — no zoneinfo_edit is passed.

Rule 57 clean — `Gusgen Mines` is the only Gusgen string in zones.json.
Rule 65 applied — all 38 names resolved against the FILE first try.
Rule 91 — zoneinfo publishes 13 nms[] + 25 mobs[]; the shots read 13 + 27 rows,
and the two duplicate rows are the job pairs below, so 38 = 38. Nothing lost at
the shot 3/4 seam.

40 page rows -> 38 distinct records, 0 missing.
TWO rule-2 merges, both matching zoneinfo:
  Ghoul  WAR 20-24 + BLM 23-27 -> 20-27   (already stored correctly)
  Wight  BLM 29-33 + WAR 31-34 -> 29-34   (stored 30-33 — see below)

`wight`'s stored 30-33 matches NEITHER published block and NEITHER of its other
nine zone entries (26-36 x3, 28-30, 28-33, 32-35) — rule 78's donor-less shape,
so the page is taken as-is.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Gusgen Mines"
SLUG = "gusgen_mines"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    # The six Ghost ring-NMs already carry the page's band in `nmlv`; the ZONE
    # entry was level-less, which is what the per-zone row renders from.
    ("asphyxiated amsel",  "36-38", "NM  Random 0:00/1:00/2:00 after siren"),
    ("burned bergmann",    "36-41", "NM  Random 0:00/1:00/2:00 after siren"),
    ("crushed krause",     "36-38", "NM  Random 0:00/1:00/2:00 after siren"),
    ("pulverized pfeffer", "36-40", "NM  Random 0:00/1:00/2:00 after siren"),
    ("smothered schmidt",  "36-38", "NM  Random 0:00/1:00/2:00 after siren"),
    ("wounded wurfel",     "36-42", "NM  Random 0:00/1:00/2:00 after siren"),
    ("foul meat",          "43-45", "NM  Timed 24-36 hr"),
    ("juggler hecatomb",   "46-48", "NM  Timed 21-24 hr, RDM"),
    ("aroma fly",          "44-48", "NM  Forced (??? RSE week), WAR"),
    ("blind moby",         "25-26", "NM  Mission (Bastok 3-2), WAR"),
    ("pudding",            SKIP,    "NM  Quest(Eco-Warrior Bastok) — Lv BLANK"),
    ("wandering ghost",    "45",    "NM  Quest(Ghosts of the Past), WAR"),
    ("lorbulcrud",         SKIP,    "NM  Voidwatch — Lv BLANK"),
    # --- Adversaries ------------------------------------------------------
    ("skeleton warrior",   "15-17", "ADV 15-17 WAR"),
    ("fly agaric",         "20-23", "ADV 20-23"),
    ("ghoul",              "20-27", "ADV rule 2: WAR 20-24 + BLM 23-27"),
    ("bandersnatch",       "21-24", "ADV 21-24"),
    ("ore eater",          "23-26", "ADV 23-26"),
    ("wendigo",            "26-30", "ADV 26-30 WAR"),
    ("bogy",               "27-29", "ADV 27-29"),
    ("jelly",              "27-29", "ADV 27-29"),
    ("sadfly",             "27-30", "ADV 27-30"),
    ("amphisbaena",        "28-30", "ADV 28-30"),
    ("spunkie",            "28-30", "ADV 28-30"),
    ("mauthe doog",        "28-31", "ADV 28-31"),
    ("greater pugil",      "29-31", "ADV 29-31"),
    ("wight",              "29-34", "ADV rule 2: BLM 29-33 + WAR 31-34 (stored 30-33, no donor)"),
    ("myconid",            "30-32", "ADV 30-32"),
    ("banshee",            "31-34", "ADV 31-34"),
    ("rancid ooze",        "31-34", "ADV 31-34"),
    ("gallinipper",        "32-35", "ADV 32-35"),
    ("earth elemental",    "33-36", "ADV 33-36 weather-spawned  (rule 79 — 8th zone)"),
    ("ghast",              "33-36", "ADV 33-36 BLM"),
    ("thunder elemental",  "33-36", "ADV 33-36 weather-spawned  (rule 79 — 8th zone)"),
    ("feu follet",         "35-38", "ADV 35-38"),
    ("pirate pugil",       "20-22", "ADV Fished-Up 20-22"),
    ("ooze",               "30-32", "ADV Fished-Up 30-32"),
    ("mush",               "35-37", "ADV Fished-Up 35-37"),
]

# rule 9 — nothing to extend; every page level sits inside its record's band.
LV_EXTEND = {}

run(ZONE, SLUG, ROWS, LV_EXTEND, write=wants_write())
