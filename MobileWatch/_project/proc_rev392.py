#!/usr/bin/env python3
"""
REV 392 — `Amorphic Spikes` defined from its page.

That was the single biggest entry in decision item 10: 32 Flan-type mobs pointed
at a name the `abilities` dict did not have, so every one of them rendered it as
a bare word. Undefined references drop 49 -> 17 and the distinct-name count
17 -> 16 in one write.

INCIDENTAL, AND WORTH MORE THAN THE ASK: looking for a house style to match, two
existing defs turned out to have an INTERWIKI LINK where their description should
be. `Magic Fruit`'s `d` was the bare string "de:Magische Frucht" and `Sheep
Song`'s was "de:Schafliedja:...Category:MagicCategory:Blue MagicCategory:Mob
Abilities". Both are the sixth flavour of leaked wiki markup, and audit.py's
detector CANNOT SEE EITHER — its regex wants brackets, and an interwiki prefix
has none. It scored 0 file-wide while these two sat there. Regex extended with
`Category:` and a leading two-letter language prefix; it now reads 2 before the
fix and 0 after.
"""
import json, os, re

P = 'app/src/main/assets/mobs.json'
if not os.path.exists(P):
    P = 'android/' + P
d = json.load(open(P))
M = d['mobs']; A = d['abilities']

def undef():
    return [a for m in M.values() for a in (m.get('ab') or []) if a not in A]
before_refs = undef()
print('undefined refs before: %d across %d names' % (len(before_refs), len(set(before_refs))))

# ------------------------------------------------------------- Amorphic Spikes
# Page fields used: Description, Type=Physical, Number of Hits=5, Target=Single.
# `Range` and `Additional Effects` are BLANK on the page, so `r` stays unset and
# `fx` is an explicit [] only because Additional Effects is a labelled row the
# page would have filled — the rest of the page's numbers go in notes.
assert 'Amorphic Spikes' not in A
A['Amorphic Spikes'] = {
    'd': 'Delivers a fivefold attack. Damage varies with TP.',
    't': 'Physical',
    'tgt': 'Single',
    'fx': [],
    'notes': 'Skillchain properties: Gravitation / Transfixion. Weapon-skill '
             'attributes are 20% DEX and 20% INT; fTP is 1.0 below 1500 TP and '
             '1.375 from 1500 to 2999. Also a Blue Magic spell, learned from Flan '
             'and usable from level 98 for 79 MP and 4 blue magic points, granting '
             'INT+5, MND+2 and the Gilfinder trait.',
}
users = [k for k, m in M.items() if 'Amorphic Spikes' in (m.get('ab') or [])]
print('\nAmorphic Spikes defined — %d mobs stop rendering it as a bare name '
      '(all %s)' % (len(users), sorted({M[k]['fam'] for k in users})))

# --------------------------------------------------- two interwiki-link `d`s
print('\n=== INTERWIKI MARKUP IN `d` ===')
# Magic Fruit already carried the real description in `notes`; it is promoted into
# `d` rather than invented, and the now-duplicate `notes` is dropped.
print('  Magic Fruit  d was: %r' % A['Magic Fruit']['d'])
print('               notes: %r' % A['Magic Fruit'].get('notes'))
A['Magic Fruit']['d'] = ("Restores over 3,000 HP to the user, erases its status "
                         "ailments, and resets the enmity of the player holding "
                         "the most hate.")
A['Magic Fruit'].pop('notes', None)

# Sheep Song's own structured fields already say what it does: t Magical,
# tgt AoE, fx ["Sleep I"]. The description is written from those, not guessed.
print('  Sheep Song   d was: %r' % A['Sheep Song']['d'])
print('               t/tgt/fx: %s / %s / %s' %
      (A['Sheep Song'].get('t'), A['Sheep Song'].get('tgt'), A['Sheep Song'].get('fx')))
A['Sheep Song']['d'] = 'Puts all players within range to sleep.'

# ------------------------------------------------------------- guards
MARKUP = re.compile(r"__NOTOC|==|\{\{|\[\[|File:|thumb\||\d+px|none\||'''|\{\||^\*|<br"
                    r"|Category:|(?:^|(?<=[a-z]))[a-z]{2}:[A-ZÀ-ÿ\u3000-\u9fff]")
hits = [k for k, v in A.items()
        if MARKUP.search(' '.join(str(v.get(f) or '') for f in ('d', 'notes')))]
print('\nextended markup detector: %d hits %s' % (len(hits), hits))
assert not hits

assert not [k for m in M.values() for k, v in m.items() if v is None], 'NULL POISON'
assert not [k for a in A.values() for k, v in a.items() if v is None], 'NULL POISON (ab)'
assert not [k for k, m in M.items() if k != m['n'].lower()]
sets = {s['label']: s for s in d['family_resist_sets']['Elemental']}
for key, label in [('shadowfang void', 'Dark'), ('touched gefyrst', 'Gefyrst')]:
    assert M[key]['wk'] == sets[label]['wk'] and M[key]['st'] == sets[label]['st'], key

after_refs = undef()
print('\nundefined refs after:  %d across %d names' % (len(after_refs), len(set(after_refs))))
print('remaining names: %s' % sorted(set(after_refs)))
json.dump(d, open(P, 'w'), separators=(', ', ': '), ensure_ascii=False)
print('\nmobs %d, abilities %d, orphans %d' %
      (len(M), len(A), sum(1 for m in M.values() if not m.get('fam'))))
