# rev 373 — deterministic name folds (user: "lets do 1"). 28 folds, 5 rejected as false matches.
# BalladOfWorms
import json, collections, copy
P='/home/claude/android/app/src/main/assets/mobs.json'
d=json.load(open(P)); M=d['mobs']; AB=d['abilities']
def gk(v): return json.dumps([v.get('wk'),v.get('st')],ensure_ascii=False)
def mode_grid(f):
    c=collections.Counter(gk(v) for v in M.values() if v.get('fam')==f)
    wk,st=json.loads(c.most_common(1)[0][0]); return copy.deepcopy(wk),copy.deepcopy(st)
def mode_field(f,k):
    c=collections.Counter(json.dumps(v[k],ensure_ascii=False) for v in M.values() if v.get('fam')==f and v.get(k))
    return json.loads(c.most_common(1)[0][0]) if c else None
log=[]
def fold(key,fam,job=None,crys=None,kit=None,regrid=False,why=''):
    v=M[key]; v['fam']=fam
    bits=[f'fam={fam}']
    if regrid:
        wk,st=mode_grid(fam); v['wk']=wk; v['st']=st; bits.append('grid=family')
    if crys and not v.get('crys'): v['crys']=crys; bits.append(f'crys={crys}')
    if job and not v.get('job'):   v['job']=job;   bits.append(f'job={job}')
    if kit and not v.get('ab'):    v['ab']=kit;    bits.append(f'kit x{len(kit)}')
    log.append(f'  {key:26s} {", ".join(bits)}   [{why}]')

QUA=mode_field('Quadav','ab'); YAG=mode_field('Yagudo','ab'); TON=mode_field('Tonberry','ab')
GOB=mode_field('Goblin','ab'); PIX=mode_field('Pixie','ab');  CAR=mode_field('Cardian','ab')

# --- Garrison-shaped job sets: cohort is EXACTLY the unstamped set -> family grid
log.append('== metaquadav x7 -> Quadav  (grid cohort = the 7 unstamped records; family grid x154)')
for j in ['black mage','dark knight','paladin','red mage','thief','warrior','white mage']:
    fold(f'metaquadav {j}','Quadav',job=j.title().replace('Mage','Mage'),crys='Water',kit=QUA,
         regrid=True,why='name contains Quadav')
log.append('== theoyagudo x7 -> Yagudo  (same shape; family grid x138)')
for j in ['bard','black mage','monk','ninja','samurai','summoner','white mage']:
    fold(f'theoyagudo {j}','Yagudo',job=j.title(),crys='Wind',kit=YAG,regrid=True,why='name contains Yagudo')
log.append('== noctonberry x4 -> Tonberry  (same grid the four Cooks wore before r369 replaced it)')
for j in ['black mage','ninja','summoner','thief']:
    fold(f'noctonberry {j}','Tonberry',job=j.title(),crys='Light',kit=TON,regrid=True,why='rule 369')

# --- hobgoblins: grid KEPT, their three page-stamped siblings kept the same one
log.append('== hobgoblin x5 -> Goblin  (grid KEPT — stabnix skewerfinger is a healthy holder and the')
log.append('   three sibling pages read "Weak to: Light", which is what the stored grid says)')
for j in ['ranger','red mage','thief','warrior','white mage']:
    fold(f'hobgoblin {j}','Goblin',job=j.title(),crys='Fire',kit=GOB,why='name contains Goblin')

# --- the four fae: their grid was contradicted by TWO pages (fay + feeorin, r370)
log.append('== bucca / faerie / puca / titania -> Pixie  (their -62.5%-across-the-board grid is the one')
log.append('   fay and feeorin wore until their pages contradicted it — an import row, now replaced)')
for k in ['bucca','faerie','puca','titania']:
    fold(k,'Pixie',crys='Wind',kit=PIX,regrid=True,why='fae name + r370 grid evidence')

# --- cardian prototype: fold, but KEEP its distinctive grid
log.append('== cardian prototype -> Cardian  (grid KEPT — an all-elements -25% resist is not the')
log.append('   generic +12.5/+25 import shape, and nothing corroborates a replacement)')
fold('cardian prototype','Cardian',crys='Light',kit=CAR,why='name contains Cardian')

REJECTED = {
 'umarid':          'glued match inside "uMARIDs" — bare lv-75 Aht Urhgan NM, almost certainly Humanoid',
 'pixiebane':       'a pixie-BANE kills pixies, it is not one; lv [1,1] placeholder',
 'yrvaulair s cousseraux':'glued match inside "yrvauLAIR" — a person name, not a Lair',
 'savage hound condottiere':'one of the esquire/condottiere PvP-rank set, not a Hound',
 "eschan il'aern's spirit":'its siblings (euvhi, wynav) are filed by their own model family, not Aern; '
                           'its spell list is a Dark/Absorb caster — no Spirit family exists here',
}
assert not [k for m in M.values() for k,v in m.items() if v is None], 'null poison'
bad=[(k,a) for k,v in M.items() for a in (v.get('ab') or []) if a not in AB]
json.dump(d,open(P,'w'),separators=(', ', ': '),ensure_ascii=False)
print('\n'.join(log))
print('\nREJECTED as false substring matches (left as orphans, flagged in review):')
for k,w in REJECTED.items(): print(f'  {k:26s} {w}')
print(f'\nmobs {len(M)}  orphans {sum(1 for v in M.values() if not v.get("fam"))}  undefined {len(bad)}/{len(set(a for _,a in bad))}')
