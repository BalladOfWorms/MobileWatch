#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 289 — zone pass: The Sanctuary of ZiTah.
Zone string per zones.json = 'The Sanctuary of ZiTah'.
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'The Sanctuary of ZiTah'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Keeper of Halidom",   "56-61", "Lottery (Goobbue Gardener)"),
    ("Noble Mold",          "50",    "Special (morphs from Myxomycete, rain weather)"),
    ("Bastet",              SKIP,    "Timed (unknown)"),
    ("Elusive Edwin",       SKIP,    "Timed"),
    ("Huwasi",              SKIP,    "Timed (2 hrs)"),
    ("Blest Bones",         SKIP,    "Timed (17:00-7:00, immediate respawn)"),
    ("Doomed Pilgrims",     "70",    "Mission (Zilart 5)"),
    ("Greenman",            "80-81", "Quest (The Weight of Your Limits)"),
    ("Guardian Treant",     SKIP,    "Quest (Forge Your Destiny)"),
    ("Holey Horror",        SKIP,    "Timed (17:00-7:00, immediate respawn)"),
    ("Isonade",             SKIP,    "Quest (The Sacred Katana)"),
    ("Skeleton Scuffler",   SKIP,    "Timed (17:00-7:00, immediate respawn)"),
    ("Keeper of Heiligtum", "122",   "UNM (1,800 Unity Accolades)"),
    ("Cath Palug",          SKIP,    "Voidwatch (Ashen stratum abyssite II + Voidstone)"),
]

ADV = [
    ("Goblin Gambler",   "25-29"),
    ("Goblin Leecher",   "25-29"),
    ("Goblin Mugger",    "25-29"),
    ("Ancient Bat",      "26-28"),
    ("Goblin Furrier",   "31-34"),
    ("Goblin Smithy",    "31-34"),
    ("Goblin's Leech",   "35-40"),
    ("Lesser Gaylas",    "39-42"),
    ("Goobbue Gardener", "40-43"),
    ("Ogrefly",          "41-44"),
    ("Myxomycete",       "41-46"),
    ("Goobbue Parasite", "42-45"),
    ("Goblin Poacher",   "42-46"),
    ("Goblin Reaper",    "42-46"),
    ("Goblin Robber",    "42-46"),
    ("Goblin Trader",    "42-46"),
    ("Master Coeurl",    "44-47"),
    ("Revenant",         "45-47"),
    ("Hell Hound",       "46-50"),
    ("Puroboros",        "47-49"),
    ("Thunder Elemental","48-49"),
    ("Water Elemental",  "48-49"),
    ("Rock Golem",       "49-50"),
    ("Rot Prowler",      "49-53"),
    ("Lost Soul",        "51-55"),
    ("Goblin Bouncer",   "54-58"),
    ("Goblin Enchanter", "54-58"),
    ("Clipper",          "25-28"),   # Fished Up
    ("Greater Pugil",    "25-28"),   # Fished Up
    ("Big Jaw",          "34-37"),   # Fished Up
    ("Bigclaw",          "42-45"),   # Fished Up
    ("Makara",           "47-50"),   # Fished Up
]

ROWS = [(n, l) for n, l, _ in NM] + ADV


def load():
    p = os.path.join(ASSETS, 'mobs.json')
    with open(p, encoding='utf-8') as f:
        return p, json.load(f)


def find(mobs, name):
    """Resolve a page name to a record key.

    rev 292: a page name can match BOTH a bare key and a `<name> (monster)` twin — 22 such
    pairs exist file-wide. Preferring the bare key silently added a SECOND Antares to Gustav
    Tunnel. Prefer whichever twin already holds THIS zone, then whichever holds any zone at
    all; the bare stub is almost always the empty one.
    """
    k = name.lower()
    cands = [c for c in (k, k + ' (monster)', k + ' (nm)') if c in mobs]
    if not cands:
        return None
    if len(cands) > 1:
        here = [c for c in cands if zentry(mobs[c])]
        if here:
            return here[0]
        zoned = [c for c in cands if mobs[c].get('zones')]
        if zoned:
            return zoned[0]
    return cands[0]


def zentry(rec):
    for e in rec.get('zones') or []:
        zn = e[0] if isinstance(e, list) else e
        if zn == ZONE:
            return e
    return None


def survey():
    _, d = load()
    mobs = d['mobs']
    missing, ok, add_zone, fill_lvl, change_lvl, kept = [], [], [], [], [], []
    for name, lvl in ROWS:
        k = find(mobs, name)
        if not k:
            missing.append(name)
            continue
        rec = mobs[k]
        e = zentry(rec)
        cur = e[1] if (isinstance(e, list) and len(e) > 1) else None
        if e is None:
            add_zone.append((name, k, lvl, rec.get('lv'), rec.get('nmlv')))
        elif lvl == SKIP:
            kept.append((name, k, cur))
        elif cur is None:
            fill_lvl.append((name, k, lvl, rec.get('lv'), rec.get('nmlv')))
        elif cur != lvl:
            change_lvl.append((name, k, cur, lvl, rec.get('lv'), rec.get('nmlv')))
        else:
            ok.append(name)
    print('rows', len(ROWS), 'ok', len(ok))
    for lbl, b in (('MISSING', missing), ('ADD ZONE', add_zone), ('FILL LEVEL', fill_lvl),
                   ('CHANGE LEVEL', change_lvl), ('KEPT (page blank)', kept)):
        print('\n== %s (%d)' % (lbl, len(b)))
        for x in b:
            print('  ', x)


if __name__ == '__main__':
    survey()









# ---------------------------------------------------------------- apply
WRITES_ZONE = [
    ('bastet',            None),   # ZERO zones before
    ('blest bones',       None),   # ZERO zones — Luminous beige fragment
    ('holey horror',      None),   # ZERO zones — Luminous green fragment
    ('skeleton scuffler', None),   # ZERO zones — Luminous red fragment
    ('cath palug',        None),   # ZERO zones — Voidwatch
    ('thunder elemental', '48-49'),
    ('water elemental',   '48-49'),
]
WRITES_LEVEL = [
    ('greenman',        None, '80-81'),   # nmlv already 80-81
    ('rock golem',      None, '49-50'),
    ('doomed pilgrims', '60', '70'),      # zone level was a copy of its own wrong lv; nmlv reads 70
]


def apply():
    p, d = load()
    mobs = d['mobs']
    for k, lvl in WRITES_ZONE:
        rec = mobs[k]
        assert zentry(rec) is None, k
        rec.setdefault('zones', [])
        rec['zones'].append([ZONE, lvl] if lvl else [ZONE])
        print('ZONE ADD  ', k, lvl)
    for k, old, new in WRITES_LEVEL:
        rec = mobs[k]
        e = zentry(rec)
        cur = e[1] if len(e) > 1 else None
        assert cur == old, (k, cur, old)
        if len(e) > 1:
            e[1] = new
        else:
            e.append(new)
        print('LEVEL     ', k, old, '->', new)
    assert not [1 for mm in mobs.values() for v in mm.values() if v is None]
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, separators=(', ', ': '), ensure_ascii=False)
    print('written', p)


if len(sys.argv) > 1 and sys.argv[1] == 'apply':
    apply()
