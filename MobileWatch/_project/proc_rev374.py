# rev 374 — delete the 24 NPC/structure records (user ruling). Trust-named records untouched.
# BalladOfWorms
import json
P='/home/claude/android/app/src/main/assets/mobs.json'
d=json.load(open(P)); M=d['mobs']
TRUSTS={t['n'].lower() for t in json.load(open('/home/claude/android/app/src/main/assets/trusts.json'))['trusts']}

STRUCTURES=['allied belfry','allied mantelet','bastion gate','binding tube','city gate',
            'dilapidated gate','paralyzing tube','royal banneret','silencing tube']
UNITS=['bastion fighter','bastion mage','cobra mercenary','confederate +d568','crocodile mercenary',
       'field musician guard','immortal guard','imperial trooper','python mercenary']
RANKS=['crimson wolf esquire','gold badger esquire','red rose condottiere','royal esquire',
       'savage hound condottiere','scarlet boar esquire']
DELETE=STRUCTURES+UNITS+RANKS

# guard 1: never delete a Trust-named record (the user's explicit carve-out)
clash=[k for k in DELETE if k in TRUSTS]
assert not clash, f'REFUSING — Trust-named records in the delete list: {clash}'
# guard 2: every target must exist and still be an orphan
missing=[k for k in DELETE if k not in M]
assert not missing, f'not in file: {missing}'
familied=[k for k in DELETE if M[k].get('fam')]
assert not familied, f'REFUSING — these have a family: {familied}'
# guard 3: is any of them referenced by a surviving record?
refs={}
for k in DELETE:
    n=M[k]['n']
    hits=[o for o,v in M.items() if o not in DELETE and
          (n in ' '.join(v.get('notes') or []) or n == (v.get('spawn') or ''))]
    if hits: refs[k]=hits
print('cross-references from surviving records:', refs if refs else 'none')

print(f'\nDELETING {len(DELETE)} records:')
for grp,ks in [('structures',STRUCTURES),('allied/imperial units',UNITS),('PvP ranks',RANKS)]:
    print(f'  {grp} ({len(ks)}):')
    for k in ks: print(f'      {M[k]["n"]}')
    for k in ks: del M[k]

assert not [k for m in M.values() for k,v in m.items() if v is None]
json.dump(d,open(P,'w'),separators=(', ', ': '),ensure_ascii=False)
print(f'\nmobs {len(M)}  orphans {sum(1 for v in M.values() if not v.get("fam"))}')
