# rev 368 — SECTION X BATCH 18: the last 12 records. Section X closes.
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
    log.append(f'  {key}: {f} {json.dumps(old,ensure_ascii=False)[:46]} -> {json.dumps(val,ensure_ascii=False)[:70]}  [{why}]')
def D(key,f,why):
    if f in M[key]: log.append(f'  {key}: REMOVED {f} ({json.dumps(M[key].pop(f),ensure_ascii=False)[:36]})  [{why}]')
def FS(key,grid=None,crys=None,job=None,det=None,kit=None):
    v=M[key]; f=v['fam']
    if grid=='family':
        wk,st=mode_grid(f); S(key,'wk',wk,'family grid'); S(key,'st',st,'family grid')
    if crys and not v.get('crys'): S(key,'crys',crys,'crystal')
    if job and not v.get('job'):   S(key,'job',job,'job')
    if det: S(key,'det',det,'detection')
    if kit is not None and not v.get('ab'): S(key,'ab',kit,'kit')

LEECH_KIT=mode_field('Leech','ab'); GNAT_KIT=mode_field('Gnat','ab')
GEAR_KIT=mode_field('Gear','ab');   CRAB_KIT=mode_field('Crab','ab')
DRAGON_KIT=mode_field('Dragon','ab')

# ---- 1 quiescent leech (AI panel) -------------------------------------------
log.append('== quiescent leech (AI panel)')
FS('quiescent leech', crys='Water', job='Warrior', det=['Sound'], kit=LEECH_KIT)
S('quiescent leech','zones',[['Sih Gates','119-121']],'panel')
S('quiescent leech','drops','Water Crest Card','panel')
S('quiescent leech','notes',['Found on Map 2 of Sih Gates, reached from the Ceizak Battlegrounds crystal.',
  'Drops the Water Crest Card used in Escutcheon crafting.',
  'The deeper part of the map needs the matching Ulbukan Wildskeeper Reive key item.'],'panel')

# ---- 2 liquidbone leech (AI panel) ------------------------------------------
log.append('== liquidbone leech (AI panel)')
FS('liquidbone leech', crys='Water', job='Warrior', kit=LEECH_KIT)
S('liquidbone leech','zones',[['Moh Gates','120-124']],'panel')
S('liquidbone leech','notes',['Found on Map 2 of Moh Gates.',
  'Drops Escutcheon crest cards and Fiend Blood.'],'panel')

# ---- 3 duke vepar's gnat (AI panel) -----------------------------------------
log.append("== duke vepar's gnat (AI panel)")
FS("duke vepar's gnat", grid='family', crys='Dark', job='Thief', det=['Sight'], kit=GNAT_KIT)
S("duke vepar's gnat",'sp',['Blind II','Paralyze II','Sleep II'],'panel')
S("duke vepar's gnat",'zones',[['Escha RuAun']],'panel')
S("duke vepar's gnat",'content',['Geas Fete: Escha RuAun: Tier 3'],'copied from duke vepar')
S("duke vepar's gnat",'spawn','Add of Duke Vepar','panel')
S("duke vepar's gnat",'notes',['Attacks at high speed and disrupts shadow recasting.',
  'Booming Bombination is area-of-effect magic damage with Plague, Defense down and Magic Defense down.',
  'Cimicine Discharge slows players in range and hastes the gnat.',
  'Insipid Nip steals a single attribute from its target.'],'panel')

# ---- 4 ark angel's gnat (AI panel) ------------------------------------------
log.append("== ark angel's gnat (AI panel)")
FS("ark angel's gnat", grid='family', crys='Dark', job='Thief', kit=GNAT_KIT)
S("ark angel's gnat",'zones',[['Escha RuAun']],'panel')
S("ark angel's gnat",'content',['Geas Fete: Escha RuAun: Ark Angels'],'copied from ark angel mr')
S("ark angel's gnat",'spawn',"Pet of Ark Angel MR",'panel')
S("ark angel's gnat",'notes',['A pet spawned alongside Ark Angel MR in place of the usual Tiger or Mandragora.',
  'Pandemic Nip stacks Paralyze, Blind and Silence; Bombilation wipes TP in an area.'],'panel')

# ---- 5/6 vigilant gear + vigilant gears (two separate BG pages) --------------
for k in ['vigilant gear','vigilant gears']:
    log.append(f'== {k} (BG page — Crystal: None; a REAL page, not a duplicate)')
    FS(k, grid='family', job='Ranger', det=mode_field('Gear','det'), kit=GEAR_KIT)
    S(k,'spawn','Bastion','page')
    S(k,'notes',['Spawns during Bastion; only aggressive to players with Pennant status.',
      'Four spawn per Abyssea zone.','The page states Crystal: None.'],'page')

# ---- 7 rancidclaw crab (AI panel) -------------------------------------------
log.append('== rancidclaw crab (AI panel)')
D('rancidclaw crab','agg','panel: Passive, does not aggro on sight')
FS('rancidclaw crab', crys='Water', job='Paladin', kit=CRAB_KIT)
S('rancidclaw crab','notes',['Found on Map 2 of Dho Gates.'],'panel')

# ---- 8 plunderer crab (BG page) ---------------------------------------------
log.append('== plunderer crab (BG page)')
D('plunderer crab','agg','page Notes column reads NA (non-aggressive)')
FS('plunderer crab', crys='Water', job='Paladin', kit=CRAB_KIT)

# ---- 9 yilan's dragon (AI panel) --------------------------------------------
log.append("== yilan's dragon (AI panel)")
FS("yilan's dragon", grid='family', crys='Dark', job='Warrior', kit=DRAGON_KIT)
S("yilan's dragon",'zones',[['Escha RuAun']],'panel')
S("yilan's dragon",'content',['Geas Fete: Escha RuAun: Tier 2'],'copied from yilan')
S("yilan's dragon",'spawn','Add of Yilan','panel')
S("yilan's dragon",'notes',['Smaller helper dragons that spawn alongside the Geas Fete notorious monster Yilan.'],'panel')

# ---- 10 hraun dragon (BG page) ----------------------------------------------
log.append('== hraun dragon (BG page — Voidwatch NM (Zilart Stage I))')
FS('hraun dragon', grid='family', crys='Dark', job='Warrior', kit=DRAGON_KIT)
S('hraun dragon','lnk',True,'page Notes column prints L')
S('hraun dragon','zones',[['Ifrits Cauldron','95-96']],'page')
S('hraun dragon','spawn','Voidwatch (Ashen stratum abyssite + Voidstone at a Planar Rift)','page')
S('hraun dragon','notes',['Two spawn per rift, at the Planar Rift on Map 3 (F-9) or on Map 5 at (F-9) or (I-6).',
  'Assists Ildebrann and must be defeated before Ildebrann will land on the ground.',
  'Resummoned a few minutes after death.'],'page')

# ---- 11 mystic avatar (BG page) ---------------------------------------------
log.append('== mystic avatar (BG page)')
S('mystic avatar','wk',[['Varies',None]],'page: Weak to Varies — the family\u2019s established shape')
S('mystic avatar','st',[['Varies',None]],'page: Strong to Varies')
FS('mystic avatar', job='Varies', det=['True Sound'])
S('mystic avatar','nm',True,'page red banner')
S('mystic avatar','zones',[['Temenos']],'page (Eastern Tower / Central 2nd / Central 4th are sub-areas)')
S('mystic avatar','drops','Anct. Beastcoin','page')
S('mystic avatar','notes',['Avatars that appear in certain areas of Temenos: 7 in the Eastern Tower, 7 on Central Temenos 2nd Floor, 6 on Central Temenos 4th Floor.',
  'May be any avatar except Diabolos, Alexander and Odin, usually matching the associated elemental.',
  'All are susceptible to Stun — even Ramuh and Titan.',
  'Can use any of their blood pacts including Astral Flow pacts; damage from those (Tidal Wave, for instance) is blocked by a difference in terrain height, so standing on a ramp above the avatar protects you.',
  'Eastern Tower: up to two crates appear per floor, one holding treasure and one holding a Mystic Avatar of that floor\u2019s element — opening the treasure crate makes the avatar crate vanish.',
  'Central Temenos 2nd Floor: defeating an elemental turns the elemental weak to it into the matching Mystic Avatar (killing the Fire Elemental replaces the Ice Elemental with Shiva). The zone Mega Boss is a Mystic Avatar (Carbuncle) guarded by two Light Elementals.',
  'Central Temenos 4th Floor: summoned by Koo Buzu the Theomanic.'],'page')

# ---- 12 fantoccini avatar (BG page) -----------------------------------------
log.append('== fantoccini avatar (BG page — "Empty Notorious Monster")')
S('fantoccini avatar','wk',[['Varies',None]],'page: Weak to varies')
FS('fantoccini avatar', det=['True Sound'])
S('fantoccini avatar','nm',True,'page banner reads "Empty Notorious Monster" — an ENM boss')
S('fantoccini avatar','zones',[['Mine Shaft 2716','49']],'page')
S('fantoccini avatar','spawn','ENM (Pulling the Strings)','page')
S('fantoccini avatar','notes',['A single spawn, fought in the ENM Pulling the Strings.'],'page')

CLEARED=['quiescent leech','liquidbone leech',"duke vepar's gnat","ark angel's gnat",
         'vigilant gear','vigilant gears','rancidclaw crab','plunderer crab',
         "yilan's dragon",'hraun dragon','mystic avatar','fantoccini avatar']
for k in CLEARED:
    if M[k].get('img')=='mobimages/review_x.png': M[k].pop('img')
log.append(f'== review_x cleared on {len(CLEARED)} records — SECTION X IS EMPTY')

assert not [k for m in M.values() for k,v in m.items() if v is None], 'null poison'
bad=[(k,a) for k,v in M.items() for a in (v.get('ab') or []) if a not in AB]
assert not [x for x in bad if x[0] in CLEARED], f'undefined refs: {[x for x in bad if x[0] in CLEARED]}'
json.dump(d,open(P,'w'),separators=(', ', ': '),ensure_ascii=False)
print('\n'.join(log))
rx=[k for k,v in M.items() if v.get('img')=='mobimages/review_x.png']
print(f'\nmobs {len(M)}  review_x {len(rx)}  NM {sum(1 for v in M.values() if v.get("nm"))}  undefined {len(bad)}/{len(set(a for _,a in bad))}')
