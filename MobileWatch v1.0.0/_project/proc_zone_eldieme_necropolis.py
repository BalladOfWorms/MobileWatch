#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: The Eldieme Necropolis (rev 264). Engine = zonepass.py

MOBS ONLY (rev-171 ruling: "just mobs though going forward") — no zoneinfo_edit is
passed, so the info-box footnote (Magicked Astrolabe doors, the two G-9 block drops)
and the Map-Acquisition row are deliberately NOT harvested.

RULE 98: `The Eldieme Necropolis` is a strict prefix of `The Eldieme Necropolis [S]`,
and 6 of these records carry BOTH (gazer, lost soul, revenant, hell hound, lich,
+ earth elemental). zonepass matches the zone by exact string, and the [S] entries
are re-verified after the write.

RULE 2 merges: `Lost Soul` is two job rows (BLM + WAR, both 42-46); `Shade`, `Ka`,
`Dark Stalker` and `Spriggan` are four job rows each — one record, one zone entry.

43 page records (17 NM + 26 Adversaries), 0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "The Eldieme Necropolis"
SLUG = "the_eldieme_necropolis"

ROWS = [
    # --- Notorious Monsters ------------------------------------------------
    ("cwn cyrff",        "68",    "NM  Lottery(Tomb Wolf) (D-5/6) Map 2"),
    ("skull of envy",    "60",    "NM  7 Deadly Sins shared spawn, DRG"),
    ("skull of gluttony","60",    "NM  7 Deadly Sins shared spawn, PLD"),
    ("skull of greed",   "60",    "NM  7 Deadly Sins shared spawn, MNK"),
    ("skull of lust",    "60",    "NM  7 Deadly Sins shared spawn, THF"),
    ("skull of pride",   "60",    "NM  7 Deadly Sins shared spawn (Map 3)"),
    ("skull of sloth",   "60",    "NM  7 Deadly Sins shared spawn, BLM"),
    ("skull of wrath",   "60",    "NM  7 Deadly Sins shared spawn, WAR"),
    ("namorodo",         SKIP,    "NM  Quest(Girl in the Looking Glass) — Lv BLANK (keeps 61-65)"),
    ("dog guardian",     "52",    "NM  Quest(The Requiem) — zone stored level-less"),
    ("owl guardian",     "52",    "NM  Quest(The Requiem) — zone stored level-less"),
    ("yum kimil",        "54",    "NM  Quest(The Requiem) — zone stored level-less"),
    ("lich c magnus",    "58",    "NM  Quest(Blue Ribbon Blues), BLM — zone stored level-less"),
    ("sturm",            "62",    "NM  Quest(A New Dawn), THF — zone stored level-less"),
    ("taifun",           "58",    "NM  Quest(A New Dawn), WAR, Tiger — 0 zones before"),
    ("trombe",           "58",    "NM  Quest(A New Dawn), WAR, Tiger — 0 zones before"),
    ("gasha",            SKIP,    "NM  Voidwatch (White stratum abyssite II) — Lv BLANK, 0 zones before"),
    # --- Adversaries --------------------------------------------------------
    ("marchosias",       "40-43", "ADV Hound"),
    ("gazer",            "41-43", "ADV Hecteyes"),
    ("puroboros",        "42-44", "ADV Bomb"),
    ("lost soul",        "42-46", "ADV Skeleton — BLM + WAR rows, both 42-46 (rule 2)"),
    ("revenant",         "44-47", "ADV Ghost"),
    ("anemone",          "45-46", "ADV Morbol"),
    ("shade",            "46-48", "ADV Fomor — WAR/RNG/THF/BLM rows, all 46-48"),
    ("hell hound",       "46-49", "ADV Hound"),
    ("blood soul",       "50-52", "ADV Ghost, Eld. Chest Key"),
    ("mummy",            "50-52", "ADV Skeleton WAR, Eld. Chest Key"),
    ("azer",             "51-53", "ADV Bomb, Eld. Chest Key — stored 51-58 = its own lv (rule 49)"),
    ("lich",             "51-55", "ADV Skeleton BLM, Eld. Chest Key"),
    ("ka",               "52-54", "ADV Fomor — BLM/THF/RNG/WAR rows, all 52-54"),
    ("earth elemental",  "52-55", "ADV Elemental, earth weather — 0 Eldieme entry before"),
    ("ice elemental",    "52-55", "ADV Elemental, ice weather — 0 Eldieme entry before"),
    ("tomb wolf",        "53-55", "ADV Hound, Eld. Chest Key (Cwn Cyrff PH)"),
    ("fallen knight",    "54-56", "ADV Skeleton WAR, Eld. Chest Key"),
    ("utukku",           "55-57", "ADV Ghost, Eld. Chest Key"),
    ("dark stalker",     "57-59", "ADV Fomor — 4 job rows, all 57-59 — 0 zones before"),
    ("tomb warrior",     "60-62", "ADV Skeleton WAR, Eld. Coffer Key"),
    ("tomb mage",        "60-63", "ADV Skeleton BLM, Eld. Coffer Key"),
    ("haunt",            "63-65", "ADV Ghost, Eld. Coffer Key"),
    ("spriggan",         "64-66", "ADV Fomor — 4 job rows, Eld. Coffer Key — 0 zones before"),
    ("nekros hound",     "91-95", "ADV Hound (high-tier block)"),
    ("hellbound warlock","91-95", "ADV Skeleton BLM (high-tier block) — fam=None orphan"),
    ("hellbound warrior","91-95", "ADV Skeleton WAR (high-tier block) — fam=None orphan"),
]

# rule 9 — a level write EXTENDS lv, never shrinks it
LV_EXTEND = {
    "nekros hound": (91, 95),   # stored [93,95]; page publishes 91-95
}

run(ZONE, SLUG, ROWS, lv_extend=LV_EXTEND, write=wants_write())
