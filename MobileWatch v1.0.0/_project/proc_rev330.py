#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 330
Author: BalladOfWorms

FOUR ZONES: Promyvion-Dem (3 NM + 7 ADV), Promyvion-Holla (3+7), Promyvion-Mea (3+7),
Promyvion-Vahzl (11 published NM rows + 9 ADV).

ZONE STRINGS read out of zones.json FIRST (rule 244): `Promyvion-Dem`, `Promyvion-Holla`,
`Promyvion-Mea`, `Promyvion-Vahzl` - NO spaces around the hyphen, the Abyssea-/Dynamis- form.

Rule 91: exact on Dem/Holla/Mea.  Vahzl's page prints ELEVEN NM rows against zoneinfo's NINE,
and the difference is entirely the THREE `Stray` rows (Genus Wanderer / Weeper / Seether) that
both zoneinfo and mobs.json can only hold once.  A shared-name collision, not a miss.

The Promyvion set arrives almost fully covered - this is a fill/correct rev, one single add.

SENTINEL
  SKIP = blank Lv cell -> never touch a stored level.  Vahzl's `wailer`, `ponderer`,
         `propagator`, `solicitor` and `apex livid rager` all publish nothing and keep what
         they have (`apex livid rager` keeps 139-142).
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

DEM = 'Promyvion-Dem'
HOLLA = 'Promyvion-Holla'
MEA = 'Promyvion-Mea'
VAHZL = 'Promyvion-Vahzl'

DEM_ROWS = {
    'satiator': '38',
    'memory receptacle': '30',
    'stray': '19-31',                    # stored 29-31 -> correction
    'gorger': '29-40',
    'seether': '31-38',
    'wanderer': '22-36',
    'weeper': '25-37',
    'apex idle drifter': '139-142',
    'apex woeful lamenter': '139-142',
    'apex livid rager': '139-142',
}

HOLLA_ROWS = {
    'cerebrator': '38',
    'memory receptacle': '30',
    'stray': '19-31',                    # stored 29-31 -> correction
    'seether': '31-38',
    'thinker': '29-40',
    'wanderer': '22-36',
    'weeper': '25-37',
    'apex idle drifter': '139-142',
    'apex woeful lamenter': '139-142',
    'apex livid rager': '139-142',
}

MEA_ROWS = {
    'coveter': '38',
    'memory receptacle': '30',
    'stray': '19-31',                    # stored 29-31 -> correction
    'craver': '28-40',                   # stored 29-40 -> correction
    'seether': '31-38',
    'wanderer': '22-36',
    'weeper': '25-37',
    'apex idle drifter': '139-142',
    'apex woeful lamenter': '139-142',
    'apex livid rager': '139-142',
}

VAHZL_ROWS = {
    # --- Notorious Monsters (11 printed rows; 3 of them share the name `Stray`)
    'deviator': '58',
    'provoker': '~60',
    'wailer': SKIP,
    'memory receptacle': '50',
    'stray': '39-51',
    'ponderer': SKIP,
    'propagator': SKIP,
    'offspring': SKIP,                   # the rev's only add
    'solicitor': SKIP,
    # --- Adversaries (9)
    'craver': '54-60',
    'gorger': '54-60',
    'seether': '51-58',
    'thinker': '54-60',
    'wanderer': '49-56',
    'weeper': '50-57',
    'apex idle drifter': '139-142',
    'apex woeful lamenter': '139-142',
    'apex livid rager': SKIP,            # blank here, keeps its stored 139-142
}


def band(s):
    if s.startswith('~'):
        s = s[1:]
    s = s.rstrip('+')
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
    """rule 9 - the global lv may only ever be EXTENDED (rule 248: never from an `N+`)."""
    if lvl is SKIP or lvl.endswith('+'):
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

    for table, zone in ((DEM_ROWS, DEM), (HOLLA_ROWS, HOLLA),
                        (MEA_ROWS, MEA), (VAHZL_ROWS, VAHZL)):
        for key, lvl in table.items():
            if f'{key} (monster)' in mobs:          # rule 239 guard
                log['twin_warn'].append(key)
            if f'{key} (s)' in mobs:                # rule 247 guard
                log['twin_warn'].append(key + ' (s)')
            mob = mobs.get(key)
            if mob is None:
                log['missing'].append(key)
                continue
            apply_zone(mob, zone, lvl, log, key)
            widen(mob, lvl, log, key)

    assert not log['twin_warn'], f'suffixed twin exists for: {log["twin_warn"]}'
    assert not log['missing'], f'unmatched keys: {log["missing"]}'
    assert not [k for m in mobs.values() for k, v in m.items() if v is None], 'null poison'
    for k, mb in mobs.items():
        for z in mb.get('zones') or []:
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
