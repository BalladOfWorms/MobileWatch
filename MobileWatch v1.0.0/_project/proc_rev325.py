#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 325
Author: BalladOfWorms

THREE ZONES: Sauromugue Champaign [S] (18 NM + 26 ADV) + Garlaige Citadel [S] (4 NM + 13 ADV on
the page, 12 in zoneinfo) + Beadeaux [S] (11 NM + 21 ADV).

SKIP = the page's Lv cell is blank -> ensure the zone exists, never touch a stored level.
Beadeaux's ENTIRE Adversaries table has a blank Lv column, so every one of its 21 rows is a SKIP.

Rule 239: `lycopodium` is written to `lycopodium (monster)`, which already holds the zone.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

SAURO = 'Sauromugue Champaign [S]'
GARLAIGE = 'Garlaige Citadel [S]'
BEADEAUX = 'Beadeaux [S]'

TWIN_OK = {'lycopodium (monster)'}

SAURO_ROWS = {
    'balam-quitz': '53',
    'hyakinthos': '58-60',
    'sandworm': SKIP,
    'coquecigrue': SKIP,
    'herensugue': SKIP,
    'gugalanna': SKIP,
    'aither': SKIP,
    'deorc': SKIP,
    'eorthe': SKIP,
    'puretos': SKIP,
    'pruina': SKIP,
    'beorht': SKIP,
    'thunor': SKIP,
    'lacus': SKIP,
    'urd': SKIP,
    'skuld': SKIP,
    'verthandi': SKIP,
    'yilbegan': SKIP,
    'diving beetle': '44-47',
    'earth elemental': SKIP,
    'gnat': '75-78',
    'goblin flagman': '66-69',
    'goblin grenadier': '66-69',
    'goblin guerrilla': '66-69',
    'goblin toxophilite': '66-69',
    "goblin's beetle": SKIP,
    'hill lizard': '45-48',
    'lycopodium (monster)': '28-31',
    'lynx': '46-48',
    'midnight wings': '38-42',
    'moon bat': '38-40',
    'sauromugue skink': '51-53',
    'scavenging hound': '47-50',
    'sprite': '61-63',
    'tabar beak': '52-54',
    'thunder elemental': SKIP,
    'yagudo abbot': '71-73',
    'yagudo inquisitor': '71-73',
    'yagudo lutenist': '71-73',
    'yagudo missionary': '71-73',
    'yagudo prior': '71-73',
    'yagudo pythoness': '71-73',
    'yagudo zealot': '71-73',
    "yagudo's elemental": SKIP,
}

GARLAIGE_ROWS = {
    'buarainech': SKIP,
    'citadel pipistrelles': SKIP,
    'elatha': SKIP,
    'laidly laurence': SKIP,
    'dire bat': '63-65',
    'explosure': SKIP,
    'incubus bats': '63-65',
    'mousse': '65',
    'scolopendrid': '68-70',
    'yagudo abbot': '71-73',
    'yagudo lutenist': '71-73',
    'yagudo missionary': '71-73',
    'yagudo prior': '71-73',          # on the page, absent from zoneinfo - record already zoned
    'yagudo pythoness': '71-73',
    'yagudo templar': '71-73',
    'yagudo zealot': '71-73',
    "yagudo's elemental": SKIP,
}

BEADEAUX_ROWS = {
    "ba'tho mercifulheart": '80-81',
    'blifnix oilycheeks': SKIP,
    'bres': SKIP,
    "da'dha hundredmask": SKIP,
    "di'zho spongeshell": SKIP,
    "ea'tho cruelheart": '80-81',
    "ga'lhu nevermolt": SKIP,
    "mu'nhi thimbletail": SKIP,
    'observant zekka': '81',
    "ra'dha scarscute": SKIP,
    "va'gho bloodbasked": '85',
    # the whole Adversaries table prints a blank Lv column
    'adaman quadav': SKIP,
    'ancient quadav': SKIP,
    'baetyl quadav': SKIP,
    'chatoyant quadav': SKIP,
    'doyen quadav': SKIP,
    'edible slug': SKIP,
    'electrumcap': SKIP,
    'ferroalloy quadav': SKIP,
    'gold quadav': SKIP,
    'iron quadav': SKIP,
    'magnes quadav': SKIP,
    'meteor quadav': SKIP,
    'pitchy pudding': SKIP,
    'platinum quadav': SKIP,
    'seneschal imp': SKIP,
    'star ruby quadav': SKIP,
    'steel quadav': SKIP,
    'thunder elemental': SKIP,
    'vajra quadav': SKIP,
    'virulent peiste': SKIP,
    'water elemental': SKIP,
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

    for table, zone in ((SAURO_ROWS, SAURO), (GARLAIGE_ROWS, GARLAIGE),
                        (BEADEAUX_ROWS, BEADEAUX)):
        for key, lvl in table.items():
            if key not in TWIN_OK and f'{key} (monster)' in mobs:
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
                 'missing', 'kept_flat', 'twin_warn'):
        rows = log[name]
        print(f'== {name} ({len(rows)})')
        for r in rows:
            print('   ', r)
    print(f'== blank_kept ({len(log["blank_kept"])})  == same ({len(log["same"])})')


if __name__ == '__main__':
    main()
