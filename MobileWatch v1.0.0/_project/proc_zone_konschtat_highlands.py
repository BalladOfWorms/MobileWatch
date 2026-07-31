#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Konschtat Highlands (rev 177). Engine = zonepass.py
Mobs only (rule 84/87) — no zoneinfo_edit is passed.

Rule 57 clean — `Konschtat Highlands` and `Abyssea-Konschtat` are both zones.json
names (two real zones, the Bibiki/Purgonorgo shape).
Rule 65 applied — all 43 names resolved against the FILE first try.
Rule 91 — zoneinfo publishes 17 nms[] + 26 mobs[] rows and the shots read 17 + 27
(Poltergeist is RDM + WAR, both 18-20, one record), so nothing was lost above the
top of shot 2 even though the NM table's header row is not in frame.

44 page rows -> 43 distinct records, 0 missing.
Lv-column leading zeros normalised on write: `07-10` -> `7-10`, `08-10` -> `8-10`.

The page's `Grenade` row is matched to **`grenade (monster)`** — the record that
holds all three zones and the full kit — which is also what zoneinfo names here
after the rev-171 rename. NOTE the user's naming rule inverts this pairing; when
the 23-pair swap runs, this row and the record both move together.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Konschtat Highlands"
SLUG = "konschtat_highlands"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("haty",                 "14",    "NM  Timed (Full Moon)"),
    ("bendigeit vran",       "14",    "NM  Timed (New Moon)"),
    ("stray mary",           "19-20", "NM  Lottery(Mad Sheep)"),
    ("rampaging ram",        "27-28", "NM  Lottery(Tremor Ram)"),
    ("goblin archaeologist", "30-75", "NM  Forced — zone stored level-less"),
    ("steelfleece baldarich","55-56", "NM  Lottery(Rampaging Ram, 21-24 hr)"),
    ("ghillie dhu",          SKIP,    "NM  TODO: spawn cell — Lv BLANK (0 zones before)"),
    ("highlander lizard",    "27-28", "NM  Timed 20-30 min"),
    ("forger",               "33",    "NM  Quest(Forge Your Destiny) — zone level-less"),
    ("sleepy mabel",         "99",    "NM  UNM 400 accolades — 0 zones AND no `lv` key"),
    ("gwynn ap nudd",        SKIP,    "NM  Voidwatch — Lv BLANK"),
    ("prickly sheep",        SKIP,    "NM  Voidwalker — Lv BLANK (not zoned here)"),
    ("void hare",            SKIP,    "NM  Voidwalker — Lv BLANK (not zoned here)"),
    ("chesma",               SKIP,    "NM  Voidwalker — Lv BLANK"),
    ("tammuz",               SKIP,    "NM  Voidwalker — Lv BLANK"),
    ("dawon",                SKIP,    "NM  Voidwalker — Lv BLANK (not zoned here)"),
    ("yilbegan",             SKIP,    "NM  Voidwalker — Lv BLANK (keeps 90-92, rule 15)"),
    # --- Adversaries ------------------------------------------------------
    ("huge wasp",            "7-10",  "ADV 07-10 -> 7-10"),
    ("strolling sapling",    "7-10",  "ADV 07-10 -> 7-10"),
    ("rock eater",           "7-11",  "ADV 07-11 -> 7-11"),
    ("amber quadav",         "8-10",  "ADV 08-10 BLM"),
    ("amethyst quadav",      "8-10",  "ADV 08-10 WHM"),
    ("goblin thug",          "8-10",  "ADV 08-10 THF"),
    ("goblin weaver",        "8-10",  "ADV 08-10 RDM"),
    ("wolf zombie",          "8-10",  "ADV 08-10 undead"),
    ("young quadav",         "8-10",  "ADV 08-10 WAR"),
    ("mist lizard",          "10-12", "ADV 10-12"),
    ("skeleton warrior",     "10-12", "ADV 10-12 WAR undead"),
    ("greater quadav",       "10-16", "ADV 10-16 DRK"),
    ("onyx quadav",          "10-16", "ADV 10-16 RDM"),
    ("veteran quadav",       "10-16", "ADV 10-16 PLD"),
    ("mad sheep",            "11-13", "ADV 11-13"),
    ("skeleton sorcerer",    "11-13", "ADV 11-13 BLM undead"),
    ("goblin digger",        "11-14", "ADV 11-14"),
    ("goblin ambusher",      "12-16", "ADV 12-16 RNG"),
    ("goblin butcher",       "12-16", "ADV 12-16 WAR"),
    ("goblin tinkerer",      "12-16", "ADV 12-16 DRK"),
    ("ghost",                "15-17", "ADV 15-17 undead"),
    ("grenade (monster)",    "15-17", "ADV 15-17 fog weather"),
    ("earth elemental",      "18-20", "ADV 18-20 weather-spawned  (rule 79 — 7th zone)"),
    ("poltergeist",          "18-20", "ADV RDM + WAR rows, both 18-20"),
    ("thunder elemental",    "18-20", "ADV 18-20 weather-spawned  (rule 79 — 7th zone)"),
    ("tremor ram",           "21-23", "ADV 21-23"),
]

# rule 9 / rule 73 — `sleepy mabel` has NO `lv` key at all and the page publishes 99,
# so the band is created from the page. (mi) 964 -> 963.
LV_EXTEND = {
    "sleepy mabel": (99, 99),
}

run(ZONE, SLUG, ROWS, LV_EXTEND, write=wants_write())
