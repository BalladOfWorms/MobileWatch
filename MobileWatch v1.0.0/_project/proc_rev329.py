#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 329
Author: BalladOfWorms

THREE ZONES: Castle Zvahl Baileys [S] (0 NM + 40 ADV), Manaclipper (3 NM + 8 ADV),
Phanauet Channel (3 NM + 10 ADV).  Rule 91 exact against zoneinfo on all three.

ZONE STRINGS read out of zones.json FIRST (rule 244): `Castle Zvahl Baileys [S]`,
`Manaclipper`, `Phanauet Channel`.  (`Castle Zvahl Baileys` and `Castle Zvahl Keep [S]`
are separate zones - this is neither.)

Castle Zvahl Baileys [S] arrives with ONE holder against forty published rows, and the
page publishes a level on only two of them.  So it is almost entirely level-less ADDS:
the row itself is the data.

SENTINEL
  SKIP = the page's Lv cell is blank -> never touch a stored level.  A missing zone is
         still ADDED, level-less.  Phanauet's five blank rows (`big jaw`, `fishtrap`,
         `flytrap`, `giant pugil`, `snipper`) all already store a level for the zone and
         keep it untouched - USER, this rev: "if we already have info on a mob somewhere,
         that mob stays."
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

ZVAHL = 'Castle Zvahl Baileys [S]'
MANACLIPPER = 'Manaclipper'
PHANAUET = 'Phanauet Channel'

# 40 Adversaries; the page has NO NM table (zoneinfo agrees: 0).
# Only two rows publish a level, and only four publish a Genus.
ZVAHL_ROWS = {
    'adaman quadav': SKIP,
    'ancient quadav': SKIP,
    'dark elemental': SKIP,
    'deathwreaker demon': SKIP,
    'demon befouler': SKIP,
    'demon condemner': SKIP,
    'demon corrupter': SKIP,
    'demon entomber': SKIP,
    'demon justiciar': SKIP,
    'demon magus': SKIP,
    'demon suppressor': SKIP,
    'demon warrior': SKIP,
    "demon's elemental": '75-80',
    'dire gargouille': SKIP,
    'doom lens': SKIP,
    'errand imp': SKIP,
    'foredoomer demon': SKIP,
    'gold quadav': SKIP,
    'ice elemental': SKIP,
    'icefall': '79-82',
    'iron quadav': SKIP,
    'magnes quadav': SKIP,
    'ogler': SKIP,
    'orcish augur': SKIP,
    'orcish bowshooter': SKIP,
    'orcish champion': SKIP,
    'orcish dragonbrander': SKIP,
    'orcish protector': SKIP,
    'orcish veteran': SKIP,
    'orcish warlord': SKIP,
    'soulsearer demon': SKIP,
    'star ruby quadav': SKIP,
    'vajra quadav': SKIP,
    'woebringer demon': SKIP,
    'yagudo chanter': SKIP,
    'yagudo eradicator': SKIP,
    'yagudo high priest': SKIP,
    'yagudo knight templar': SKIP,
    'yagudo prelate': SKIP,
    'yagudo sentinel': SKIP,
}

MANACLIPPER_ROWS = {
    # --- Notorious Monsters (3)
    'cyclopean conch': SKIP,
    'harajnite': SKIP,
    'zoredonite': '62',
    # --- Adversaries (8)
    'cutter': '25-35',                   # stored 28-30 -> correction
    'fatty pugil': '25-35',
    'clot': '30-35',
    'uragnite': '30-37',
    'colossal calamari': '40-42',
    'ghost crab': '30-34',
    'greater pugil': '35-39',
    'kraken': '40-42',
}

PHANAUET_ROWS = {
    # --- Notorious Monsters (3)
    'aipaloovik': SKIP,
    'stubborn dredvodd': '37-38',
    'vodyanoi': '45-47',
    # --- Adversaries (10)
    'big jaw': SKIP,
    'fishtrap': SKIP,
    'flytrap': SKIP,
    'giant pugil': SKIP,
    'ooze': '25-29',
    'protozoan': '29-31',
    'snipper': SKIP,
    'thickshell': '10-20',
    'thunder elemental': SKIP,
    'water elemental': SKIP,
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

    for table, zone in ((ZVAHL_ROWS, ZVAHL), (MANACLIPPER_ROWS, MANACLIPPER),
                        (PHANAUET_ROWS, PHANAUET)):
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
