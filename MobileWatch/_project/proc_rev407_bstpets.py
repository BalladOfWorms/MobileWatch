#!/usr/bin/env python3
"""
REV 407 — the user adjudicates the three page-vs-bestiary disputes and supplies
the two missing familiar families. Touches jobs.json AND mobs.json.

USER: "corrosive ooze is water, choke breath is earth, spider web is 3% slow
       effect. presto family is flytrap, anna is hill lizard"

THE THREE DISPUTES SPLIT — NEITHER SOURCE WON THEM ALL
------------------------------------------------------
That is the finding. Rules 477/482 held all three open precisely because there
was no way to tell which side was right, and the answer turned out to be
different for each:

  Corrosive Ooze   BESTIARY was right (Water). Generous Arthur's page said Fire
                   -> the PET PAGE carried the error. Fixing the pet record.
  Choke Breath     PET PAGE was right (Earth). The bestiary def said "Wind-based
                   ... el: Wind" -> the BESTIARY carried the error, and 19 mobs
                   have been rendering it. Fixing the ability def.
  Spider Web       PET PAGE was right (3% Slow). The bestiary said "inflicts
                   Slow II" -> wrong potency on 40 mobs. Fixing the def.

=> Do NOT adopt "the bestiary always adjudicates" (rule 466) as a general law.
   It holds for TARGET SHAPE, where the ability table is systematically better.
   For ELEMENT and POTENCY both sources are fallible and a dispute needs a real
   ruling. 1 for the bestiary, 2 for the pet pages.

THE TWO FAMILIES ARE CORROBORATED BY DATA WE ALREADY HAD
---------------------------------------------------------
Neither page prints a Familiar column, which is why they sat empty since r398.
The stored kits confirm the user's answer independently:
  Audacious Anna's six moves — Tail Blow, Fireball, Blockhead, Brain Crush,
  Infrasonics, Secretion — are EXACTLY Warlike Patrick's Hill Lizard kit.
  Presto Julio's three — Soporific, Gloeosuccus, Palsy Pollen — are Flytrap.
`eco` is NOT written for either: their pages are the old layout and print none,
and eco has only ever come from a Lv.99 page. The bestiary's family_eco already
maps Flytrap -> Plantoid and Hill Lizard -> Lizard if it is ever wanted.

ALSO: `Colibri Familiar` was re-sent, identical to the rev-402 transcription —
ONE Ready move, Pecking Flurry. That CLOSES rule 478: the kit shrink is real,
not a cropped screenshot.
"""
import json, os

BASE = 'app/src/main/assets'
if not os.path.exists(BASE):
    BASE = 'android/' + BASE
PJ, PM = os.path.join(BASE, 'jobs.json'), os.path.join(BASE, 'mobs.json')
d = json.load(open(PJ, encoding='utf-8'))
mob = json.load(open(PM, encoding='utf-8'))
pets = d['pets']['9']
by_name = {p['n']: p for p in pets}
ABIL = mob['abilities']


def users(name):
    return [k for k, v in mob['mobs'].items() if name in (v.get('ab') or [])]


# ------------------------------------------------- 1. Corrosive Ooze: the PET record was wrong
print('=== `Corrosive Ooze` IS WATER — the BESTIARY was right, the pet page was wrong ===')
arthur = by_name['Generous Arthur']
row = next(r for r in arthur['ready'] if r['n'] == 'Corrosive Ooze')
old = row['d']
row['d'] = old.replace('Deals Fire elemental damage', 'Deals Water elemental damage')
assert row['d'] != old
print('  Generous Arthur / Corrosive Ooze')
print('    was: %s' % old)
print('    now: %s' % row['d'])
print('  bestiary def unchanged (el = %s, %d mobs use it)'
      % (ABIL['Corrosive Ooze']['el'], len(users('Corrosive Ooze'))))

# ------------------------------------------------- 2. Choke Breath: the BESTIARY def was wrong
print('\n=== `Choke Breath` IS EARTH — the PET PAGE was right, the bestiary def was wrong ===')
cb = ABIL['Choke Breath']
print('  was: el=%s  d=%s' % (cb['el'], cb['d']))
cb['el'] = 'Earth'
cb['d'] = ('Earth-based damage in a frontal area of effect. Additional effects: Silence and '
           'Paralysis.')
print('  now: el=%s  d=%s' % (cb['el'], cb['d']))
print('  %d mobs carry Choke Breath and have all been rendering Wind' % len(users('Choke Breath')))

# ------------------------------------------------- 3. Spider Web: the BESTIARY potency was wrong
print('\n=== `Spider Web` IS A 3%% SLOW — the PET PAGES were right, the bestiary was wrong ===')
sw = ABIL['Spider Web']
print('  was: d=%s  fx=%s' % (sw['d'], sw['fx']))
sw['d'] = 'AoE that inflicts a 3% Slow.'
sw['fx'] = ['Slow']
print('  now: d=%s  fx=%s' % (sw['d'], sw['fx']))
print('  %d mobs carry Spider Web and have all been claiming Slow II' % len(users('Spider Web')))
print('  (two pet pages printed 3%% — Gussy Hachirobe and Spider Familiar — rule 482)')

# ------------------------------------------------- 4. the two missing families
print('\n=== THE TWO FAMILIARS WITH NO `fam` — pages print no Familiar column ===')
FAMS = {'Presto Julio': 'Flytrap', 'Audacious Anna': 'Hill Lizard'}
KIT_PROOF = {'Presto Julio': ('Flytrap', 'Soporific / Gloeosuccus / Palsy Pollen'),
             'Audacious Anna': ('Hill Lizard', "exactly Warlike Patrick's kit")}
for name, fam in FAMS.items():
    p = by_name[name]
    assert not p.get('fam'), p.get('fam')
    p['fam'] = fam
    print('  %-16s fam = %-12s  corroborated by its stored kit: %s'
          % (name, fam, KIT_PROOF[name][1]))
print('  eco NOT written — old-layout pages print none (family_eco has Flytrap->%s, Hill Lizard->%s)'
      % (mob['family_eco'].get('Flytrap'), mob['family_eco'].get('Hill Lizard')))
print('  familiars still missing a fam: %d' % sum(1 for p in pets if not p.get('fam')))

# ------------------------------------------------- 5. Colibri Familiar re-confirmed (rule 478)
col = by_name['Colibri Familiar']
same = (col.get('cap') == '117' and col.get('tp') == '70'
        and col.get('stats') == {'hp': '5,308', 'acc': '915', 'atk': '750', 'eva': '744',
                                 'def': '915'}
        and [r['n'] for r in col['ready']] == ['Pecking Flurry'])
print('\n=== `Colibri Familiar` RE-SENT — rule 478 (the kit shrink) ===')
print('  rev-402 transcription %s' % ('RE-CONFIRMED: one Ready move, the shrink is real'
                                      if same else '!! DIVERGES !!'))
assert same

# ------------------------------------------------- guards
unmatched = sorted({it['n'] for p in pets for sec in (p.get('sections') or []) for it in sec['items']
                    if it['n'] not in ABIL} |
                   {r['n'] for p in pets for r in (p.get('ready') or []) if r['n'] not in ABIL})
print('\npet ability names with no bestiary definition: %d %s' % (len(unmatched), unmatched))
assert not unmatched
assert not [k for p in pets for k, v in p.items() if v is None], 'NULL POISON'
assert not [k for a in ABIL.values() for k, v in a.items() if v is None], 'NULL POISON (abilities)'
assert not [k for m in mob['mobs'].values() for k, v in m.items() if v is None], 'NULL POISON (mobs)'
assert isinstance(cb['el'], str) and isinstance(sw['fx'], list)
BST_ONLY = {'fam', 'job', 'lvl', 'cap', 'hp', 'dmg', 'tp', 'dur', 'traits', 'notes', 'ready',
            'eco', 'atk', 'def', 'stats'}
assert not [p['n'] for p in d['pets']['15'] if BST_ONLY & set(p)], 'a Summoner avatar was modified'
assert len(pets) == 97 and not [p for p in pets if 'ready' not in p]

print('\nroster %d, all with a Ready list, %d with a fam, %d abilities'
      % (len(pets), sum(1 for p in pets if p.get('fam')), len(ABIL)))
json.dump(d, open(PJ, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
json.dump(mob, open(PM, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('written: %s\nwritten: %s' % (PJ, PM))
