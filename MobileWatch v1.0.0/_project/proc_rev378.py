# rev 378 — one correction on top of rev 377: the Sibilus det.
# BalladOfWorms
import json, collections
A='/home/claude/android/app/src/main/assets'
d=json.load(open(f'{A}/mobs.json')); M=d['mobs']
k="quetzalcoatl's sibilus"
fam=[v for v in M.values() if v.get('fam')=='Peiste']
print('Peiste det spread:', collections.Counter(json.dumps(v.get('det')) for v in fam).most_common())
# rev 377 kept ["Sight","True Sight"] citing rule 350. But rule 350 covers a value that is NOT a
# known bad stamp — and this exact shape WAS cleaned at rev 368 on `duke vepar's gnat`, whose Gnat
# family was 19/20 ["Sight"]. Peiste is 17/18. Same shape, same evidence, so same treatment.
print(f'\nbefore: {M[k]["det"]}')
M[k]['det']=['Sight']
print(f'after : {M[k]["det"]}   [rev-368 `duke vepar\'s gnat` precedent]')
assert not [x for m in M.values() for x,y in m.items() if y is None]
json.dump(d,open(f'{A}/mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print(f'\nmobs {len(M)}  orphans {sum(1 for v in M.values() if not v.get("fam"))}')
