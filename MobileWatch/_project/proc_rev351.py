#!/usr/bin/env python3
"""rev 351 — user ruling: harpimaira is Walk of Echoes.
Author: BalladOfWorms
"""
import json, os

P = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
MOBS = os.path.join(P, 'mobs.json')
d = json.load(open(MOBS, encoding='utf-8'))
m = d['mobs']
ZONES = {z['name'] for z in json.load(open(os.path.join(P, 'zones.json'), encoding='utf-8'))['zones']}
assert 'Walk of Echoes' in ZONES

r = m['harpimaira']
assert not r.get('zones'), r.get('zones')
r['zones'] = [['Walk of Echoes', '90-92']]

# rev 350 parked the entry point in a note because the zone could not be resolved; it is
# still the useful detail, so it stays — reworded now that the zone carries the location.
old = 'Listed on Veridical Conflux 4. Drops and steal are both None.'
ns = r['notes']
ns[ns.index(old)] = 'Entered from Veridical Conflux 4. Drops and steal are both None.'

json.dump(d, open(MOBS, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('harpimaira ->', json.dumps({k: r[k] for k in ('fam', 'lv', 'zones', 'notes')}, ensure_ascii=False))
print('orphans', sum(1 for v in m.values() if not v.get('fam')))
