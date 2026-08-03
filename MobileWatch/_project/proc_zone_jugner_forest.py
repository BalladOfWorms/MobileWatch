#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Jugner Forest (rev 266). Engine = zonepass.py
MOBS ONLY — no zoneinfo_edit (rev-171 ruling). The info-box footnote (Crimson
stratum abyssite Tier III unlocks the Voidwatch Warp) is NOT harvested here.

RULE 91 reconciled: zoneinfo publishes 18 nms[] + 37 mobs[]; the shots read 18 + 38,
which is 18 + 37 after `Boggart`'s two job rows (RDM + WAR, both 25-27). The NM
table's top edge is cut in the shot but loses nothing — 18 rows both sides.

RULE 98: `Jugner Forest` is a strict prefix of `Jugner Forest [S]`, and 17 of these
records carry BOTH. Matched by exact string; [S] entries re-verified after the write.

55 page records, 0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Jugner Forest"
SLUG = "jugner_forest"

ROWS = [
    # --- Notorious Monsters ------------------------------------------------
    ("fradubio",            "58-60", "NM  Lottery(Fraelissa) — stored 55-60 = its own lv (rule 49); nmlv already 58-60"),
    ("fraelissa",           "33-35", "NM  Timed ~1 hr"),
    ("giollemitte b feroun", SKIP,   "NM  Quest(A Timely Visit), PLD — Lv BLANK, 0 zones before"),
    ("skeleton esquire",    SKIP,    "NM  Quest(A Timely Visit), DRK — Lv BLANK (zone held, stays level-less)"),
    ("king arthro",         "55",    "NM  Timed 21-24 hrs"),
    ("meteormauler zhagtegg","35-40","NM  Timed ~21 hrs — zone stored level-less"),
    ("panzer percival",     "25-26", "NM  Lottery(Stag Beetle)"),
    ("sappy sycamore",      "~43",   "NM  Timed 60-70 min, WAR — tilde verbatim (arioch/thoon precedent), 0 zones before"),
    ("supplespine mujwuj",  SKIP,    "NM  Lottery(Orcish Grunt), DRG — Lv BLANK, 0 zones before"),
    ("cernunnos",           SKIP,    "NM  Mission(WotG 10), BLM/WHM — Lv BLANK, 0 zones before"),
    ("emperor arthro",      SKIP,    "NM  UNM 1,800 accolades — page prints 122, record holds 99; RULE 48 false positive (nmlv '99 (CL 122)'), left alone"),
    ("belphoebe",           SKIP,    "NM  Voidwatch (Crimson stratum abyssite III) — Lv BLANK (rule 42)"),
    ("quagmire pugil",      SKIP,    "NM  Voidwalker (Clear abyssite) — Lv BLANK (rule 42)"),
    ("sunderclaw",          SKIP,    "NM  Voidwalker (Clear abyssite) — Lv BLANK (rule 42)"),
    ("yacumama",            SKIP,    "NM  Voidwalker (Colorful abyssite), MNK/WAR — Lv BLANK (rule 42)"),
    ("capricornus",         SKIP,    "NM  Voidwalker (Colorful abyssite), WAR — Lv BLANK (rule 42)"),
    ("krabkatoa",           SKIP,    "NM  Voidwalker (Blue abyssite), PLD/WAR — Lv BLANK (keeps 90)"),
    ("yilbegan",            SKIP,    "NM  Voidwalker (Black abyssite) — Lv BLANK (keeps 90-92; the rule-15 mob)"),
    # --- Adversaries --------------------------------------------------------
    ("wandering sapling",   "13-16", "ADV Sapling"),
    ("screamer",            "15-18", "ADV Lesser Bird"),
    ("goblin ambusher",     "16-20", "ADV Goblin RNG"),
    ("goblin butcher",      "16-20", "ADV Goblin WAR"),
    ("goblin tinkerer",     "16-20", "ADV Goblin DRK"),
    ("orcish grunt",        "16-20", "ADV Orc DRG (Supplespine Mujwuj PH)"),
    ("orcish neckchopper",  "16-20", "ADV Orc DRK"),
    ("orcish stonechucker", "16-20", "ADV Orc RNG"),
    ("ghoul",               "16-26", "ADV Skeleton BLM, undead 20:00-4:00"),
    ("zombie",              "16-26", "ADV Skeleton BLM, undead 20:00-4:00"),
    ("spring pugil",        "16-18", "ADV Pugil, Fished Up"),
    ("stag crab",           "16-18", "ADV Crab, Fished Up"),
    ("land pugil",          "17-20", "ADV Pugil"),
    ("snipper",             "17-20", "ADV Crab"),
    ("brutal sheep",        "18-21", "ADV Sheep — stored 18-23 = Jugner 18-21 U Valkurm 20-23 (rule-49 shape)"),
    ("goblin digger",       "18-21", "ADV Goblin"),
    ("scavenging hound",    "18-25", "ADV Hound"),
    ("forest leech",        "19-22", "ADV Leech"),
    ("thread leech",        "19-22", "ADV Leech, Fished Up"),
    ("stag beetle",         "20-23", "ADV Beetle (Panzer Percival PH)"),
    ("goblin gambler",      "21-25", "ADV Goblin BLM"),
    ("goblin leecher",      "21-25", "ADV Goblin WHM"),
    ("goblin mugger",       "21-25", "ADV Goblin THF"),
    ("jugner funguar",      "21-25", "ADV Funguar"),
    ("orcish cursemaker",   "21-25", "ADV Orc BLM"),
    ("orcish fighter",      "21-25", "ADV Orc WAR"),
    ("orcish serjeant",     "21-25", "ADV Orc PLD"),
    ("forest tiger",        "22-25", "ADV Tiger"),
    ("will-o'-the-wisp",    "24-25", "ADV Bomb, fog weather (usually 2:00-7:00)"),
    ("ferocious pugil",     "24-25", "ADV Pugil, Fished Up"),
    ("boggart",             "25-27", "ADV Evil Weapon — RDM + WAR rows, both 25-27 (rule 2)"),
    ("walking tree",        "25-28", "ADV Treant"),
    ("bogy",                "25-29", "ADV Ghost, undead 20:00-4:00"),
    ("thunder elemental",   "27-29", "ADV Elemental, thunder weather — 0 Jugner entry before"),
    ("water elemental",     "27-29", "ADV Elemental, water weather — 0 Jugner entry before"),
    ("huge leech",          "27-29", "ADV Leech, Fished Up"),
    ("knight crab",         "35",    "ADV Crab — page reads 35-35"),
]

run(ZONE, SLUG, ROWS, write=wants_write())
