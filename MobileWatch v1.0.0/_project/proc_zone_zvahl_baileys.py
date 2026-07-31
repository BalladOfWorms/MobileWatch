#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 294 — zone pass: Castle Zvahl Baileys.
Zone string per zones.json = 'Castle Zvahl Baileys'.
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'Castle Zvahl Baileys'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Duke Haborym",         "76", "Timed (21-24 hrs)"),
    ("Grand Duke Batym",     "76", "Timed (21-24 hrs)"),
    ("Marquis Allocen",      "76", "Timed (21-24 hrs)"),
    ("Marquis Amon",         "76", "Timed (21-24 hrs)"),
    ("Likho",                SKIP, "unknown"),
    ("Marquis Naberius",     "74", "Timed (1-2 hrs)"),
    ("Marquis Sabnock",      SKIP, "Lottery (Abyssal/Doom/Blood Demon)"),
    ("Dark Spark",           "55", "Quest (Borghertz artifact hands)"),
    ("Marquis Andrealphus",  SKIP, "Quest (Better the Demon You Know)"),
    ("Demon Banneret",       SKIP, "Quest (Better the Demon You Know)"),
    ("Demon Secretary",      SKIP, "Quest (Better the Demon You Know)"),
]

ADV = [
    ("Goblin's Bats",       "40-42"),
    ("Demon's Elemental",   "43-54"),   # rule 2: 43-45 (assists Demon Warlock) U 52-54 (assists Demon Magistrate)
    ("Evil Eye",            "46-48"),
    ("Elder Quadav",        "47-49"),
    ("Emerald Quadav",      "47-49"),
    ("Goblin Poacher",      "47-49"),
    ("Goblin Reaper",       "47-49"),
    ("Goblin Robber",       "47-49"),
    ("Goblin Trader",       "47-49"),
    ("Iron Quadav",         "47-49"),
    ("Orcish Bowshooter",   "47-49"),
    ("Orcish Footsoldier",  "47-49"),
    ("Orcish Gladiator",    "47-49"),
    ("Orcish Trooper",      "47-49"),
    ("Spinel Quadav",       "47-49"),
    ("Yagudo Conquistador", "47-49"),
    ("Yagudo Lutenist",     "47-49"),
    ("Yagudo Prior",        "47-49"),
    ("Yagudo Zealot",       "47-49"),
    ("Dark Elemental",      "48-49"),
    ("Ice Elemental",       "48-49"),
    ("Demon Pawn",          "48-52"),
    ("Demon Knight",        "50-52"),
    ("Demon Warlock",       "50-52"),
    ("Demon Wizard",        "50-52"),
    ("Morbid Eye",          "52-55"),
    ("Demon Chancellor",    "57-59"),
    ("Demon Commander",     "57-59"),
    ("Demon General",       "57-59"),
    ("Demon Magistrate",    "57-59"),
    ("Ahriman",             "63-65"),
    ("Abyssal Demon",       "64-66"),
    ("Arch Demon",          "64-66"),
    ("Blood Demon",         "64-66"),
    ("Doom Demon",          "64-66"),
    ("Dread Demon",         "71-73"),
    ("Gore Demon",          "71-73"),
    ("Judicator Demon",     "71-73"),
    ("Stygian Demon",       "71-73"),
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
    ('marquis naberius',  '74'),      # NM, ZERO zones (nmlv 74)
    ('marquis sabnock',   None),      # NM, ZERO zones, page publishes no level
    ("demon's elemental", '43-54'),   # ZERO zones; rule 2 merge of the two pet blocks
    ('dark elemental',    '48-49'),
    ('ice elemental',     '48-49'),
]
WRITES_LEVEL = [
    ('dark spark',  None,    '55'),      # nmlv already 55
    ('evil eye',    '48',    '46-48'),   # stored a POINT where the page publishes a band
    ('demon pawn',  '50-52', '48-52'),   # shared-stamp artifact: identical to Knight/Wizard
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
