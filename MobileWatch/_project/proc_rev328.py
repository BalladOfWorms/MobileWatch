#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 328
Author: BalladOfWorms

TWO ZONES: Beaucedine Glacier [S] (11 NM + 18 ADV) + Xarcabard [S] (12 NM + 29 ADV).
Rule 91 exact against zoneinfo on both.

ZONE STRINGS read out of zones.json FIRST (rule 244): `Beaucedine Glacier [S]` and
`Xarcabard [S]`.  (Both zones also exist un-bracketed, and Xarcabard has a
`Dynamis-Xarcabard` sibling - none of the three is this page.)

These are the THINNEST-COVERED zones of the sweep: 17 and 14 holders on arrival against
29 and 40 published rows, so this is an add rev, not a correction rev.

SENTINELS
  SKIP  = the page's Lv cell is blank (every Voidwalker / Fished-Up row here) -> never
          touch a stored level; a missing zone is still ADDED, level-less.
SETLV   = rule 245, additive only: `menacing eye` has NO `lv` at all and, once this zone
          is added, holds exactly one zone - so this page's band IS its global band.

NOT WRITTEN - FLAGGED
  `Becut` (Beaucedine NM table, Gigas, Lottery from Gigas, drops Aptant: Arkhe / Primus)
  HAS NO RECORD IN mobs.json under any spelling.  Fuzzy-searched 'becut'/'bec'/'ecut'
  (0 hits) and both its drops (7 holders, none a Beaucedine Gigas).  zoneinfo carries the
  row; mobs.json does not.  Creating a mob record is outside this phase's remit -> flagged.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

BEAUCEDINE = 'Beaucedine Glacier [S]'
XARCABARD = 'Xarcabard [S]'

BEAUCEDINE_ROWS = {
    # --- Notorious Monsters (11; 'Becut' flagged, see docstring)
    'amphiptere': SKIP,
    'came-cruse': '74',
    'scylla': SKIP,
    "grand'goule": SKIP,
    'gjenganger': SKIP, 'gorehound': SKIP, 'erebus': SKIP, 'feuerunke': SKIP,
    'lord ruthven': SKIP,
    'yilbegan': SKIP,
    # --- Adversaries (18)
    'cyhiraeth': '78-80',
    'dark elemental': '79-80',
    'dryptotaur': '79-80',
    'ekimmu': '79-80',
    'fulminator': '77-79',
    'gargouille': '77-80',
    'gawper': '80-81',
    'gigas cleaver': '80-82',
    'gigas flesher': '80-82',
    'gigas pelter': '80-82',
    'gigas pounder': '80-82',
    "gigas's tiger": '75-76',
    'glacial imp': '79-80',
    'ice elemental': '79-80',
    'icefang tiger': '77-79',
    'ruszor': '78-80',                   # stored 79-81 -> correction
    'thawed bones': '76-78',
    'angler crab': SKIP,
}

XARCABARD_ROWS = {
    # --- Notorious Monsters (12)
    'zirnitra': SKIP,
    'torvotaur': SKIP,
    'graoully': SKIP,
    'prince orobas': SKIP,
    'greater amphiptere': '82-83',       # blank on the NM table, 82-83 on the ADV table
    'tikbalang': SKIP,
    'gjenganger': SKIP, 'gorehound': SKIP, 'erebus': SKIP, 'feuerunke': SKIP,
    'lord ruthven': SKIP,
    'yilbegan': SKIP,
    # --- Adversaries (29)
    'adjudicator demon': '82',
    'berserker demon': '82',
    'caracal': '80-82',
    'cointeach': '79-80',
    'dark elemental': '80',
    'demon befouler': '80-81',
    'demon justiciar': '80-81',
    'demon magus': '80-81',
    'demon warrior': '80-81',
    "demon's elemental": '75-78',
    'dire gargouille': '80-82',          # stored 80-81 -> correction
    'eclipse demon': '82',
    'fusty gnole': '81-82',
    'gidim': '81-82',
    'gigas flogger': '80-82',
    'gigas hurler': '80-82',
    'gigas lopper': '80-82',
    'gigas slugger': '80-82',
    "gigas's tiger": '75-76',
    'gorgotaur': '81-82',
    'harum-scarum': '80-82',             # stored 81-82 -> correction
    'ice elemental': '80',
    'inferno demon': '82',
    'menacing eye': '80-81',
    'ruly imp': '80-81',
    'savage ruszor': '79-82',
    'snow wight': '80-81',
    'tarbotaur': '82-83',
}

# rule 245 - record has NO `lv`; after the add its ONLY zone is this page's
SETLV = [('menacing eye', XARCABARD)]

FLAGGED_NO_RECORD = ['Becut']


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
            'lv_union', 'lv_set', 'missing', 'kept_flat', 'twin_warn')}

    for table, zone in ((BEAUCEDINE_ROWS, BEAUCEDINE), (XARCABARD_ROWS, XARCABARD)):
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

    for key, zone in SETLV:
        mob = mobs[key]
        assert 'lv' not in mob, f'{key} already has lv - SETLV is additive only'
        zs = [z for z in mob.get('zones') or [] if isinstance(z, list)]
        assert len(zs) == 1 and zs[0][0] == zone and len(zs[0]) == 2, f'{key} zones={zs}'
        b = band(zs[0][1])
        mob['lv'] = [b[0], b[1]]
        log['lv_set'].append((key, mob['lv']))

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

    for name in ('added', 'filled', 'changed', 'lv_union', 'lv_set',
                 'missing', 'kept_flat', 'twin_warn'):
        rows = log[name]
        print(f'== {name} ({len(rows)})')
        for r in rows:
            print('   ', r)
    print(f'== blank_kept ({len(log["blank_kept"])})  == same ({len(log["same"])})')
    print(f'== NO RECORD IN mobs.json (flagged, not created): {FLAGGED_NO_RECORD}')


if __name__ == '__main__':
    main()
