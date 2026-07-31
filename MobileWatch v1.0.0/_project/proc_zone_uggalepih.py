#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 299 — zone pass: Temple of Uggalepih.
Zone string per zones.json = 'Temple of Uggalepih'.
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'Temple of Uggalepih'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Beryl-footed Molberry",    "75", "Forced (trade Tonberry Rattle to ???)"),
    ("Bonze Marberry",           "66", "Timed (5 min)"),
    ("Crimson-toothed Pawberry", "70", "Forced (trade Uggalepih Offering to ???)"),
    ("Death from Above",         "62", "Forced (trade Bee Larvae to ???)"),
    # page prints 60, but the stored 59-60 wins: the record's own nmlv READS 59-60 and backs the
    # range (Frogamander shape, rev-279 tie-breaker). Row kept at 59-60 so re-runs stay clean.
    ("Flauros",                  "59-60", "Lottery (Torama)"),
    ("Habetrot",                 "58", "Forced (trade a stack of La Theine Cabbage to ???)"),
    ("Manipulator",              "60", "Timed (~2 hrs)"),
    ("Sacrificial Goblet",       "67", "Forced (trade Uggalepih Whistle to ???)"),
    ("Sozu Rogberry",            "66", "Forced (trade Flickering Lantern to ???)"),
    ("Sozu Sarberry",            "66", "Lottery (Tonberry Cutter)"),
    ("Sozu Terberry",            "65", "Lottery (Tonberry Harrier)"),
    ("Tonberry Kinq",            "65", "Lottery (Tonberry Dismayer)"),   # KinQ, not King
    ("Cleuvarion M Resoaix",     "63", "Quest (Knight Stalker)"),
    ("Nio-A",                    "70", "Mission (San d'Oria 8-2)"),
    ("Nio-Hum",                  "70", "Mission (San d'Oria 8-2)"),
    ("Rompaulion S Citalle",     "63", "Quest (Knight Stalker)"),
    ("Trompe L'Oeil",            "60", "Quest (A Question of Taste)"),
    ("Yallery Brown",            "80", "Quest (Axe the Competition)"),
    ("Azure-toothed Clawberry",  "125","UNM (2,100 Unity Accolades)"),
    ("Neith",                    SKIP, "Voidwatch (Ashen stratum abyssite + Voidstone)"),
]

ADV = [
    ("Tonberry's Elemental", "43-55"),
    ("Temple Opo-opo",       "51-54"),
    ("Tonberry Cutter",      "51-59"),
    ("Tonberry Harrier",     "51-59"),
    ("Tonberry Stalker",     "51-59"),
    ("Wespe",                "52-55"),
    ("Rumble Crawler",       "53-56"),
    ("Branding Iron",        "55-58"),
    ("Torama",               "55-58"),
    ("Temple Bee",           "60-63"),
    ("Water Elemental",      "61-64"),
    ("Tonberry Dismayer",    "61-67"),
    ("Tonberry Maledictor",  "61-67"),
    ("Tonberry Pursuer",     "61-67"),
    ("Tonberry Stabber",     "61-67"),
    ("Hover Tank",           "64-67"),
    ("Iron Maiden",          "64-68"),
    ("Temple Guardian",      "65"),
    ("Fire Elemental",       "65-68"),
    ("Uggalepih Leech",      "50-52"),   # Fished Up
    ("Bloodsucker",          "55-62"),   # rule 2: Fished Up 55-57 U 60-62
    ("Bouncing Ball",        "65-67"),   # Fished Up
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
    ('cleuvarion m resoaix', '63'),      # ZERO zones (nmlv 63)
    ('rompaulion s citalle', '63'),      # ZERO zones (nmlv 63)
    ("tonberry's elemental", '43-55'),
    ('water elemental',      '61-64'),
    ('fire elemental',       '65-68'),
]
WRITES_LEVEL = [
    ("trompe l'oeil",         None,    '60'),
    ('yallery brown',         None,    '80'),
    # rule 107/116 + the rev-279 tie-breaker: stored range CONTAINS the page value and the record's
    # own nmlv BACKS THE PAGE -> the page wins.  (`flauros` is the one where nmlv backs the RANGE.)
    ('beryl-footed molberry', '73-75', '75'),
    ('habetrot',              '57-59', '58'),
    ('sozu rogberry',         '65-66', '66'),
    ('rumble crawler',        '53-55', '53-56'),   # 53-55 == its Crawlers Nest entry (rule 3)
]
# NOT WRITTEN: `flauros` 59-60 -> 60. nmlv reads 59-60 and BACKS THE RANGE (Frogamander shape).


def apply():
    p, d = load()
    mobs = d['mobs']
    # --- rule 7: five records hold a NON-CANONICAL zone string, each minting a phantom bucket ---
    fixes = 0
    rec = mobs['sacrificial goblet']
    for e in rec['zones']:
        if e[0] == 'The Temple of Uggalepih':
            e[0], e[1] = ZONE, '67'          # nmlv reads 67 and backs the page
            fixes += 1
    for e in mobs['hrungnir']['zones']:      # curly U+2019 apostrophes
        if '\u2019' in e[0]:
            e[0] = e[0].replace('\u2019', "'")
            fixes += 1
    mobs['bumba']['zones'] = [['Sheol - Gaol']]   # held BOTH ['Sheol Gaol'] and the bare string
    fixes += 1
    print('ZONE-STRING FIXES', fixes)

    for k, lvl in WRITES_ZONE:
        r = mobs[k]
        assert zentry(r) is None, k
        r.setdefault('zones', [])
        r['zones'].append([ZONE, lvl] if lvl else [ZONE])
        print('ZONE ADD  ', k, lvl)
    for k, old, new in WRITES_LEVEL:
        r = mobs[k]
        e = zentry(r)
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
