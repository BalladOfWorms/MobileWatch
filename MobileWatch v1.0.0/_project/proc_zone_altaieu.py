#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 290 — zone pass: Al'Taieu.
Zone string per zones.json = 'AlTaieu' (no apostrophe).
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'AlTaieu'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Absolute Virtue",    "95", "Special (defeat Jailer of Love)"),
    ("Aw'euvhi",           SKIP, "Timed (5 min)"),
    ("Jailer of Hope",     SKIP, "Forced (trade)"),
    ("Jailer of Justice",  SKIP, "Forced (trade)"),
    ("Jailer of Love",     SKIP, "Forced (trade)"),
    ("Jailer of Prudence", SKIP, "Forced (trade)"),
    ("Om'yovra",           "87", "Timed (30 min)"),
    ("Ul'yovra",           "82", "Timed (1 hr)"),
    ("Ru'aern",            SKIP, "Mission (Promathia 8-1)"),
]

ADV = [
    ("Aern's Elemental", "63-67"),
    ("Aern's Xzomit",    "64-73"),
    ("Aern's Wynav",     "65-73"),
    ("Ul'xzomit",        "68-71"),
    ("Ul'hpemde",        "68-72"),
    ("Ul'aern",          "70-73"),   # rule 2: SIX job rows, all 70-73
    ("Om'xzomit",        "73-76"),
    ("Om'hpemde",        "73-77"),
    ("Ul'phuabo",        "75-76"),
    ("Om'aern",          "75-78"),   # rule 2: SIX job rows, all 75-78
    ("Om'phuabo",        "79-81"),
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
    ("aern's elemental", '63-67'),   # ZERO zones before
]
WRITES_LEVEL = [
    ('absolute virtue', None,    '95'),      # nmlv 95; stored lv [92,92] is the stale one
    ("om'yovra",        None,    '87'),      # nmlv 87; stored lv [84,85] stale
    ("aern's wynav",    None,    '65-73'),
    ("ul'yovra",        '79-82', '82'),      # nmlv 82
    ("ul'hpemde",       '68-76', '68-72'),   # own lv [68,72] already matched the page
    ("om'xzomit",       '74-76', '73-76'),
    ("ul'phuabo",       '75-77', '75-76'),   # own lv [75,76] already matched the page
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
