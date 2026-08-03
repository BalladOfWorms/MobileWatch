import json
d=json.load(open('mobs.json'))
m=d['mobs']; AB=d['abilities']

# ================= ABILITIES =================
AB['Seed of Nihility']={'d':"Deals minor damage to players in range and resets every party member's job-ability recast timers to maximum, including two-hour abilities.",'tgt':'AoE','notes':'Used by Seed Crystal.'}
AB['Seed of Deference']={'d':"Charms players in range, dressing any charmed player in a Mandragora costume.",'tgt':'AoE','fx':['Charm'],'notes':'Used by Seed Crystal.'}
AB['Seed of Deception']={'d':"Clones the targeted player as a 'Seed Thrall' that attacks whoever currently holds hate.",'tgt':'Single','notes':'Used frequently by Seed Crystal.'}
AB['Seed of Judgement']={'d':"A high-damage knockback blast over an area.",'tgt':'AoE','fx':['Knockback'],'notes':'Used by Seed Crystal only below 50% HP.'}
# Replica shared kit
AB['Seismostomp']={'d':"A stomping shockwave that damages nearby players. Additional effect: Stun.",'t':'Physical','tgt':'AoE','fx':['Stun'],'notes':"Used by all Replicas. Absorbed by Utsusemi. As a Replica's HP falls its regain intensifies, so it uses Seismostomp more often and can chain it back-to-back when fed TP by incoming damage."}
AB['Lead Breath']={'d':"A heavy breath striking players in a cone. Additional effect: Weight.",'t':'Breath','el':'Wind','r':'Front cone','tgt':'Cone AoE','fx':['Weight'],'notes':'Used by Quadav-type Replicas.'}
AB['Numbing Glare']={'d':"A paralyzing gaze at a player in front.",'t':'Magical','r':'Frontal gaze','tgt':'Cone AoE','fx':['Paralysis'],'notes':'Used by Orc-type Replicas. A gaze \u2014 avoid by facing away.'}
AB['Tormentful Glare']={'d':"A cursing gaze at a player in front, cutting maximum HP by 10%.",'t':'Magical','r':'Frontal gaze','tgt':'Cone AoE','fx':['Curse'],'notes':'Used by Yagudo-type Replicas. A gaze \u2014 avoid by facing away. Remove Curse with Holy Water or Cursna.'}
AB['Torpid Glare']={'d':"A sleep-inducing gaze at a player in front.",'t':'Magical','r':'Frontal gaze','tgt':'Cone AoE','fx':['Sleep'],'notes':'Used by Goblin-type Replicas. A gaze \u2014 avoid by facing away.'}

def upd(key,**kw):
    v=m[key]
    for k,val in kw.items():
        if val is None: continue
        v[k]=val
    return v

# ================= LIVING CRYSTAL / SEED CRYSTAL =================
d['family_eco']['Living Crystal']='Unclassified'
upd('seed crystal', nm=True, job='Black Mage',
    st=[['Magical','-50%']], wk=[],
    ab=['Draw-In','Seed of Nihility','Seed of Deference','Seed of Deception','Seed of Judgement'],
    sp=['Firaga III','Blizzaga III','Aeroga III','Stonega III','Thundaga III','Waterga III'],
    zones=[['Stellar Fulcrum','']],
    img='mobimages/seed crystal.png',
    notes=["Spawned in the Stellar Fulcrum battlefield Ode of Life Bestowing (Crystalline Prophecy), entered with the Omnis Stone key item. ~25,000 HP with strong physical and magical defense; has Draw-In.",
           "Seed of Deception clones the targeted player as a 'Seed Thrall' that attacks the current hate-holder (used often). Seed of Nihility resets every party member's job-ability recast timers to maximum, including two-hour abilities. Seed of Deference charms and puts victims in a Mandragora costume. Seed of Judgement is a high-damage knockback used only below 50% HP."])

# ================= REPLICA family =================
d['family_eco']['Replica']='Unclassified'
d.setdefault('family_notes',{})['Replica']=[
  "Dynamis 'Replica' constructs \u2014 effigies, idols, tombstones and golems modeled on the Beastmen, found in the Divergence versions of the four original Dynamis zones (and as Prototypes in Dynamis-Tavnazia).",
  "Every Replica uses Seismostomp, plus one signature move set by the Beastman it mimics: Quadav effigies use Lead Breath (Weight), Orc tombstones use Numbing Glare (Paralysis), Yagudo idols use Tormentful Glare (Curse), and Goblin golems use Torpid Glare (Sleep)."
]

# type-move mapping (Dynamis-type rule, confirmed by the detailed pages)
QUADAV=['adamantking effigy','adamantking image','arch gu\u0027dha effigy','gu\u0027dha effigy','mu\u0027sha effigy','effigy prototype']
ORC=['arch overlord tombstone','overlord\u0027s tombstone','overseer\u0027s tombstone','serjeant tombstone','warchief tombstone','tombstone','tombstone prototype']
YAGUDO=['arch tzee xicu idol','tzee xicu idol','avatar idol','evincing idol','avatar icon','manifest icon','icon prototype']
GOBLIN=['arch goblin golem','goblin golem','impish golem','goblin replica','goblin statue','statue prototype']
SPECIAL=['fangmonger colossus']  # Seismostomp only
tmove={}
for k in QUADAV: tmove[k]='Lead Breath'
for k in ORC: tmove[k]='Numbing Glare'
for k in YAGUDO: tmove[k]='Tormentful Glare'
for k in GOBLIN: tmove[k]='Torpid Glare'
allrepl=QUADAV+ORC+YAGUDO+GOBLIN+SPECIAL
assert len(allrepl)==27, len(allrepl)

# uniform family stamp: Seismostomp + type move (fill only where ab empty; detailed ones set explicitly below)
detailed={'evincing idol','mu\u0027sha effigy','overseer\u0027s tombstone','impish golem',
          'arch gu\u0027dha effigy','arch overlord tombstone','arch goblin golem'}
for k in allrepl:
    if k in detailed: continue
    v=m[k]
    kit=['Seismostomp']
    if k in tmove: kit.append(tmove[k])
    if not v.get('ab'):
        v['ab']=kit

# --- DETAILED: Divergence mid-bosses (job Warrior, lv132, Auto-Regain, physical resist) ---
mid={'evincing idol':('Dynamis-Windurst','Tormentful Glare',
        [['Fire','+15%'],['Lightning','+15%'],['Light','+15%'],['Ice','+30%'],['Water','+15%'],['Dark','+15%']],
        [['Breath','-87.5%'],['Impact','-13.5%'],['H2H','-18.75%'],['Piercing','-25%'],['Ranged','-25%'],['Wind','-15%'],['Earth','-15%']]),
     'mu\u0027sha effigy':('Dynamis-Bastok','Lead Breath',
        [['Wind','+15%'],['Lightning','+30%'],['Light','+15%'],['Ice','+15%'],['Earth','+15%'],['Dark','+15%']],
        [['Breath','-87.5%'],['Impact','-13.5%'],['H2H','-18.75%'],['Piercing','-25%'],['Ranged','-25%'],['Fire','-15%'],['Water','-15%']]),
     'overseer\u0027s tombstone':('Dynamis-San d\u0027Oria','Numbing Glare',
        [['Wind','+15%'],['Lightning','+15%'],['Light','+15%'],['Earth','+15%'],['Water','+30%'],['Dark','+15%']],
        [['Breath','-87.5%'],['Impact','-13.5%'],['H2H','-18.75%'],['Piercing','-25%'],['Ranged','-25%'],['Fire','-15%'],['Ice','-15%']]),
     'impish golem':('Dynamis-Jeuno','Torpid Glare',
        [['Fire','+15%'],['Wind','+15%'],['Lightning','+15%'],['Light','+30%'],['Ice','+15%'],['Earth','+15%'],['Water','+15%']],
        [['Breath','-87.5%'],['Impact','-13.5%'],['H2H','-18.75%'],['Piercing','-25%'],['Ranged','-25%'],['Dark','-15%']])}
zt={'Dynamis-Windurst':'Windurst','Dynamis-Bastok':'Bastok','Dynamis-San d\u0027Oria':'San d\u0027Oria','Dynamis-Jeuno':'Jeuno'}
for k,(zone,move,wk,st) in mid.items():
    upd(k, nm=True, job='Warrior', lv=[132,132], wk=wk, st=st,
        ab=['Seismostomp',move],
        zones=[[zone,'132']],
        drops="Beastmen's Medal, Rusted I. Card",
        notes=["Mid-boss of %s (D). Uses only Seismostomp and %s. Innate Auto-Regain that grows stronger as its HP drops, so it fires TP moves more frequently and can chain them back-to-back when fed TP by incoming damage \u2014 have damage dealers sub Ninja to absorb Seismostomp with Utsusemi, and stun to suppress its TP." % (zone.replace('-',' - '), move),
               "Resists physical damage, so skillchains and magic bursts are the fastest kill. Defeating it grants a 30-minute time extension and the title %s [D] Trespasser." % zone.replace('-','-').replace('Dynamis-','Dynamis-')])

# --- DETAILED: Arch reissues (Dynamis reissue NMs) ---
upd('arch gu\u0027dha effigy', nm=True, crys='Water', det=['True Sound'],
    ab=['Seismostomp','Lead Breath','Blood Weapon'],
    zones=[['Dynamis-Bastok','']],
    sp=['Bio III','Death'],
    drops="Oneiros Axe, Oneiros Annulet, Oneiros Barbut",
    notes=["Dynamis-Bastok reissue NM (Quadav effigy). Uses Blood Weapon and back-to-back Seismostomp, and casts dark magic \u2014 Absorb spells, Bio III and Death.",
           "Traded for with Fiendish Tome chapters at the ??? near the South Gustaberg exit (H-10)."])
upd('arch overlord tombstone', nm=True, det=['True Sound'],
    ab=['Seismostomp','Numbing Glare','Hundred Fists'],
    zones=[['Dynamis-San d\u0027Oria','']],
    drops="Oneiros Lance, Oneiros Cest, Oneiros Helm",
    notes=["Dynamis-San d'Oria reissue NM (Orc tombstone). Uses Hundred Fists and has enhanced movement speed; its Seismostomp carries a hate reset.",
           "Traded for with Fiendish Tome chapters at the ??? near the Northern San d'Oria exit (I-7/8)."])
upd('arch goblin golem', nm=True, job='Warrior',
    ab=['Seismostomp','Torpid Glare','Mighty Strikes'],
    zones=[['Dynamis-Jeuno','~100']], lv=[100,100],
    sp=['Holy','Banish IV','Death'],
    drops="Oneiros Knife, Oneiros Grip, Oneiros Coif",
    notes=["Dynamis-Jeuno reissue NM (Goblin golem). Uses Mighty Strikes (gaining triple attack) with Seismostomp for large AoE and can one-shot anyone without shadows \u2014 Sentinel's Scherzo or Earthen Armor recommended. Weak to magic, resistant to physical; not a challenge at item level 119.",
           "Traded for with Fiendish Tome chapters at the ??? near the Upper Jeuno exit (H-10/11). Can drop 0 or all three Oneiros pieces (~50% each with Treasure Hunter 9)."])

json.dump(d, open('mobs.json','w'), separators=(', ', ': '), ensure_ascii=False)

# guards
d2=json.load(open('mobs.json'))
bad=[k for mob in d2['mobs'].values() for k,v in mob.items() if v is None]
assert not bad, ('NULL POISON', bad[:5])
undef=sorted({a for v in d2['mobs'].values() for a in (v.get('ab') or []) if a not in d2['abilities']})
mine=['Seed of Nihility','Seed of Deference','Seed of Deception','Seed of Judgement','Seismostomp','Lead Breath','Numbing Glare','Tormentful Glare','Torpid Glare']
print('abilities:',len(d2['abilities']),'| mobs:',len(d2['mobs']),'| family_eco:',len(d2['family_eco']),'| family_notes:',len(d2.get('family_notes',{})))
print('this-pass undefined refs:',[a for a in undef if a in mine])
print('total undefined refs file-wide:',len(undef))
print('Living Crystal eco:',d2['family_eco'].get('Living Crystal'),'| Replica eco:',d2['family_eco'].get('Replica'))
for k in ['seed crystal','evincing idol','mu\u0027sha effigy','overseer\u0027s tombstone','impish golem','arch goblin golem','tzee xicu idol','goblin statue']:
    v=d2['mobs'][k]; print('  %-20s ab=%s wk=%d st=%d' % (k, v.get('ab'), len(v.get('wk') or []), len(v.get('st') or [])))
