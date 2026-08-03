#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rev 288 — normalize stored ABJURATION drop names to the item DB's form.

The DB stores every abjuration as `<Prefix>.Abjuration: <Slot>` with **NO SPACE**
after the prefix dot and an abbreviated slot: Bd. Ft. Hd. Hn. Lg.
122 such entries exist (24 families x 5 slots, + `Lib. Abjuration` / `Obl. Abjuration`).

The family->prefix map is NOT guessed: candidate prefixes are those that are a real
prefix of the family word, then constraint-propagated (a family with one candidate
claims it, freeing the ambiguous ones), and every rewritten name is verified present
in ffxi_items.json before it is written.
"""
import json, os, re, sys, collections

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
SLOT = {'Head': 'Hd.', 'Body': 'Bd.', 'Hands': 'Hn.', 'Legs': 'Lg.', 'Feet': 'Ft.'}


def load():
    mp = os.path.join(ASSETS, 'mobs.json')
    with open(mp, encoding='utf-8') as f:
        d = json.load(f)
    with open(os.path.join(ASSETS, 'ffxi_items.json'), encoding='utf-8') as f:
        it = json.load(f)
    names = {v['n'] for v in it.values() if isinstance(v, dict) and 'n' in v}
    return mp, d, names


def build_prefix_map(names, families):
    """Return {family: prefix} using only prefixes that really exist in the DB."""
    dbpre = sorted({re.match(r'^(.*?)Abjuration', n).group(1)
                    for n in names if 'Abjuration' in n})
    dbpre = [p for p in dbpre if p.endswith('.')]            # drop the spaced oddballs
    cand = {f: {p for p in dbpre if f.startswith(p[:-1])} for f in families}
    resolved, changed = {}, True
    while changed:
        changed = False
        for f, ps in list(cand.items()):
            ps -= set(resolved.values())
            if len(ps) == 1:
                resolved[f] = ps.pop()
                del cand[f]
                changed = True
    return resolved, cand


def sweep(write=False):
    mp, d, names = load()
    mobs = d['mobs']
    bad = []
    for k, v in mobs.items():
        for x in [s.strip() for s in (v.get('drops') or '').split(',') if s.strip()]:
            if 'Abjuration' in x and x not in names:
                bad.append((k, x))
    fams = sorted({x.split(' Abjuration')[0] for _, x in bad if ' Abjuration' in x})
    pmap, unresolved = build_prefix_map(names, fams)
    print('families seen  :', len(fams))
    print('prefix map     :', pmap)
    if unresolved:
        print('!! UNRESOLVED  :', unresolved, '-> those rows are SKIPPED')

    fixes, skips = {}, []
    for k, x in bad:
        m = re.match(r'^(.+?)[. ]Abjuration: (\w+)$', x)
        if not m:
            skips.append((k, x, 'unparsed'))
            continue
        fam, slot = m.group(1), m.group(2)
        if slot not in SLOT:
            skips.append((k, x, 'unknown slot'))
            continue
        pre = pmap.get(fam) or (fam + '.' if fam + '.Abjuration: ' + SLOT[slot] in names else None)
        if not pre:
            skips.append((k, x, 'no prefix'))
            continue
        new = pre + 'Abjuration: ' + SLOT[slot]
        if new not in names:                       # HARD GUARD: never invent a name
            skips.append((k, x, 'target %r not in DB' % new))
            continue
        fixes.setdefault(k, []).append((x, new))

    n = sum(len(v) for v in fixes.values())
    print('\nfixable %d entries across %d mobs; skipped %d' % (n, len(fixes), len(skips)))
    for k, pairs in sorted(fixes.items()):
        for a, b in pairs:
            print('   %-22s %-30s -> %s' % (k, a, b))
    for s in skips:
        print('   SKIP', s)

    if write and fixes:
        for k, pairs in fixes.items():
            parts = [s.strip() for s in mobs[k]['drops'].split(',') if s.strip()]
            for a, b in pairs:
                parts = [b if p == a else p for p in parts]
            mobs[k]['drops'] = ', '.join(parts)
        assert not [1 for mm in mobs.values() for v in mm.values() if v is None]
        with open(mp, 'w', encoding='utf-8') as f:
            json.dump(d, f, separators=(', ', ': '), ensure_ascii=False)
        print('\nwritten', mp)


if __name__ == '__main__':
    sweep(write=len(sys.argv) > 1 and sys.argv[1] == 'apply')
