#!/usr/bin/env python3
"""rev 354 — Unknown bucket section 4, fifth batch, from 13 user screenshots.
Author: BalladOfWorms

DET POLICY (rev 350): page notes-column letters REPLACE det; `Blood` survives where
the record already carries it. Absence of BOTH A and NA is an incomplete column, not
a statement — leave `agg` alone in that case (rev 349, bloody skull).
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
    'Treant': ['Drill Branch', 'Entangle', 'Leafstorm', 'Pinecone Bomb'],
    'Rafflesia': ['Bloody Caress', 'Floral Bouquet', 'Rotten Stench', 'Seedspray', 'Viscid Emission'],
    'Ghost': ['Curse', 'Dark Sphere', 'Ectosmash', 'Fear Touch', 'Grave Reel', 'Terror Touch'],
    'Scorpion': ['Cold Breath', 'Critical Bite', 'Death Scissors', 'Earth Pounder', 'Earthbreaker',
                 'Evasion', 'Hell Scissors', 'Mandible Bite', 'Numbing Breath', 'Poison Sting',
                 'Sharp Strike', 'Stasis', 'Venom Breath', 'Venom Sting', 'Venom Storm', 'Wild Rage'],
    'Flytrap': ['Gleosuccus', 'Palsy Pollen', 'Soporific'],
    'Antica': ['Jamming Wave', 'Magnetite Cloud', 'Sand Shield', 'Sand Trap', 'Sand Veil',
               'Sandstorm', 'Shoulder Slam', 'Spikeball'],
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

def stamp(key, fam, kit=True, **kw):
    assert key in m, key
    assert fam in FE, fam
    fill(key, 'fam', fam)
    if kit and fam in KIT:
        fill(key, 'ab', list(KIT[fam]))
    for f, v in kw.items():
        fill(key, f, v)

# ================================================== The Prince and the Hopper toads
# Five identical pages. "Does not use TP Moves or any magic spells" is the Worm
# statement — explicit ab: [] AND sp: [], not a blank to be refilled later.
HOPPER = ['mikilulu', 'mikiluru', 'mikirulu', 'mikiruru', 'nikilulu']
for k in HOPPER:
    stamp(k, 'Frog', crys='Water', spawn='1')
    m[k]['ab'] = []
    m[k]['sp'] = []
    addzone(k, 'Mamook', '50')
    addnotes(k, 'Spawned for the quest The Prince and the Hopper.',
             'Follows and assists Poroggo Casanova.',
             'Does not use TP moves or any magic spells, but has a naturally high rate of attack.')
addnotes('mikilulu', 'Cannot be killed, but can be brought down to 1% HP.')

# ================================================== Voidwatch adds
stamp("modron's druid", 'Treant', spawn='2 per Planar Rift')
addzone("modron's druid", 'The Boyahda Tree', '92-93')
addnotes("modron's druid",
         'Two accompany the Voidwatch notorious monster Modron in The Boyahda Tree, popped from the Planar Rift at (F-7) with an Ashen Stratum Abyssite II and a Voidstone.')

stamp('moly', 'Rafflesia', spawn='2 per rift')
addzone('moly', 'Yuhtunga Jungle')
addnotes('moly', 'Voidwatch notorious monster, Zilart Stage I.',
         'Spawned with an Ashen Stratum Abyssite and a Voidstone at the Planar Rift at (F-11), (G-6) or (J-7). Assists Holy Moly.')

stamp('peon pounder', 'Scorpion', spawn='2 per Malleator Maurok')
addzone('peon pounder', 'Quicksand Caves', '99')
addnotes('peon pounder',
         'Two are summoned during the Voidwatch battle against Malleator Maurok in Quicksand Caves, reached from Western Altepa Desert at (J-9).')

# ================================================== Lebros Cavern assault
# 48 of the 70 Elemental members carry NO `ab` — every base-game-era elemental included.
# The four kits that exist are ELEMENT-SPECIFIC (Baelfyr fire / Gefyrst ice / Ungeweder
# thunder / Byrgen earth) and the modal is the THUNDER pair, which would be flatly wrong
# on a fire elemental. No kit.
stamp('nocuous inferno', 'Elemental', kit=False, job='Black Mage', spawn='8')
det('nocuous inferno', ['Magic'])
addzone('nocuous inferno', 'Lebros Cavern', '75')
addnotes('nocuous inferno',
         'Appears in the Lebros Cavern assault "Better Than One". Sometimes summoned by Black Shuck after it howls.',
         'Casts Flare, Firaga III, Fire IV and Burn.',
         'Highly resistant to Sleep, if not immune.')
skipped.append('nocuous inferno: NO kit — the Elemental modal is the thunder pair and 48 of 70 members have none')

# ================================================== Treasures of the Earth
stamp('otherworldly rimester', 'Ghost', job='Bard', crys='Dark', lv=[109, 135],
      spawn='Spawned for the quest Treasures of the Earth',
      drops="Codex of Etchings, Fiendish Skin, Siren's Hair, Arachne Thread, Khroma Ore, Star Sapphire")
addzone('otherworldly rimester', 'La Theine Plateau', '109')
addzone('otherworldly rimester', 'Konschtat Highlands', '125-135')
addlist('otherworldly rimester', 'sp', 'Victory March', 'Magic Finale', 'Massacre Elegy',
        'Foe Requiem VII', 'Horde Lullaby II')
addnotes('otherworldly rimester',
         'Check the Ergon Locus ??? underneath the Telepoint at the Crag of Holla (K-8) in La Theine Plateau; you lose your Holla crystal of gales.',
         'A solo fight. Geomancer must be your main job to participate. Trusts are allowed, fellows are not. Buffs and TP are reset, and the time limit appears to be 5-10 minutes.',
         'Also drops a pale azure cloth (100%), 10,000 bayld, and at level 135 a random assortment of ten of its listed items.',
         'Uses Dark Sphere, Terror Touch, Fear Touch and Ectosmash.',
         'Particularly weak to magic burst damage \u2014 Fire II from a geomancer deals a consistent 200 without a burst and 9,500 with one; Fire III reaches 13,000 with a burst.',
         'Roughly 12,000 HP at level 135. Its weaknesses shift randomly between elements at level 135.')

# ================================================== Succor to the Sidhe
stamp('pixietrap', 'Flytrap', agg=True, spawn='4')
addzone('pixietrap', 'Jugner Forest [S]')
addnotes('pixietrap', 'Spawned for the quest Succor to the Sidhe.')

# ================================================== Walk of Echoes — When Wills Collide
# Same battlefield and the same lv [84, 84] as `larzos`, stamped last rev.
stamp('portia', 'Humanoid', kit=False, job='Dancer', spawn='1')
addzone('portia', 'Walk of Echoes', '84')
addnotes('portia',
         'Portia Fonteyn, a member of Troupe Mayakov. Fought in the battlefield event When Wills Collide.',
         'Wields daggers and uses dancer job abilities, including Curing Waltz on herself and others. May use Healing Waltz when enfeebled, so kiters should take extra care.',
         'Says "Those who dare oppose Sir Ragelise must answer to me!" before using her two-hour, Melancholy Jig, which inflicts area-of-effect Doom.',
         'Roughly 5,000 HP.')
for a in ['Melancholy Jig', 'Curing Waltz', 'Healing Waltz']:
    if a not in ABIL:
        undef.append('portia: %r not in abilities dict — note only, add to ABIL_WANTED' % a)

# ================================================== Garrison
stamp('princeps xiii-lxxxix', 'Antica', job='Ranger', crys='Dark',
      spawn='Garrison (Eastern Altepa Desert)')
addzone('princeps xiii-lxxxix', 'Eastern Altepa Desert')
addnotes('princeps xiii-lxxxix', 'Drops no gil and cannot be mugged.')

# ================================================== guards + write
assert not [k for r in m.values() for k, v in r.items() if v is None], 'null poison'
bad = [a for r in m.values() for a in (r.get('ab') or []) if a not in ABIL]
assert not ({r.get('fam') for r in m.values() if r.get('fam')} - set(FE))
orph = sum(1 for r in m.values() if not r.get('fam'))
json.dump(d, open(MOBS, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

print('mobs %d  orphans %d  NM-flagged %d' % (len(m), orph, sum(1 for r in m.values() if r.get('nm'))))
print('undefined ability refs: %d uses / %d names' % (len(bad), len(set(bad))))
print('\n--- corrections ---'); [print(' ', x) for x in log]
print('\n--- abilities NOT written ---'); [print(' ', x) for x in undef]
print('\n--- withheld ---'); [print(' ', x) for x in skipped]
print('\n--- fill-only declines ---'); [print(' ', x) for x in declined]
