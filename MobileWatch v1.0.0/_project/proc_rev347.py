#!/usr/bin/env python3
"""rev 347 — Unknown bucket sections 2 + 3, from 15 user screenshots.
Fill-only unless a change is listed in CORRECTIONS; every decline is logged.
Author: BalladOfWorms
"""
import json, sys, os

P = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
MOBS = os.path.join(P, 'mobs.json')

d = json.load(open(MOBS, encoding='utf-8'))
m, ABIL, FE = d['mobs'], d['abilities'], d['family_eco']
log, declined = [], []

# ---- guards -------------------------------------------------------------
ZONES = {z['name'] for z in json.load(open(os.path.join(P, 'zones.json'), encoding='utf-8'))['zones']}
INUSE = set()
for v in m.values():
    for z in (v.get('zones') or []):
        INUSE.add(z[0] if isinstance(z, list) else z)
def zok(z):
    assert z in ZONES or z in INUSE, 'unknown zone %r' % z
    return z

KIT = {  # family -> modal kit, computed live below and asserted
    'Mimic': ['Death Trap', 'Draw-In'],
    'Taurus': ['Back Swish', 'Frightful Roar', 'Mortal Ray', 'Mow', 'Triclip', 'Unblest Armor'],
    'Gargouille': ['Bloody Claw', 'Dark Mist', 'Dark Orb', 'Terror Eye', 'Triumphant Roar'],
    'Skeleton': ['Black Cloud', 'Blood Saber', 'Hell Slash', 'Horror Cloud'],
    'Flock Bat': ['Jet Stream', 'Slipstream', 'Sonic Boom', 'Turbulence'],
    'Hound': ['Dirty Claw', 'Howling', 'Methane Breath', 'Poison Breath', 'Rot Gas', 'Shadow Claw'],
}
for f, k in KIT.items():
    assert f in FE, f
    for a in k:
        assert a in ABIL, 'undefined ability %r' % a

def fill(key, field, val):
    """write only into an empty field; log every decline"""
    r = m[key]
    if r.get(field) in (None, '', [], {}):
        r[field] = val
        return True
    if r[field] != val:
        declined.append('%s.%s kept %r (page said %r)' % (key, field, r[field], val))
    return False

def correct(key, field, val, why):
    r = m[key]
    log.append('CORRECT %s.%s %r -> %r  [%s]' % (key, field, r.get(field), val, why))
    r[field] = val

def addzone(key, zone, lvs=None):
    r = m[key]
    zs = r.setdefault('zones', [])
    have = {z[0] if isinstance(z, list) else z for z in zs}
    if zone in have:
        return False
    zs.append([zok(zone), lvs] if lvs else [zok(zone)])
    return True

def addnotes(key, *bullets):
    r = m[key]
    ns = r.setdefault('notes', [])
    for b in bullets:
        if b not in ns:
            ns.append(b)

def addsp(key, *spells):
    r = m[key]
    sp = r.setdefault('sp', [])
    for s in spells:
        if s not in sp:
            sp.append(s)

def stamp(key, fam, kit=True, **kw):
    assert key in m, 'MISSING RECORD %r' % key
    assert fam in FE, 'unknown family %r' % fam
    fill(key, 'fam', fam)
    if kit and fam in KIT:
        fill(key, 'ab', list(KIT[fam]))
    for f, v in kw.items():
        fill(key, f, v)

# =========================================================================
# SECTION 2 — zoned reals
# =========================================================================

# --- sturdy pyxis -> Mimic (BG "Sturdy Pyxis (NM)") ----------------------
stamp('sturdy pyxis', 'Mimic', job='Warrior', crys='Dark', nm=True,
      spawn='4 per zone. Free-spawning Sturdy Pyxides in every Abyssea area; some are real chests.')
for z in ['Abyssea-La Theine', 'Abyssea-Uleguerand', 'Abyssea-Altepa', 'Abyssea-Grauberg']:
    addzone('sturdy pyxis', z, '78-87')
    t = 'Abyssea: %s: Adversary' % z
    c = m['sturdy pyxis'].setdefault('content', [])
    if t not in c:
        c.append(t)
addsp('sturdy pyxis', 'Comet')
addnotes('sturdy pyxis',
         'Roughly 60,000 HP.',
         'Mimics only appear from Sturdy Pyxides that are free-spawning in each Abyssea area; they never drop from monsters. A Sturdy Pyxis found in the zone can still be a real chest.',
         'Reverts to a Sturdy Pyxis when everyone and every pet on its hate list is dead or has lost hate by distance. May despawn entirely once all players with hate are dead.',
         'Cannot be deaggroed by parking a pet on it and running: the draw-in range is massive and it constantly pulls anyone with hate back in. The pet owner joins the hate list if the pet attacks.',
         'Death Trap has roughly 35 yalms of range and adds Stun and Poison. It appears to carry a high Regain effect.',
         'Only the Mimics in Abyssea-Grauberg, Abyssea-Altepa, Abyssea-Attohwa and Abyssea-Uleguerand cast Comet.',
         'Immune to dark-based Sleep. Light-based sleep (Lullaby) still works.')

# --- megalotaur -> Taurus ------------------------------------------------
stamp('megalotaur', 'Taurus', job='Warrior', nm=True, agg=True, lnk=True,
      im=['Sleep'])
correct('megalotaur', 'det', ['True Sight'], 'page notes column reads T(S)')
if 'Mighty Strikes' not in m['megalotaur']['ab']:
    m['megalotaur']['ab'].append('Mighty Strikes')
    assert 'Mighty Strikes' in ABIL
addnotes('megalotaur',
         'Uses its two-hour ability and TP moves in unison with Torvotaur.',
         'Hate is reset whenever Mortal Ray or Mighty Strikes goes off. Two blink tanks are the recommended setup for the pair.',
         'Very highly resistant and probably outright immune to Sleep, even through Elemental Seal.',
         'A summoner kiting with Leviathan and Spinning Dive is highly effective.')

# --- the three Beaucedine gargouilles (siblings of astika, rev 344) ------
for k in ['shesha', 'kaliya', 'vasuki']:
    stamp(k, 'Gargouille', agg=True)
addsp('shesha', 'Stun', 'Bind')
addnotes('shesha', 'Can cast Stun and Bind.')
addsp('kaliya', 'Stun')
addnotes('kaliya', 'Can cast Stun.',
         'Very resistant to Repose, but it did stick for about 10 seconds with a Light Staff equipped.')
fill('vasuki', 'job', 'Red Mage')
addsp('vasuki', 'Gravity', 'Silence')
addnotes('vasuki', 'Can cast Gravity and Silence.')

# =========================================================================
# SECTION 3 — the rev-141 hand-exclusions, now page-resolved
# =========================================================================

# --- the toads: BG "Toad"/"Toads" is our Frog (rule 289, 5th payout) -----
stamp('chorus toad', 'Frog', crys='Water')
addzone('chorus toad', 'Caedarva Mire', '95-96')
addnotes('chorus toad',
         'A standard Caedarva Mire mob that also supports the Voidwatch NM Brekekekex during that fight.',
         'Assists the main boss with area-of-effect silence.')

stamp("poroggo's toady", 'Frog', crys='Water', nm=True, agg=True, lnk=True, spawn='6')
correct("poroggo's toady", 'det', ['True Sound'], 'page notes column reads T(H)')
addzone("poroggo's toady", 'West Sarutabaruta [S]')
addnotes("poroggo's toady",
         'Spawned with Poroggo Gourmand for the quest Succor to the Sidhe.',
         'Respawns if all six are killed.',
         'Extremely low HP and Defense.',
         'Susceptible to Sleep, Gravity and Bind, but resistance builds: after a third Sleepga they start waking early, and a fourth is outright resisted.')

stamp('wetscale toad', 'Frog', crys='Water', lnk=True, spawn='7')
addzone('wetscale toad', 'Cirdas Caverns', '119-121')
correct('wetscale toad', 'lv', [119, 126], 'page measures 119-121 in Cirdas Caverns; the stored 125-126 has no zone attached (union, see open item)')
addnotes('wetscale toad',
         'Spawns around the south-east areas of map 2.',
         'Despoil: Poroggo Hat.')

# --- the draugar: BG "Skeletons" is our Skeleton (rule 5) ----------------
stamp('distraught draugar', 'Skeleton', spawn='2 per Reive')
addzone('distraught draugar', 'RaKaznar Inner Court', '118-124')
addnotes('distraught draugar',
         'Guards the Dimensional Tethers in the Lair Reives in Ra\u2019Kaznar Inner Court.',
         'Aggressive to Reive participants only.')

stamp('procrustean draugar', 'Skeleton', agg=True)
correct('procrustean draugar', 'det', ['Sight', 'Sound', 'Blood'], 'page notes column reads A(R), S, H, HP')
addzone('procrustean draugar', 'Outer RaKaznar', '113-116')
addnotes('procrustean draugar',
         'Guards the Dimensional Tether in the Lair Reive at (J-6) in Outer Ra\u2019Kaznar.',
         'Aggressive to Reive participants only.')

# --- Muut's adds: Muut's OWN page calls them "the skeletons" (rule 295) --
for k in ["muut's hound warrior", "muut's sacrifice"]:
    stamp(k, 'Skeleton', lnk=True)
    addzone(k, 'Attohwa Chasm')
    addsp(k, 'Sleepga II')
    addnotes(k,
             'Summoned by Muut during its Unity fight; killing all of the summoned skeletons procs Muut and inflicts terror on it for a few seconds.',
             'Automatically attacks whoever started the Unity fight. Tends to weapon-skill at the same time as Muut and can cast Sleepga II \u2014 keep the backline clear.',
             'If the adds are supertanked rather than killed, Muut keeps summoning more; 7-8 have been up at once.')

# --- vampyr bats: BG "Bat Trio" is our Flock Bat (rule 289, 6th payout) --
stamp('vampyr bats', 'Flock Bat', job='Warrior', nm=True, spawn='6')
correct('vampyr bats', 'det', ['True Sound', 'Blood'], 'page notes column reads A, L, T(H), HP')
for z in ["Ortlinde's Chamber", "Gerhilde's Chamber", "Brunhilde's Chamber"]:
    addzone('vampyr bats', z, '75-80')
addnotes('vampyr bats',
         'A transformation of the Vampyr Jarl. The bats must be killed in a random, sequential order.',
         'Once all (or most) are slain they converge back into the Vampyr Jarl, which returns with reduced HP.',
         'Immune to every form of Sleep, including Lullaby and Repose.')
m['vampyr bats']['im'] = ['Sleep']

# --- vampyr wolf: the panel names the family outright, "Hounds" ----------
stamp('vampyr wolf', 'Hound', nm=True)
addnotes('vampyr wolf',
         'A wolf/hound form the Vampyr Jarl periodically transforms into during Einherjar in the Hazhalm Testing Grounds.',
         'The spawned hounds must be defeated in a randomised sequential order before they converge back into the Vampyr Jarl.',
         'Immune to every form of Sleep.')
m['vampyr wolf']['im'] = ['Sleep']

# --- dragzagg's wyvern -> the family we already keep for dragoon pets ----
stamp("dragzagg's wyvern", 'Wyvern (Dragoon Pet)', nm=True)
addzone("dragzagg's wyvern", 'Horlais Peak')
addnotes("dragzagg's wyvern",
         'The pet wyvern called out by Wyvernkin Dragzagg at the start of the "Last Orc-Shunned Hero" BCNM at Horlais Peak, entered through Yughott Grotto.',
         'Up to six players, 30-minute limit; the battlefield is traded a Deimos Orb or 50 Kindred\u2019s Crests.',
         'Uses a dark model in the style of the Dynamis enemies.')

# =========================================================================
# BONUS — same panel, rule 295: the Horlais Peak BCNM orcs
# =========================================================================
ORCS = {'wyvernkin dragzagg': 'Dragoon', 'bruteborn krushkosh': 'Warrior',
        'bonesetter medokvok': 'White Mage', 'crackshot zwogchog': 'Ranger'}
for k, job in ORCS.items():
    stamp(k, 'Orc', kit=False, nm=True, job=job)
    addzone(k, 'Horlais Peak')
    addnotes(k, 'An opponent in the "Last Orc-Shunned Hero" BCNM at Horlais Peak, entered through Yughott Grotto. Up to six players, 30-minute limit.')
addnotes('bonesetter medokvok', 'Moves around actively to heal the other members of the mob group.')
addnotes('crackshot zwogchog', 'Uses fast ranged attacks.')
addnotes('wyvernkin dragzagg', 'Calls out Dragzagg\u2019s Wyvern at the start of the fight.')

# =========================================================================
# guards + write
# =========================================================================
assert not [k for r in m.values() for k, v in r.items() if v is None], 'null poison'
bad = [a for r in m.values() for a in (r.get('ab') or []) if a not in ABIL]
fams = {r.get('fam') for r in m.values() if r.get('fam')}
assert not (fams - set(FE)), fams - set(FE)
orph = sum(1 for r in m.values() if not r.get('fam'))

json.dump(d, open(MOBS, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

print('mobs %d  orphans %d  NM-flagged %d' % (len(m), orph, sum(1 for r in m.values() if r.get('nm'))))
print('undefined ability refs: %d uses / %d names' % (len(bad), len(set(bad))))
print('\n--- corrections ---'); [print(' ', x) for x in log]
print('\n--- fill-only declines ---'); [print(' ', x) for x in declined]
