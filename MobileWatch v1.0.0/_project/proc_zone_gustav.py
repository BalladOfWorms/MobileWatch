#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 292b — zone pass: Gustav Tunnel.
Zone string per zones.json = 'Gustav Tunnel'.
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'Gustav Tunnel'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Amikiri",                "80",    "Lottery (Antares)"),
    ("Baobhan Sith",           "77-81", "Lottery (Erlik)"),
    ("Bune",                   "80",    "Timed (21-24 hrs)"),
    ("Goblinsavior Heronox",   "55-59", "Lottery (Goblin Reaper)"),
    ("Taxim",                  "78-79", "Lottery (Doom Warlock)"),
    ("Ungur",                  "80-82", "Lottery (Typhoon Wyvern)"),
    ("Wyvernpoacher Drachlox", "70-75", "Lottery (Goblin Mercenary)"),
    ("Baronial Bat",           "82",    "Quest (Cloak and Dagger)"),
    ("Bompupu",                SKIP,    "Mission (A Shantotto Ascension 6)"),
    ("Gigaplasm",              SKIP,    "Mission (Bastok 9-1)"),
    ("Gorattz",                SKIP,    "Mission (A Shantotto Ascension 6)"),
    ("Macroplasm",             SKIP,    "Mission (Bastok 9-1)"),
    ("Microplasm",             SKIP,    "Mission (Bastok 9-1)"),
    ("Nanoplasm",              SKIP,    "Mission (Bastok 9-1)"),
    ("Renfred",                SKIP,    "Mission (A Shantotto Ascension 6)"),
    ("Wyvernhunter Bambrox",   "128",   "UNM (2,400 Unity Accolades)"),
]

ADV = [
    ("Hell Bat",         "44-48"),
    ("Hawker",           "45-48"),
    ("Labyrinth Leech",  "45-48"),
    ("Goblin Poacher",   "46-49"),
    ("Goblin Reaper",    "46-49"),
    ("Goblin Robber",    "46-49"),
    ("Greater Gaylas",   "46-49"),
    ("Labyrinth Lizard", "46-49"),
    ("Makara",           "46-49"),
    ("Goblin's Leech",   "53-55"),
    ("Doom Mage",        "65-67"),
    ("Doom Soldier",     "65-67"),
    ("Goblin Alchemist", "65-68"),
    ("Goblin Mercenary", "65-68"),
    ("Goblin Shepherd",  "65-68"),
    ("Robber Crab",      "65-68"),
    ("Demonic Pugil",    "73-76"),
    ("Doom Guard",       "75-77"),
    ("Earth Elemental",  "75-77"),
    ("Fire Elemental",   "75-77"),
    ("Erlik",            "75-78"),
    ("Doom Warlock",     "76-78"),
    ("Antares",          "77-79"),
    ("Typhoon Wyvern",   "78-80"),
    ("Boulder Eater",    "100-102"),
    ("Pygmytoise",       "102-103"),
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
    ('bune',            '80'),        # NM, ZERO zones — nmlv 80
    ('ungur',           '80-82'),     # NM, ZERO zones — nmlv 80-82
    ('typhoon wyvern',  '78-80'),     # Ungur's PLACEHOLDER, also ZERO zones (rule 125)
    ('antares',         '77-79'),     # Amikiri's placeholder, ZERO zones
    ('bompupu',         None),        # ZERO zones, no published level
    ('gorattz',         None),
    ('renfred',         None),
    ('earth elemental', '75-77'),
    ('fire elemental',  '75-77'),
    ('boulder eater',   '100-102'),   # 100+ tier, ZERO zones (rule 130)
    ('pygmytoise',      '102-103'),
]
WRITES_LEVEL = [
    ('baronial bat', None, '82'),     # nmlv already 82
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
