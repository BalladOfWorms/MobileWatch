#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 317
Author: BalladOfWorms

TWO ZONES: Dho Gates (1 NM + 45 ADV) + Kamihr Drifts (6 NM + 15 ADV).

SKIP  = the page's Lv cell is blank -> ensure the zone exists, NEVER touch a stored
        level (refining rule 15).
Collapse convention applied on write: the page prints '125-125' / '120-120' /
'124-124' / '116-116'; stored as '125' / '120' / '124' / '116'.

Rule 217: Kamihr's Lv column read as '111-118' on several rows.  zoneinfo says
111-113 and the pixel decode gives a final glyph with a blank LEFT side through the
middle rows = a '3'.  Diffed before writing; nothing was corrected off the misread.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

DHO = 'Dho Gates'
KAMIHR = 'Kamihr Drifts'

DHO_ROWS = {
    'dreadpincer': '126',
    'apex bats': '128-130',
    'apex crab': '128-130',
    'apex craklaw': '128-130',
    'apex jagil': '128-130',
    'blightdella': SKIP,
    'bloodspattered fly': '121-122',
    'chumchomp jagil': SKIP,
    'corallitic crab': SKIP,
    'coverime gefyrst': SKIP,
    'crevice tarichuk': SKIP,
    'crusty crab': SKIP,
    'duskprowlers': SKIP,
    'dwende': '125',
    'fetid umbril': '121-123',
    'firth umbril': SKIP,
    'fleshrending obdella': '120-122',
    'irascible tarichuk': '120',
    'knotted root': SKIP,
    'kopffussler': SKIP,
    'leafdancer twitherym': SKIP,
    'midnight worm': '120',
    'peevish acuex': '121-123',
    'plagueborn dullahan': '121-123',
    'pungent fungus': SKIP,
    'rancidclaw crab': '120-122',
    'ravenous craklaw': SKIP,
    'ripsaw jagil': SKIP,
    'septic acuex': '120-122',
    'slinking slug': '121-123',
    'spinescent protuberance': SKIP,
    'spumous slug': '120-122',
    'surly craklaw': '124',
    'trogloptera': SKIP,
    'twilight bat': SKIP,
    'unyielding tarichuk': SKIP,
    'velkk berserker': SKIP,
    'velkk magus': SKIP,
    'velkk manipulator': SKIP,
    'velkk punisher': SKIP,
    'velkk ravager': SKIP,
    'velkk reaver': SKIP,
    'velkk stormcaller': SKIP,
    'velkk vaticinator': SKIP,
    'void worm': SKIP,
    'whirlwind ungeweder': SKIP,
}

KAMIHR_ROWS = {
    'azeman': SKIP,
    'calydontis': SKIP,
    'cherti': SKIP,
    'kumhau': '116',
    'mirka': '125',
    'sinaa': SKIP,
    'ashen tiger': '111-113',
    'bedraggled lucerewe': '111-113',
    'cicatricose raaz': '111-113',
    'cyanotic raptor': '111-113',
    'gnarring yztarg': '111-113',
    'graupel formation': SKIP,
    'hailstone': '111-113',
    'incensed lucerewe': '111-113',
    'shaggy ovim': '111-113',
    'shivering heartwing': '111-113',
    'slobbering ruszor': '111-113',
    'sprightly leafkin': '111-113',
    'snowpaw rabbit': '111-113',
    'snowpelt rabbit': '111-113',
    'wintry cave': SKIP,
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

    for table, zone in ((DHO_ROWS, DHO), (KAMIHR_ROWS, KAMIHR)):
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
