#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 332
Author: BalladOfWorms

ONE ZONE: Reisenjima - 67 published rows, 0 missing.

ZONE STRING from zones.json (rule 244): `Reisenjima`.  (`Reisenjima Henge` and
`Reisenjima Sanctorium` are separate zones - this is neither.)

RULE 91 / RULE 262 AGAIN: zoneinfo holds 20 NM + 19 ADV.  The ADV count is exact.  The page
carries FOUR MORE NM tables under section headers - Geas Fete Tier 1 (12), Tier 2 (6),
Tier 3 (3) and HELM (7) - so it publishes 48 NM rows against zoneinfo's 20.  Same shape as
the two Escha pages last rev: the intake stopped at the first NM table.

SENTINELS
  SKIP  = blank Lv cell.  EVERY ONE of the 48 NM rows publishes a blank Lv here, and most of
          those records already store a level, so this is a SKIP-heavy page by construction.
  SETLV = rule 265 variant (additive only): a record with NO `lv` whose single zone entry
          already carries a band - `oryx` (129) and `neak` (145).  The band comes from the
          record's own stored entry, not from this page, which publishes nothing.

KEPT FLAT
  `sarsaok` stores `"Reisenjima"` as a bare string rather than a [zone, level] pair - the
  second instance of rule 263 in two revs.  Nothing lost this time (the page publishes no
  level for it), but it is unfillable until the 36 flat entries are converted.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()
REISENJIMA = 'Reisenjima'

ROWS = {
    # --- Notorious Monsters, main table (20) - every row blank
    'ascended beetle': SKIP, 'ascended chapuli': SKIP, 'ascended chigoe': SKIP,
    'ascended cyhiraeth': SKIP, 'ascended faaz': SKIP, 'ascended gefyrst': SKIP,
    'ascended hippogryph': SKIP, 'ascended lucani': SKIP, 'ascended luckybug': SKIP,
    'ascended mantis': SKIP, 'ascended mosquito': SKIP, 'ascended naraka': SKIP,
    'ascended panopt': SKIP, 'ascended poroggo': SKIP, 'ascended porxie': SKIP,
    'ascended tiger': SKIP, 'ascended ungeweder': SKIP, 'heavenly veela': SKIP,
    'ogdoad': SKIP, 'quetzalcoatl': SKIP,
    # --- Geas Fete Tier 1 (12)
    'belphegor': SKIP, 'crom dubh': SKIP, 'dazzling dolores': SKIP, 'golden kist': SKIP,
    'kabandha': SKIP, 'mauve-wristed gomberry': SKIP, 'oryx': SKIP,
    'sabotender royal': SKIP, 'sang buaya': SKIP, 'selkit': SKIP,
    'taelmoth the diremaw': SKIP, 'zduhac': SKIP,
    # --- Geas Fete Tier 2 (6)
    'bashmu': SKIP, 'gajasimha': SKIP, 'ironside': SKIP, 'old shuck': SKIP,
    'sarsaok': SKIP, 'strophadia': SKIP,
    # --- Geas Fete Tier 3 (3)
    'maju': SKIP, 'neak': SKIP, 'yakshi': SKIP,
    # --- HELM (7)
    'albumen': SKIP, 'erinys': SKIP, 'onychophora': SKIP, 'schah': SKIP,
    'teles': SKIP, 'vinipata': SKIP, 'zerde': SKIP,
    # --- Adversaries (19)
    'agitated chapuli': '122-124',
    'arboreal chigoe': '122-124',
    'asphyxiating cyhiraeth': '122-124',
    'devouring mosquito': '122-124',
    'glowering ladybug': '122-124',
    'ignoble skeleton': '122-124',
    'indomitable faaz': '122-124',
    'lentic toad': '122-124',
    'lucani': '122-124',
    'obstreperous panopt': '122-124',    # stored 115-119 -> correction
    'officious unseelie': '122-124',
    'perfervid naraka': '123-125',
    'porxie': '122-124',
    'quarrelsome hippogryph': '122-124',
    'rampaging beetle': '122-124',
    'snaggletoothed tiger': '122-124',
    'territorial mantis': '122-124',
    'wanton danaid': '123-125',          # stored 122-124 -> correction
    'wretched poroggo': '122-124',
}

SETLV = [('oryx', REISENJIMA), ('neak', REISENJIMA)]


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

    for key, lvl in ROWS.items():
        if f'{key} (monster)' in mobs:              # rule 239 guard
            log['twin_warn'].append(key)
        if f'{key} (s)' in mobs:                    # rule 247 guard
            log['twin_warn'].append(key + ' (s)')
        mob = mobs.get(key)
        if mob is None:
            log['missing'].append(key)
            continue
        apply_zone(mob, REISENJIMA, lvl, log, key)
        widen(mob, lvl, log, key)

    for key, zone in SETLV:
        mob = mobs[key]
        assert 'lv' not in mob, f'{key} already has lv - SETLV is additive only'
        zs = [z for z in mob.get('zones') or [] if isinstance(z, list)]
        assert len(zs) == 1 and zs[0][0] == zone and len(zs[0]) == 2, f'{key} zones={zs}'
        b = band(zs[0][1])
        mob['lv'] = [b[0], b[1]]
        log['lv_set'].append((key, mob['lv']))

    # REPORT ONLY - records whose global lv does not cover the band they store for this zone
    drift = []
    for key in ROWS:
        mob = mobs.get(key)
        if not mob or not isinstance(mob.get('lv'), list):
            continue
        for z in mob.get('zones') or []:
            if isinstance(z, list) and z[0] == REISENJIMA and len(z) == 2:
                b = band(z[1])
                if b and (b[0] < mob['lv'][0] or b[1] > mob['lv'][1]):
                    drift.append((key, z[1], mob['lv']))

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
    print(f'== REPORT ONLY: lv does not cover the stored zone band ({len(drift)})')
    for r in drift:
        print('   ', r)


if __name__ == '__main__':
    main()
