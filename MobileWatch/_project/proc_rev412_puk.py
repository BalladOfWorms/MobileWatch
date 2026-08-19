#!/usr/bin/env python3
"""rev 412 - PUK family repair.

Two problems, both traced to the rev-68 pass:

1. THE ELEMENT ROW WAS READ IN THE WRONG ORDER.  The BG-wiki Puk page prints its
   element gems as Fire / Wind / Lightning / Light / Ice / Earth / Water / Dark
   (verified by colour-matching every gem against the labelled reference set).
   rev-68 read it as Fire / Ice / Wind / Earth / Lightning / ... , which put the
   "A" cell on Ice instead of Wind and the 130% cell on Lightning instead of Ice.
   Truth: Puks ABSORB WIND and are WEAK TO ICE (+30%); Lightning is neutral.

2. THE FAMILY KIT WAS NEVER STAMPED.  rev-68 left the moves in family_notes and
   set `ab` on three NMs only, so 20 of 24 records render with no abilities at
   all in every downstream tool.

Also: Obfuscate's element icon is the pale Light gem (it inflicts Flash);
Boreas Mantle (Phantom Puk's ISNM replica move) was missing from `abilities`
entirely; two notes still said "III Wind" after the rev-379 key rename.

Author: BalladOfWorms
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jsonfmt

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
mobs, abil = d['mobs'], d['abilities']

puks = {k: v for k, v in mobs.items() if v.get('fam') == 'Puk'}
assert len(puks) == 24, len(puks)

FAMILY_WK = [["Piercing", "+12.5%"], ["Ranged", "+12.5%"], ["Fire", "+15%"],
             ["Ice", "+30%"], ["Earth", "+15%"], ["Water", "+15%"],
             ["Light", "+15%"], ["Dark", "+15%"]]

# ---------------------------------------------------------------- 1. the grid
grid_fixed = absorb_fixed = 0
for k, m in puks.items():
    wk = m.get('wk')
    if wk:
        new = []
        for pair in wk:
            if pair[0] == 'Lightning' and pair[1] == '+30%':
                new.append(['Ice', '+30%'])       # the mis-mapped cell
            else:
                new.append(pair)
        if new != wk:
            m['wk'] = new
            grid_fixed += 1
    if m.get('ab_el') == ['Ice']:
        m['ab_el'] = ['Wind']
        absorb_fixed += 1

# amymone's peapuk still carried the pre-rev-68 junk import stamp
am = mobs["amymone's peapuk"]
if am.get('wk') == [["Piercing", "+25%"], ["Ice", "+12.5%"]]:
    am['wk'] = [list(p) for p in FAMILY_WK]
    am['ab_el'] = ['Wind']
    grid_fixed += 1

# ------------------------------------------------------------------ 2. the kit
BASE = ['Crosswind', 'Obfuscate', 'Wind Shear', 'Zephyr Mantle']
MAMOOK = {'puk', 'carpophagous puk', 'sea puk'}          # "Ill Wind: Mamook Puks and NMs only"
PEAPUK = {'peapuk', 'putrid peapuk', 'snaggletooth peapuk', "amymone's peapuk"}
PAGE_SOURCED = {'jaculus', 'nguruvilu', 'sarimanok'}     # own page publishes a smaller set

stamped = 0
for k, m in puks.items():
    if k in PAGE_SOURCED:
        continue
    kit = list(BASE)
    if k == 'phantom puk':
        # ISNM "Shadows of the Mind" variant: Boreas Mantle replaces Zephyr Mantle
        kit[kit.index('Zephyr Mantle')] = 'Boreas Mantle'
    if k in MAMOOK or m.get('nm'):
        kit.append('Ill Wind')
    if k in PEAPUK or m.get('nm'):
        kit.append('White Wind')
    m['ab'] = kit
    stamped += 1

# ------------------------------------------------------------- 3. ability defs
abil['Obfuscate']['el'] = 'Light'                        # pale Light gem, and it inflicts Flash
abil['Boreas Mantle'] = {
    "d": "Creates ghostly copies of the user.",
    "tgt": "Self",
    "notes": "Only used by the Phantom Puk in the ISNM Shadows of the Mind. "
             "Instead of the ordinary Blink effect it creates replicas of itself (500 HP each).",
}

# --------------------------------------------------------- 4. prose / spawn fix
for k in ('nguruvilu', 'sarimanok'):
    mobs[k]['notes'] = [n.replace('III Wind', 'Ill Wind') for n in mobs[k]['notes']]

mobs['vulpangue']['spawn'] = 'Forced (trade Hellcage Butterfly to ??? (D-10))'
mobs['nis puk']['spawn'] = 'Lottery (Sea Puk) (H-9, second map)'

# ----------------------------------------------------------------- 5. guards
assert not [k for m in d['mobs'].values() for k, v in m.items() if v is None]
assert not [k for k, m in d['mobs'].items() if k != m['n'].lower()]
undef = [a for m in puks.values() for a in (m.get('ab') or []) if a not in abil]
assert not undef, undef[:10]   # file-wide there are 19 deliberate player-WS/JA refs
for k, m in puks.items():
    assert m.get('ab'), k
    assert m.get('ab_el') in (None, ['Wind']), (k, m.get('ab_el'))
    assert not [p for p in (m.get('wk') or []) if p[0] == 'Lightning']

jsonfmt.dump(d, P)          # one record per line — never plain json.dump here
print(f"grids fixed {grid_fixed} · absorbs fixed {absorb_fixed} · kits stamped {stamped}")
print(f"mobs {len(mobs)} · abilities {len(abil)}")
