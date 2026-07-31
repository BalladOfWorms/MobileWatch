#!/usr/bin/env python3
"""rev 352 — Unknown bucket section 4, fourth batch, from 11 user screenshots.
User named the four untitled pages, in screenshot order: lilisette, kukki, lion, makki.
Author: BalladOfWorms

DET POLICY (rev 350): the page's notes-column letters REPLACE det; `Blood` survives
where the record already carries it. Everything else the page omits is dropped.
"""
import json, os

P = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
MOBS = os.path.join(P, 'mobs.json')
d = json.load(open(MOBS, encoding='utf-8'))
m, ABIL, FE = d['mobs'], d['abilities'], d['family_eco']
log, declined, undef, skipped = [], [], [], []

ZONES = {z['name'] for z in json.load(open(os.path.join(P, 'zones.json'), encoding='utf-8'))['zones']}
INUSE = {(z[0] if isinstance(z, list) else z) for v in m.values() for z in (v.get('zones') or [])}
def zok(z):
    assert z in ZONES or z in INUSE, 'unknown zone %r' % z
    return z

KIT = {
    'Crab': ['Big Scissors', 'Bubble Curtain', 'Bubble Shower', 'Metallic Body', 'Scissor Guard'],
    'Dragon': ['Body Slam', 'Chaos Blade', 'Flame Breath', 'Heavy Stomp', 'Lodesong',
               'Petro Eyes', 'Poison Breath', 'Thornsong', 'Voidsong', 'Wind Breath'],
    'Fomor': ['Aegis Schism', 'Barbed Crescent', 'Carnal Nightmare', 'Dancing Chains',
              'Foxfire', 'Grim Halo', 'Netherspikes', 'Shackled Fists'],
    'Orc': ['Aerial Wheel', 'Armblock', 'Battle Dance', 'Howl', 'Shoulder Attack',
            'Slam Dunk', 'Veil of Chaos'],
    'Evil Weapon': ['Flurry of Rage', 'Smite of Fury', 'Smite of Rage', 'Whirl of Rage',
                    'Whispers of Ire'],
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

def det(key, letters):
    cur = m[key].get('det') or []
    new = list(letters) + (['Blood'] if 'Blood' in cur and 'Blood' not in letters else [])
    if new != cur:
        log.append('CORRECT %-22s det %r -> %r' % (key, cur, new))
        m[key]['det'] = new

def addzone(key, zone, lvs=None):
    zs = m[key].setdefault('zones', [])
    if zone in {z[0] if isinstance(z, list) else z for z in zs}:
        return
    zs.append([zok(zone), lvs] if lvs else [zok(zone)])

def addnotes(key, *bs):
    ns = m[key].setdefault('notes', [])
    for b in bs:
        if b not in ns:
            ns.append(b)

def addlist(key, field, *vals):
    xs = m[key].setdefault(field, [])
    for v in vals:
        if v not in xs:
            xs.append(v)

def addab(key, *names):
    for a in names:
        if a in ABIL:
            addlist(key, 'ab', a)
        else:
            undef.append('%s: %r not in abilities dict — note only' % (key, a))

def stamp(key, fam, kit=True, **kw):
    assert key in m, key
    assert fam in FE, fam
    fill(key, 'fam', fam)
    if kit and fam in KIT:
        fill(key, 'ab', list(KIT[fam]))
    for f, v in kw.items():
        fill(key, f, v)

# ===================================================== Tangaroa's three adds
# The panel names all three by family. `tangaroa` is Uragnite in Kuftal Tunnel 96-97;
# koura / pekapeka / moki are all lv [92, 93] orphans — one page, three records.
ADDS = {'koura': ('Crab', 'a crab'), 'pekapeka': ('Sea Monk', 'a seamonk'), 'moki': ('Pugil', 'a pugil')}
for k, (fam, what) in ADDS.items():
    stamp(k, fam)
    addzone(k, 'Kuftal Tunnel', '92-93')
    addnotes(k,
             'Summoned as %s when the Voidwatch notorious monster Tangaroa is engaged, alongside Koura (a crab), Pekapeka (a seamonk) and Moki (a pugil).' % what,
             'The helpers reappear whenever Tangaroa retreats into its shell.',
             'Pekapeka is the more dangerous heavy hitter with area-of-effect damage; Koura is the crustacean minion supporting the encounter.')
addnotes('koura', 'The name also covers the native crab mobs found inside Kuftal Tunnel.')

# ===================================================== Fields of Valor
# BG "Dragons" -> our Dragon. Its page names NINE of the ten modal moves as "attack modes".
stamp('kulili', 'Dragon', job='Warrior')
addzone('kulili', 'Xarcabard')
addnotes('kulili',
         'Fields of Valor notorious monster. Spawns at the Field Parchment at (H-9) after obtaining a Chapter 4 Elite Training key item from the Field Manual, then trading up to 900 gil, up to 18 Beastmen\u2019s Seals, or a level-45 item or under.',
         'Roughly 2,000-2,500 HP and no MP. Drops no gil and cannot be mugged.',
         'Appears to pick about three TP moves per fight and stick to them, described as five "attack modes": Wind Breath; Thornsong, Voidsong and Chaos Blade; Heavy Stomp and Body Slam; Petro Eyes; Lodesong. Flame Breath has also been seen. What causes a mode, or whether it can be changed, is unknown.',
         'Carries an en-effect that seems to change \u2014 Endrain, Enpoison, Enstone, Enaero, Enwater, Enthunder, Enblizzard and Enaspir have all been seen.',
         'Ice damage heals it: Blizzard IV healed it for 1,024 HP, and it may have a random element that heals it. Bind works.',
         'May be able to intimidate players, sometimes has an auto-regen, has a very high level of accuracy, and its Petro Eyes can last an incredibly long time.')

# BG "Weapons" -> our Evil Weapon. The page names Whispers of Ire and Flurry of Rage,
# both of which sit in the Evil Weapon modal kit — the moves confirm the family, not just the word.
stamp('malefic fencer', 'Evil Weapon', job='Red Mage')
addzone('malefic fencer', 'Qufim Island')
addnotes('malefic fencer',
         'Fields of Valor notorious monster, spawned by the Field Parchment at (F-5). Roughly 820 HP.',
         'Begins the fight with several buffs already up, including Enblizzard and Stoneskin.',
         'Every melee attack carries an additional effect \u2014 Blizzard, Thunder or Poison.',
         'Tries to Cure III itself at low HP and casts multiple Red Magic spells.',
         'Absorbs and heals from lightning spells, and may favour lightning-related augments.',
         'Soloable by most jobs at 40+.')

# ===================================================== Periqia assault, the last two
GOLD = {'living staves': ('Black Mage', 'Casts various black magic spells.'),
        'magic shields': ('Paladin', 'Does not melee, but uses Shield Bash constantly.')}
for k, (job, quirk) in GOLD.items():
    stamp(k, 'Animated Weapon', job=job, agg=True, spawn='Summoned by King Goldemar')
    det(k, ['True Sound'])
    addzone(k, 'Periqia')
    addnotes(k, 'Summoned by King Goldemar during the Periqia assault "The Price Is Right".',
             'Roughly 3,500 HP.', quirk, 'Uses Dire Whorl with sufficient TP.')

# ===================================================== Vunkerl Inlet [S]
stamp('madthrasher zradbodd', 'Orc', job='Black Mage, Red Mage', crys='Fire',
      spawn='Spawned at the Underbrush at (F-13) for the quest The Price of Valor')
det('madthrasher zradbodd', ['True Sight', 'Scent'])
addzone('madthrasher zradbodd', 'Vunkerl Inlet [S]')
addab('madthrasher zradbodd', 'Berserker Dance')
addnotes('madthrasher zradbodd', 'Roughly 11,000 HP.',
         'Normally casts tier IV magic and tier III -aga spells for around 900 damage. Tier IV spells are absorbed by shadows, and the tier III -agas can easily be stunned.',
         'After using Berserker Dance it gains a large amount of Fast Cast, close to Chainspell, and starts casting Dispelga, Blindga and Sleepga II \u2014 but stops using tier III -agas for the duration.',
         'Its melee attacks carry a very potent additional effect, Curse, which halves both MP and HP.',
         'Slow and Paralyze land easily.')

# ===================================================== Walk of Echoes
stamp('larzos', 'Fomor', job='Monk', crys='Dark')
addzone('larzos', 'Walk of Echoes', '84')
addab('larzos', 'Hundred Fists', 'Cataclysm', 'Forlorn Impact')
addnotes('larzos',
         'One of Lady Lilith\u2019s Spitewardens alongside Aquila and Haudrale, and commander of the "Bismuth Musketeers". Appears to be a galkan fomor.',
         'Appears in the battlefield event When Wills Collide. Roughly 9,000 HP.',
         'Uses a staff, and favours Cataclysm when it has TP for strong area-of-effect dark damage.',
         'Uses Hundred Fists at around 50% health, and can easily be bound while it is up.',
         'Forlorn Impact deals moderate radial area-of-effect damage with knockback and paralysis.')

# ===================================================== Nyzul Isle, Heroines' Holdfast
stamp('lilisette', 'Humanoid', kit=False, job='Dancer', agg=True, spawn='2')
addzone('lilisette', 'Nyzul Isle')
addnotes('lilisette', 'Fought in Nyzul Isle for Heroines\u2019 Holdfast.',
         'Uses standard dancer abilities including repeated Trances, and spams area-of-effect dispels.',
         'Sensual Dance gives an attack bonus for Lilisette and an attack down for its targets; Thorned Stance gives it a defense and magic defense bonus; Vivifying Waltz heals it; Whirling Edge and Dancer\u2019s Fury deal damage.',
         'At 50-25% health it splits into two. Both Lilisettes share a single HP bar, but only one can be damaged at a time, which makes holding hate a challenge.')

stamp('lion', 'Humanoid', kit=False, job='Thief', agg=True, spawn='1')
addzone('lion', 'Nyzul Isle')
addnotes('lion', 'Fought in Nyzul Isle for Heroines\u2019 Holdfast.',
         'Weapon skills: Pirate Pummel, single-target damage with a high damage-over-time Burn; Powder Keg, conal damage with defense and magic defense down; Grapeshot, conal damage and stun.',
         'Walk the Plank is used only at low HP after being prompted by Gilgamesh \u2014 area-of-effect damage with knockback, bind and dispel.')

# ===================================================== Chebukki siblings, filled in
fill('kukki-chebukki', 'job', 'Black Mage, Red Mage')
addlist('kukki-chebukki', 'sp', 'Blind', 'Stun')
fill('makki-chebukki', 'job', 'Ranger')

skipped.append("prishe: same Master Trials tag as lilisette/lion, still fam=None \u2014 no page this batch")
skipped.append("aquila / haudrale: named as Larzos's fellow Spitewardens but neither is in the file")

# ===================================================== guards + write
assert not [k for r in m.values() for k, v in r.items() if v is None], 'null poison'
bad = [a for r in m.values() for a in (r.get('ab') or []) if a not in ABIL]
assert not ({r.get('fam') for r in m.values() if r.get('fam')} - set(FE))
orph = sum(1 for r in m.values() if not r.get('fam'))
json.dump(d, open(MOBS, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

print('mobs %d  orphans %d  NM-flagged %d' % (len(m), orph, sum(1 for r in m.values() if r.get('nm'))))
print('undefined ability refs: %d uses / %d names' % (len(bad), len(set(bad))))
print('\n--- corrections ---'); [print(' ', x) for x in log]
print('\n--- abilities NOT written (undefined) ---'); [print(' ', x) for x in undef]
print('\n--- deliberately withheld ---'); [print(' ', x) for x in skipped]
print('\n--- fill-only declines ---'); [print(' ', x) for x in declined]
