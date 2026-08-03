#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 321
Author: BalladOfWorms

FOUR ZONES: Ruhotz Silvermines (2 NM) + Ghoyu's Reverie (1 NM) + Fort Karugo-Narugo [S]
(6 NM + 19 ADV) + West Sarutabaruta [S] (13 NM + 24 ADV).

SKIP = the page's Lv cell is blank or '?' -> ensure the zone exists, never touch a stored level.
Zone strings follow zones.json: `Ghoyus Reverie` has NO apostrophe (all 33 stored entries agree).

`serket` is a deliberate SKIP: the page prints `80+` while the record stores the more precise `83`.
Rule 1 says a zone pass must never make the file poorer, so 83 stands.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

RUHOTZ = 'Ruhotz Silvermines'
GHOYU = 'Ghoyus Reverie'
KARUGO = 'Fort Karugo-Narugo [S]'
WSARU = 'West Sarutabaruta [S]'

RUHOTZ_ROWS = {
    'lambton worm': SKIP,
    'guivre': SKIP,
}

GHOYU_ROWS = {
    'serket': SKIP,
}

KARUGO_ROWS = {
    'dark ixion': '80-85',
    'demoiselle desolee': '83-84',
    'emela-ntouka': SKIP,
    'kirtimukha': '65',
    'ratatoskr': '55-58',
    'kalasutrax': SKIP,
    'air elemental': '60',
    'carrion crow': '37-40',
    'death jacket': '34-37',
    'dragonfly': '55-60',
    'earth elemental': '60',
    'goblin pioneer': '62-64',
    'jumbo rafflesia': '64-68',
    'lycopodium': '22-25',
    'pixie': '56-59',
    'rafflesia': '59-62',
    'vorpal bunny': '26-29',
    'wandering sapling': '26-28',
    'war lizard': '40-43',
    'yagudo drummer': '64-68',
    'yagudo herald': '64-68',
    'yagudo interrogator': '64-68',
    'yagudo priest': '64-68',
    'yagudo theologist': '64-68',
    'yagudo votary': '64-68',
}

WSARU_ROWS = {
    'dark ixion': '80-85',
    'jeduah': '17-18',
    'sandworm': '~88',
    'belladonna (nm)': '53-54',          # page row reads "Belladonna"; base record deleted r99
    'ramponneau': SKIP,
    'tiffenotte': SKIP,
    'pancimanci': SKIP,
    'rummager beetle': SKIP,
    'raker bee': SKIP,
    'farruca fly': SKIP,
    'jyeshtha': SKIP,
    'orcus': SKIP,
    'yilbegan': SKIP,
    'bumblebee': '15-17',
    'carrion crow': '22-25',
    'crawler': '18-21',
    'goblin draftee': '56-59',
    'goblin franctireur': '56-59',
    'goblin patrolman': '56-59',
    'goblin skirmisher': '56-59',
    "goblin's rarab": '52-54',
    'mad fox': SKIP,
    'pixie': '51-54',
    'poroggo gent': '56-58',
    'rafflesia': '49-52',
    'river crab': '22-25',
    'savanna dhalmel': '34-37',
    'savanna rarab': '13-15',
    'tiny lycopodium': '10-12',
    'toad': '49-52',
    'yagudo acolyte': '61-63',
    'yagudo condottiere': '62-64',
    'yagudo initiate': '61-63',
    'yagudo mendicant': '61-63',
    'yagudo persecutor': '62-64',
    'yagudo piper': '61-63',
    'yagudo scribe': '61-63',
}

# Notorious-Monsters-table row rendering as an ordinary mob
NM_SET = ['pancimanci']


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
            'lv_union', 'nm_set', 'missing', 'kept_flat')}

    for table, zone in ((RUHOTZ_ROWS, RUHOTZ), (GHOYU_ROWS, GHOYU),
                        (KARUGO_ROWS, KARUGO), (WSARU_ROWS, WSARU)):
        for key, lvl in table.items():
            mob = mobs.get(key)
            if mob is None:
                log['missing'].append(key)
                continue
            apply_zone(mob, zone, lvl, log, key)
            widen(mob, lvl, log, key)

    for key in NM_SET:
        mob = mobs[key]
        if not mob.get('nm'):
            mob['nm'] = True
            log['nm_set'].append(key)

    assert not [k for m in mobs.values() for k, v in m.items() if v is None], 'null poison'
    for k, m in mobs.items():
        for z in m.get('zones') or []:
            if isinstance(z, list):
                assert 1 <= len(z) <= 2 and isinstance(z[0], str), (k, z)
                assert len(z) == 1 or isinstance(z[1], str), (k, z)

    with open(PATH, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, separators=(', ', ': '), ensure_ascii=False)

    for name in ('added', 'filled', 'changed', 'lv_union', 'nm_set',
                 'missing', 'blank_kept', 'kept_flat'):
        rows = log[name]
        print(f'== {name} ({len(rows)})')
        for r in rows:
            print('   ', r)
    print(f'== same ({len(log["same"])})')


if __name__ == '__main__':
    main()
