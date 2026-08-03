#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Ghelsba Outpost (rev 153). Data only; engine = zonepass.py

Sources: 4 uploaded shots — (1) info box, (2) the full Notorious Monsters table,
(3)+(4) the Adversaries table.

27 page rows -> 27 distinct records. No row merges this time: the ground Pugil of
this zone is `Ghelsba Pugil` (3-6) and the plain `Pugil` appears ONLY as a
Fished-Up row (03-05), so they are two separate records, not one merge.

LEADING ZEROS THROUGHOUT the Adversaries Lv column (01-05, 03-05, 04-06, 07-09,
08-10) — normalized on write, the Palborough Mines convention. `14-14` -> "14"
and `16-16` -> "16" (the 1-1 / 60-60 collapse).

TWO RULE-3 ERRORS, both involving the ADJACENT zone Fort Ghelsba:
  pug pugil    stored 6-8  == its Fort Ghelsba entry exactly -> page says 7-9
  cheiroptera  stored 3-10 == the UNION of Ghelsba Outpost (3-6, per the page)
               and Fort Ghelsba (8-10) collapsed into ONE entry, i.e. the
               record's GLOBAL lv band written into a per-zone slot -> 3-6
Both were already correct in zoneinfo.json's mobs[] (rule 46's good half).
`spectacled bats` is the control: Ghelsba 1-5 + Fort Ghelsba 6-8, lv [1,8],
all three consistent — the same zone pair handled correctly.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Ghelsba Outpost"
SLUG = "ghelsba_outpost"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("thousandarm deshglesh", "11-13", "NM  Lottery(various Orcs)"),
    ("orcish wallbreacher",   "15-16", "NM  Timed 60-90 min"),
    ("orcish barricader",     "17-18", "NM  Timed 60-90 min"),
    ("bloody vrukwuk",        "14",    "NM  14-14 -> '14'; alternates with Fogweaver Mozzfuzz"),
    ("fogweaver mozzfuzz",    "14",    "NM  14-14 -> '14'; alternates with Bloody Vrukwuk"),
    ("warchief vatgit",       "16",    "NM  16-16 -> '16'; Timed 16 min"),
    ("carrion dragon",        SKIP,    "NM  Quest Mirror, Mirror — Lv cell BLANK"),
    ("cyranuce m cutauleon",  SKIP,    "NM  Quest The Holy Crest — Lv cell BLANK (0 zones)"),
    ("fodderchief vokdek",    SKIP,    "NM  Mission Save the Children — Lv cell BLANK"),
    ("strongarm zodvad",      SKIP,    "NM  Mission Save the Children — Lv cell BLANK"),
    ("sureshot snatgat",      SKIP,    "NM  Mission Save the Children — Lv cell BLANK"),
    # --- Adversaries (ground) --------------------------------------------
    ("spectacled bats",       "1-5",   "ADV 01-05 nighttime"),
    ("watch lizard",          "3-5",   "ADV 03-05"),
    ("cheiroptera",           "3-6",   "ADV 03-06  (rule-3: stored 3-10 was the global lv band)"),
    ("ghelsba pugil",         "3-6",   "ADV 03-06"),
    ("orcish fodder",         "3-9",   "ADV 03-09"),
    ("orcish grappler",       "3-9",   "ADV 03-09"),
    ("orcish mesmerizer",     "3-9",   "ADV 03-09"),
    ("toadstool",             "4-6",   "ADV 04-06"),
    ("orcish stonelauncher",  "8-10",  "ADV 08-10"),
    ("orcish grunt",          "11-15", "ADV 11-15"),
    ("orcish neckchopper",    "11-15", "ADV 11-15"),
    ("orcish stonechucker",   "11-15", "ADV 11-15"),
    # --- Adversaries (Fished Up) -----------------------------------------
    ("pugil",                 "3-5",   "ADV Fished-Up 03-05"),
    ("pug pugil",             "7-9",   "ADV Fished-Up 07-09  (rule-3 copy of Fort Ghelsba 6-8)"),
    ("giant pugil",           "11-13", "ADV Fished-Up 11-13"),
    ("puffer pugil",          "15-17", "ADV Fished-Up 15-17"),
]

# rule 9 — no unions needed, and both corrections IMPROVE lv support:
#   cheiroptera lv [3,10] is now exactly Ghelsba 3-6 + Fort Ghelsba 8-10
#   pug pugil   lv [4,64]: the new 9 sits inside it; min 4 backed by East Sarutabaruta
LV_EXTEND = {}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # rule 12 — travel ADVICE and an access gate, not zone geometry, so notes not travel.
    # (rule 4 fires for a portal/passage; a teleport NPC with no published coord is not one.)
    notes = [
        "Domenic will only teleport you here after completing Beyond Infinity.",
        "The Fort Ghelsba Survival Guide is a good quick-travel alternative.",
        "You can also Home Point to Yughott Grotto and cast Escape — it leaves you at "
        "the Ghelsba Outpost entrance from West Ronfaure.",
    ]
    e.setdefault('notes', [])
    for n in notes:
        if n not in e['notes']:
            e['notes'].append(n)
    if notes:
        out.append(f"notes += {len(notes)} (Domenic gate, Fort Ghelsba guide, Yughott/Escape route)")
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
