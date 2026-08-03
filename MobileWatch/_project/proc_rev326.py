#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 326
Author: BalladOfWorms

TWO ZONES: Crawlers Nest [S] (4 NM + 32 ADV) + Pashhow Marshlands [S] (11 NM + 38 ADV).

ZONE STRING: `Crawlers Nest [S]` - NO apostrophe, per zones.json and all 41 stored entries.
(My first comparison used `Crawlers' Nest [S]` and reported the whole zone as unzoned; that was
the wrong string, not a data gap.  Check zones.json for the canonical spelling FIRST.)

SKIP  = the page's Lv cell is blank (incl. every "Fished Up" row) -> never touch a stored level.
SETLV = additive only: give `lv` to a record that has NONE, from the band the page publishes for
        its ONLY zone.  Used for the 16 Apex/Locus rows, every one of which holds this zone alone.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

NEST = 'Crawlers Nest [S]'
PASHHOW = 'Pashhow Marshlands [S]'

NEST_ROWS = {
    'abatwa': SKIP,
    'lugh': SKIP,
    'morille mortelle': '82-83',
    'nympha eunomia': SKIP,
    'apex lugcrawler': '129-131',
    'locus lugcrawler': '129-131',
    'apex hornfly': '131-133',
    'apex worker lugcrawler': '132-134',
    'apex nest elytra': '132-134',
    'apex dragonfly': '133-135',
    'apex soldier lugcrawler': '134-136',
    'apex blazer elytra': '134-136',
    'apex mycelar': '136-138',
    'apex rumble lugcrawler': '136-138',
    'apex helm elytra': '136-138',
    'apex doom scorpion': '136-138',
    'apex lugcrawler hunter': '137-139',
    'apex knight lugcrawler': '138-140',
    'apex fire elemental': '132-135',
    'apex water elemental': '132-135',
    'brass quadav': '66-69',
    'bronze quadav': '66-69',
    'doom scorpion': '72-74',
    'electrumcap': '68-70',
    'emerald quadav': '66-69',
    'fire elemental': '70',
    'heliodor quadav': '66-69',
    'labyrinth lizard': '64-66',
    'old quadav': '66-69',
    'processionaire': '69-71',
    'puroboros': '72-73',
    'sapphirine quadav': '66-69',
    'silver quadav': '66-69',
    'water elemental': '70',
    'wespe': '63-65',
    'witch hazel': '62-64',
}

PASHHOW_ROWS = {
    'kinepikwa': '78',
    'croque-mitaine': SKIP,
    'nommo': SKIP,
    'sugaar': SKIP,
    'melancholic moira': SKIP,
    'ground guzzler': SKIP,
    'globster': SKIP,
    'shoggoth': SKIP,
    'lamprey lord': SKIP,
    'blobdingnag': SKIP,
    'yilbegan': SKIP,
    'swamp leech': SKIP,
    'stag crab': SKIP,
    'swamp pugil': SKIP,
    'thread leech': SKIP,
    'snipper': '62-65',
    'ancient quadav': '76-78',
    'bog bunny': '62-64',
    'bogy': '71-73',
    'elder quadav': '71-74',
    'electrumcap': '68-70',
    'gadfly': '64-68',
    'garnet quadav': '71-74',
    'ghoul': SKIP,
    'goblin flagman': '66-69',
    'goblin grenadier': '66-69',
    'goblin guerrilla': '66-69',
    'goblin toxophilite': SKIP,
    "goblin's dragonfly": '61-63',
    'gold quadav': '76-78',
    'goobbue': '73-76',
    'lou carcolh': '69-73',
    'malboro': '71-74',
    'moor hound': '69-71',
    'mousse': '69-71',
    'mythril quadav': SKIP,
    'nickel quadav': SKIP,
    'night bats': '65-67',
    'peiste': '73-76',
    'ruby quadav': SKIP,
    'sanguine bat': SKIP,
    'silver quadav': '71-74',
    'sprite': '61-64',
    'thunder elemental': SKIP,
    'vajra quadav': '76-78',
    'virulent peiste': '78-81',
    'water elemental': SKIP,
    'zircon quadav': '71-74',
    'zombie': SKIP,
}

# records with NO `lv` at all whose single zone is this page - additive fill of the global band
SETLV = ['apex lugcrawler', 'locus lugcrawler', 'apex hornfly', 'apex worker lugcrawler',
         'apex nest elytra', 'apex dragonfly', 'apex soldier lugcrawler', 'apex blazer elytra',
         'apex mycelar', 'apex rumble lugcrawler', 'apex helm elytra', 'apex doom scorpion',
         'apex lugcrawler hunter', 'apex knight lugcrawler', 'apex fire elemental',
         'apex water elemental']


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
            'lv_union', 'lv_set', 'missing', 'kept_flat', 'twin_warn')}

    for table, zone in ((NEST_ROWS, NEST), (PASHHOW_ROWS, PASHHOW)):
        for key, lvl in table.items():
            if f'{key} (monster)' in mobs:
                log['twin_warn'].append(key)
            mob = mobs.get(key)
            if mob is None:
                log['missing'].append(key)
                continue
            apply_zone(mob, zone, lvl, log, key)
            widen(mob, lvl, log, key)

    for key in SETLV:
        mob = mobs[key]
        assert 'lv' not in mob, f'{key} already has lv - SETLV must be additive only'
        zs = [z for z in mob.get('zones') or [] if isinstance(z, list)]
        assert len(zs) == 1 and zs[0][0] == NEST and len(zs[0]) == 2, f'{key} zones={zs}'
        b = band(zs[0][1])
        mob['lv'] = [b[0], b[1]]
        log['lv_set'].append((key, mob['lv']))

    assert not log['twin_warn'], f'(monster) twin exists for: {log["twin_warn"]}'
    assert not [k for m in mobs.values() for k, v in m.items() if v is None], 'null poison'
    for k, m in mobs.items():
        for z in m.get('zones') or []:
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


if __name__ == '__main__':
    main()
