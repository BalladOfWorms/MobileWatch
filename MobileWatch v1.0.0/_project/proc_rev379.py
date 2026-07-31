# rev 379 — 13 misspelled ability keys renamed to the real game names; Gush o' Goo defined.
# Spellings from the WarnMe res merge map (Windower's own resources win).
# BalladOfWorms
import json, collections
A='/home/claude/android/app/src/main/assets'
d=json.load(open(f'{A}/mobs.json')); M=d['mobs']; AB=d['abilities']

MAP={'Homing Missle':'Homing Missile', "Gerjis's Grip":"Gerjis' Grip",
     'Gleosuccus':'Gloeosuccus',       'Hydro Canon':'Hydro Cannon',
     'Aura of Persistance':'Aura of Persistence', 'Torrential Torrent':'Torrential Torment',
     'Disorienting Wail':'Disorienting Waul',     'Fortifying Wall':'Fortifying Wail',
     'Nepanthean Hum':'Nepenthean Hum', 'Flourescence':'Fluorescence',
     'Ochre Blast':'Ocher Blast',       'Petrification':'Petrifaction',
     'III Wind':'Ill Wind'}

# guards: every bad key must exist, and no good key may already be taken
assert not [b for b in MAP if b not in AB], [b for b in MAP if b not in AB]
assert not [g for g in MAP.values() if g in AB], 'a target name already exists — would clobber'
assert len(set(MAP.values()))==len(MAP), 'duplicate target names'

# 1. rename the definition keys, preserving insertion order
newAB={}
for k,v in AB.items(): newAB[MAP.get(k,k)]=v
d['abilities']=newAB; AB=newAB

# 2. repoint every mob `ab` reference
refs=collections.Counter()
for k,v in M.items():
    if v.get('ab'):
        out=[MAP.get(a,a) for a in v['ab']]
        for a in v['ab']:
            if a in MAP: refs[a]+=1
        v['ab']=out

# 3. fix prose mentions in ability notes/descriptions and family_notes
prose=collections.Counter()
for name,ab in AB.items():
    for f in ('d','notes'):
        if isinstance(ab.get(f),str):
            for b,g in MAP.items():
                if b in ab[f]: ab[f]=ab[f].replace(b,g); prose[b]+=1
for fam,bul in d.get('family_notes',{}).items():
    if isinstance(bul,list):
        for i,line in enumerate(bul):
            if isinstance(line,str):
                for b,g in MAP.items():
                    if b in line: bul[i]=line=line.replace(b,g); prose[b]+=1

print('renamed 13 keys; mob references repointed:')
for b,g in MAP.items(): print(f'   {b:22s} -> {g:22s} {refs[b]:3d} refs')
print(f'   total {sum(refs.values())} references, {sum(prose.values())} prose mentions')

# 4. Gush o' Goo — the one genuine bestiary gap, from the user's panel
assert "Gush o' Goo" not in AB
AB["Gush o' Goo"]={
 "d":"Deals magic damage in an area around the monster and inflicts Encumbrance, which unequips all "
     "gear and blocks equipment changes.",
 "t":"Magical", "tgt":"AoE", "fx":["Encumbrance"],
 "notes":"Encumbrance lasts roughly 60 seconds. A Flan-type move; often paired with the Xenoglossia "
         "trait, which grants the monster an instant cast on its next spell."}
ngoo=sum(1 for v in M.values() if "Gush o' Goo" in (v.get('ab') or []))
print("\ndefined Gush o' Goo -", ngoo, "mobs reference it")

# 5. what is left undefined, and why it is not a bestiary gap
J=json.load(open(f'{A}/jobs.json'))
ja={x[k] for lst in J['abilities'].values() for x in lst if isinstance(x,dict)
    for k in ('n','name') if isinstance(x.get(k),str)}
si=set(J['spellinfo'])
ws=set()
def walk(o):
    if isinstance(o,dict):
        if isinstance(o.get('n'),str): ws.add(o['n'])
        for v in o.values(): walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(json.load(open(f'{A}/weaponskills.json')))
undef=sorted({a for v in M.values() for a in (v.get('ab') or []) if a not in AB})
print('\nstill undefined, with where each one really lives:')
for a in undef:
    where=('Rune Fencer job ability (jobs.json)' if a in ja else
           f'Blue Magic (jobs.json spellinfo: {J["spellinfo"][a]["type"]})' if a in si else
           'Sword weapon skill (weaponskills.json)' if a in ws else
           '!! NOT IN ANY TABLE — a real loose end')
    who=[k for k,v in M.items() if a in (v.get('ab') or [])]
    print(f'   {a:17s} {len(who):2d} mob(s)  {where}')

assert not [k for m in M.values() for k,v in m.items() if v is None]
assert not [k for k,v in AB.items() if v is None]
json.dump(d,open(f'{A}/mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print(f'\nabilities {len(AB)}  mobs {len(M)}  undefined {len(undef)}')
