#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 296 — zone pass: Uleguerand Range.
Zone string per zones.json = 'Uleguerand Range'.
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'Uleguerand Range'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Black Coney",     "70-72", "Forced (San d'Orian Carrot to Rabbit Footprint, new moon)"),
    ("Bonnacon",        "69",    "Lottery (Buffalo)"),
    ("Father Frost",    "74-75", "Special (morphs from Snow Maiden)"),
    ("Geush Urvan",     SKIP,    "Forced (trade Haunted Muleta to ???)"),
    ("Jormungand",      "95",    "Timed (every 3-5 Earth days)"),
    # Mountain Worm is a CROSS-TABLE mob and the file models it CORRECTLY as a bare/(nm) PAIR:
    # `mountain worm` holds the Adversaries band 66-70, `mountain worm (nm)` holds the NM row 73.
    # Merging them into one 66-73 entry (tried, reverted) puts two Mountain Worms in the zone view.
    ("Mountain Worm",   "66-70", "Timed (21 hrs)"),
    ("Snow Maiden",     "71-72", "Special (morphs from Morozko)"),
    ("White Coney",     "70-72", "Forced (San d'Orian Carrot to Rabbit Footprint, full moon)"),
    ("Frost Flambeau",  "74",    "Timed (2-2.5 hrs)"),
    ("Magnotaur",       "~83",   "Lottery (Molech)"),
    ("Skvader",         "77-78", "Lottery (Polar Hare)"),
    ("Camahueto",       "128",   "UNM (2,400 Unity Accolades)"),
    ("Isarukitsck",     SKIP,    "Voidwatch (Hyacinth stratum abyssite + Voidstone)"),
]

ADV = [
    ("Variable Hare",       "58-61"),
    ("Glacier Eater",       "58-62"),
    ("Esbat",               "59-61"),
    ("Cwn Annwn",           "59-64"),
    ("Snoll",               "60-63"),
    ("Uleguerand Tiger",    "60-63"),
    ("Buffalo",             "62-65"),
    ("Polar Hare",          "65-68"),
    ("Succubus Bats",       "65-68"),
    ("Ice Elemental",       "66-84"),   # rule 2: 66-68 U 82-84
    ("Doom Soldier",        "66-70"),
    ("Morozko",             "67-70"),
    ("Phasma",              "67-72"),
    ("Nival Raptor",        "68-70"),
    ("Brontotaur",          "68-71"),
    ("Giant Buffalo",       "68-71"),
    ("Mindgazer",           "69-72"),
    ("Nightmare Bats",      "69-72"),
    ("Akselloak",           "71-74"),
    ("Srei Ap",             "71-76"),
    ("Demon's Elemental",   "72-74"),
    ("Tyrannotaur",         "72-75"),
    ("Fachan",              "73-75"),
    ("Doom Mage",           "73-76"),
    ("Dread Demon",         "73-76"),
    ("Gore Demon",          "73-76"),
    ("Judicator Demon",     "73-76"),
    ("Stygian Demon",       "73-76"),
    ("Agloolik",            "77-80"),
    ("King Buffalo",        "79-82"),
    ("Molech",              "79-82"),
    ("Smolenkos",           "80-82"),
    ("Kindred Black Mage",  "81-84"),
    ("Kindred Dark Knight", "81-84"),
    ("Kindred Summoner",    "81-84"),
    ("Kindred Warrior",     "81-84"),
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
    ('frost flambeau',    '74'),      # NM, ZERO zones (nmlv 74)
    ('magnotaur',         '~83'),     # NM, ZERO zones; page prints the tilde -> stored verbatim
    ('skvader',           '77-78'),   # NM, ZERO zones (nmlv 77-78)
    ('ice elemental',     '66-84'),   # rule 2: 66-68 U 82-84
    ("demon's elemental", '72-74'),
]
WRITES_LEVEL = [
    ('jormungand',          None,    '95'),
    ('uleguerand tiger',    '59-62', '60-63'),
    ('doom soldier',        '73-76', '66-70'),   # was Doom Mage's band
    ('nival raptor',        '66-69', '68-70'),
    ('molech',              '78-81', '79-82'),
    ('smolenkos',           '79-80', '80-82'),   # its own lv [80,82] already matched the page
    ('kindred black mage',  '79-83', '81-84'),   # all four Kindred share one stamp — all four wrong
    ('kindred dark knight', '79-83', '81-84'),
    ('kindred summoner',    '79-83', '81-84'),
    ('kindred warrior',     '79-83', '81-84'),
]
LV_EXTEND = [
    ('uleguerand tiger', [59, 63]),
    ('nival raptor',     [66, 70]),
    ('molech',           [78, 82]),
    ('ice elemental',    [38, 84]),
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
    for k, lv in LV_EXTEND:
        print('LV EXTEND ', k, mobs[k].get('lv'), '->', lv)
        mobs[k]['lv'] = lv
    assert not [1 for mm in mobs.values() for v in mm.values() if v is None]
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, separators=(', ', ': '), ensure_ascii=False)
    print('written', p)


if len(sys.argv) > 1 and sys.argv[1] == 'apply':
    apply()
