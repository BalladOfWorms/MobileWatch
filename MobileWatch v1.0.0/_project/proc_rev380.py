# rev 380 — remove "Gaze Attack", a prose fragment glued into mokumokuren's kit.
# BalladOfWorms
import json, collections
A='/home/claude/android/app/src/main/assets'
d=json.load(open(f'{A}/mobs.json')); M=d['mobs']; AB=d['abilities']
k='mokumokuren'
fam=M[k]['fam']
kit=collections.Counter(json.dumps(v['ab'],ensure_ascii=False) for v in M.values()
                        if v.get('fam')==fam and v.get('ab')).most_common(1)[0]
print(f'{fam} family kit, {kit[1]} of its members: {kit[0]}')
print('before:', M[k]['ab'])
M[k]['ab']=[a for a in M[k]['ab'] if a!='Gaze Attack']
print('after :', M[k]['ab'], '  == family kit:', json.dumps(M[k]['ab'],ensure_ascii=False)==kit[0])
print('"Gaze Attack" is not in jobs.json, weaponskills.json or the abilities dict, and the family')
print('already carries the real gazes (Hex Eye, Petrogaze) — it was descriptive prose, not a move.')
assert not [x for m in M.values() for x,y in m.items() if y is None]
json.dump(d,open(f'{A}/mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
undef=sorted({a for v in M.values() for a in (v.get('ab') or []) if a not in AB})
print(f'\nundefined ability references: {len(undef)} — {undef}')
