#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 318
Author: BalladOfWorms

TWO ZONES: Woh Gates (1 NM + 23 ADV) + Outer Ra'Kaznar (1 NM + 18 ADV).

ZONE STRING NOTE: `Outer RaKaznar` is written WITHOUT the apostrophe because that is
the zones.json spelling and the form all 10 pre-existing entries already use.  Writing
`Outer Ra'Kaznar` would create a second bucket in the Zone view (rule 7).

The Outer Ra'Kaznar [U] Skirmish / Vagary roster (5 NM + 8 regular) is NOT touched here:
none of those 13 records exists.  Flagged, not built - see the handoff.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

WOH = 'Woh Gates'
OUTER = 'Outer RaKaznar'

WOH_ROWS = {
    'cowll hippogryph': SKIP,
    'apex jagil': '131-133',
    'apex toad': '131-133',
    'bergschrund gefyrst': '126',
    'bound twitherym': '121-123',
    'cliffclinger toad': '124-125',
    'drusy twitherym': '125-126',
    'draftrider bat': '110',
    'malodorous tarichuk': '121-123',
    'metalcruncher worm': '124-126',
    'nesting hippogryph': '123-125',
    'pestiferous acuex': SKIP,
    'powdery snoll': '125',
    'schorl umbril': '122-124',
    'serac rabbit': '124-126',
    'slabspitter jagil': '121-123',
    'soundsplitter bat': '121-123',
    'talus tarichuk': SKIP,
    'wayward dullahan': '121-123',
    'wheezing acuex': SKIP,
    'velkk abyssal': '131-133',
    'velkk junglemancer': '131-133',
    'velkk mindmelter': '131-133',
    'velkk tearlicker': '131-133',
}

OUTER_ROWS = {
    'suspended sculpture': SKIP,
    'apex bat': '134-136',
    'apex ironclad': '134-136',
    'apex twitherym': '134-136',
    'astringent acuex': '114-116',
    'bristlehair bat': '113-115',
    'debauched unseelie': SKIP,
    'dreadhound': '114-116',
    'dullahan': '115-117',
    'enshrouded cyhiraeth': '113-116',
    'fluturini': '114-116',
    'horrific bhoot': '114-115',
    'legionless draugar': '114-116',
    'obfuscous obdella': '113-115',
    'phlegmatic byrgen': '116',
    'restless twitherym': '113-115',
    'shunned deeparrow': '114-116',
    'shunned hexer': '114-116',
    'shunned nightstalker': '114-116',
}


def band(s):
    if s.startswith('~'):
        s = s[1:]
    if not s or not s[0].isdigit():
        return None
    lo, _, hi = s.partition('-')
    try:
        return int(lo), int(hi or lo)
    except ValueError:
        return None


def apply_zone(mob, zone, lvl, log, key):
    zones = mob.setdefault('zones', [])
    entry = None
    for z in zones:
        if isinstance(z, list) and z and z[0] == zone:
            entry = z
            break
        if isinstance(z, str) and z == zone:
            log['kept_flat'].append(key)
            return
    if entry is None:
        zones.append([zone] if lvl is SKIP else [zone, lvl])
        log['added'].append((key, zone, None if lvl is SKIP else lvl))
        return
    if lvl is SKIP:
        log['blank_kept'].append((key, zone, entry[1] if len(entry) > 1 else None))
        return
    if len(entry) == 1:
        entry.append(lvl)
        log['filled'].append((key, zone, lvl))
    elif entry[1] != lvl:
        log['changed'].append((key, zone, entry[1], lvl))
        entry[1] = lvl
    else:
        log['same'].append((key, zone, lvl))


def widen(mob, lvl, log, key):
    if lvl is SKIP:
        return
    b = band(lvl)
    cur = mob.get('lv')
    if b is None or not isinstance(cur, list) or len(cur) != 2:
        return
    new = [min(cur[0], b[0]), max(cur[1], b[1])]
    if new != cur:
        log['lv_union'].append((key, list(cur), new))
        mob['lv'] = new


def main():
    with open(PATH, encoding='utf-8') as fh:
        data = json.load(fh)
    mobs = data['mobs']

    log = {k: [] for k in
           ('added', 'filled', 'changed', 'blank_kept', 'same',
            'lv_union', 'missing', 'kept_flat')}

    for table, zone in ((WOH_ROWS, WOH), (OUTER_ROWS, OUTER)):
        for key, lvl in table.items():
            mob = mobs.get(key)
            if mob is None:
                log['missing'].append(key)
                continue
            apply_zone(mob, zone, lvl, log, key)
            widen(mob, lvl, log, key)

    assert not [k for m in mobs.values() for k, v in m.items() if v is None], 'null poison'
    for k, m in mobs.items():
        for z in m.get('zones') or []:
            if isinstance(z, list):
                assert 1 <= len(z) <= 2 and isinstance(z[0], str), (k, z)
                assert len(z) == 1 or isinstance(z[1], str), (k, z)
    # no new spelling of the Ra'Kaznar zone may appear
    assert not [k for k, m in mobs.items() for z in (m.get('zones') or [])
                if isinstance(z, list) and z[0] == "Outer Ra'Kaznar"], "apostrophe form written"

    with open(PATH, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, separators=(', ', ': '), ensure_ascii=False)

    for name in ('added', 'filled', 'changed', 'lv_union',
                 'missing', 'blank_kept', 'kept_flat', 'same'):
        rows = log[name]
        print(f'== {name} ({len(rows)})')
        for r in rows:
            print('   ', r)


if __name__ == '__main__':
    main()
