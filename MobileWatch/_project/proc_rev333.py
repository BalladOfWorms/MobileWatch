#!/usr/bin/env python3
"""
MobileWatch mobs.json - rev 333
Author: BalladOfWorms

FOUR JOBS, all from the user's instructions this session:

1. NYZUL ISLE.  The floor-layout table lists 41 distinct mobs; all 41 have records and
   THREE of them have no zones at all (`kulshedra`, `manticore`, `bull bugard`).
   USER: "if we have mobs on this list that dont have zones in our app, we can add this
   zone" -> only those three get `Nyzul Isle`; the other 38 already carry zones and are
   left alone.

2. THE ` (monster)` SUFFIX RETIRED.  USER: "only nms get '(NM)' appending their name if we
   have duplicate names, monsters are left alone."
   Twenty-two records ended in ` (monster)`.  Twenty-one are TRUE DUPLICATES of their
   base-named twin - two imports of one mob, not two mobs (the base side carries the old
   NM-list shape: fam=None, no `ab`, half-tier resist grid, agg/lnk/resp; the twin side
   carries the bestiary family pass: fam set, full kit, family grid).  Those 21 MERGE into
   the plain name.
   ONE is a genuine name collision: `siren` is the AVATAR (fam=Avatar, siren prime.png) and
   `siren (monster)` is a Lesser Bird.  Per the rule the monster keeps the plain name and
   the notable one takes the suffix -> `siren (nm)` / n "Siren (NM)".  FLAGGED: one line to
   revert if you would rather the avatar kept the bare name.

   MERGE POLICY: the surviving record is the PRIMARY = whichever side holds more zones
   (rule 246's census; ties broken by key count).  Every field the primary lacks is folded
   in from the other side, `zones` and `lv` are unioned, `notes` are concatenated, and
   every field where the two disagreed is PRINTED so nothing is dropped silently.

3. zoneinfo rows spelled `X (Monster)` (5 of them) renamed to the plain name to match.

4. GEAS FETE CONTENT TAGS - 96 mobs across the three Eschan zones, tagged
   `Geas Fete: <zone>: <group>` so the new Content > Geas Fete screen can read them live.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
MOBS = os.path.join(ASSETS, 'mobs.json')
ZINFO = os.path.join(ASSETS, 'zoneinfo.json')

NYZUL = 'Nyzul Isle'
NYZUL_ADD = ['kulshedra', 'manticore', 'bull bugard']

# the one genuine collision - handled by rename, not merge
COLLISION = 'siren'

DROP_NOTES = {'Likely duplicate of Antares (Monster).'}

LIST_FIELDS = ('ab', 'sp', 'wk', 'st', 'det', 'im', 'ab_el', 'notes', 'content', 'zones')

GEAS = {
    'Escha ZiTah': {
        'Tier 1': ['wepwawet', 'lustful lydia', 'aglaophotis', 'tangata manu', 'vidala',
                   'gestalt', 'angrboda', 'cunnast', 'revetaur', 'ferrodon', 'gulltop', 'vyala'],
        'Tier 2': ['ionos', 'sensual sandy', 'nosoi', 'brittlis', 'kamohoalii', 'umdhlebi'],
        'Tier 3': ['fleetstalker', 'shockmaw', 'urmahlullu'],
        'HELM': ['alpluachra bucca and puca', 'blazewing', 'pazuzu', 'wrathare'],
    },
    'Escha RuAun': {
        'Tier 1': ['asida', 'bia', 'emputa', 'khon', 'khun', 'ma', 'met', 'peirithoos',
                   'ruea', 'sava savanovic', 'tenodera', 'wasserspeier'],
        'Tier 2': ['amymone', 'hanbi', 'kammavaca', 'naphula', 'palila', 'yilan'],
        'Tier 3': ['duke vepar', 'pakecet', "vir'ava"],
        'Ark Angels': ['ark angel ev', 'ark angel gk', 'ark angel hm', 'ark angel mr',
                       'ark angel tt'],
        'Heavenly Beasts': ['byakko', 'genbu', 'kirin', 'kouryu', 'seiryu', 'suzaku'],
        'Nazar': ['warder of courage', 'warder of dignity', 'warder of faith',
                  'warder of fortitude', 'warder of hope', 'warder of justice',
                  'warder of love', 'warder of loyalty', 'warder of mercy',
                  'warder of prudence', 'warder of temperance'],
    },
    'Reisenjima': {
        'Tier 1': ['belphegor', 'crom dubh', 'dazzling dolores', 'golden kist', 'kabandha',
                   'mauve-wristed gomberry', 'oryx', 'sabotender royal', 'sang buaya',
                   'selkit', 'taelmoth the diremaw', 'zduhac'],
        'Tier 2': ['bashmu', 'gajasimha', 'ironside', 'old shuck', 'sarsaok', 'strophadia'],
        'Tier 3': ['maju', 'neak', 'yakshi'],
        'HELM': ['albumen', 'erinys', 'onychophora', 'schah', 'teles', 'vinipata', 'zerde'],
    },
}


def zkey(z):
    return z[0] if isinstance(z, list) else z


def union_zones(a, b):
    out = list(a or [])
    have = {zkey(z): i for i, z in enumerate(out)}
    for z in (b or []):
        k = zkey(z)
        if k not in have:
            out.append(z)
            have[k] = len(out) - 1
        else:
            cur = out[have[k]]
            # prefer the entry that carries a level
            if isinstance(z, list) and len(z) == 2 and not (isinstance(cur, list) and len(cur) == 2):
                out[have[k]] = z
    return out


def merge_pair(mobs, base, twin, log):
    B, T = mobs.get(base), mobs[twin]
    if B is None:                                   # no base record: plain rename
        T['n'] = T['n'].replace(' (Monster)', '').replace(' (monster)', '')
        mobs[base] = T
        del mobs[twin]
        log['renamed'].append(base)
        return
    bz = len([z for z in (B.get('zones') or [])])
    tz = len([z for z in (T.get('zones') or [])])
    primary, secondary = (T, B) if tz > bz else (B, T)
    if tz == bz:
        primary, secondary = (T, B) if len(T) > len(B) else (B, T)
    which = 'twin' if primary is T else 'base'

    merged = dict(primary)
    folded, conflicts = [], []
    for f, v in secondary.items():
        if f in ('n', 'zones', 'lv', 'notes'):
            continue
        if f not in merged:
            merged[f] = v
            folded.append(f)
        elif merged[f] != v:
            conflicts.append((f, merged[f], v))

    merged['zones'] = union_zones(primary.get('zones'), secondary.get('zones'))
    if not merged['zones']:
        merged.pop('zones')

    lv = [x.get('lv') for x in (primary, secondary)
          if isinstance(x.get('lv'), list) and len(x.get('lv')) == 2]
    if lv:
        merged['lv'] = [min(x[0] for x in lv), max(x[1] for x in lv)]

    notes = []
    for x in (primary, secondary):
        for nt in (x.get('notes') or []):
            if nt not in notes and nt not in DROP_NOTES:
                notes.append(nt)
    if notes:
        merged['notes'] = notes
    else:
        merged.pop('notes', None)

    merged['n'] = (B.get('n') or T.get('n', '')).replace(' (Monster)', '').replace(' (monster)', '')

    mobs[base] = merged
    del mobs[twin]
    log['merged'].append((base, which, len(merged.get('zones') or []), folded, conflicts))


def main():
    with open(MOBS, encoding='utf-8') as fh:
        data = json.load(fh)
    mobs = data['mobs']
    log = {k: [] for k in ('nyzul', 'merged', 'renamed', 'collision', 'tagged', 'zinfo')}

    # ---- 1. Nyzul Isle -------------------------------------------------------------
    for k in NYZUL_ADD:
        mob = mobs[k]
        assert not mob.get('zones'), f'{k} already has zones'
        mob['zones'] = [[NYZUL]]
        log['nyzul'].append((k, mob.get('fam'), mob.get('lv')))

    # ---- 2. retire the ` (monster)` suffix ------------------------------------------
    pairs = sorted(k[:-10] for k in mobs if k.endswith(' (monster)'))
    for base in pairs:
        if base == COLLISION:
            continue
        merge_pair(mobs, base, base + ' (monster)', log)

    # the genuine collision: monster takes the plain name, the notable one takes (nm)
    av = mobs.pop(COLLISION)
    bird = mobs.pop(COLLISION + ' (monster)')
    av['n'] = 'Siren (NM)'
    bird['n'] = 'Siren'
    mobs[COLLISION + ' (nm)'] = av
    mobs[COLLISION] = bird
    log['collision'].append(('siren (nm)', av.get('fam'), 'siren', bird.get('fam')))

    assert not [k for k in mobs if k.endswith(' (monster)')], 'a (monster) key survived'

    # ---- 4. Geas Fete content tags ---------------------------------------------------
    for zone, groups in GEAS.items():
        for grp, keys in groups.items():
            tag = f'Geas Fete: {zone}: {grp}'
            for k in keys:
                mob = mobs[k]
                tags = mob.setdefault('content', [])
                if tag not in tags:
                    tags.append(tag)
                    log['tagged'].append((k, tag))

    assert not [k for m in mobs.values() for k, v in m.items() if v is None], 'null poison'
    for k, mb in mobs.items():
        for z in mb.get('zones') or []:
            if isinstance(z, list):
                assert 1 <= len(z) <= 2 and isinstance(z[0], str), (k, z)
                assert len(z) == 1 or isinstance(z[1], str), (k, z)

    with open(MOBS, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, separators=(', ', ': '), ensure_ascii=False)

    # ---- 3. zoneinfo rows spelled "(Monster)" ---------------------------------------
    with open(ZINFO, encoding='utf-8') as fh:
        zi = json.load(fh)
    for slug, e in zi.items():
        if not isinstance(e, dict):
            continue
        for sec in ('nms', 'mobs'):
            for r in e.get(sec, []) or []:
                if isinstance(r, dict) and isinstance(r.get('n'), str) and '(Monster)' in r['n']:
                    old = r['n']
                    r['n'] = old.replace(' (Monster)', '')
                    log['zinfo'].append((slug, sec, old, r['n']))
    with open(ZINFO, 'w', encoding='utf-8') as fh:
        json.dump(zi, fh, separators=(', ', ': '), ensure_ascii=False)

    print(f'== Nyzul Isle adds ({len(log["nyzul"])})')
    for r in log['nyzul']:
        print('   ', r)
    print(f'== (monster) merges ({len(log["merged"])})')
    for base, which, nz, folded, conflicts in log['merged']:
        print(f'    {base:18s} primary={which:4s} zones={nz}  folded={folded}')
        for f, kept, dropped in conflicts:
            print(f'        conflict {f}: KEPT {str(kept)[:60]}')
            print(f'        {" "*(9+len(f))} drop {str(dropped)[:60]}')
    print(f'== collision renamed ({len(log["collision"])}): {log["collision"]}')
    print(f'== zoneinfo rows renamed ({len(log["zinfo"])})')
    for r in log['zinfo']:
        print('   ', r)
    print(f'== Geas Fete tags ({len(log["tagged"])})')


if __name__ == '__main__':
    main()
