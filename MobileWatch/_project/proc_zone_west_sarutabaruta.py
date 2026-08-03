#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: West Sarutabaruta (rev 159). Engine = zonepass.py

Rule 57 run first and came back CLEAN this time — only the three canonical
Sarutabaruta strings remain after rev 158's file-wide reconciliation.

Sources: 4 shots — (1) info box, (2) Notorious Monsters, (3)+(4) Adversaries.

34 page rows -> 33 distinct records. `Magicked Bones` is TWO rows with DIFFERENT
levels this time — WAR 4-8 and DRK 5-8 -> merged span 4-8 (rule 2; 5-8 sits
inside, so the stored value was already right).

SEVEN of the ten NM rows publish no level: Virvatuli (Voidwatch) and the five
Voidwalkers plus Numbing Norman's bare "Timed:" — rule 42's cluster, now with the
rev-134 "a bare Timed: with no interval is an incomplete wiki field" shape too.
"""
from zonepass import run, wants_write, SKIP

ZONE = "West Sarutabaruta"
SLUG = "west_sarutabaruta"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("tom tit tat",     "9-10", "NM  Lottery(Mandragora)"),
    ("nunyenunc",       "12",   "NM  Lottery(Carrion Crow)  (stored 10-12)"),
    ("numbing norman",  SKIP,   "NM  bare 'Timed:' with no interval — Lv BLANK (0 zones)"),
    ("virvatuli",       SKIP,   "NM  Voidwatch — Lv BLANK"),
    ("rummager beetle", SKIP,   "NM  Voidwalker — Lv BLANK"),
    ("raker bee",       SKIP,   "NM  Voidwalker — Lv BLANK"),
    ("farruca fly",     SKIP,   "NM  Voidwalker — Lv BLANK"),
    ("jyeshtha",        SKIP,   "NM  Voidwalker — Lv BLANK (keeps stored 82)"),
    ("orcus",           SKIP,   "NM  Voidwalker — Lv BLANK"),
    ("yilbegan",        SKIP,   "NM  Voidwalker — Lv BLANK (keeps 90-92; the rule-15 mob)"),
    # --- Adversaries (ground) --------------------------------------------
    ("bumblebee",       "1",    "ADV 1-1 -> '1'"),
    ("tiny mandragora", "1",    "ADV 1-1 -> '1'"),
    ("river crab",      "1-3",  "ADV 1-3"),
    ("savanna rarab",   "1-5",  "ADV 1-5"),
    ("carrion crow",    "2-6",  "ADV 2-6"),
    ("goblin fisher",   "3-4",  "ADV 3-4"),
    ("mandragora",      "3-5",  "ADV 3-5  (stored 3-6)"),
    ("goblin thug",     "3-6",  "ADV 3-6  (stored 4-8)"),
    ("goblin weaver",   "3-6",  "ADV 3-6"),
    ("crawler",         "3-8",  "ADV 3-8"),
    ("mad fox",         "4-6",  "ADV 4-6 undead"),
    ("magicked bones",  "4-8",  "ADV WAR 4-8 + DRK 5-8 -> merged 4-8 (rule 2)"),
    ("yagudo acolyte",  "4-8",  "ADV 4-8"),
    ("yagudo initiate", "4-8",  "ADV 4-8"),
    ("yagudo scribe",   "4-8",  "ADV 4-8"),
    ("giant bee",       "5-8",  "ADV 5-8"),
    ("goblin digger",   "5-8",  "ADV 5-8"),
    ("balloon",         "8-10", "ADV 8-10 fog weather"),
    # --- Adversaries (Fished Up) -----------------------------------------
    ("palm crab",       "2-4",  "ADV Fished-Up 2-4"),
    ("savanna crab",    "2-4",  "ADV Fished-Up 2-4"),
    ("land crab",       "5-6",  "ADV Fished-Up 5-6"),
    ("mugger crab",     "7-8",  "ADV Fished-Up 7-8"),
    ("passage crab",    "9-10", "ADV Fished-Up 9-10"),
]

# rule 9 — nothing to extend; all three corrections NARROW.
#   mandragora  3-6 -> 3-5 : lv [3,6] max still backed by East Sarutabaruta 3-6
#   goblin thug 4-8 -> 3-6 : lv [1,10] fully backed by its other 13 zones
#   nunyenunc   10-12 -> 12: SINGLE-zone mob, so lv [10,12] loses ALL support for
#                            its min of 10 -> tracked (kz) debt, not a silent shrink
LV_EXTEND = {}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # rule 12 / 43 — a FIFTH distinct Voidwatch abyssite value (Jade, Tier I+)
    note = ("Possession of Jade stratum abyssite (Tier I or above) is required to "
            "unlock the Voidwatch Warp for this area.")
    e.setdefault('notes', [])
    if note not in e['notes']:
        e['notes'].append(note)
        out.append("notes += Jade stratum abyssite (Tier I+) Voidwatch Warp requirement")
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
