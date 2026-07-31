#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Castle Oztroja (rev 269). Engine = zonepass.py
MOBS ONLY — no zoneinfo_edit, so the info box's Brass Statue password pointer and
the two Brass Door lever procedures are read and NOT harvested.

RULE 91: zoneinfo publishes 14 nms[] + 27 mobs[] and the shots read exactly that —
the NM table's cut top edge loses nothing.

!! THE NM ROW `Odontotyrannus (Monster)` IS THE WIKI DISAMBIGUATING A MOB FROM AN
ITEM OF THE SAME NAME (the row's own drop is the `Odontotyrannus` weapon). We target
`odontotyrannus (monster)` because the page's Genus column says **Pugil** and that is
the record carrying fam=Pugil; the bare `odontotyrannus` record is a fam=None,
zone-less stub. See the rev-269 (monster)-suffix measurement — 22 such records, all
with a bare twin, NOT resolved here.

41 page records (14 NM + 27 Adversaries), 0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Castle Oztroja"
SLUG = "castle_oztroja"

ROWS = [
    # --- Notorious Monsters ------------------------------------------------
    ("moo ouzi the swiftblade", "30",  "NM  Lottery(Yagudo Theologist), SAM"),
    ("mee deggi the punisher",  "36",  "NM  Lottery every 1-3 hr, MNK"),
    ("quu domi the gallant",    "36",  "NM  Lottery(Yagudo Herald/Oracle), NIN"),
    ("yaa haqa the profane",    "43",  "NM  Lottery(various Yagudo), BLM"),
    ("yagudo high priest",      "72-74", "NM  Timed 25 min, WHM"),
    ("yagudo avatar",           "75",  "NM  Timed 21-24 hr, SMN"),
    ("tzee xicu the manifest",  "85",  "NM  Lottery(Yagudo Avatar, every 2 Earth days), SMN"),
    ("saa doyi the fervid",     SKIP,  "NM  Timed 60-90 min, NIN — Lv BLANK, 0 zones before"),
    ("yagudo templar",          "72-74", "NM  Timed 20 min, SAM"),
    ("lii jixa the somnolist",  "48",  "NM  Timed 1.5 hr, WHM — 0 zones before; nmlv already 48"),
    ("huu xalmo the savage",    "63",  "NM  Quest(True Strength), MNK — 0 zones before"),
    ("odontotyrannus (monster)", "52", "NM  Quest(A Boy's Dream), WAR, Pugil — zone stored level-less, record has no lv"),
    ("warder partisan",         SKIP,  "NM  Timed (no interval published), MNK — Lv BLANK, 0 zones before"),
    ("yagudo muralist",         SKIP,  "NM  Quest(Picture Perfect), BLM — Lv BLANK, 0 zones before"),
    # --- Adversaries --------------------------------------------------------
    ("bastion bats",        "18-21", "ADV Flock Bat WAR, 16 spawns"),
    ("yagudo votary",       "22-26", "ADV MNK"),
    ("yagudo theologist",   "23-27", "ADV BLM (Moo Ouzi PH)"),
    ("yagudo priest",       "24-28", "ADV WHM"),
    ("yagudo's elemental",  "25-29", "ADV Elemental BLM — pet, assists Yagudo Oracle; 0 Oztroja entry before"),
    ("bulwark bat",         "29-31", "ADV Bat WAR"),
    ("meat maggot",         "29-31", "ADV Crawler WAR"),
    ("cutter",              "29-31", "ADV Crab"),
    ("yagudo herald",       "32-36", "ADV NIN (Quu Domi PH)"),
    ("yagudo drummer",      "33-37", "ADV BRD"),
    ("yagudo oracle",       "34-38", "ADV SMN (Quu Domi PH)"),
    ("yagudo interrogator", "35-39", "ADV SAM"),
    ("ooze",                "38-40", "ADV Slime"),
    ("yagudo zealot",       "42-46", "ADV MNK"),
    ("yagudo lutenist",     "42-48", "ADV BRD"),
    ("yagudo conquistador", "43-47", "ADV NIN"),
    ("yagudo parasite",     "45-48", "ADV Leech WAR"),
    ("yagudo prior",        "45-49", "ADV BLM"),
    ("earth elemental",     "47-49", "ADV Elemental BLM, earth weather — 0 Oztroja entry before"),
    ("fire elemental",      "47-49", "ADV Elemental BLM, fire weather — 0 Oztroja entry before"),
    ("yagudo sentinel",     "52-56", "ADV MNK — stored 51-56"),
    ("yagudo chanter",      "53-57", "ADV BRD"),
    ("yagudo inquisitor",   "54-58", "ADV SAM"),
    ("yagudo flagellant",   "62-72", "ADV MNK — stored 64-72; lv min 62 already matched the page (rule 104)"),
    ("yagudo conductor",    "63-72", "ADV BRD — stored 63-67"),
    ("yagudo assassin",     "64-72", "ADV NIN"),
    ("yagudo prelate",      "65-69", "ADV BLM"),
]

LV_EXTEND = {
    "lii jixa the somnolist":   (48, 48),   # [43,43] -> [43,48]; nmlv said 48 all along
    "odontotyrannus (monster)": (52, 52),   # record had NO lv at all
}

run(ZONE, SLUG, ROWS, lv_extend=LV_EXTEND, write=wants_write())
