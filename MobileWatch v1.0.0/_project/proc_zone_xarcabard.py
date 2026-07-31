#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 297 — zone pass: Xarcabard.
Zone string per zones.json = 'Xarcabard'.
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'Xarcabard'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Biast",            "70",    "Lottery (Shadow Dragon, every 21 hrs)"),
    ("Boreal Coeurl",    "58",    "Timed (5 min)"),
    ("Boreal Hound",     "58",    "Timed (5 min)"),
    ("Boreal Tiger",     "58",    "Timed (5 min)"),
    ("Chaos Elemental",  "42",    "Quest (The Three Magi)"),
    ("Duke Focalor",     "53",    "Timed (15-30 min)"),
    ("Ereshkigal",       SKIP,    "Timed (21-24 hrs, gloom weather)"),
    ("Koenigstiger",     "63",    "Quest (Unbridled Passion)"),
    ("Shadow Eye",       "48-49", "Lottery (Evil Eye)"),
    ("Barbaric Weapon",  SKIP,    "Lottery (Cursed Weapon)"),
    ("Timeworn Warrior", SKIP,    "Lottery (Lost Soul)"),
    ("Beist",            "125",   "UNM (2,100 Unity Accolades)"),
    ("Gjenganger",       SKIP,    "Voidwalker (Clear abyssite)"),
    ("Gorehound",        SKIP,    "Voidwalker (Clear abyssite)"),
    ("Erebus",           SKIP,    "Voidwalker (Colorful abyssite)"),
    ("Feuerunke",        SKIP,    "Voidwalker (Colorful abyssite)"),
    ("Lord Ruthven",     SKIP,    "Voidwalker (Purple abyssite)"),
    ("Yilbegan",         SKIP,    "Voidwalker (Black abyssite)"),
]

ADV = [
    ("Gigas's Tiger",     "38-40"),
    ("Lost Soul",         "42-45"),   # rule 2: WAR + BLM rows, same band
    ("Cursed Weapon",     "43-45"),   # rule 2: WAR + RDM rows, same band
    ("Demon's Elemental", "43-45"),
    ("Etemmu",            "43-46"),
    ("Blizzard Gigas",    "45-48"),
    ("Evil Eye",          "45-48"),
    ("Frost Gigas",       "45-48"),
    ("Graupel Gigas",     "45-48"),
    ("Hail Gigas",        "45-48"),
    ("Dark Elemental",    "48-50"),
    ("Ice Elemental",     "48-50"),
    ("Demon Knight",      "48-52"),
    ("Demon Pawn",        "48-52"),
    ("Demon Wizard",      "48-52"),
    ("Demon Warlock",     "50-52"),
    ("Shadow Dragon",     "52-53"),
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
    ('boreal coeurl',     '58'),      # NM, ZERO zones (nmlv 58)
    ('boreal tiger',      '58'),      # NM, ZERO zones (nmlv 58)
    ('chaos elemental',   '42'),      # NM, ZERO zones
    ('duke focalor',      '53'),      # NM, ZERO zones (nmlv 53)
    ('koenigstiger',      '63'),      # NM, ZERO zones
    ('timeworn warrior',  None),      # NM, ZERO zones, page publishes no level
    ("demon's elemental", '43-45'),
    ('dark elemental',    '48-50'),
    ('ice elemental',     '48-50'),
]
WRITES_LEVEL = [
    ('boreal hound',  None,    '58'),      # held the zone with a NULL level; nmlv 58
    ("gigas's tiger", '38-42', '38-40'),
    ('lost soul',     '45-47', '42-45'),
]
# rule 9 SUSPENDED on the three Boreal NMs: each stores lv [53,53] against nmlv 58 — disjoint
# points, so a union would invent a 53-58 band. nmlv overrides on the card.


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
