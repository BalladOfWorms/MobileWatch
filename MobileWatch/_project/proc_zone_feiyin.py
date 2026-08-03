#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Fei'Yin (rev 282). Engine = zonepass.py
MOBS ONLY. Zone string is `FeiYin` (no apostrophe) per zones.json.

RULE 2: `Shadow` is FOUR job rows (RNG/THF/WAR/BLM, all 44-46) and `Specter` is four
more (THF/BLM/WAR/RNG, all 55-58) — one record each.

!! THE STANDOUT: **the four compass-point Shadow NMs AND their placeholder had ZERO
zones between them.** Eastern / Northern / Southern / Western Shadow are all Lottery
pops off `Specter`, and none of the five records carried Fei'Yin at all. The same
shape one rung down: `goliath` and its placeholder `colossus` BOTH stored the zone
with a null level, exactly like Beaucedine's Gargantua/Stone Golem pair last rev.

33 page records (14 NM + 19 Adversaries), 0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "FeiYin"
SLUG = "feiyin"

ROWS = [
    ("capricious cassie",  "70",    "NM  Timed 2+ hr, WAR, Morbol"),
    ("eastern shadow",     "63",    "NM  Lottery(Specter) every 16-32 hr, RNG — 0 zones before"),
    ("goliath",            "62",    "NM  Lottery(Colossus), Golem — zone stored level-less"),
    ("northern shadow",    "63",    "NM  Lottery(Specter) every 16-30 hr, WAR — 0 zones before"),
    ("southern shadow",    "63",    "NM  Lottery(Specter) every 16-30 hr, BLM — 0 zones before"),
    ("western shadow",     "63",    "NM  Lottery(Specter) every 16-30 hr, THF — 0 zones before"),
    ("jenglot",            "73",    "NM  Timed 2 hr, WHM, Doll"),
    ("mind hoarder",       SKIP,    "NM  Lottery(Clockwork Pod), WAR, Magic Pot — Lv BLANK (keeps 61)"),
    ("sluagh",             "78-80", "NM  spawn cell reads '?', WAR, Ghost — 0 zones before; nmlv already 78-80"),
    ("altedour i tavnazia","65",    "NM  Quest(Pieuje's Decision), BLM, Fomor"),
    ("dabotz's ghost",     "53",    "NM  Quest(Scattered into Shadow), BLM — zone stored level-less"),
    ("miser murphy",       "62",    "NM  Quest(Peace for the Spirit), BLM/RDM — zone stored level-less"),
    ("borealis shadow",    "128",   "NM  UNM 2,400 accolades, Fomor"),
    ("carousing celine",   "128",   "NM  UNM 2,400 accolades, WAR, Morbol"),
    ("undead bats",        "38-40", "ADV Flock Bat"),
    ("revenant",           "40-42", "ADV Ghost"),
    ("vampire bat",        "40-42", "ADV Bat"),
    ("clockwork pod",      "41-43", "ADV Magic Pot (Mind Hoarder PH)"),
    ("drone",              "41-43", "ADV Doll"),
    ("ore golem",          "43-45", "ADV Golem, Fei'Yin Chest Key — zone stored level-less"),
    ("shadow",             "44-46", "ADV Fomor — RNG/THF/WAR/BLM rows, all 44-46, Fei'Yin Chest Key"),
    ("underworld bats",    "50-52", "ADV Flock Bat, Fei'Yin Chest Key"),
    ("camazotz",           "51-54", "ADV Bat"),
    ("talos",              "53-55", "ADV Doll"),
    ("droma",              "54-56", "ADV Magic Pot"),
    ("utukku",             "55-57", "ADV Ghost"),
    ("specter",            "55-58", "ADV Fomor — THF/BLM/WAR/RNG rows, all 55-58; PH for all four Shadow NMs — 0 zones before"),
    ("colossus",           "56-58", "ADV Golem — zone stored level-less (Goliath PH)"),
    ("dark elemental",     "56-58", "ADV Elemental, dark weather — 0 Fei'Yin entry before"),
    ("ice elemental",      "56-58", "ADV Elemental, ice weather — 0 Fei'Yin entry before"),
    ("killing weapon",     "59-61", "ADV Evil Weapon WAR"),
    ("hellish weapon",     "61-63", "ADV Evil Weapon RDM"),
    ("wekufe",             "95-99", "ADV Ghost BLM, 20 spawns — 0 zones before"),
]

LV_EXTEND = {
    "wekufe": (95, 99),   # [97,99] -> [95,99]
}

run(ZONE, SLUG, ROWS, lv_extend=LV_EXTEND, write=wants_write())
