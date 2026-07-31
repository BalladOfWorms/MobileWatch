#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 315
Author: BalladOfWorms

TWO ZONES: Cirdas Caverns [U] (Delve/Skirmish instance) + Sih Gates.

Row tables transcribed from the BG-wiki page shots.
  SKIP  = the page's Lv cell is blank / '?'  -> ensure the zone exists, NEVER touch a stored level
          (refining rule 15; the writer physically cannot clear a level).
  a str = the page publishes that band -> add or overwrite the ZONE entry's level.

Rule 217 applied: every level I first read as ending in '8' was diffed against
zoneinfo before it became a correction.  Craklaw / Fulvous Jagil / Lyngbakr /
Malodorous Twitherym all decode to a final '3' (101-103), not 108.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

CIRDAS = 'Cirdas Caverns [U]'   # mobs.json convention (rule 216); zones.json spells it 'Cirdas Caverns U'
SIH = 'Sih Gates'

# ---------------------------------------------------------------- row tables
# Cirdas Caverns [U] - three Delve "Boss Monsters" tables, Lv column is '?' on every row
CIRDAS_ROWS = {
    'unfettered twitherym': SKIP,
    'transcendent scorpion': SKIP,
    'volatile matamata': SKIP,
    'perdurable raptor': SKIP,
    'tojil': SKIP,
    'aberrant uragnite': SKIP,
    'divagating jagil': SKIP,
}
# these three hold the UNBRACKETED 'Cirdas Caverns', which no page supports;
# their own spawn strings name "Cirdas Caverns [U] fracture"
CIRDAS_RESTRING = ['shimmering tarichuk', 'tutewehiwehi', 'kurma']
# Boss-Monsters-table rows that render as ordinary mobs
CIRDAS_NM = ['volatile matamata', 'perdurable raptor', 'aberrant uragnite', 'tojil']

# Sih Gates - 2 NM rows + 27 Adversaries
SIH_ROWS = {
    'fomor pioneer': SKIP,
    'furious arundmite': '126',
    'apex chapuli': '125-127',
    'apex jagil': '125-127',
    'apex leech': '125-127',
    'apex mandragora': '125-127',
    'baited jagil': SKIP,
    'bloated acuex': SKIP,
    'bonaria': SKIP,
    'burrowing chapuli': SKIP,
    'choleric umbril': '102-104',
    'craklaw': '101-103',
    'cthonic chapuli': SKIP,
    'echo bats': SKIP,
    'ferocious funguar': SKIP,
    'fetid twitherym': SKIP,
    'fulvous jagil': '101-103',
    'hemorraghic bats': SKIP,
    'javelin wasp': SKIP,
    'loathsome leech': SKIP,
    'loathsome obdella': SKIP,
    'lyngbakr': '101-103',
    'malodorous twitherym': '101-103',
    'mighty craklaw': '102-105',
    'somber obdella': SKIP,
    'speleothem gefyrst': SKIP,
    'speleothem ungeweder': SKIP,
    'sprightly acuex': '101-104',
    'unrelenting dullahan': '102-105',
}


def band(s):
    lo, _, hi = s.partition('-')
    return int(lo), int(hi or lo)


def apply_zone(mob, zone, lvl, log, key):
    zones = mob.setdefault('zones', [])
    entry = None
    for z in zones:
        if isinstance(z, list) and z and z[0] == zone:
            entry = z
            break
        if isinstance(z, str) and z == zone:      # legacy flat string
            entry = None
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
    """rule 9 - lv only ever grows to cover a published zone band."""
    if lvl is SKIP:
        return
    lo, hi = band(lvl)
    cur = mob.get('lv')
    if not isinstance(cur, list) or len(cur) != 2:
        return
    new = [min(cur[0], lo), max(cur[1], hi)]
    if new != cur:
        log['lv_union'].append((key, list(cur), new))
        mob['lv'] = new


def main():
    with open(PATH, encoding='utf-8') as fh:
        data = json.load(fh)
    mobs = data['mobs']

    log = {k: [] for k in
           ('added', 'filled', 'changed', 'blank_kept', 'same',
            'lv_union', 'restrung', 'nm_set', 'missing', 'kept_flat')}

    for table, zone in ((CIRDAS_ROWS, CIRDAS), (SIH_ROWS, SIH)):
        for key, lvl in table.items():
            mob = mobs.get(key)
            if mob is None:
                log['missing'].append(key)
                continue
            apply_zone(mob, zone, lvl, log, key)
            widen(mob, lvl, log, key)

    # unbracketed -> bracketed, page-backed
    for key in CIRDAS_RESTRING:
        mob = mobs[key]
        for z in mob.get('zones') or []:
            if isinstance(z, list) and z and z[0] == 'Cirdas Caverns':
                z[0] = CIRDAS
                log['restrung'].append((key, 'Cirdas Caverns', CIRDAS))

    for key in CIRDAS_NM:
        mob = mobs[key]
        if not mob.get('nm'):
            mob['nm'] = True
            log['nm_set'].append(key)

    # guards
    assert not [k for m in mobs.values() for k, v in m.items() if v is None], 'null poison'
    for k, m in mobs.items():
        for z in m.get('zones') or []:
            if isinstance(z, list):
                assert 1 <= len(z) <= 2 and isinstance(z[0], str), (k, z)
                assert len(z) == 1 or isinstance(z[1], str), (k, z)

    with open(PATH, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, separators=(', ', ': '), ensure_ascii=False)

    for name in ('added', 'filled', 'changed', 'lv_union', 'restrung',
                 'nm_set', 'missing', 'blank_kept', 'kept_flat', 'same'):
        rows = log[name]
        print(f'== {name} ({len(rows)})')
        for r in rows:
            print('   ', r)


if __name__ == '__main__':
    main()
