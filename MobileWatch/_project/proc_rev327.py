#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 327
Author: BalladOfWorms

TWO ZONES: Rolanberry Fields [S] (19 NM + 38 ADV) + Vunkerl Inlet [S] (6 NM + 40 ADV).
Rule 91 exact against zoneinfo on both.

ZONE STRINGS read out of zones.json FIRST (rule 244): `Rolanberry Fields [S]` and
`Vunkerl Inlet [S]` - both exactly as the pages print them, no apostrophe trap here.

SENTINELS
  SKIP  = the page's Lv cell is blank (incl. every "Fished Up" / Voidwalker row) -> never
          touch a stored level.  A missing zone still gets ADDED, level-less.
  VAGUE = the page publishes a LOOSER band than we already store (rule 237): keep ours.
          Used for `dark ixion` - page "80+", stored "80-85".

ROUTED ROWS (rule 239 - the `(monster)` twin, and the `(s)` twin)
  Four page rows do NOT go to the bare key:
    Lycopodium -> lycopodium (monster)     Ochu   -> ochu (monster)
    Chigoe     -> chigoe (monster)         Gnole  -> gnole (monster)
  In every one of those four the bare record holds ZERO zones file-wide and the twin
  already carries this zone.  Fifth/sixth/seventh confirmations of the rev-322/324 finding.
    Pallas -> pallas (s)                   (bare `pallas` is the Upper Delkfutt's Tower
                                            Gigas at 72; `pallas (s)` already holds this
                                            zone at 83.  One of the ten parked shared-key
                                            collisions, already split correctly in the data.)

NOT WRITTEN - FLAGGED
  Rolanberry's ADV table prints `Sapphire Quadav` with a BLANK Lv, but `sapphirine quadav`
  already holds `Rolanberry Fields [S]` at 66-69 while `sapphire quadav` holds Beadeaux /
  Qulun Dome / Ruhotz.  Two real records, one page row, nothing to gain from the blank cell
  -> no write, user's ruling.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()
VAGUE = object()

ROLANBERRY = 'Rolanberry Fields [S]'
VUNKERL = 'Vunkerl Inlet [S]'

ROLANBERRY_ROWS = {
    # --- Notorious Monsters (19)
    'dyinyinga': '65-68',
    'dark ixion': VAGUE,                 # page "80+", stored "80-85" (rule 237)
    'sandworm': '80+',                   # entry present with no level -> fill verbatim
    'delicieuse delphine': '~74',
    'erle': '62',
    'lamina': '58-60',                   # stored 57-60 -> correction
    'agathos': SKIP,
    'aither': SKIP, 'deorc': SKIP, 'eorthe': SKIP, 'puretos': SKIP,
    'pruina': SKIP, 'beorht': SKIP, 'thunor': SKIP, 'lacus': SKIP,
    'urd': SKIP, 'skuld': SKIP, 'verthandi': SKIP,
    'yilbegan': SKIP,                    # stores 90-92; blank cell must not wipe it (rule 15)
    # --- Adversaries (38)
    'snipper': SKIP, 'big jaw': SKIP, 'horrid fluke': SKIP,
    'greater pugil': SKIP, 'big leech': SKIP,
    'lycopodium (monster)': '28-31',     # ROUTED
    'death jacket': '39-42',
    'death wasp': '36-40',
    'coppercap': '47-49',
    'goobbue farmer': '59-62',
    'midnight wings': '38-42',
    'moon bat': '38-40',
    'ochu (monster)': '65-68',           # ROUTED
    'berry grub': '49-52',
    'worker crawler': '60-62',
    'wight': SKIP, 'evil spirit': SKIP,
    'fire elemental': SKIP, 'water elemental': SKIP,
    'chigoe (monster)': '53-55',         # ROUTED
    'poison leech': '44-47',
    'scabrous slug': '56-62',
    'dragonfly': '58-62',
    'clipper': SKIP,
    'hawker': '45-48',
    'bronze quadav': '65-68',
    'heliodor quadav': '65-68',
    'old quadav': '65-68',
    # 'sapphire quadav' - FLAGGED, not written (see docstring)
    'silver quadav': '65-68',
    'emerald quadav': '65-68',
    'brass quadav': '65-68',
    'goblin skirmisher': '56-59',
    'goblin patrolman': '56-59',
    'goblin franctireur': '56-59',
    'goblin draftee': '56-59',
    "goblin's crawler": '52-54',
    'sprite': SKIP,
}

VUNKERL_ROWS = {
    # --- Notorious Monsters (6)
    'big bang': '75',
    'judgmental julika': '82',
    'pallas (s)': '83',                  # ROUTED
    'procrustes': SKIP,                  # page prints "?"
    'warabouc': '75',
    'gaunab': SKIP,
    # --- Adversaries (40)
    'abyssal pugil': SKIP,
    'air elemental': '45',
    'bloodsucker': '60-65',
    'bugard': '67-70',
    'carrion marabou': '35-38',
    'chigoe (monster)': '55-56',         # ROUTED
    'demonic rose': '75-78',
    'dire bat': '61-63',
    'doom mage': '69-71',
    'doom soldier': '69-71',
    'dragonfly': '58-60',
    'duriumshell': '92-93',
    'fierce smilodon': '67-68',          # stored 67-70 -> correction
    'gigas deckhand': '78-82',
    'gigas helmsman': '78-82',
    'gigas jack': '78-82',
    'gigas marine': '78-82',
    "gigas's tiger": '73-75',
    'gnole (monster)': '68-72',          # ROUTED
    'goblin flagman': '66-69',
    'goblin grenadier': '66-69',
    'goblin guerrilla': '66-69',
    'goblin toxophilite': '66-69',
    "goblin's bat": '61-63',
    'goliath beetle': '34-36',
    'haunt': '66-69',
    'ignis djinn': '71-76',
    'orcish footsoldier': '71-73',
    'orcish gladiator': '71-73',
    'orcish hexspinner': '71-73',
    'orcish zerker': '71-73',
    'robber crab': '62-64',
    'royal leech': '37-40',
    'sprite': '65-68',
    'stygian pugil': '62-64',            # stored 60-66 -> correction
    'submarine nipper': SKIP,
    'thalassic pugil': SKIP,
    'thunder elemental': '60',
    'treant': '73-75',
    'wandering sapling': '33-36',
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
    blank = lvl is SKIP or lvl is VAGUE
    if entry is None:
        zones.append([zone] if blank else [zone, lvl])
        log['added'].append((key, zone, None if blank else lvl))
        return
    if lvl is VAGUE:
        log['vague_kept'].append((key, zone, entry[1] if len(entry) > 1 else None))
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
    """rule 9 - the global lv may only ever be EXTENDED, never narrowed."""
    if lvl is SKIP or lvl is VAGUE:
        return
    if lvl.endswith('+'):
        # "80+" is an open-ended FLOOR, not a measured band - widening the global lv
        # DOWN to it would trade a measured 85-88 for the page's vaguer wording (rule 237).
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
           ('added', 'filled', 'changed', 'blank_kept', 'vague_kept', 'same',
            'lv_union', 'missing', 'kept_flat', 'twin_warn')}

    for table, zone in ((ROLANBERRY_ROWS, ROLANBERRY), (VUNKERL_ROWS, VUNKERL)):
        for key, lvl in table.items():
            if f'{key} (monster)' in mobs:          # rule 239 guard
                log['twin_warn'].append(key)
            mob = mobs.get(key)
            if mob is None:
                log['missing'].append(key)
                continue
            apply_zone(mob, zone, lvl, log, key)
            widen(mob, lvl, log, key)

    assert not log['twin_warn'], f'(monster) twin exists for: {log["twin_warn"]}'
    assert not log['missing'], f'unmatched keys: {log["missing"]}'
    assert not [k for m in mobs.values() for k, v in m.items() if v is None], 'null poison'
    for k, mb in mobs.items():
        for z in mb.get('zones') or []:
            if isinstance(z, list):
                assert 1 <= len(z) <= 2 and isinstance(z[0], str), (k, z)
                assert len(z) == 1 or isinstance(z[1], str), (k, z)

    with open(PATH, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, separators=(', ', ': '), ensure_ascii=False)

    for name in ('added', 'filled', 'changed', 'lv_union', 'vague_kept',
                 'missing', 'kept_flat', 'twin_warn'):
        rows = log[name]
        print(f'== {name} ({len(rows)})')
        for r in rows:
            print('   ', r)
    print(f'== blank_kept ({len(log["blank_kept"])})  == same ({len(log["same"])})')


if __name__ == '__main__':
    main()
