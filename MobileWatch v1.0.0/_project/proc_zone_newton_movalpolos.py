#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Newton Movalpolos (rev 277). Engine = zonepass.py
MOBS ONLY — the info box's Furnace Hatch / Firesand gate mechanic is read and NOT
harvested (no note authorised for this zone).

RULE 2: `Goblin's Bat` is TWO blocks — 61-64 (pet, assists Goblin Foreman) and 69-74
(pet, assists Goblin Headman, drops the Newton Coffer Key) -> **61-74**. zoneinfo
already stores the two-block string "61-64, 69-74".

33 page records (4 NM + 29 Adversaries), 0 missing.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Newton Movalpolos"
SLUG = "newton_movalpolos"

ROWS = [
    ("bugbear matman",        SKIP, "NM  Forced (trade Air Tank to Moblin Showman), MNK — Lv BLANK"),
    ("goblin collector",      SKIP, "NM  Forced (trade Premium Bag to ???), WHM — Lv BLANK"),
    ("swashstox beadblinker", SKIP, "NM  Lottery(Goblin Swordsman), WAR — Lv BLANK"),
    ("sword sorcerer solisoq",SKIP, "NM  spawn cell is literally 'TODO', RDM, Moblin — Lv BLANK, 0 zones before"),
    ("goblin's bat",     "61-74", "ADV Bat — RULE 2: 61-64 (assists Goblin Foreman) + 69-74 (assists Goblin Headman)"),
    ("succubus bats",    "63-65", "ADV Flock Bat"),
    ("dire bat",         "63-65", "ADV Bat"),
    ("bugbear trashman", "65-67", "ADV Bugbear MNK"),
    ("moblin yardman",   "66-69", "ADV Moblin THF"),
    ("goblin lengthman", "66-69", "ADV Goblin RNG"),
    ("goblin packman",   "66-69", "ADV Goblin DRK"),
    ("moblin tankman",   "66-69", "ADV Moblin WHM"),
    ("moblin draftsman", "66-69", "ADV Moblin BLM"),
    ("moblin workman",   "66-69", "ADV Moblin RDM"),
    ("goblin fireman",   "66-69", "ADV Goblin WAR"),
    ("goblin foreman",   "66-69", "ADV Goblin BST"),
    ("thunder elemental","70-80", "ADV Elemental, thunder weather — 0 Newton entry before"),
    ("earth elemental",  "70-80", "ADV Elemental, earth weather — 0 Newton entry before"),
    ("bugbear watchman", "71-76", "ADV Bugbear MNK, Newton Coffer Key"),
    ("nightmare bats",   "72-74", "ADV Flock Bat, Newton Coffer Key"),
    ("purgatory bat",    "72-74", "ADV Bat, Newton Coffer Key"),
    ("bugbear deathsman","74-76", "ADV Bugbear MNK, Newton Coffer Key"),
    ("moblin aidman",    "75-79", "ADV Moblin WHM, Newton Coffer Key"),
    ("moblin topsman",   "75-79", "ADV Moblin RDM"),
    ("moblin roadman",   "75-79", "ADV Moblin THF"),
    ("moblin engineman", "75-79", "ADV Moblin BLM"),
    ("goblin marksman",  "75-79", "ADV Goblin RNG"),
    ("goblin headman",   "75-79", "ADV Goblin BST"),
    ("goblin hangman",   "75-79", "ADV Goblin DRK"),
    ("goblin junkman",   "75-79", "ADV Goblin WAR, Newton Coffer Key"),
    ("moblin groundman", "77",    "ADV Moblin RDM — page reads 77-77"),
    ("goblin swordsman", "78",    "ADV Goblin WAR — page reads 78-78 (Swashstox Beadblinker PH)"),
    ("moblin scalpelman","78-80", "ADV Moblin WHM"),
]

LV_EXTEND = {
    "goblin's bat": (61, 74),   # [23,64] -> [23,74]
}

run(ZONE, SLUG, ROWS, lv_extend=LV_EXTEND, write=wants_write())
