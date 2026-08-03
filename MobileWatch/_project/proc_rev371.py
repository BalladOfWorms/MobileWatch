# rev 371 — ORPHAN BUCKET, alphabetical run G-H: 18 folds
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
def S(key,f,val,why):
    old=M[key].get(f); M[key][f]=val
    log.append(f'  {key}: {f} {json.dumps(old,ensure_ascii=False)[:34]} -> {json.dumps(val,ensure_ascii=False)[:60]}  [{why}]')
def FS(key,fam=None,grid=None,crys=None,job=None,det=None,kit=None):
    if fam and not M[key].get('fam'): S(key,'fam',fam,'FOLD')
    v=M[key]; f=v['fam']
    if grid=='family':
        wk,st=mode_grid(f); S(key,'wk',wk,'family grid'); S(key,'st',st,'family grid')
    if crys and not v.get('crys'): S(key,'crys',crys,'crystal')
    if job and not v.get('job'):   S(key,'job',job,'job')
    if det: S(key,'det',det,'detection')
    if kit is not None and not v.get('ab'): S(key,'ab',kit,'kit')

ORC=mode_field('Orc','ab'); ANT=mode_field('Antica','ab')
GOB=mode_field('Goblin','ab'); GB=mode_field('Greater Bird','ab')

# ---- the four Gullin hybrid elementals -> Elemental --------------------------
log.append('== the four Gullin elementals (AI panels) — grids KEPT (bergschrund gefyrst is a healthy holder)')
for k in ['gullin baelfyr','gullin gefyrst','gullin ungeweder','gullin byrgen']:
    FS(k, fam='Elemental')
    S(k,'zones',[['Monarch Linn']],'panel')
    S(k,'spawn','Battlefield (Nest of Nightmares)','panel')
    S(k,'notes',['One of four hybrid elementals that accompany Gullinkambi in the Nest of Nightmares battlefield, entered by spatial displacement from Monarch Linn.'],'panel')

# ---- gullinkambi -> Greater Bird ---------------------------------------------
log.append('== gullinkambi (AI panel) — "Roc-type battlefield boss"; `roc` itself is Greater Bird')
FS('gullinkambi', fam='Greater Bird', grid='family', crys='Light', kit=GB)
S('gullinkambi','ab',['Giga Scream','Blind Vortex','Dread Wind'],'panel names all three')
S('gullinkambi','nm',True,'panel: a battlefield boss with a party cap and a time limit')
S('gullinkambi','zones',[['Monarch Linn']],'panel')
S('gullinkambi','spawn','Battlefield (Nest of Nightmares)','panel')
S('gullinkambi','notes',['Boss of the Nest of Nightmares battlefield, entered by spatial displacement from Monarch Linn.',
  'Up to a six-person party, with a fifteen-minute limit.',
  'Accompanied by four hybrid elementals: Gullin Baelfyr, Gullin Gefyrst, Gullin Byrgen and Gullin Ungeweder.'],'panel')

# ---- habraheem + hkadouf -> Humanoid -----------------------------------------
log.append('== habraheem + hkadouf (BG pages) — the Red Versus Blue assault opponents')
for k in ['habraheem','hkadouf']:
    FS(k, fam='Humanoid', job='Blue Mage', det=['True Sound'])
    S(k,'zones',[['Leujaoam Sanctum','75']],'page')
    S(k,'spawn','Assault (Red Versus Blue)','page')
    S(k,'notes',['One of your opponents during the Red Versus Blue assault.'],'page')

# ---- the seven Halforcs -> Orc (Expeditionary Force, NOT NMs) ----------------
log.append('== the seven Halforcs (BG pages) — grid KEPT, page "Weak to: Water" matches')
for k,job,two in [('halforc black mage','Black Mage','Manafont'),
                  ('halforc dark knight','Dark Knight','Blood Weapon'),
                  ('halforc dragoon','Dragoon',None),
                  ('halforc monk','Monk','Hundred Fists'),
                  ('halforc paladin','Paladin','Invincible'),
                  ('halforc ranger','Ranger','Eagle Eye Shot'),
                  ('halforc warrior','Warrior','Mighty Strikes')]:
    FS(k, fam='Orc', crys='Fire', job=job, kit=ORC)
    if two: S(k,'ab',ORC+[two],f'page: uses {two} at some point')
    S(k,'lv',[30,35],'page level column: 30 in Valkurm Dunes, 35 in Jugner Forest')
    S(k,'zones',[['Valkurm Dunes','30'],['Jugner Forest','35']],'page')
    S(k,'spawn',"Expeditionary Force (Beastman's Banner)",'page')
    S(k,'notes',["Sometimes spawned from a Beastman's Banner during Expeditionary Force.",
        'Calls a pet wyvern, which follows and assists it in combat.' if job=='Dragoon'
        else f'Uses {two} at some point.'],'page')

# ---- the four Hastatus -> Antica ---------------------------------------------
log.append('== the four Hastatus (BG pages) — grid KEPT, 4 healthy Contantican holders')
for k in ['hastatus xiii-cxxviii','hastatus xiii-lxxv','hastatus xiii-xcvi','hastatus xiii-xxv']:
    FS(k, fam='Antica', crys='Dark', job='Warrior', kit=ANT)
    S(k,'zones',[['Eastern Altepa Desert']],'page')
    S(k,'spawn','Garrison (Eastern Altepa Desert)','page')
S('hastatus xiii-lxxv','notes',['Drops no gil and cannot be mugged.'],'page')

# ---- the three Hobgoblins with pages -> Goblin -------------------------------
log.append('== hobgoblin beastmaster / black mage / dark knight (BG pages) — EF, NOT NMs')
HZ=[['Buburimu Peninsula','30'],['Valkurm Dunes','30'],['Jugner Forest','35'],
    ['Meriphataud Mountains','35'],['Pashhow Marshlands','35'],['Qufim Island','35'],
    ['Beaucedine Glacier','45'],['The Sanctuary of ZiTah','45'],['Yuhtunga Jungle','45'],
    ['Eastern Altepa Desert','50'],['Xarcabard','50'],['Yhoator Jungle','55'],['Cape Teriggan','75']]
for k,job,crys,note in [
    ('hobgoblin beastmaster','Beastmaster','Fire','Calls a pet; if the pet is killed it may try to charm a player instead. The pet it summons varies by zone — Rabbit, Dragonfly, Beetle, Bee, Leech, Tiger or Spider.'),
    ('hobgoblin black mage','Black Mage','Fire','Uses Manafont at some point.'),
    ('hobgoblin dark knight','Dark Knight','Lightning','Uses Blood Weapon at some point.')]:
    FS(k, fam='Goblin', crys=crys, job=job, kit=GOB)
    if job=='Black Mage': S(k,'ab',GOB+['Manafont'],'page')
    if job=='Dark Knight': S(k,'ab',GOB+['Blood Weapon'],'page')
    S(k,'lv',[30,75],'page level column spans 30-75 across its thirteen zones')
    S(k,'zones',[list(z) for z in HZ],'page')
    S(k,'spawn',"Expeditionary Force (Beastman's Banner)",'page')
    S(k,'notes',["Sometimes spawned from a Beastman's Banner during Expeditionary Force.",note],'page')

assert not [k for m in M.values() for k,v in m.items() if v is None], 'null poison'
T=['gullin baelfyr','gullin gefyrst','gullin ungeweder','gullin byrgen','gullinkambi','habraheem',
   'hkadouf','halforc black mage','halforc dark knight','halforc dragoon','halforc monk',
   'halforc paladin','halforc ranger','halforc warrior','hastatus xiii-cxxviii','hastatus xiii-lxxv',
   'hastatus xiii-xcvi','hastatus xiii-xxv','hobgoblin beastmaster','hobgoblin black mage','hobgoblin dark knight']
bad=[(k,a) for k,v in M.items() for a in (v.get('ab') or []) if a not in AB]
assert not [x for x in bad if x[0] in T], f'undefined refs: {[x for x in bad if x[0] in T]}'
json.dump(d,open(P,'w'),separators=(', ', ': '),ensure_ascii=False)
print('\n'.join(log[:6]))
print(f'\nmobs {len(M)}  orphans {sum(1 for v in M.values() if not v.get("fam"))}  NM {sum(1 for v in M.values() if v.get("nm"))}  undefined {len(bad)}/{len(set(a for _,a in bad))}')
