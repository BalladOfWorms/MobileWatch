# rev 370 — ORPHAN BUCKET, alphabetical run D-G: 17 folds + 1 enrichment
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
    log.append(f'  {key}: {f} {json.dumps(old,ensure_ascii=False)[:38]} -> {json.dumps(val,ensure_ascii=False)[:64]}  [{why}]')
def RM(key,f,why):
    if f in M[key]: log.append(f'  {key}: REMOVED {f} ({json.dumps(M[key].pop(f),ensure_ascii=False)[:44]})  [{why}]')
def FS(key,fam=None,grid=None,crys=None,job=None,det=None,kit=None):
    if fam: S(key,'fam',fam,'FOLD')
    v=M[key]; f=v['fam']
    if grid=='family':
        wk,st=mode_grid(f); S(key,'wk',wk,'family grid'); S(key,'st',st,'family grid')
    if crys and not v.get('crys'): S(key,'crys',crys,'crystal')
    if job and not v.get('job'):   S(key,'job',job,'job')
    if det: S(key,'det',det,'detection')
    if kit is not None and not v.get('ab'): S(key,'ab',kit,'kit')

# ---- dweomershell -> Crab (page grid corroborated: "Weak to: Ice, Lightning") --
log.append('== dweomershell (BG page)')
FS('dweomershell', fam='Crab', crys='Water', job='Paladin', kit=mode_field('Crab','ab'))
S('dweomershell','zones',[['Arrapago Reef','88-89']],'page')
S('dweomershell','notes',['Nineteen spawn around (I-8) on Map 3, on a 16-minute respawn.'],'page')

# ---- eraser -> Doll (Fields of Valor NM) --------------------------------------
log.append('== eraser (BG page — "Fields of Valor Notorious Monster")')
FS('eraser', fam='Doll', grid='family', crys='Ice', kit=mode_field('Doll','ab'))
S('eraser','det',['Sight','Magic'],'page notes column: A, S, M')
S('eraser','nm',True,'banner reads "Fields of Valor Notorious Monster"')
S('eraser','zones',[['RuAun Gardens']],'page')
S('eraser','spawn','Fields of Valor (Chapter 7 Elite Training)','page')
S('eraser','notes',['Spawned at the north-west corner of (H-9) in RuAun Gardens with Chapter 7 Elite Training. Roughly 4,600 HP.',
  'About as strong as a Groundskeeper, with double the accuracy.',
  'Its job changes on each pop or each day. Seen as Thief (near-100% Triple Attack), Dark Knight, White Mage, Monk (2-4 attacks a round) and Bard; every job seems to have Double Attack.',
  'May additionally spawn with damage spikes, En- spells, Aspir or TP drain on melee hits, high Auto-Regen, up to nine shadow images, or the ability to absorb the current day\u2019s element.',
  'Depops, uncharms or dismisses pets when summoned, but does not dismiss wyverns. It will not aggro to reraise or to magic casting.',
  'Death to it costs no items, and no XP while under battle conditions.'],'page')

# ---- fantoccini monster + fantoccini -> Humanoid ------------------------------
log.append('== fantoccini monster + fantoccini (BG page + the ENM Enemies table)')
FS('fantoccini monster', fam='Humanoid')
RM('fantoccini monster','wk','a Rabbit import default — its 3 other holders are all Rabbits, and the page\u2019s Weak line is blank')
S('fantoccini monster','nm',True,'banner reads "Empty Notorious Monster"')
S('fantoccini monster','zones',[['Mine Shaft 2716','49']],'page')
S('fantoccini monster','spawn','ENM (Pulling the Strings)','page')
S('fantoccini monster','notes',['Fought in the ENM Pulling the Strings, alongside the Moblin Fantocciniman.',
  'Matches its job to your main job, and attacks and casts accordingly. A Blue Mage Fantoccini always has Frypan and is otherwise restricted to the Blue Magic you have equipped.',
  'Only uses weapon skills and job abilities — two-hours included — when the Moblin Fantocciniman rolls the right number.',
  'Defeating it spawns a chest worth 2,000 experience or limit points plus a chance at gear matching your main job.'],'ENM page')
FS('fantoccini', fam='Humanoid')
S('fantoccini','zones',[['Mine Shaft 2716','55']],'ENM Enemies table')
S('fantoccini','notes',['Listed as Humanoid in the Pulling the Strings ENM enemy table.'],'ENM page')

# ---- fay + feeorin -> Pixie (page grid OVERRIDES both the stored and the family)
log.append('== fay + feeorin (BG pages) — page names directions without magnitudes')
for k in ['fay','feeorin']:
    FS(k, fam='Pixie', crys='Wind', job='White Mage')
    S(k,'wk',[['Fire',None],['Light',None],['Slashing',None]],'page: Weak to Fire, Light, Slashing')
    S(k,'st',[['Wind',None]],'page: Strong to Wind')
    S(k,'nm',True,'page red banner')
    S(k,'zones',[['North Gustaberg [S]','60']],'page')
    S(k,'spawn','Quest (Succor to the Sidhe)','page')
S('fay','notes',['Six spawn alongside Feeorin.','Casts nothing at all — melees for roughly 49-70 a hit, quickly.',
  'Resistant or immune to Repose and Lullaby.'],'page')
S('feeorin','sp',['Banishga III','Diaga II','Death'],'page')
S('feeorin','notes',['Spawned by examining the "Shredded Label" at (G-7) in North Gustaberg [S] with the Blue-Labeled Crate key item. A level 60 cap applies.',
  'Assisted by six Fay.','Immune to sleep, Elemental Magic and Stun. Erase helps against its Bind and Slow.',
  'Casts Death — through shadows, quickly, at any HP, and more than once per fight. Shield Bash stops it; Super Jump also works. Unlocking Death may be triggered by killing a particular Fay.',
  'Also has an area-of-effect Silence move. Rarely melees, mostly spamming -na spells, buffs and debuffs.'],'page')

# ---- gelatinous clot -> Slime (grid matches the panel, KEPT) ------------------
log.append('== gelatinous clot (AI panel) — "Clots are a red subspecies of the slime family"')
FS('gelatinous clot', fam='Slime', crys='Water', job='Warrior', kit=mode_field('Slime','ab'))
S('gelatinous clot','zones',[['Moh Gates','120-124']],'panel')
S('gelatinous clot','notes',['Found in the subterranean tunnels of Moh Gates.',
  'Very resistant to physical weapon damage and vulnerable to magic, fire above all.'],'panel')

# ---- ghayaraan + gowam -> Humanoid -------------------------------------------
log.append('== ghayaraan + gowam (BG pages)')
FS('ghayaraan', fam='Humanoid', job='Blue Mage', det=['True Sound'])
S('ghayaraan','zones',[['Leujaoam Sanctum','75']],'page')
S('ghayaraan','spawn','Assault (Red Versus Blue)','page')
S('ghayaraan','notes',['One of your opponents during the Red Versus Blue assault.'],'page')
FS('gowam', fam='Humanoid', job='Blue Mage')
S('gowam','nm',True,'page red banner')
S('gowam','zones',[['The Ashu Talif','75']],'page')
S('gowam','spawn','Quest (Against All Odds)','page')
S('gowam','notes',['Roughly 5,800 HP.','Spawned for the quest Against All Odds, alongside Yazquhl.'],'page')

# ---- the four Expeditionary Force Giants -> Gigas -----------------------------
log.append('== giant beastmaster / high ranger / monk / warrior (BG pages) — EF, NOT NMs')
GIG=mode_field('Gigas','ab')
for k,job,note in [('giant beastmaster','Beastmaster','Calls a pet; if the pet is killed it may try to charm a player instead. Summons a Gigas\u2019s Leech.'),
                   ('giant high ranger','Ranger','Uses Eagle Eye Shot at some point.'),
                   ('giant monk','Monk','Uses Hundred Fists at some point.'),
                   ('giant warrior','Warrior','Uses Mighty Strikes at some point.')]:
    FS(k, fam='Gigas', crys='Ice', job=job, kit=GIG)
    if not M[k].get('lv'): S(k,'lv',[35,35],'page level column')
    S(k,'zones',[['Qufim Island','35']],'page')
    S(k,'spawn',"Expeditionary Force (Beastman's Banner)",'page')
    S(k,'notes',["Sometimes spawned from a Beastman's Banner during Expeditionary Force.",note],'page')

# ---- glacial wisp -> Snoll (family grid IS the page) --------------------------
log.append('== glacial wisp (BG page) — the Snoll family grid matches the page exactly')
FS('glacial wisp', fam='Snoll', grid='family', crys='Ice', job='Warrior', kit=mode_field('Snoll','ab'))
S('glacial wisp','nm',True,'page red banner')
S('glacial wisp','zones',[['Vunkerl Inlet [S]','75']],'page')
S('glacial wisp','spawn','Quest (Succor to the Sidhe)','page')
S('glacial wisp','notes',['Four spawn when the quest is started — two tied to Almops and two to Edonus.',
  'If one of those Gigas is dead, its two Glacial Wisps will not repop once defeated. Otherwise they respawn when killed.',
  'They use Mighty Strikes whenever their corresponding Gigas does.'],'page')

# ---- gnashfang rahskhas -> Orc, and its pets -> Tiger -------------------------
log.append("== gnashfang rahskhas -> Orc, and rahskhas's pet -> Tiger (page: \"five pet tigers\")")
FS('gnashfang rahskhas', fam='Orc', crys='Fire', job='Red Mage / Beastmaster', kit=mode_field('Orc','ab'))
S('gnashfang rahskhas','ab',mode_field('Orc','ab')+['Chainspell'],'page names Chainspell')
S('gnashfang rahskhas','sp',['Slow II','Paralyze II','Diaga III','Bio III','Cure IV'],'page')
S('gnashfang rahskhas','agg',True,'page notes column: A, L, S')
S('gnashfang rahskhas','lnk',True,'page notes column: A, L, S')
S('gnashfang rahskhas','det',['Sight'],'page notes column: A, L, S')
S('gnashfang rahskhas','nm',True,'page red banner')
S('gnashfang rahskhas','zones',[['Batallia Downs [S]']],'page')
S('gnashfang rahskhas','spawn','Quest (Succor to the Sidhe)','page')
S('gnashfang rahskhas','notes',['Accompanied by five pet tigers; if they are killed he eventually summons new ones.',
  'Very high HP, but easy to tank so long as you do not feed him TP. His pets sleep, but not for long.',
  'The fight is confined to a 50-foot radius from the top of the hill at (F-7) — leaving it drops you from the battle with no way back in.',
  'Buffs carry in; no cures from outside the party, and outside monsters and -ga spells cannot reach you.',
  'If the party wipes, the mobs return to the hilltop and despawn after two minutes.'],'page')
FS("rahskhas's pet", fam='Tiger', grid='family', crys='Lightning', job='Warrior', kit=mode_field('Tiger','ab'))
S("rahskhas's pet",'agg',True,'assists an aggressive NM')
S("rahskhas's pet",'zones',[['Batallia Downs [S]']],'page')
S("rahskhas's pet",'spawn','Pet of Gnashfang Rahskhas','page')
S("rahskhas's pet",'notes',["Five accompany Gnashfang Rahskhas during Succor to the Sidhe; he summons replacements if they are killed."],'page')

# ---- go'rha sludgewater -> Quadav (family grid fits the page; stored did not) --
log.append("== go'rha sludgewater (BG page) — stored grid had NO Lightning; the page says Lightning")
FS("go'rha sludgewater", fam='Quadav', grid='family', crys='Water', job='Warrior',
   det=['True Sound'], kit=mode_field('Quadav','ab'))
S("go'rha sludgewater",'agg',True,'page notes column: A, T(H)')
S("go'rha sludgewater",'nm',True,'page red banner')
S("go'rha sludgewater",'zones',[['Pashhow Marshlands [S]']],'page')
S("go'rha sludgewater",'spawn','Quest (Succor to the Sidhe)','page')
S("go'rha sludgewater",'notes',['Assisted by ten Swamp Mucks.'],'page')

# ---- enrichment: moblin fantocciniman (already Goblin) ------------------------
log.append('== moblin fantocciniman — already familied; enriched from the ENM page')
S('moblin fantocciniman','notes',['The second enemy of the Pulling the Strings ENM. Will not aggro and never attacks unless you take offensive action against him — an area-of-effect will do it.',
  'His dice ability rolls effects onto either the Fantoccini or you: Attack Bonus, Defense Bonus, +100% TP, full HP restore, all job-ability timers reset, or permission for the Fantoccini to use a weapon skill or job ability.',
  'Killing him instead of the Fantoccini leaves the Fantoccini and its pet frozen in terror for the rest of the fight — amusing, but harder.'],'ENM page')

assert not [k for m in M.values() for k,v in m.items() if v is None], 'null poison'
T=['dweomershell','eraser','fantoccini monster','fantoccini','fay','feeorin','gelatinous clot',
   'ghayaraan','gowam','giant beastmaster','giant high ranger','giant monk','giant warrior',
   'glacial wisp','gnashfang rahskhas',"rahskhas's pet","go'rha sludgewater",'moblin fantocciniman']
bad=[(k,a) for k,v in M.items() for a in (v.get('ab') or []) if a not in AB]
assert not [x for x in bad if x[0] in T], f'undefined refs: {[x for x in bad if x[0] in T]}'
json.dump(d,open(P,'w'),separators=(', ', ': '),ensure_ascii=False)
print('\n'.join(log))
print(f'\nmobs {len(M)}  orphans {sum(1 for v in M.values() if not v.get("fam"))}  NM {sum(1 for v in M.values() if v.get("nm"))}  undefined {len(bad)}/{len(set(a for _,a in bad))}')
