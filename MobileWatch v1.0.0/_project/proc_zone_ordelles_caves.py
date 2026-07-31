#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Ordelle's Caves (rev 174). Engine = zonepass.py
Mobs only (rule 84/87) — no zoneinfo_edit is passed, so zoneinfo cannot be touched.

Rule 7 LIVE CASE: the page banner reads **Ordelle's Caves** (apostrophe) while
zones.json stores **`Ordelles Caves`** (none). The zones.json form is what gets
written; the engine aborts on anything else.

Rule 57 clean — `Ordelles Caves` is the only Ordelle string in zones.json.
Rule 65 applied — every page name was looked up in the FILE. `Gerwitz's Axe (NM)`
and `Gerwitz's Sword (NM)` carry the page's own `(NM)` suffix; the file keys them
bare, and both resolved after the strip. 52/52 resolved.

52 page rows (12 NM + 40 Adversaries) -> 52 distinct records, 0 missing.
43 already carried the zone; nothing carries the zone that is NOT on the page.

SHOT BOUNDARIES: the six shots overlap rather than skip — the half-row at the foot
of shot 2 is Polevik itself (its name's top pixel row, x70-102, reappears at shot 3
y14 as x72-104 with an identical 9-pixel count), and the boundaries at shots 3/4 and
4/5 split Fly Agaric's and Goliath Beetle's icon blocks. No row was lost.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Ordelles Caves"      # rule 7 — NOT the banner's "Ordelle's Caves"
SLUG = "ordelles_caves"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("bombast",           "42-44", "NM  Timed 90 min          (0 zones before)"),
    ("morbolger",         "42-44", "NM  Timed 1-2 hr"),
    ("aroma leech",       "38",    "NM  Forced (??? RSE week) — lv [44,48] excludes 38"),
    ("donggu",            SKIP,    "NM  Lottery(Fly Agaric) — Lv BLANK (0 zones before)"),
    ("agar agar",         SKIP,    "NM  TODO: spawn cell     — Lv BLANK (0 zones before)"),
    ("gerwitz's axe",     "50",    "NM  Quest(Dark Puppet)   — page name has '(NM)'"),
    ("gerwitz's sword",   "52",    "NM  Quest(Dark Puppet)   — page name has '(NM)'"),
    ("gerwitz's soul",    "54",    "NM  Quest(Dark Puppet)   — zone stored level-less"),
    ("metallic slime",    SKIP,    "NM  Quest(Blighted Gloom) — Lv BLANK"),
    ("necroplasm",        SKIP,    "NM  Quest(Eco-Warrior)   — Lv BLANK (keeps 37)"),
    ("polevik",           SKIP,    "NM  Quest(Sharpening the Sword) — Lv BLANK (0 zones)"),
    ("krabimanjaro",      SKIP,    "NM  Voidwatch            — Lv BLANK"),
    # --- Adversaries ------------------------------------------------------
    ("stink bats",        "15-18", "ADV 15-18"),
    ("blood bunny",       "17-19", "ADV 17-19"),
    ("goblin ambusher",   "17-20", "ADV 17-20 RNG"),
    ("goblin butcher",    "17-20", "ADV 17-20 WAR"),
    ("goblin tinkerer",   "17-20", "ADV 17-20 DRK"),
    ("hognosed bat",      "17-20", "ADV 17-20"),
    ("snipper",           "17-20", "ADV 17-20"),
    ("stalking sapling",  "18-21", "ADV 18-21"),
    ("thread leech",      "18-21", "ADV 18-21"),
    ("fly agaric",        "21-24", "ADV 21-24"),
    ("goblin gambler",    "22-26", "ADV 22-26 BLM"),
    ("goblin leecher",    "22-26", "ADV 22-26 WHM"),
    ("goblin mugger",     "22-26", "ADV 22-26 THF"),
    ("will-o'-the-wisp",  "23-25", "ADV 23-25"),
    ("dung beetle",       "23-26", "ADV 23-26"),
    ("seeker bats",       "23-26", "ADV 23-26"),
    ("vorpal bunny",      "23-26", "ADV 23-26"),
    ("goblin's bats",     "24-26", "ADV 24-26 Pet"),
    ("shrieker",          "24-27", "ADV 24-27  (stored 24-33 = its own global lv)"),
    ("poison leech",      "25-27", "ADV 25-27"),
    ("ancient bat",       "26-28", "ADV 26-28"),
    ("jelly",             "26-28", "ADV 26-28"),
    ("clipper",           "26-29", "ADV 26-29"),
    ("slash pine",        "27-29", "ADV 27-29"),
    ("goliath beetle",    "29-31", "ADV 29-31"),
    ("napalm",            "31-33", "ADV 31-33"),
    ("goblin furrier",    "31-34", "ADV 31-34 RNG"),
    ("goblin pathfinder", "31-34", "ADV 31-34 BST"),
    ("goblin shaman",     "31-34", "ADV 31-34 BLM"),
    ("goblin smithy",     "31-34", "ADV 31-34 WAR"),
    ("stroper",           "31-34", "ADV 31-34"),
    ("stroper chyme",     "33-35", "ADV 33-35"),
    ("air elemental",     "33-36", "ADV 33-36 weather-spawned  (rule 79 — 5th zone)"),
    ("water elemental",   "33-36", "ADV 33-36 weather-spawned  (rule 79 — 5th zone)"),
    ("targe beetle",      "84-85", "ADV 84-85 high tier  (0 zones before)"),
    ("buds bunny",        "84-86", "ADV 84-86 high tier  (0 zones before)"),
    ("swagger spruce",    "86-88", "ADV 86-88 high tier  (stored 83-89 = its own global lv)"),
    ("bilis leech",       "86-89", "ADV 86-89 high tier  (0 zones before)"),
    ("stag crab",         "15-17", "ADV Fished-Up 15-17"),
    ("rancid ooze",       "34-36", "ADV Fished-Up 34-36"),
]

# rule 9 — the only page level outside its record's band. Every other row on the
# page sits inside the stored `lv`, and no record here is missing `lv` (so (mi)
# stays at 964 for this zone).
LV_EXTEND = {
    "aroma leech": (38, 48),      # [44,48] -> [38,48]; the page's 38 is its only zone
}

run(ZONE, SLUG, ROWS, LV_EXTEND, write=wants_write())
