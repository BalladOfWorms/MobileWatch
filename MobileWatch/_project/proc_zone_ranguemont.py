#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 284 — zone pass: Ranguemont Pass.
Zone string per zones.json = 'Ranguemont Pass'.
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'Ranguemont Pass'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Taisaijin",      "60-63", "Special (morphs from Taisai after 23-25 hr undisturbed)"),
    ("Mucoid Mass",    "45-48", "Timed (90-100 min)"),
    ("Gloom Eye",      SKIP,    "Lottery (Seeker Bats, 1-1.5 hr)"),
    ("Hyakume",        SKIP,    "Lottery (Hecteyes)"),
    ("Metallic Slime", SKIP,    "Quest (Blighted Gloom)"),
    ("Tros",           "44",    "Quest (Painful Memory)"),
]

ADV = [
    ("Wind Bats",         "3-5"),
    ("Blade Bat",         "4-7"),
    ("Goblin Thug",       "4-8"),
    ("Goblin Weaver",     "4-8"),
    ("Oil Slick",         "7-9"),
    ("Goblin's Bats",     "25-27"),
    ("Seeker Bats",       "25-28"),
    ("Goblin Gambler",    "26-30"),
    ("Goblin Leecher",    "26-30"),
    ("Goblin Mugger",     "26-30"),
    ("Ooze",              "28-30"),
    ("Cave Scorpion",     "30-33"),
    ("Stirge",            "30-33"),
    ("Hecteyes",          "31-34"),
    ("Goblin Furrier",    "32-34"),
    ("Goblin Pathfinder", "32-34"),
    ("Goblin Shaman",     "32-34"),
    ("Goblin Smithy",     "32-34"),
    ("Floating Eye",      "34-36"),
    ("Evil Weapon",       "35-37"),
    ("Taisai",            "35-38"),
    ("Giant Scorpion",    "38-40"),
    ("Goblin Hoodoo",     "86-90"),
    ("Bilesucker",        "87-92"),
    ("Hovering Oculus",   "87-92"),
    ("Goblin Artificer",  "88-90"),
    ("Goblin Chaser",     "88-90"),
    ("Goblin Tanner",     "88-90"),
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
    ('mucoid mass',      '45-48'),   # NM with nmlv 45-48 and ZERO zones
    ('goblin hoodoo',    '86-90'),   # the 86-92 high-tier block: all six had ZERO zones
    ('bilesucker',       '87-92'),
    ('hovering oculus',  '87-92'),
    ('goblin artificer', '88-90'),
    ('goblin chaser',    '88-90'),
    ('goblin tanner',    '88-90'),
]
WRITES_LEVEL = [
    ('tros', None, '44'),            # zone held a null level; nmlv already 44
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
