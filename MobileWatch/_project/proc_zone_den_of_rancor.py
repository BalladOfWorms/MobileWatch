#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 298a — zone pass: Den of Rancor.
Zone string per zones.json = 'Den of Rancor'.
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'Den of Rancor'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Bistre-hearted Malberry", "75",    "Lottery (Tonberry Beleaguerer)"),
    ("Carmine-tailed Janberry", "66-67", "Lottery (Tonberry Imprecator)"),
    ("Celeste-eyed Tozberry",   "67-69", "Lottery (Tonberry Trailer)"),
    ("Friar Rush",              "70",    "Lottery (Bifrons)"),
    ("Hakutaku",                "85",    "Forced (trade Hakutaku Eye Cluster to ???)"),
    ("Ogama",                   SKIP,    "Lottery (Doom Toad)"),
    ("Sozu Bliberry",           "65",    "Lottery (Tonberry Imprecator)"),
    ("Tawny-fingered Mugberry", "71-73", "Lottery (Tonberry Slasher)"),
    ("Tonberry Decapitator",    "72-74", "Timed (24 min)"),
    ("Tonberry Pontifex",       "75",    "Timed (21-24 hrs)"),
    ("Tonberry Tracker",        "72-74", "Timed (24 min)"),
    ("Mokumokuren",             "80-82", "Quest (Souls in Shadow)"),
    ("Rancor Torch",            "66",    "Quest (Everyone's Grudging)"),
    ("Azrael",                  "128",   "UNM (2,400 Unity Accolades)"),
]

ADV = [
    ("Tonberry's Elemental",  "53-55"),
    ("Dire Bat",              "60-63"),
    ("Cave Worm",             "61-64"),
    ("Tonberry Imprecator",   "62-64"),
    ("Tonberry Trailer",      "62-65"),
    ("Stygian Pugil",         "63-76"),   # rule 2: ground 63-65 U 73-76
    ("Mousse",                "63-70"),   # rule 2: ground 64-67 U Fished Up 63-65 U 68-70
    ("Succubus Bats",         "65-69"),
    ("Tonberry Beleaguerer",  "66-69"),
    ("Tonberry Slasher",      "67-69"),
    ("Bifrons",               "68-70"),
    ("Cutlass Scorpion",      "68-70"),
    ("Water Elemental",       "68-73"),
    ("Fire Elemental",        "70-72"),
    ("Million Eyes",          "73-76"),
    ("Puck",                  "74-77"),
    ("Tormentor",             "75-79"),
    ("Bullbeggar",            "78-80"),
    ("Den Scorpion",          "79-81"),
    ("Doom Toad",             "79-81"),
    ("Razorjaw Pugil",        "53-55"),   # Fished Up
    ("Rock Crab",             "53-55"),   # Fished Up
    ("Bloodsucker",           "58-60"),   # Fished Up
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
    ("tonberry's elemental", '53-55'),
    ('water elemental',      '68-73'),
    ('fire elemental',       '70-72'),
]
WRITES_LEVEL = [
    ('mokumokuren',   None,    '80-82'),   # nmlv already 80-82
    ('rancor torch',  None,    '66'),      # nmlv 66; stored lv [69,73] is disjoint -> rule 9 suspended
    ('stygian pugil', '63-77', '63-76'),
    ('mousse',        '63-65', '63-70'),   # rule 2: ground 64-67 U two Fished Up blocks
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
