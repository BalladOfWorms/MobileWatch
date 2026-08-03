#!/usr/bin/env python3
"""Unity retag (rev 247) — "Unity Mobs" -> "Unity: Wanted: Wanted <1|2|3>".

USER: "starting unity. rename the content label to just Unity. ... mobs get link to bestiary"
rev-194 tagged the 56 Unity Wanted NMs with the flat tag `Unity Mobs` (levels + zones came with
it). The Content tab label is now just "Unity", and the guide page reads its roster through
vm.mobsForContent("Unity", "Wanted"), which needs the Group: Section: Role shape. The Wanted tier
(1/2/3) comes from the Category column of the BG table and becomes the Role segment.
"""
import json, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']
OLD = 'Unity Mobs'

TIER = {  # BG "Category" column
    'bounding belinda': 1, 'hugemaw harold': 1, 'prickly pitriv': 1, 'ironhorn baldurno': 1,
    'sleepy mabel': 1, 'serpopard ninlil': 1, 'abyssdiver': 1, 'immanibugard': 2, 'intuila': 1,
    'jester malatrix': 1, 'orcfeltrap': 1, 'sybaritic samantha': 1, 'valkurm imperator': 1,
    'cactrot veloz': 1, 'emperor arthro': 1, 'garbage gel': 2, 'joyous green': 1,
    'keeper of heiligtum': 1, 'tiyanak': 2, 'voso': 2, 'warblade beak': 1, 'woodland mender': 1,
    'arke': 1, 'ayapec': 2, 'azure-toothed clawberry': 2, 'bakunawa': 2, 'beist': 2,
    'centurio xx-i': 2, 'coca': 2, 'douma weapon': 1, 'king uropygid': 1,
    "kubool ja's mhuufya": 2, 'largantua': 1, 'lumber jill': 1, 'mephitas': 2, 'muut': 2,
    'specter worm': 2, 'strix': 1, 'vermillion fishfly': 2, 'azrael': 2, 'borealis shadow': 2,
    'camahueto': 2, 'carousing celine': 2, 'grand grenade': 2, 'vedrfolnir': 1, 'vidmapire': 2,
    'volatile cluster': 2, 'glazemane': 2, 'wyvernhunter bambrox': 2, 'hidhaegg': 2,
    'sovereign behemoth': 2, 'tolba': 2, "thu'ban": 3, 'sarama': 3, 'shedu': 3,
    'tumult curator': 3,
}

carried = [k for k, m in M.items() if OLD in (m.get('content') or [])]
untiered, nmset = [], []
for k in carried:
    m = M[k]
    tier = TIER.get(k)
    if tier is None:
        untiered.append(k)
        continue
    tags = [t for t in m['content'] if t != OLD]
    new = 'Unity: Wanted: Wanted %d' % tier
    if new not in tags:
        tags.append(new)
    m['content'] = tags
    if not m.get('nm'):
        m['nm'] = True
        nmset.append(k)

assert not [kk for mm in M.values() for kk, v in mm.items() if v is None]
assert not [k for k, m in M.items() if OLD in (m.get('content') or [])], 'old tag survived'
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

from collections import Counter
c = Counter(t for m in M.values() for t in (m.get('content') or []) if t.startswith('Unity'))
print('carried the old tag: %d | tiers unknown: %s' % (len(carried), untiered or '(none)'))
print('nm flag newly set on:', nmset or '(none)')
for t, n in sorted(c.items()):
    print('  %2d  %s' % (n, t))
