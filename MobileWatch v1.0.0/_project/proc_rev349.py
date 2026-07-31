#!/usr/bin/env python3
"""rev 349 — Unknown bucket section 4, second batch, from 13 user screenshots.
Author: BalladOfWorms
"""
import json, os

P = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
MOBS = os.path.join(P, 'mobs.json')
d = json.load(open(MOBS, encoding='utf-8'))
m, ABIL, FE = d['mobs'], d['abilities'], d['family_eco']
log, declined, undef = [], [], []

ZONES = {z['name'] for z in json.load(open(os.path.join(P, 'zones.json'), encoding='utf-8'))['zones']}
INUSE = {(z[0] if isinstance(z, list) else z) for v in m.values() for z in (v.get('zones') or [])}
def zok(z):
    assert z in ZONES or z in INUSE, 'unknown zone %r' % z
    return z

KIT = {
    'Antica': ['Jamming Wave', 'Magnetite Cloud', 'Sand Shield', 'Sand Trap', 'Sand Veil',
               'Sandstorm', 'Shoulder Slam', 'Spikeball'],
    'Animated Weapon': ['Dire Whorl'],
    'Ghost': ['Curse', 'Dark Sphere', 'Ectosmash', 'Fear Touch', 'Grave Reel', 'Terror Touch'],
    'Gigas': ['Catapult', 'Colossal Blow', 'Grand Slam', 'Ice Roar', 'Impact Roar',
              'Lightning Roar', 'Mercurial Strike', 'Moribund Hack', 'Power Attack', 'Trebuchet'],
    'Demon': ['Demonic Howl', 'Hecatomb Wave', 'Soul Drain'],
    'Djinn': ['Berserk', 'Dark Wave', 'Nocturnal Combustion', 'Penumbral Impact'],
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
    log.append('CORRECT %-24s %-4s %r -> %r  [%s]' % (key, field, m[key].get(field), val, why))
    m[key][field] = val

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
    """abilities dict is the gate — undefined names are logged, never written"""
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

# ============================================================ Mercenary Camp BCNM
# Four pages, identical family / zone / spawns / detects. The Paladin page arrived
# with its title cropped; `counselor rughadjeen` is the only counselor in the file
# carrying a Paladin spell set (Cure IV, Holy, Banish II, Protect III, Shell III,
# Flash) — `counselor mihli` holds a full White Mage set. The file named it, not us.
COUNSEL = {
    'counselor gadalar':    ('Black Mage', ['Manafont'],       ['Salamander Flame']),
    'counselor najelith':   ('Ranger',     ['Eagle Eye Shot'], ['Typhonic Arrow']),
    'counselor rughadjeen': ('Paladin',    ['Invincible'],     ['Victory Beacon']),
    'counselor zazarg':     ('Monk',       ['Hundred Fists'],  ['Meteoric Impact']),
}
for k, (job, defined, missing) in COUNSEL.items():
    stamp(k, 'Humanoid', kit=False, job=job,
          spawn='Special BCNM: Mercenary Camp (requires a Mercenary Camp Entry item)')
    correct(k, 'det', ['True Sound'], 'notes column reads A, L, T(H)')
    addzone(k, 'Stellar Fulcrum')
    addab(k, *defined, *missing)
    addnotes(k, 'Fought for the Mercenary Camp special battlefield event at Stellar Fulcrum. Entry requires a Mercenary Camp Entry item.',
             'Uses %s and %s.' % (defined[0], missing[0]))

# ============================================================ Periqia assault
GOLD = {'cursed axe':  ('Warrior',    'Melee attacks have a 100% critical hit rate.'),
        'demonic rod': ('White Mage', 'Attempts to heal King Goldemar with white magic, up to Cure V.')}
for k, (job, quirk) in GOLD.items():
    stamp(k, 'Animated Weapon', job=job, spawn='Summoned by King Goldemar')
    correct(k, 'det', ['True Sound'], 'notes column reads A, T(H)')
    addzone(k, 'Periqia')
    addnotes(k, 'Summoned by King Goldemar during the Periqia assault "The Price Is Right".',
             'Roughly 3,500 HP.', quirk, 'Uses Dire Whorl with sufficient TP.')

# ============================================================ Antica
stamp('decurio xiii-lv', 'Antica', job='Black Mage', crys='Dark',
      spawn='Garrison (Eastern Altepa Desert)')
addzone('decurio xiii-lv', 'Eastern Altepa Desert')
addnotes('decurio xiii-lv', 'Drops no gil and cannot be mugged.')

# ============================================================ Eldieme [S] pair
stamp('dhoul', 'Ghost', job='Black Mage', spawn='6')
addzone('dhoul', 'The Eldieme Necropolis [S]')
addlist('dhoul', 'sp', 'Sleepga II', 'Poisonga II', 'Blizzaga III')
addnotes('dhoul', 'Spawns with Ellylldan, six at a time.',
         'Casts Sleepga II, Poisonga II, Blizzaga III and other high-level black magic.',
         'Susceptible to Sleep spells and Lullaby songs without much resistance, though the duration is short for both. Also susceptible to Silence.',
         'A summoner is helpful for both Ellylldan and Dhoul.')

stamp('ellylldan', 'Djinn', spawn='Forced \u2014 select the "Shredded Label" at (I-10) on the third map of The Eldieme Necropolis [S] with a Red-labeled crate')
addzone('ellylldan', 'The Eldieme Necropolis [S]')
addnotes('ellylldan', 'Assisted by six Dhoul.',
         'Does not spawn claimed, and will only attack those in its pseudo-random path up and down the hallways near the "Shredded Label".',
         'Trampling attacks appear to be fire-based and can dramatically reduce MP \u2014 damage may be proportional to MP taken, or a function of its HP.',
         'Like Armed Gears, its elemental susceptibility changes with a TP move, in this case Berserk. Whether it follows a pattern is unknown.',
         'Uses a potent area-of-effect Bio TP move.',
         'For all intents and purposes untankable \u2014 it ignores hate. It tends to stay at the end of the tunnel where the Dhoul are if left alone, but will come down the tunnel every now and then, and will use its bio explosion move if anyone is in front of the "Shredded Label" altar.',
         'Hiding behind the "Shredded Label" keeps you out of range of its attacks.',
         'Speeds up as its HP drops. A summoner is helpful for both Ellylldan and Dhoul.')

# ============================================================ Lair Reive anchor
# Same flat -50%-to-all-eight grid and det [Sight] as every other Lair member.
stamp('dimensional tether', 'Lair', spawn='1 per Reive')
for z in ['Outer RaKaznar', 'RaKaznar Inner Court']:
    addzone('dimensional tether', z)
addnotes('dimensional tether',
         'Periodically spawns enemies which protect the Dimensional Tether \u2014 Procrustean Draugar in Outer Ra\u2019Kaznar and Distraught Draugar in Ra\u2019Kaznar Inner Court.',
         'Fought during Lair Reives.',
         'Cannot be damaged without the Pulverizing skill.')

# ============================================================ Succor to the Sidhe
stamp('edonus', 'Gigas', job='Warrior', crys='Ice')
addzone('edonus', 'Vunkerl Inlet [S]')
addab('edonus', 'Mighty Strikes')
addnotes('edonus', 'Spawned for the quest Succor to the Sidhe.',
         'Uses Mighty Strikes at 75%, 50% and 25% of its HP, and spams Power Attack while it is up.')

# ============================================================ Voidwatch
stamp('gloam servitor', 'Demon', spawn='2 per Planar Rift')
correct('gloam servitor', 'det', ['True Sound'], 'notes column reads T(H)')
addzone('gloam servitor', 'Lufaise Meadows')
addlist('gloam servitor', 'sp', 'Dispelga', 'Silencega', 'Addle')
addnotes('gloam servitor', 'Voidwatch notorious monster, Tavnazia Stage I.',
         'Spawned by examining a Planar Rift at (H-9) in Lufaise Meadows while holding a Hyacinth Stratum Abyssite and a Voidstone.',
         'Two spawn per rift and they follow and assist Abununnu \u2014 one is a mage and one is a melee. Defeating them unlocks abilities for Abununnu; when Abununnu casts, the mage casts too, and when Abununnu uses a TP move, the melee follows.')

# ============================================================ no family named
addnotes('esoteric scrivening',
         'A magic trap or circle spawned by Kam\u2019lanaut during the \u2605Return to Delkfutt\u2019s Tower battle. It matches his current element.',
         'Spawned when Kam\u2019lanaut uses his elemental sword moves (the -maeken magic attacks) below 50% health.',
         'Places a localised hazard field on the ground inflicting matching elemental stats-down and status debuffs.',
         'If it is not destroyed quickly it transforms into an exact copy of Kam\u2019lanaut, doubling the boss threat \u2014 switch targets on spawn.',
         'Extremely physically resistant; highly vulnerable to magic damage, and area-of-effect or targeted high-tier elemental spells take it down fast.')

# ============================================================ guards + write
assert not [k for r in m.values() for k, v in r.items() if v is None], 'null poison'
bad = [a for r in m.values() for a in (r.get('ab') or []) if a not in ABIL]
assert not ({r.get('fam') for r in m.values() if r.get('fam')} - set(FE))
orph = sum(1 for r in m.values() if not r.get('fam'))
json.dump(d, open(MOBS, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

print('mobs %d  orphans %d  NM-flagged %d' % (len(m), orph, sum(1 for r in m.values() if r.get('nm'))))
print('undefined ability refs: %d uses / %d names' % (len(bad), len(set(bad))))
print('\n--- corrections ---'); [print(' ', x) for x in log]
print('\n--- abilities NOT written (undefined) ---'); [print(' ', x) for x in undef]
print('\n--- fill-only declines ---'); [print(' ', x) for x in declined]
