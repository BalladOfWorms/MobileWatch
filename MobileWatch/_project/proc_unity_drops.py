#!/usr/bin/env python3
"""Unity NM drops backfill (rev 248).

15 of the 56 Unity Wanted NMs had an EMPTY `drops` string. The BG reward tables name, for each NM,
its x50 UCNM material and every piece that material upgrades — so the gap closes straight from the
same screenshots that built the Unity rewards page. Every name is validated against ffxi_items.json
(rule: fuzzy-verify, never write a name the DB doesn't have) and only the NQ/+1 gear plus the
material go in. Records that already had drops are left alone.
"""
import json, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']

items = json.load(open(P.replace('mobs.json', 'ffxi_items.json'), encoding='utf-8'))
src = items.get('items') if isinstance(items, dict) and 'items' in items else (
    items.values() if isinstance(items, dict) else items)
NAMES = {v['n'] for v in src if isinstance(v, dict) and 'n' in v}

# key -> the item names published on the Unity reward tables for that NM
DROPS = {
    'azrael':                 ["Azrael's Eye", 'Aizkora', 'Aizkora +1', 'Alhazen Hat', 'Alhazen Hat +1'],
    'azure-toothed clawberry': ["Clawberry's Coat", 'Asteria Mitts', 'Asteria Mitts +1',
                                'Lamassu Mitts', 'Lamassu Mitts +1'],
    'borealis shadow':        ['Ethereal Incense', 'Beheader', 'Beheader +1', 'Fists of Fury',
                               'Fists of Fury +1', 'Paloma Bow', 'Paloma Bow +1', 'Deliverance',
                               'Deliverance +1'],
    'camahueto':              ["Camahueto's Fur", 'Triska Scythe', 'Triska Scythe +1',
                               'Hygieia Clogs', 'Hygieia Clogs +1'],
    'coca':                   ["Coca's Wing", 'Gae Derg', 'Gae Derg +1', 'Ajax', 'Ajax +1'],
    'grand grenade':          ["G. Grenade's Ash", 'Loxotic Mace', 'Loxotic Mace +1',
                               'Seething Bomblet', 'Seeth. Bomblet +1'],
    'hidhaegg':               ["Hidhaegg's Scale", 'Combuster', 'Combuster +1', 'Nullis', 'Nullis +1',
                               'Loess Barbuta', 'Loess Barbuta +1'],
    'king uropygid':          ["Uropygid's Needle", 'Stinger Helm', 'Stinger Helm +1'],
    "kubool ja's mhuufya":    ["Mhuufya's Beak", 'Mdomo Axe', 'Mdomo Axe +1', 'Zwazo Earring',
                               'Zwazo Earring +1'],
    'orcfeltrap':             ["Orcfeltrap's Leaf", 'Tancho', 'Tancho +1', 'Shinjutsu-no-Obi',
                               'Shinjutsu-no-Obi +1'],
    'sleepy mabel':           ["Sleepy Mabel's Fur", 'Damani Horn', 'Damani Horn +1'],
    'specter worm':           ["Specter's Ore", 'Kladenets', 'Kladenets +1', 'Ghastly Tathlum',
                               'Ghastly Tathlum +1'],
    'tumult curator':         ["Tumult's Blood", 'Comeuppances', 'Comeuppances +1', 'Contemplator',
                               'Contemplator +1', 'Tatena. Haramaki', 'Tatena. Harama. +1'],
    'volatile cluster':       ["V. Cluster's Ash", 'Norifusa', 'Norifusa +1', "Aurist's Cape",
                               "Aurist's Cape +1"],
    'wyvernhunter bambrox':   ["Bambrox's Shawl", 'Pixquizpan', 'Pixquizpan +1', 'Imati', 'Imati +1'],
}

filled, skipped, dropped = [], [], []
for k, names in DROPS.items():
    m = M.get(k)
    if m is None:
        skipped.append('%s (no record)' % k)
        continue
    if m.get('drops'):
        skipped.append('%s (already had drops)' % k)
        continue
    good = [n for n in names if n in NAMES]
    bad = [n for n in names if n not in NAMES]
    dropped += ['%s: %s' % (k, n) for n in bad]
    if not good:
        skipped.append('%s (nothing validated)' % k)
        continue
    m['drops'] = ', '.join(good)
    filled.append('%s -> %s' % (k, m['drops']))

assert not [kk for mm in M.values() for kk, v in mm.items() if v is None]
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

print('filled %d' % len(filled))
for r in filled:
    print('  ', r)
print('skipped:', skipped or '(none)')
print('names the item DB does not have (left out):', dropped or '(none)')
