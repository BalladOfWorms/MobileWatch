#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 286 — zone pass: Yuhtunga Jungle.
Zone string per zones.json = 'Yuhtunga Jungle'.
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'Yuhtunga Jungle'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Meww the Turtlerider",  "47",    "Timed (21 hrs)"),
    ("Mischievous Micholas",  "53-55", "Lottery (Young Opo-opo)"),
    ("Rose Garden",           "50",    "Special (morphs from Overgrown Rose, ~10 hrs undisturbed)"),
    ("Voluptuous Vilma",      SKIP,    "Special (morphs from Rose Garden, unknown period)"),
    ("Bayawak",               "67-70", "Timed (1.5-2 hrs, weather)"),
    ("Koropokkur",            SKIP,    "Timed (60-90 min)"),
    ("Pyuu the Spatemaker",   SKIP,    "Timed (90-120 min, caves)"),
    ("Carthi",                "65",    "Mission (Zilart 5)"),
    ("Nasus",                 SKIP,    "Quest (Tuning Out)"),
    ("Tipha",                 "65",    "Mission (Zilart 5)"),
    ("Sybaritic Samantha",    "119",   "UNM (1,500 Unity Accolades)"),
    ("Holy Moly",             SKIP,    "Voidwatch (Ashen stratum abyssite + Voidstone)"),
]

ADV = [
    ("Yuhtunga Mandragora", "30-33"),
    ("Ivory Lizard",        "32-35"),
    ("Goblin Furrier",      "32-37"),
    ("Goblin Smithy",       "32-37"),
    ("Death Jacket",        "33-37"),
    ("Young Opo-opo",       "34-36"),
    ("Creek Sahagin",       "34-38"),
    ("River Sahagin",       "34-38"),
    ("Stream Sahagin",      "34-38"),
    ("Goblin Digger",       "35-38"),
    ("Jungle Coeurl",       "35-38"),
    ("Makara",              "35-38"),
    ("Soldier Crawler",     "37-41"),
    ("Goblin Poacher",      "42-47"),
    ("Goblin Reaper",       "42-47"),
    ("Goblin Robber",       "42-47"),
    ("Overgrown Rose",      "45-48"),
    ("Lava Bomb",           "47-49"),
    ("Fire Elemental",      "48-50"),
    ("Water Elemental",     "48-50"),
    ("Ironshell",           "35-37"),   # Fished Up
    ("Bigclaw",             "41-49"),   # rule 2: TWO Fished Up blocks, 41-43 U 47-49
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
    ('meww the turtlerider', '47'),     # held only YHOATOR Jungle 47 — the wrong jungle
    ('koropokkur',           None),     # ZERO zones before; page publishes no level
    ('pyuu the spatemaker',  None),     # ZERO zones before; page publishes no level
    ('carthi',               '65'),     # ZERO zones before
    ('tipha',                '65'),     # ZERO zones before
    ('fire elemental',       '48-50'),
    ('water elemental',      '48-50'),
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
    assert not [1 for mm in mobs.values() for v in mm.values() if v is None]
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, separators=(', ', ': '), ensure_ascii=False)
    print('written', p)


if len(sys.argv) > 1 and sys.argv[1] == 'apply':
    apply()
