#!/usr/bin/env python3
"""
REV 398 — the first 16 Beastmaster familiars filled in.

The 98 BST pets already existed in jobs.json as name + jug and an empty
`sections` list. This adds the rest of what a familiar page publishes, under
optional keys so the other 82 and all 22 Summoner avatars are untouched:

    fam  familiar's monster family        traits[]  notable traits
    job  its job                          ready[]   {n, c charges, d desc, i /bstpet index}
    lvl  level the jug becomes available
    cap  pet level cap                    hp, dmg, tp, dur

`ready` FOLLOWS THE EMPTY-LIST DISCIPLINE from mobs.json: an explicit [] means
the page states the familiar HAS no Ready abilities (Slippery Silas), an absent
key means we have not recorded them yet. JobDb reads `po.has("ready")` to tell
those apart, so the card can say "no Ready abilities" without claiming that for
the 82 pets still to do.

ONE VALUE RECORDED AS PRINTED AND FLAGGED: Mailbuster Cetas' page says
"TP: 75 / Hit". Every sibling page says 7.4 or 7.5. It is almost certainly a
wiki typo for 7.5, but the rule here has always been that the page wins and the
conflict gets reported rather than silently corrected.
"""
import json, os

P = 'app/src/main/assets/jobs.json'
if not os.path.exists(P):
    P = 'android/' + P
d = json.load(open(P, encoding='utf-8'))
pets = d['pets']['9']            # 9 = Beastmaster
by_name = {p['n']: p for p in pets}

def R(n, c, desc, i=None):
    r = {'n': n, 'c': c, 'd': desc}
    if i:
        r['i'] = i
    return r

CRAB_KIT = [
    R('Metallic Body', '1 charge', 'The crab gains a Stoneskin effect.'),
    R('Bubble Shower', '1 charge', 'Deals area-of-effect water damage and lowers STR.'),
    R('Bubble Curtain', '3 charges', 'The crab gains a Shell effect.'),
    R('Scissor Guard', '2 charges', 'The crab gains a Defense Up effect.'),
]
MANDY_KIT = [
    R('Head Butt', '1 charge', 'Single target damage with Knockback.'),
    R('Scream', '1 charge', 'Area-of-effect MND down.'),
    R('Dream Flower', '2 charges', 'Area-of-effect Sleep.'),
    R('Wild Oats', '1 charge', 'Single target VIT down.'),
]

DATA = {
    'Faithful Falcorr': dict(
        fam='Hippogryph', job='Thief', lvl='86', cap='99', hp='4,968 (level 99)',
        dmg='Slashing', tp='7.4 / hit', dur='120 min.',
        traits=['Triple Attack', 'Gilfinder', 'High Evasion', 'Treasure Hunter',
                'Enhanced Movement Speed'],
        ready=[
            R('Back Heel', '1 charge', 'Deals physical Blunt damage.'),
            R('Jettatura', '3 charges',
              'Causes Fear to enemies in a fan-shaped area in front of the pet.'),
            R('Choke Breath', '1 charge',
              'Deals magical damage in a fan-shaped area in front of the pet. '
              'Additional effects: Paralysis and Silence.'),
            R('Fantod', '2 charges',
              'Grants the pet a quadruple attack bonus that varies with TP. It is a Boost '
              'effect and applies to only the next attack, including a missed one — but it '
              'does apply to every hit of a multi-hit round such as Double or Triple Attack.'),
        ]),
    'Bloodclaw Shasra': dict(
        fam='Lynx', job='Warrior', lvl='90', cap='99', hp='5,218 (level 99)',
        dmg='Slashing', tp='7.5 / hit', dur='120 min.',
        traits=['Double Attack', 'Fencer', 'Critical Attack Bonus', 'Enhanced Movement Speed'],
        ready=[
            R('Chaotic Eye', '1 charge', 'Silences an enemy.'),
            R('Blaster', '2 charges', 'Paralyzes an enemy.'),
            R('Charged Whisker', '2 charges',
              'Deals lightning damage to enemies within range of the pet.'),
        ]),
    'Mailbuster Cetas': dict(
        fam='Fly', job='Warrior', lvl='85', cap='95', hp='4,660 (level 95)',
        dmg='Slashing', tp='75 / hit',
        traits=['Double Attack', 'Fencer', 'Critical Attack Bonus',
                'Resistant to Darkness magic'],
        ready=[
            R('Cursed Sphere', '1 charge', 'Deals damage to enemies within an area of effect.'),
            R('Venom', '1 charge', 'Deals damage in a fan-shaped area. Additional effect: Poison.'),
        ]),
    'Courier Carrie': dict(
        fam='HQ Crab', lvl='23', cap='75', dmg='Blunt',
        ready=CRAB_KIT + [R('Big Scissors', '1 charge',
                            'Single-hit TP attack. Slashing damage.')]),
    'Crab Familiar': dict(
        fam='Crab', lvl='23', cap='55',
        ready=CRAB_KIT + [R('Big Scissors', '1 charge', 'Single-hit TP attack.')]),
    'Hare Familiar': dict(
        fam='Rabbit', lvl='23', cap='35',
        ready=[
            R('Whirl Claws', '1 charge', 'Area-of-effect damage.'),
            R('Dust Cloud', '1 charge', 'Single target Blind.'),
            R('Foot Kick', '1 charge', 'Single target damage.'),
        ]),
    'Homunculus': dict(
        fam='Black Mandragora', lvl='23', cap='75',
        ready=MANDY_KIT + [R('Leaf Dagger', '1 charge', 'Single target Poison.')]),
    'Sheep Familiar': dict(
        fam='Sheep', lvl='23', cap='35',
        ready=[
            R('Lamb Chop', '1 charge', 'Single target critical attack.', '1'),
            R('Rage', '2 charges', 'The pet gains Berserk.', '2'),
            R('Sheep Charge', '1 charge', 'Single target attack with Knockback.', '3'),
            R('Sheep Song', '2 charges', 'Area-of-effect Sleep.', '4'),
        ]),
    'Slippery Silas': dict(
        fam='Toad', job='Black Mage (noncasting)', lvl='23', cap='99',
        hp='3,388 (level 99)', dmg='Slashing',
        traits=['High resistance to Water-based moves'],
        ready=[]),                       # the page states None — see the header note
    'Flowerpot Bill': dict(
        fam='Mandragora', lvl='28', cap='40',
        ready=MANDY_KIT + [R('Leaf Dagger', '1 charge',
                             'Single target damage, possible Poison.')]),
    'Flytrap Familiar': dict(
        fam='Flytrap', lvl='28', cap='40',
        ready=[
            R('Gloeosuccus', '2 charges', 'Single target Slow.'),
            R('Palsy Pollen', '1 charge', 'Frontal-cone Paralyze.'),
            R('Soporific', '1 charge', 'Area-of-effect Sleep.'),
        ]),
    'Tiger Familiar': dict(
        fam='Tiger', lvl='28', cap='40', traits=['Can Double Attack'],
        ready=[
            R('Claw Cyclone', '1 charge', 'Area-of-effect damage.'),
            R('Razor Fang', '1 charge', 'Single target damage.'),
            R('Roar', '2 charges', 'Area-of-effect Paralyze.'),
        ]),
    'Eft Familiar': dict(
        fam='Eft', lvl='33', cap='45',
        ready=[
            R('Geist Wall', '1 charge', 'Area-of-effect Dispel.'),
            R('Toxic Spit', '2 charges', 'Single target Poison.'),
            R('Numbing Noise', '1 charge', 'Area-of-effect Stun.'),
            R('Nimble Snap', '1 charge', 'Single target damage.'),
            R('Cyclotail', '1 charge', 'Area-of-effect damage.'),
        ]),
    'Funguar Familiar': dict(
        fam='Funguar', lvl='33', cap='65',
        ready=[
            R('Frog Kick', '1 charge', 'Single target attack.'),
            R('Queasyshroom', '1 charge', 'Single target damage and Poison.'),
            R('Silence Gas', '3 charges', 'Frontal-cone damage and Silence.'),
            R('Numbshroom', '2 charges', 'Single target damage and Paralyze.'),
            R('Spore', '1 charge', 'Single target Paralyze.'),
            R('Dark Spore', '3 charges', 'Frontal-cone damage and Blind.'),
            R('Shakeshroom', '2 charges', 'Single target damage and Disease.'),
        ]),
    'Lizard Familiar': dict(
        fam='Lizard', lvl='33', cap='45',
        ready=[
            R('Blockhead', '1 charge', 'Single target damage plus Knockback.'),
            R('Secretion', '1 charge', 'Evasion boost.'),
            R('Baleful Gaze', 'Not available via Ready', 'Single target Petrify.'),
            R('Fireball', '1 charge', 'Area-of-effect fire damage.'),
            R('Tail Blow', '1 charge', 'Single target damage.'),
            R('Plague Breath', 'Not available via Ready', 'Area-of-effect cone Poison.'),
            R('Brain Crush', '1 charge', 'Single target damage.'),
            R('Infrasonics', '2 charges', 'Area-of-effect cone Evasion down.'),
        ]),
    'Mayfly Familiar': dict(
        fam='Fly', lvl='33', cap='45',
        ready=[
            R('Cursed Sphere', '1 charge', 'Area-of-effect damage.'),
            R('Venom', '1 charge', 'Frontal-cone Poison.'),
        ]),
}

print('=== FILLING %d BEASTMASTER FAMILIARS ===' % len(DATA))
for name, fields in DATA.items():
    p = by_name.get(name)
    assert p is not None, 'not in the roster: %s' % name
    for k, v in fields.items():
        assert v is not None
        p[k] = v
    n = len(p.get('ready', []))
    print('  %-20s %-18s lv %-3s cap %-3s  %s'
          % (name, fields.get('fam', ''), fields.get('lvl', '?'), fields.get('cap', '?'),
             ('%d ready' % n) if n else 'ready: none (stated)'))

# ------------------------------------------------ split the level band out of `sub`
# 95 of the 98 jug strings already end "· Lv a-b" — the level the jug becomes available
# and the pet level cap, the same two numbers the familiar pages print in their own
# columns. Pull them into `lvl`/`cap` so the card can label them, and leave `sub` as just
# the jug item. Where a value was typed in by hand above, the parsed one MUST agree —
# that is the cross-check, and it covers 13 of the 16.
import re
SUFFIX = re.compile(r'^(.*?)\s*\u00b7\s*Lv\s*(\d+)\s*-\s*(\d+)\s*$')
split = agreed = 0
for p in pets:
    m = SUFFIX.match(p.get('sub', ''))
    if not m:
        continue
    jug, lo, hi = m.group(1).strip(), m.group(2), m.group(3)
    if p.get('lvl'):
        assert p['lvl'] == lo and p['cap'] == hi, \
            'hand-typed %s lv %s-%s vs jug string %s-%s' % (p['n'], p.get('lvl'), p.get('cap'), lo, hi)
        agreed += 1
    p['sub'] = jug
    p['lvl'] = lo
    p['cap'] = hi
    split += 1
print('\nlevel band split out of the jug string: %d pets (%d cross-checked against the '
      'hand-typed values, all agreed)' % (split, agreed))
missing = [p['n'] for p in pets if not p.get('lvl')]
print('pets still without a level band: %s' % (missing or 'none'))

# ---------------------------- drop the superseded bare "Ready" sections, normalise names
# 22 BST pets already carried `sections: [{t:"Ready", items:[bare names]}]`. For the 16
# filled above the new `ready` list supersedes that entirely, so the old section is removed
# rather than rendered twice. Before dropping it, it was compared name-for-name and all ten
# that had one agreed on the count — two disagreed on spelling and the panels settle both.
#
# Then EVERY remaining pet ability name is normalised to the bestiary's own vocabulary, so
# a familiar's Ready move and the same TP move on a mob card are the same string. That is
# what makes this data usable for the OmniWatch / WarnMe handoff.
NAME_FIX = {
    'Frogkick': 'Frog Kick',                 # panel and the bestiary table both say two words
    'Baleful Gaze Lizard': 'Baleful Gaze',   # a wiki disambiguation suffix
    'Power Attack Beetle': 'Power Attack',   # same
    'Hi-freq Field': 'Hi-Freq Field',        # case
    'Sand Blast': 'Sandblast',
    'Sand Pit': 'Sandpit',
    'Plague Breath': 'Plaguebreath',         # the bestiary spells it as one word
}
dropped = renamed = 0
for p in pets:
    if 'ready' in p and p.get('sections'):
        keep = [sec for sec in p['sections'] if sec['t'] != 'Ready']
        if len(keep) != len(p['sections']):
            dropped += 1
        p['sections'] = keep
    for sec in (p.get('sections') or []):
        for it in sec['items']:
            if it['n'] in NAME_FIX:
                it['n'] = NAME_FIX[it['n']]; renamed += 1
    for r in (p.get('ready') or []):
        if r['n'] in NAME_FIX:
            r['n'] = NAME_FIX[r['n']]; renamed += 1
print('\nsuperseded bare "Ready" sections removed: %d' % dropped)
print('ability names normalised to the bestiary vocabulary: %d' % renamed)

# every pet ability name must now exist in the bestiary's ability table
mobs_path = os.path.join(os.path.dirname(P), 'mobs.json')
ABIL = json.load(open(mobs_path, encoding='utf-8'))['abilities']
unmatched = sorted({it['n'] for p in pets for sec in (p.get('sections') or []) for it in sec['items']
                    if it['n'] not in ABIL} |
                   {r['n'] for p in pets for r in (p.get('ready') or []) if r['n'] not in ABIL})
print('pet ability names with no bestiary definition: %d %s' % (len(unmatched), unmatched))
assert not unmatched

# ---------------------------------------------------------------- guards
assert not [k for p in pets for k, v in p.items() if v is None], 'NULL POISON'
for p in pets:
    assert 'n' in p and 'sections' in p
    for r in (p.get('ready') or []):
        assert set(r) <= {'n', 'c', 'd', 'i'}, r
done = [p['n'] for p in pets if 'ready' in p]
todo = [p['n'] for p in pets if 'ready' not in p]
print('\nBST familiars with a Ready list recorded: %d of %d' % (len(done), len(pets)))
print('still to do (%d): %s%s' % (len(todo), ', '.join(todo[:12]),
                                  ' …' if len(todo) > 12 else ''))

# the Summoner side must be untouched
# Summoner avatars carry only n / sub / sections; none of the new BST keys may appear there.
BST_ONLY = {'fam', 'job', 'lvl', 'cap', 'hp', 'dmg', 'tp', 'dur', 'traits', 'ready'}
smn = d['pets']['15']
assert not [p['n'] for p in smn if BST_ONLY & set(p)], 'a Summoner avatar was modified'
print('Summoner avatars untouched: %d' % len(smn))

json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('written: %s' % P)
