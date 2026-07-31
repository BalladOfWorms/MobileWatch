#!/usr/bin/env python3
"""
REV 403 — seventeen more jug familiars (plus Droopy Dortwin re-confirmed).
Runs after 398, 399, 400, 401 and 402.

TOUCHES mobs.json TOO: two Lucani Ready moves have no bestiary definition
(`Disembowel`, `Extirpating Salvo`), so they are created here rather than
left to render as bare names. Defs only — NOT stamped onto any Lucani mob,
because a BST pet page is not a statement about the wild family's kit.

THE THING THIS BATCH SETTLES
----------------------------
`Spider Web` reads **"3% Slow"** on Spider Familiar's page too — a SECOND
independent pet page with the same figure. Rev 402 flagged it as a possible
dropped zero against the bestiary's "inflicts Slow II" (~30%). Two sources
printing 3% means it is what BG publishes, not a one-off typo. Still
recorded as printed; the bestiary/page disagreement stands as a real one.

FOUR KIT DISAGREEMENTS WITH THE OLD NAME-ONLY `sections` LISTS
--------------------------------------------------------------
  Lynx Familiar        section 2 -> page 4   (superset: +Charged Whisker,
                                              +Frenzied Rage)
  Slime Familiar       section 3 -> page 3   exact match
  Spider Familiar      section 3 -> page 3   exact match
  Porter Crab Familiar section 5 -> page 5   SAME SLOTS, TWO RENAMED:
                       Bubble Shower -> Venom Shower, Big Scissors ->
                       Mega Scissors. It is a **Barnacled Crab**, not a
                       Crab, and Jovial Edwin (also Barnacled Crab) prints
                       the same two upgrades. The old list looks like plain
                       Crab data.
  Mosquito Familiar    section 2 -> page 2   COMPLETE REPLACEMENT: the old
                       list said Cursed Sphere + Venom, which is the FLY
                       kit (Headbreaker Ken has exactly those). The page
                       says Infected Leech + Gloom Spray, and Left-Handed
                       Yoko, the other Mosquito, agrees. The old list was
                       wrong, not merely thin.

CHARGE-COST DISCREPANCY LEFT ALONE, FLAGGED
-------------------------------------------
`Scissor Guard` costs 2 charges on Jovial Edwin, Porter Crab Familiar and
Sunburst Malfik. Rev 402 recorded 1 for Herald Henry. Three against one
makes a rev-402 transcription slip likely, but changing it on a majority
vote would be a guess — left as recorded and raised with the user.

Special Traits: icon-coupled entries not transcribed (rule 472/480). Two
textual readings ARE taken and are flagged as icon-ADJACENT rather than
clean: Redolent Candi "MDB -50%" and Submerged Iyo "Store TP V" / "MDT -25%".

`Slime Familiar` and `Sultry Patrice` print Attack ± with NO SIGN ("20%",
"30%") and Defense ± as "N/A". Recorded verbatim; "N/A" is not a value so
no `def` key is written.
"""
import json, os

BASE = 'app/src/main/assets'
if not os.path.exists(BASE):
    BASE = 'android/' + BASE
P = os.path.join(BASE, 'jobs.json')
M = os.path.join(BASE, 'mobs.json')
d = json.load(open(P, encoding='utf-8'))
mob = json.load(open(M, encoding='utf-8'))
pets = d['pets']['9']
by_name = {p['n']: p for p in pets}


def R(n, c, desc, sc=None):
    r = {'n': n, 'c': c, 'd': desc}
    if sc:
        r['sc'] = sc
    return r


# ---------------------------------------------------------------- shared kits
# Defined once so cross-page contradictions stay visible (standing rule).
RABBIT = [
    R('Foot Kick', '1 charge', 'Critical hit rate varies with TP.', 'Reverberation'),
    R('Dust Cloud', '1 charge',
      'Deals Earth elemental damage to enemies within a fan-shaped area. Additional effect: '
      'Blind. Damage varies with TP.'),
    R('Whirl Claws', '1 charge',
      'Deals physical damage to enemies within range. Area of effect varies with TP.', 'Impaction'),
    R('Wild Carrot', '2 charges',
      'Restores HP of all party members within area of effect. HP restored varies with TP.'),
]
BARNACLED_CRAB = [
    R('Venom Shower', '1 charge',
      'Deals Water elemental damage to enemies within area of effect. Additional effect: lowers '
      'STR. Area of effect varies with TP.'),
    R('Bubble Curtain', '3 charges',
      '-50% magic damage taken for pet and Beastmaster. Duration of effect varies with TP.'),
    R('Mega Scissors', '1 charge', 'Critical hit rate varies with TP.', 'Gravitation / Scission'),
    R('Scissor Guard', '2 charges',
      '+100% Defense for pet and Beastmaster. Duration of effect varies with TP.'),
    R('Metallic Body', '1 charge',
      'Gives the effect of a roughly 200 HP Stoneskin for pet and Beastmaster. Duration of effect '
      'varies with TP.'),
]
MOSQUITO = [
    R('Infected Leech', '1 charge',
      'Deals Darkness elemental damage and absorbs HP from enemies in a fan-shaped area. '
      'Additional effect: Plague (-50 TP/tic) for 45 seconds. Additional effect duration varies '
      'with TP.'),
    R('Gloom Spray', '2 charges',
      'Deals Darkness elemental damage in a fan-shaped area. Additional effect: Dispel. Damage '
      'varies with TP.'),
]
SLIME = [
    R('Fluid Toss', '1 charge', 'Deals physical damage. Damage varies with TP.', 'Reverberation'),
    R('Fluid Spread', '2 charges',
      'Deals physical damage to all enemies around the pet. Damage varies with TP.',
      'Transfixion / Fragmentation'),
    R('Digest', '1 charge', 'Absorbs HP from an enemy. Damage varies with TP.'),
]
SPIDER = [
    R('Sickle Slash', '1 charge', 'Critical hit rate varies with TP.', 'Transfixion'),
    R('Acid Spray', '1 charge',
      'Deals Water elemental damage. Additional effect: Poison (31 damage/tic) for 3 minutes. '
      'Damage varies with TP.'),
    R('Spider Web', '2 charges', '3% Slow for enemies within range. Duration varies with TP.'),
]
CHAPULI = [
    R('Sensilla Blades', '1 charge',
      'Deals physical damage to enemies within a fan-shaped area. Damage varies with TP.',
      'Scission'),
    R('Tegmina Buffet', '2 charges',
      'Deals physical damage to enemies within range. Additional effect: Choke (-33 VIT and 15 '
      'damage/tic) for 60 seconds. Damage varies with TP.', 'Distortion / Detonation'),
]
BEETLE = [
    R('Power Attack', '1 charge', 'Critical hit rate varies with TP.', 'Reverberation'),
    R('Hi-Freq Field', '2 charges',
      '-40 Evasion for enemies within a fan-shaped area. Area of effect varies with TP. '
      'Duration 3 minutes.'),
    R('Rhino Attack', '1 charge', 'Damage varies with TP.', 'Detonation'),
    R('Rhino Guard', '1 charge', '+25% Evasion. Duration of effect varies with TP.'),
    R('Spoil', '1 charge',
      '-20% Strength to an enemy, decaying over time. Duration of effect varies with TP, from 3 '
      'minutes to 9 minutes.'),
]

DATA = {
    'Hurler Percival': dict(fam='Beetle', eco='Vermin', job='Paladin', tp='95', cap='116',
        atk='+20%',
        stats={'hp': '4,988', 'acc': '863', 'atk': '909', 'eva': '690', 'def': '1,029'},
        ready=list(BEETLE)),

    'Jovial Edwin': dict(fam='Barnacled Crab', eco='Aquan', job='Paladin', tp='73',
        ready=list(BARNACLED_CRAB)),

    'Left-Handed Yoko': dict(fam='Mosquito', eco='Vermin', job='Dark Knight', tp='49', cap='119',
        atk='-30%',
        stats={'hp': '4,508', 'acc': '899', 'atk': '599', 'eva': '959', 'def': '907'},
        ready=list(MOSQUITO)),

    'Lynx Familiar': dict(fam='Lynx', eco='Beast', tp='73',
        ready=[
            R('Chaotic Eye', '1 charge',
              'Silences an enemy within range. Duration of effect varies with TP.'),
            R('Blaster', '2 charges',
              'Paralyzes an enemy within range. Duration of effect varies with TP.'),
            R('Charged Whisker', '2 charges',
              'Deals Lightning damage to enemies within range of the pet. Damage varies with TP.'),
            R('Frenzied Rage', '1 charge',
              'Increases the attack of pet and master, if in area of effect. Duration varies with TP.'),
        ]),

    'Mosquito Familiar': dict(fam='Mosquito', eco='Vermin', job='Dark Knight', tp='44', cap='119',
        atk='-40%',
        stats={'hp': '4,322', 'acc': '889', 'atk': '512', 'eva': '939', 'def': '907'},
        ready=list(MOSQUITO)),

    'Pondering Peter': dict(fam='Rabbit', eco='Beast', job='Warrior', tp='75', cap='103',
        deff='+10%',
        stats={'hp': '5,702', 'acc': '869', 'atk': '791', 'eva': '704', 'def': '1,040'},
        ready=list(RABBIT)),

    'Porter Crab Familiar': dict(fam='Barnacled Crab', eco='Aquan', tp='73',
        ready=list(BARNACLED_CRAB)),

    'Redolent Candi': dict(fam='Snapweed', eco='Plantoid', job='Warrior', tp='75', cap='115',
        deff='+20%', traits=['MDB -50%'],
        stats={'hp': '5,832', 'acc': '876', 'atk': '793', 'eva': '704', 'def': '1,128'},
        ready=[
            R('Tickling Tendrils', '1 charge',
              'Delivers a fivefold attack. Additional effect: Stun. Damage varies with TP.',
              'Impaction'),
            R('Stink Bomb', '2 charges',
              'Deals Earth elemental damage to enemies within area of effect. Additional effects: '
              'Blind and Paralysis. Duration of effect varies with TP.'),
            R('Nectarous Deluge', '2 charges',
              'Deals Water elemental damage to enemies within area of effect. Additional effect: '
              'Poison. Duration of effect varies with TP.'),
            R('Nepenthic Plunge', '3 charges',
              'Deals Water elemental damage within a fan-shaped area. Additional effects: Drown '
              '(-33 STR and 15 damage/tic) and Weight. Duration of effect varies with TP, from 60 '
              'seconds to about two and a half minutes.'),
        ]),

    'Rhyming Shizuna': dict(fam='Sheep', eco='Beast', job='Warrior', tp='80', cap='107',
        atk='+10%', deff='+30%',
        stats={'hp': '5,832', 'acc': '866', 'atk': '873', 'eva': '704', 'def': '1,229'},
        ready=[
            R('Lamb Chop', '1 charge', 'Damage varies with TP.', 'Impaction'),
            R('Rage', '2 charges',
              '+50% Attack and -50% Defense for pet and Beastmaster. Duration of effect varies '
              'with TP.'),
            R('Sheep Charge', '1 charge', 'Damage varies with TP.', 'Reverberation'),
            R('Sheep Song', '2 charges',
              'Puts all enemies to sleep within range. Area of effect varies with TP. Duration 45 '
              'seconds.'),
        ]),

    'Scissorleg Xerin': dict(fam='Chapuli', eco='Vermin', job='Warrior', tp='75', cap='105',
        atk='+10%', deff='-10%',
        stats={'hp': '5,670', 'acc': '879', 'atk': '950', 'eva': '707', 'def': '855'},
        ready=list(CHAPULI)),

    'Sharpwit Hermes': dict(fam='Citrullus', eco='Plantoid', job='Monk', tp='57', cap='119',
        stats={'hp': '5,678', 'acc': '871', 'atk': '750', 'eva': '706', 'def': '940'},
        ready=[
            R('Head Butt', '1 charge', 'Damage varies with TP.', 'Detonation'),
            R('Wild Oats', '1 charge',
              'Additional effect: -20% Vitality, decaying over time. Damage varies with TP. '
              'Duration 3 minutes.', 'Transfixion'),
            R('Leaf Dagger', '1 charge', 'Additional effect: Poison. Damage varies with TP.',
              'Scission'),
            R('Scream', '1 charge',
              '-20% Mind for enemies within range, decaying over time. Duration of effect varies '
              'with TP, from 3 minutes to 9 minutes.'),
        ]),

    'Slime Familiar': dict(fam='Slime', eco='Amorph', job='Warrior', tp='73', cap='119',
        atk='20%', ready=list(SLIME)),

    'Spider Familiar': dict(fam='Spider', eco='Vermin', job='Warrior', tp='75', cap='118',
        atk='+20%', deff='-20%',
        stats={'hp': '5,508', 'acc': '901', 'atk': '948', 'eva': '704', 'def': '753'},
        ready=list(SPIDER)),

    'Stalwart Angelina': dict(fam='Lucani', eco='Vermin', cap='119',
        ready=[
            R('Disembowel', '1 charge',
              'Deals physical damage to all enemies in a fan-shaped area in front of the pet. '
              'Additional effect: decreases accuracy. Damage varies with TP.', 'Impaction'),
            R('Extirpating Salvo', '2 charges',
              'Deals physical damage. Additional effect: Stun. Damage varies with TP.',
              'Fusion / Impaction'),
        ]),

    'Submerged Iyo': dict(fam='Apkallu', eco='Bird', job='Monk', tp='59', cap='119',
        traits=['Store TP V', 'MDT -25%'],
        stats={'hp': '5,878', 'acc': '891', 'atk': '753', 'eva': '706', 'def': '933'},
        ready=[
            R('Wing Slap', '2 charges',
              'Delivers a fivefold attack. Additional effect: Stun. Damage varies with TP.',
              'Gravitation / Liquefaction'),
            R('Beak Lunge', '1 charge', 'Delivers a twofold attack. Damage varies with TP.',
              'Scission'),
        ]),

    'Sultry Patrice': dict(fam='Slime', eco='Amorph', job='Warrior', tp='73', cap='119',
        atk='30%', ready=list(SLIME)),

    'Sunburst Malfik': dict(fam='Crab', eco='Aquan', job='Paladin', tp='75', cap='104',
        atk='-10%', deff='+10%',
        stats={'hp': '5,250', 'acc': '860', 'atk': '681', 'eva': '690', 'def': '1,120'},
        ready=[
            R('Bubble Shower', '1 charge',
              'Deals Water elemental damage to enemies within area of effect. Additional effect: '
              'lowers STR. Area of effect varies with TP.'),
            R('Bubble Curtain', '3 charges',
              '-50% magic damage taken for pet and Beastmaster. Duration of effect varies with TP.'),
            R('Big Scissors', '1 charge',
              'Deals physical damage. Critical hit rate varies with TP.', 'Scission'),
            R('Scissor Guard', '2 charges',
              '+100% Defense for pet and Beastmaster. Duration of effect varies with TP.'),
            R('Metallic Body', '1 charge',
              'Gives the effect of a roughly 200 HP Stoneskin for pet and Beastmaster. Duration '
              'of effect varies with TP.'),
        ]),
}
for f in DATA.values():
    if 'deff' in f:
        f['def'] = f.pop('deff')

# ---------------------------------------------------------------- new ability defs
NEW_ABIL = {
    'Disembowel': {'d': 'Physical damage to enemies in a frontal cone. Additional effect: '
                        'Accuracy Down.',
                   't': 'Physical', 'r': 'Cone', 'tgt': 'Cone AoE',
                   'fx': ['Damage', 'Accuracy Down']},
    'Extirpating Salvo': {'d': 'Physical damage to a single target. Additional effect: Stun.',
                          't': 'Physical', 'tgt': 'Single', 'fx': ['Damage', 'Stun']},
}
print('=== NEW BESTIARY ABILITY DEFS (Lucani; defs only, not stamped on any mob) ===')
for n, v in NEW_ABIL.items():
    assert n not in mob['abilities'], n
    mob['abilities'][n] = v
    print('  + %-20s %s' % (n, v['d']))

# ---------------------------------------------------------------- apply
print('\n=== REV 403 — 17 MORE JUG FAMILIARS ===')
cap_changes = []
for name, fields in sorted(DATA.items()):
    p = by_name[name]
    stored, page_cap = p.get('cap'), fields.get('cap')
    for k, v in fields.items():
        p[k] = v
    if page_cap is None:
        note = 'page prints "?" — jug-string cap %s kept' % stored
    elif stored == page_cap:
        note = 'cap matches the jug string'
    else:
        note = 'CAP CHANGED %s -> %s  (rule 467)' % (stored, page_cap)
        cap_changes.append((name, stored, page_cap))
    print('  %-22s %-16s %-9s cap %-5s %d ready   %s'
          % (name, fields['fam'], fields['eco'], page_cap or '-', len(fields['ready']), note))
print('\ncap conflicts resolved in favour of the familiar page: %d %s' % (len(cap_changes), cap_changes))

# Droopy Dortwin was re-sent this batch, identical to rev 402 — verify, do not rewrite.
dd = by_name['Droopy Dortwin']
same = (dd.get('cap') == '103' and dd.get('tp') == '75'
        and dd.get('stats') == {'hp': '5,500', 'acc': '848', 'atk': '775', 'eva': '689',
                                'def': '929'}
        and [r['n'] for r in dd['ready']] == [r['n'] for r in RABBIT])
print('\nDroopy Dortwin re-sent: rev-402 transcription %s' % ('RE-CONFIRMED, no change' if same
                                                              else '!! DIVERGES !!'))
assert same

# ---------------------------------------------------------------- section vs page
print('\n=== OLD NAME-ONLY `sections` LIST vs THE Lv.99 PAGE ===')
for name in ('Lynx Familiar', 'Slime Familiar', 'Spider Familiar', 'Porter Crab Familiar',
             'Mosquito Familiar'):
    prior = [i['n'] for s in (by_name[name].get('sections') or []) if s['t'] == 'Ready'
             for i in s['items']]
    now = [r['n'] for r in DATA[name]['ready']]
    verdict = ('exact match' if prior == now else
               'superset' if set(prior) <= set(now) else
               'REPLACED — old: %s' % ', '.join(n for n in prior if n not in now))
    print('  %-22s %d -> %d   %s' % (name, len(prior), len(now), verdict))

print('\n=== `Spider Web` — A SECOND PET PAGE PRINTS "3%" ===')
print('  Gussy Hachirobe (rev 402) and Spider Familiar both read "3% Slow";')
print('  the bestiary def still reads "AoE that inflicts Slow II". Recorded as printed.')

print('\n=== `Scissor Guard` CHARGE COST — 3 vs 1, LEFT AS RECORDED ===')
for p in pets:
    for r in (p.get('ready') or []):
        if r['n'] == 'Scissor Guard':
            print('  %-22s %s' % (p['n'], r['c']))

# ---------------------------------------------------------------- guards
for p in pets:
    if 'ready' in p and p.get('sections'):
        p['sections'] = [s for s in p['sections'] if s['t'] != 'Ready']

ABIL = mob['abilities']
unmatched = sorted({it['n'] for p in pets for sec in (p.get('sections') or []) for it in sec['items']
                    if it['n'] not in ABIL} |
                   {r['n'] for p in pets for r in (p.get('ready') or []) if r['n'] not in ABIL})
print('\npet ability names with no bestiary definition: %d %s' % (len(unmatched), unmatched))
assert not unmatched
assert not [k for p in pets for k, v in p.items() if v is None], 'NULL POISON'
assert not [k for a in ABIL.values() for k, v in a.items() if v is None], 'NULL POISON (abilities)'
for p in pets:
    st = p.get('stats')
    if st:
        assert set(st) <= {'hp', 'acc', 'atk', 'eva', 'def'} and all(isinstance(v, str) for v in st.values())
BST_ONLY = {'fam', 'job', 'lvl', 'cap', 'hp', 'dmg', 'tp', 'dur', 'traits', 'notes', 'ready',
            'eco', 'atk', 'def', 'stats'}
assert not [p['n'] for p in d['pets']['15'] if BST_ONLY & set(p)], 'a Summoner avatar was modified'

done = [p['n'] for p in pets if 'ready' in p]
todo = [p['n'] for p in pets if 'ready' not in p]
sc = [r for p in pets for r in (p.get('ready') or []) if r.get('sc')]
print('ready moves carrying a skillchain: %d' % len(sc))
print('familiars carrying a stat block: %d' % sum(1 for p in pets if p.get('stats')))
print('\nBST familiars with a Ready list recorded: %d of %d' % (len(done), len(pets)))
print('still to do (%d): %s' % (len(todo), ', '.join(todo)))

json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
json.dump(mob, open(M, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('written: %s' % P)
print('written: %s' % M)
