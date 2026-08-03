# rev 367 — Section X batch 17: 15 records / 9 families (the tail continues)
# BalladOfWorms
import json, collections, copy

P = '/home/claude/android/app/src/main/assets/mobs.json'
d = json.load(open(P)); M = d['mobs']; AB = d['abilities']
def gk(v): return json.dumps([v.get('wk'), v.get('st')], ensure_ascii=False)
def mode_grid(f):
    c = collections.Counter(gk(v) for v in M.values() if v.get('fam') == f)
    wk, st = json.loads(c.most_common(1)[0][0]); return copy.deepcopy(wk), copy.deepcopy(st)
def mode_field(f, k):
    c = collections.Counter(json.dumps(v[k], ensure_ascii=False) for v in M.values()
                            if v.get('fam') == f and v.get(k))
    return json.loads(c.most_common(1)[0][0]) if c else None
log = []
def S(key, field, val, why):
    old = M[key].get(field); M[key][field] = val
    log.append(f'  {key}: {field} {json.dumps(old,ensure_ascii=False)[:52]} -> {json.dumps(val,ensure_ascii=False)[:72]}  [{why}]')
def D(key, field, why):
    if field in M[key]:
        log.append(f'  {key}: REMOVED {field} ({json.dumps(M[key].pop(field),ensure_ascii=False)[:40]})  [{why}]')
def fam_stamp(key, grid=None, crys=None, job=None, det=None, kit=None):
    v = M[key]; f = v['fam']
    if grid == 'family':
        wk, st = mode_grid(f); S(key,'wk',wk,'family grid'); S(key,'st',st,'family grid')
    if crys and not v.get('crys'): S(key,'crys',crys,'crystal')
    if job and not v.get('job'):   S(key,'job',job,'job')
    if det:                        S(key,'det',det,'detection')
    if kit is not None and not v.get('ab'): S(key,'ab',kit,'kit')

# ---- 1 ravager chariot (BG page) --------------------------------------------
log.append('== ravager chariot (BG page — Crystal: None, stated)')
fam_stamp('ravager chariot', job='Warrior', kit=mode_field('Chariot','ab'))
S('ravager chariot','notes',['Spawns during Bastion; only aggressive to players with Pennant status.',
   '2-3 spawn per Bastion.','The page states Crystal: None — Bastion Chariots drop no crystal.'],'page')
S('ravager chariot','spawn','Bastion','page')

# ---- 2 flitting bee (AI panel) ----------------------------------------------
log.append('== flitting bee (AI panel)')
fam_stamp('flitting bee', grid='family', crys='Wind', job='Warrior',
          det=['Sight'], kit=mode_field('Bee','ab'))
S('flitting bee','zones',[['Sih Gates','119-122']],'panel')
S('flitting bee','drops','S. Kindred Crest','panel (Beehive Chip / Pot of Honey / Insect Wing omitted as craft mats)')

# ---- 3 chary apkallu (BG page) ----------------------------------------------
log.append('== chary apkallu (BG page)')
fam_stamp('chary apkallu', crys='Water', job='Monk', kit=mode_field('Apkallu','ab'))
S('chary apkallu','im',['Sleep','Gravity','Bind'],'page')
S('chary apkallu','zones',[['Mount Zhayolm','76-77']],'page')
S('chary apkallu','notes',['Roughly 10,000-11,000 HP. Spawns at (K-8) near the shore.',
   'Uses Wing Slap and Yawn.','Does not aggro, and will not link to the other Apkallu in the area.',
   'Susceptible to Paralyze, Blind, Poison and Slow.','Has an innate Enwater effect on its melee attacks.'],'page')

# ---- 4 warder's wynav (AI panel) --------------------------------------------
log.append("== warder's wynav (AI panel)")
S("warder's wynav",'ab',['Mijin Gakure'],'panel names it; Wynav has no family kit (rule 346)')
S("warder's wynav",'sp',['Dispel','Sleepga II','Flash','Banishga III'],'panel (day-dependent examples)')
S("warder's wynav",'zones',[['Escha RuAun']],'panel')
S("warder's wynav",'content',['Geas Fete: Escha RuAun: Nazar'],'copied from warder of courage')
S("warder's wynav",'spawn','Geas Fete (Warder of Courage, via Call Wyvern)','panel')
S("warder's wynav",'notes',['Called by the Warder of Courage with Call Wyvern, in sets of 3 or 6.',
   'Roughly 12,000 HP each, with high magic defence.',
   'Casts tier-IV and -ga III spells matching the current in-game day — Dispel and Sleepga II on Darksday, Flash and Banishga III on Lightsday.',
   'Mimics the boss\u2019s moves and answers Astral Flow with breath attacks.'],'panel')

# ---- 5 eschan il'aern's wynav (AI panel) ------------------------------------
log.append("== eschan il'aern's wynav (AI panel)")
S("eschan il'aern's wynav",'zones',[['Escha RuAun','116']],'panel')
S("eschan il'aern's wynav",'spawn',"Add of Eschan Il'aern",'panel')
S("eschan il'aern's wynav",'notes',['A minor add tied to the Il\u2019aern of the area; uses the classic Wynav (wyvern) model carried by dragoon-type Aerns.',
   'Wynavs act as helper entities or companion pets \u2014 the same role as the Bard helpers summoned by dragoon-type Ix\u2019aern.'],'panel')

# ---- 6 patrol worm (BG page — Campaign Battle NPC) --------------------------
log.append('== patrol worm (BG page — Type: Campaign Battle NPC)')
fam_stamp('patrol worm', grid='family', crys='Earth', job='Black Mage', kit=mode_field('Worm','ab'))
S('patrol worm','zones',[['Fort Karugo-Narugo [S]']],'page Location')
S('patrol worm','spawn','Campaign Battle','page')
S('patrol worm','notes',['Appears during Campaign Battles as a squadron of Nyumomo pets, on the Windurst [S] side.',
   'They do not move, but spawn around Nyumomo periodically.',
   'Devastates enemy forces with high-tier earth elemental spells, usually cast in unison.'],'page')

# ---- 7 midnight worm (AI panel) ---------------------------------------------
log.append('== midnight worm (AI panel)')
D('midnight worm','agg','panel states Behavior: Passive')
fam_stamp('midnight worm', grid='family', crys='Earth', job='Black Mage',
          det=['Sound'], kit=mode_field('Worm','ab'))

# ---- 8 snowpelt rabbit (BG page) --------------------------------------------
log.append('== snowpelt rabbit (BG page)')
fam_stamp('snowpelt rabbit', crys='Earth', job='Warrior', det=['Sight'], kit=mode_field('Rabbit','ab'))
S('snowpelt rabbit','notes',['Records of Eminence: Combat Adoulin / Conflict 1 target at Kamihr Drifts #2 (H-10).'],'page footnote')

# ---- 9 snowpaw rabbit (AI panel) --------------------------------------------
log.append('== snowpaw rabbit (AI panel)')
D('snowpaw rabbit','agg','panel: passive toward players, unlike the Snowpelt Rabbit')
fam_stamp('snowpaw rabbit', crys='Earth', job='Warrior', kit=mode_field('Rabbit','ab'))
S('snowpaw rabbit','spawn','Lair Reive (Kamihr Drifts)','panel')
S('snowpaw rabbit','notes',['Appears as part of Lair Reives, around (I-11) in Kamihr Drifts.',
   'Passive toward players, unlike the aggressive Snowpelt Rabbit that shares the region.'],'panel')

# ---- 10/11 sharptusk + famished raaz (BG pages) -----------------------------
for k, place, reive in [('sharptusk raaz','the Icy Palisades','Colonization Reives'),
                        ('famished raaz','the Wintry Caves','Lair Reives')]:
    log.append(f'== {k} (BG page)')
    fam_stamp(k, grid='family', crys='Earth', job='Monk',
              det=['Sight','Sound'], kit=mode_field('Raaz','ab'))
    S(k,'zones',[['Kamihr Drifts']],'page')
    S(k,'spawn',f'{reive[:-1]} (Kamihr Drifts)','page note')
    S(k,'notes',[f'Defends {place} in certain Kamihr Drifts {reive}.',
                 'Aggressive to Reive participants only (A(R)).','Drops and steals nothing.'],'page')

# ---- 12 orobon (BG page) -----------------------------------------------------
log.append('== orobon (BG page)')
fam_stamp('orobon', grid='family', crys='Water', job='Warrior', kit=mode_field('Orobon','ab'))
S('orobon','zones',[['Ilrusi Atoll'],['Silver Sea route to Al Zahbi'],
                    ['Silver Sea route to Nashmau','75-'],['Arrapago Remnants']],'page')
S('orobon','drops','Orobon Lure, Ahtapot, Cumulus Cell, Radiatus Cell','page')
S('orobon','notes',['Fished up — a minnow lure works at any Fishing skill level.',
   'In Arrapago Remnants it is spawned by the Archaic Rampart on the 5th floor.',
   'In Desperately Seeking Cephalopods the Ahtapot goes automatically to whoever lands the killing blow.'],'page')

# ---- 13 giant orobon (BG page) ----------------------------------------------
log.append('== giant orobon (BG page)')
fam_stamp('giant orobon', grid='family', crys='Water', job='Warrior', kit=mode_field('Orobon','ab'))
S('giant orobon','nm',True,'page red banner')
S('giant orobon','nmlv','78-83','page')
S('giant orobon','zones',[['Arrapago Reef','78-83'],['Mount Zhayolm','78-83'],['Talacca Cove','78-83']],'page')
S('giant orobon','notes',['Fished up in three separate zones: Talacca Cove, Arrapago Reef and Mount Zhayolm.',
   'Has access to the full Orobon family kit and good evasion.',
   'Double, and possibly triple, attack — Utsusemi shadows drop fast.'],'page')

# ---- 14 mimic jester (AI panel) ---------------------------------------------
log.append('== mimic jester (AI panel)')
fam_stamp('mimic jester', crys='Light', job='Black Mage', det=['Sound','Magic'])
S('mimic jester','ab',['Death Trap'],'panel: "exclusively uses the Death Trap ability" — the trim rule')
S('mimic jester','zones',[['RoMaeve','90-91']],'panel + mimic king')
S('mimic jester','spawn','Voidwatch add of Mimic King','panel')
S('mimic jester','notes',['Spawns alongside the Mimic King and fires Death Trap at the exact moment the King uses a TP move.',
   'Death Trap is a 20\u2032 area-of-effect Stun and Poison that bypasses shadow images.',
   'Never moves from its spawn point, so melee can stand clear of it.',
   'Does not respawn once defeated — kill it early.'],'panel')

# ---- 15 mimic mage (USER: no info, just add to the Mimic family) ------------
log.append('== mimic mage (USER: "no info, just add to mimic family")')
fam_stamp('mimic mage', crys='Light', job='Black Mage', det=['Sound','Magic'],
          kit=mode_field('Mimic','ab'))

# ---- clear the red X ---------------------------------------------------------
CLEARED = ['ravager chariot','flitting bee','chary apkallu',"warder's wynav",
           "eschan il'aern's wynav",'patrol worm','midnight worm','snowpelt rabbit',
           'snowpaw rabbit','sharptusk raaz','famished raaz','orobon','giant orobon',
           'mimic jester','mimic mage']
for k in CLEARED:
    if M[k].get('img') == 'mobimages/review_x.png': M[k].pop('img')
log.append(f'== review_x cleared on {len(CLEARED)} records')

# ---- guards ------------------------------------------------------------------
assert not [k for m in M.values() for k, v in m.items() if v is None], 'null poison'
bad = [(k,a) for k,v in M.items() for a in (v.get('ab') or []) if a not in AB]
assert not [x for x in bad if x[0] in CLEARED], f'undefined refs introduced: {[x for x in bad if x[0] in CLEARED]}'
json.dump(d, open(P,'w'), separators=(', ', ': '), ensure_ascii=False)
print('\n'.join(log))
rx=[k for k,v in M.items() if v.get('img')=='mobimages/review_x.png']
print(f'\nmobs {len(M)}  review_x {len(rx)}  NM {sum(1 for v in M.values() if v.get("nm"))}  undefined {len(bad)}/{len(set(a for _,a in bad))}')
