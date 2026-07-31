#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 291b — zone pass: Grand Palace of Hu'Xzoi.
Zone string per zones.json = 'Grand Palace of HuXzoi' (no apostrophe).
Rows transcribed from the user's three BG-wiki screenshots (NM table + Adversaries).
SKIP = page publishes no level -> ensure zone, NEVER touch a stored level (rule 15).
"""
import json, sys, os

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
ZONE = 'Grand Palace of HuXzoi'
SKIP = 'SKIP'

# (page name, page level or SKIP, note)
NM = [
    ("Ix'aern (MNK)",         SKIP, "Forced (trade 1-3 HQ Aern Organs to ???)"),
    ("Jailer of Temperance",  "85", "Lottery (Eo'zdei)"),
    ("Ix'ghrah",              SKIP, "Mission (Promathia 8-2)"),
]

ADV = [
    ("Aern's Elemental", SKIP),   # Lv cell reads ?-?  (rule 10)
    ("Aern's Euvhi",     SKIP),
    ("Aern's Wynav",     SKIP),
    ("Eo'euvhi",         "74-76"),
    ("Eo'ghrah",         "75-77"),
    ("Eo'zdei",          "77-78"),
    ("Eo'aern",          "79-81"),   # rule 2: four job rows, all 79-81
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
# NOT WRITTEN: Ix'aern (MNK) — see proc_zone_ruhmet.py; one `ix'aern` record covers all three.
WRITES_ZONE = [("aern's elemental", None)]     # page Lv reads ?-?
WRITES_LEVEL = [
    ("eo'ghrah", '75-76', '75-77'),
    ("eo'aern",  '79-82', '79-81'),
]
LV_EXTEND = [("eo'ghrah", [75, 77])]   # rule 9


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
        e[1] = new
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
