#!/usr/bin/env python3
"""
REV 399 — 15 more Beastmaster familiars. Runs AFTER proc_rev398_bstpets.py.

THREE THINGS THIS BATCH TURNED UP THAT ARE WORTH MORE THAN THE 15 PAGES:

1. TWO FAMILIAR PAGES DISAGREE ABOUT THE SAME MOVE, AND THE BESTIARY SETTLES IT.
   `Flytrap Familiar` says Gloeosuccus is single-target and Palsy Pollen is a cone.
   `Voracious Audrey` — the HQ version of the same familiar — says the exact
   opposite. mobs.json defines both moves independently: Gloeosuccus is
   `tgt: Cone AoE`, Palsy Pollen is `tgt: Single`. **Audrey is right and the
   Flytrap Familiar page has the two swapped**, which means rev 398 copied that
   error in. Fixed retroactively here.
   Same shape twice more: `Numbing Noise` (Eft "AoE" vs Allie "single target";
   the def says Cone AoE) and `Filamented Hold` (Mite "single target" vs Lars
   "cone"; the def says Cone AoE). In all three the pet pages are loose about
   target shape and the ability table is not.
   => THE BESTIARY ABILITY TABLE IS A THIRD SOURCE THAT CAN ADJUDICATE BETWEEN
      TWO FAMILIAR PAGES. Use it whenever two pages describe one move differently.

2. TWO PET LEVEL CAPS CONFLICT WITH THE JUG STRING. `Chopsuey Chucky` and
   `Amigo Sabotender` both carry cap 85 from the "· Lv a-b" suffix rev 398 split
   out of `sub`, but their own pages print 75. The familiar page is the specific
   source and wins, the same way a mob page beats a category table. Both flagged.

3. `Coldblood Como` (HQ Lizard) has SEVEN moves where `Lizard Familiar` has
   eight — the HQ has no Baleful Gaze. Recorded as printed, not reconciled.
"""
import json, os

P = 'app/src/main/assets/jobs.json'
if not os.path.exists(P):
    P = 'android/' + P
d = json.load(open(P, encoding='utf-8'))
pets = d['pets']['9']
by_name = {p['n']: p for p in pets}

def R(n, c, desc, i=None):
    r = {'n': n, 'c': c, 'd': desc}
    if i:
        r['i'] = i
    return r

ANTLION_KIT = [
    R('Sandpit', '2 charges', 'Single target Bind.'),
    R('Sandblast', '1 charge', 'Area-of-effect Blind.'),
    R('Venom Spray', '2 charges', 'Frontal-cone Poison.'),
    R('Mandibular Bite', '1 charge', 'Single target attack.'),
]
BEETLE_KIT = [
    R('Spoil', '1 charge', 'Single target STR down.'),
    R('Rhino Guard', '1 charge', 'The pet gains an Evasion boost.'),
    R('Rhino Attack', '1 charge', 'Single target Knockback.'),
    R('Power Attack', '1 charge', 'Single target damage.'),
    R('Hi-Freq Field', '2 charges', 'Cone Evasion down.'),
]
RABBIT_KIT = [
    R('Whirl Claws', '1 charge', 'Area-of-effect damage.'),
    R('Dust Cloud', '1 charge', 'Single target Blind.'),
    R('Foot Kick', '1 charge', 'Single target damage.'),
]
SHEEP_KIT = [
    R('Sheep Charge', '1 charge', 'Single target attack with Knockback.'),
    R('Lamb Chop', '1 charge', 'Single target critical attack.'),
    R('Rage', '2 charges', 'The pet gains Berserk.'),
    R('Sheep Song', '2 charges', 'Area-of-effect Sleep.'),
]
# Filamented Hold: Mite's page says single target, Lars' says cone. The ability table
# says Cone AoE, so the shape below follows the table and the magnitude is left off,
# because the two sources disagree about that too (25% on the page, ~50% in the table).
DIREMITE_KIT = [
    R('Grapple', '1 charge', 'Fan-shaped damage attack.'),
    R('Spinning Top', '1 charge', 'Area-of-effect damage attack.'),
    R('Double Claw', '1 charge', 'Single target attack.'),
    R('Filamented Hold', '2 charges', 'Cone Slow.'),
]
MANDY_KIT = [
    R('Head Butt', '1 charge', 'Single target damage with Knockback.'),
    R('Scream', '1 charge', 'Area-of-effect MND down.'),
    R('Dream Flower', '2 charges', 'Area-of-effect Sleep.'),
    R('Wild Oats', '1 charge', 'Single target VIT down.'),
    R('Leaf Dagger', '1 charge', 'Single target damage, possible Poison.'),
]
TIGER_KIT = [
    R('Claw Cyclone', '1 charge', 'Area-of-effect damage.'),
    R('Razor Fang', '1 charge', 'Single target damage.'),
    R('Roar', '2 charges', 'Area-of-effect Paralyze.'),
]
FLY_KIT = [
    R('Cursed Sphere', '1 charge', 'Area-of-effect damage.'),
    R('Venom', '1 charge', 'Cone attack, damage and Poison.'),
]
EFT_KIT = [
    R('Geist Wall', '1 charge', 'Area-of-effect Dispel.'),
    R('Toxic Spit', '2 charges', 'Single target Poison.'),
    R('Numbing Noise', '1 charge', 'Cone Stun.'),   # see the header note
    R('Nimble Snap', '1 charge', 'Single target damage.'),
    R('Cyclotail', '1 charge', 'Area-of-effect damage.'),
]
# Gloeosuccus / Palsy Pollen shapes per the ability table, not the Flytrap Familiar page.
FLYTRAP_KIT = [
    R('Gloeosuccus', '2 charges', 'Frontal-cone Slow.'),
    R('Palsy Pollen', '1 charge', 'Single target Paralyze.'),
    R('Soporific', '1 charge', 'Area-of-effect Sleep.'),
]

DATA = {
    'Antlion Familiar':  dict(fam='Antlion', lvl='38', cap='50', ready=ANTLION_KIT),
    'Beetle Familiar':   dict(fam='Beetle', lvl='38', cap='45', ready=BEETLE_KIT),
    'Keeneared Steffi':  dict(fam='HQ Rabbit', lvl='43', cap='55', ready=RABBIT_KIT,
        notes=['Compared with the Funguar familiar, Steffi falls well short on damage and TP '
               'moves but is much cheaper — better for soloing, or whenever you do not actually '
               'need big damage out of the pet.']),
    'Lullaby Melodia':   dict(fam='HQ Sheep', lvl='43', cap='55', ready=SHEEP_KIT,
        notes=['Sheep are very strong DPS pets and Rage sends that through the roof — but Rage '
               'also makes the sheep the centre of the mob\u2019s attention and gets it killed. '
               'Wants a very good tank.']),
    'Mite Familiar':     dict(fam='Diremite', lvl='43', cap='55', ready=DIREMITE_KIT),
    'Flowerpot Ben':     dict(fam='HQ Mandragora', lvl='51', cap='63', ready=MANDY_KIT),
    'Saber Siravarde':   dict(fam='HQ Tiger', lvl='51', cap='63', ready=TIGER_KIT),
    'Coldblood Como':    dict(fam='HQ Lizard', lvl='53', cap='65', ready=[
        R('Blockhead', '1 charge', 'Single target damage plus Knockback.'),
        R('Secretion', '1 charge', 'Evasion boost.'),
        R('Fireball', '1 charge', 'Area-of-effect fire damage.'),
        R('Tail Blow', '1 charge', 'Single target damage.'),
        R('Plague Breath', 'Not available via Ready', 'Area-of-effect cone Poison.'),
        R('Brain Crush', '1 charge', 'Single target damage.'),
        R('Infrasonics', '2 charges', 'Area-of-effect cone Evasion down.'),
    ]),
    'Shellbuster Orob':  dict(fam='HQ Fly', lvl='53', cap='65', ready=FLY_KIT,
                              traits=['Occasionally uses Double Attack']),
    'Voracious Audrey':  dict(fam='HQ Flytrap', lvl='53', cap='75', ready=FLYTRAP_KIT),
    'Ambusher Allie':    dict(fam='HQ Eft', lvl='58', cap='75', ready=EFT_KIT),
    'Chopsuey Chucky':   dict(fam='HQ Antlion', lvl='63', cap='75',
                              hp='3,182 (level 75)', ready=ANTLION_KIT),
    'Lifedrinker Lars':  dict(fam='HQ Diremite', lvl='63', cap='75', ready=DIREMITE_KIT),
    'Panzer Galahad':    dict(fam='HQ Beetle', lvl='63', cap='75', ready=BEETLE_KIT),
    'Amigo Sabotender':  dict(fam='Sabotender', lvl='75', cap='75', hp='3,182 (level 75)',
        ready=[
            R('1000 Needles', '3 charges',
              'Deals exactly 1000 damage, split evenly between every target in the area.'),
            R('Needleshot', '1 charge', 'Single target attack.'),
        ]),
}

print('=== 15 MORE BEASTMASTER FAMILIARS ===')
conflicts = []
for name, fields in DATA.items():
    p = by_name.get(name)
    assert p is not None, 'not in the roster: %s' % name
    # the jug string's level band vs the familiar page's own columns
    for k in ('lvl', 'cap'):
        if p.get(k) and fields.get(k) and p[k] != fields[k]:
            conflicts.append((name, k, p[k], fields[k]))
    for k, v in fields.items():
        p[k] = v
    print('  %-20s %-16s lv %-3s cap %-3s  %d ready%s'
          % (name, fields['fam'], fields['lvl'], fields['cap'], len(fields['ready']),
             '  +notes' if 'notes' in fields else ''))

if conflicts:
    print('\n  LEVEL-BAND CONFLICTS — the familiar page wins over the jug string:')
    for n, k, was, now in conflicts:
        print('    %-20s %s  jug string %s  ->  page %s' % (n, k, was, now))

# ------------------------------------------------- retro-fix from rev 398
# The Flytrap Familiar page has Gloeosuccus and Palsy Pollen swapped; the ability
# table and the HQ page both disagree with it. Rev 398 copied the page.
ff = by_name['Flytrap Familiar']
before = [(r['n'], r['d']) for r in ff['ready']]
ff['ready'] = [
    R('Gloeosuccus', '2 charges', 'Frontal-cone Slow.'),
    R('Palsy Pollen', '1 charge', 'Single target Paralyze.'),
    R('Soporific', '1 charge', 'Area-of-effect Sleep.'),
]
print('\n  RETRO-FIX Flytrap Familiar (rev 398 copied its page\'s swapped shapes):')
for (n, was), r in zip(before, ff['ready']):
    if was != r['d']:
        print('    %-14s %-28s -> %s' % (n, was, r['d']))

# ------------------------------------------------- names + guards
NAME_FIX = {'1000 Needles': '1,000 Needles', 'Plague Breath': 'Plaguebreath'}
renamed = 0
for p in pets:
    if 'ready' in p and p.get('sections'):
        p['sections'] = [s for s in p['sections'] if s['t'] != 'Ready']
    for r in (p.get('ready') or []):
        if r['n'] in NAME_FIX:
            r['n'] = NAME_FIX[r['n']]; renamed += 1
print('\nability names normalised to the bestiary vocabulary: %d' % renamed)

ABIL = json.load(open(os.path.join(os.path.dirname(P), 'mobs.json'), encoding='utf-8'))['abilities']
unmatched = sorted({it['n'] for p in pets for sec in (p.get('sections') or []) for it in sec['items']
                    if it['n'] not in ABIL} |
                   {r['n'] for p in pets for r in (p.get('ready') or []) if r['n'] not in ABIL})
print('pet ability names with no bestiary definition: %d %s' % (len(unmatched), unmatched))
assert not unmatched
assert not [k for p in pets for k, v in p.items() if v is None], 'NULL POISON'
BST_ONLY = {'fam', 'job', 'lvl', 'cap', 'hp', 'dmg', 'tp', 'dur', 'traits', 'notes', 'ready'}
assert not [p['n'] for p in d['pets']['15'] if BST_ONLY & set(p)], 'a Summoner avatar was modified'

done = [p['n'] for p in pets if 'ready' in p]
todo = [p['n'] for p in pets if 'ready' not in p]
print('\nBST familiars with a Ready list recorded: %d of %d' % (len(done), len(pets)))
print('still to do (%d): %s%s' % (len(todo), ', '.join(todo[:10]), ' …' if len(todo) > 10 else ''))
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('written: %s' % P)
