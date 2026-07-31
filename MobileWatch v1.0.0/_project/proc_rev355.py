#!/usr/bin/env python3
"""rev 355 — Unknown bucket section 4, sixth batch, from 13 user screenshots.
Author: BalladOfWorms

DET POLICY (rev 350): page notes-column letters REPLACE det; `Blood` survives where
the record already carries it.
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
    'Sheep': ['Feeble Bleat', 'Lamb Chop', 'Rage', 'Sheep Bleat', 'Sheep Charge', 'Sheep Song'],
    'Skeleton': ['Black Cloud', 'Blood Saber', 'Hell Slash', 'Horror Cloud'],
    'Fomor': ['Aegis Schism', 'Barbed Crescent', 'Carnal Nightmare', 'Dancing Chains',
              'Foxfire', 'Grim Halo', 'Netherspikes', 'Shackled Fists'],
    'Lesser Bird': ['Blindside Barrage', 'Broadside Barrage', 'Damnation Dive', 'Helldive', 'Wing Cutter'],
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

def correct(key, field, val, why):
    log.append('CORRECT %-22s %-3s %r -> %r  [%s]' % (key, field, m[key].get(field), val, why))
    m[key][field] = val

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

def want(key, *names):
    for a in names:
        if a not in ABIL:
            undef.append('%s: %r — note only, add to ABIL_WANTED' % (key, a))

def stamp(key, fam, kit=True, **kw):
    assert key in m, key
    assert fam in FE, fam
    fill(key, 'fam', fam)
    if kit and fam in KIT:
        fill(key, 'ab', list(KIT[fam]))
    for f, v in kw.items():
        fill(key, f, v)

# ============================================= Voidwatch, the Qilin/Uptala pairs again
# Qing Long is Bai Hu's twin (rev 348): same summoner, same zone, same ~55,000 HP,
# and the same "Special Abilities: N/A" -> explicit ab: [], NOT the family modal.
stamp('qing long', 'Wyvern', kit=False, lnk=True, spawn='Summoned by Qilin (1 per Qilin)')
m['qing long']['ab'] = []
det('qing long', ['True Sound'])
addzone('qing long', 'The Shrine of RuAvitau')
addnotes('qing long', 'Voidwatch notorious monster, Zilart Stage III.',
         'Summoned by Qilin, one per Qilin. Roughly 55,000 HP.',
         'Carries the passive trait Silence Aura. The page lists no TP moves.')

# Trna is Bisa's twin (rev 348) — same summoner, same zone, same resummon behaviour.
stamp('trna', 'Skeleton', spawn="Summoned by Uptala's Yaksha Stance (1 per Uptala)")
det('trna', ['True Sound'])
addzone('trna', 'VeLugannon Palace')
addnotes('trna', 'Voidwatch notorious monster, Jeuno Stage II.',
         "Spawned by Uptala's Yaksha Stance. If defeated, Uptala resummons it the next time it uses Yaksha Stance.")

# ============================================= Einherjar
stamp('vanquished einherjar', 'Skeleton', job='Black Mage', spawn='12',
      drops="Hero's Reflections")
det('vanquished einherjar', ['True Sound'])
for z in ["Brunhilde's Chamber", "Gerhilde's Chamber", "Ortlinde's Chamber"]:
    addzone('vanquished einherjar', z, '75-80')
addnotes('vanquished einherjar', 'A possible encounter during Einherjar, Wing III chambers.')

# ============================================= Ra'Kaznar Colonization Reives
# The exact counterpart of `indomitable spurned` (rev 350): that one is a Fomor guarding
# the Heliotrope Barriers in RaKaznar Inner Court, this one guards the Amaranth Barriers
# in Outer RaKaznar — and its lv [113, 116] matches `amaranth barrier` exactly.
stamp('vengeful shunned', 'Fomor', job='Bard')
det('vengeful shunned', ['Sight', 'Sound'])
addzone('vengeful shunned', 'Outer RaKaznar', '113-116')
addnotes('vengeful shunned',
         'Guards the Amaranth Barriers in certain Colonization Reives in Outer Ra\u2019Kaznar.',
         'Aggressive to Reive participants only.')

# ============================================= Kamihr Drifts Colonization Reives
stamp('territorial lucerewe', 'Sheep', spawn='Colonization Reive')
det('territorial lucerewe', ['Sight', 'Sound'])
addzone('territorial lucerewe', 'Kamihr Drifts', '111-113')
addnotes('territorial lucerewe',
         'Defends the Icy Palisades in certain Kamihr Drifts Colonization Reives.',
         'Aggressive to Reive participants only.')

# BONUS — `icy palisade` was an orphan carrying the Obstacle fingerprint exactly: the flat
# -50% across all eight elements, det [Sight], no ab. Same lv [111, 113] as the Lucerewe
# that guards it, exactly as `amaranth barrier`/`heliotrope barrier` pair with their guards.
stamp('icy palisade', 'Obstacle', spawn='Colonization Reive')
addzone('icy palisade', 'Kamihr Drifts', '111-113')
addnotes('icy palisade',
         'Defended by Territorial Lucerewe during certain Kamihr Drifts Colonization Reives.',
         'Can be fought during Colonization Reives.')

# ============================================= Garrison
stamp('triarius xiii-lix', 'Antica', job='Black Mage', crys='Dark',
      spawn='Garrison (Eastern Altepa Desert)')
addzone('triarius xiii-lix', 'Eastern Altepa Desert')

# ============================================= Fields of Valor
correct('zagh', 'lv', [15, 15], 'page Level column prints 15; [1,1] was a placeholder')
stamp('zagh', 'Lesser Bird', agg=True, spawn='1, at (I-7)')
addzone('zagh', 'La Theine Plateau', '15')
addnotes('zagh',
         'Fields of Valor notorious monster. Spawned in Chapter 1 of Elite Training by trading up to 6 Beastmen\u2019s Seals, 300 gil, or up to level-15 equipment to the Field Parchment at (I-7) \u2014 awarding 450 EXP, 600 gil, or an augment respectively.',
         'Roughly 350 HP. Appears to have a random en-spell every time; Enblizzard, Enfire and Enthunder have all been reported.',
         'Absorbs wind-based damage.',
         'Soloed by DNC/WAR 16 with TP300 and no two-hour, by DRG/WAR 18, and quite easily by RDM/BLM 27.')

# ============================================= Supreme Being
# "Has all of Shinryu's abilities but lacks the ability to recover HP by taking damage
# while readying TP moves or casting magic" — that mechanic is OUR OWN def of
# `Battle Stances`: "Wings spread: absorbs damage from any source if the hit lands
# during a TP move or a cast." So the kit is Shinryu's minus exactly that one move.
SHINRYU = list(m['shinryu']['ab'])
assert 'Battle Stances' in SHINRYU
stamp('sempurne', 'Supreme Being', kit=False, job='Black Mage')
fill('sempurne', 'ab', [a for a in SHINRYU if a != 'Battle Stances'])
det('sempurne', ['True Sight'])
addzone('sempurne', 'Desuetia Empyreal Paradox', '125')
addnotes('sempurne', 'Fought for the mission No Time Like the Future. Roughly 100,000 HP.',
         'A weaker version of Shinryu. It has all of Shinryu\u2019s abilities but lacks the ability to recover HP by taking damage while readying TP moves or casting magic.',
         'Blue mages can learn Mighty Guard from it.')

# ============================================= Walk of Echoes — When Wills Collide
# Third record from this battlefield: `larzos` (r352), `portia` (r354), now Ragelise.
# All three are lv [84, 84] Walk of Echoes NMs.
stamp('ragelise', 'Humanoid', kit=False, agg=True, spawn='1')
addzone('ragelise', 'Walk of Echoes', '84')
addnotes('ragelise',
         'Sir Ragelise B Baloumat, captain of the Knights of the Ironcrest Hawk. Fought in the battlefield event When Wills Collide. Roughly 6,000 HP.',
         'Uses the sword weapon skill Sanguine Blade, and his melee attacks carry an additional effect of paralysis. Casts Banishga III and Holy.',
         'Says "Mere mortals cannot hope to withstand my newfound might!" before using Rancor Smash, which deals damage, knockback and Amnesia.',
         'Seems to share hate under certain conditions with Portia \u2014 kiting Ragelise while attacking Portia first may make him abandon the kiter for whoever has hate on Portia, and possibly the reverse.')
want('ragelise', 'Sanguine Blade', 'Rancor Smash')

# ============================================= Promathia Mission 5-3 / Ulmia Path
SHIK = {'shikaree x': ('Beastmaster, Ninja',
                       'Wields two daggers and is capable of using Evisceration. Summons a pet rabbit to assist her, and will resummon it if it is slain.'),
        'shikaree z': ('Dragoon, White Mage',
                       'Wields a polearm and is capable of using Impulse Drive. Tries to heal herself and her comrades during the battle.')}
for k, (job, quirk) in SHIK.items():
    stamp(k, 'Humanoid', kit=False, job=job, agg=True, spawn='1')
    addzone(k, 'Boneyard Gully', '50-53')
    addnotes(k, 'Mission boss. Appears in the battlefield event for Promathia Mission 5-3 / Ulmia Path, and in the quests Tango with a Tracker and Requiem of Sin, both uncapped.',
             'As of the 2010-06-21 update there is no longer a level restriction on Promathia Mission 5-3 / Ulmia Path.', quirk)
fill('shikaree x', 'drops', 'Nilgal Pole')
addnotes('shikaree x', 'Also appears in the \u2605Head Wind battlefield in Boneyard Gully at level 113-121+, three at a time.')
want('shikaree x', 'Evisceration')
want('shikaree z', 'Impulse Drive')
skipped.append("shikaree y is filed `Blessed Races of Altana` while X and Z's pages both print "
               "`Family: Humanoids` — the three sisters are split across two families, see handoff note")

# ============================================= Bastok Mission 9-2
stamp('zeid', 'Humanoid', kit=False, job='Dark Knight', spawn='1')
det('zeid', ['True Sight'])
addzone('zeid', 'Throne Room', '75-78')
addlist('zeid', 'ab', 'Blood Weapon')
addnotes('zeid', 'Fought for Bastok Mission 9-2: Where Two Paths Converge. Roughly 7,800 HP.',
         'Can use all great sword skills up to, and tends to favour, Ground Strike.',
         'Uses a ranged attack called Abyssal Strike with an additional effect of Stun, and a fairly potent Drain skill called Abyssal Drain. Casts various Absorb spells and seems to have TP Regain.',
         'Summons two Shadows of Rage to assist him and resummons them later if they are defeated. Both use the same Abyssal weapon skills Zeid does, and the two can skillchain with him.')
want('zeid', 'Ground Strike', 'Abyssal Strike', 'Abyssal Drain')

# ============================================= Zerde's three minions — no family named
for k in ["zerde's drisheen", "zerde's haupia", "zerde's kacamak"]:
    addzone(k, 'Reisenjima', '123-124')
    addlist(k, 'content', 'Geas Fete: Reisenjima: HELM')
    addnotes(k, 'An add spawned during the Zerde Geas Fete notorious monster encounter in Reisenjima, alongside Haupia and Kacamak and Drisheen.',
             'Square Enix greatly reduced the darkness resistances of Zerde\u2019s minions, and gave them a cumulative resistance to the black magic spell Death.')
skipped.append("zerde's drisheen/haupia/kacamak: the panel names all three minions but NOT their "
               "family \u2014 zone, content tag and notes only")

# ============================================= guards + write
assert not [k for r in m.values() for k, v in r.items() if v is None], 'null poison'
bad = [a for r in m.values() for a in (r.get('ab') or []) if a not in ABIL]
assert not ({r.get('fam') for r in m.values() if r.get('fam')} - set(FE))
orph = sum(1 for r in m.values() if not r.get('fam'))
json.dump(d, open(MOBS, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

print('mobs %d  orphans %d  NM-flagged %d' % (len(m), orph, sum(1 for r in m.values() if r.get('nm'))))
print('undefined ability refs: %d uses / %d names' % (len(bad), len(set(bad))))
print('\n--- corrections ---'); [print(' ', x) for x in log]
print('\n--- abilities NOT written ---'); [print(' ', x) for x in undef]
print('\n--- withheld / flagged ---'); [print(' ', x) for x in skipped]
print('\n--- fill-only declines ---'); [print(' ', x) for x in declined]
