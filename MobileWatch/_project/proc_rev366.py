# rev 366 — Section X batch 16: the single-record tail, 14 records / 14 families
# BalladOfWorms
import json, collections, sys, copy

P = '/home/claude/android/app/src/main/assets/mobs.json'
d = json.load(open(P))
M = d['mobs']; AB = d['abilities']

def gk(v): return json.dumps([v.get('wk'), v.get('st')], ensure_ascii=False)

def mode_grid(fam):
    mem = [v for v in M.values() if v.get('fam') == fam]
    c = collections.Counter(gk(v) for v in mem)
    wk, st = json.loads(c.most_common(1)[0][0])
    return copy.deepcopy(wk), copy.deepcopy(st)

def mode_field(fam, key):
    mem = [v for v in M.values() if v.get('fam') == fam and v.get(key)]
    c = collections.Counter(json.dumps(v[key], ensure_ascii=False) for v in mem)
    return json.loads(c.most_common(1)[0][0]) if c else None

log = []
def setk(key, field, val, why):
    old = M[key].get(field)
    M[key][field] = val
    log.append(f'  {key}: {field} {json.dumps(old,ensure_ascii=False)[:60]} -> {json.dumps(val,ensure_ascii=False)[:80]}  [{why}]')

def delk(key, field, why):
    if field in M[key]:
        old = M[key].pop(field)
        log.append(f'  {key}: REMOVED {field} ({json.dumps(old,ensure_ascii=False)[:50]})  [{why}]')

def stamp(key, fam=None, grid=None, crys=None, job=None, det=None, kit=None):
    v = M[key]
    f = fam or v['fam']
    if grid == 'family':
        wk, st = mode_grid(f); setk(key,'wk',wk,'family grid'); setk(key,'st',st,'family grid')
    if crys and not v.get('crys'): setk(key,'crys',crys,'family/page crystal')
    if job and not v.get('job'): setk(key,'job',job,'family/page job')
    if det: setk(key,'det',det,'page/family detection')
    if kit is not None and not v.get('ab'): setk(key,'ab',kit,'family kit')

# ---------------------------------------------------------------- 1 pixie impaler -> Bee
log.append('== pixie impaler (BG page: Family Bees)')
wk,st = mode_grid('Bee')
setk('pixie impaler','fam','Bee','page infobox says Family: Bees; grid twin flitting bee is Bee; pixietrap precedent')
setk('pixie impaler','wk',wk,'Bee family grid (page Weak to Ice+Piercing = its top two)')
setk('pixie impaler','st',st,'Bee family grid')
setk('pixie impaler','crys','Wind','Bee family')
setk('pixie impaler','job','Warrior','Bee family default (page Job blank)')
setk('pixie impaler','ab',mode_field('Bee','ab'),'Bee family kit')
setk('pixie impaler','agg',True,'page notes column prints A')
setk('pixie impaler','spawn','Quest (Succor to the Sidhe)','page')
setk('pixie impaler','notes',['Spawned with Stabnix Skewerfinger for the quest Succor to the Sidhe.','Six spawn in North Gustaberg [S].'],'page')

# ---------------------------------------------------------------- 2 warder's phuabo
log.append("== warder's phuabo (AI panel)")
stamp("warder's phuabo", grid='family', crys='Varies', job='Varies', det=['Sound'], kit=mode_field('Phuabo','ab'))
setk("warder's phuabo",'zones',[['Escha RuAun']],'panel')
setk("warder's phuabo",'content',['Geas Fete: Escha RuAun: Nazar'],'copied from warder of love')
setk("warder's phuabo",'spawn','Geas Fete (Escha - Ru\u2019Aun)','panel')
setk("warder's phuabo",'notes',['Drops a component used to spawn high-tier Escha - Ru\u2019Aun notorious monsters such as the Warder of Love.','Panel gives the level as 120; the stored band is 123.'],'panel')

# ---------------------------------------------------------------- 3 temple opo-opo
log.append('== temple opo-opo (BG page)')
stamp('temple opo-opo', crys='Lightning', det=['Scent'], kit=mode_field('Opo-opo','ab'))
setk('temple opo-opo','notes',['Twenty-three spawn in the Temple of Uggalepih.'],'page')

# ---------------------------------------------------------------- 4 sprightly leafkin
log.append('== sprightly leafkin (BG page)')
stamp('sprightly leafkin', crys='Earth', kit=mode_field('Leafkin','ab'))
setk('sprightly leafkin','notes',['Single spawn in Kamihr Drifts; steals nothing.'],'page')

# ---------------------------------------------------------------- 5 hydra -> merge into hydra (nm), delete
log.append('== hydra  MERGE INTO "hydra (nm)" then DELETE (review rule 7)')
h = M['hydra']; n = M['hydra (nm)']
for f in ('lv','resp','spawn','nmlv'):
    if f in h and f not in n:
        n[f] = h[f]; log.append(f'  hydra (nm): merged {f} = {json.dumps(h[f],ensure_ascii=False)} from the duplicate')
n['agg'] = True; log.append('  hydra (nm): agg = True (Listings behavior column)')
n['zones'] = [['Wajaom Woodlands','80'],['Nyzul Isle'],['Zhayolm Remnants']]
n['drops'] = ', '.join(["Berserker's Torque","Sirius Axe",
  'Askar Manopolas','Denali Wristbands','Goliard Cuffs',
  'Askar Korazin','Denali Jacket','Goliard Saio',
  'Askar Zucchetto','Denali Bonnet','Goliard Chapeau',
  "Ate's Mask","Ate's Gauntlets","Ate's Flanchard",'Genta Kabuto',
  "Idi's Jerkin","Idi's Trousers","Idi's Ledelsens",
  "Namru's Crackows","Namru's Jubbah","Neit's Cuffs"])
log.append('  hydra (nm): drops rebuilt from the Listings table (Hydra Fang/Meat/Scale dropped as crafting mats)')
n['notes'] = n['notes'] + [
  'Wajaom Woodlands HNM: roughly 73,000 HP, M.DEF 130, INT 75, with Auto-Regen, Draw-In and Regain. Defeating it earns the title Hydra Headhunter.',
  'Spawns at (F-10) on a 48-72 hour timer checked hourly; the area is reached through Exit (7) at (I/J-8) on Map 3 of Aydeewa Subterrane.',
  'Nyzul Isle: appears on Investigation floors 60, 80 and 100 and drops a random Vigil weapon; only the floor-100 Hydra gains Nerve Gas under 30% HP.',
  'Zhayolm Remnants: spawns from the 6th floor North Rampart and the 7th floor boss Rampart, and gains Nerve Gas at low HP.']
log.append('  hydra (nm): +4 notes')
del M['hydra']
log.append('  DELETED the duplicate record "hydra"')

# ---------------------------------------------------------------- 6 nekros hound
log.append('== nekros hound (BG page)')
stamp('nekros hound', crys='Dark', job='Warrior', kit=mode_field('Hound','ab'))
setk('nekros hound','notes',['The Eldieme Necropolis: 2 spawns at (K/L-7) and 2 at (K-11/12) on Map 2; 13 more on Map 3, all level 91-95.'],'page Locations')

# ---------------------------------------------------------------- 7 nesting hippogryph
log.append('== nesting hippogryph (AI panel)')
stamp('nesting hippogryph', crys='Light', job='Thief / Black Mage', kit=mode_field('Hippogryph','ab'))
setk('nesting hippogryph','drops','Sullied Feather, Wind Crest Card','panel (Hippogryph Tf. omitted as a craft mat)')
setk('nesting hippogryph','notes',['Found on Map 2 of Woh Gates.','The Rare/Ex Sullied Feather is the pop item for the notorious monster Cowll Hippogryph.'],'panel')

# ---------------------------------------------------------------- 8 shivering heartwing
log.append('== shivering heartwing (BG page)')
stamp('shivering heartwing', crys='Light', job='White Mage', kit=mode_field('Heartwing','ab'))

# ---------------------------------------------------------------- 9 warder's ghrah
log.append("== warder's ghrah (AI panel)")
setk("warder's ghrah",'wk',[],'Ghrah is a swipe-set family - members carry empty grids')
setk("warder's ghrah",'st',[],'Ghrah is a swipe-set family')
stamp("warder's ghrah", crys='Varies', job='Black Mage / Warrior / Thief / Paladin',
      det=['Sound'], kit=mode_field('Ghrah','ab'))
setk("warder's ghrah",'zones',[['Escha RuAun']],'panel')
setk("warder's ghrah",'content',['Geas Fete: Escha RuAun: Nazar'],'copied from warder of fortitude')
setk("warder's ghrah",'spawn','Geas Fete (Escha - Ru\u2019Aun, Portal 3)','panel')
setk("warder's ghrah",'notes',['Shifts between four forms, each with its own job: Ball (Black Mage), Bird (Thief), Spider (Warrior) and Humanoid (Paladin).','Damnation Dive is used in Bird form only.','Defeating these can spawn the Warder of Fortitude.'],'panel')

# ---------------------------------------------------------------- 10 plodding funguar
log.append('== plodding funguar (BG page - ordinary mob page, no red banner)')
delk('plodding funguar','nm','page has no Notorious Monster banner: 8 spawns, NA/H/L, ordinary drop table')
setk('plodding funguar','lv',[119,121],'page level column (was the suspect Cirdas [125,126] import default)')
setk('plodding funguar','zones',[['Cirdas Caverns','119-121']],'page')
setk('plodding funguar','lnk',True,'page notes column prints L')
stamp('plodding funguar', crys='Dark', job='Warrior', kit=mode_field('Funguar','ab'))
setk('plodding funguar','notes',['Eight spawn in Cirdas Caverns.'],'page')

# ---------------------------------------------------------------- 11 eschan il'aern's euvhi
log.append("== eschan il'aern's euvhi (AI panel)")
stamp("eschan il'aern's euvhi", grid='family', crys='Varies', job='Warrior', kit=mode_field('Euvhi','ab'))
setk("eschan il'aern's euvhi",'sp',['Aero IV','Aeroga III','Stone IV','Slowga'],'panel')
setk("eschan il'aern's euvhi",'zones',[['Escha RuAun','116']],'panel')
setk("eschan il'aern's euvhi",'spawn',"Add of Eschan Il'aern",'panel')
setk("eschan il'aern's euvhi",'notes',['Shifts between an open and a closed state.','Open: takes double damage, deals wind damage and casts wind spells such as Aero IV and Aeroga III.','Closed: hits much harder physically, deals earth damage and casts earth spells such as Stone IV and Slowga.','Found on the floating islands reached through Portals 3, 6 and 9.'],'panel')

# ---------------------------------------------------------------- 12 surly craklaw
log.append('== surly craklaw (AI panel)')
delk('surly craklaw','agg','panel states Behavior: Passive')
stamp('surly craklaw', grid='family', crys='Water', kit=mode_field('Craklaw','ab'))
setk('surly craklaw','nmlv','124','panel')
setk('surly craklaw','drops','Wrecked Pincer, S. Kindred Crest','panel (Sacred Kindred\u2019s Crest -> DB "S. Kindred Crest")')

# ---------------------------------------------------------------- 13 naphula's corpselight
log.append("== naphula's corpselight (AI panel)")
stamp("naphula's corpselight", grid='family', crys='Dark', job='Black Mage',
      det=['Sound','Blood'], kit=['Corpse Breath'])
setk("naphula's corpselight",'zones',[['Escha RuAun']],'panel')
setk("naphula's corpselight",'content',['Geas Fete: Escha RuAun: Tier 2'],'copied from naphula')
setk("naphula's corpselight",'spawn','Add of Naphula','panel')
setk("naphula's corpselight",'notes',['Two are called during the Naphula fight when it uses its area-of-effect stun.','Hostile magic-users; an Undead Kahiraise sub-species.'],'panel')

# ---------------------------------------------------------------- 14 predatory colibri
log.append('== predatory colibri (AI panel)')
stamp('predatory colibri', grid='family', crys='Wind', job='Red Mage', kit=mode_field('Colibri','ab'))
setk('predatory colibri','sp',['Firaja','Thundaja','Comet','Meteor'],'panel')
setk('predatory colibri','zones',[['Mamook','99']],'panel')
setk('predatory colibri','spawn','Voidwatch add of Yalungur','panel')
setk('predatory colibri','notes',['Summoned by Yalungur when Snatch Morsel successfully strips a food effect from a player, and when the fight is left unchecked.','Casts high-tier -aja spells and Comet, and will use Meteor if enough of them accumulate.'],'panel')

# ---------------------------------------------------------------- clear the red X
CLEARED = ['pixie impaler',"warder's phuabo",'temple opo-opo','sprightly leafkin','nekros hound',
           'nesting hippogryph','shivering heartwing',"warder's ghrah",'plodding funguar',
           "eschan il'aern's euvhi",'surly craklaw',"naphula's corpselight",'predatory colibri']
for k in CLEARED:
    if M[k].get('img') == 'mobimages/review_x.png': M[k].pop('img')
log.append(f'== review_x cleared on {len(CLEARED)} records (+1 deleted with the hydra duplicate)')

# ---------------------------------------------------------------- guards
assert not [k for m in M.values() for k, v in m.items() if v is None], 'null poison'
bad = [(k, a) for k, v in M.items() for a in (v.get('ab') or []) if a not in AB]
newbad = [x for x in bad if x[0] in CLEARED or x[0] == 'hydra (nm)']
assert not newbad, f'undefined ability refs introduced: {newbad}'
for k in CLEARED:
    assert isinstance(M[k].get('ab', []), list)
    assert M[k].get('ab') is None or all(isinstance(a, str) for a in M[k]['ab'])

json.dump(d, open(P, 'w'), separators=(', ', ': '), ensure_ascii=False)
print('\n'.join(log))
rx = [k for k, v in M.items() if v.get('img') == 'mobimages/review_x.png']
print(f'\nmobs {len(M)}  review_x {len(rx)}  undefined-ref pairs {len(bad)} / names {len(set(a for _,a in bad))}')
