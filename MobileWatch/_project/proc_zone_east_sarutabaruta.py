#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: East Sarutabaruta (rev 158). Engine = zonepass.py
Run AFTER proc_paren_zonestrings.py and proc_zonestring_reconcile.py (rule 57).

Sources: 4 uploaded shots — (1) info box, (2) Notorious Monsters, (3)+(4) Adversaries.
First Mindartia zone of the sweep; every previous one was Quon.

30 page rows -> 28 distinct records:
  * `Magicked Bones` is TWO rows (an unjobbed one and a WAR one, both 3-8) -> one record
  * `Pug Pugil` is ground 4-8 AND Fished-Up 7-8 -> one record, merged span 4-8
    (the Fished-Up block sits INSIDE the ground range here, so the merge is a no-op —
    the stored 4-8 was already right)

THREE NARROWING CORRECTIONS, and zoneinfo had all four right before the page did:
  savanna rarab   1-6 -> 1-5   (its West Sarutabaruta entry is 1-5; the two now agree)
  yagudo acolyte  1-8 -> 3-8
  yagudo initiate 1-8 -> 3-8
  yagudo scribe   1-8 -> 3-8
"""
from zonepass import run, wants_write, SKIP

ZONE = "East Sarutabaruta"
SLUG = "east_sarutabaruta"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("duke decapod",       "8",     "NM  (0 zones before)"),
    ("spiny spipi",        "9-10",  "NM  Lottery(Crawler)"),
    ("sharp-eared ropipi", "10",    "NM  Lottery(Savanna Rarab)"),
    ("prickly pitriv",     "75",    "NM  UNM 200 accolades (0 zones before)"),
    ("rw nw prt m hrw",    SKIP,    "NM  Voidwatch — Lv cell BLANK"),
    # --- Adversaries (ground) --------------------------------------------
    ("bumblebee",          "1",     "ADV 1-1 -> '1'"),
    ("tiny mandragora",    "1",     "ADV 1-1 -> '1'"),
    ("savanna rarab",      "1-5",   "ADV 1-5  (stored 1-6)"),
    ("carrion crow",       "2-5",   "ADV 2-5"),
    ("river crab",         "2-6",   "ADV 2-6"),
    ("crawler",            "3-6",   "ADV 3-6  (0 zones before)"),
    ("mandragora",         "3-6",   "ADV 3-6"),
    ("goblin thug",        "3-8",   "ADV 3-8"),
    ("goblin weaver",      "3-8",   "ADV 3-8"),
    ("mad fox",            "3-8",   "ADV 3-8 undead"),
    ("magicked bones",     "3-8",   "ADV 3-8 undead (two rows = one record)"),
    ("yagudo acolyte",     "3-8",   "ADV 3-8  (stored 1-8)"),
    ("yagudo initiate",    "3-8",   "ADV 3-8  (stored 1-8)"),
    ("yagudo scribe",      "3-8",   "ADV 3-8  (stored 1-8)"),
    ("goblin fisher",      "4-8",   "ADV 4-8"),
    ("pug pugil",          "4-8",   "ADV ground 4-8 + Fished-Up 7-8 (rule 2, 7-8 sits inside)"),
    ("giant bee",          "5-8",   "ADV 5-8"),
    ("goblin digger",      "5-8",   "ADV 5-8"),
    ("balloon",            "8-10",  "ADV 8-10 fog weather"),
    # --- Adversaries (Fished Up) -----------------------------------------
    ("palm crab",          "2-4",   "ADV Fished-Up 2-4"),
    ("savanna crab",       "2-4",   "ADV Fished-Up 2-4"),
    ("mud pugil",          "5-6",   "ADV Fished-Up 5-6"),
    ("fighting pugil",     "9-10",  "ADV Fished-Up 9-10"),
]

# rule 9 — nothing to extend; all three corrections NARROW. Note the side effect:
# the Yagudo trio's `lv` min of 1 was almost certainly derived from the old 1-8
# entry, and after this correction NO zone of theirs starts below 3 (Giddeus 3-10,
# West Saruta 4-8, Tahrongi 8-10, West Saruta [S] 61-63). Rule 1 forbids shrinking
# `lv`, so the 1 stays as tracked (kz) debt rather than being quietly rewritten.
LV_EXTEND = {}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # the info box publishes NO Goblin Footprint row and zoneinfo's `footprint` is
    # already "" — consistent, not a gap (the rev-150 East Ronfaure precedent).
    # No footnote on this page, so nothing for `notes`.
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
