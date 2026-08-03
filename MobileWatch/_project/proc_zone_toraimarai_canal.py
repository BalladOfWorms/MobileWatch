#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Toraimarai Canal (rev 163). Engine = zonepass.py

Rule 57 clean — one Toraimarai string. Rule 65 applied: all 38 page names looked
up against the file, all resolved first try.

Sources: 5 shots — (1) info box, (2) NM table + start of Adversaries, (3)-(5) the rest.

43 page rows -> 38 distinct records. THREE rule-2 merges and one cross-table pair:
  bigclaw     ground 49-52 + Fished-Up 45-47 -> 45-52  (already stored correctly)
  bloodsucker ground 54-57 + Fished-Up 59-61 -> 54-61  <- the merge flagged at rev 155
  mousse      ground 63-65 + Fished-Up 65-67 -> 63-67
  hinge oil   appears in BOTH tables — NM row (65, Timed 16 min) and Adversaries
              row (65-65 WAR) -> one record, one entry, "65"

THE 94-99 BLOCK HAD ZERO ZONES — eight records. Fourth zone running where a
high-level tier bolted onto an older dungeon has no coverage at all (King
Ranperre's Locus block, Inner Horutoto 78-84, Outer Horutoto 81-85, now this).
"""
from zonepass import run, wants_write, SKIP

ZONE = "Toraimarai Canal"
SLUG = "toraimarai_canal"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("hinge oil",             "65",    "NM row 65 + ADV row 65-65 -> one record"),
    ("oni carcass",           "68-70", "NM  Timed 21-24 hr"),
    ("konjac",                "~78",   "NM  Lottery(Mousse) — page prints the tilde (0 zones before)"),
    ("brazen bones",          "81-89", "NM  Timed '?'  (0 zones before)"),
    ("canal moocher",         SKIP,    "NM  Lottery(Bouncing Ball) — Lv BLANK (0 zones before)"),
    ("magic sludge",          SKIP,    "NM  Quest: The Root of the Problem — Lv BLANK (0 zones before)"),
    # --- Adversaries, the 45-67 tier -------------------------------------
    ("canal bats",            "45-47", "ADV 45-47"),
    ("canal leech",           "45-47", "ADV Fished-Up 45-47"),
    ("bigclaw",               "45-52", "ADV ground 49-52 + Fished-Up 45-47 (rule 2)"),
    ("hell bat",              "47-49", "ADV 47-49"),
    ("makara",                "49-52", "ADV 49-52"),
    ("rock crab",             "52-54", "ADV Fished-Up 52-54"),
    ("fallen knight",         "52-55", "ADV 52-55"),
    ("dark aspic",            "53-55", "ADV 53-55"),
    ("bloodsucker (monster)", "54-61", "ADV ground 54-57 + Fished-Up 59-61 (rule 2; flagged at rev 155)"),
    ("lich",                  "54-57", "ADV 54-57"),
    ("girtab",                "58-60", "ADV 58-60  (drops Tor. Coffer Key)"),
    ("impish bats",           "58-60", "ADV 58-60  (drops Tor. Coffer Key)"),
    ("rotten sod",            "58-60", "ADV 58-60  (drops Tor. Coffer Key)"),
    ("fleshcraver",           "60-62", "ADV 60-62  (drops Tor. Coffer Key)"),
    ("mindcraver",            "60-62", "ADV 60-62  (drops Tor. Coffer Key)"),
    ("scavenger crab",        "60-62", "ADV 60-62  (drops Tor. Coffer Key)"),
    ("dire bat",              "62-64", "ADV 62-64  (drops Tor. Coffer Key)"),
    ("stygian pugil",         "63-65", "ADV 63-65  (drops Tor. Coffer Key)"),
    ("mousse",                "63-67", "ADV ground 63-65 + Fished-Up 65-67 (rule 2)"),
    ("bouncing ball",         "64-67", "ADV 64-67  (drops Tor. Coffer Key)"),
    ("doom mage",             "65-67", "ADV 65-67  (drops Tor. Coffer Key)"),
    ("doom soldier",          "65-67", "ADV 65-67  (drops Tor. Coffer Key)"),
    ("starmite",              "65-67", "ADV 65-67  (drops Tor. Coffer Key)"),
    # --- Adversaries, the 94-99 tier (all had ZERO zones) ----------------
    ("flume toad",            "94-96", "ADV high tier"),
    ("deviling bats",         "95-97", "ADV high tier"),
    ("starborer",             "95-97", "ADV high tier (fam=Wamouracampa vs page Genus Beetle — see rule 5)"),
    ("drowned bones",         "95-98", "ADV high tier (fam=None orphan; page Genus Skeleton)"),
    ("plunderer crab",        "95-98", "ADV high tier"),
    ("sodden bones",          "95-98", "ADV high tier (fam=None orphan; page Genus Skeleton)"),
    ("rapier scorpion",       "95-99", "ADV high tier"),
    ("blackwater pugil",      "96-98", "ADV high tier"),
    ("poroggo excavator",     "97-99", "ADV high tier"),
]

# rule 9 — brazen bones stores a single point where the page publishes a wide band.
# Every other addition sits inside its record's existing lv.
LV_EXTEND = {
    "brazen bones": (81, 89),   # was [85,85]
}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # rule 12 — both page notes are zone-level facts, not travel rows
    notes = [
        "The Goblin Footprint at (F-5) on Map 1 is reached from Inner Horutoto Ruins Map 4.",
        "Oni Carcass has moved to (E-9) on Map 1.",
    ]
    e.setdefault('notes', [])
    added = [n for n in notes if n not in e['notes']]
    e['notes'].extend(added)
    if added:
        out.append(f"notes += {len(added)} (footprint route from Inner Horutoto; Oni Carcass relocation)")
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
