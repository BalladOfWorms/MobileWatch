# rev 376 — user delete list: general*, volunteer*, wildcat*, scylla brigade,
#           combat salvemixer, silver fox archer.  Two records EXCLUDED as real mobs.
# BalladOfWorms
import json
A='/home/claude/android/app/src/main/assets'
d=json.load(open(f'{A}/mobs.json')); M=d['mobs']
TR={t['n'].lower() for t in json.load(open(f'{A}/trusts.json'))['trusts']}

DELETE=[
 # the five Serpent General records — the user said four; all five are the same shape
 'general gadalar','general mihli','general najelith','general rughadjeen','general zazarg',
 'cougar volunteer','volunteer','wildcat volunteer','wildcat vanguard',
 'scylla brigade elite','scylla brigade healer','scylla brigade officer',
 'combat salvemixer','silver fox archer',
]
EXCLUDED={
 'fallen volunteer':'matches "volunteer" but is a REAL mob — fam Fomor, lv 72-78, zoned to Arrapago Reef',
 'scylla':'matches "scylla" but is a REAL NM — fam Ruszor, lv 85, Beaucedine Glacier [S], NM-flagged',
}
# guards
assert not [k for k in DELETE if k in TR], 'Trust-named record in the delete list'
assert not [k for k in DELETE if k not in M], f'missing: {[k for k in DELETE if k not in M]}'
kept=[k for k in DELETE if M[k].get('fam')]
assert not kept, f'REFUSING — these have a family: {kept}'
zoned=[k for k in DELETE if M[k].get('zones')]
assert not zoned, f'REFUSING — these have a zone: {zoned}'
refs={}
for k in DELETE:
    hits=[o for o,v in M.items() if o not in DELETE and M[k]['n'] in ' '.join(v.get('notes') or [])]
    if hits: refs[k]=hits
print('cross-references from survivors:', refs if refs else 'none')
print('\nEXCLUDED from the pattern (left in the file):')
for k,w in EXCLUDED.items(): print(f'   {M[k]["n"]:20s} {w}')
print(f'\nDELETING {len(DELETE)}:')
for k in DELETE: print(f'   {M[k]["n"]}')
for k in DELETE: del M[k]
assert not [k for m in M.values() for k,v in m.items() if v is None]
json.dump(d,open(f'{A}/mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print(f'\nmobs {len(M)}  orphans {sum(1 for v in M.values() if not v.get("fam"))}')
