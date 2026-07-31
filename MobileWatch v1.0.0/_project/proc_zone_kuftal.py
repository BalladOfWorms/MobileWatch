#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 293a — zone pass: Kuftal Tunnel.
Zone string per zones.json = 'Kuftal Tunnel'.
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'Kuftal Tunnel'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Amemet",               "66",    "Lottery (Sand Lizard)"),
    ("Arachne",              "69-70", "Lottery (Recluse Spider)"),
    ("Bloodthirster Madkix", "69-72", "Lottery (Goblin Mercenary)"),
    ("Cancer",               "65",    "Forced (trade Quus to ???)"),
    ("Guivre",               "82-83", "Timed (21-24 hrs)"),
    ("Pelican",              "80-81", "Lottery (Greater Cockatrice)"),
    ("Phantom Worm",         "70-72", "Forced (trade Darksteel Ore to ???)"),
    ("Sabotender Mariachi",  "68-70", "Lottery (Sabotender Sediendo)"),
    ("Yowie",                "69-71", "Lottery (Deinonychus)"),
    ("Dervo's Ghost",        "68",    "Mission (Bastok 8-2)"),
    ("Gizerl's Ghost",       "68",    "Mission (Bastok 8-2)"),
    ("Gordov's Ghost",       "68",    "Mission (Bastok 8-2)"),
    ("Kettenkaefer",         SKIP,    "Quest (The Potential Within)"),
    ("Specter Worm",         "125",   "UNM (2,100 Unity Accolades)"),
    ("Tangaroa",             SKIP,    "Voidwatch (Ashen stratum abyssite + Voidstone)"),
]

ADV = [
    ("Goblin's Spider",      "53-55"),
    ("Cave Worm",            "60-63"),
    ("Robber Crab",          "60-63"),
    ("Sand Lizard",          "61-64"),
    ("Haunt",                "63-66"),
    ("Recluse Spider",       "63-66"),
    ("Sabotender Sediendo",  "64-67"),
    ("Deinonychus",          "65-68"),
    ("Goblin Alchemist",     "66-69"),
    ("Goblin Bandit",        "66-69"),
    ("Goblin Mercenary",     "66-69"),
    ("Goblin Tamer",         "66-69"),
    ("Kuftal Digger",        "66-69"),
    ("Air Elemental",        "68-70"),
    ("Fire Elemental",       "68-70"),
    ("Diplopod",             "68-71"),
    ("Ovinnik",              "77-79"),
    ("Machairodus",          "90-?"),   # half-known Lv form — see the rev header
    ("Kuftal Delver",        "90-?"),
    ("Greater Cockatrice",   "78-80"),
    ("Ladon",                "80-82"),
    ("Scavenger Crab",       "60-62"),   # Fished Up
    ("Stygian Pugil",        "64-66"),   # Fished Up
    ("Devil Manta",          "66-68"),   # Fished Up
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
    ('guivre',          '82-83'),   # NM, ZERO zones before
    ("goblin's spider", '53-55'),
    ('air elemental',   '68-70'),
    ('fire elemental',  '68-70'),
    # `90-?` is a HALF-known cell: the record's own lv (99-103 / 99-102) is more precise than
    # the page's floor, so rule 116 keeps lv and the entry goes in level-less (rule 11).
    ('machairodus',     None),
    ('kuftal delver',   None),
    ('ladon',           '80-82'),
]
WRITES_LEVEL = [
    ("dervo's ghost",  None,    '68'),
    ("gizerl's ghost", None,    '68'),
    ("gordov's ghost", None,    '68'),
    ('goblin tamer',   '66-68', '66-69'),
]
LV_EXTEND = [("goblin's spider", [38, 55])]   # rule 9: Eastern Altepa 38-40 U Kuftal 53-55


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
