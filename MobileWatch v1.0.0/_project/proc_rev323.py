#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 323
Author: BalladOfWorms

TWO ZONES: La Vaule [S] (11 NM + 31 ADV) + The Eldieme Necropolis [S] (6 NM + 20 ADV).

SKIP = the page's Lv cell is blank (incl. every "Fished Up" row) -> ensure the zone exists,
never touch a stored level (rule 15).

Rule 239 check done: none of the 68 rows on these two pages has a `<name> (monster)` twin.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

VAULE = 'La Vaule [S]'
ELDIEME = 'The Eldieme Necropolis [S]'

VAULE_ROWS = {
    'all-seeing onyx eye': '83',
    'agrios': '83',
    'ashmaker gotblut': SKIP,
    'cogtooth skagnogg': '83',
    'coinbiter cjaknokk': '83',
    'draketrader zlodgodd': '83',
    'falsespinner bhudbrodd': '83',
    'feeblescheme bhogbigg': '83',
    'hawkeyed dnatbat': '81',
    'rugaroo': '83',
    'shatterskull mippdapp': '72-74',
    'fighting smilodon': '75-78',
    'gloop': SKIP,
    'greater pugil': SKIP,
    'la vaule pugil': '72-75',
    'lobison': SKIP,
    'mariehene': '71-74',
    'morbol': '79-80',
    'ogrish pugil': SKIP,
    'oil spill': SKIP,
    'orcish augur': '77-79',
    'orcish bowshooter': '79-81',
    'orcish champion': '77-79',
    'orcish cupholder': '81-83',
    'orcish dragonbrander': '77-79',
    'orcish dreadnought': '81-83',
    'orcish farkiller': '81-83',
    'orcish firebelcher': '77-79',
    'orcish imperial guard': '81-83',
    'orcish prophetess': '81-83',
    'orcish protector': '79-81',
    'orcish strategist': '81-83',
    'orcish veteran': '77-79',
    'orcish warlord': '79-81',
    'orcish wyrmbrander': '81-83',
    'seneschal imp': '77-79',
    'thunder elemental': SKIP,
    'war lizard': '68-74',
    'water elemental': SKIP,
    'wolf bat': SKIP,
    'wood bats': SKIP,
    'ferocious pugil': SKIP,
}

ELDIEME_ROWS = {
    'ethniu': SKIP,
    'laelaps': SKIP,
    'tethra': SKIP,
    'orcish transporter': SKIP,
    'orcish guard': SKIP,
    'giltine': SKIP,
    'earth elemental': SKIP,
    'eastern spriggan': '66-69',
    'gazer': '63-65',
    'goblin blastmaster': '62-64',
    'goblin corpsman': '62-64',
    'goblin freesword': '62-64',
    'goblin pioneer': '62-64',
    'hell hound': '64-66',
    'ignis djinn': '68-72',
    'lich': '67-69',
    'lost soul': '67-69',
    'northern spriggan': '66-69',
    'orcish brawler': '68-71',
    'orcish chasseur': '68-71',
    'orcish cursemaker': '68-71',
    'orcish trooper': '68-71',
    'revenant': '68-70',
    'southern spriggan': '66-69',
    'war smilodon': '61-64',
    'western spriggan': '66-69',
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

    for table, zone in ((VAULE_ROWS, VAULE), (ELDIEME_ROWS, ELDIEME)):
        for key, lvl in table.items():
            if f'{key} (monster)' in mobs:            # rule 239 guard
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
