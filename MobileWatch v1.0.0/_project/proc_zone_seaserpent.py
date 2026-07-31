#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 285 — zone pass: Sea Serpent Grotto.
Zone string per zones.json = 'Sea Serpent Grotto'.
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'Sea Serpent Grotto'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Abyss Sahagin",         "72-74", "Timed (16-21 min)"),
    ("Charybdis",             "80-81", "Lottery (Devil Manta, every 8 hrs)"),
    ("Coral Sahagin",         "72-74", "Timed (16-21 min)"),
    ("Denn the Orcavoiced",   "64-65", "Lottery (Coastal Sahagin)"),
    ("Fyuu the Seabellow",    "48",    "Lottery (Riparian Sahagin)"),
    ("Masan",                 "39-40", "Lottery (Royal Leech)"),
    ("Mouu the Waverider",    "64-66", "Lottery (Bog Sahagin)"),
    ("Namtar",                "40-41", "Lottery (Ghast, 1 hr minimum)"),
    ("Novv the Whitehearted", "67",    "Timed (2+ hrs)"),
    ("Ocean Sahagin",         "75",    "Timed (21-24 hrs)"),
    ("Pahh the Gullcaller",   "57",    "Lottery (Bog Sahagin)"),
    ("Qull the Shellbuster",  "49-51", "Lottery (Brook Sahagin)"),
    ("Sea Hog",               "62",    "Lottery (Razorjaw Pugil)"),
    ("Seww the Squidlimbed",  "48",    "Lottery (Riparian Sahagin)"),
    ("Voll the Sharkfinned",  "64-66", "Lottery (Marsh Sahagin)"),
    ("Worr the Clawfisted",   "61",    "Lottery (Marsh/Bog/Swamp Sahagin)"),
    ("Wuur the Sandcomber",   "48-50", "Lottery (Spring Sahagin)"),
    ("Yarr the Pearleyed",    "64-66", "Lottery (Lagoon Sahagin)"),
    ("Zuug the Shoreleaper",  "70",    "Lottery (Sahagin, exact unknown)"),
    ("Glyryvilu",             "<52",   "Quest (An Undying Pledge) - Lv cell literally reads <52"),
    ("Water Leaper",          "80-82", "Quest (Methods Create Madness)"),
    ("Bakunawa",              "125",   "UNM (2,100 Unity Accolades)"),
]

ADV = [
    ("Royal Leech",        "35-38"),
    ("Lake Sahagin",       "36-39"),
    ("Pond Sahagin",       "36-39"),
    ("Spring Sahagin",     "36-39"),
    ("Undead Bats",        "36-39"),
    ("Ironshell",          "37-40"),
    ("Ghast",              "38-41"),   # rule 2: BLM row + WAR row, same band
    ("Ooze",               "39-42"),
    ("Brook Sahagin",      "41-48"),
    ("Rivulet Sahagin",    "41-48"),
    ("Vampire Bat",        "42-45"),
    ("Bigclaw",            "43-48"),   # rule 2: ground 43-48 U Fished Up 43-47
    ("Grotto Pugil",       "44-47"),
    ("Riparian Sahagin",   "44-48"),
    ("Sea Bonze",          "47-50"),
    ("Sahagin Parasite",   "50-53"),
    ("Bog Sahagin",        "52-59"),
    ("Marsh Sahagin",      "52-59"),
    ("Swamp Sahagin",      "52-59"),
    ("Rock Crab",          "53-58"),   # rule 2: ground U Fished Up 55-57; see rev header on the 53/54 read
    ("Blubber Eyes",       "55-58"),
    ("Thunder Elemental",  "55-58"),
    ("Razorjaw Pugil",     "57-60"),
    ("Sahagin's Wyvern",   "58-60"),
    ("Mousse",             "62-65"),
    ("Robber Crab",        "62-67"),
    ("Coastal Sahagin",    "62-72"),
    ("Delta Sahagin",      "62-72"),
    ("Lagoon Sahagin",     "62-72"),
    ("Shore Sahagin",      "62-72"),
    ("Dire Bat",           "63-66"),
    ("Water Elemental",    "65-68"),
    ("Devil Manta",        "66-69"),
    ("Greatclaw",          "66-69"),
    ("Mindgazer",          "66-69"),
    ("Nightmare Bats",     "66-69"),
    ("Big Jaw",            "35-37"),   # Fished Up
    ("Stygian Pugil",      "65-67"),   # Fished Up
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
    ('thunder elemental', '55-58'),
    ("sahagin's wyvern",  '58-60'),   # ZERO zones before
    ('water elemental',   '65-68'),
]
WRITES_LEVEL = [
    ('glyryvilu',   None,    '<52'),   # nmlv already stores the literal "<52"
    ('water leaper', None,   '80-82'),
    ('ooze',        '29-42', '39-42'),
]
LV_EXTEND = [('water leaper', [80, 82])]   # rule 9: page 80-82, nmlv 80-82, only zone


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
