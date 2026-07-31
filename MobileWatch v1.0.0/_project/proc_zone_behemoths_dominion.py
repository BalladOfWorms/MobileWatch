#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Behemoth's Dominion (rev 274). Engine = zonepass.py
MOBS ONLY. Zone string is `Behemoths Dominion` (no apostrophe) per zones.json.

RULE 2 merges: `Demonic Weapon` (WAR + RDM, both 45-46) and `Lost Soul` (WAR + BLM,
both 45-47) are two job rows each -> one record.

!! THE WHOLE NM BLOCK WAS ZONE-PRESENT AND LEVEL-LESS — all nine NMs carried the zone
with a null level. That is a distinct intake signature: something wrote `zones` here
without ever writing the level, unlike the usual "some rows missing" pattern.

17 page records (9 NM + 8 Adversaries), 0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Behemoths Dominion"
SLUG = "behemoths_dominion"

ROWS = [
    ("behemoth",           "80",  "NM  Forced (trade Beastly Shank to ???)"),
    ("king behemoth",      "85",  "NM  Forced (trade Savory Shank to ???)"),
    ("ancient weapon",     "66",  "NM  Mission(Zilart 5 - Headstone Pilgrimage), WAR"),
    ("doglix muttsnout",   "58",  "NM  Quest(The Talekeeper's Gift), WHM"),
    ("legendary weapon",   "65",  "NM  Mission(Zilart 5), RDM"),
    ("moxnix nightgoggle", SKIP,  "NM  Quest(The Talekeeper's Gift), RNG — Lv BLANK"),
    ("picklix longindex",  SKIP,  "NM  Quest(The Talekeeper's Gift), THF — Lv BLANK"),
    ("sovereign behemoth", "135", "NM  UNM 3,100 accolades, WAR/THF"),
    ("pil",                SKIP,  "NM  Voidwatch (White stratum abyssite III), Caturae — Lv BLANK (keeps 94-99)"),
    ("lesser gaylas",      "40-42", "ADV Flock Bat"),
    ("greater gayla",      "42-44", "ADV Bat"),
    ("demonic weapon",     "45-46", "ADV Evil Weapon — WAR + RDM rows, both 45-46"),
    ("lost soul",          "45-47", "ADV Skeleton — WAR + BLM rows, both 45-47"),
    ("master coeurl",      "45-50", "ADV Coeurl"),
    ("bhuta",              "46-48", "ADV Ghost"),
    ("light elemental",    "48-50", "ADV Elemental, light weather — the record had ZERO zones file-wide"),
    ("thunder elemental",  "48-50", "ADV Elemental, thunder weather — 0 entry here before"),
]

run(ZONE, SLUG, ROWS, write=wants_write())
