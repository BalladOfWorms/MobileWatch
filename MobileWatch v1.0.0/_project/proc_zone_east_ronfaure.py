#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: East Ronfaure (rev 150). Data only; engine = zonepass.py

Sources: 5 uploaded shots of the BG-wiki zone page
  (1) info box, (2)+(3) Notorious Monsters, (3)+(4)+(5) Adversaries.

37 page rows -> 35 distinct records:
  * `Enchanted Bones` is TWO rows (BLM 4-8 and WAR 4-8)  -> one record  (South Gustaberg precedent)
  * `Pugil` is ground 1-5 AND Fished-Up 2-4              -> one record, merged span 1-5 (rule 2)
  * `Cheval Pugil` straddles the shot boundary           -> one row, not two
"""
from zonepass import run, wants_write, SKIP

ZONE = "East Ronfaure"
SLUG = "east_ronfaure"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("bigmouth billy",    "9-10",  "NM  Lottery(Carrion Worm)"),
    ("rambukk",           "12-15", "NM  Timed 15-60 min"),
    ("swamfisk",          "10-11", "NM  Lottery(Pugil)"),
    ("hugemaw harold",    "75",    "NM  UNM 200 accolades"),
    ("sarimanok",         SKIP,    "NM  Voidwatch — Lv cell BLANK"),
    ("quagmire pugil",    SKIP,    "NM  Voidwalker — Lv cell BLANK"),
    ("sunderclaw",        SKIP,    "NM  Voidwalker — Lv cell BLANK"),
    ("yacumama",          SKIP,    "NM  Voidwalker — Lv cell BLANK"),
    ("capricornus",       SKIP,    "NM  Voidwalker — Lv cell BLANK"),
    ("krabkatoa",         SKIP,    "NM  Voidwalker — Lv cell BLANK"),
    ("yilbegan",          SKIP,    "NM  Voidwalker — Lv cell BLANK (the rule-15 mob)"),
    # --- Adversaries (ground) --------------------------------------------
    ("tunnel worm",       "1",     "ADV 1-1 -> '1'"),
    ("wild rabbit",       "1",     "ADV 1-1 -> '1'"),
    ("carrion worm",      "1-5",   "ADV 1-5"),
    ("ding bats",         "1-5",   "ADV 1-5 nighttime"),
    ("forest hare",       "1-5",   "ADV 1-5"),
    ("pugil",             "1-5",   "ADV ground 1-5 + Fished-Up 2-4 (rule 2)"),
    ("forest funguar",    "3-6",   "ADV 3-6"),
    ("mouse bat",         "3-6",   "ADV 3-6 nighttime"),
    ("scarab beetle",     "3-6",   "ADV 3-6"),
    ("goblin fisher",     "3-8",   "ADV 3-8"),
    ("goblin thug",       "3-8",   "ADV 3-8"),
    ("orcish fodder",     "3-8",   "ADV 3-8"),
    ("orcish grappler",   "3-8",   "ADV 3-8"),
    ("orcish mesmerizer", "3-8",   "ADV 3-8"),
    ("enchanted bones",   "4-8",   "ADV 4-8 (BLM row + WAR row = one record)"),
    ("goblin weaver",     "4-8",   "ADV 4-8"),
    ("goblin digger",     "5-8",   "ADV 5-8"),
    ("tainted hound",     "5-8",   "ADV 5-8"),
    ("wild sheep",        "5-8",   "ADV 5-8"),
    ("bomb",              "8-10",  "ADV 8-10 fog weather"),
    # --- Adversaries (Fished Up) -----------------------------------------
    ("cheval pugil",      "2-4",   "ADV Fished-Up 2-4"),
    ("mud pugil",         "5-6",   "ADV Fished-Up 5-6"),
    ("pug pugil",         "7-8",   "ADV Fished-Up 7-8"),
    ("fighting pugil",    "8-10",  "ADV Fished-Up 8-10"),
]

LV_EXTEND = {
    # rule 9 — the fighting pugil correction drags the lv min down with it
    "fighting pugil": (8, 64),   # was [9,64]; page + zoneinfo both say 8-10
    # not a correction this pass, but the record's ONLY zone entry (2-4, already
    # matching the page) sits entirely outside its stored lv [9,10]. Union it and
    # flag the now-unsupported max as (kz) debt.
    "cheval pugil":   (2, 10),
}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # rule 12 — access requirement, not a travel row (the Voidwatch Warp row exists)
    note = ("Possession of Crimson stratum abyssite (Tier I or above) is required "
            "to unlock the Voidwatch Warp for this area.")
    e.setdefault('notes', [])
    if note not in e['notes']:
        e['notes'].append(note)
        out.append("notes += Crimson stratum abyssite (Tier I+) Voidwatch Warp requirement")
    # the only EMPTY drops string on the page's NM table (partial ones left alone)
    for row in e.get('nms', []):
        if row.get('n') == 'Hugemaw Harold' and not row.get('drops'):
            row['drops'] = ("Harold's Coffer, Harold's Ore, Setae Ring, "
                            "Megasco Earring, Indi-Frailty, Gain-MND")
            out.append("nms[Hugemaw Harold].drops filled")
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
