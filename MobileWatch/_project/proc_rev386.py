#!/usr/bin/env python3
"""rev 386 — the M-S panel batch: 15 folded, 13 deleted.

USER: fourteen panels plus "dwende is morbol. icant find darkness anywhere, you want to try?
mobs in last screenshot can be removed"

Same policy as r385: the mob's own page wins outright, the family standard FILLS BLANKS ONLY,
and a page's Notes-column flags beat any inherited ["Sight","Sound","True Sight"] import stamp.
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
        # an EMPTY list is not a stamp — writing ab=[] would assert "genuinely no moves" (Avatar
        # and Elemental both mode to [], and Razfahd/Onibi must not inherit that claim)
        ok = val is not None and ct >= floor and val != []
        out[k] = val if ok else None
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
    print('  %-13s -> %-11s filled %-22s kit %d' % (
        key, fam, ','.join(filled) or '-', len(v.get('ab') or [])))
    return v

print('=== FOLDS ===')

fold('dwende', 'Morbol')                                    # user ruling

fold('mistdagger', 'Humanoid', dict(
    job='Ninja', nm=True, lnk=True, det=['True Sight'],
    zones=[['Rala Waterways [U]', '108']],
    spawn='One spawn in the Behind the Sluices battlefield.',
    notes=['A mission boss, fought in Behind the Sluices in Rala Waterways [U].', 'Casts Ninjutsu.'],
))

# Mortobello: the page's resist grid is ALL "?", which is no data at all — the stored grid stays,
# minus the bogus "Dark Earth" row. The General Notes state a smaller kit outright, so it is trimmed.
mo = fold('mortobello', 'Funguar', dict(
    crys='Dark', det=['Sound'],
    st=[['Water', '-50%'], ['Dark', '-50%']],
    ab=['Queasyshroom', 'Numbshroom', 'Shakeshroom'],
    notes=['Can only use Queasyshroom, Numbshroom and Shakeshroom \u2014 once each and in that order, '
           'each one visibly spending one of the three spores on its cap.'],
))

fold('nirgali', 'Leech', dict(
    job='Warrior', crys='Water', lv=[88, 88], resp=960, lnk=True, det=['Sight'],
    zones=[['Arrapago Reef', '88']],
    spawn='Eighteen spawn in Arrapago Reef; sixteen-minute respawn.',
    notes=['5,707-5,715 HP.'],
))

fold('nutcracker', 'Opo-opo', dict(
    job='Warrior', nm=True, agg=True, lv=[55, 55],
    zones=[['Yuhtunga Jungle', '55']],
    spawn='Spawned from the Field Parchment at F-10 in Yuhtunga Jungle with the Chapter 5 Elite '
          'Training page, by trading 22 Beastmen\u2019s Seals, up to 1100 gil, or an item up to level 55.',
    notes=['A Fields of Valor notorious monster, roughly 3000 HP.',
           'Like all Fields of Valor notorious monsters it spawns with random attributes \u2014 '
           'additional effects on melee strikes, job traits, buffs such as shadows.'],
))

fold('oko', 'Humanoid', dict(
    job='Ninja', nm=True, det=['True Sight'],
    zones=[['Leujaoam Sanctum', '79-80']],
    spawn='One spawn during Imperial Code.',
    notes=['Appears in Imperial Code.'],
))

fold('onibi', 'Elemental', dict(
    job='Black Mage / Red Mage / Dark Knight', nm=True, lnk=True,
    zones=[['Waughroon Shrine', '66-67']],
    spawn='One spawn, assisting Onki.',
    notes=['Assists Onki in the battlefield event for the Samurai AF3 quest A Thief in Norg!?.',
           'Its crystal and its elemental weakness both vary.'],
))

fold('pixiebane', 'Rafflesia', dict(
    crys='Earth', nm=True,
    zones=[['Fort Karugo-Narugo [S]']],
    spawn='Four spawn for the quest Succor to the Sidhe.',
    notes=['Spawned for the quest Succor to the Sidhe.'],
))

fold('qudeen', 'Humanoid', dict(
    job='Blue Mage', det=['True Sound'],
    zones=[['Leujaoam Sanctum', '75']],
    spawn='One spawn in Leujaoam Sanctum.',
    notes=['Fought for Red Versus Blue.'],
))

fold('raubahn', 'Humanoid', dict(
    job='Blue Mage', nm=True, det=['True Sight'],
    zones=[['Jade Sepulcher', '70'], ['Leujaoam Sanctum'], ['Nyzul Isle']],
    spawn='One spawn in each of three fights: The Beast Within in the Jade Sepulcher, Red Versus '
          'Blue in Leujaoam Sanctum, and Nashmeira\u2019s Plea on Nyzul Isle.',
    notes=['A mission boss. In The Beast Within \u2014 the Blue Mage limit break \u2014 he uses '
           'pre-Wings of the Goddess Blue Magic up to level 70, every sword weapon skill available '
           'to a level 70 Blue Mage, Quick Magic, and often answers your own Azure Lore with his.',
           'In Red Versus Blue he must be defeated to unlock the Rune of Release and clear the assault; '
           'roughly 3,000 HP there.',
           'In Nashmeira\u2019s Plea he fights alongside Razfahd but can be pulled separately, since '
           'Razfahd cannot move. 5,500-6,000 HP.',
           'He Reraises twice. After each Reraise he gains a partial resistance \u2014 around 50% \u2014 '
           'to whichever damage type mostly killed his previous life, announced in the chat log. Those '
           'resistances stack, so if the first two kills use the same type he is immune to it on the '
           'third life. Killing him once with magic damage avoids making him immune to melee.',
           'He uses Azure Lore once on his second life and once on his third, and is susceptible to sleep.',
           'Eyes On Me is the only blue magic he casts in that fight: heavy damage, not blocked by '
           'Utsusemi shadows, but stunnable.'],
))

fold('razfahd', 'Avatar', dict(
    job='Red Mage / White Mage', det=['True Sight'],
    zones=[['Nyzul Isle', '76']],
    spawn='One spawn in the first battle of Nashmeira\u2019s Plea.',
    notes=['A mission boss, fought in the first battle of Nashmeira\u2019s Plea alongside Raubahn.',
           'He sits inside the Iron Colossus, so he neither moves nor regenerates health.',
           'At 50% health he becomes completely immune to damage through Perfect Defense. The battle '
           'ends there \u2014 but only if Raubahn has also been defeated a third time.'],
))

fold('saizo', 'Humanoid', dict(
    job='Ninja', nm=True, det=['True Sight'],
    zones=[['Leujaoam Sanctum', '79-80']],
    spawn='One spawn during Imperial Code.',
    notes=['Appears in Imperial Code.',
           'He wields a Great Katana rather than the usual ninja katana.'],
))

fold('salyhaar', 'Humanoid', dict(
    job='Blue Mage', det=['True Sound'],
    zones=[['Leujaoam Sanctum', '75']],
    spawn='One spawn in Leujaoam Sanctum.',
    notes=['Fought for Red Versus Blue.'],
))

fold('satyral', 'Manticore', dict(
    nm=True,
    zones=[['Eastern Altepa Desert']],
    spawn='Spawned from the Field Parchment at I-10 with the Chapter 5 Elite Training page, by '
          'trading 22 Beastmen\u2019s Seals, up to 1100 gil, or an item up to level 55.',
    notes=['A Fields of Valor notorious monster.',
           'Double attacks very frequently, uses Silence, and its petrify is fairly potent.'],
))

# Scowlenkos: its stored grid RESISTED Light at -25%; its own page says Weak against: Light.
# The mob page wins, so Light moves from `st` into `wk`. Dark stays resisted, which the page agrees with.
sc = fold('scowlenkos', 'Ahriman', dict(
    job='Black Mage', crys='Dark', resp=300,
    wk=[['Light', None]],
    st=[e for e in M['scowlenkos']['st'] if e[0] != 'Light'],
    zones=[['Uleguerand Range', '86-87']],
    spawn='Twenty-seven spawn in Uleguerand Range; five-minute respawn.',
    notes=['Found just north of Jormungand.',
           'Checks as Incredibly Tough++ to a level 75 player.',
           'Its Level 5 Petrify seems to last only 2-30 seconds, and Level Sync will not protect a '
           'level 80 from the Petrification.',
           'Ahriman Tears can be stolen from it.'],
))
assert ['Light', None] in sc['wk'] and not any(e[0] == 'Light' for e in sc['st'])

# ==================================================================== DELETES
ASKED = ['mareyamad', 'momowa', 'nareema', 'nyumomo', 'odzmanouk', 'oggbi', 'papako', 'popochu',
         'pya', 'rahdjab', 'rhushouf', 'rongo-nango', 'salimuhl']
print('\n=== DELETE GUARD (rule 389) ===')
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

print('\n=== CROSS-REFERENCES FROM SURVIVING RECORDS (word-boundary, rule 413) ===')
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
zi = {norm(z) for z in zn} | {'rala waterways [u]', 'dho gates'}
FOLDED = ['dwende', 'mistdagger', 'mortobello', 'nirgali', 'nutcracker', 'oko', 'onibi',
          'pixiebane', 'qudeen', 'raubahn', 'razfahd', 'saizo', 'salyhaar', 'satyral', 'scowlenkos']
for k in FOLDED:
    for z in (M[k].get('zones') or []):
        assert norm(z[0] if isinstance(z, list) else z) in zi, (k, z)

GOOD = {'Physical', 'Magical', 'Breath', 'Slashing', 'Blunt', 'Impact', 'H2H', 'Piercing', 'Ranged',
        'Fire', 'Wind', 'Lightning', 'Light', 'Ice', 'Earth', 'Water', 'Dark', 'Varies'}
bogus = collections.Counter()
for k, v in M.items():
    for e in (v.get('wk') or []) + (v.get('st') or []):
        if e[0] not in GOOD:
            bogus[e[0]] += 1
print('\nNON-STANDARD resist-grid labels still in the file: %d entries across %d labels' % (
    sum(bogus.values()), len(bogus)))
print(' ', dict(bogus))

json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('\nmobs %d | abilities %d | bucket %d' % (
    len(M), len(AB), sum(1 for v in M.values() if not v.get('fam'))))
