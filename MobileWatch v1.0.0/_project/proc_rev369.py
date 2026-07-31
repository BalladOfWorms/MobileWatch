# rev 369 — ORPHAN BUCKET: 19 fam=None records folded into 7 families from 16 sources
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
    log.append(f'  {key}: {f} {json.dumps(old,ensure_ascii=False)[:40]} -> {json.dumps(val,ensure_ascii=False)[:66]}  [{why}]')
def FOLD(key,fam,why):
    S(key,'fam',fam,'FOLD '+why)
def FS(key,grid=None,crys=None,job=None,det=None,kit=None):
    v=M[key]; f=v['fam']
    if grid=='family':
        wk,st=mode_grid(f); S(key,'wk',wk,'family grid'); S(key,'st',st,'family grid')
    if crys and not v.get('crys'): S(key,'crys',crys,'crystal')
    if job and not v.get('job'):   S(key,'job',job,'job')
    if det: S(key,'det',det,'detection')
    if kit is not None and not v.get('ab'): S(key,'ab',kit,'kit')

BAT_KIT=mode_field('Bat','ab'); SHEEP_KIT=mode_field('Sheep','ab')
TON_KIT=mode_field('Tonberry','ab'); PUGIL_KIT=mode_field('Pugil','ab')
CRAB_KIT=mode_field('Crab','ab'); SAH_KIT=mode_field('Sahagin','ab')

# ---------------- BAT: balayang + desmodus (BG pages, "Family: Giant Bats") ----
log.append('== balayang + desmodus (BG pages) — grid CORROBORATED by both pages, KEPT')
for k,zone,lv in [('balayang',['FeiYin','95-99'],None),('desmodus',['Castle Zvahl Keep [S]','80-82'],None)]:
    FOLD(k,'Bat','BG says "Family: Giant Bats"; no Giant Bat family exists here — see review')
    FS(k, crys='Wind', job='Warrior', kit=BAT_KIT)
    S(k,'zones',[zone],'page')
S('balayang','notes',['Non-aggressive, with roughly 8,800 HP.',
  'Twenty-four spawn in the four small rooms on the first map, at (J-6), (J-7), (K-7), (I-6) and (I-7).'],'page')
S('desmodus','notes',['Nine spawn in Castle Zvahl Keep [S], on a 16-minute respawn.'],'page')

# ---------------- SHEEP: ark angel's karakul (AI panel) -----------------------
log.append("== ark angel's karakul (AI panel)")
FOLD("ark angel's karakul",'Sheep','panel: pet of Ark Angel MR; wild karakul is already Sheep')
FS("ark angel's karakul", crys='Earth', job='Warrior', kit=SHEEP_KIT)
S("ark angel's karakul",'zones',[['Escha RuAun']],'panel')
S("ark angel's karakul",'content',['Geas Fete: Escha RuAun: Ark Angels'],'copied from ark angel mr')
S("ark angel's karakul",'spawn','Pet of Ark Angel MR','panel')
S("ark angel's karakul",'notes',['Summoned at the start of the Ark Angel MR fight, as an alternative to the Gnat.',
  'Uses Sheep Song every single time it wakes, alongside Lamb Chop, and regains TP very fast.',
  'Sleeps easily to elemental or dark sleep spells — park it and focus the Ark Angel.'],'panel')

# ---------------- TONBERRY: the four Cooks (AI panel names all four) ----------
log.append('== the four Cook tonberries (AI panel names all four + their jobs)')
for k,job in [('cook nalberry','Thief'),('cook minberry','Ninja'),
              ('cook solberry','Black Mage'),('cook fulberry','Summoner')]:
    FOLD(k,'Tonberry','panel names all four Cooks as Tonberry NMs')
    FS(k, grid='family', crys='Light', job=job, kit=TON_KIT)
    S(k,'nm',True,'panel: Notorious Monster')
    S(k,'zones',[['Temple of Uggalepih','75']],'panel')
    S(k,'spawn','Quest penalty ("You Call That a Knife?")','panel')
S('cook nalberry','notes',['Spawns at (G-10) in the Temple of Uggalepih as a penalty during "You Call That a Knife?", if an item other than the correct Tonberry Board is traded to Chef Nonberry.',
  'Comes with three other chef NMs: Cook Minberry, Cook Solberry and Cook Fulberry.',
  'All four use two-hour job abilities; dangerous to lower-level players, but easily slept by level 75+.'],'panel')
for k in ['cook minberry','cook solberry','cook fulberry']:
    S(k,'notes',['Spawns alongside Cook Nalberry at (G-10) as a penalty during "You Call That a Knife?", if the wrong item is traded to Chef Nonberry.',
      'Uses two-hour job abilities.'],'panel')

# ---------------- PUGIL: chrysoberyl jagil (AI panel) -------------------------
log.append('== chrysoberyl jagil (AI panel) — the last unfamilied jagil')
FOLD('chrysoberyl jagil','Pugil','24 of the 25 jagils are already Pugil; this was the orphan')
FS('chrysoberyl jagil', crys='Water', job='Warrior', kit=PUGIL_KIT)
S('chrysoberyl jagil','zones',[['Woh Gates','111']],'panel')
S('chrysoberyl jagil','spawn','Fished Up','panel')
S('chrysoberyl jagil','notes',['A hooked sea-catch fished up in Woh Gates, near (H-5) and (I-10).'],'panel')

# ---------------- CRAB: crabshaw (BG page) -----------------------------------
log.append('== crabshaw (BG page) — grid corroborated ("Weak against: Lightning, Ice")')
FOLD('crabshaw','Crab','page: Family: Crabs')
FS('crabshaw', crys='Water', job='Paladin', kit=CRAB_KIT)
S('crabshaw','nm',True,'page red banner')
S('crabshaw','zones',[['QuBia Arena']],'page')
S('crabshaw','notes',['Assists your Adventuring Fellow in Clash of the Comrades when their job is set to Beastmaster.',
  'Susceptible to sleep.'],'page')

# ---------------- SAHAGIN: the three Demisahagins (BG pages) ------------------
log.append('== demisahagin bard / dragoon / monk (BG pages) — Expeditionary Force, NOT NMs')
for k,job,note in [('demisahagin bard','Bard','Uses Soul Voice at some point.'),
                   ('demisahagin dragoon','Dragoon','Calls a pet wyvern, which follows and assists it in combat.'),
                   ('demisahagin monk','Monk','Uses Hundred Fists at some point.')]:
    FOLD(k,'Sahagin','page: Family: Sahagin')
    FS(k, crys='Water', job=job, kit=SAH_KIT)
    S(k,'zones',[['Yuhtunga Jungle','45']],'page')
    S(k,'spawn',"Expeditionary Force (Beastman's Banner)",'page')
    S(k,'notes',["Sometimes spawned from a Beastman's Banner during Expeditionary Force.",note],'page')

# ---------------- AVATAR: ayakashi (BG page) ---------------------------------
log.append('== ayakashi (BG page)')
FOLD('ayakashi','Avatar','page: Family: Avatar')
S('ayakashi','wk',[['Varies',None]],'page: Weak to Varies (rule 361 shape)')
FS('ayakashi', det=['Sight','Scent'])
S('ayakashi','nm',True,'page red banner')
S('ayakashi','zones',[['Waughroon Shrine','66-67']],'page')
S('ayakashi','spawn','Battlefield (SAM AF3: A Thief in Norg!?)','page')
S('ayakashi','notes',['Fought in the battlefield for SAM AF3: A Thief in Norg!?.',
  'Summoned by Onki when it uses Astral Flow, and assists it.'],'page')

# ---------------- HUMANOID: amnaf, bashdeel, counselor mihli, curilla, danzo --
log.append('== the five Humanoids (BG pages) — Humanoid has no family stamp to give (rule 346)')
FOLD('amnaf','Humanoid','page: Family: Humanoids/Soulflayers — first two forms are the Humanoid')
FS('amnaf', job='Blue Mage', det=['Magic','JA','True Sound'])
S('amnaf','nm',True,'page red banner')
S('amnaf','zones',[['Nyzul Isle','77-79']],'page')
S('amnaf','spawn','Aht Urhgan Mission 42: Path of Darkness','page')
S('amnaf','notes',['Fought for Aht Urhgan Mission 42: Path of Darkness.',
  'Summons Imperial Gears when first engaged, then triple gears when engaged in the second round.',
  'Transforms into a Soulflayer for the third round.',
  'Susceptible to ordinary Enfeebling Magic in its first two forms; far more resistant once it is a Soulflayer.'],'page')

FOLD('bashdeel','Humanoid','page: Family: Humanoids')
FS('bashdeel', job='Blue Mage', det=['True Sound'])
S('bashdeel','zones',[['Leujaoam Sanctum','75']],'page')
S('bashdeel','spawn','Assault (Red Versus Blue)','page')
S('bashdeel','notes',['One of your opponents during the Red Versus Blue assault.'],'page')

FOLD('counselor mihli','Humanoid','page: Family: Humanoids')
FS('counselor mihli', job='White Mage', det=['True Sound'])
S('counselor mihli','nm',True,'page red banner')
# 'Scouring Bubbles' had no def — it is Mihli Aliapoh's own AoE club weapon skill,
# listed under her `ws` in trusts.json. Defined from that in-file source, not invented.
if 'Scouring Bubbles' not in AB:
    AB['Scouring Bubbles'] = {"d": "Area-of-effect club weapon skill.", "tgt": "AoE",
        "notes": "Mihli Aliapoh's signature weapon skill; she prefers it over other WS."}
    log.append("  abilities: DEFINED 'Scouring Bubbles' from Mihli Aliapoh's ws list in trusts.json")
S('counselor mihli','ab',['Benediction','Scouring Bubbles'],'page names both')
S('counselor mihli','zones',[['Stellar Fulcrum','60']],'page')
S('counselor mihli','spawn','Battlefield (Mercenary Camp)','page')
S('counselor mihli','notes',['Fought for the Mercenary Camp special battlefield event.'],'page')

FOLD('curilla','Humanoid','page: Family: Humanoids')
FS('curilla', job='Paladin')
S('curilla','nm',True,'page red banner')
S('curilla','ab',['Invincible'],'page: "Special Attacks: will use Invincible"')
S('curilla','sp',['Flash','Protect III','Shell II','Cure IV'],'page')
S('curilla','zones',[['Stellar Fulcrum','60']],'page')
S('curilla','spawn',"Battlefield (Heroine's Combat)",'page')
S('curilla','notes',["Fought for the Heroine's Combat special BCNM.",'Will use Invincible.'],'page')

FOLD('danzo','Humanoid','page: Family: Humanoids')
FS('danzo', job='Ninja', det=['True Sight'])
S('danzo','nm',True,'page red banner')
S('danzo','zones',[['Leujaoam Sanctum','79-80']],'page')
S('danzo','spawn','Assault (Imperial Code)','page')
S('danzo','notes',['Appears in the Imperial Code assault.'],'page')

assert not [k for m in M.values() for k,v in m.items() if v is None], 'null poison'
TOUCHED=['balayang','desmodus',"ark angel's karakul",'cook nalberry','cook minberry','cook solberry',
         'cook fulberry','chrysoberyl jagil','crabshaw','demisahagin bard','demisahagin dragoon',
         'demisahagin monk','ayakashi','amnaf','bashdeel','counselor mihli','curilla','danzo']
bad=[(k,a) for k,v in M.items() for a in (v.get('ab') or []) if a not in AB]
assert not [x for x in bad if x[0] in TOUCHED], f'undefined refs: {[x for x in bad if x[0] in TOUCHED]}'
json.dump(d,open(P,'w'),separators=(', ', ': '),ensure_ascii=False)
print('\n'.join(log))
orph=sum(1 for v in M.values() if not v.get('fam'))
print(f'\nmobs {len(M)}  fam=None orphans {orph}  NM {sum(1 for v in M.values() if v.get("nm"))}  undefined {len(bad)}/{len(set(a for _,a in bad))}')
