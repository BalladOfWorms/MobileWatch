#!/usr/bin/env python3
"""
REV 400 — 20 more Beastmaster familiars. Runs after 398 and 399.

SIXTEEN come from the usual familiar layout. FOUR (Acuex Familiar, Aged Angus,
Alluring Honey, Amiable Roche) come from the Lv.99 jug pages, which use a
completely different, richer layout and are why the schema grew this rev:
`eco` (the Type column), `atk`/`def` (the Attack ± / Defense ± modifiers), a
`stats` block measured at the level cap, and `sc` (skillchain) on a Ready move.

TWO THINGS RECORDED AS PRINTED AND FLAGGED RATHER THAN "CORRECTED":

1. THE TP/HIT DECIMAL. Some pages print 7.5 / 7.3 / 8.5 and others print
   75 / 73 / 85 for what is plainly the same figure — and the Lv.99 pages print
   a flat 75 for all four. That is now six-plus instances across two different
   page layouts, so it is a convention or a rendering difference, not a typo on
   one page, and it is not mine to resolve. Every value goes in exactly as the
   page shows it.

2. TWO LEVEL CAPS ON THE Lv.99 PAGES DISAGREE WITH THE JUG STRING, AND THE
   READING ITSELF IS UNCERTAIN. That table prints "119 (119)" / "110 (119)",
   where the parenthetical is a superscript footnote marker rather than a value.
   Acuex (119) and Roche (110) match what the jug string already gave; Aged
   Angus reads 119 against a stored 104 and Alluring Honey 119 against 115.
   Where a page beats the jug string unambiguously the page wins (rev 399 did
   exactly that twice) — but here the ambiguity is in how to read the column, so
   the stored values stand and the conflict is reported instead.

ALSO NOT TRANSCRIBED: the Lv.99 pages carry a Special Traits column that is
almost entirely ICONS with percentages beside them — weapon-type and elemental
resistances. Without a labelled reference to match the icons against, writing
them down would be guessing, so only the one textual entry (Alluring Honey's
"MDB -50%") is recorded.
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

WARRIOR3 = ['Double Attack', 'Fencer', 'Critical Attack Bonus']
MONK_KIT = ['Guard', 'Counter', 'Kick Attacks', 'Tactical Guard', 'Subtle Blow', 'Max HP Boost']
THIEF_KIT = ['Triple Attack', 'Gilfinder', 'High Evasion', 'Treasure Hunter']

FUNGUAR_KIT = [
    R('Frog Kick', '1 charge', 'Single target attack.'),
    R('Queasyshroom', '1 charge', 'Single target damage and Poison.'),
    R('Silence Gas', '3 charges', 'Frontal-cone dark magic damage and Silence.'),
    R('Numbshroom', '2 charges', 'Single target damage and Paralyze.'),
    R('Spore', '1 charge', 'Single target Paralyze.'),
    R('Dark Spore', '3 charges', 'Frontal-cone dark magic damage and Blind.'),
    R('Shakeshroom', '2 charges', 'Single target damage and Disease.'),
]
LIZARD_KIT = [
    R('Tail Blow', '1 charge', 'Physical damage. Additional effect: Stun.'),
    R('Fireball', '1 charge', 'Fire damage to enemies within an area of effect.'),
    R('Blockhead', '1 charge', 'Physical damage.'),
    R('Brain Crush', '1 charge', 'Physical damage. Additional effect: Silence.'),
    R('Infrasonics', '2 charges', 'Cone attack, Evasion down.'),
    R('Secretion', '1 charge', "Enhances the pet's evasion."),
]
EFT_KIT = [
    R('Geist Wall', '1 charge', 'Area-of-effect Dispel.'),
    R('Numbing Noise', '1 charge', 'Cone Stun.'),
    R('Nimble Snap', '1 charge', 'Single target damage.'),
    R('Cyclotail', '1 charge', 'Area-of-effect damage.'),
    R('Toxic Spit', '2 charges', 'Single target Poison.'),
]
TIGER_KIT = [
    R('Roar', '2 charges', 'Paralyzes every enemy within range of the pet.'),
    R('Razor Fang', '1 charge', 'Physical damage.'),
    R('Claw Cyclone', '1 charge',
      'Physical damage in a fan-shaped area originating from the pet.'),
]
FLYTRAP_KIT = [
    R('Soporific', '1 charge', 'Area-of-effect Sleep.'),
    R('Gloeosuccus', '2 charges', 'Frontal-cone Slow.'),
    R('Palsy Pollen', '1 charge', 'Single target Paralyze.'),
]
PUGIL_KIT = [
    R('Intimidate', '2 charges', 'Reduces the attack speed of enemies.'),
    R('Recoil Dive', '1 charge',
      'Physical damage to enemies in a fan-shaped area originating from the pet.'),
    R('Water Wall', '3 charges', "Enhances the pet's defense."),
]

DATA = {
    'Turbid Toloi': dict(fam='Pugil', job='Warrior', hp='4,912 (level 99)', dmg='Slashing',
        tp='75 / hit', dur='120 min.',
        traits=WARRIOR3 + ['High resistance to Water-based moves'], ready=PUGIL_KIT),
    'Crafty Clyvonne': dict(fam='Coeurl', job='Warrior', hp='4,886 (level 90)', dmg='Slashing',
        tp='7.5 / hit', dur='120 min.',
        traits=WARRIOR3 + ['Enhanced Movement Speed'], ready=[
            R('Chaotic Eye', '1 charge', 'Gaze attack. Silences the enemy.'),
            R('Blaster', '2 charges', 'Not a gaze attack. Paralyzes the enemy.'),
        ]),
    'Dapper Mac': dict(fam='Apkallu', job='Monk', hp='5,542 (level 99)', dmg='Blunt',
        tp='7.0 / hit', dur='120 min.',
        traits=MONK_KIT + ['Store TP', 'Resistant to Water-based attacks and magic',
                           'Reduced Movement Speed'],
        ready=[
            R('Wing Slap', '2 charges', 'Single target damage. Additional effect: Stun.'),
            R('Beak Lunge', '1 charge', 'Single target damage.'),
        ]),
    'Dipper Yuly': dict(fam='Ladybug', job='Thief', hp='4,092 (level 99)', dmg='Slashing',
        tp='73 / hit', dur='120 min.',
        traits=THIEF_KIT + ['Critical Attack Bonus',
                            'Very resistant to Wind-based attacks and magic'],
        ready=[
            R('Sudden Lunge', '2 charges',
              "Knockback damage and Stun. Sacrifices 1% of the pet's HP."),
            R('Spiral Spin', '2 charges', 'Cone damage and Accuracy down.'),
            R('Noisome Powder', '2 charges', "10' area-of-effect 40% Attack down."),
        ]),
    'Flowerpot Merle': dict(fam='Lycopodium', job='Monk', hp='5,216 (level 99)', dmg='Blunt',
        tp='5.7 / hit', dur='180 min.', traits=MONK_KIT, ready=[
            R('Head Butt', '1 charge', 'Single target damage with Knockback.'),
            R('Scream', '1 charge', 'Area-of-effect MND down.'),
            R('Wild Oats', '1 charge', 'Single target VIT down.'),
            R('Leaf Dagger', '1 charge', 'Single target Poison.'),
        ]),
    'Lucky Lulush': dict(fam='Rabbit', job='Warrior', hp='4,912 (level 99)', dmg='Slashing',
        tp='7.3 / hit', dur='120 min.', traits=WARRIOR3, ready=[
            R('Foot Kick', '1 charge', 'Physical damage.'),
            R('Whirl Claws', '1 charge', 'Area damage to enemies within range of the pet.'),
            R('Snow Cloud', '1 charge',
              'Ice damage in a fan-shaped area originating from the pet. '
              'Additional effect: Paralyze.'),
            R('Wild Carrot', '2 charges',
              'Restores the HP of every party member within the area, the pet included. '
              'The amount healed varies with TP.'),
        ]),
    'Nursery Nazuna': dict(fam='Sheep', job='Warrior', hp='5,114 (level 86)', dmg='Slashing',
        tp='8.0 / hit', dur='120 min.', traits=WARRIOR3, ready=[
            R('Lamb Chop', '1 charge', 'Single target physical damage (Blunt).'),
            R('Rage', '2 charges',
              "Enhances the pet's attack by 50% but weakens its defense by 50%."),
            R('Sheep Charge', '1 charge', 'Single target physical damage plus Knockback.'),
            R('Sheep Song', '2 charges', 'Area-of-effect Sleep.'),
        ]),
    'Discreet Louise': dict(fam='Funguar', job='Warrior', hp='4,604 (level 99)', dmg='Slashing',
        tp='85 / hit', dur='120 min.',
        traits=WARRIOR3 + ['Store TP', 'High resistance to Darkness-based moves'],
        ready=FUNGUAR_KIT),
    'Fatso Fargann': dict(fam='Leech', job='Warrior', hp='4,298 (level 99)', dmg='Slashing',
        tp='8.0 / hit', dur='120 min.',
        traits=WARRIOR3 + ['Blunt damage taken -25%',
                           'Resistant to Water-based attacks and magic'],
        ready=[
            R('Suction', '1 charge', 'Single target attack. Additional effect: Stun.'),
            R('Drainkiss', '1 charge', "Single target attack. Steals an enemy's HP."),
            R('Acid Mist', '2 charges',
              'Area-of-effect water damage. Additional effect: weakens attack.'),
            R('TP Drainkiss', '3 charges', "Single target attack. Steals an enemy's TP."),
        ]),
    'Presto Julio': dict(job='Warrior', hp='4,532 (level 93)', dmg='Slashing',
        tp='7.0 / hit', dur='120 min.', traits=WARRIOR3, ready=FLYTRAP_KIT),
    'Audacious Anna': dict(job='Warrior', hp='5,242 (level 95)', dmg='Slashing',
        tp='8.0 / hit', dur='120 min.',
        traits=WARRIOR3 + ['30% Critical Hit Rate'], ready=LIZARD_KIT),
    'Swift Sieghard': dict(fam='Raptor', job='Warrior', hp='4,596 (level 94)', dmg='Slashing',
        tp='8.5 / hit', dur='120 min.',
        traits=WARRIOR3 + ['Enhanced Movement Speed', 'Fire Resistance (Feral Skill)'],
        ready=[
            R('Scythe Tail', '1 charge', 'Single target physical damage plus Stun.'),
            R('Ripper Fang', '1 charge', 'Single target physical damage.'),
            R('Chomp Rush', '3 charges', 'Single target physical damage plus Slow.'),
        ]),
    'Bugeyed Broncha': dict(fam='HQ Eft', job='Warrior', hp='4,912 (level 99)', dmg='Slashing',
        tp='6.8 / hit', dur='120 min.', traits=WARRIOR3, ready=EFT_KIT),
    'Gorefang Hobs': dict(fam='Tiger', job='Warrior', hp='5,218 (level 99)', dmg='Slashing',
        tp='75 / hit', dur='120 min.',
        traits=WARRIOR3 + ['Enhanced Movement Speed'], ready=TIGER_KIT),
    'Gooey Gerard': dict(fam='Slug', job='Warrior', hp='4,298 (level 99)', dmg='Slashing',
        tp='75 / hit', dur='90 min.',
        traits=WARRIOR3 + ['Additional effect: Slow on melee attacks', 'Magic Defense Bonus',
                           'High resistance to Water-based moves'],
        ready=[
            R('Purulent Ooze', '2 charges',
              'Water damage in a fan-shaped area originating from the pet. Additional effects: '
              'Bio, and lowers maximum HP by 10%.'),
            R('Corrosive Ooze', '3 charges',
              'Fire damage to enemies within an area of effect. Additional effect: weakens '
              'attack and defense by 33%.'),
        ]),
    'Crude Raphie': dict(fam='Adamantoise', job='Paladin', hp='4,212 (level 99)', dmg='Slashing',
        tp='7.5 / hit', dur='90 min.',
        traits=['Defense Bonus', 'Decreased Movement Speed',
                'Resistant to most Earth, Water and Thunder-based attacks'],
        ready=[
            R('Tortoise Stomp', '2 charges',
              'Single target damage. Additional effect: weakens Defense.'),
            R('Harden Shell', '2 charges', "Enhances the pet's defense."),
            R('Aqua Breath', '3 charges',
              'Water damage to enemies within a fan-shaped area.'),
        ]),

    # ---- the four Lv.99 jug pages, in the richer layout --------------------
    'Acuex Familiar': dict(fam='Acuex', eco='Amorph', job='Black Mage', tp='75',
        atk='+20%', stats={'hp': '5,558', 'acc': '879', 'atk': '1,031', 'eva': '695', 'def': '949'},
        ready=[
            R('Foul Waters', '2 charges',
              'Water damage to enemies in a fan-shaped area. Additional effects: Drown '
              '(-33 STR and 15 damage per tick) and Weight for 60 seconds. Damage varies with TP.'),
            R('Pestilent Plume', '2 charges',
              'Darkness damage in a fan-shaped area. Additional effects: Plague (-50 TP per tick), '
              'Blind (-50 accuracy) and -25 magic defense bonus for 60 seconds. '
              'Damage varies with TP.'),
        ]),
    'Aged Angus': dict(fam='Crab', eco='Aquan', job='Paladin', tp='75',
        atk='-10%', deff='+20%',
        stats={'hp': '5,434', 'acc': '860', 'atk': '681', 'eva': '690', 'def': '1,224'},
        ready=[
            R('Bubble Shower', '1 charge',
              'Water damage to enemies within an area of effect. Additional effect: STR down. '
              'Area of effect varies with TP.'),
            R('Bubble Curtain', '3 charges',
              '-50% magic damage taken for the pet and the Beastmaster. Duration varies with TP.'),
            R('Big Scissors', '1 charge',
              'Physical damage. Critical hit rate varies with TP.', 'Scission'),
            R('Scissor Guard', '2 charges',
              '+100% Defense for the pet and the Beastmaster. Duration varies with TP.'),
            R('Metallic Body', '3 charges',
              'Gives roughly a 200 HP Stoneskin to the pet and the Beastmaster. '
              'Duration varies with TP.'),
        ]),
    'Alluring Honey': dict(fam='Snapweed', eco='Plantoid', job='Warrior', tp='75',
        deff='+30%', traits=['MDB -50%'],
        stats={'hp': '6,026', 'acc': '886', 'atk': '793', 'eva': '704', 'def': '1,220'},
        ready=[
            R('Tickling Tendrils', '1 charge',
              'Delivers a fivefold attack. Additional effect: Stun. Damage varies with TP.',
              'Impaction'),
            R('Stink Bomb', '2 charges',
              'Earth damage to enemies within an area of effect. Additional effects: Blind and '
              'Paralysis. Duration varies with TP.'),
            R('Nectarous Deluge', '2 charges',
              'Water damage to enemies within an area of effect. Additional effect: Poison. '
              'Duration varies with TP.'),
            R('Nepenthic Plunge', '3 charges',
              'Water damage within a fan-shaped area. Additional effects: Drown (-33 STR and 15 '
              'damage per tick) and Weight. Duration varies with TP, from 60 seconds to about '
              'two and a half minutes.'),
        ]),
    'Amiable Roche': dict(fam='Pugil', eco='Aquan', job='Warrior', tp='75',
        atk='+40%', deff='-10%',
        stats={'hp': '5,184', 'acc': '876', 'atk': '1,108', 'eva': '707', 'def': '855'},
        ready=[
            R('Intimidate', '2 charges', 'Slow for an enemy. Duration varies with TP.'),
            R('Recoil Dive', '1 charge',
              'Physical damage to enemies within a fan-shaped area. Damage varies with TP.',
              'Transfixion'),
            R('Water Wall', '3 charges',
              '+100% Defense for the pet and the Beastmaster. Duration varies with TP.'),
        ]),
}
# `def` is a Python builtin-ish name in a dict literal context, so the four above spell it
# `deff`; map it back to the JSON key here.
for f in DATA.values():
    if 'deff' in f:
        f['def'] = f.pop('deff')

print('=== 20 MORE BEASTMASTER FAMILIARS ===')
for name, fields in DATA.items():
    p = by_name.get(name)
    assert p is not None, 'not in the roster: %s' % name
    for k, v in fields.items():
        p[k] = v
    print('  %-19s %-14s %-11s lv %-4s cap %-4s %d ready%s'
          % (name, fields.get('fam', '(not printed)'), fields.get('eco', ''),
             p.get('lvl'), p.get('cap'), len(fields['ready']),
             '  +stats' if 'stats' in fields else ''))

print('\n  `fam` LEFT UNSET on Presto Julio and Audacious Anna — their pages do not print a')
print('  Familiar column. The jug and the kit both point at the Flytrap and Lizard lines,')
print('  but that is inference, so it is reported rather than written.')

CAP_CONFLICT = [('Aged Angus', '104', '119'), ('Alluring Honey', '115', '119')]
print('\n  LEVEL-CAP READING LEFT ALONE (see the header):')
for n, stored, page in CAP_CONFLICT:
    print('    %-16s stored %s, the Lv.99 table prints %s (%s)' % (n, stored, page, page))

# ---------------------------------------------------------------- guards
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
        assert set(st) <= {'hp', 'acc', 'atk', 'eva', 'def'}, st
        assert all(isinstance(v, str) for v in st.values())
BST_ONLY = {'fam', 'job', 'lvl', 'cap', 'hp', 'dmg', 'tp', 'dur', 'traits', 'notes', 'ready',
            'eco', 'atk', 'def', 'stats'}
assert not [p['n'] for p in d['pets']['15'] if BST_ONLY & set(p)], 'a Summoner avatar was modified'

done = [p['n'] for p in pets if 'ready' in p]
todo = [p['n'] for p in pets if 'ready' not in p]
print('\nBST familiars with a Ready list recorded: %d of %d' % (len(done), len(pets)))
print('still to do (%d): %s%s' % (len(todo), ', '.join(todo[:10]), ' …' if len(todo) > 10 else ''))
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('written: %s' % P)
