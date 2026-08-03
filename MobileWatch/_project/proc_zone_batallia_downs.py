#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Batallia Downs (rev 184). Engine = zonepass.py
Mobs only (rule 84/87) — no zoneinfo_edit is passed.

RULE 98 again: `Batallia Downs` is a prefix of `Batallia Downs [S]`, and 15
records carry BOTH. [S] entries re-checked after the write.
Rule 65 applied — all 62 names resolved first try.
Rule 91 — zoneinfo publishes 27 nms[] + 35 mobs[]; the shots read 27 + 38, which
is 27 + 35 after the two job pairs (Wight WAR/BLM 26-36, Evil Weapon RDM/WAR
36-38) and `Sobbing Sapling`, which zoneinfo files under nms[] only. The seam
between shots 6 and 7 loses nothing — the adversary list matches row for row.

65 page rows -> 62 distinct records, 0 missing.

`Sobbing Sapling` is the FOURTH cross-table mob of the sweep (after King
Ranperre's `Spook`, Toraimarai's `Hinge Oil` and Bibiki's pattern): NM row 36-38
AND Adversaries row 36-38 -> one record, one zone entry.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Batallia Downs"
SLUG = "batallia_downs"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("ahtu",               "51-52", "NM  Timed 2-4 hr — zone stored level-less"),
    ("lumber jack",        "55",    "NM  Defeat(Weeping Willow), DRK"),
    ("suparna",            SKIP,    "NM  Mission(San d'Oria 9-1) — Lv BLANK (0 zones)"),
    ("suparna fledgling",  SKIP,    "NM  Assists Suparna, WHM — Lv BLANK (0 zones)"),
    ("weeping willow",     "45",    "NM  Timed 21-24 hr, WAR"),
    ("sobbing sapling",    "36-38", "NM + ADV — the same mob on both tables"),
    ("tottering toby",     "27-28", "NM  Lottery(Stalking Sapling), WAR"),
    ("eyegouger",          SKIP,    "NM  TODO: spawn cell — Lv BLANK (keeps ~46)"),
    ("prankster maverix",  SKIP,    "NM  TODO: spawn cell — Lv BLANK (keeps 51)"),
    ("skirling liger",     SKIP,    "NM  TODO: spawn cell — Lv BLANK (0 zones)"),
    ("badshah",            SKIP,    "NM  Quest(A Chocobo's Tale), WAR — Lv BLANK (0 zones)"),
    ("sturmtiger",         "52",    "NM  Quest(Chasing Quotas), WAR  (0 zones before)"),
    ("vegnix greenthumb",  SKIP,    "NM  Mission(Crystalline 3), WAR — Lv BLANK (0 zones)"),
    ("lumber jill",        "125",   "NM  UNM 2,100 accolades"),
    ("cherufe",            SKIP,    "NM  Voidwatch — Lv BLANK (keeps 93-94)"),
    ("aither",             SKIP,    "NM  Voidwalker Elemental — Lv BLANK (2nd zone ever)"),
    ("deorc",              SKIP,    "NM  Voidwalker Elemental — Lv BLANK (2nd zone ever)"),
    ("eorthe",             SKIP,    "NM  Voidwalker Elemental — Lv BLANK (2nd zone ever)"),
    ("puretos",            SKIP,    "NM  Voidwalker Elemental — Lv BLANK (2nd zone ever)"),
    ("pruina",             SKIP,    "NM  Voidwalker Elemental — Lv BLANK (2nd zone ever)"),
    ("beorht",             SKIP,    "NM  Voidwalker Elemental — Lv BLANK (2nd zone ever)"),
    ("thunor",             SKIP,    "NM  Voidwalker Elemental — Lv BLANK (2nd zone ever)"),
    ("lacus",              SKIP,    "NM  Voidwalker Elemental — Lv BLANK (2nd zone ever)"),
    ("urd",                SKIP,    "NM  Voidwalker Pixie, DNC — Lv BLANK"),
    ("skuld",              SKIP,    "NM  Voidwalker Pixie — Lv BLANK"),
    ("verthandi",          SKIP,    "NM  Voidwalker Pixie — Lv BLANK"),
    ("yilbegan",           SKIP,    "NM  Voidwalker — Lv BLANK (keeps 90-92)"),
    # --- Adversaries ------------------------------------------------------
    ("goblin bounty hunter", SKIP,  "ADV Lv reads `?-?` — rule 10"),
    ("stalking sapling",   "20-24", "ADV 20-24"),
    ("may fly",            "22-26", "ADV 22-26"),
    ("clipper",            "23-25", "ADV 23-25"),
    ("goblin's dragonfly", "23-25", "ADV 23-25"),
    ("ba",                 "25-28", "ADV 25-28"),
    ("goblin gambler",     "26-30", "ADV 26-30 BLM"),
    ("goblin leecher",     "26-30", "ADV 26-30 WHM"),
    ("goblin mugger",      "26-30", "ADV 26-30 THF"),
    ("orcish cursemaker",  "26-30", "ADV 26-30 BLM"),
    ("orcish fighter",     "26-30", "ADV 26-30 WAR"),
    ("orcish serjeant",    "26-30", "ADV 26-30 PLD"),
    ("wight",              "26-36", "ADV WAR + BLM rows, both 26-36"),
    ("goblin digger",      "28-32", "ADV 28-32"),
    ("mauthe doog",        "28-32", "ADV 28-32 undead"),
    ("sabertooth tiger",   "28-32", "ADV 28-32"),
    ("goblin furrier",     "28-36", "ADV 28-36 RNG"),
    ("goblin pathfinder",  "28-36", "ADV 28-36 BST"),
    ("goblin shaman",      "28-36", "ADV 28-36 BLM"),
    ("goblin smithy",      "28-36", "ADV 28-36 WAR"),
    ("orcish beastrider",  "30-36", "ADV 30-36 DRK"),
    ("orcish brawler",     "30-36", "ADV 30-36 MNK"),
    ("orcish impaler",     "30-36", "ADV 30-36 DRG"),
    ("orcish nightraider", "30-36", "ADV 30-36 RNG"),
    ("ignis fatuus",       "34-36", "ADV 34-36 DRK, fog weather, 4 spawns"),
    ("treant",             "35-37", "ADV 35-37"),
    ("evil spirit",        "35-38", "ADV 35-38 undead"),
    ("evil weapon",        "36-38", "ADV RDM + WAR rows, both 36-38"),
    ("earth elemental",    "38-40", "ADV 38-40 weather-spawned  (rule 79 — 13th zone)"),
    ("ice elemental",      "38-40", "ADV 38-40 weather-spawned  (rule 79; 0 zones anywhere)"),
    ("land pugil",         "20-23", "ADV Fished-Up 20-23"),
    ("snipper",            "20-23", "ADV Fished-Up 20-23 — zone stored level-less"),
    ("cutter",             "28-30", "ADV Fished-Up 28-30"),
    ("dagon",              "33-35", "ADV Fished-Up 33-35 — record has NO `lv` key"),
    ("kraken",             "38-40", "ADV Fished-Up 38-40"),
]

# rule 9 / rule 73 — `dagon` already carried the zone at the right level but has
# no `lv` key at all; the band is created from the page. (mi) 963 -> 962.
LV_EXTEND = {
    "dagon": (33, 35),
}

run(ZONE, SLUG, ROWS, LV_EXTEND, write=wants_write())
