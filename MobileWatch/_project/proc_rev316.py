#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 316
Author: BalladOfWorms

TWO ZONES: Cirdas Caverns (2 NM + 28 ADV) + Marjami Ravine (6 NM + 36 ADV).

SKIP  = the page's Lv cell is blank -> ensure the zone exists, NEVER touch a stored
        level (refining rule 15).
a str = the page publishes that band -> add / fill / overwrite the ZONE entry's level.
        Tilde forms are stored verbatim (rule 11): '~124', '~108'.

Rule 217: every level read as ending in '8' was diffed against zoneinfo first.
Marjami's 106-108 / ~108 block AGREES with zoneinfo, so those 8s are real and were
written; the rule rejects nothing by default, it only forces the diff.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

CIRDAS = 'Cirdas Caverns'
MARJAMI = 'Marjami Ravine'

CIRDAS_ROWS = {
    # Notorious Monsters
    'vemosia': '126',
    'ancestral rage': SKIP,
    # Adversaries
    'asperous marolith': '103-105',
    'balas bats': '102-104',
    'bloodmoon umbril': '107-109',
    'crepuscular worm': '103-105',
    'flatus acuex': '103-105',
    'foreboding funguar': '102-104',
    'frightful funguar': SKIP,
    'fuliginous mandragora': '102-104',
    'grossular bat': '102-104',
    'hefty marolith': '~124',
    'igneous clot': '102-104',
    'invidious lizard': '102-104',
    'knotted root': SKIP,
    'livid umbril': '103-105',
    'molten clot': SKIP,
    'oregorger worm': SKIP,
    'pallid funguar': '102-104',
    'pungent fungus': SKIP,
    'putrid funguar': SKIP,
    'pyre bat': SKIP,
    'shadowshiver umbril': '120-122',
    'sordid lizard': SKIP,
    'speckled spider': '102-104',
    'subterrane spider': '102-104',
    'tenebrous obdella': '102-104',
    'tormented obdella': SKIP,
    'tunnel lizard': '102-104',
    'umbril shadewarrior': SKIP,
}

MARJAMI_ROWS = {
    # Notorious Monsters - the Lv column is blank on all six
    'broxa': SKIP,
    'plaguevein bats': SKIP,
    'hakawai': SKIP,
    'ironbeak inguza': SKIP,
    'podarge': SKIP,
    'hurkan': SKIP,
    # Adversaries
    'avian roost': SKIP,
    'breezewing vulture': SKIP,
    'canyon apkallu': '106-108',
    'chumchomp jagil': SKIP,
    'cliffclinger toad': '106-108',
    'crackling ungeweder': '105-106',
    'diffident heartwing': SKIP,
    'dirtcaked jagil': '106-108',
    'embattled roc': SKIP,
    'foraging apkallu': SKIP,
    'gerent apkallu': SKIP,
    'gorge vulture': SKIP,
    'gully toad': SKIP,
    'ironclaw tulfaire': SKIP,
    'lapinion': '106-108',
    'lapiniontrap': '106-108',
    'longface colibri': SKIP,
    'monolithic boulder': SKIP,
    'playful leafkin': SKIP,
    'precipice vulture': SKIP,
    'preening tulfaire': SKIP,
    'resilient colibri': SKIP,
    'riverscum': '106-108',
    'soulwrenching umbril': SKIP,
    'spinescent protuberance': SKIP,
    'stonefaced roc': SKIP,
    'stryx': '106-108',
    'trembling tulfaire': SKIP,
    'tulfaire': '106-108',
    'undaunted colibri': SKIP,
    'velkk defiler': '107-109',
    'velkk inquisitor': '107-109',
    'velkk jaguar': '~108',
    'velkk shadowmancer': '107-109',
    'vinelash vulture': '106-108',
    'whispering twitherym': '106-108',
}

# Notorious-Monsters-table row rendering as an ordinary mob
NM_SET = ['hurkan']


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
    """rule 9 - lv only ever grows."""
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

    for table, zone in ((CIRDAS_ROWS, CIRDAS), (MARJAMI_ROWS, MARJAMI)):
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
