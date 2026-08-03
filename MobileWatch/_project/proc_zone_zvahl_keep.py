#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 295 — zone pass: Castle Zvahl Keep.
Zone string per zones.json = 'Castle Zvahl Keep'.
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'Castle Zvahl Keep'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Baron Vapula",   "68", "Lottery (Demon Wizard)"),
    ("Baronet Romwe",  "68", "Lottery (Demon Pawn)"),
    ("Count Bifrons",  "68", "Lottery (Demon Knight)"),
    ("Viscount Morax", "68", "Lottery (Demon Warlock)"),
]

ADV = [
    ("Goblin's Bat",         "40-42"),
    ("Demon's Elemental",    "45-53"),
    ("Evil Eye",             "46-48"),
    ("Elder Quadav",         "47-49"),
    ("Emerald Quadav",       "47-49"),
    ("Goblin Poacher",       "47-49"),
    ("Goblin Reaper",        "47-49"),
    ("Goblin Robber",        "47-49"),
    ("Goblin Trader",        "47-49"),
    ("Iron Quadav",          "47-49"),
    ("Orcish Bowshooter",    "47-49"),
    ("Orcish Footsoldier",   "47-49"),
    ("Orcish Gladiator",     "47-49"),
    ("Orcish Trooper",       "47-49"),
    ("Spinel Quadav",        "47-49"),
    ("Yagudo Conquistador",  "47-49"),
    ("Yagudo Lutenist",      "47-49"),
    ("Yagudo Prior",         "47-49"),
    ("Yagudo Zealot",        "47-49"),
    ("Goblin Bouncer",       "50-52"),
    ("Goblin Enchanter",     "50-52"),
    ("Goblin Hunter",        "50-52"),
    ("Gold Quadav",          "50-52"),
    ("Mythril Quadav",       "50-52"),
    ("Orcish Predator",      "50-52"),
    ("Orcish Veteran",       "50-52"),
    ("Orcish Warchief",      "50-52"),
    ("Orcish Zerker",        "50-52"),
    ("Steel Quadav",         "50-52"),
    ("Topaz Quadav",         "50-52"),
    ("Yagudo Abbot",         "50-52"),
    ("Yagudo Chanter",       "50-52"),
    ("Yagudo Inquisitor",    "50-52"),
    ("Yagudo Sentinel",      "50-52"),
    ("Morbid Eye",           "52-53"),
    ("Demon Knight",         "52-56"),
    ("Demon Pawn",           "52-56"),
    ("Demon Warlock",        "52-56"),
    ("Demon Wizard",         "52-56"),
    ("Deadly Iris",          "55-56"),
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
WRITES_ZONE = [("demon's elemental", '45-53')]


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
