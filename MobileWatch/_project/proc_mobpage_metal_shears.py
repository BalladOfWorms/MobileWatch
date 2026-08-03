#!/usr/bin/env python3
"""
MOB PAGE — Metal Shears (rev 176). Engine = zonepass.py, one row.

The Valkurm Dunes ZONE page publishes a BLANK Lv cell for this NM, so rev 175's
SKIP guard added the zone level-less. The mob's OWN page publishes **25-30** for
Valkurm Dunes — and the mob page beats the zone/summary table (the standing rule
in mobs-update's Conventions). So the level lands now.

In remit (rule 87): zone + level only. The page also publishes job Paladin,
crystal Water, weak Ice/Lightning, HP 700-800, immunities, susceptibilities,
a Spawns count of 1, the (J-6) spawn point and a 60-70 minute timer — NOT written.
The record already carries job/crys/det/drops/ab consistent with all of it.

rule 9: lv [22,22] -> [22,30]. The 22 has no donor anywhere — `metal shears` had
ZERO zones before rev 175, so nothing in the file ever sourced it (rule 78's
fourth shape, third zone running after aroma leech and marchelute).
"""
from zonepass import run, wants_write

ZONE = "Valkurm Dunes"
SLUG = "valkurm_dunes"

ROWS = [
    ("metal shears", "25-30", "MOB PAGE — zone page's Lv cell was blank"),
]

LV_EXTEND = {
    "metal shears": (25, 30),     # [22,22] -> [22,30]
}

run(ZONE, SLUG, ROWS, LV_EXTEND, write=wants_write())
