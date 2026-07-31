#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 324
Author: BalladOfWorms

TWO ZONES: Meriphataud Mountains [S] (12 NM + 35 ADV) + Castle Oztroja [S] (11 NM + 26 ADV).

SKIP = the page's Lv cell is blank -> ensure the zone exists, never touch a stored level.

Rule 239: two rows here DO have a `(monster)` twin and both are written to the TWIN -
`lycopodium (monster)` (which already holds the zone at 31-34) and `condor (monster)`, whose
row the wiki page itself prints as "Condor (Monster)".  The writer asserts on any other twin.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

MERI = 'Meriphataud Mountains [S]'
OZTROJA = 'Castle Oztroja [S]'

# keys we deliberately address by their `(monster)` form
TWIN_OK = {'lycopodium (monster)', 'condor (monster)'}

MERI_ROWS = {
    'bloodlapper': '80',
    'sandworm': SKIP,
    'centipedal centruroides': SKIP,
    'hemodrosophila': SKIP,
    'muq shabeel': '74',
    'akupara': SKIP,
    'rummager beetle': SKIP,
    'raker bee': SKIP,
    'farruca fly': SKIP,
    'jyeshtha': SKIP,
    'orcus': SKIP,
    'yilbegan': SKIP,
    'axe beak': '66-69',
    'black bat': SKIP,
    'dragonfly': '59-63',
    'earth elemental': SKIP,
    'fire elemental': SKIP,
    'gnat': '79-82',
    'goblin bombardier': '71-73',
    'goblin field doctor': '71-73',
    'goblin paratrooper': '71-73',
    'goblin picket': '71-73',
    'hill lizard': '44-47',
    'jubjub': '42-44',
    'jumbo rafflesia': '68-72',
    'lycopodium (monster)': '31-34',
    'lynx': '49-51',
    'mountain jubjub': SKIP,
    'mountain scolopendrid': '77-80',
    'night bats': SKIP,
    'raptor': '64-68',
    'scavenging hound': SKIP,
    'scolopendrid': SKIP,
    'sprite': '61-63',
    'stag beetle': '45-48',
    'treant sapling': '56-59',
    'wandering sapling': '28-30',
    'war lynx': '68-72',
    'yagudo chanter': '76-78',
    'yagudo eradicator': '76-78',
    'yagudo high priest': '76-78',
    'yagudo knight templar': '76-78',
    'yagudo prelate': '76-78',
    'yagudo prioress': '76-78',
    'yagudo sentinel': '76-78',
    "yagudo's elemental": SKIP,
    'condor (monster)': '93-94',
}

OZTROJA_ROWS = {
    'aa xalmo the savage': SKIP,
    'asterion': SKIP,
    'dee zelko the esoteric': SKIP,
    'duu masa the onecut': '83',
    'fleshgnasher': SKIP,
    'loo kutto the pensive': SKIP,
    'maa illmu the bestower': SKIP,
    'marquis forneus': SKIP,
    'suu xicu the cantabile': SKIP,
    'vee ladu the titterer': SKIP,
    'zhuu buxu the silent': SKIP,
    'antlion fly': '65-68',
    'bastion bats': SKIP,
    'blooming rafflesia': '62-68',
    'bulwark bat': '68-71',
    'earth elemental': SKIP,
    'fire elemental': SKIP,
    'gnat': '79-82',
    'immolatory pugil': '65-67',
    'seneschal imp': '77-79',
    'war lynx': SKIP,
    'yagudo abbot': '79-82',
    'yagudo chanter': '77-79',
    'yagudo conductor': '79-82',
    'yagudo eradicator': '77-79',
    'yagudo flagellant': '79-82',
    'yagudo hierogrammat': '79-82',
    'yagudo high priest': '77-79',
    'yagudo knight templar': '77-79',
    'yagudo nokizaru': '79-82',
    'yagudo parasite': SKIP,
    'yagudo prelate': '77-79',
    'yagudo prioress': '77-79',
    'yagudo sentinel': '77-79',
    'yagudo superior': '79-82',
    'yagudo yojimbo': '81-83',
    "yagudo's elemental": SKIP,
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
            'lv_union', 'missing', 'kept_flat', 'twin_warn')}

    for table, zone in ((MERI_ROWS, MERI), (OZTROJA_ROWS, OZTROJA)):
        for key, lvl in table.items():
            if key not in TWIN_OK and f'{key} (monster)' in mobs:   # rule 239 guard
                log['twin_warn'].append(key)
            mob = mobs.get(key)
            if mob is None:
                log['missing'].append(key)
                continue
            apply_zone(mob, zone, lvl, log, key)
            widen(mob, lvl, log, key)

    assert not log['twin_warn'], f'(monster) twin exists for: {log["twin_warn"]}'
    assert not [k for m in mobs.values() for k, v in m.items() if v is None], 'null poison'
    for k, m in mobs.items():
        for z in m.get('zones') or []:
            if isinstance(z, list):
                assert 1 <= len(z) <= 2 and isinstance(z[0], str), (k, z)
                assert len(z) == 1 or isinstance(z[1], str), (k, z)

    with open(PATH, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, separators=(', ', ': '), ensure_ascii=False)

    for name in ('added', 'filled', 'changed', 'lv_union',
                 'missing', 'blank_kept', 'kept_flat', 'twin_warn'):
        rows = log[name]
        print(f'== {name} ({len(rows)})')
        for r in rows:
            print('   ', r)
    print(f'== same ({len(log["same"])})')


if __name__ == '__main__':
    main()
