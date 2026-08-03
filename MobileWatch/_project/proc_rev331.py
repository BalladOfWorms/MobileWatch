#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 331
Author: BalladOfWorms

TWO ZONES: Escha ZiTah and Escha RuAun - the two biggest pages of the sweep.
117 published rows, 0 missing.

ZONE STRINGS read out of zones.json FIRST (rule 244), and this is the trap again:
the pages are titled "Escha - Zi'Tah" and "Escha - Ru'Aun", but zones.json spells them
**`Escha ZiTah`** and **`Escha RuAun`** - no hyphen, no apostrophe, bare.

RULE 91: zoneinfo holds 13 NM + 20 ADV (ZiTah) and 3 NM + 13 ADV (RuAun).  The ADV counts
are exact.  The NM counts are NOT: each page carries SEVERAL NM tables under section
headers - Geas Fete Tier 1/2/3, HELM (ZiTah) and Geas Fete, Ark Angels, Heavenly Beasts,
Nazar (RuAun) - and zoneinfo captured only the FIRST table on each page.
Published NM rows: ZiTah 38 (zoneinfo 13), RuAun 46 (zoneinfo 3).  All 117 rows resolve to
a mobs.json record, so mobs.json is fine; zoneinfo is short by 25 and 43 rows.

SENTINELS
  SKIP  = blank Lv cell -> never touch a stored level.  Nearly every Geas Fete / Nazar /
          Heavenly Beast row publishes no level, and many already store one.
  SETLV = rule 245, additive only, for a record with NO `lv` whose single zone entry
          carries a band: `eschan sorceror` (page and store agree at 70-78) and
          `duke vepar` (the band comes from the record's OWN stored entry, 135, since the
          page publishes nothing - noted in the handoff as a variant of the rule).
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

ZITAH = 'Escha ZiTah'
RUAUN = 'Escha RuAun'

ZITAH_ROWS = {
    # --- Notorious Monsters, main table (13)
    'prickly pitriv': '75', 'hugemaw harold': '75', 'serpopard ninlil': '99',
    'abyssdiver': '119', 'immanibugard': '119', 'jester malatrix': '119',
    'keeper of heiligtum': '122', 'voso': '122', 'emperor arthro': '122',
    'beist': '125', 'muut': '125', 'eschan jewelweed': SKIP, 'azi dahaka': SKIP,
    # --- Geas Fete Tier 1 (12), all blank
    'wepwawet': SKIP, 'lustful lydia': SKIP, 'aglaophotis': SKIP, 'tangata manu': SKIP,
    'vidala': SKIP, 'gestalt': SKIP, 'angrboda': SKIP, 'cunnast': SKIP,
    'revetaur': SKIP, 'ferrodon': SKIP, 'gulltop': SKIP, 'vyala': SKIP,
    # --- Geas Fete Tier 2 (6), all blank
    'ionos': SKIP, 'sensual sandy': SKIP, 'nosoi': SKIP, 'brittlis': SKIP,
    'kamohoalii': SKIP, 'umdhlebi': SKIP,
    # --- Geas Fete Tier 3 (3)
    'fleetstalker': '135', 'shockmaw': '135', 'urmahlullu': '135',
    # --- HELM (4), all blank
    'alpluachra bucca and puca': SKIP, 'blazewing': SKIP, 'pazuzu': SKIP, 'wrathare': SKIP,
    # --- Adversaries (20)
    'eschan worm': '50-59', 'eschan obdella': '50-59', 'eschan crawler': '52-59',
    'eschan dhalmel': '59-68', 'eschan weapon': '59-69', 'eschan coeurl': '61-69',
    'eschan vulture': '70-79', 'eschan warrior': '70-78', 'eschan sorceror': '70-78',
    'eschan corse': '72-79', 'eschan goobbue': '80-89', 'eschan wasp': '80-89',
    'eschan snapweed': '80-89', 'eschan bugard': '107-110', 'eschan opo-opo': '107-110',
    'eschan puk': '107-110', 'eschan shadow dragon': '107-110',
    'eschan tarichuk': '107-110', 'eschan yztarg': '107-110', 'eschan mosquito': '119',
}

RUAUN_ROWS = {
    # --- Notorious Monsters, main table (3), all blank
    'naga raja': SKIP, "naga raja's lamia": SKIP, 'eschan porxie': SKIP,
    # --- Geas Fete Tier 1 (12), all blank
    'asida': SKIP, 'bia': SKIP, 'emputa': SKIP, 'khon': SKIP, 'khun': SKIP, 'ma': SKIP,
    'met': SKIP, 'peirithoos': SKIP, 'ruea': SKIP, 'sava savanovic': SKIP,
    'tenodera': SKIP, 'wasserspeier': SKIP,
    # --- Geas Fete Tier 2 (6), all blank
    'amymone': SKIP, 'hanbi': SKIP, 'kammavaca': SKIP, 'naphula': SKIP,
    'palila': SKIP, 'yilan': SKIP,
    # --- Geas Fete Tier 3 (3), all blank
    'duke vepar': SKIP, 'pakecet': SKIP, "vir'ava": SKIP,
    # --- Ark Angels (5), all blank
    'ark angel ev': SKIP, 'ark angel gk': SKIP, 'ark angel hm': SKIP,
    'ark angel mr': SKIP, 'ark angel tt': SKIP,
    # --- Heavenly Beasts (6), all blank
    'byakko': SKIP, 'genbu': SKIP, 'kirin': SKIP, 'kouryu': SKIP,
    'seiryu': SKIP, 'suzaku': SKIP,
    # --- Nazar (11), all blank
    'warder of courage': SKIP, 'warder of dignity': SKIP, 'warder of faith': SKIP,
    'warder of fortitude': SKIP, 'warder of hope': SKIP, 'warder of justice': SKIP,
    'warder of love': SKIP, 'warder of loyalty': SKIP, 'warder of mercy': SKIP,
    'warder of prudence': SKIP, 'warder of temperance': SKIP,
    # --- Adversaries (13)
    'eschan zdei': '81-85', 'eschan gargouille': '110-112', 'eschan phuabo': '112-115',
    "eschan il'aern": '115-119', 'eschan ghrah': '115-119', 'eschan limule': '115-119',
    'eschan murex': '115-119', 'eschan hpemde': '115-119', 'eschan amoeban': '115-119',
    'eschan euvhi': '115-119', 'eschan clionid': '115-119', 'eschan xzomit': '115-119',
    'eschan yovra': '120-121',
}

SETLV = [('eschan sorceror', ZITAH), ('duke vepar', RUAUN)]


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

    for table, zone in ((ZITAH_ROWS, ZITAH), (RUAUN_ROWS, RUAUN)):
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


if __name__ == '__main__':
    main()
