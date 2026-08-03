#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Garlaige Citadel (rev 270). Engine = zonepass.py

RULE 2 merges (job-pair rows -> one record): Fallen Evacuee (WAR+BLM, 42-43),
Demonic Weapon (RDM+WAR, 47-49), Fallen Soldier (WAR+BLM, 47-49), Fallen Officer
(WAR+BLM, 52-55).

RULE 98: `Garlaige Citadel` is a prefix of `Garlaige Citadel [S]` (explosure carries
both). Matched by exact string.

!! NAME CHECK — the page row reads **Frogamander**, not "Frogmander". The name cell
segments into ELEVEN letter blobs with the wide `m` blob sixth
(F-r-o-g-a-**m**-a-n-d-e-r); "Frogmander" would put `m` fifth of ten. mobs.json and
zoneinfo both already spell it Frogamander. No rename.

43 page records (10 NM + 33 Adversaries), 0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Garlaige Citadel"
SLUG = "garlaige_citadel"

ROWS = [
    # --- Notorious Monsters ------------------------------------------------
    ("frogamander",     SKIP,    "NM  Timed 2 hr — page prints the point value 72; record AND its own nmlv both say 71-73, so the richer range is KEPT (the wurdalak/emperor-arthro precedent)"),
    ("old two-wings",   "52",    "NM  Timed 21-24 hr, Bat"),
    ("serket",          "70",    "NM  Timed 21-24 hr, WAR, Scorpion"),
    ("skewer sam",      "54",    "NM  Timed 21-24 hr, Cockatrice"),
    ("hazmat",          "58-60", "NM  Lottery(Explosure), BLM, Bomb"),
    ("hovering hotpot", "58-60", "NM  Lottery(Fallen Major/Fallen Mage), DRK, Magic Pot"),
    ("chandelier",      "63",    "NM  Quest(Hitting the Marquisate), Bomb — zone stored level-less"),
    ("guardian statue", "61",    "NM  Quest(Peace for the Spirit), Doll"),
    ("mephitas",        "125",   "NM  UNM 2,100 accolades, THF, Scorpion"),
    ("roly-poly",       SKIP,    "NM  Voidwatch (White stratum abyssite II), Flan — Lv BLANK, 0 zones before"),
    # --- Adversaries --------------------------------------------------------
    ("wingrats",        "40-42", "ADV Flock Bat"),
    ("siege bat",       "40-43", "ADV Bat"),
    ("borer beetle",    "41-44", "ADV Beetle — stored 40-44 while its own lv floor is 41 (rule 104)"),
    ("fallen evacuee",  "42-43", "ADV Skeleton — WAR + BLM rows, both 42-43"),
    ("oil spill",       "43-45", "ADV Slime"),
    ("puroboros",       "43-45", "ADV Bomb"),
    ("clockwork pod",   "44-45", "ADV Magic Pot"),
    ("revenant",        "44-46", "ADV Ghost"),
    ("citadel bats",    "46-48", "ADV Flock Bat"),
    ("bhuta",           "47-49", "ADV Ghost"),
    ("demonic weapon",  "47-49", "ADV Evil Weapon — RDM + WAR rows, both 47-49"),
    ("fallen soldier",  "47-49", "ADV Skeleton — WAR + BLM rows, both 47-49"),
    ("funnel bats",     "51-55", "ADV Flock Bat, Garlaige Chest Key"),
    ("explosure",       "52-53", "ADV Bomb, Chest Key (Hazmat PH)"),
    ("acid grease",     "52-54", "ADV Slime, Chest Key"),
    ("droma",           "52-54", "ADV Magic Pot, Chest Key"),
    ("earth elemental", "52-54", "ADV Elemental, earth weather, Chest Key — 0 Garlaige entry before"),
    ("thunder elemental","52-54","ADV Elemental, thunder weather, Chest Key — 0 Garlaige entry before"),
    ("fallen officer",  "52-55", "ADV Skeleton — WAR + BLM rows, both 52-55, Chest Key"),
    ("fetid flesh",     "54-56", "ADV Doomed, Chest Key"),
    ("chamber beetle",  "56-58", "ADV Beetle"),
    ("fallen mage",     "59-62", "ADV Skeleton BLM, Coffer Key (Hovering Hotpot PH)"),
    ("fallen major",    "59-62", "ADV Skeleton WAR, Coffer Key (Hovering Hotpot PH)"),
    ("hellmine",        "59-62", "ADV Bomb, Coffer Key"),
    ("over weapon",     "59-62", "ADV Evil Weapon WAR, Coffer Key"),
    ("vault weapon",    "59-62", "ADV Evil Weapon RDM, Coffer Key"),
    ("wraith",          "60-62", "ADV Ghost WAR, Coffer Key, 8 spawns"),
    ("magic jug",       "62-64", "ADV Magic Pot RDM, Coffer Key, 6 spawns"),
    ("tainted flesh",   "63-65", "ADV Doomed, Coffer Key, 4 spawns"),
    ("donjon bat",      "91-96", "ADV Bat WAR, 18 spawns — 0 zones before"),
    ("kaboom",          "91-96", "ADV Bomb WAR, 10 spawns — 0 zones before; fam=None ORPHAN"),
    ("fortalice bats",  "92-96", "ADV Flock Bat WAR, 26 spawns — 0 zones before"),
    ("warden beetle",   "95-98", "ADV Beetle PLD, 18 spawns — 0 zones before"),
]

LV_EXTEND = {
    "warden beetle": (95, 98),   # [92,96] -> [92,98]
}

run(ZONE, SLUG, ROWS, lv_extend=LV_EXTEND, write=wants_write())
