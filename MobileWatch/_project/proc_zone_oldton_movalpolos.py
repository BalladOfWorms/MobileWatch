#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Oldton Movalpolos (rev 278). Engine = zonepass.py
MOBS ONLY — the info box's three travel footnotes (Geomagnetic Fount via Newton, the
Snow Lily -> Tarnotik teleport to Mine Shaft #2716, the Gusgen Survival Guide) are
read and NOT harvested.

RULE 2: `Goblin's Bat` is two blocks again — 28-31 (assists Goblin Leadman) and 36-37
(assists Goblin Tollman) -> **28-37**. zoneinfo already stores "28-31, 36-37".
That is the SECOND Movalpolos zone in two revs where this one record splits in two.

`goblin preceptor` gets its zone level (80) but **`lv` is deliberately NOT extended**:
the record stores lv [45,49] against nmlv "80" — the known (ls) disjoint class — and
unioning would invent a 45-80 band no zone supports. `nmlv` overrides `lv` in the UI
for NMs (rule 47), so the display is right either way.

38 page records (8 NM + 30 Adversaries), 0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Oldton Movalpolos"
SLUG = "oldton_movalpolos"

ROWS = [
    ("bugbear strongman",      "50-52", "NM  Lottery(Bugbear Bondman)"),
    ("goblin wolfman",         "50-55", "NM  Forced (trade Goblin Drink to Scrawled Writing)"),
    ("bugbear muscleman",      SKIP,    "NM  Timed (no interval published), MNK — Lv BLANK (keeps 52-53)"),
    ("bugallug",               "45-50", "NM  Quest(A Question of Faith), MNK — zone stored level-less"),
    ("bugbear porterman",      SKIP,    "NM  Quest(A Generous General?), MNK — Lv BLANK"),
    ("dread dealing dredodak", SKIP,    "NM  Quest(A Generous General?), DRK — Lv BLANK"),
    ("goblin preceptor",       "80",    "NM  Quest(A Generous General?), RDM — zone level-less; lv [45,49] vs nmlv 80 is (ls)"),
    ("grimoire guru grimogek", SKIP,    "NM  Quest(A Generous General?), BLM — Lv BLANK"),
    ("goblin's bat",   "28-37", "ADV Bat — RULE 2: 28-31 (assists Goblin Leadman) + 36-37 (assists Goblin Tollman)"),
    ("dark bats",      "31-35", "ADV Flock Bat"),
    ("goblin gutterman","33-36","ADV Goblin RNG"),
    ("goblin hammerman","33-36","ADV Goblin DRK"),
    ("goblin leadman", "33-36", "ADV Goblin BST"),
    ("moblin chapman", "33-36", "ADV Moblin BLM"),
    ("moblin pickman", "33-36", "ADV Moblin RDM"),
    ("moblin witchman","33-36", "ADV Moblin WHM"),
    ("stirge",         "33-36", "ADV Bat"),
    ("ancient bomb",   "40-45", "ADV Bomb, Oldton Chest Key"),
    ("moblin rodman",  "41-43", "ADV Moblin WAR, Oldton Chest Key"),
    ("goblin oilman",  "42-43", "ADV Goblin DRK, Oldton Chest Key"),
    ("goblin shovelman","42-43","ADV Goblin RNG, Oldton Chest Key"),
    ("goblin tollman", "42-43", "ADV Goblin BST, Oldton Chest Key"),
    ("moblin repairman","42-43","ADV Moblin THF, Oldton Chest Key"),
    ("bugbear bondman","42-45", "ADV Bugbear MNK, Oldton Chest Key (Bugbear Strongman PH)"),
    ("goblin doorman", "43-44", "ADV Goblin WAR, Oldton Chest Key"),
    ("moblin coalman", "43-44", "ADV Moblin BLM, Oldton Chest Key"),
    ("moblin gasman",  "43-44", "ADV Moblin WHM, Oldton Chest Key"),
    ("moblin pikeman", "43-44", "ADV Moblin RDM, Oldton Chest Key"),
    ("moblin ashman",  "45",    "ADV Moblin RDM, Oldton Chest Key — page reads 45-45"),
    ("goblin freelance","45-46","ADV Goblin WAR"),
    ("earth elemental","45-50", "ADV Elemental, earth weather, Chest Key — 0 Oldton entry before"),
    ("thunder elemental","45-50","ADV Elemental, thunder weather, Chest Key — 0 Oldton entry before"),
    ("moblin gurneyman","46-47","ADV Moblin RDM"),
    ("blind crab",     "20-24", "ADV Crab, Fished Up"),
    ("snipper",        "20-24", "ADV Crab, Fished Up"),
    ("cutter",         "25-29", "ADV Crab, Fished Up"),
    ("ghost crab",     "30-32", "ADV Crab, Fished Up — stored 25-29"),
    ("amoebic nodule", "34-36", "ADV Slime, Fished Up"),
]

run(ZONE, SLUG, ROWS, write=wants_write())
