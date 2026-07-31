#!/usr/bin/env python3
"""
REV 402 — thirteen more jug familiars. Runs after 398, 399, 400 and 401.

THE LEVEL-CAP READING (rule 473) HOLDS UP AND GAINS A NEW WRINKLE
-----------------------------------------------------------------
Eleven of the thirteen pages print a main Level Cap figure, and ELEVEN OF
ELEVEN match the cap already stored from the jug string (116 / 119 / 117 /
118 / 103 / 117 / 119 / 119 / 115 / 113 — plus Gussy Hachirobe, see below).
That takes the running tally to 18 of 20.  Rule 473 is now settled beyond
argument.

NEW: the parenthetical is NOT the constant 119 it looked like.  Droopy
Dortwin prints "103 (118)".  So the parenthetical is a per-familiar
footnote of its own, not a fixed page constant — which independently kills
the rev-400 worry that the two figures might be swapped.

ONE REAL CONFLICT, resolved by rule 467 (the familiar page beats the jug
string): `Gussy Hachirobe` 118 -> 119.

THREE PLACES WHERE THE PET PAGE AND THE BESTIARY ABILITY TABLE DISAGREE
-----------------------------------------------------------------------
Recorded AS PRINTED on the pet page and flagged; NOT silently reconciled,
because rule 466 adjudicates *between two pet pages*, and this is a
different kind of disagreement — one source against the other, once each.

  1. Choke Breath   pet page: "Earth elemental"  |  bestiary: Wind-based
  2. Corrosive Ooze pet page: "Fire elemental"   |  bestiary: el = Water
  3. Spider Web     pet page: "3% Slow"          |  bestiary: "inflicts Slow II"
     (Slow II is ~30%; the page's 3% looks like a dropped zero, but writing
     30% would be a guess, so it goes in as printed.)

ONE KIT SHRINK WORTH THE USER'S EYES
------------------------------------
`Colibri Familiar` already carried an old NAME-ONLY Ready list of three —
Pecking Flurry, Snatch Morsel, Feather Tickle.  Its Lv.99 stat-block page
lists ONE (Pecking Flurry), and `Choral Leera`, the other Lv.99 Colibri,
lists the same one.  Every other overlap this batch runs the other way (the
stat-block page is a superset: Hippogryph +Hoof Volley, Yellow Beetle
+Rhinowrecker; Porter Crab and Spider match exactly), so a SHRINK is the
odd case.  Taken from the page per standing practice, and the two dropped
names are recorded here so nothing is lost.

`Daring Roland` and `Energized Sefina` are the "?" pages — no job, no level
cap, no attack/defence modifiers, no stat block.  A "?" is not data, so
those keys are simply not written (their jug-string caps stand).

Special Traits are icon-only except two textual entries, which ARE taken:
Daring Roland "Treasure Hunter I" and Generous Arthur "MDB +40" /
"En-Slow (15% Slow)".  (rule 472)

Melee Type is icon-only on this page layout, so no `dmg` is written — same
ruling as the ability-element icons.

One normalisation to the bestiary vocabulary: High-Frequency Field ->
Hi-Freq Field.
"""
import json, os

P = 'app/src/main/assets/jobs.json'
if not os.path.exists(P):
    P = 'android/' + P
d = json.load(open(P, encoding='utf-8'))
pets = d['pets']['9']
by_name = {p['n']: p for p in pets}


def R(n, c, desc, sc=None):
    r = {'n': n, 'c': c, 'd': desc}
    if sc:
        r['sc'] = sc
    return r


DATA = {
    'Caring Kiyomaro': dict(fam='Raaz', eco='Beast', job='Monk', tp='75', cap='116',
        atk='+10%', deff='-20%',
        stats={'hp': '6,346', 'acc': '858', 'atk': '818', 'eva': '706', 'def': '779'},
        ready=[
            R('Sweeping Gouge', '1 charge',
              'Delivers a twofold attack to enemies within a fan-shaped area. Additional '
              'effect: -25% Defense for 60 seconds. Damage varies with TP.', 'Induration'),
            R('Zealous Snort', '3 charges',
              '+25% Haste, +25 magic defense bonus, and increases the likelihood of both '
              'countering and guarding for pet and Beastmaster. Duration of effect varies '
              'with TP.'),
        ]),

    'Choral Leera': dict(fam='Colibri', eco='Bird', job='Red Mage', tp='70', cap='119',
        stats={'hp': '5,496', 'acc': '925', 'atk': '750', 'eva': '754', 'def': '915'},
        ready=[
            R('Pecking Flurry', '1 charge', 'Delivers a fourfold attack. Damage varies with TP.',
              'Transfixion'),
        ]),

    'Colibri Familiar': dict(fam='Colibri', eco='Bird', job='Red Mage', tp='70', cap='117',
        stats={'hp': '5,308', 'acc': '915', 'atk': '750', 'eva': '744', 'def': '915'},
        ready=[
            R('Pecking Flurry', '1 charge', 'Delivers a fourfold attack. Damage varies with TP.',
              'Transfixion'),
        ]),

    'Cursed Annabelle': dict(fam='Antlion', eco='Vermin', job='Warrior', tp='81', cap='118',
        deff='+30%',
        stats={'hp': '5,184', 'acc': '886', 'atk': '793', 'eva': '704', 'def': '1,229'},
        ready=[
            R('Mandibular Bite', '1 charge', 'Damage varies with TP.', 'Detonation'),
            R('Sandblast', '2 charges',
              'Blinds (-40 Accuracy) all enemies within range. Duration of effect varies with TP.'),
            R('Sandpit', '1 charge', 'Binds an enemy. Duration of effect varies with TP.'),
            R('Venom Spray', '2 charges',
              'Poisons (31 damage/tic) enemies within a fan-shaped area. Duration of effect '
              'varies with TP.'),
        ]),

    'Daring Roland': dict(fam='Hippogryph', eco='Bird', tp='73',
        traits=['Treasure Hunter I'],
        ready=[
            R('Back Heel', '1 charge', 'Damage varies with TP.', 'Reverberation'),
            R('Jettatura', '3 charges',
              'Terrorizes enemies within a fan-shaped area. Duration of effect varies with TP, '
              'from 15 to 25 seconds.'),
            R('Choke Breath', '1 charge',
              'Deals Earth elemental damage to enemies within a fan-shaped area. Additional '
              'effect: Paralysis and Silence. Duration of effect varies with TP.'),
            R('Fantod', '2 charges',
              'Increases the damage of the pet\u2019s next attack by an unstated amount. '
              'Duration of effect varies with TP.'),
            R('Hoof Volley', '3 charges', 'Deals physical damage. Damage varies with TP.',
              'Fragmentation'),
            R('Nihility Song', '1 charge',
              'Removes one beneficial magic effect from all enemies around the pet. Area varies '
              'with TP.'),
        ]),

    'Droopy Dortwin': dict(fam='Rabbit', eco='Beast', job='Warrior', tp='75', cap='103',
        stats={'hp': '5,500', 'acc': '848', 'atk': '775', 'eva': '689', 'def': '929'},
        ready=[
            R('Foot Kick', '1 charge', 'Critical hit rate varies with TP.', 'Reverberation'),
            R('Dust Cloud', '1 charge',
              'Deals Earth elemental damage to enemies within a fan-shaped area. Additional '
              'effect: Blind. Damage varies with TP.'),
            R('Whirl Claws', '1 charge',
              'Deals physical damage to enemies within range. Area of effect varies with TP.',
              'Impaction'),
            R('Wild Carrot', '2 charges',
              'Restores HP of all party members within area of effect. HP restored varies with TP.'),
        ]),

    'Energized Sefina': dict(fam='Yellow Beetle', eco='Vermin', tp='73',
        ready=[
            R('Power Attack', '1 charge', 'Critical hit rate varies with TP.', 'Reverberation'),
            R('Hi-Freq Field', '2 charges',
              '-40 Evasion for enemies within a fan-shaped area. Area of effect varies with TP. '
              'Duration 3 minutes.'),
            R('Rhino Attack', '1 charge', 'Damage varies with TP.', 'Detonation'),
            R('Rhino Guard', '1 charge', '+25% Evasion. Duration of effect varies with TP.'),
            R('Spoil', '1 charge',
              '-20% Strength to an enemy, decaying over time. Duration of effect varies with TP, '
              'from 3 minutes to 9 minutes.'),
            R('Rhinowrecker', '2 charges',
              'Deals physical damage to all enemies in a fan-shaped area in front of the pet. '
              'Additional effect: decreases defense. Damage varies with TP.',
              'Fusion / Transfixion'),
        ]),

    'Fleet Reinhard': dict(fam='Raptor', eco='Lizard', job='Warrior', tp='85', cap='117',
        atk='+30%', deff='-10%',
        stats={'hp': '5,184', 'acc': '856', 'atk': '1,028', 'eva': '727', 'def': '849'},
        ready=[
            R('Scythe Tail', '1 charge', 'Additional effect: Stun. Damage varies with TP.',
              'Liquefaction'),
            R('Ripper Fang', '1 charge', 'Damage varies with TP.', 'Induration'),
            R('Chomp Rush', '3 charges',
              'Additional effect: 25% Slow. Duration varies with TP.', 'Darkness / Gravitation'),
        ]),

    'Fluffy Bredo': dict(fam='Acuex', eco='Amorph', job='Black Mage', tp='75', cap='119',
        atk='+30%',
        stats={'hp': '5,744', 'acc': '889', 'atk': '1,115', 'eva': '695', 'def': '949'},
        ready=[
            R('Foul Waters', '2 charges',
              'Deals Water elemental damage to enemies in a fan-shaped area. Additional effects: '
              'Drown (-33 STR and 15 damage/tic) and Weight for 60 seconds. Damage varies with TP.'),
            R('Pestilent Plume', '2 charges',
              'Deals Darkness elemental damage in a fan-shaped area. Additional effects: Plague '
              '(-50 TP/tic), Blind (-50 Accuracy) and -25 magic defense bonus for 60 seconds. '
              'Damage varies with TP.'),
        ]),

    'Generous Arthur': dict(fam='Slug', eco='Amorph', job='Warrior', tp='75', cap='119',
        atk='-20%', deff='+30%',
        traits=['MDB +40', 'En-Slow (15% Slow)'],
        stats={'hp': '4,860', 'acc': '866', 'atk': '635', 'eva': '698', 'def': '1,241'},
        ready=[
            R('Purulent Ooze', '2 charges',
              'Deals Water elemental damage to enemies within a fan-shaped area. Additional '
              'effects: Bio (-10% Attack and 15 damage/tic) and -10% HP. Damage varies with TP. '
              'Duration 70 seconds.'),
            R('Corrosive Ooze', '3 charges',
              'Deals Fire elemental damage to enemies within area of effect. Additional effect: '
              '-33% Attack and Defense. Damage varies with TP. Duration 60-90 seconds.'),
        ]),

    'Gussy Hachirobe': dict(fam='Spider', eco='Vermin', job='Warrior', tp='75', cap='119',
        atk='+30%', deff='-10%',
        stats={'hp': '5,702', 'acc': '911', 'atk': '1,025', 'eva': '704', 'def': '849'},
        ready=[
            R('Sickle Slash', '1 charge', 'Critical hit rate varies with TP.', 'Transfixion'),
            R('Acid Spray', '1 charge',
              'Deals Water elemental damage. Additional effect: Poison (31 damage/tic) for 3 '
              'minutes. Damage varies with TP.'),
            R('Spider Web', '2 charges',
              '3% Slow for enemies within range. Duration varies with TP.'),
        ]),

    'Headbreaker Ken': dict(fam='Fly', eco='Vermin', job='Warrior', tp='75', cap='115',
        stats={'hp': '5,184', 'acc': '866', 'atk': '791', 'eva': '737', 'def': '948'},
        ready=[
            R('Cursed Sphere', '1 charge',
              'Deals Dark elemental damage to enemies within area of effect. Damage varies with TP.'),
            R('Venom', '1 charge',
              'Deals Water elemental damage to enemies within a fan-shaped area. Additional '
              'effect: Poison. Duration of effect varies with TP.'),
            R('Somersault', '1 charge', 'Damage varies with TP.', 'Compression'),
        ]),

    'Herald Henry': dict(fam='Crab', eco='Aquan', job='Paladin', tp='75', cap='113',
        atk='-10%', deff='+20%',
        stats={'hp': '5,612', 'acc': '860', 'atk': '690', 'eva': '690', 'def': '1,224'},
        ready=[
            R('Bubble Shower', '1 charge',
              'Deals Water elemental damage to enemies within area of effect. Additional effect: '
              'lowers STR. Area of effect varies with TP.'),
            R('Bubble Curtain', '3 charges',
              '-50% magic damage taken for pet and Beastmaster. Duration of effect varies with TP.'),
            R('Big Scissors', '1 charge',
              'Deals physical damage. Critical hit rate varies with TP.', 'Scission'),
            R('Scissor Guard', '1 charge',
              '+100% Defense for pet and Beastmaster. Duration of effect varies with TP.'),
            R('Metallic Body', '1 charge',
              'Gives the effect of a roughly 200 HP Stoneskin for pet and Beastmaster. Duration '
              'of effect varies with TP.'),
        ]),
}
for f in DATA.values():
    if 'deff' in f:
        f['def'] = f.pop('deff')

# ------------------------------------------------- apply
print('=== REV 402 — 13 MORE JUG FAMILIARS ===')
cap_changes = []
for name, fields in sorted(DATA.items()):
    p = by_name[name]
    stored = p.get('cap')
    page_cap = fields.get('cap')
    for k, v in fields.items():
        p[k] = v
    if page_cap is None:
        note = 'page prints "?" — jug-string cap %s kept' % stored
    elif stored == page_cap:
        note = 'cap matches the jug string'
    else:
        note = 'CAP CHANGED %s -> %s  (rule 467)' % (stored, page_cap)
        cap_changes.append((name, stored, page_cap))
    print('  %-18s %-14s %-9s cap %-5s %d ready   %s'
          % (name, fields['fam'], fields['eco'], page_cap or '-', len(fields['ready']), note))

print('\ncap conflicts resolved in favour of the familiar page: %d %s' % (len(cap_changes), cap_changes))

# ------------------------------------------------- the Colibri kit shrink
prior = [i['n'] for s in (by_name['Colibri Familiar'].get('sections') or [])
         if s['t'] == 'Ready' for i in s['items']]
kept = [r['n'] for r in DATA['Colibri Familiar']['ready']]
dropped = [n for n in prior if n not in kept]
print('\n=== KIT SHRINK — Colibri Familiar ===')
print('  old name-only list: %s' % ', '.join(prior))
print('  Lv.99 stat-block page: %s' % ', '.join(kept))
print('  dropped: %s   (Choral Leera, the other Lv.99 Colibri, lists the same single move)'
      % ', '.join(dropped))

print('\n=== PET PAGE vs BESTIARY ABILITY TABLE — recorded as printed, NOT reconciled ===')
for move, page, table in (
        ('Choke Breath', 'Earth elemental', 'Wind-based'),
        ('Corrosive Ooze', 'Fire elemental', 'el = Water'),
        ('Spider Web', '3% Slow', 'inflicts Slow II (~30%)')):
    print('  %-15s page: %-16s | bestiary: %s' % (move, page, table))

# ------------------------------------------------- guards
for p in pets:
    if 'ready' in p and p.get('sections'):
        p['sections'] = [s for s in p['sections'] if s['t'] != 'Ready']

ABIL = json.load(open(os.path.join(os.path.dirname(P), 'mobs.json'), encoding='utf-8'))['abilities']
unmatched = sorted({it['n'] for p in pets for sec in (p.get('sections') or []) for it in sec['items']
                    if it['n'] not in ABIL} |
                   {r['n'] for p in pets for r in (p.get('ready') or []) if r['n'] not in ABIL})
print('\npet ability names with no bestiary definition: %d %s' % (len(unmatched), unmatched))
assert not unmatched

assert not [k for p in pets for k, v in p.items() if v is None], 'NULL POISON'
for p in pets:
    st = p.get('stats')
    if st:
        assert set(st) <= {'hp', 'acc', 'atk', 'eva', 'def'} and all(isinstance(v, str) for v in st.values())
BST_ONLY = {'fam', 'job', 'lvl', 'cap', 'hp', 'dmg', 'tp', 'dur', 'traits', 'notes', 'ready',
            'eco', 'atk', 'def', 'stats'}
assert not [p['n'] for p in d['pets']['15'] if BST_ONLY & set(p)], 'a Summoner avatar was modified'

done = [p['n'] for p in pets if 'ready' in p]
todo = [p['n'] for p in pets if 'ready' not in p]
sc = [(p['n'], r['n'], r['sc']) for p in pets for r in (p.get('ready') or []) if r.get('sc')]
stat_blocks = [p['n'] for p in pets if p.get('stats')]
print('ready moves carrying a skillchain: %d' % len(sc))
print('familiars carrying a stat block: %d' % len(stat_blocks))
print('\nBST familiars with a Ready list recorded: %d of %d' % (len(done), len(pets)))
print('still to do (%d): %s' % (len(todo), ', '.join(todo)))

json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('written: %s' % P)
