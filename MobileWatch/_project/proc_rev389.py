#!/usr/bin/env python3
"""
REV 389 — the A-L slice of the EVERYTHING ELSE bucket.
12 panels folded, 18 deleted per the user's last screenshot.

DELIBERATE GUARD OVERRIDE: none needed — all 18 delete targets are fam=None with
no zones / content / notes / ab / drops / img. One (incandescent baelfyr) is
nm-flagged; that fact is printed before the delete and reported to decision item 8.

KEY RENAME: 'demishagin white mage' -> 'demisahagin white mage'. Its three
siblings (demisahagin bard / dragoon / monk) all spell it correctly and the
page title confirms them. The r200 lesson cuts both ways: fuzzy-search first,
then fix the outlier.
"""
import json, re, sys, os

P = 'app/src/main/assets/mobs.json'
if not os.path.exists(P):
    P = 'android/' + P
d = json.load(open(P))
M = d['mobs']; A = d['abilities']

before_mobs, before_ab = len(M), len(A)
before_bucket = sum(1 for m in M.values() if not m.get('fam'))

# ---------------------------------------------------------------- family kits
GIGAS_AB = ['Grand Slam', 'Ice Roar', 'Impact Roar', 'Power Attack', 'Lightning Roar',
            'Catapult', 'Moribund Hack', 'Trebuchet', 'Colossal Blow', 'Mercurial Strike']
MORBOL_AB = ['Bad Breath', 'Impale', 'Sweet Breath', 'Vampiric Lash', 'Vampiric Root']
FUNGUAR_AB = ['Dark Spore', 'Silence Gas', 'Frog Kick', 'Queasyshroom', 'Numbshroom',
              'Shakeshroom', 'Spore', 'Agaricus']
YAGUDO_AB = ['Howl', 'Parry', 'Double Kick', 'Feather Storm', 'Sweep']
SAHAGIN_AB = ['Bubble Armor', 'Hydroball', 'Hydro Shot', 'Spinning Fin']

ELEMS = ['Fire', 'Wind', 'Lightning', 'Light', 'Ice', 'Earth', 'Water', 'Dark']
GYVE_WK = [[e, None] for e in ELEMS]
GYVE_ST = [[t, None] for t in ['Physical', 'Slashing', 'Impact', 'H2H', 'Piercing', 'Ranged']]
OBSTACLE_ST = [[e, '-50%'] for e in
               ['Fire', 'Ice', 'Wind', 'Earth', 'Lightning', 'Water', 'Light', 'Dark']]

# ---------------------------------------------------------------- new ability
# Fourth Spitewarden's page describes Essence Jack fully; Type/element are not
# stated, so they stay unset (Quake Blast / Gravitic Horn precedent).
if 'Essence Jack' not in A:
    A['Essence Jack'] = {
        'd': "Used at low health on the player whose gear the Spitewarden copied. "
             "Inflicts Terror and lowers all of that player's stats; the Spitewarden's "
             "own damage rises sharply, apparently by absorbing what it drains.",
        'tgt': 'Single',
        'fx': ['Terror', 'Stats Down'],
        'notes': "If the copied player is out of range the Spitewarden breaks off its "
                 "current target and runs at them to land it. Not a hate reset — the "
                 "behaviour lasts only until Essence Jack connects.",
    }

# ---------------------------------------------------------------- 12 folds
FOLD = {}

FOLD['atori-tutori ???'] = dict(
    fam='Humanoid', job='Monk', nm=True, agg=True, det=['True Sound'],
    ab=['Hundred Fists'],
    zones=[['Balgas Dais'], ['QuBia Arena'], ['Horlais Peak'], ['Waughroon Shrine']],
    spawn='Quest (Beyond Infinity)',
    notes=[
        "Approximately 27,000 HP. One spawn per battlefield.",
        "Fought during the tenth limit-break quest, Beyond Infinity.",
        "Normal melee attacks carry extra physical damage that looks like Enfire. "
        "Ochain converts that added damage to MP if you block the normal hit; "
        "Barfire does not reduce it, because the damage is physical.",
        "Damage taken is capped at 100 per hit from any source. Anteaus has the same resistance.",
        "Using an Olde Rarab Tail on it freezes it in place for 90 seconds and removes "
        "its damage resistance for the duration.",
        "Gains resistance to Stun over repeated use.",
        "Can use any Hand-to-Hand weapon skill, and chains them back to back for "
        "skillchains. Asuran Fists reaches about 3,900 damage.",
        "Extremely accurate — its hit rate stays capped against a level 95 Thief in "
        "full evasion gear.",
        "Holds party-wide hate and does not go passive until every member in the "
        "battlefield is KO'd.",
    ])

FOLD['bopa greso'] = dict(
    fam='Humanoid', job='Thief', nm=True, agg=True, lnk=True, det=['True Sight'],
    ab=['Perfect Dodge'],
    zones=[['Chamber of Oracles']],
    spawn="Mission (Roar! A Cat Burglar Bares Her Fangs)",
    notes=[
        "4,000-4,100 HP. One spawn.",
        "Fought for the mission Roar! A Cat Burglar Bares Her Fangs. Nanaa Mihgo "
        "summons her as she takes damage.",
        "Uses every Dagger weapon skill up to Evisceration and favours Evisceration.",
        "Uses Perfect Dodge at low health.",
        "She and Cha Lebagta can both be slept.",
    ])

FOLD['brittle rock'] = dict(
    fam='Obstacle', det=['Sight'], st=OBSTACLE_ST,
    zones=[['Lebros Cavern', '75']],
    spawn='Assault (Excavation Duty)',
    notes=[
        "2,300-2,400 HP. Five spawn.",
        "Only found in the Lebros Cavern assault mission Excavation Duty.",
        "Takes 0-18 damage from normal melee and magic attacks and up to 100 from a "
        "weapon skill, so it cannot be broken down by ordinary damage. A bomb "
        "Self-Destruct does nothing to it.",
        "Use a Qiqirn Mine on it while staying engaged — the explosion takes the wall "
        "out in one shot.",
        "Damage-over-time spells such as Bio and Shock also do significant damage. "
        "Poison and Requiem are fully resisted.",
    ])

FOLD['cha lebagta'] = dict(
    fam='Humanoid', job='Ninja', nm=True, agg=True, lnk=True, det=['True Sight'],
    ab=['Mijin Gakure'],
    zones=[['Chamber of Oracles']],
    spawn="Mission (Roar! A Cat Burglar Bares Her Fangs)",
    notes=[
        "5,000-5,100 HP. One spawn.",
        "Fought for the mission Roar! A Cat Burglar Bares Her Fangs.",
        "Uses every Dagger weapon skill up to Evisceration and favours Evisceration.",
        "Casts Ninjutsu.",
        "Uses Mijin Gakure at low health.",
        "She and Bopa Greso can both be slept.",
    ])

FOLD['demishagin white mage'] = dict(
    _rename='demisahagin white mage', n='Demisahagin White Mage',
    fam='Sahagin', job='White Mage', crys='Water', ab=SAHAGIN_AB,
    zones=[['Yuhtunga Jungle', '45']],
    spawn="Expeditionary Force (Beastman's Banner)",
    notes=[
        "Sometimes spawned from a Beastman's Banner during Expeditionary Force.",
        "Uses Benediction at some point.",
    ])

FOLD['esoteric scrivening'] = dict(
    fam='Gyve', wk=GYVE_WK, st=GYVE_ST,
    zones=[['Stellar Fulcrum']],
    spawn="Summoned by Kam'lanaut",
    # notes already written from this page in an earlier session — kept as is
    )

FOLD['fourth spitewarden'] = dict(
    fam='Humanoid', nm=True, agg=True,
    ab=['Essence Jack'],
    zones=[['Walk of Echoes']],
    notes=[
        "Approximately 5,000 HP. One spawn.",
        "Copies the equipment from the waist up of the first player to enter the "
        "battlefield. Armour is copied in appearance only.",
        "Uses whatever weapon that player has equipped, which gives it that weapon's "
        "weapon skills including ones above level 75 such as Sanguine Blade and "
        "Cataclysm. Entering first on a Staff is recommended, since it keeps the "
        "Spitewarden off multi-hit weapon skills.",
        "Does not copy the spells or job abilities of the copied player's current job. "
        "Beastmaster, Puppetmaster and Summoner clones do not summon pets.",
        "Has Dual Wield if the copied player entered with two weapons equipped.",
        "Says \u201cThere can be only one!\u201d or \u201cYou are my future.\u201d before using Essence Jack.",
    ])

FOLD['hunting chief'] = dict(
    fam='Gigas', job='Monk', crys='Ice', nm=True, det=['Sight'],
    ab=GIGAS_AB + ['Hundred Fists'],
    zones=[['Qufim Island']],
    spawn='Garrison (Qufim Island)',
    notes=["Uses Hundred Fists at some point."])

FOLD['kedgebelly kate'] = dict(
    fam='Morbol', crys='Earth', nm=True, det=['Sound'], ab=MORBOL_AB,
    zones=[['Yhoator Jungle']],
    spawn='Fields of Valor (Elite Training: Chapter 6)',
    notes=[
        "Approximately 3,700 HP. One spawn.",
        "Spawned at (F-10) in Yhoator Jungle with Elite Training: Chapter 6 (400 tabs).",
        "As with every Fields of Valor NM it can spawn with varying traits — job, "
        "abilities, enspells, spikes, favoured TP moves, critical rate.",
        "Spawns with at least six shadows.",
    ])

FOLD['laa heha the falconer'] = dict(
    fam='Yagudo', crys='Wind', nm=True, agg=True, lnk=True, det=['Sight'],
    ab=YAGUDO_AB,
    zones=[['Sauromugue Champaign [S]']],
    spawn='Quest (Succor to the Sidhe)',
    notes=[
        "Spawned for the quest Succor to the Sidhe.",
        "Assisted by four Cinderwings and four Gorebeaks.",
    ])

FOLD['laa vaqu the sutler'] = dict(
    fam='Yagudo', job='Dancer', crys='Wind', nm=True, agg=True, lnk=True, det=['Sight'],
    ab=YAGUDO_AB + ['Kamaitachi'],
    zones=[['Fort Karugo-Narugo [S]']],
    spawn='Quest (Succor to the Sidhe)',
    notes=[
        "Approximately 15,000 HP. One spawn.",
        "Spawned for the quest Succor to the Sidhe, accompanied by four Pixiebanes.",
        "Kamaitachi is a heavy area attack with knockback that also strips every buff.",
        "The Pixiebanes resist Sleepga II moderately — Elemental Seal is advised, "
        "though it has been known to stick without it. They also hit hard and evade "
        "well: normal hits of 150-220, and a Thief and a Dragoon with capped and "
        "merited weapon skill plus sushi still struggled to land anything.",
    ])

FOLD['malodorous mort'] = dict(
    fam='Funguar', crys='Dark', nm=True, det=['True Sight'], ab=FUNGUAR_AB,
    zones=[['Horlais Peak']],
    spawn='KCNM (Kindergarten Cap)',
    notes=[
        "One spawn. Appears in the Kindred's Crest battlefield Kindergarten Cap.",
        "Assisted by three Mortobello.",
        "Drops a three-day-only Campaign item.",
    ])

# ---------------------------------------------------------------- apply folds
print('=== FOLDS ===')
for key, patch in FOLD.items():
    assert key in M, key
    m = M[key]
    assert not m.get('fam'), (key, m.get('fam'))
    rename = patch.pop('_rename', None)
    for k, v in patch.items():
        if k == 'notes' and m.get('notes'):
            for b in v:
                if b not in m['notes']:
                    m['notes'].append(b)
        else:
            m[k] = v
    if rename:
        assert rename not in M, rename
        M[rename] = M.pop(key)
        print('  RENAMED %-28s -> %s' % (key, rename))
        key = rename
    print('  %-28s fam=%-10s nm=%-5s zones=%s' %
          (key, M[key]['fam'], M[key].get('nm'), [z[0] for z in M[key].get('zones', [])]))

# ---------------------------------------------------------------- 18 deletes
DELETE = ['aragoneu knight', 'ashmea b greinner', 'babban ny mheillea', 'cerane i virgaut',
          'choh moui', 'clavauert b chanoix', 'dusk raider', 'febrenard c brunnaut',
          'federation dispenser', 'feldrautte i rouhent', 'field woundpatcher',
          'flame giant', 'haja zhwan', 'ice fiend', 'incandescent baelfyr',
          'invincible shield', 'laisavie x berlends', 'luminous coalescence']

print('\n=== DELETE PRE-FLIGHT ===')
survivors = json.dumps({k: v for k, v in M.items() if k not in DELETE}, ensure_ascii=False)
for k in DELETE:
    m = M[k]
    xref = survivors.count(m['n'])
    flags = []
    if m.get('zones'):   flags.append('ZONES')
    if m.get('content'): flags.append('CONTENT')
    if m.get('notes'):   flags.append('NOTES')
    if m.get('ab'):      flags.append('AB')
    if m.get('drops'):   flags.append('DROPS')
    if m.get('img'):     flags.append('IMG')
    if m.get('nm'):      flags.append('** NM-FLAGGED **')
    if xref:             flags.append('** XREF x%d **' % xref)
    print('  %-24s lv=%-10s %s' % (k, m.get('lv'), ' '.join(flags) or 'clean'))
    assert not (m.get('zones') or m.get('content') or m.get('notes') or
                m.get('ab') or m.get('drops') or m.get('img')), k
    assert xref == 0, k

for k in DELETE:
    del M[k]

# ------------------------------------------------- stray zone-string cleanup
# 49 records store 'QuBia Arena' (the zones.json form) and exactly one stores
# "Qu'Bia Arena". Normalised so the Zone view does not split the arena in two.
fixed = 0
for m in M.values():
    for z in (m.get('zones') or []):
        if isinstance(z, list) and z and z[0] == "Qu'Bia Arena":
            z[0] = 'QuBia Arena'; fixed += 1
print('\nzone-string normalise:  Qu\'Bia Arena -> QuBia Arena  x%d' % fixed)

# ------------------------------------------- pre-existing key/name mismatch
# Same class as the demishagin typo, found by the guard below: the key was
# missing the 'h' while the name field (the display authority) was correct.
# Nothing anywhere references the misspelled key form.
if "onycophora's sandworm" in M and "onychophora's sandworm" not in M:
    M["onychophora's sandworm"] = M.pop("onycophora's sandworm")
    print("key fix:  onycophora's sandworm -> onychophora's sandworm")

# ---------------------------------------------------------------- guards
assert not [k for m in M.values() for k, v in m.items() if v is None], 'NULL POISON'
assert not [k for a in A.values() for k, v in a.items() if v is None], 'NULL POISON (abilities)'
for k, m in M.items():
    assert k == m['n'].lower(), (k, m['n'])   # now 0 file-wide
    for z in (m.get('zones') or []):
        assert isinstance(z, (list, str)), (k, z)
    assert isinstance(m.get('ab_el', []), list)
undef = sorted({a for m in M.values() for a in (m.get('ab') or []) if a not in A})
print('undefined ability refs (names): %d' % len(undef))

json.dump(d, open(P, 'w'), separators=(', ', ': '), ensure_ascii=False)

after_bucket = sum(1 for m in M.values() if not m.get('fam'))
print('\nmobs      %d -> %d' % (before_mobs, len(M)))
print('abilities %d -> %d' % (before_ab, len(A)))
print('BUCKET    %d -> %d' % (before_bucket, after_bucket))
print('remaining bucket:')
for k in sorted(k for k, m in M.items() if not m.get('fam')):
    print('   ', k)
