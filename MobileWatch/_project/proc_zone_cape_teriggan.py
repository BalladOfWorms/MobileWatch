#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 292a — zone pass: Cape Teriggan.
Zone string per zones.json = 'Cape Teriggan'.
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'Cape Teriggan'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Frostmane",               "80",    "Lottery (Greater Manticore)"),
    ("Kreutzet",                "79-80", "Timed (9-12 hrs, wind weather)"),
    ("Killer Jonny",            "82-83", "Lottery (Velociraptor, every 2 hrs)"),
    ("Tegmine",                 "71-72", "Timed (120-180 min)"),
    ("Zmey Gorynych",           SKIP,    "Timed (unknown)"),
    ("Axesarion the Wanderer",  "69-70", "Mission (Zilart 5)"),
    ("Stolas",                  "80",    "Quest (From Saplings Grow)"),
    ("Vedrfolnir",              "128",   "UNM (2,400 Unity Accolades)"),
    ("Glazemane",               "128",   "UNM (2,400 Unity Accolades)"),
]

ADV = [
    # first three rows sit above the shot's crop; values from zoneinfo, same page
    ("Goblin's Rabbit",   "48-50"),
    ("Beach Bunny",       "62-65"),
    ("Sand Lizard",       "62-66"),
    ("Robber Crab",       "64-67"),
    ("Fantasma",          "65-68"),
    ("Goblin Alchemist",  "65-68"),
    ("Goblin Bandit",     "65-68"),
    ("Goblin Mercenary",  "65-68"),
    ("Goblin Shepherd",   "65-68"),
    ("Enna-enna",         "65-69"),
    ("Velociraptor",      "66-69"),
    ("Doom Soldier",      "66-70"),
    ("Terror Pugil",      "66-70"),
    ("Air Elemental",     "67-69"),
    ("Fire Elemental",    "67-69"),
    ("Doom Mage",         "67-71"),
    ("Sand Cockatrice",   "71-74"),
    ("Greater Manticore", "76-79"),
    ("Razorjaw Pugil",    "59-60"),   # Fished Up
    ("Rock Crab",         "59-60"),   # Fished Up
    ("Stygian Pugil",     "63-67"),   # Fished Up
    ("Devil Manta",       "68-70"),   # Fished Up
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
    ('air elemental',  '67-69'),
    ('fire elemental', '67-69'),
    ('devil manta',    '68-70'),
]
WRITES_LEVEL = [
    ('stolas',         None,    '80'),      # nmlv already 80
    ('razorjaw pugil', '57-60', '59-60'),   # rule 3: 57-60 == its Sea Serpent Grotto entry
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
