# rev 372 — gullin baelfyr: fire elemental grid (user ruling)
# BalladOfWorms
import json
P='/home/claude/android/app/src/main/assets/mobs.json'
d=json.load(open(P)); M=d['mobs']
# `nocuous inferno` is the exact template: a FIRE elemental at the Gullin battlefield
# scale (-75% physical, +/-25% elemental) and using the same "Impact" label.
donor = M['nocuous inferno']
print('donor  nocuous inferno :', json.dumps([donor['wk'], donor['st']], ensure_ascii=False))
print('before gullin baelfyr  :', json.dumps([M['gullin baelfyr']['wk'], M['gullin baelfyr']['st']], ensure_ascii=False))
M['gullin baelfyr']['wk'] = json.loads(json.dumps(donor['wk']))
M['gullin baelfyr']['st'] = json.loads(json.dumps(donor['st']))
print('after  gullin baelfyr  :', json.dumps([M['gullin baelfyr']['wk'], M['gullin baelfyr']['st']], ensure_ascii=False))
assert not [k for m in M.values() for k, v in m.items() if v is None]
json.dump(d, open(P,'w'), separators=(', ', ': '), ensure_ascii=False)

# sanity: the four Gullin elementals, side by side
print()
for k in ['gullin baelfyr','gullin gefyrst','gullin byrgen','gullin ungeweder']:
    v=M[k]; wk=[e[0] for e in v['wk']]; st=[e[0] for e in v['st'] if e[0] not in ('Slashing','Piercing','H2H','Impact','Ranged','Blunt')]
    print(f'  {k:20s} weak {str(wk):22s} resists {st}')
