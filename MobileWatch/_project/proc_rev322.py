#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 322
Author: BalladOfWorms

TWO ZONES: Batallia Downs [S] (19 NM + 23 ADV) + Jugner Forest [S] (12 NM + 29 ADV).

PLUS A REVERT I OWE.  There is a 22-record `<name> (monster)` duplicate class, and in revs 320-321
I added three zone entries to the BASE twin while the `(monster)` twin already held the identical
zone at the identical level - which puts two same-named rows under one zone header in the Zone view.
Those three adds are removed here, restoring the exact pre-rev-320 state.  The merge question itself
is NOT decided.

Consequently the two rows on this page whose `(monster)` twin already carries the zone are written
to the TWIN, not the base: `gnole (monster)` and `lycopodium (monster)`.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

BATALLIA = 'Batallia Downs [S]'
JUGNER = 'Jugner Forest [S]'

# (key, zone, level) added in revs 320-321 that duplicate the `(monster)` twin's own entry
REVERT = [
    ('chigoe', 'Grauberg [S]', '43-46'),
    ('crawler', 'West Sarutabaruta [S]', '18-21'),
    ('lycopodium', 'Fort Karugo-Narugo [S]', '22-25'),
]

BATALLIA_ROWS = {
    'chaneque': '58-60',
    'dark ixion': '80-85',
    'habergoass': SKIP,
    'la velue': '60',
    'sandworm': '~88',
    'burlibix brawnback': SKIP,
    'taweret': SKIP,                     # the page spells it "Tawaret"
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
    'ba': '36-37',
    'clipper': '32-35',
    'djinn': '54-56',
    'earth elemental': SKIP,
    'evil spirit': SKIP,
    'forester beetle': '47-50',
    'gnole (monster)': '65-67',          # twin holds the zone; base `gnole` has none
    'goblin blastmaster': '62-64',
    'goblin corpsman': '62-64',
    'goblin freesword': '62-64',
    'goblin pioneer': '62-64',
    'ice elemental': SKIP,
    'lycopodium (monster)': '28-31',     # twin already holds it at 28-31
    'orcish brawler': '65-67',
    'orcish chasseur': '65-67',
    'orcish impaler': '65-67',
    'orcish trooper': '65-67',
    'pixie': '56-59',
    'sadfly': '29-31',
    'smilodon': '46-48',
    'stalking sapling': '31-34',
    'tsetse fly': '93-94',
    'wight': SKIP,
}

JUGNER_ROWS = {
    'dark ixion': '80-85',
    'vulkodlac': SKIP,
    'boll weevil': SKIP,
    'drumskull zogdregg': SKIP,
    'voirloup': SKIP,
    'kholomodumo': SKIP,
    'quagmire pugil': SKIP,
    'sunderclaw': SKIP,
    'yacumama': SKIP,
    'capricornus': SKIP,
    'krabkatoa': SKIP,
    'yilbegan': SKIP,
    'biddybug': '62-64',
    'brutal sheep': '38-41',
    'decrepit gnole': '73-76',
    'forest leech': '38-41',
    'ghoul': '38-41',                    # two rows (BLM + WAR), one record
    'gnoletrap': '93-94',
    'goblin bombardier': '71-73',
    'goblin field doctor': '71-73',
    'goblin paratrooper': '71-73',
    'goblin picket': '71-73',
    'hawkertrap': '42-44',
    'ignis djinn': '77-79',
    'jugner funguar': '42-44',
    'land pugil': '38-41',
    'lobison': '80-82',
    'orcish bowshooter': '77-79',
    'orcish champion': '77-79',
    'orcish dragonbrander': '77-79',
    'orcish protector': '77-79',
    'orcish veteran': '77-79',
    'screamer': '42-44',
    'snipper': '38-41',
    'sprite': '61-63',
    'stag beetle': '38-41',
    'thunder elemental': SKIP,
    'walking tree': '54-56',
    'wandering sapling': '38-41',
    'war smilodon': '57-59',
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
            'lv_union', 'missing', 'kept_flat', 'reverted')}

    # ---- the revert
    for key, zone, lvl in REVERT:
        twin = f'{key} (monster)'
        assert any(isinstance(z, list) and z[0] == zone and len(z) > 1 and z[1] == lvl
                   for z in mobs[twin].get('zones') or []), f'{twin} does not hold {zone} {lvl}'
        zs = mobs[key].get('zones') or []
        before = len(zs)
        mobs[key]['zones'] = [z for z in zs
                              if not (isinstance(z, list) and z[0] == zone
                                      and len(z) > 1 and z[1] == lvl)]
        if not mobs[key]['zones']:
            del mobs[key]['zones']
        log['reverted'].append((key, zone, lvl, before, len(mobs[key].get('zones') or [])))

    for table, zone in ((BATALLIA_ROWS, BATALLIA), (JUGNER_ROWS, JUGNER)):
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

    for name in ('reverted', 'added', 'filled', 'changed', 'lv_union',
                 'missing', 'blank_kept', 'kept_flat'):
        rows = log[name]
        print(f'== {name} ({len(rows)})')
        for r in rows:
            print('   ', r)
    print(f'== same ({len(log["same"])})')


if __name__ == '__main__':
    main()
