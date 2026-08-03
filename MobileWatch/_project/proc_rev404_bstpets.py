#!/usr/bin/env python3
"""
REV 404 — ten more jug familiars, three re-sent pages that CORRECT already-filled
records, and the resolution of the long-open TP/hit scale question.
Runs after 398-403. jobs.json only.

THE 7.5-vs-75 TP/hit QUESTION IS ANSWERED — SAME FAMILIAR, BOTH FORMS
---------------------------------------------------------------------
Rules 470/475 have carried this open since rev 400: some pages print "7.5 / hit"
and others print "75". This batch re-sent two familiars that were recorded from
the OLD layout, and their own pages print the integer:

    Bloodclaw Shasra   stored "7.5 / hit"   page prints  75
    Faithful Falcorr   stored "7.4 / hit"   page prints  74
    Mailbuster Cetas   stored "75 / hit"    page prints  75   (control)

So the decimal form is the SAME NUMBER at one tenth the scale — a rendering of
the older layout, not a different measurement. Every one of the 12 decimal
values maps to a figure inside the observed 44-95 range when multiplied by ten.
=> ALL TP VALUES NORMALISE TO THE BARE INTEGER, and the " / hit" suffix goes.

THREE ALREADY-FILLED RECORDS WERE INCOMPLETE — the old-layout pages published a
SHORTER Ready list than the familiar's own page does:

    Faithful Falcorr   4 -> 6   (+ Hoof Volley, + Nihility Song)
    Bloodclaw Shasra   3 -> 4   (+ Frenzied Rage)
    Mailbuster Cetas   2 -> 3   (+ Somersault)

RULE 483 CLAIMS A THIRD VICTIM
------------------------------
`Weevil Familiar`'s old name-only list is the BEETLE kit (Power Attack,
Hi-Freq Field, Rhino Attack, Rhino Guard, Spoil). Its page says it is a
**Lucani** with Disembowel + Extirpating Salvo, matching Stalwart Angelina.
That is three of the nine "<X> Familiar" section lists now proven wrong rather
than merely thin (Mosquito, Porter Crab, Weevil).

`Store TP` CONFIRMS THE ICON-ADJACENT TRAIT READING
---------------------------------------------------
Rev 403 recorded `Submerged Iyo` "Store TP V" as a flagged, uncertain reading.
`Surging Storm` — the other Apkallu — prints **"Store TP III"**. A roman numeral
that VARIES between two familiars of one family is real transcribed text, not a
mis-split icon label. Both keep their "MDT -25%" alongside.

THE PARENTHETICAL TRACKS THE JUG TIER
-------------------------------------
Lv.99 jugs print (119); the Lv.86/Lv.90 jugs here print (114) and the Lv.85 one
prints (110). Combined with Droopy Dortwin's (118) from rev 402, the second
figure is a per-tier ceiling, not a page constant. All three re-sent caps match
what was stored (99, 99, 95).
"""
import json, os, re

BASE = 'app/src/main/assets'
if not os.path.exists(BASE):
    BASE = 'android/' + BASE
P = os.path.join(BASE, 'jobs.json')
d = json.load(open(P, encoding='utf-8'))
pets = d['pets']['9']
by_name = {p['n']: p for p in pets}


def R(n, c, desc, sc=None):
    r = {'n': n, 'c': c, 'd': desc}
    if sc:
        r['sc'] = sc
    return r


# ---------------------------------------------------------------- shared kits
APKALLU = [
    R('Wing Slap', '2 charges',
      'Delivers a fivefold attack. Additional effect: Stun. Damage varies with TP.',
      'Gravitation / Liquefaction'),
    R('Beak Lunge', '1 charge', 'Delivers a twofold attack. Damage varies with TP.', 'Scission'),
]
CITRULLUS = [
    R('Head Butt', '1 charge', 'Damage varies with TP.', 'Detonation'),
    R('Wild Oats', '1 charge',
      'Additional effect: -20% Vitality, decaying over time. Damage varies with TP. Duration 3 '
      'minutes.', 'Transfixion'),
    R('Leaf Dagger', '1 charge', 'Additional effect: Poison. Damage varies with TP.', 'Scission'),
    R('Scream', '1 charge',
      '-20% Mind for enemies within range, decaying over time. Duration of effect varies with TP, '
      'from 3 minutes to 9 minutes.'),
]
TULFAIRE = [
    R('Molting Plumage', '1 charge',
      'Deals Wind damage to enemies within a fan-shaped area. Additional effect: Dispel '
      '(light-based). Area of effect varies with TP.'),
    R('Swooping Frenzy', '2 charges',
      'Deals physical damage to enemies within a fan-shaped area. Additional effects: -25% '
      'Defense and -25 magic defense bonus. Duration of effect varies with TP, from 60 seconds to '
      'two and a half minutes.', 'Fusion / Reverberation'),
    R('Pentapeck', '3 charges',
      'Deals physical damage. Additional effect: Amnesia. Duration of effect varies with TP.',
      'Light / Distortion'),
]
LYNX = [
    R('Chaotic Eye', '1 charge',
      'Silences an enemy within range. Duration of effect varies with TP.'),
    R('Blaster', '2 charges',
      'Paralyzes an enemy within range. Duration of effect varies with TP.'),
    R('Charged Whisker', '2 charges',
      'Deals Lightning damage to enemies within range of the pet. Damage varies with TP.'),
    R('Frenzied Rage', '1 charge',
      'Increases the attack of pet and master, if in area of effect. Duration varies with TP.'),
]
RAAZ = [
    R('Sweeping Gouge', '1 charge',
      'Delivers a twofold attack to enemies within a fan-shaped area. Additional effect: -25% '
      'Defense for 60 seconds. Damage varies with TP.', 'Induration'),
    R('Zealous Snort', '3 charges',
      '+25% Haste, +25 magic defense bonus, and increases the likelihood of both countering and '
      'guarding for pet and Beastmaster. Duration of effect varies with TP.'),
]
LUCANI = [
    R('Disembowel', '1 charge',
      'Deals physical damage to all enemies in a fan-shaped area in front of the pet. Additional '
      'effect: decreases accuracy. Damage varies with TP.', 'Impaction'),
    R('Extirpating Salvo', '2 charges',
      'Deals physical damage. Additional effect: Stun. Damage varies with TP.', 'Fusion / Impaction'),
]
YELLOW_BEETLE = [
    R('Power Attack', '1 charge', 'Critical hit rate varies with TP.', 'Reverberation'),
    R('Hi-Freq Field', '2 charges',
      '-40 Evasion for enemies within a fan-shaped area. Area of effect varies with TP. '
      'Duration 3 minutes.'),
    R('Rhino Attack', '1 charge', 'Damage varies with TP.', 'Detonation'),
    R('Rhino Guard', '1 charge', '+25% Evasion. Duration of effect varies with TP.'),
    R('Spoil', '1 charge',
      '-20% Strength to an enemy, decaying over time. Duration of effect varies with TP, from 3 '
      'minutes to 9 minutes.'),
    R('Rhinowrecker', '2 charges',
      'Deals physical damage to all enemies in a fan-shaped area in front of the pet. Additional '
      'effect: decreases defense. Damage varies with TP.', 'Fusion / Transfixion'),
]
HIPPOGRYPH = [
    R('Back Heel', '1 charge', 'Damage varies with TP.', 'Reverberation'),
    R('Jettatura', '3 charges',
      'Terrorizes enemies within a fan-shaped area. Duration of effect varies with TP, from 15 to '
      '25 seconds.'),
    R('Choke Breath', '1 charge',
      'Deals Earth elemental damage to enemies within a fan-shaped area. Additional effect: '
      'Paralysis and Silence. Duration of effect varies with TP.'),
    R('Fantod', '2 charges',
      'Increases the damage of the pet\u2019s next attack by an unstated amount. Duration of '
      'effect varies with TP.'),
    R('Hoof Volley', '3 charges', 'Deals physical damage. Damage varies with TP.', 'Fragmentation'),
    R('Nihility Song', '1 charge',
      'Removes one beneficial magic effect from all enemies around the pet. Area varies with TP.'),
]
FLY = [
    R('Cursed Sphere', '1 charge',
      'Deals Dark elemental damage to enemies within area of effect. Damage varies with TP.'),
    R('Venom', '1 charge',
      'Deals Water elemental damage to enemies within a fan-shaped area. Additional effect: '
      'Poison. Duration of effect varies with TP.'),
    R('Somersault', '1 charge', 'Damage varies with TP.', 'Compression'),
]

NEW = {
    'Surging Storm': dict(fam='Apkallu', eco='Bird', job='Monk', tp='59', cap='118',
        traits=['Store TP III', 'MDT -25%'],
        stats={'hp': '5,678', 'acc': '881', 'atk': '753', 'eva': '706', 'def': '933'},
        ready=list(APKALLU)),

    'Suspicious Alice': dict(fam='Eft', eco='Lizard', job='Warrior', tp='68', cap='113',
        stats={'hp': '5,184', 'acc': '906', 'atk': '793', 'eva': '704', 'def': '948'},
        ready=[
            R('Nimble Snap', '1 charge', 'Damage varies with TP.', 'Impaction'),
            R('Cyclotail', '1 charge',
              'Deals physical damage to enemies within range. Damage varies with TP.', 'Impaction'),
            R('Geist Wall', '1 charge',
              'Removes one beneficial magic effect from enemies within range. Area of effect '
              'varies with TP.'),
            R('Numbing Noise', '1 charge', 'Stuns enemies within a fan-shaped area.'),
            R('Toxic Spit', '2 charges',
              'Poisons (23 damage/tic) an enemy. Duration of effect varies with TP.'),
        ]),

    'Sweet Caroline': dict(fam='Citrullus', eco='Plantoid', job='Monk', cap='119',
        ready=list(CITRULLUS)),

    'Swooping Zhivago': dict(fam='Tulfaire', eco='Bird', job='Warrior', tp='75', cap='119',
        atk='-10%',
        stats={'hp': '5,544', 'acc': '869', 'atk': '720', 'eva': '727', 'def': '941'},
        ready=list(TULFAIRE)),

    'Threestar Lynn': dict(fam='Ladybug', eco='Vermin', job='Thief', tp='73', cap='119',
        deff='-10%', traits=['Treasure Hunter I'],
        stats={'hp': '3,604', 'acc': '934', 'atk': '737', 'eva': '858', 'def': '807'},
        ready=[
            R('Sudden Lunge', '1 charge', 'Additional effect: Stun. Damage varies with TP.',
              'Impaction'),
            R('Spiral Spin', '1 charge',
              'Deals physical damage to enemies within a fan-shaped area. Additional effect: -20 '
              'Accuracy. Duration of effect varies with TP.', 'Scission'),
            R('Noisome Powder', '2 charges',
              'Lowers the attack of enemies within range by an unstated amount. Duration of '
              'effect varies with TP.'),
        ]),

    'Vivacious Gaston': dict(fam='Lynx', eco='Beast', tp='73', ready=list(LYNX)),

    'Vivacious Vickie': dict(fam='Raaz', eco='Beast', job='Monk', tp='75', cap='119',
        atk='+10%', deff='-10%',
        stats={'hp': '6,546', 'acc': '858', 'atk': '818', 'eva': '706', 'def': '877'},
        ready=list(RAAZ)),

    'Warlike Patrick': dict(fam='Hill Lizard', eco='Lizard', job='Warrior', tp='80', cap='104',
        atk='+30%', deff='-20%',
        stats={'hp': '5,508', 'acc': '879', 'atk': '1,028', 'eva': '704', 'def': '753'},
        ready=[
            R('Tail Blow', '1 charge', 'Additional effect: Stun. Damage varies with TP.',
              'Impaction'),
            R('Fireball', '1 charge',
              'Deals Fire elemental damage to enemies within area of effect. Damage varies with TP.'),
            R('Blockhead', '1 charge', 'Damage varies with TP.', 'Reverberation'),
            R('Brain Crush', '1 charge', 'Additional effect: Silence. Damage varies with TP.',
              'Liquefaction'),
            R('Infrasonics', '2 charges',
              '-40 Evasion for 3 minutes for enemies within a fan-shaped area. Area of effect '
              'varies with TP.'),
            R('Secretion', '1 charge',
              '+25 Evasion for pet and Beastmaster. Duration of effect varies with TP.'),
        ]),

    'Weevil Familiar': dict(fam='Lucani', eco='Vermin', cap='119', ready=list(LUCANI)),

    'Yellow Beetle Familiar': dict(fam='Yellow Beetle', eco='Vermin', tp='73',
        ready=list(YELLOW_BEETLE)),
}

# Re-sent pages that CORRECT an already-filled record.
FIX = {
    'Faithful Falcorr': dict(tp='74', cap='99', ready=list(HIPPOGRYPH)),
    'Bloodclaw Shasra': dict(tp='75', cap='99', ready=list(LYNX)),
    'Mailbuster Cetas': dict(tp='75', cap='95', ready=list(FLY)),
}
for f in list(NEW.values()) + list(FIX.values()):
    if 'deff' in f:
        f['def'] = f.pop('deff')

# ---------------------------------------------------------------- apply
print('=== REV 404 — 10 NEW JUG FAMILIARS ===')
for name, fields in sorted(NEW.items()):
    p = by_name[name]
    stored, page_cap = p.get('cap'), fields.get('cap')
    for k, v in fields.items():
        p[k] = v
    note = ('page prints "?" — jug-string cap %s kept' % stored if page_cap is None else
            'cap matches the jug string' if stored == page_cap else
            'CAP CHANGED %s -> %s' % (stored, page_cap))
    print('  %-24s %-14s %-9s cap %-5s %d ready   %s'
          % (name, fields['fam'], fields['eco'], page_cap or '-', len(fields['ready']), note))

print('\n=== RE-SENT PAGES THAT CORRECT AN ALREADY-FILLED RECORD ===')
for name, fields in sorted(FIX.items()):
    p = by_name[name]
    before = [r['n'] for r in (p.get('ready') or [])]
    old_tp = p.get('tp')
    for k, v in fields.items():
        p[k] = v
    after = [r['n'] for r in p['ready']]
    added = [n for n in after if n not in before]
    print('  %-20s ready %d -> %d  (+ %s)   tp %-12s -> %s   cap %s'
          % (name, len(before), len(after), ', '.join(added) or 'nothing',
             old_tp, fields['tp'], 'matches' if p.get('cap') == fields['cap'] else 'CHANGED'))

# ---------------------------------------------------------------- TP/hit normalisation
print('\n=== TP/hit NORMALISED TO THE INTEGER SCALE (rules 470/475 CLOSED) ===')
changed = 0
for p in pets:
    tp = p.get('tp')
    if not tp:
        continue
    m = re.fullmatch(r'(\d+)\.(\d)\s*/\s*hit', tp)
    if m:
        new = m.group(1) + m.group(2)
    elif re.fullmatch(r'\d+\s*/\s*hit', tp):
        new = tp.split('/')[0].strip()
    else:
        continue
    print('  %-24s %-12s -> %s' % (p['n'], tp, new))
    p['tp'] = new
    changed += 1
print('  %d values rewritten' % changed)
assert all(re.fullmatch(r'\d+', p['tp']) for p in pets if p.get('tp')), 'a TP value is not a bare integer'
vals = sorted({int(p['tp']) for p in pets if p.get('tp')})
print('  TP/hit now ranges %d-%d across %d familiars'
      % (vals[0], vals[-1], sum(1 for p in pets if p.get('tp'))))

# ---------------------------------------------------------------- rule 483 again
print('\n=== OLD `sections` LIST vs THE PAGE — Weevil Familiar ===')
prior = [i['n'] for s in (by_name['Weevil Familiar'].get('sections') or []) if s['t'] == 'Ready'
         for i in s['items']]
print('  old: %s' % ', '.join(prior))
print('  page: %s   -> REPLACED (the old list is the Beetle kit; this is a Lucani)'
      % ', '.join(r['n'] for r in LUCANI))
prior_yb = [i['n'] for s in (by_name['Yellow Beetle Familiar'].get('sections') or [])
            if s['t'] == 'Ready' for i in s['items']]
print('  Yellow Beetle Familiar: %d -> %d  (superset, + Rhinowrecker)' % (len(prior_yb), len(YELLOW_BEETLE)))

# ---------------------------------------------------------------- guards
for p in pets:
    if 'ready' in p and p.get('sections'):
        p['sections'] = [s for s in p['sections'] if s['t'] != 'Ready']
ABIL = json.load(open(os.path.join(BASE, 'mobs.json'), encoding='utf-8'))['abilities']
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
print('ready moves carrying a skillchain: %d'
      % sum(1 for p in pets for r in (p.get('ready') or []) if r.get('sc')))
print('familiars carrying a stat block: %d' % sum(1 for p in pets if p.get('stats')))
print('\nBST familiars with a Ready list recorded: %d of %d' % (len(done), len(pets)))
print('still to do (%d): %s' % (len(todo), ', '.join(todo)))

# the new list order the UI will use
order = sorted(pets, key=lambda p: (int(p['cap']) if (p.get('cap') or '').isdigit() else 10 ** 6,
                                    p['n']))
print('\nlowest-cap-first order, first 8: %s'
      % ', '.join('%s (%s)' % (p['n'], p.get('cap') or '-') for p in order[:8]))

json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('written: %s' % P)
