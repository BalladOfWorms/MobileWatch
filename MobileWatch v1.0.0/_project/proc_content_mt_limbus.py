#!/usr/bin/env python3
"""Master Trials + Limbus (119) content tagging (rev 253).

USER: "master trials and limbus to the content section"
Sources: BG-wiki Category:Master Trials and Category:Limbus (user screenshots).

Master Trials -> "Master Trials: <battlefield>"  (2-segment: the section IS the battlefield)
Limbus        -> "Limbus: <Apollyon|Temenos>: Tier N"  (the four Central NM tiers)

Only mobs that already exist are tagged; the rest are listed as plain text on the pages and
reported here so they can be created later.
"""
import json, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']

MASTER_TRIALS = {
    'Black and White': ['alexander', 'odin', 'brunhilde', 'gerhilde', 'grimgerde', 'helmwige',
                        'ortlinde', 'rossweisse', 'schwertleite', 'siegrune', 'waltraute'],
    'Unafraid of the Dark': ['shadow lord', 'tzee xicu the manifest', 'bloodcrown brradhod',
                             "za'dha adamantking"],
    'Sealed Fate': ['arch-ultima', 'arch-omega'],
    'Heroines Combat II': ['lion', 'prishe', 'lilisette', 'arciela'],
    'Crystal Paradise': ["eald'narche", "kam'lanaut", 'ark angel hm', 'ark angel ev',
                         'ark angel tt', 'ark angel mr', 'ark angel gk'],
    'Oathsworn Blade': ['august', 'teodor'],
    'Wings of War': ['chaos (nm)', 'bahamut'],
}

LIMBUS = {
    ('Apollyon', 'Tier 1'): ['ischyros sandworm', 'ischyros mantis', 'ischyros adamantoise'],
    ('Apollyon', 'Tier 2'): ['tolimi wyrm', 'tolimi dvergr', 'tolimi vampyr'],
    ('Apollyon', 'Tier 3'): ['omega forerunner'],
    ('Temenos', 'Tier 1'): ['agrios ixion', 'agrios alicorn', 'agrios aern'],
    ('Temenos', 'Tier 2'): ['pallikari khrysokhimaira', 'pallikari ironclad', 'pallikari mammet'],
    ('Temenos', 'Tier 3'): ['ultima forerunner'],
}

missing, tagged = [], []


def tag(key, t):
    m = M.get(key)
    if m is None:
        missing.append(key)
        return
    c = m.get('content') or []
    if t not in c:
        c.append(t)
    m['content'] = c
    m['nm'] = True
    tagged.append((key, t))


for bf, keys in MASTER_TRIALS.items():
    for k in keys:
        tag(k, 'Master Trials: %s' % bf)
for (zone, tier), keys in LIMBUS.items():
    for k in keys:
        tag(k, 'Limbus: %s: %s' % (zone, tier))

assert not [kk for mm in M.values() for kk, v in mm.items() if v is None]
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

from collections import Counter
c = Counter(t for m in M.values() for t in (m.get('content') or [])
            if t.startswith(('Master Trials', 'Limbus')))
print('tagged %d mobs' % len(tagged))
for t, n in sorted(c.items()):
    print('  %2d  %s' % (n, t))
print('MISSING (not tagged):', missing or '(none)')
