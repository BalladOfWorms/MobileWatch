#!/usr/bin/env python3
"""rev 387 — the S-Z batch. Ten folded, fourteen deleted, and the SINGLE-WORD PROPER NOUNS
section of the bucket goes to ZERO.

USER: ten panels plus "and that section is done, you can delete the rest in the last screenshot"

CONFLICT HANDLED: `shayaam` appears BOTH in the delete screenshot AND as one of the ten panels.
It is folded, not deleted — it is the fifth of five identical Red Versus Blue Blue Mage opponents
(qudeen, salyhaar, ubdeen, varajahl, shayaam) and deleting one of five identical siblings while
filing the other four would be obviously wrong. Flagged to the user.
"""
import json, collections, re

P = 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M, AB = d['mobs'], d['abilities']

def standard(fam):
    mem = [v for v in M.values() if v.get('fam') == fam]
    n = len(mem); floor = max(2, int(0.3 * n)); out = {}
    for k in ('crys', 'job', 'det', 'ab'):
        c = collections.Counter(json.dumps(v.get(k), ensure_ascii=False) for v in mem)
        raw, ct = c.most_common(1)[0]; val = json.loads(raw)
        out[k] = val if (val is not None and ct >= floor and val != []) else None
    c = collections.Counter(json.dumps([v.get('wk'), v.get('st')], ensure_ascii=False) for v in mem)
    raw, ct = c.most_common(1)[0]; wk, st = json.loads(raw)
    out['wk'], out['st'] = ((wk, st) if (wk is not None or st is not None) and ct >= floor
                            else (None, None))
    return out

STD = {}
def fold(key, fam, page=None, kit_add=(), clear=(), fill=('crys', 'job', 'det', 'wk', 'st', 'ab')):
    v = M[key]
    assert not v.get('fam'), (key, v.get('fam'))
    if fam not in STD:
        STD[fam] = standard(fam)
    s = STD[fam]
    v['fam'] = fam
    for f in clear:
        v.pop(f, None)
    v.update(page or {})
    filled = []
    for f in fill:
        if f not in v and s.get(f) is not None:
            v[f] = s[f]; filled.append(f)
    if kit_add:
        kit = list(v.get('ab') or [])
        for a in kit_add:
            if a not in kit:
                kit.append(a)
        v['ab'] = kit
    print('  %-12s -> %-11s filled %-22s kit %d' % (
        key, fam, ','.join(filled) or '-', len(v.get('ab') or [])))
    return v

print('=== FOLDS ===')

# Shadowsoul: the page says "Family: Kindred", which is not a family in this file — all 16
# `kindred <job>` records are filed Demon, so Kindred maps to Demon.
# Banner is "Campaign Leader", NOT "Notorious Monster", so no nm flag (the r386 banner rule).
fold('shadowsoul', 'Demon', dict(
    job='Dark Knight', agg=True, lnk=True, det=['True Sight', 'Scent'],
    zones=[['Xarcabard [S]', '70']],
    drops='Dread Spikes',
    spawn='One spawn during Campaign Battles in Xarcabard [S].',
    sp=['Death'],
    notes=['Appears during Campaign Battles as the leader of the Dark Kindred\u2019s Shadowsoul '
           'Battalion, deployed exclusively to Xarcabard.',
           'Absorbs both physical and magical damage after using Hellborn Yawp.',
           'He is a Dark Knight, so he casts dark magic \u2014 including Death.',
           'Rewards come as Union Spoils; he drops no gil.'],
), kit_add=['Hellborn Yawp'])

fold('shadowwing', 'Gargouille', dict(
    job='Black Mage', agg=True, lnk=True, det=['True Sight', 'True Sound'],
    zones=[['Beaucedine Glacier [S]']],
    spawn='One spawn during Campaign Battles in Beaucedine Glacier [S].',
    sp=['Bindga', 'Blindga', 'Dispelga', 'Graviga', 'Paralyga', 'Silencega', 'Blizzaga', 'Thundaga'],
    notes=['Appears during Campaign Battles as the leader of the Dark Kindred\u2019s Shadowwing '
           'Battalion, deployed exclusively to Beaucedine Glacier. Roughly 50,000 HP.',
           'Never lands on the ground.',
           'Additional effect on its attacks: a short Petrification.',
           'Casts area enfeebles \u2014 Bindga, Blindga, Dispelga, Graviga, Paralyga, Silencega \u2014 '
           'and area elemental spells that climb in tier as its HP falls.',
           'Uses Manafont more than once.',
           'Its Dark Orb has a far larger radius than usual and hits extremely hard. It also uses '
           'Dark Mist.'],
), kit_add=['Dark Orb', 'Dark Mist', 'Manafont'])

fold('shamarhaan', 'Humanoid', dict(
    job='Puppetmaster', nm=True,
    zones=[['Navukgo Execution Chamber', '75']],
    spawn='One spawn in the Navukgo Execution Chamber.',
    ab=['Overdrive'],
    notes=['Fought for Achieving True Power, the level 71 Puppetmaster limit break, alongside his '
           'automaton Valkeng.',
           'Uses Overdrive and every maneuver, and hand-to-hand weapon skills up to Howling Fist.',
           'Valkeng casts Stun and Shock Spikes, cannot change frames, and uses the automaton '
           'weapon skill Slapstick.'],
))

for k in ('shayaam', 'ubdeen', 'varajahl'):
    fold(k, 'Humanoid', dict(
        job='Blue Mage', agg=True, lnk=True, det=['True Sound'],
        zones=[['Leujaoam Sanctum', '75']],
        spawn='One spawn in Leujaoam Sanctum.',
        notes=['One of your opponents during Red Versus Blue.'],
    ))

# Simorg: the page says Immune: Light, which is the `im` field — so Light comes OUT of `st`,
# where it was stored as a mere -62.5% resistance.
si = fold('simorg', 'Wyvern', dict(
    nm=True, det=['Sight'],
    im=['Light'],
    st=[e for e in M['simorg']['st'] if e[0] != 'Light'],
    zones=[['Grauberg [S]', '70']],
    spawn='Spawned by selecting "Shredded Label" at D-8 in Grauberg [S] with the Blue-Labeled Crate '
          'key item. A level 70 cap is applied.',
    notes=['Assisted by six Hippocentaur.',
           'Uses the regular Wyvern TP moves plus Blizzard Breath, Thunder Breath, Chaos Breath and '
           'Hurricane Breath \u2014 the last of which damages and strips one piece of equipment.',
           'Can be tanked safely by a PLD/WAR as long as the pets are dealt with promptly, though MP '
           'becomes a problem after about ten minutes.',
           'Builds and spends TP normally until roughly 50% health, then spams breaths regardless '
           'of TP.'],
), kit_add=['Blizzard Breath', 'Thunder Breath', 'Chaos Breath', 'Hurricane Breath'])
assert si.get('im') == ['Light'] and not any(e[0] == 'Light' for e in si['st'])

fold('titanotaur', 'Taurus', dict(
    job='Monk', crys='Dark', det=['True Sight'],
    zones=[['Castle Zvahl Keep [S]', '83']],
    spawn='Two spawn in Castle Zvahl Keep [S]; sixteen-minute respawn.',
))

fold('umarid', 'Humanoid', dict(
    job='Warrior', nm=True, det=['Sight'],
    zones=[['Periqia', '75']],
    spawn='One spawn during Operation: Snake Eyes, in the cell at H-6.',
    notes=['Spawns during Operation: Snake Eyes, in the cell at H-6.',
           'He is charmed, and attacks as you approach.',
           'Fight him only until Lamia No.17 appears, then switch to her immediately \u2014 if Umarid '
           'is defeated the mission fails.'],
))

fold('yazquhl', 'Humanoid', dict(
    job='Warrior', nm=True,
    zones=[['The Ashu Talif', '75']],
    spawn='One spawn aboard The Ashu Talif.',
    notes=['Spawns for the quest Against All Odds, together with Gowam.'],
))

# ==================================================================== DELETES
SCREENSHOT = ['shailham', 'sharayaan', 'shayaam', 'sonia', 'tahbmar', 'tiyaash', 'udhaaman',
              'ulla', 'vahi', 'wabjahl', 'wharadi', 'yhalbin', 'zhadjaraf', 'zolku-azolku',
              'zonpa-zippa']
KEEP = {'shayaam'}                       # panel supplied this turn — see the header
ASKED = [k for k in SCREENSHOT if k not in KEEP]
print('\n=== DELETE GUARD (rule 389) ===')
print('  HELD BACK, panel supplied the same turn: %s' % sorted(KEEP))
targets, refused = [], []
for k in ASKED:
    v = M.get(k)
    if v is None:
        refused.append((k, 'MISSING'))
    elif v.get('fam'):
        refused.append((k, 'has fam %r' % v['fam']))
    elif v.get('zones'):
        refused.append((k, 'has zones %s lv=%s' % (v['zones'], v.get('lv'))))
    else:
        targets.append(k)
for k, why in refused:
    print('  REFUSED  %-14s %s' % (k, why))
print('  NM-flagged among the targets: %s' % [k for k in targets if M[k].get('nm')])

print('\n=== CROSS-REFERENCES FROM SURVIVING RECORDS (word-boundary) ===')
disp = {k: M[k]['n'] for k in targets}
hits = 0
for mk, mv in M.items():
    if mk in targets:
        continue
    blob = json.dumps(mv, ensure_ascii=False)
    for k, name in disp.items():
        if re.search(r"(?<![\w'-])%s(?![\w'-])" % re.escape(name), blob):
            print('  %-24s mentions %s' % (mk, name)); hits += 1
if not hits:
    print('  (none)')
for k in targets:
    del M[k]
print('  deleted %d of %d asked' % (len(targets), len(ASKED)))

# ==================================================================== GUARDS
bad = [(k, f) for k, mm in M.items() for f, val in mm.items() if val is None]
assert not bad, bad[:10]
zn = {x['name'] for x in json.load(open('app/src/main/assets/zones.json', encoding='utf-8'))['zones']}
def norm(s): return s.replace('\u2019', "'").replace("'", '').lower()
zi = {norm(z) for z in zn}
FOLDED = ['shadowsoul', 'shadowwing', 'shamarhaan', 'shayaam', 'simorg', 'titanotaur', 'ubdeen',
          'umarid', 'varajahl', 'yazquhl']
for k in FOLDED:
    for z in (M[k].get('zones') or []):
        assert norm(z[0] if isinstance(z, list) else z) in zi, (k, z)
items = {v['n'] for v in json.load(open('app/src/main/assets/ffxi_items.json', encoding='utf-8')).values()}
for k in FOLDED:
    for dr in (M[k].get('drops') or '').split(', '):
        if dr:
            assert dr in items, (k, dr)

left = sorted(k for k, v in M.items() if not v.get('fam') and len(k.split()) == 1)
print('\nsingle-word proper-noun orphans remaining: %d %s' % (len(left), left))
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('mobs %d | abilities %d | bucket %d' % (
    len(M), len(AB), sum(1 for v in M.values() if not v.get('fam'))))
