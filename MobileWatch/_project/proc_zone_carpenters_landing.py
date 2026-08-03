#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Carpenters' Landing (rev 185). Engine = zonepass.py
Mobs only. Rule 7: banner `Carpenters' Landing` -> zones.json `Carpenters Landing`.
Rule 91: zoneinfo 10 nms[] + 37 mobs[] vs shots 10 + 39 = 47 after the Ghoul and
Water Elemental pairs.

49 page rows -> 47 distinct records. ONE MISSING RECORD — `Crab Shell` — created
below from the page row alone (name / Genus / Lv / Fished-Up / behaviour icons).
First creation of the whole sweep.

Rule 2: Water Elemental 24-26 + 36-38 -> 24-38.
"""
import json, os
from zonepass import run, wants_write, SKIP, ASSETS

ZONE = "Carpenters Landing"
SLUG = "carpenters_landing"

# ---- the missing record, straight off the Adversaries row -------------------
def create_crab_shell():
    p = os.path.join(ASSETS, 'mobs.json')
    m = json.load(open(p, encoding='utf-8'))
    if 'crab shell' in m['mobs']:
        print("crab shell: already present, nothing to create")
        return
    m['mobs']['crab shell'] = {
        "n": "Crab Shell",
        "fam": "Crab",          # page Genus column
        "lv": [20, 24],         # page Lv column
        "agg": True,            # red Aggressive glyph
        "det": ["Sound"],       # red speaker glyph
        "zones": [[ZONE, "20-24"]],
    }
    json.dump(m, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"crab shell: CREATED (mobs {len(m['mobs'])-1} -> {len(m['mobs'])})")

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("hercules beetle",       "34",    "NM  Forced (trade Honey 22:00-4:00), DRK"),
    ("mycophile",             "30-35", "NM  Forced (trade 3 shrooms), DRK"),
    ("orctrap",               "37-39", "NM  Lottery(Birdtrap), WAR"),
    ("tempest tigon",         "43",    "NM  Timed 1-2 hr, WAR  (0 zones before)"),
    ("bullheaded grosvez",    SKIP,    "NM  Quest(Behind the Smile), MNK — Lv BLANK"),
    ("cryptonberry assassin", SKIP,    "NM  Mission(Promathia 7-4) — Lv BLANK"),
    ("cryptonberry executor", SKIP,    "NM  Mission(Promathia 7-4), NIN — Lv BLANK"),
    ("overgrown ivy",         SKIP,    "NM  Mission(Promathia 3-3), WAR — Lv BLANK (0 zones)"),
    ("para",                  SKIP,    "NM  Quest(Elderly Pursuits), WAR — Lv BLANK"),
    ("orcfeltrap",            "119",   "NM  UNM 1,500 accolades — 0 zones AND no `lv` key"),
    # --- Adversaries ------------------------------------------------------
    ("digger wasp",           "14-17", "ADV 14-17"),
    ("beady beetle",          "15-18", "ADV 15-18"),
    ("bulldog bats",          "15-20", "ADV 15-20 nighttime"),
    ("specter bat",           "15-20", "ADV 15-20 nighttime"),
    ("poison funguar",        "16-19", "ADV 16-19"),
    ("orcish grunt",          "16-20", "ADV 16-20 DRG"),
    ("orcish neckchopper",    "16-20", "ADV 16-20 DRK"),
    ("orcish stonechucker",   "16-20", "ADV 16-20 RNG"),
    ("land pugil",            "17-19", "ADV 17-19"),
    ("flytrap",               "18-22", "ADV 18-22"),
    ("spider wasp",           "19-22", "ADV 19-22"),
    ("glide bomb",            "20-21", "ADV 20-21 WAR, fog weather, 1 spawn"),
    ("stag beetle",           "20-23", "ADV 20-23"),
    ("marsh funguar",         "20-24", "ADV 20-24"),
    ("orcish cursemaker",     "21-25", "ADV 21-25 BLM"),
    ("orcish fighter",        "21-25", "ADV 21-25 WAR"),
    ("orcish serjeant",       "21-25", "ADV 21-25 PLD"),
    ("ghoul",                 "21-27", "ADV BLM + WAR rows, both 21-27"),
    ("fosse pugil",           "22-24", "ADV 22-24"),
    ("forest tiger",          "22-25", "ADV 22-25"),
    ("battrap",               "23-27", "ADV 23-27"),
    ("thunder elemental",     "24-26", "ADV 24-26 weather-spawned  (rule 79 — 14th zone)"),
    ("water elemental",       "24-38", "ADV rule 2: 24-26 + 36-38  (rule 79 — 14th zone)"),
    ("will-o'-the-wisp",      "25-26", "ADV 25-26 DRK, fog weather, 2 spawns"),
    ("diving beetle",         "27-30", "ADV 27-30"),
    ("shrieker",              "28-31", "ADV 28-31"),
    ("wendigo",               "28-33", "ADV 28-33 WAR undead"),
    ("wight",                 "28-33", "ADV 28-33 BLM undead"),
    ("spinous pugil",         "29-31", "ADV 29-31"),
    ("sabertooth tiger",      "29-32", "ADV 29-32"),
    ("birdtrap",              "29-33", "ADV 29-33"),
    ("spunkie",               "32-33", "ADV 32-33 WAR, fog weather"),
    ("snipper",               "15-19", "ADV Fished-Up 15-19"),
    ("triangle crab",         "15-19", "ADV Fished-Up 15-19"),
    ("crab shell",            "20-24", "ADV Fished-Up 20-24  — RECORD CREATED THIS REV"),
    ("fishtrap",              "25-27", "ADV Fished-Up 25-27"),
    ("greater pugil",         "29-31", "ADV Fished-Up 29-31"),
]

LV_EXTEND = {
    "orcfeltrap": (119, 119),     # no `lv` key at all — created from the page
}

if wants_write():
    create_crab_shell()
run(ZONE, SLUG, ROWS, LV_EXTEND, write=wants_write())
