#!/usr/bin/env python3
"""
REV 401 — five more Lv.99 jug familiars. Runs after 398, 399 and 400.

THIS BATCH RESOLVES THE THING REV 400 DELIBERATELY LEFT OPEN.

Rev 400 refused to act on the Lv.99 pages' Level Cap column because it prints
"119 (119)" / "110 (119)" and it was not clear whether the main figure or the
parenthetical was the value. All five pages here print a DIFFERENT main figure —
116, 109, 117, 105, 113 — and every one of them matches the cap already stored
from the jug string, exactly. That is 7 of 9 across the two batches matching on
the main number, with the parenthetical a constant 119 throughout.

=> THE FORMAT IS SETTLED: the main figure is the cap and (119) is a footnote.
=> Which means the two that did NOT match were never a reading problem, they are
   real value conflicts — and rule 467 already says the familiar page beats the
   jug string. So rev 400's hold is REVERSED here: `Aged Angus` 104 -> 119 and
   `Alluring Honey` 115 -> 119.

TWO SMALLER THINGS THE PAGES SETTLED ON THEIR OWN:

- `Filamented Hold` reads "50% Slow for enemies within a fan-shaped area", which
  is the bestiary definition word for word (~50%, cone). Rev 399 had to choose
  between the Mite page (single target) and the Lifedrinker Lars page (cone, 25%)
  and went with the ability table. That was right, and Lars' 25% is the outlier.

- `Brainy Waluis` spells it **Frogkick**, one word — the same spelling jobs.json
  originally had and rev 398 normalised away. The bestiary table says `Frog Kick`
  and 62 mobs use that form, so the normalisation STANDS (it is what makes the
  pet and mob data cross-reference), but two BST sources now disagree with it and
  that is worth knowing.

Special Traits are icon-only on all five and are not transcribed (rule 472).
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
    'Anklebiter Jedd': dict(fam='Diremite', eco='Vermin', job='Dark Knight', tp='73',
        cap='116', atk='+30%',
        stats={'hp': '4,938', 'acc': '886', 'atk': '1,107', 'eva': '701', 'def': '911'},
        ready=[
            R('Double Claw', '1 charge', 'Damage varies with TP.', 'Liquefaction'),
            R('Grapple', '1 charge',
              'Physical damage to enemies within a fan-shaped area. Damage varies with TP.',
              'Reverberation'),
            R('Spinning Top', '1 charge',
              'Physical damage to enemies within range. Damage varies with TP.', 'Impaction'),
            R('Filamented Hold', '2 charges',
              '50% Slow for enemies within a fan-shaped area. Duration varies with TP.'),
        ]),
    'Attentive Ibuki': dict(fam='Tulfaire', eco='Bird', job='Warrior', tp='75',
        cap='109', atk='-10%', deff='-10%',
        stats={'hp': '5,354', 'acc': '869', 'atk': '720', 'eva': '727', 'def': '849'},
        ready=[
            R('Molting Plumage', '1 charge',
              'Wind damage to enemies within a fan-shaped area. Additional effect: Dispel '
              '(light-based). Area of effect varies with TP.'),
            R('Swooping Frenzy', '2 charges',
              'Physical damage to enemies within a fan-shaped area. Additional effects: -25% '
              'Defense and -25 magic defense bonus. Duration varies with TP, from 60 seconds to '
              'two and a half minutes.', 'Fusion / Reverberation'),
            R('Pentapeck', '3 charges',
              'Physical damage. Additional effect: Amnesia. Duration varies with TP.',
              'Light / Distortion'),
        ]),
    'Blackbeard Randy': dict(fam='Tiger', eco='Beast', job='Warrior', tp='95',
        cap='117', atk='+60%', deff='-10%',
        stats={'hp': '4,860', 'acc': '889', 'atk': '1,266', 'eva': '704', 'def': '855'},
        ready=[
            R('Roar', '2 charges',
              'Paralyzes every enemy within range. Duration varies with TP.'),
            R('Razor Fang', '1 charge', 'Damage varies with TP.', 'Impaction'),
            R('Claw Cyclone', '1 charge',
              'Physical damage to enemies within a fan-shaped area. Damage varies with TP.',
              'Scission'),
            R('Crossthrash', '2 charges',
              'Physical damage to every enemy in a fan-shaped area in front of the pet. '
              'Additional effect: Dispel. Damage varies with TP.', 'Distortion / Detonation'),
            R('Predatory Glare', '2 charges',
              'Stuns every enemy in a fan-shaped area in front of the pet. The page says damage '
              'varies with TP, but it deals no damage — a localisation error.'),
        ]),
    'Bouncing Bertha': dict(fam='Chapuli', eco='Vermin', job='Warrior', tp='75',
        cap='105', atk='+10%',
        stats={'hp': '5,858', 'acc': '879', 'atk': '950', 'eva': '707', 'def': '948'},
        ready=[
            R('Sensilla Blades', '1 charge',
              'Physical damage to enemies within a fan-shaped area. Damage varies with TP.',
              'Scission'),
            R('Tegmina Buffet', '2 charges',
              'Physical damage to enemies within range. Additional effect: Choke (-33 VIT and 15 '
              'damage per tick) for 60 seconds. Damage varies with TP.', 'Distortion / Detonation'),
        ]),
    'Brainy Waluis': dict(fam='Funguar', eco='Plantoid', job='Warrior', tp='85', cap='113',
        stats={'hp': '5,508', 'acc': '886', 'atk': '796', 'eva': '704', 'def': '948'},
        ready=[
            R('Frog Kick', '1 charge',
              "Delivers an attack that ignores the target's defense. The amount ignored varies "
              'with TP.', 'Compression'),
            R('Spore', '1 charge', 'Paralyzes an enemy. Duration varies with TP.'),
            R('Queasyshroom', '2 charges',
              'Additional effect: Poison (7 damage per tick). Duration varies with TP.'),
            R('Numbshroom', '2 charges',
              'Additional effect: Paralysis. Duration varies with TP.'),
            R('Shakeshroom', '2 charges',
              'Additional effect: Disease. Duration varies with TP.'),
            R('Silence Gas', '3 charges',
              'Darkness damage to enemies within a fan-shaped area. Additional effect: Silence. '
              'Duration varies with TP.'),
            R('Dark Spore', '3 charges',
              'Darkness damage to enemies within a fan-shaped area. Additional effect: Blind '
              '(-30 accuracy). Duration varies with TP.'),
        ]),
}
for f in DATA.values():
    if 'deff' in f:
        f['def'] = f.pop('deff')

print('=== 5 MORE Lv.99 FAMILIARS ===')
for name, fields in DATA.items():
    p = by_name[name]
    stored = p.get('cap')
    for k, v in fields.items():
        p[k] = v
    match = 'cap matches the jug string' if stored == fields['cap'] else 'CAP CHANGED %s -> %s' % (stored, fields['cap'])
    print('  %-18s %-10s %-9s cap %-4s %d ready   %s'
          % (name, fields['fam'], fields['eco'], fields['cap'], len(fields['ready']), match))

# ------------------------------------------------- reverse the rev-400 hold
print('\n=== THE LEVEL-CAP COLUMN IS NOW SETTLED (see the header) ===')
print('  5 of 5 this batch print a distinct main figure and all 5 match the stored cap.')
print('  With 7 of 9 matching across both batches, the main figure IS the cap.')
for name, page in (('Aged Angus', '119'), ('Alluring Honey', '119')):
    p = by_name[name]
    print('  %-16s cap %s -> %s   (rev 400 held this back; the page wins, rule 467)'
          % (name, p.get('cap'), page))
    p['cap'] = page

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
print('ready moves carrying a skillchain: %d' % len(sc))
print('\nBST familiars with a Ready list recorded: %d of %d' % (len(done), len(pets)))
print('still to do (%d): %s%s' % (len(todo), ', '.join(todo[:10]), ' …' if len(todo) > 10 else ''))
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('written: %s' % P)
