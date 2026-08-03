#!/usr/bin/env python3
"""rev 382 — the Trust-named orphan block resolved.

USER: seven BG panels (Ayame, Klara, Maat, Prishe, Qultada, Trion, Volker), all
"Family: Humanoids", plus a screenshot of the REMAINING Trust-named list with the
ruling "the ones leftover in the screenshot are strictly npcs with no combat
encounters, ok to remove those".

So: stamp the seven from their panels, delete the leftovers.

Guards carried from rules 385 / 389 / null-poison:
  - refuse any delete target that has a `fam`
  - refuse any delete target that has `zones`
  - every target must exist and still be fam=None
  - print every cross-reference from a SURVIVING record
  - assert no None-valued keys before json.dump
"""
import json, sys, collections

P = 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M, AB = d['mobs'], d['abilities']

# ---------------------------------------------------------------- 1. DELETES
# The 13 names still on the Trust-named list in the user's screenshot.
DELETE_ASKED = [
    'areuhat', 'darrcuiln', 'elivira', 'excenmille', 'ferreous coffin',
    'kayeel-payeel', 'leonoyne', 'lhu mhakaracca', 'maximilian',
    'naja salaheem', 'noillurie', 'rainemard', 'romaa mihgo',
]

targets, refused = [], []
for k in DELETE_ASKED:
    v = M.get(k)
    if v is None:
        refused.append((k, 'MISSING from the file'))
    elif v.get('fam'):
        refused.append((k, "has a family: %r" % v['fam']))
    elif v.get('zones'):
        refused.append((k, 'has zones: %r  (real, fightable — NOT a bare NPC stub)' % (v['zones'],)))
    else:
        targets.append(k)

print('=== DELETE GUARD ===')
for k, why in refused:
    print('  REFUSED  %-18s %s' % (k, why))
print('  will delete %d of %d asked' % (len(targets), len(DELETE_ASKED)))

# cross-reference scan against SURVIVING records (rule 385 guard 3)
print('\n=== CROSS-REFERENCES FROM SURVIVING RECORDS ===')
disp = {k: M[k]['n'] for k in targets}
hits = 0
for mk, mv in M.items():
    if mk in targets:
        continue
    blob = json.dumps(mv, ensure_ascii=False)
    for k, name in disp.items():
        if name in blob:
            print('  %-28s mentions %s' % (mk, name)); hits += 1
if not hits:
    print('  (none)')

for k in targets:
    del M[k]

# ------------------------------------------------- 2. NEW ABILITY DEFINITIONS
# Mob-side moves the panels actually describe. Player JAs / WS are NOT added
# here (rule 396 — the abilities table is mob TP moves only).
NEW_AB = {
    'Temblor Blade': {
        'd': "Area-of-effect sword weapon skill: heavy magic damage and Petrification. Also resets the user's hate.",
        't': 'Magical', 'tgt': 'AoE', 'fx': ['Petrification', 'Hate Reset'],
        'notes': "Klara's signature move; used in both of her quest battles.",
    },
    'Darkring Blade': {
        'd': 'Area-of-effect sword weapon skill: heavy damage, knockback and Curse, dropping maximum HP by about half.',
        't': 'Physical', 'tgt': 'AoE', 'fx': ['Knockback', 'Curse', 'Max HP Down'],
        'notes': 'Klara only uses this in the Bonds of Mythril fight.',
    },
    'Royal Bash': {
        'd': 'An enhanced Shield Bash: single-target damage and Stun.',
        't': 'Physical', 'tgt': 'Single', 'fx': ['Stun'],
    },
    'Auroral Uppercut': {
        'd': 'Single-target damage and Stun.',
        't': 'Physical', 'tgt': 'Single', 'fx': ['Stun'],
    },
    'Nullifying Dropkick': {
        'd': 'Single-target damage and knockback.',
        't': 'Physical', 'tgt': 'Single', 'fx': ['Knockback'],
    },
    'Knuckle Sandwich': {
        'd': 'Conal damage that inflicts Weakness.',
        't': 'Physical', 'tgt': 'Cone AoE', 'fx': ['Weakness'],
    },
}
for name, defn in NEW_AB.items():
    if name in AB:
        print('  ability ALREADY DEFINED, skipped: %s' % name)
    else:
        AB[name] = defn

# --------------------------------------------------------- 3. HUMANOID STAMPS
# Panel data only. No family grid/crys/job stamp: the Humanoid family has no
# uniform standard (46 members, crys None across the board, 29 with no grid,
# job per-mob), so these are individual story NMs.
# det is NOT re-stamped where a panel's Detects box is blank (rule 350) —
# only the "S" flag in the Notes column licenses a Sight write.
STAMP = {
    'ayame': dict(
        job='Samurai', nm=True, agg=True,
        zones=[['Stellar Fulcrum']],
        ab=['Meikyo Shisui'],
        spawn='One spawn in Stellar Fulcrum for the Heroine\u2019s Combat special BCNM.',
        notes=[
            'Fought for the Heroine\u2019s Combat special BCNM.',
            'Opens with Meikyo Shisui, and will skillchain with herself.',
        ],
    ),
    'klara': dict(
        job='Paladin / Warrior', nm=True, agg=True, det=['Sight'],
        zones=[['Everbloom Hollow'], ['Throne Room [S]']],
        ab=['Temblor Blade', 'Swift Blade', 'Flat Blade', 'Circle Blade', 'Savage Blade', 'Darkring Blade'],
        spawn='One spawn in Everbloom Hollow (What Price Loyalty) and one in Throne Room [S] (Bonds of Mythril).',
        notes=[
            'Fought in both the What Price Loyalty and Bonds of Mythril quests.',
            'Temblor Blade is an AoE weapon skill dealing heavy magic damage and Petrification, and it also resets hate.',
            'In What Price Loyalty she has roughly 25,000 HP, and 12% movement speed is not enough to kite her.',
            'In Bonds of Mythril she adds Darkring Blade: an AoE knockback with heavy damage and Curse, dropping maximum HP by about half.',
        ],
    ),
    'maat': dict(
        job='Varies (any job except Blue Mage, Corsair, Puppetmaster, Scholar, Dancer, Geomancer, Rune Fencer)',
        nm=True, lv=[70, 70],
        zones=[['Horlais Peak', '70'], ['Balgas Dais', '70'], ['Waughroon Shrine', '70'],
               ['QuBia Arena', '70'], ['Chamber of Oracles', '70']],
        spawn='One spawn; the job you face and the arena you face it in are both set by your own job.',
        notes=[
            'Fought during the Shattering Stars quest \u2014 the level-75 limit break \u2014 and again in The Ultimate Challenge.',
            'Level 70 in every version. He takes the job matching your own, and the arena changes with it: Warrior, Black Mage and Ranger in Horlais Peak; Monk, White Mage and Summoner in Balga\u2019s Dais; Red Mage, Thief and Beastmaster in Waughroon Shrine; Paladin, Dark Knight and Bard in Qu\u2019Bia Arena; Samurai, Ninja and Dragoon in the Chamber of Oracles.',
            'Three versions bring help: Beastmaster is assisted by Maat\u2019s Pet, Dragoon by Maat\u2019s Wyvern, Summoner by Maat\u2019s Avatar.',
            'The Thief version can be stolen from for a Scroll of Instant Warp.',
            'He drops nothing.',
        ],
    ),
    'prishe': dict(
        job='Monk', nm=True, agg=True,
        zones=[['Stellar Fulcrum'], ['Nyzul Isle']],
        ab=['Hundred Fists', 'Auroral Uppercut', 'Nullifying Dropkick', 'Knuckle Sandwich', 'Benediction'],
        spawn='One spawn in Stellar Fulcrum (Heroine\u2019s Combat) and one in Nyzul Isle (Heroines\u2019 Holdfast).',
        notes=[
            'Fought for Heroine\u2019s Combat in Stellar Fulcrum, where she uses Hundred Fists, Auroral Uppercut and Nullifying Dropkick.',
            'Fought again in Nyzul Isle for Heroines\u2019 Holdfast, adding Knuckle Sandwich and Benediction.',
            'Auroral Uppercut is single-target damage and Stun; Nullifying Dropkick is single-target damage and knockback; Knuckle Sandwich is conal damage that inflicts Weakness.',
        ],
    ),
    'qultada': dict(
        job='Corsair', nm=True,
        zones=[['Talacca Cove']],
        spawn='One spawn in Talacca Cove for Breaking the Bonds of Fate.',
        notes=[
            'Spawns for Breaking the Bonds of Fate, the level-71 Corsair limit break quest.',
            'Nothing to drop and nothing to steal.',
        ],
    ),
    'trion': dict(
        job='Paladin', nm=True, agg=True,
        zones=[['Stellar Fulcrum']],
        ab=['Royal Bash'],
        spawn='One spawn in Stellar Fulcrum for the Hero\u2019s Combat special BCNM.',
        notes=[
            'Fought for the Hero\u2019s Combat special BCNM, alongside Volker.',
            'Royal Bash is an enhanced Shield Bash. He also casts a Protect version the page calls Royal Savior, on himself only.',
            'Will skillchain with Volker.',
        ],
    ),
    'volker': dict(
        job='Warrior', nm=True, agg=True,
        zones=[['Stellar Fulcrum']],
        ab=['Warcry'],
        spawn='One spawn in Stellar Fulcrum for the Hero\u2019s Combat special BCNM.',
        notes=[
            'Fought for the Hero\u2019s Combat special BCNM, alongside Trion.',
            'Uses Warcry on himself only \u2014 the page labels it Berserk-Ruf.',
            'Will skillchain with Trion.',
        ],
    ),
}

print('\n=== HUMANOID STAMPS ===')
for k, patch in STAMP.items():
    v = M[k]
    assert not v.get('fam'), (k, v.get('fam'))
    v['fam'] = 'Humanoid'
    for f, val in patch.items():
        v[f] = val
    print('  %-10s job=%-12s lv=%s zones=%d ab=%d' % (
        k, (v.get('job') or '')[:12], v.get('lv'), len(v.get('zones') or []), len(v.get('ab') or [])))

# ------------------------------------------------------------------- 4. GUARDS
bad = [(k, f) for k, m in M.items() for f, val in m.items() if val is None]
assert not bad, bad[:10]
bad = [(k, f) for k, a in AB.items() for f, val in a.items() if val is None]
assert not bad, bad[:10]

zn = {x['name'] for x in json.load(open('app/src/main/assets/zones.json', encoding='utf-8'))['zones']}
def norm(s): return s.replace('\u2019', "'").replace("'", '').lower()
zi = {norm(z) for z in zn}
for k in STAMP:
    for z in (M[k].get('zones') or []):
        assert norm(z[0]) in zi, (k, z[0])

undef = collections.Counter(a for v in M.values() for a in (v.get('ab') or []) if a not in AB)
print('\nundefined ability refs: %d across %d names' % (sum(undef.values()), len(undef)))
print('  new-to-the-list from this rev:', [n for n in ('Warcry', 'Shield Bash', 'Flat Blade', 'Circle Blade') if n in undef])

json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

print('\nmobs %d | abilities %d | bucket %d' % (
    len(M), len(AB), sum(1 for v in M.values() if not v.get('fam'))))
