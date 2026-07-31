#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Qulun Dome (rev 182). Engine = zonepass.py
Mobs only (rule 84/87) — no zoneinfo_edit is passed.

**THE FIRST ZONE OF THE SWEEP WITH NOTHING TO WRITE.** 0 missing, 0 zone adds,
0 level fills, 0 corrections, 0 lv unions. Run dry — no --write needed, and the
report below is the deliverable.

Rule 57 clean — `Qulun Dome` is the only Qulun string in zones.json and it has no
`[S]` twin, so rule 98's prefix hazard does not apply here.
Rule 65 applied — all 14 names resolved first try.
Rule 91 — zoneinfo publishes 11 nms[] + 4 mobs[]; the shots read 11 + 4, and the
11 NM rows collapse to 10 records because `Diamond Quadav` appears twice (the
Timed 21-24 hr spawn at 75 and the *An Affable Adamantking?* quest row, Lv blank).

15 page rows -> 14 distinct records, ALL 14 already exactly right.

WHY THIS PAGE IS CLEAN — see rule 102. It carries none of the five known gap
categories: no weather elementals (rule 79), no retail-era high-level tier
(rule 70), no Fished-Up block, no Voidwalker/Voidwatch NMs, no two-block spawns
(rule 100). It is a single-family Quadav dungeon whose content has not moved
since it shipped.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Qulun Dome"
SLUG = "qulun_dome"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("adaman quadav",       "72-74", "NM  Timed 20 min, DRK"),
    ("ruby quadav",         "71-73", "NM  Timed 20 min, RDM"),
    ("diamond quadav",      "75",    "NM  Timed 21-24 hr, WHM (+ a 2nd quest row, Lv blank)"),
    ("za'dha adamantking",  "85",    "NM  Lottery(Diamond Quadav) every 2-7 Earth days, WHM"),
    ("de'pha unscarred",    SKIP,    "NM  Quest(An Affable Adamantking?), WAR — Lv BLANK"),
    ("hu'rhe marrowgorger", SKIP,    "NM  Quest(An Affable Adamantking?), DRK — Lv BLANK"),
    ("ka'ghi trovetaker",   SKIP,    "NM  Quest(An Affable Adamantking?), THF — Lv BLANK"),
    ("mu'zha infernoblade", SKIP,    "NM  Quest(An Affable Adamantking?), RDM — Lv BLANK"),
    ("no'bhu unyielding",   SKIP,    "NM  Quest(An Affable Adamantking?), PLD — Lv BLANK"),
    ("so'hyu quakemaker",   SKIP,    "NM  Quest(An Affable Adamantking?), BLM — Lv BLANK"),
    # --- Adversaries ------------------------------------------------------
    ("ancient quadav",      "69-72", "ADV 69-72 WAR, 3 spawns"),
    ("darksteel quadav",    "69-72", "ADV 69-72 PLD, 4 spawns"),
    ("platinum quadav",     "69-72", "ADV 69-72 THF, 3 spawns"),
    ("sapphire quadav",     "69-72", "ADV 69-72 BLM, 5 spawns"),
]

LV_EXTEND = {}

run(ZONE, SLUG, ROWS, LV_EXTEND, write=wants_write())
