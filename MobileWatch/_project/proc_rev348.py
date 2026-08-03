#!/usr/bin/env python3
"""rev 348 — Unknown bucket section 4, first batch, from 15 user screenshots.
Fill-only unless listed in CORRECTIONS; every decline logged.
Author: BalladOfWorms
"""
import json, os

P = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
MOBS = os.path.join(P, 'mobs.json')
d = json.load(open(MOBS, encoding='utf-8'))
m, ABIL, FE = d['mobs'], d['abilities'], d['family_eco']
log, declined = [], []

ZONES = {z['name'] for z in json.load(open(os.path.join(P, 'zones.json'), encoding='utf-8'))['zones']}
INUSE = {(z[0] if isinstance(z, list) else z) for v in m.values() for z in (v.get('zones') or [])}
def zok(z):
    assert z in ZONES or z in INUSE, 'unknown zone %r' % z
    return z

KIT = {
    'Fomor':      ['Aegis Schism', 'Barbed Crescent', 'Carnal Nightmare', 'Dancing Chains',
                   'Foxfire', 'Grim Halo', 'Netherspikes', 'Shackled Fists'],
    'Skeleton':   ['Black Cloud', 'Blood Saber', 'Hell Slash', 'Horror Cloud'],
    'Crab':       ['Big Scissors', 'Bubble Curtain', 'Bubble Shower', 'Metallic Body', 'Scissor Guard'],
    'Antica':     ['Jamming Wave', 'Magnetite Cloud', 'Sand Shield', 'Sand Trap', 'Sand Veil',
                   'Sandstorm', 'Shoulder Slam', 'Spikeball'],
    'Corpselight': ['Corpse Breath'],
    'Animated Weapon': ['Dire Whorl'],
}
for f, k in KIT.items():
    assert f in FE, f
    for a in k:
        assert a in ABIL, a

def fill(key, field, val):
    r = m[key]
    if r.get(field) in (None, '', [], {}):
        r[field] = val
        return True
    if r[field] != val:
        declined.append('%s.%s kept %r (page said %r)' % (key, field, r[field], val))
    return False

def correct(key, field, val, why):
    log.append('CORRECT %-26s %-5s %r -> %r  [%s]' % (key, field, m[key].get(field), val, why))
    m[key][field] = val

def addzone(key, zone, lvs=None):
    zs = m[key].setdefault('zones', [])
    if zone in {z[0] if isinstance(z, list) else z for z in zs}:
        return
    zs.append([zok(zone), lvs] if lvs else [zok(zone)])

def addnotes(key, *bullets):
    ns = m[key].setdefault('notes', [])
    for b in bullets:
        if b not in ns:
            ns.append(b)

def addlist(key, field, *vals):
    xs = m[key].setdefault(field, [])
    for v in vals:
        if v not in xs:
            xs.append(v)

def addcontent(key, tag):
    have = {t for v in m.values() for t in (v.get('content') or [])}
    assert tag in have, 'new content tag %r' % tag
    addlist(key, 'content', tag)

def stamp(key, fam, kit=True, **kw):
    assert key in m, key
    assert fam in FE, fam
    fill(key, 'fam', fam)
    if kit and fam in KIT:
        fill(key, 'ab', list(KIT[fam]))
    for f, v in kw.items():
        fill(key, f, v)

# ---------------------------------------------------------------- Fomor shadows
# The panel names all four counterparts; `borealis shadow` was already Fomor with
# the full record, so the other three mirror it (rule 295).
for k in ['australis shadow', 'orientalis shadow', 'occidentalis shadow']:
    stamp(k, 'Fomor', nmlv='128',
          spawn='UNM \u2014 Ethereal Junction in FeiYin (I-7), (J-8) or (F-9) with an active Unity Wanted quest')
    addzone(k, 'FeiYin', '128')
    addcontent(k, 'Unity: Wanted: Wanted 2')
    addnotes(k,
             'Four spawn at once \u2014 Borealis Shadow, Australis Shadow, Orientalis Shadow and Occidentalis Shadow \u2014 and all four must be defeated to finish the Unity Wanted objective.',
             'Elvaan types in chainmail, typically found in The Eldieme Necropolis and Fei\u2019Yin.')

# ---------------------------------------------------------------- Voidwatch NMs
stamp('bai hu', 'Tiger', kit=False, lnk=True, spawn='Summoned by Qilin (1 per Qilin)')
m['bai hu']['ab'] = []          # page prints "Special Abilities: N/A" — a statement, not a blank
correct('bai hu', 'det', ['True Sound'], 'notes column reads A, L, T(H)')
addzone('bai hu', 'The Shrine of RuAvitau')
addnotes('bai hu',
         'Voidwatch notorious monster, Zilart Stage III.',
         'Summoned by Qilin, one per Qilin.',
         'Roughly 55,000 HP.',
         'Carries the passive trait Flash Aura. The page lists no TP moves.')

stamp('bisa', 'Skeleton', spawn="Summoned by Uptala's Yaksha Stance (1 per Uptala)")
correct('bisa', 'det', ['True Sound', 'Blood'],
        'notes column reads A, L, T(H); Blood kept — the Skeleton family standard, and the column is not exhaustive')
addzone('bisa', 'VeLugannon Palace')
addnotes('bisa',
         'Voidwatch notorious monster, Jeuno Stage II.',
         "Spawned by Uptala's Yaksha Stance. If defeated, Uptala resummons it the next time it uses Yaksha Stance.")

stamp('bloody skull', 'Corpselight', job='Black Mage', spawn='Summoned by Fjalar (3 per Fjalar)')
correct('bloody skull', 'det', ['True Sound', 'Blood'],
        'notes column reads T(H); Blood kept — undead-family standard')
addzone('bloody skull', 'Attohwa Chasm')
addlist('bloody skull', 'sp', 'Sleep', 'Sleep II', 'Sleepga', 'Sleepga II', 'Ice Spikes',
        'Stun', 'Blind', 'Aero IV', 'Thundaga III', 'Burst', 'Frost', 'Rasp')
addnotes('bloody skull',
         'Voidwatch notorious monster, Tavnazia Stage I.',
         'Spawned by Fjalar, three at a time.',
         'Favours its sleep spells.',
         'Its melee attacks can deal over 300 damage each to a mage.')

# ---------------------------------------------------------------- Assault / FoV
stamp('bloody daggers', 'Animated Weapon', job='Thief', spawn='Summoned by King Goldemar')
correct('bloody daggers', 'det', ['True Sound'], 'notes column reads A, T(H)')
addzone('bloody daggers', 'Periqia')
addnotes('bloody daggers',
         'Summoned by King Goldemar during the Periqia assault "The Price Is Right".',
         'Roughly 3,500 HP.',
         'Has a high rate of Triple Attack, which makes keeping shadows up difficult. An alternative is a Blue Mage running Cocoon and Plasma Charge who tanks them with stun spells such as Head Butt and Frypan.',
         'Uses Dire Whorl with sufficient TP.')

stamp('blue bascinet', 'Crab', job='Paladin, Bard', crys='Water')
addzone('blue bascinet', 'Valkurm Dunes')
addnotes('blue bascinet',
         'Fields of Valor notorious monster. Spawned in Chapter 1 of Elite Training by trading up to 8 Beastmen\u2019s Seals, 400 gil, or up to level-20 equipment to the Field Parchment at (E-7) near the bottom of the rocks \u2014 awarding 600 EXP, 400 gil, or an augment respectively.',
         'Its job is random each time it spawns, either Paladin or Bard.',
         'Can spawn with any elemental enspell, a 6 HP-per-tick enpoison, or an enaspir.',
         'Roughly 471 HP. Soloable by some jobs at level 20, by most at 25.',
         'Uses Metallic Body often.')

# ---------------------------------------------------------------- Antica
stamp('centurio xiii-v', 'Antica', job='Paladin', crys='Dark',
      spawn='Garrison (Eastern Altepa Desert)')
addzone('centurio xiii-v', 'Eastern Altepa Desert')
addnotes('centurio xiii-v', 'Drops no gil and cannot be mugged.')

CONT = {'contantican black mage': ('Black Mage', 'Manafont'),
        'contantican warrior':    ('Warrior', 'Mighty Strikes'),
        'contantican ranger':     ('Ranger', 'Eagle Eye Shot'),
        'contantican paladin':    ('Paladin', 'Invincible')}
for k, (job, twohr) in CONT.items():
    stamp(k, 'Antica', job=job, crys='Dark',
          spawn="Sometimes spawned from a Beastman's Banner during Expeditionary Force")
    correct(k, 'lv', [50, 50], 'page Level column prints 50 (rule 4 — the mob page outranks the zone page)')
    addzone(k, 'Eastern Altepa Desert', '50')
    assert twohr in ABIL
    addlist(k, 'ab', twohr)
    addnotes(k, 'Sometimes spawned from a Beastman\u2019s Banner during Expeditionary Force.',
             'Uses %s at some point.' % twohr)

# ---------------------------------------------------------------- Chebukki siblings
for k in ['cherukiki', 'kukki-chebukki', 'makki-chebukki']:
    stamp(k, 'Humanoid', kit=False, lnk=True)
    correct(k, 'det', ['True Sight'], 'notes column reads L, T(S)')
    correct(k, 'lv', [66, 68], 'page Level column prints ~66-68')
    addzone(k, 'Sealions Den', '66-68')
    addnotes(k,
             'Mission boss. Assists Tenzen in battle during The Warrior\u2019s Path; the siblings take no action until Tenzen is engaged.',
             'None of the three Chebukki siblings can be hurt by players \u2014 they evade or resist every attack \u2014 but they can still deal damage.')
fill('cherukiki', 'job', 'White Mage')

# ---------------------------------------------------------------- Geas Fete
stamp("amymone's peapuk", 'Puk', kit=False,
      spawn="Summoned by Amymone when its HP drops below 50%, or by specific spell triggers")
addzone("amymone's peapuk", 'Escha RuAun')
addcontent("amymone's peapuk", 'Geas Fete: Escha RuAun: Tier 2')
addnotes("amymone's peapuk",
         'A minion of the Geas Fete notorious monster Amymone in Escha - Ru\u2019Aun.',
         'Up to three can be active at once. Left unprovoked they target whoever popped the notorious monster, and they can be slept.',
         'Standard crowd control handles them while the main hydra is burned down.')

# `alpluachra bucca and puca` was already Pixie — the page adds the level and the flags
fill('alpluachra bucca and puca', 'lv', [135, 135])
fill('alpluachra bucca and puca', 'nm', True)
fill('alpluachra bucca and puca', 'agg', True)

# ---------------------------------------------------------------- no family, zone only
addzone("assassin's apprentice", 'Arrapago Reef')
addnotes("assassin's apprentice",
         'A pet/minion tied to the Voidwatch Tier 1 target Dimgruzub in Arrapago Reef.',
         'Uses a low-delay cleave-type normal attack that can stun its target.')

# ---------------------------------------------------------------- guards + write
assert not [k for r in m.values() for k, v in r.items() if v is None], 'null poison'
bad = [a for r in m.values() for a in (r.get('ab') or []) if a not in ABIL]
assert not ({r.get('fam') for r in m.values() if r.get('fam')} - set(FE))
orph = sum(1 for r in m.values() if not r.get('fam'))
json.dump(d, open(MOBS, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

print('mobs %d  orphans %d  NM-flagged %d' % (len(m), orph, sum(1 for r in m.values() if r.get('nm'))))
print('undefined ability refs: %d uses / %d names' % (len(bad), len(set(bad))))
print('\n--- corrections ---'); [print(' ', x) for x in log]
print('\n--- fill-only declines ---'); [print(' ', x) for x in declined]
