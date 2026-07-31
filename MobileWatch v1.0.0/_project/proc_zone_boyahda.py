#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 287 — zone pass: The Boyahda Tree.
Zone string per zones.json = 'The Boyahda Tree'.
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'The Boyahda Tree'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Ancient Goobbue",   "78-80",  "Timed (21-24 hrs)"),
    ("Aquarius",          "69-71",  "Lottery (Robber Crab)"),
    ("Ellyllon",          "66",     "Lottery (Death Cap)"),
    ("Leshonki",          "79-81",  "Lottery (Boyahda Sapling)"),
    ("Unut",              "72",     "Lottery (Moss Eater)"),
    ("Voluptuous Vivian", "80",     "Lottery (Demonic Rose)"),
    ("Agas",              "~70-80", "Quest (Searching for the Right Words)"),
    ("Beet Leafhopper",   "75",     "Quest (Shoot First, Ask Questions Later)"),
    ("Ayapec",            "125",    "UNM (2,100 Unity Accolades)"),
    ("Hidhaegg",          "135",    "UNM (3,100 Unity Accolades)"),
    ("Modron",            SKIP,     "Voidwatch (Ashen stratum abyssite II + Voidstone)"),
]

ADV = [
    ("Bark Spider",          "60-63"),
    ("Death Cap",            "60-63"),
    ("Moss Eater",           "62-66"),
    ("Robber Crab",          "62-66"),
    ("Knight Crawler",       "62-67"),
    ("Mourioche",            "62-68"),
    ("Old Goobbue",          "65-68"),
    ("Morbol Menace",        "67-70"),
    ("Thunder Elemental",    "69-72"),
    ("Water Elemental",      "69-72"),
    ("Skimmer",              "72-74"),
    ("Korrigan",             "72-75"),
    ("Processionaire",       "72-75"),
    ("Mourning Crawler",     "103-105"),
    ("Steelshell",           "73-76"),
    ("Viseclaw",             "102-105"),
    ("Boyahda Sapling",      "74-77"),
    ("Elder Goobbue",        "74-77"),
    ("Bark Tarantula",       "75-78"),
    ("Blood Ball",           "75-78"),
    ("Darter",               "75-78"),
    ("Demonic Rose",         "75-78"),
    ("Snaggletooth Peapuk",  "102-105"),
    ("Scavenger Crab",       "60-62"),   # Fished Up
    ("Stygian Pugil",        "60-62"),   # Fished Up
    ("Bouncing Ball",        "65-67"),   # Fished Up
    ("Demonic Pugil",        "70-78"),   # rule 2: THREE Fished Up rows, 70-72 U 76-78 U 76-78
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
    ('thunder elemental',   '69-72'),
    ('water elemental',     '69-72'),
    ('viseclaw',            '102-105'),   # ZERO zones before (and fam=None)
    ('snaggletooth peapuk', '102-105'),   # ZERO zones before
]
WRITES_LEVEL = [
    ('agas',           None,    '~70-80'),  # nmlv already ~70-80
    ('beet leafhopper', None,   '75'),
    ('bark tarantula', '75-79', '75-78'),
    ('stygian pugil',  '64-66', '60-62'),   # rule 3: 64-66 == its Kuftal Tunnel entry
    ('bouncing ball',  '76-78', '65-67'),   # took the Demonic Pugil row's value
    ('demonic pugil',  '65-72', '70-78'),   # took Bouncing Ball's 65 as its min
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
