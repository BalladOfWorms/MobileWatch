#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 283 — zone pass: Pso'Xja.
Zone string per zones.json = 'PsoXja' (no apostrophe).
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'PsoXja'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Golden-tongued Culberry", "84-85", "Forced (trade Odorous Knife to ???)"),
    ("Gyre-Carlin",             "50",    "Lottery (Diremite)"),
    ("Gargoyle-Iota",           SKIP,    "Quest (A Reputation in Ruins)"),
    ("Gargoyle-Kappa",          SKIP,    "Quest (A Reputation in Ruins)"),
    ("Gargoyle-Lambda",         SKIP,    "Quest (A Reputation in Ruins)"),
    ("Gargoyle-Mu",             SKIP,    "Quest (A Reputation in Ruins)"),
    ("Nunyunuwi",               "50",    "Mission (Promathia 5-1)"),
]

ADV = [
    ("Tonberry's Elemental",  SKIP),   # Lv cell reads ?-?  (rule 10)
    ("Vampire Bat",           "42-44"),
    ("Diremite",              "42-45"),
    ("Maze Lizard",           "43-45"),
    ("Gazer",                 "43-46"),
    ("Snowball",              "43-46"),
    ("Camazotz",              "52-57"),
    ("Labyrinth Lizard",      "52-58"),
    ("Gargoyle",              "53-57"),
    ("Blubber Eyes",          "53-58"),
    ("Cryptonberry Cutter",   "53-59"),
    ("Cryptonberry Plaguer",  "53-59"),
    ("Cryptonberry Harrier",  "53-60"),
    ("Cryptonberry Stalker",  "53-60"),
    ("Magic Millstone",       "54-58"),
    ("Treasure Chest",        "55-60"),
    ("Talos",                 "56"),
    ("Goblin Bouncer",        "56-58"),
    ("Goblin Enchanter",      "56-58"),
    ("Goblin Hunter",         "56-58"),
    ("Goblin Jeweler",        "56-58"),
    ("Snoll",                 "57-58"),
    ("Diremite Stalker",      "57-59"),
    ("Goblin's Bat",          "58-61"),
    ("Goblin Bandit",         "62-67"),
    ("Goblin Alchemist",      "62-68"),
    ("Diremite Assaulter",    "63-68"),
    ("Goblin Mercenary",      "63-68"),
    ("Goblin Veterinarian",   "63-68"),
    ("Ice Elemental",         "63-80"),
    ("Dire Bat",              "64-68"),
    ("Thousand Eyes",         "64-68"),
    ("Morozko",               "65-66"),
    ("Maledict Millstone",    "65-68"),
    ("Snow Lizard",           "65-68"),
    ("Aura Pot",              "72-75"),
    ("Purgatory Bat",         "72-76"),
    ("Frost Lizard",          "73-77"),
    ("Diremite Dominator",    "74-77"),
    ("Million Eyes",          "74-77"),
    ("Avalanche",             "75"),
    ("Archaic Chest",         "80"),
    ("Dark Elemental",        "84-86"),
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
    # (key, level or None-for-no-level)
    ("tonberry's elemental", None),   # page Lv reads ?-?  (rule 10)
    ('ice elemental',        '63-80'),
    ('dark elemental',       '84-86'),
]
WRITES_LEVEL = [
    # (key, old, new)
    ('nunyunuwi',        None,    '50'),     # zone held a null level; nmlv already 50
    ('treasure chest',   '56-60', '55-60'),
    ('goblin mercenary', '63-67', '63-68'),
]
# 3 Millstone records store a CHARACTER-EXPLODED notes list (list(str) instead of [str]).
NOTES_STRIP = ['magic millstone', 'maledict millstone', 'demonic millstone']


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
    for k in NOTES_STRIP:
        rec = mobs[k]
        ns = rec.get('notes') or []
        assert ns and all(len(x.strip()) <= 1 for x in ns), (k, ns)
        del rec['notes']
        print('NOTES STRIP', k, '(%d single-char bullets removed)' % len(ns))
    assert not [1 for mm in mobs.values() for v in mm.values() if v is None]
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, separators=(', ', ': '), ensure_ascii=False)
    print('written', p)


if len(sys.argv) > 1 and sys.argv[1] == 'apply':
    apply()
