# rev 377 — user: delete patriarch protector; the Sibilus are Peistes.
# BalladOfWorms
import json, collections, copy
A='/home/claude/android/app/src/main/assets'
d=json.load(open(f'{A}/mobs.json')); M=d['mobs']
TR={t['n'].lower() for t in json.load(open(f'{A}/trusts.json'))['trusts']}
def gk(v): return json.dumps([v.get('wk'),v.get('st')],ensure_ascii=False)

# ---- delete -------------------------------------------------------------------
DEL=['patriarch protector']
assert not [k for k in DEL if k in TR]
assert not [k for k in DEL if k not in M]
assert not [k for k in DEL if M[k].get('fam')],  'has a family — refusing'
assert not [k for k in DEL if M[k].get('zones')],'has a zone — refusing'
refs={k:[o for o,v in M.items() if o not in DEL and M[k]['n'] in ' '.join(v.get('notes') or [])] for k in DEL}
print('cross-references:', {k:v for k,v in refs.items() if v} or 'none')
for k in DEL: print('DELETING', M[k]['n']); del M[k]

# ---- fold quetzalcoatl's sibilus -> Peiste ------------------------------------
# family standards computed ONCE, before any write (rule 387)
mem=[v for v in M.values() if v.get('fam')=='Peiste']
c=collections.Counter(gk(v) for v in mem); top,n=c.most_common(1)[0]
WK,ST=json.loads(top); assert n>=max(2,len(mem)*0.3) and not (WK is None and ST is None)
KIT=collections.Counter(json.dumps(v['ab'],ensure_ascii=False) for v in mem if v.get('ab')).most_common(1)[0][0]
KIT=json.loads(KIT)
print(f'\nPeiste standard: {n}/{len(mem)} share the grid; kit x{len(KIT)}; crys Water; job Warrior')

k="quetzalcoatl's sibilus"; v=M[k]
v['fam']='Peiste'
print(f'  grid {gk(v)[:60]} -> family (its lone Ice +12.5 contradicts the family Ice -50)')
v['wk']=copy.deepcopy(WK); v['st']=copy.deepcopy(ST)
v['crys']='Water'; v['job']='Warrior'; v['ab']=copy.deepcopy(KIT)
v['zones']=[['Reisenjima','117']]
v['spawn']='Domain Invasion add of Quetzalcoatl'
v['notes']=['Eleven spawn during the preamble phase of the Domain Invasion event.',
            'These herald mobs must be defeated to make the boss dragon Quetzalcoatl appear.']
if M['quetzalcoatl'].get('content'): v['content']=copy.deepcopy(M['quetzalcoatl']['content'])
# det LEFT ALONE per rule 350 — the panel prints none, and ["Sight","True Sight"] is not the
# documented junk stamp, even though all 17 Peiste carry ["Sight"].
print(f'  det kept as {v["det"]} (family is 17/17 ["Sight"] — flagged, not overwritten)')

assert not [x for m in M.values() for x,y in m.items() if y is None]
bad=[a for a in v['ab'] if a not in d['abilities']]; assert not bad, bad
json.dump(d,open(f'{A}/mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print(f'\nmobs {len(M)}  orphans {sum(1 for x in M.values() if not x.get("fam"))}')
