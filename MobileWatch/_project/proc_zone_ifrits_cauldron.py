#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 298b — zone pass: Ifrit's Cauldron.
Zone string per zones.json = 'Ifrits Cauldron' (check zones.json).
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'Ifrits Cauldron'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Ash Dragon",       "85",    "Timed (~72 hrs)"),
    ("Bomb Bastard",     SKIP,    "Summoned by Bomb Queen"),
    ("Bomb Prince",      SKIP,    "Summoned by Bomb Queen"),
    ("Bomb Princess",    SKIP,    "Summoned by Bomb Queen"),
    ("Bomb Queen",       "80-81", "Forced (Bomb Queen Core + 3 Bomb Queen Ash)"),
    ("Foreseer Oramix",  "71-72", "Lottery (Goblin Alchemist)"),
    ("Lindwurm",         "74-76", "Lottery (Eotyrannus)"),
    ("Tarasque",         "72-74", "Forced (trade Rattling Egg to ???)"),
    ("Tyrannic Tunnok",  "75",    "Lottery (Sulfur Scorpion)"),
    ("Vouivre",          "79-80", "Lottery (Hurricane Wyvern)"),
    ("Cailleach Bheur",  "82",    "Quest (Blood and Glory)"),
    ("Magma",            "65",    "Mission (Bastok 6-2)"),
    ("Salamander",       SKIP,    "Mission (Bastok 6-2)"),
    ("Coca",             "125",   "UNM (2,100 Unity Accolades)"),
    ("Ildebrann",        SKIP,    "Voidwatch (Ashen stratum abyssite + Voidstone)"),
]

ADV = [
    ("Goblin's Bats",    "53-55"),
    ("Dire Bat",         "60-64"),
    ("Volcano Wasp",     "61-64"),
    ("Old Opo-opo",      "61-65"),
    ("Volcanic Gas",     "62-68"),
    ("Dodomeki",         "63-69"),
    ("Goblin Alchemist", "66-69"),
    ("Goblin Bandit",    "66-69"),
    ("Goblin Mercenary", "66-69"),
    ("Goblin Shepherd",  "66-69"),
    ("Nightmare Bats",   "68-72"),
    ("Eotyrannus",       "70-73"),
    ("Sulfur Scorpion",  "70-73"),
    ("Volcanic Bomb",    "71-78"),
    ("Ash Lizard",       "73-76"),
    ("Hurricane Wyvern", "75-78"),
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
    ('vouivre',          '79-80'),   # NM, ZERO zones (nmlv 79-80)
    ('hurricane wyvern', '75-78'),   # Vouivre's PLACEHOLDER, also ZERO zones (rule 125)
    ('magma',            '65'),      # held only Garlaige Citadel — see the rev header
    ('salamander',       None),      # NM, ZERO zones, page publishes no level
]
WRITES_LEVEL = [
    ('cailleach bheur', None,    '82'),
    # rule 107/116 + the rev-279 tie-breaker: the stored range CONTAINS the page value and the
    # record's own nmlv reads 75, BACKING THE PAGE -> the page wins (Centurio shape).
    ('tyrannic tunnok', '73-76', '75'),
    ('eotyrannus',      '70-72', '70-73'),
]
LV_EXTEND = [('eotyrannus', [70, 73])]


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
