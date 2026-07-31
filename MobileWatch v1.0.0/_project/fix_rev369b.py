import json, collections
P='/home/claude/android/app/src/main/assets/mobs.json'
d=json.load(open(P)); M=d['mobs']; AB=d['abilities']

# (1) curilla — I overwrote a richer stored sp with the page's four. Merge instead:
#     keep Holy + Banish II from the import, take the page's Shell II over Shell III.
M['curilla']['sp']=['Cure IV','Holy','Banish II','Protect III','Shell II','Flash']
print('curilla sp ->', M['curilla']['sp'])

# (2) amnaf — Tail Slap and Hysteric Barrage are TP moves filed under `sp`. Move to `ab`.
M['amnaf']['ab']=['Tail Slap','Hysteric Barrage']
del M['amnaf']['sp']
print('amnaf ab ->', M['amnaf']['ab'], '| sp removed')

# survey: how much of the sp/ab overlap is real vs the 'Burst' name collision?
c=collections.Counter()
for k,v in M.items():
    for x in (v.get('sp') or []):
        if x in AB: c[x]+=1
print('sp entries that are also ability names:', c.most_common(12))

assert not [k for m in M.values() for k,v in m.items() if v is None]
bad=[(k,a) for k,v in M.items() for a in (v.get('ab') or []) if a not in AB]
assert not [x for x in bad if x[0] in ('curilla','amnaf')], bad
json.dump(d,open(P,'w'),separators=(', ', ': '),ensure_ascii=False)
print('undefined', len(bad), len(set(a for _,a in bad)))
