#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Inner Horutoto Ruins (rev 160). Engine = zonepass.py

Rule 57 clean — only the two canonical Horutoto strings exist.

Sources: 4 shots — (1) info box, (2) NM table + start of Adversaries, (3)+(4) the rest.

29 page rows -> 26 distinct records. THREE two-row pairs, and rule 61 fires on two
of them (the job variants publish DIFFERENT ranges):
  Magicked Bones  WAR 3-8  + unjobbed 6-8 -> merged 3-8
  Boggart         WAR 22-25 + RDM 23-26   -> merged 22-26
  Wendigo         BLM 25-28 + WAR 25-28   -> 25-28 (same range)

THE WHOLE 78-84 BLOCK HAD ZERO ZONES — nine records (covin bat, deathwatch beetle,
goblin flesher/lurcher/metallurgist/trailblazer, skinnymajinx, skinnymalinks,
troika bats). Same shape as King Ranperre's `Locus` block last week: a high-level
tier bolted onto a starter dungeon that early intake never covered.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Inner Horutoto Ruins"
SLUG = "inner_horutoto_ruins"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("maltha",                "22-23", "NM  Timed 1.5-2 hr"),
    ("nocuous weapon",        "22-26", "NM  Lottery(Boggart)"),
    ("slendlix spindlethumb", "33",    "NM  Lottery(Goblin Leecher)  (0 zones before)"),
    # --- Adversaries, the original tier ----------------------------------
    ("battue bats",           "1-5",   "ADV 1-5"),
    ("goblin thug",           "1-6",   "ADV 1-6"),
    ("goblin weaver",         "1-7",   "ADV 1-7"),
    ("magicked bones",        "3-8",   "ADV WAR 3-8 + unjobbed 6-8 -> merged (rule 2/61)"),
    ("blade bat",             "4-6",   "ADV 4-6"),
    ("balloon",               "8-10",  "ADV 8-10"),
    ("blob",                  "15-18", "ADV 15-18  (drops Hrt. Chest Key)"),
    ("battle bat",            "17-20", "ADV 17-20  (drops Hrt. Chest Key)"),
    ("goblin leecher",        "20-23", "ADV 20-23  (drops Hrt. Chest Key)"),
    ("goblin mugger",         "20-23", "ADV 20-23  (drops Hrt. Chest Key)"),
    ("goblin gambler",        "20-23", "ADV 20-23  (drops Hrt. Chest Key)"),
    ("will-o'-the-wisp",      "22-25", "ADV 22-25"),
    ("boggart",               "22-26", "ADV WAR 22-25 + RDM 23-26 -> merged (rule 2/61)"),
    ("wendigo",               "25-28", "ADV BLM 25-28 + WAR 25-28"),
    # --- Adversaries, the 78-84 tier (all had ZERO zones) ----------------
    ("troika bats",           "78-80", "ADV high tier"),
    ("deathwatch beetle",     "79-81", "ADV high tier"),
    ("goblin flesher",        "80-82", "ADV high tier"),
    ("goblin metallurgist",   "80-82", "ADV high tier"),
    ("goblin trailblazer",    "80-82", "ADV high tier"),
    ("skinnymalinks",         "80-83", "ADV high tier (fam=None orphan; page Genus = Skeleton)"),
    ("covin bat",             "81-83", "ADV high tier"),
    ("skinnymajinx",          "81-83", "ADV high tier (fam=None orphan; page Genus = Skeleton)"),
    ("goblin lurcher",        "83-84", "ADV high tier"),
]

# rule 9 — two records whose stored `lv` does not contain the page's zone range.
# Neither is a correction (both zone entries already matched or were absent), but
# the union is purely additive and leaves each record consistent with its own zone.
LV_EXTEND = {
    "nocuous weapon": (22, 27),   # was [25,27]; its only zone reads 22-26
    "skinnymalinks":  (80, 84),   # was [81,84]; page publishes 80-83
}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # type Dungeon and footprint (I-7) already match the info box; no footnote to note.
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
