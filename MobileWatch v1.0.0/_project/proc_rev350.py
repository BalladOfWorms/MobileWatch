#!/usr/bin/env python3
"""rev 350 — Unknown bucket section 4, third batch, from 12 user screenshots.
Author: BalladOfWorms

DET POLICY, settled this rev: the page's notes-column letters REPLACE det, with one
carve-out — `Blood` survives where the record already carries it, because HP is the
flag editors most often omit and 510 records file-wide have it. Everything else the
page does not print is dropped.
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
    'Gallu': ['Bolt of Perdition', 'Crippling Rime', 'Diluvial Wake', 'Divesting Gale',
              'Kurnugi Collapse', "Oblivion's Mantle", 'Searing Halitus'],
    'Lesser Bird': ['Blindside Barrage', 'Broadside Barrage', 'Damnation Dive', 'Helldive', 'Wing Cutter'],
    'Coeurl': ['Blaster', 'Blink of Peril', 'Chaotic Eye', 'Charged Whisker', 'Frenzied Rage',
               'Mortal Blast', 'Petrifactive Breath', 'Pounce', 'Preternatural Gleam'],
    'Hippogryph': ['Back Heel', 'Choke Breath', 'Fantod', 'Hoof Volley', 'Jettatura', 'Nihility Song'],
    'Fomor': ['Aegis Schism', 'Barbed Crescent', 'Carnal Nightmare', 'Dancing Chains',
              'Foxfire', 'Grim Halo', 'Netherspikes', 'Shackled Fists'],
    'Gigas': ['Catapult', 'Colossal Blow', 'Grand Slam', 'Ice Roar', 'Impact Roar',
              'Lightning Roar', 'Mercurial Strike', 'Moribund Hack', 'Power Attack', 'Trebuchet'],
    'Wamoura': ['Erosion Dust', 'Erratic Flutter', 'Exuviation', 'Fire Break', 'Magma Fan', 'Proboscis'],
    'Cockatrice': ['Baleful Gaze', 'Contagion Transfer', 'Contamination', 'Hammer Beak',
                   'Poison Pick', 'Sound Blast', 'Sound Vacuum', 'Toxic Pick'],
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
    """page letters replace det; Blood survives if already present"""
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

# ------------------------------------------------------- Walk of Echoes pair
stamp('gloomtalon', 'Gallu')
addzone('gloomtalon', 'Walk of Echoes')
addnotes('gloomtalon',
         'Encountered during the quest A Forbidden Reunion in the Walk of Echoes, fought alongside Gloomscale.',
         'You fight alongside Lilisette, who must stay alive to achieve victory.',
         'Cursna does not work during this encounter \u2014 bring Holy Water to manage status ailments.')
# gloomscale's panel calls it a "Zilart-type monster" and there is no such family
addzone('gloomscale', 'Walk of Echoes')
addnotes('gloomscale',
         'Fought alongside Gloomtalon during the quest A Forbidden Reunion in the Walk of Echoes.',
         'You fight alongside Lilisette, who must stay alive to achieve victory.',
         'Cursna does not work during this encounter \u2014 bring Holy Water to manage status ailments.')
skipped.append('gloomscale: panel says "Zilart-type", which is not a family we hold \u2014 zone + notes only')

# ------------------------------------------------------- Succor to the Sidhe
stamp('gorebeak', 'Lesser Bird', agg=True, spawn='4')
addzone('gorebeak', 'Sauromugue Champaign [S]')
addnotes('gorebeak', 'Spawned for the quest Succor to the Sidhe.')

stamp('jotunn ruffian', 'Gigas', job='Monk', spawn='6')
det('jotunn ruffian', ['True Sight'])
addzone('jotunn ruffian', 'Vunkerl Inlet [S]')
addnotes('jotunn ruffian', 'Spawns with Procrustes.')

# ------------------------------------------------------- Voidwatch
stamp('grwnan', 'Coeurl', spawn='2 per Planar Rift')
addzone('grwnan', 'The Sanctuary of ZiTah')
addnotes('grwnan',
         'Two Grwnan automatically assist the Voidwatch notorious monster Cath Palug when the battle is triggered from the Planar Rift at (E-9), (F-8) or (G-10) with a Voidstone and an Ashen Stratum Abyssite II.',
         'The name comes from a Welsh word meaning "purr".')

stamp('kalos eunomia', 'Wamoura',
      spawn='The evolved form of Nympha Eunomia \u2014 spawns roughly 10 seconds after it is killed',
      drops='Magma Gauntlets, Wamoura Hair, Silver Mirror, Petrified Log, Ebony Log, Mahogany Log, Darksteel Ore, Mythril Ore, Adaman Ore')
det('kalos eunomia', ['True Sound'])
addzone('kalos eunomia', 'Crawlers Nest [S]')
addlist('kalos eunomia', 'sp', 'Firaja')
addnotes('kalos eunomia', 'Voidwatch notorious monster, Jeuno Stage II.',
         'Also drops level 91-95 spell scrolls and the Vivid Periapt of Concord key item.',
         'Exuviation converts its current debuffs into instant HP. Very short cast time, and it is used multiple times above 50% until it is back to full health.',
         'Passively absorbs all debuffs and damage-over-time and turns them into HP for itself.',
         'Carries an Addle aura with a very wide, roughly 20-yalm range.',
         'Susceptible to Paralyze under Elemental Seal, and otherwise resists the spell. Resists Slow.')

# ------------------------------------------------------- Ra'Kaznar reives
stamp('heliotrope barrier', 'Obstacle', spawn='Colonization Reive (3 per Reive).')
addzone('heliotrope barrier', 'RaKaznar Inner Court')
addnotes('heliotrope barrier',
         'If all targets are defeated the barrier vanishes, allowing passage.',
         'Can be fought during Colonization Reives.',
         'Cannot be damaged without the "Pulverizing" key item.')

stamp('indomitable spurned', 'Fomor', job='Ninja')
addzone('indomitable spurned', 'RaKaznar Inner Court')
addnotes('indomitable spurned',
         'Guards the Heliotrope Barriers in certain Colonization Reives in Ra\u2019Kaznar Inner Court.',
         'Aggressive to Reive participants only.')

# ------------------------------------------------------- Yorcia Weald
stamp('inquisitor mortuus', 'Fomor', job='Ranger',
      spawn='Spawns for the quest A Thirst Before Time',
      drops='Weathered Haverton Hat')
det('inquisitor mortuus', ['True Sound'])
addzone('inquisitor mortuus', 'Yorcia Weald', '115')
addnotes('inquisitor mortuus',
         'Found at (I-10). Before his death he was Margret\u2019s former mentor, Celdricaste.',
         'As his HP dwindles he counts down \u2014 "Ten\u2026" then "Three\u2026" "Two\u2026" "One\u2026" \u2014 before using Eagle Eye Shot, which is strong enough to kill the trust August instantly.')

# ------------------------------------------------------- Grauberg [S]
stamp('hippocentaur', 'Hippogryph', job='Thief', spawn='6')
addzone('hippocentaur', 'Grauberg [S]')
addnotes('hippocentaur', 'Spawns with Simorg.',
         'Has high evasion \u2014 accuracy food is recommended.')

# ------------------------------------------------------- Odyssey-shaped, zone withheld
# The page's zone is "Veridical Conflux 4", which is not in zones.json and is used by no
# other record. Writing it would create a 22nd free-text instanced zone; it goes in notes
# until the free-text-zone open item is settled.
stamp('harpimaira', 'Khimaira', kit=False)
fill('harpimaira', 'ab', ['Dreadstorm', 'Fossilizing Breath', 'Fulmination',
                          'Tenebrous Mist', 'Thunderstrike', 'Tourbillion'])
det('harpimaira', ['True Sight', 'True Sound'])
fill('harpimaira', 'spawn', '5')
addnotes('harpimaira', 'Listed on Veridical Conflux 4. Drops and steal are both None.')
skipped.append('harpimaira: zone "Veridical Conflux 4" NOT written \u2014 not in zones.json, used by no record')

# ------------------------------------------------------- no family named
addzone('kanavid', 'Sea Serpent Grotto')
addcontent('kanavid', 'Unity: Wanted: Wanted 2')
addnotes('kanavid',
         'An add that assists the Unity Wanted notorious monster Bakunawa on map 4 of Sea Serpent Grotto, spawned from an Ethereal Junction at (J-8), (I-10) or (D-9).',
         'Two spawn alongside Bakunawa. They actively target whoever triggered the notorious monster and respawn quickly if defeated during the fight.')
skipped.append('kanavid: the panel names no family \u2014 zone, content tag and notes only')

# ------------------------------------------------------- Fields of Valor
stamp('kaneakeluh', 'Cockatrice', job='Warrior')
addzone('kaneakeluh', 'Cape Teriggan')
addnotes('kaneakeluh',
         'Fields of Valor notorious monster. Spawned at (I-8) in Cape Teriggan, in the corner of the square where H/I-8 and H/I-9 connect, with Chapter 6 Elite Training.',
         'Roughly 4,000-4,760 HP.',
         'Like all Fields of Valor notorious monsters it spawns with random attributes \u2014 additional effects on melee strikes, job traits, buffs such as shadows \u2014 and has extremely high, possibly capped, accuracy.',
         'Spawning it loses every pet called with Call Beast, along with NPCs. Buffs do not wear off on spawn.')

# ------------------------------------------------------- guards + write
assert not [k for r in m.values() for k, v in r.items() if v is None], 'null poison'
bad = [a for r in m.values() for a in (r.get('ab') or []) if a not in ABIL]
assert not ({r.get('fam') for r in m.values() if r.get('fam')} - set(FE))
orph = sum(1 for r in m.values() if not r.get('fam'))
json.dump(d, open(MOBS, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

print('mobs %d  orphans %d  NM-flagged %d' % (len(m), orph, sum(1 for r in m.values() if r.get('nm'))))
print('undefined ability refs: %d uses / %d names' % (len(bad), len(set(bad))))
print('\n--- corrections ---'); [print(' ', x) for x in log]
print('\n--- deliberately withheld ---'); [print(' ', x) for x in skipped]
print('\n--- fill-only declines ---'); [print(' ', x) for x in declined]
