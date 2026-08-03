#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 319
Author: BalladOfWorms

TWO ZONES: Ra'Kaznar Inner Court (1 NM + 30 shot rows) + East Ronfaure [S] (18 NM + 24 ADV).

SKIP  = the page's Lv cell is blank -> ensure the zone exists, NEVER touch a stored level (rule 15).
Zone strings: `RaKaznar Inner Court` (zones.json spelling, 20 pre-existing entries) and
`East Ronfaure [S]` (the [S] bracket convention).

NOT TOUCHED: Apex Bhoot / Cyhiraeth / Draugar / Poxhound / Vodoriga.  zoneinfo carries them and
all five already hold the zone at 137-139, but the CURRENT page does not list them - additive
only, so nothing is written or removed.  See the handoff.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

COURT = 'RaKaznar Inner Court'
RONF = 'East Ronfaure [S]'

COURT_ROWS = {
    'suspended sculpture': SKIP,          # on BOTH tables - rule 201, 7th instance
    'apex bats': '137-139',
    'apex umbril': '137-139',
    'bilespouting acuex': '119-122',
    'boilridden umbril': '120-123',
    'conniving unseelie': '121-124',
    'deserter draugar': SKIP,
    'disheveled naraka': SKIP,
    'dolorous cyhiraeth': SKIP,
    'draftdance fluturini': SKIP,
    'dullahan axegrinder': '123-124',
    'enigmatic vampyr': '137-139',
    'inimical corse': SKIP,
    'ironclad animus': '124',
    'ironclad wrecker': SKIP,
    'powercrazed dvergr': SKIP,
    'poxhound': '118-119',
    'scowling vodoriga': '120-123',
    'slimeskin obdella': '119-122',
    'spurned deeparrow': '120-123',
    'spurned elementalist': '120-123',
    'spurned engraver': '120-123',
    'spurned fluteslinger': '120-123',
    'spurned hexer': '120-123',
    'spurned nightstalker': '120-123',
    'spurned saboteur': '120-123',
    'spurned valiant': '120-123',
    'unrepentant byrgen': SKIP,
    'wayward bhoot': '119-121',
    'whitenoise bats': SKIP,
}

RONF_ROWS = {
    # Notorious Monsters
    'dark ixion': '80-85',
    'sandworm': '~88',
    'skogs fru': '60-65',
    'melusine': SKIP,
    'myradrosh': SKIP,
    'goblintrap': SKIP,
    'faytrapper vashgash': SKIP,
    'faygorger ram': SKIP,
    'faygorger sheep': SKIP,
    'orcish transporter': SKIP,
    'orcish guard': SKIP,
    'cottus': SKIP,
    'quagmire pugil': SKIP,
    'sunderclaw': SKIP,
    'yacumama': SKIP,
    'capricornus': SKIP,
    'krabkatoa': SKIP,
    'yilbegan': SKIP,
    # Adversaries
    'carrion worm': '10-13',
    'colibri': '45-47',
    'ding bats': '12-14',
    'djinn': '53-55',
    'enchanted bones': '37-39',          # two rows (BLM + WAR), one record - rev-132 precedent
    'forest hare': '11-15',
    'giant spider': '50-52',
    'goblin draftee': '56-59',
    'goblin franctireur': '56-59',
    'goblin patrolman': '56-59',
    'goblin skirmisher': '56-59',
    "goblin's ladybug": '52-54',
    'ladybug': '45-47',
    'mouse bat': '12-15',
    'orcish fodder': '62-64',
    'orcish mesmerizer': '62-64',
    'orcish neckchopper': '62-64',
    'orcish stonechucker': '62-64',
    'pixie': '51-54',
    'pugil': '14-17',
    'river crab': '12-14',
    'scarab beetle': '21-23',
    'walking tree': '54-56',
    'wild sheep': '16-18',
}

# Notorious-Monsters-table rows rendering as ordinary mobs
NM_SET = ['faytrapper vashgash', 'faygorger ram', 'faygorger sheep',
          'orcish transporter', 'orcish guard', 'cottus']


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

    for table, zone in ((COURT_ROWS, COURT), (RONF_ROWS, RONF)):
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
                 'missing', 'blank_kept', 'kept_flat', 'same'):
        rows = log[name]
        print(f'== {name} ({len(rows)})')
        for r in rows:
            print('   ', r)


if __name__ == '__main__':
    main()
