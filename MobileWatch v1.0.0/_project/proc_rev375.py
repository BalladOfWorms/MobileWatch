# rev 375 — user: delete zodiac casters + herd animals; fold the OBVIOUS pets/adds.
# BalladOfWorms
import json, collections, copy
P='/home/claude/android/app/src/main/assets/mobs.json'
d=json.load(open(P)); M=d['mobs']; AB=d['abilities']
TR={t['n'].lower() for t in json.load(open('/home/claude/android/app/src/main/assets/trusts.json'))['trusts']}
def gk(v): return json.dumps([v.get('wk'),v.get('st')],ensure_ascii=False)
def mode_grid(f):
    # only return a grid if the family actually HAS a shared one: a real plurality,
    # and not the null/null shape. Botulus is 4 members with no agreement at all.
    mem=[v for v in M.values() if v.get('fam')==f]
    c=collections.Counter(gk(v) for v in mem)
    top,n=c.most_common(1)[0]
    wk,st=json.loads(top)
    if wk is None and st is None: return None,None
    if n < max(2, len(mem)*0.3): return None,None
    return copy.deepcopy(wk),copy.deepcopy(st)
def mode_field(f,k):
    c=collections.Counter(json.dumps(v[k],ensure_ascii=False) for v in M.values() if v.get('fam')==f and v.get(k))
    return json.loads(c.most_common(1)[0][0]) if c else None

# ---------------- deletes ------------------------------------------------------
ZODIAC=['aquarian caster','ariesian caster','capricornian caster','libran caster','piscean caster']
HERD=[f'{a} [herd{n}]' for a in ('bull','calf','cow') for n in (1,2,3)]
DELETE=ZODIAC+HERD
assert not [k for k in DELETE if k in TR], 'Trust-named record in delete list'
assert not [k for k in DELETE if k not in M], f'missing: {[k for k in DELETE if k not in M]}'
assert not [k for k in DELETE if M[k].get('fam')], 'a target already has a family'
refs={k:[o for o,v in M.items() if o not in DELETE and M[k]['n'] in ' '.join(v.get('notes') or [])] for k in DELETE}
refs={k:v for k,v in refs.items() if v}
print('cross-references from survivors:', refs if refs else 'none')
print(f'DELETING {len(DELETE)}: {len(ZODIAC)} zodiac casters + {len(HERD)} herd animals')
for k in DELETE: del M[k]

# ---------------- obvious pet/add folds ----------------------------------------
log=[]
def fold(key,fam,parent,crys=None,zones=None,regrid=True,det=None,content=None):
    v=M[key]; v['fam']=fam
    gridnote=''
    if regrid:
        wk,st=mode_grid(fam)
        if wk is None and st is None:
            gridnote='  [no family grid to stamp]'
        else:
            v['wk']=wk; v['st']=st; gridnote='  [+family grid]'
    kit=mode_field(fam,'ab')
    if kit and not v.get('ab'): v['ab']=kit
    if crys and not v.get('crys'): v['crys']=crys
    if det: v['det']=det
    if zones and not v.get('zones'): v['zones']=zones
    v['spawn']=f'Add of {parent}'
    if content: v['content']=content
    log.append(f'  {key:26s} -> {fam:9s} (add of {parent}){gridnote}')

# warder's hpedme — its four siblings are each filed by their own model family
fold("warder's hpedme",'Hpemde','the Warder of Temperance',crys='Varies',
     zones=[['Escha RuAun']],content=['Geas Fete: Escha RuAun: Nazar'])
M["warder's hpedme"]['spawn']='Geas Fete (Escha - Ru\u2019Aun)'
# zerde's adds — Zerde is Botulus, and drisheen/haupia/kacamak are all puddings
for k in ["zerde's drisheen","zerde's haupia","zerde's kacamak"]:
    fold(k,'Botulus','Zerde',zones=[['Reisenjima']])
# schah's adds — Schah is Caturae, and these are the five chaturanga pieces
for k in ["schah's ashva","schah's bhata","schah's gaja","schah's mantri","schah's ratha"]:
    fold(k,'Caturae','Schah',zones=[['Reisenjima','150']])
# neith's bobbin — Neith is a Diremite Voidwatch NM; Voidwatch adds match the parent
fold("neith's bobbin",'Diremite','Neith',crys='Wind',zones=[['Temple of Uggalepih']])
M["neith's bobbin"]['spawn']='Voidwatch add of Neith'

SKIPPED={
 "quetzalcoatl's sibilus":"parent is a Wyrm, but a Wyrm's Domain Invasion add is as likely a Wyvern or Zilant; 'sibilus' names no family",
 "commander's pet":"its five siblings are each filed by their OWN name (avatar/wyvern/gnat/kraken/hippogryph) — 'pet' names nothing",
 "volte's pet":"same shape; the Voltes are Fomor, but a Fomor's PET would not be a Fomor",
 "eschan il'aern's spirit":"no Spirit family exists here; its siblings are filed Euvhi and Wynav, not by the owner's Aern",
 "kutkha's get":"the owner `kutkha` is itself still an orphan",
 "assassin's apprentice":"no owner record; 'assassin' matches only assassin fly/leader/commander",
 "bhogbigg's grenade":"no owner record; a grenade is an object, not obviously a mob family",
 "bhogbigg's vial":"no owner record; same",
}
assert not [k for m in M.values() for k,v in m.items() if v is None]
bad=[(k,a) for k,v in M.items() for a in (v.get('ab') or []) if a not in AB]
assert not [x for x in bad if x[0] in log], 'undefined refs'
json.dump(d,open(P,'w'),separators=(', ', ': '),ensure_ascii=False)
print('\nFOLDED (obvious):'); print('\n'.join(log))
print('\nLEFT ALONE (not obvious):')
for k,w in SKIPPED.items(): print(f'  {k:26s} {w}')
print(f'\nmobs {len(M)}  orphans {sum(1 for v in M.values() if not v.get("fam"))}')
