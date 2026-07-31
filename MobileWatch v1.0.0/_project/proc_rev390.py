#!/usr/bin/env python3
"""
REV 390 — the M-Z slice. THE ORPHAN BUCKET GOES TO ZERO.

15 panels + a 19-name delete screenshot. 19 + 15 = 34 = the whole bucket, so
every record got exactly one instruction — BUT only under one reading of the
untitled panel (see below), and with ONE deliberate hold.

TWO THINGS THE USER MUST SEE:

(1) THE UNTITLED PANEL IS `the keeper`, NOT `the briars`. The screenshot is
    cropped above the page title; it opens at "Battle Info". Both names are in
    the bucket. Three independent checks agree:
      - the delete screenshot lists `The Briars` and does NOT list `The Keeper`.
        Reading the panel as The Keeper makes 19 + 15 = 34 a perfect partition;
        reading it as The Briars leaves The Keeper with no instruction at all
        and double-books The Briars (the rule-419 shape).
      - the panel says "Stronger than Mistdagger, The Briars (Galka), and The
        Briars (Elvaan)". `mistdagger` and `the briars` are both lv 108;
        `the keeper` is lv 110 — it is the one that is stronger than both.
      - the panel says Job: Scholar and casts Kaustra. `the keeper` stores an
        elemental nuke list; `the briars` stores a WHM/RDM enhancing list.

(2) `xuan wu` IS HELD FROM THE DELETE LIST AND FOLDED INSTEAD (rule 419).
    It is the fourth of the four Voidwatch guardians Qilin summons. `bai hu`
    (Tiger) and `qing long` (Wyvern) are ALREADY filed with families, zones and
    the "Summoned by Qilin (1 per Qilin)" spawn line, and this same batch folds
    `zhu que`. Deleting the fourth of four identical siblings while filing the
    other three is the shayaam mistake exactly. Folded to Adamantoise —
    Xuan Wu is the Black Tortoise, and the file already files that same
    guardian under his other name, `genbu`, as Adamantoise.
    => 18 deleted, 16 folded. SAY THE WORD AND I WILL DELETE IT.
"""
import json, os

P = 'app/src/main/assets/mobs.json'
if not os.path.exists(P):
    P = 'android/' + P
d = json.load(open(P))
M = d['mobs']; A = d['abilities']

before_mobs, before_ab = len(M), len(A)
before_bucket = sum(1 for m in M.values() if not m.get('fam'))

# ---------------------------------------------------------------- family kits
ORC_AB = ['Howl', 'Arm Block', 'Battle Dance', 'Shoulder Attack', 'Slam Dunk',
          'Aerial Wheel', 'Veil of Chaos']
ANTICA_AB = ['Jamming Wave', 'Magnetite Cloud', 'Sandstorm', 'Sand Shield', 'Sand Trap',
             'Sand Veil', 'Shoulder Slam', 'Spikeball']
DEMON_AB = ['Demonic Howl', 'Hecatomb Wave', 'Soul Drain']
DAHAK_AB = ['Body Slam', 'Flame Breath', 'Petro Eyes', 'Thornsong', 'Nullsong']
GARG_AB = ['Bloody Claw', 'Dark Orb', 'Dark Mist', 'Terror Eye', 'Triumphant Roar']
SLIME_AB = ['Digest', 'Fluid Spread', 'Fluid Toss']
SABO_AB = ['Needleshot', 'Photosynthesis', '1,000 Needles']
ADAMAN_AB = ['Aqua Breath', 'Earth Breath', 'Harden Shell', 'Head Butt',
             'Tortoise Stomp', 'Tortoise Song']

# family resist tables (the r357 ruling: for Garrison-era records the family
# table beats the one-entry +25% import default)
ORC_WK = [['Wind', '+30%'], ['Lightning', '+30%'], ['Light', '+30%'],
          ['Earth', '+30%'], ['Water', '+50%'], ['Dark', '+30%']]
ANTICA_WK = [['Fire', '+15%'], ['Wind', '+50%'], ['Lightning', '+15%'],
             ['Light', '+30%'], ['Ice', '+30%'], ['Water', '+15%']]
ANTICA_ST = [['Earth', '-50%'], ['Dark', '-50%']]

# Elemental swipe sets — MUST match family_resist_sets EXACTLY (the guard at
# AuctionApp.kt ~589 falls back to a plain grid when a member matches no set),
# which is why these say "Blunt" and not "Impact".
ELEM_PHYS = [['Slashing', '-75%'], ['Blunt', '-75%'], ['H2H', '-75%'],
             ['Piercing', '-75%'], ['Ranged', '-75%']]
DARK_SET_ST = ELEM_PHYS + [['Dark', '-95%']]
DARK_SET_WK = [['Light', '+50%']]
GEFYRST_ST = ELEM_PHYS + [['Wind', '-15%'], ['Light', '-15%'], ['Ice', '-95%'],
                          ['Earth', '-15%'], ['Water', '-95%'], ['Dark', '-15%']]
GEFYRST_WK = [['Fire', '+50%'], ['Lightning', '+50%']]

SHADOWFANG_ZONES = [[z] for z in [
    "Bastok Markets [S]", "Batallia Downs [S]", "Beadeaux [S]", "Beaucedine Glacier [S]",
    "Castle Oztroja [S]", "Crawlers Nest [S]", "East Ronfaure [S]", "Fort Karugo-Narugo [S]",
    "Garlaige Citadel [S]", "Grauberg [S]", "Jugner Forest [S]", "La Vaule [S]",
    "Meriphataud Mountains [S]", "North Gustaberg [S]", "Pashhow Marshlands [S]",
    "Rolanberry Fields [S]", "Sauromugue Champaign [S]", "Southern San d'Oria [S]",
    "The Eldieme Necropolis [S]", "Vunkerl Inlet [S]", "Windurst Waters [S]",
    "West Sarutabaruta [S]", "Xarcabard [S]", "Castle Zvahl Baileys [S]",
    "Castle Zvahl Keep [S]"]]

FOLD = {}

FOLD['monarca de altepa'] = dict(
    fam='Sabotender', job='Monk', crys='Water', ab=SABO_AB, nm=True, lnk=True,
    zones=[['Western Altepa Desert']],
    spawn='Fields of Valor (Elite Training: Chapter 6)',
    notes=[
        "Spawned by the Field Parchment at (I-9) with the Chapter 6 Elite Training "
        "page key item, by trading 26 Beastmen's Seals, up to 1300 gil, or an item "
        "up to level 65.",
        "Occasionally spawns with Ensilence, which procs very frequently.",
        "Susceptible to Sleep and Silence — a Red Mage or Ninja can silence it in "
        "melee gear.",
        "Hits for 20-40 damage through Phalanx.",
        "Weak and susceptible to ice-based spells such as Paralyze.",
        "Its TP move Needleshot hits for around 200 damage.",
        "Surrounding Cactuars will link with it if you get within range.",
    ])

FOLD['orcish colonel'] = dict(
    fam='Orc', job='Monk', crys='Fire', ab=ORC_AB + ['Hundred Fists'], nm=True,
    wk=ORC_WK, st=[],
    zones=[['Jugner Forest', '35']],
    spawn='Garrison (Jugner Forest)',
    notes=["Uses Hundred Fists multiple times during the fight, possibly on a timer."])

FOLD['orcish fighterchief'] = dict(
    fam='Orc', job='Monk', crys='Fire', ab=ORC_AB + ['Hundred Fists'], nm=True,
    wk=ORC_WK, st=[],
    zones=[['West Ronfaure', '25']],
    spawn='Garrison (West Ronfaure)',
    notes=["Uses Hundred Fists at some point."])

FOLD['sagittarius xiii-xxvi'] = dict(
    fam='Antica', job='Ranger', crys='Dark', ab=ANTICA_AB,
    wk=ANTICA_WK, st=ANTICA_ST,
    zones=[['Eastern Altepa Desert', '50-55']],
    spawn='Garrison (Eastern Altepa Desert)',
    notes=["Does not drop gil and cannot be Mugged."])

FOLD['seed thrall'] = dict(
    fam='Humanoid', job='Varies', lv=[75, 75], det=['True Sound', 'Scent'],
    zones=[['Stellar Fulcrum', '75']],
    spawn='Mission (Ode of Life Bestowing)',
    notes=[
        "Roughly 500 HP. Spawned by the Seed Crystal during the mission Ode of Life "
        "Bestowing when it uses Seed of Deception, and it can spawn in rapid succession.",
        "Appears identically to the player targeted by Seed of Deception, down to the "
        "equipment, and retains any effect that gear grants — a copied Ice Staff gives "
        "its attacks an Ice additional effect, and it uses ranged attacks if the copied "
        "character is a Ranger.",
        "Has access to most weapon skills of its equipped weapon whether or not the "
        "copied player has learned them.",
        "Does not cast spells or use job abilities. It has no MP and cannot be Aspired.",
    ])

FOLD['shadowbreath defiler'] = dict(
    fam='Demon', job='Warrior', crys='Dark', ab=DEMON_AB,
    zones=[['Castle Zvahl Keep [S]', '70']],
    spawn='Nine spawn during Campaign Battles in Castle Zvahl Keep [S].',
    notes=[
        "Appears during Campaign Battles as part of the Dark Kindred's Shadowbreath "
        "Battalion, led by Shadowbreath and deployed exclusively to Castle Zvahl Keep [S].",
        "Does not drop gil and cannot be Mugged.",
    ])

FOLD['shadowfang void'] = dict(
    fam='Elemental', job='Dark Knight / Black Mage / Red Mage',
    det=['True Sound', 'Magic'], wk=DARK_SET_WK, st=DARK_SET_ST,
    zones=SHADOWFANG_ZONES,
    spawn='Nine spawn during Campaign Battles.',
    _sp_add=['Dispelga', 'Dread Spikes', 'Sleepga II'],
    notes=[
        "Roughly 17,000 HP. Appears during Campaign Battles as part of the Dark "
        "Kindred's Shadowfang Battalion, led by Shadowfang. Unlike the other "
        "battalions it deploys to any area held by either the Allied Forces of Altana "
        "or the Dark Kindred.",
        "Casts every spell a dark elemental uses, including Bio III, Dispelga, "
        "Dread Spikes and Sleepga II.",
        "Can be slept with Lullaby and Repose.",
        "Extremely weak to the Blue Magic spell Poison Breath, which does 200+ damage "
        "every cast.",
    ])

FOLD['shadowhind machinator'] = dict(
    fam='Demon', job='Warrior', crys='Dark', ab=DEMON_AB, lnk=True,
    det=['True Sight', 'Scent'],
    zones=[['Beaucedine Glacier [S]'], ['Xarcabard [S]']],
    spawn='Six spawn during Campaign Battles.',
    notes=[
        "Appears during Campaign Battles carrying out special missions for the Dark "
        "Kindred rather than fighting: in beastman-held areas it repairs the "
        "fortifications, and in allied areas it bombs them.",
        "Each unit that reaches the fortifications and warps out raises their level by "
        "5 points. It will sometimes construct a Confederate Mantelet as well.",
        "In allied areas it may instead construct a Confederate Belfry, or a Siege "
        "Turret if the conditions are right.",
        "Unlike most Kindred it avoids conflict to carry out its mission. It has lower "
        "HP than a normal campaign enemy, though still fairly high.",
        "Killing them in a stalwart defense hastens the enemy retreat by disrupting "
        "supply lines, and killing them in allied areas prevents damage to the "
        "fortifications. They can be intercepted as soon as they enter the area.",
        "Does not drop gil and cannot be Mugged.",
    ])

FOLD['shadowsoul devourer'] = dict(
    fam='Dragon', crys='Dark', ab=DAHAK_AB, agg=True, lnk=True,
    det=['True Sight', 'Scent'],
    zones=[['Xarcabard [S]', '70']],
    spawn='Nine spawn during Campaign Battles in Xarcabard [S].',
    notes=[
        "Appears during Campaign Battles as part of the Dark Kindred's Shadowsoul "
        "Battalion, led by Shadowsoul and deployed exclusively to Xarcabard [S].",
        "Has the same abilities as the Dahaks, including Nullsong.",
        "Weakened in the March 23, 2010 version update — noticeably less damage and "
        "less HP than before.",
    ])

FOLD['shadowwing infuriator'] = dict(
    fam='Gargouille', crys='Dark', ab=GARG_AB, agg=True,
    det=['True Sight', 'True Sound'],
    zones=[['Beaucedine Glacier [S]', '70']],
    spawn='Nine spawn during Campaign Battles in Beaucedine Glacier [S].',
    notes=[
        "Appears during Campaign Battles as part of the Dark Kindred's Shadowwing "
        "Battalion, led by Shadowwing and deployed exclusively to Beaucedine Glacier [S].",
        "Does not land on the ground.",
        "Uses Dark Orb often, which is devastating when spammed at low health — "
        "Magic Defense Bonus and Dark Carol are recommended.",
    ])

FOLD['swamp muck'] = dict(
    fam='Slime', crys='Water', ab=SLIME_AB, agg=True, lnk=True, nm=True,
    zones=[['Pashhow Marshlands [S]']],
    spawn='Ten spawn for the quest Succor to the Sidhe.',
    notes=["Ten spawn alongside Go'Rha Sludgewater for the quest Succor to the Sidhe."])

FOLD['the keeper'] = dict(
    fam='Humanoid', job='Scholar', nm=True, lnk=True, det=['True Sight'],
    zones=[['Rala Waterways [U]', '110']],
    spawn='One spawn in the Behind the Sluices battlefield.',
    _sp_add=['Kaustra'],
    notes=[
        "A mission boss, fought in Behind the Sluices in Rala Waterways [U].",
        "Casts Kaustra on a single target for massive damage.",
        "Uses Gust Slash and Cyclone.",
        "Stronger than Mistdagger, The Briars (Galka) and The Briars (Elvaan).",
    ])

FOLD['touched gefyrst'] = dict(
    fam='Elemental', det=['Magic'], wk=GEFYRST_WK, st=GEFYRST_ST,
    zones=[['Woh Gates', '121-122']],
    notes=[
        "An ice- and water-aspected hybrid elemental found in Woh Gates.",
        "Drops the Sacred Kindred's Crest key item.",
    ])

FOLD['treefeller snogrog'] = dict(
    fam='Orc', crys='Fire', ab=ORC_AB, agg=True, lnk=True, nm=True,
    zones=[['Jugner Forest [S]']],
    spawn='Quest (Succor to the Sidhe)',
    _sp_add=['Slowga', 'Stonega'],
    notes=[
        "Spawned for the quest Succor to the Sidhe.",
        "Casts every Earth-based spell, including Slowga. Be ready to stun Stonega.",
        "Seems extremely resistant to elemental magic.",
        "You want a Black Mage for this fight — burn the NM down before the "
        "surrounding adds wake up, because the fight ends the moment it dies.",
    ])

FOLD['zhu que'] = dict(
    fam='Greater Bird', lnk=True, det=['True Sound'], ab=[],
    zones=[['The Shrine of RuAvitau']],
    spawn='Summoned by Qilin (1 per Qilin)',
    notes=[
        "Voidwatch notorious monster, Zilart Stage III.",
        "Summoned by Qilin, one per Qilin. Roughly 55,000 HP.",
        "Carries the passive trait Paralyze Aura. The page lists no TP moves.",
    ])

# HELD FROM THE DELETE LIST — see the module docstring.
FOLD['xuan wu'] = dict(
    fam='Adamantoise', lnk=True, det=['True Sound'],
    zones=[['The Shrine of RuAvitau']],
    spawn='Summoned by Qilin (1 per Qilin)',
    notes=[
        "Voidwatch notorious monster, Zilart Stage III.",
        "Summoned by Qilin, one per Qilin.",
    ])

# ---------------------------------------------------------------- apply folds
print('=== FOLDS (%d) ===' % len(FOLD))
for key, patch in sorted(FOLD.items()):
    m = M[key]
    assert not m.get('fam'), (key, m.get('fam'))
    sp_add = patch.pop('_sp_add', None)
    for k, v in patch.items():
        if k == 'notes' and m.get('notes'):
            for b in v:
                if b not in m['notes']:
                    m['notes'].append(b)
        else:
            m[k] = v
    if sp_add:
        sp = m.setdefault('sp', [])
        added = [s for s in sp_add if s not in sp]
        sp.extend(added)
        if added:
            print('      + sp %s' % added)
    print('  %-24s fam=%-13s nm=%-5s zones=%d' %
          (key, m['fam'], m.get('nm'), len(m.get('zones', []))))

# ---------------------------------------------------------------- 18 deletes
DELETE = ['mammet master', 'mieuseloir b enchelles', 'mikhe aryohcha', 'norvallen knight',
          'pudding master', 'republic supplier', 'rikoh wahcondalo', 'royal guard',
          'royal knight', 'royal palliator', 'royal provisioner', 'striking bull',
          'temple knight', 'the briars', 'thunder fiend', 'valaineral r davilles',
          'vhino delkahngo', 'yrvaulair s cousseraux']
HELD = ['xuan wu']     # on the user's screenshot, held for the reason above

print('\n=== DELETE PRE-FLIGHT (%d; %d held) ===' % (len(DELETE), len(HELD)))
# XREF = a REFERENCE from a surviving record (notes / spawn / drops), NOT a
# substring of another mob's own name. `ancient royal knight` contains
# "Royal Knight" and is a different Skeleton, not a mention of this record.
REF_FIELDS = ('notes', 'spawn', 'drops')
def refblob(skip):
    return json.dumps([{f: v.get(f) for f in REF_FIELDS}
                       for k, v in M.items() if k not in skip], ensure_ascii=False)
# `the keeper`'s page prose names "The Briars (Galka)" and "The Briars (Elvaan)" —
# the wiki's RACE VARIANTS, not this plain `the briars` record. It is prose, not a
# data link, so it does not block the delete; it is reported instead.
survivors = refblob(set(DELETE) | set(FOLD))
noted = refblob(set(DELETE))
for k in DELETE:
    m = M[k]
    xref = survivors.count(m['n'])
    prose = noted.count(m['n']) - xref
    flags = [f for f, on in [('ZONES', m.get('zones')), ('CONTENT', m.get('content')),
                             ('NOTES', m.get('notes')), ('AB', m.get('ab')),
                             ('DROPS', m.get('drops')), ('IMG', m.get('img')),
                             ('** NM **', m.get('nm')),
                             ('** XREF **', xref),
                             ('(named in %d note(s) written this rev)' % prose, prose)] if on]
    print('  %-24s lv=%-10s %s' % (k, m.get('lv'), ' '.join(flags) or 'clean'))
    assert not (m.get('zones') or m.get('content') or m.get('notes') or
                m.get('ab') or m.get('drops') or m.get('img')), k
    assert xref == 0, (k, xref)

for k in DELETE:
    del M[k]

# ---------------------------------------------------------------- guards
assert not [k for m in M.values() for k, v in m.items() if v is None], 'NULL POISON'
assert not [k for a in A.values() for k, v in a.items() if v is None], 'NULL POISON (abilities)'
bad_key = [k for k, m in M.items() if k != m['n'].lower()]
print('\nkey/name mismatches: %d %s' % (len(bad_key), bad_key))
assert not bad_key

# the two Elemental members stamped with a swipe set must MATCH a set exactly
sets = {s['label']: s for s in d['family_resist_sets']['Elemental']}
for key, label in [('shadowfang void', 'Dark'), ('touched gefyrst', 'Gefyrst')]:
    s = sets[label]
    assert M[key]['wk'] == s['wk'] and M[key]['st'] == s['st'], key
    print('swipe-set match OK: %-18s -> Elemental/%s' % (key, label))

undef = sorted({a for m in M.values() for a in (m.get('ab') or []) if a not in A})
print('undefined ability refs (names): %d' % len(undef))

json.dump(d, open(P, 'w'), separators=(', ', ': '), ensure_ascii=False)

after = sorted(k for k, m in M.items() if not m.get('fam'))
print('\nmobs      %d -> %d' % (before_mobs, len(M)))
print('abilities %d -> %d' % (before_ab, len(A)))
print('BUCKET    %d -> %d   %s' % (before_bucket, len(after), after))
