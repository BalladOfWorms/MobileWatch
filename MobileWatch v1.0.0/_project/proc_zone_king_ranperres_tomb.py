#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: King Ranperres Tomb (rev 157). Engine = zonepass.py
RUN proc_ranperre_zonestring.py FIRST — 36 of these records stored the apostrophe
form of the zone name and would otherwise read as missing.

Sources: 5 uploaded shots — (1) info box, (2)+(3) Notorious Monsters, (3)+(4)+(5)
Adversaries. The biggest page of the sweep so far.

53 page rows -> 48 distinct records:
  * `Enchanted Bones`  WAR + DRK rows, both 4-8   -> one record
  * `Nachzehrer`       WAR + DRK rows, both 15-18 -> one record
  * `Spook` appears in BOTH tables — NM (11-13 WAR) and Adversaries (11-13 BLM),
    same level -> one record, one entry
  * `Hahava` is listed TWICE in the NM table (a short Voidwatch row and a fuller
    one) -> one record; its drops are consolidated in proc_nm_drops_consolidate.py
    per the user's rule: one entry, valuable drops listed, zones section lists all.

`?` in the Lv column (Airi / Iruci / Pey, all summoned by Vrtra) is rule-10
no-data, exactly like BLANK -> SKIP.

The plain-named 58-82 mobs (tomb worm, armet beetle, cutlass scorpion, dire bat,
thousand eyes, lemures) are NOT on this page and are NOT the same mobs as the
131-138 `Locus *` rows that are — both legitimately live here, so rule 1 leaves
the unlisted ones alone.
"""
from zonepass import run, wants_write, SKIP

ZONE = "King Ranperres Tomb"
SLUG = "king_ranperres_tomb"

ROWS = [
    # --- Notorious Monsters ----------------------------------------------
    ("ankou",              "21",      "NM  Undead 20:00-4:00 hourly"),
    ("arcus blades",       "109",     "NM  Quest — Epiphany hazy rune"),
    ("barbastelle",        "16-19",   "NM  Timed 50-90 min"),
    ("cemetery cherry",    "72-73",   "NM  Timed 60-72h after all Cherry Sapling die"),
    ("corrupted soffeil",  "63",      "NM  Mission San d'Oria 6-2"),
    ("corrupted ulbrig",   "63",      "NM  Mission San d'Oria 6-2"),
    ("corrupted yorgos",   "64",      "NM  Mission San d'Oria 6-2"),
    ("crypt ghost",        "20-21",   "NM  Lottery(Tomb Bat)"),
    ("gwyllgi",            SKIP,      "NM  Lottery(Nachzehrer) — Lv cell BLANK"),
    ("hahava",             SKIP,      "NM  Voidwatch — Lv cell BLANK (listed TWICE)"),
    ("spook",              "11-13",   "NM row AND Adversaries row, both 11-13"),
    ("vrtra",              "95",      "NM  Timed 3-5 days"),
    ("airi",               SKIP,      "NM  summoned by Vrtra — Lv cell '?' (rule 10)"),
    ("iruci",              SKIP,      "NM  summoned by Vrtra — Lv cell '?' (rule 10)"),
    ("pey",                SKIP,      "NM  summoned by Vrtra — Lv cell '?' (rule 10)"),
    # --- Adversaries -----------------------------------------------------
    ("carrion worm",       "2-5",     "ADV 2-5"),
    ("ding bats",          "2-5",     "ADV 2-5 night"),
    ("mouse bat",          "3-6",     "ADV 3-6"),
    ("enchanted bones",    "4-8",     "ADV 4-8 (WAR + DRK rows = one record)"),
    ("goblin thug",        "4-8",     "ADV 4-8"),
    ("goblin weaver",      "4-8",     "ADV 4-8"),
    ("stone eater",        "5-7",     "ADV 5-7"),
    ("wind bats",          "9-11",    "ADV 9-11"),
    ("grave bat",          "11-13",   "ADV 11-13"),
    ("goblin ambusher",    "12-16",   "ADV 12-16"),
    ("goblin butcher",     "12-16",   "ADV 12-16"),
    ("goblin tinkerer",    "12-16",   "ADV 12-16"),
    ("rock eater",         "14-16",   "ADV 14-16"),
    ("plague bats",        "15-17",   "ADV 15-17 night"),
    ("nachzehrer",         "15-18",   "ADV 15-18 (WAR + DRK rows = one record)"),
    ("tomb bat",           "17-19",   "ADV 17-19"),
    ("goblin gruel",       "18-20",   "ADV 18-20"),
    ("goblin gambler",     "21-23",   "ADV 21-23"),
    ("goblin leecher",     "21-23",   "ADV 21-23"),
    ("goblin mugger",      "21-23",   "ADV 21-23"),
    ("cherry sapling",     "62-64",   "ADV 62-64"),
    ("hati",               "77-79",   "ADV 77-79"),
    ("spartoi warrior",    "78-80",   "ADV 78-80"),
    ("spartoi sorcerer",   "80-82",   "ADV 80-82"),
    # --- Adversaries, the 131-138 Locus block ----------------------------
    ("locus tomb worm",       "131-133", "ADV Locus block"),
    ("locus dire bat",        "133-135", "ADV Locus block"),
    ("locus armet beetle",    "134-136", "ADV Locus block"),
    ("locus cutlass scorpion","135-137", "ADV Locus block"),
    ("locus thousand eyes",   "135-137", "ADV Locus block"),
    ("locus hati",            "135-137", "ADV Locus block"),
    ("locus spartoi sorcerer","135-137", "ADV Locus block"),
    ("locus spartoi warrior", "135-137", "ADV Locus block"),
    ("locus lemures",         "137-138", "ADV Locus block"),
]

# rule 9 — only where the page's value falls outside a stored band. Deliberately
# NOT touching `hati` [135,137] or `locus lemures` [80,82]: each holds the OTHER
# record's level band, so a union would widen them to nonsense ([77,137] /
# [80,138]) instead of fixing anything. Flagged as (ma) for the user's call —
# same treatment as be'hya's lv-vs-nmlv split at rev 152.
LV_EXTEND = {
    "locus hati": (135, 137),   # was [136,137]; page publishes 135-137
}


def zoneinfo_edit(e):
    out = []
    # rule 40 — zones.json base is the bogus ["Sunshine","Clouds"]; page says None
    if not e.get('weather'):
        e['weather'] = 'None'
        out.append("weather override '' -> 'None'")
    # rule 12 / 43 — the info-box footnote, per-zone abyssite tier (a FOURTH stratum
    # value: Crimson IV here vs Crimson I+ at East Ronfaure and Indigo at Gustaberg)
    notes = [
        "Possession of Crimson stratum abyssite IV is required to unlock the "
        "Voidwatch Warp for this area.",
        "The Voidwatch Warp does not place you inside the area — it brings you to "
        "the entrance in East Ronfaure.",
    ]
    e.setdefault('notes', [])
    added = [n for n in notes if n not in e['notes']]
    e['notes'].extend(added)
    if added:
        out.append(f"notes += {len(added)} (Crimson stratum abyssite IV; warp lands in East Ronfaure)")
    return out


run(ZONE, SLUG, ROWS, LV_EXTEND, zoneinfo_edit=zoneinfo_edit, write=wants_write())
