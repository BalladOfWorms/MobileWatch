#!/usr/bin/env python3
"""rev 385 — the biggest single batch of the orphan pass: 17 folded, 31 deleted.

USER: sixteen panels/blurbs (Boobrie, Contemplator, Gloomscale, Gunther, Hotupuku, Idun, Jackpot,
Kanavid, Ketos, Krinahal, Kumbaba, Kusa, Kutkha, Lacerator, Laila, Mammet-800), a screenshot of the
single-word orphans A-Lutete, and: "Darrcuiln family would be humanoid. boobrie is a smaller version
of the nm, erinys. kanavid is a sea monk. mobs in last screenshot can be completely removed"

POLICY APPLIED UNIFORMLY: the mob's own page wins outright; the family standard FILLS BLANKS ONLY.
A page's Notes-column flags (A / L / S / H / HP / M / T(S) / T(H)) are detection data and beat any
inherited ["Sight","Sound","True Sight"] import stamp (rule 392).
"""
import json, collections, re

P = 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M, AB = d['mobs'], d['abilities']

# ---------------------------------------------------------------- family standards
def standard(fam):
    """Mode of each field across the family. Guarded per rule 386: never return a null or a
    mode held by fewer than max(2, 30% of members)."""
    mem = [v for v in M.values() if v.get('fam') == fam]
    n = len(mem)
    floor = max(2, int(0.3 * n))
    out = {}
    for k in ('crys', 'job', 'det', 'ab'):
        c = collections.Counter(json.dumps(v.get(k), ensure_ascii=False) for v in mem)
        raw, ct = c.most_common(1)[0]
        val = json.loads(raw)
        out[k] = val if (val is not None and ct >= floor) else None
    c = collections.Counter(json.dumps([v.get('wk'), v.get('st')], ensure_ascii=False) for v in mem)
    raw, ct = c.most_common(1)[0]
    wk, st = json.loads(raw)
    out['wk'], out['st'] = ((wk, st) if (wk is not None or st is not None) and ct >= floor
                            else (None, None))
    out['_n'], out['_floor'] = n, floor
    return out

STD = {}

def fold(key, fam, page=None, kit_add=(), clear=(), fill=('crys', 'job', 'det', 'wk', 'st', 'ab')):
    """Apply the page data, then fill only the fields the record still lacks from the family."""
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
    print('  %-14s -> %-12s filled %-28s kit %d' % (
        key, fam, ','.join(filled) or '-', len(v.get('ab') or [])))
    return v

print('=== FOLDS ===')

# 1. Boobrie — Amphiptere. The blurb is explicit that the adds cast nothing, so the inherited
#    31-spell list goes. Erinys (parent, same family) is job Warrior and carries NO spells either.
fold('boobrie', 'Amphiptere', dict(
    sp=[],
    det=['Sight', 'Sound', 'Blood', 'Scent'],          # family is 11/11 on this, incl. Blood
    job='Warrior',                                     # matches Erinys, its parent
    spawn='Five accompany Erinys from the start of the Geas Fete fight at Reisenjima.',
    notes=['An add in the high-tier Geas Fete fight against Erinys, who is spawned at any ??? in '
           'Reisenjima with an Erinys\u2019s Beak and Tribulens.',
           'Five Boobrie accompany Erinys the moment the fight starts.',
           'They cast no spells at all.',
           'Left alive they build up over time and generate Reaving Wind, granting themselves '
           'Regain and knockback \u2014 heavy pressure across the whole battlefield.'],
), kit_add=['Reaving Wind'])

# 2. Contemplator — Thinker. Notes column "A, T(S)".
fold('contemplator', 'Thinker', dict(
    det=['True Sight'], nm=True, zones=[['Spire of Vahzl']],
    spawn='One spawn in the Spire of Vahzl.',
    notes=['Appears in the ENM Pulling the Plug.', 'Roughly 1,500 HP.'],
))

# 3. Gloomscale — Zilant (user's blurb: "Target Type: Zilant"). Zone and most notes were already
#    on the record from an earlier pass; only the Bio-aura mechanic is new.
g = fold('gloomscale', 'Zilant')
g['notes'].insert(2, 'Gains a Bio aura once Gloomtalon \u2014 a Gallu fought alongside it \u2014 is defeated.')

# 4. Gunther — Humanoid. "T(H), L" and NO "A": the page says outright that neither he nor the
#    Crimson Grimoire aggroes, so the aggressive flag comes OFF.
gu = fold('gunther', 'Humanoid', dict(
    job='Scholar', nm=True, lnk=True, det=['True Sound'],
    zones=[['Throne Room', '70']],
    spawn='One spawn in the Throne Room for the Survival of the Wisest battlefield.',
    ab=['Tabula Rasa'],
    sp=['Regen', 'Protect IV', 'Shell III'],
    notes=['Fought during the Survival of the Wisest battlefield event, the Scholar limit break.',
           'Fights alongside and links with the Crimson Grimoire, but neither of them aggroes.',
           'Casts Regen, Protect IV and Shell III on himself and on the Crimson Grimoire before '
           'being attacked.',
           'Uses Tabula Rasa.'],
), clear=('agg',))
assert 'agg' not in gu

# 5. Hotupuku — Bugard. Own Ice weakness kept; page gives no magnitudes and no Strong-to line.
fold('hotupuku', 'Bugard', dict(
    job='Warrior / Monk / Paladin', nm=True, det=['True Sound'],
    zones=[['Monarch Linn']],
    spawn='One spawn in Monarch Linn.',
    notes=['Appears in the ENM Bugard in the Clouds.',
           'Can use two-hour abilities \u2014 Mighty Strikes, Hundred Fists and Invincible have all '
           'been seen. It can use more than one two-hour in a fight, but never the same one twice.'],
), kit_add=['Mighty Strikes', 'Hundred Fists', 'Invincible'])

# 6. Idun — Ghost. Its stored grid already matches the page (weak Fire/Light, strong Dark/Ice).
fold('idun', 'Ghost', dict(
    job='Black Mage', nm=True, det=['True Sound', 'Blood'],
    zones=[["Brunhilde's Chamber"], ["Gerhilde's Chamber"], ["Ortlinde's Chamber"]],
    spawn='Twelve spawn in each of Brunhilde\u2019s, Gerhilde\u2019s and Ortlinde\u2019s Chamber.',
    drops="Hero's Reflections",
    notes=['A possible encounter in the Einherjar Wing III chambers.'],
))

# 7. Jackpot — Magic Pot. Page says Crystal: None, so the family's unanimous Light is NOT stamped.
fold('jackpot', 'Magic Pot', dict(
    job='Black Mage / Red Mage', nm=True, det=['Magic'],
    zones=[['RoMaeve']],
    spawn='Spawned from the Field Parchment at N-10 with the Chapter 6 Elite Training page, by '
          'trading 28 Beastmen\u2019s Seals, up to 1400 gil, or an item up to level 70.',
    sp=['Enfire II', 'Blaze Spikes', 'Thunder III', 'Aeroga III', 'Burn', 'Horde Lullaby'],
    notes=['A Fields of Valor notorious monster.',
           'May spawn with En-Paralyze, with En-Curse, or with very low defense.',
           'Drains both TP and MP, and appears able to switch between the two at will.'],
), fill=('job', 'det', 'wk', 'st', 'ab'))          # crys deliberately excluded

# 8. Kanavid — Sea Monk (user ruling). Zone/content/notes already present.
fold('kanavid', 'Sea Monk')

# 9. Ketos — Pugil. Page's Job field says White Mage but its own notes doubt it.
fold('ketos', 'Pugil', dict(
    job='White Mage', crys='Water', nm=True,
    zones=[['Buburimu Peninsula']],
    spawn='One spawn in Buburimu Peninsula.',
    notes=['A Fields of Valor notorious monster, roughly 500 HP.',
           'Additional effect on its melee attacks: Blizzard, Poison and Wind damage.',
           'Fields of Valor notorious monsters can be spawned with a random job, so the listed '
           'job is not reliable \u2014 this one shows no sign of being a White Mage.'],
))

# 10. Krinahal — Humanoid. No NM banner on the page, so no nm flag.
fold('krinahal', 'Humanoid', dict(
    job='Blue Mage', det=['True Sound'],
    zones=[['Leujaoam Sanctum']],
    spawn='One spawn in Leujaoam Sanctum.',
    notes=['Fought for Red Versus Blue.'],
))

# 11. Kumbaba — Treant.
fold('kumbaba', 'Treant', dict(
    nm=True, zones=[['Jugner Forest']],
    spawn='One spawn in Jugner Forest.',
    notes=['A Fields of Valor notorious monster, roughly 500 HP.',
           'May spawn with an en-effect \u2014 Enblizzard or Enthunder have both been seen.',
           'May spawn with shadows.'],
))

# 12. Kusa — Humanoid. 15 spawns, not an NM.
fold('kusa', 'Humanoid', dict(
    job='Ninja', det=['True Sight', 'Blood'],
    zones=[['Leujaoam Sanctum', '76-77']],
    spawn='Fifteen spawn throughout the cavern during Imperial Code.',
    notes=['Found throughout the cavern in Imperial Code.',
           'Links with the three target notorious monsters Danzo, Oko and Saizo.',
           'Casts Ninjutsu and uses katana weapon skills.'],
))

# 13. Kutkha — Lesser Bird, matching the user's ruling on its own add `kutkha's get`.
fold('kutkha', 'Lesser Bird', dict(
    nm=True, det=['True Sight'],
    zones=[['Balgas Dais']],
    spawn='One spawn in Balgas Dais for the KCNM The V Formation.',
    notes=['Appears in the KCNM The V Formation, assisted by six Kutkha\u2019s Get.',
           'During a three-day-only campaign it dropped Monarch Beetle Saliva, a Bonanza Kupon S, '
           'Flare, Indi-Malaise, a Saffron Blossom, a Wieldance Card and a Voyage Stone.'],
))

# 14. Lacerator — Crab. Page drops are all crafting mats, so none are stored (convention).
fold('lacerator', 'Crab', dict(
    job='Paladin', crys='Water', resp=300,
    zones=[['Korroloka Tunnel', '87-91']],
    spawn='Eighteen spawn on the 5th map of Korroloka Tunnel; five-minute respawn.',
    notes=['Found on the 5th map of Korroloka Tunnel.', '6,800-7,100 HP.'],
))

# 15. Laila — Humanoid.
fold('laila', 'Humanoid', dict(
    job='Dancer', nm=True, zones=[['QuBia Arena']],
    spawn='One spawn in QuBia Arena.',
    notes=['Fought during the A Furious Finale battlefield event, the Dancer limit break.'],
))

# 16. Mammet-800 — Mammets. The family det is 5/5 ["Sound","Magic"] and the record carried the
#     known bad ["Sight","Sound","True Sight"] stamp, so rule 392 applies.
fold('mammet-800', 'Mammets', dict(
    nm=True, det=['Sound', 'Magic'], agg=True, lnk=True,
    zones=[['Monarch Linn']],
    drops='Yellow Liquid',
    spawn='One spawn in Monarch Linn for the quest Uninvited Guests.',
    notes=['Spawns for the quest Uninvited Guests.', 'Yellow Liquid drops every time.'],
))

# 17. Darrcuiln — Humanoid (user ruling). Everything else on the record stays.
fold('darrcuiln', 'Humanoid')

# ==================================================================== DELETES
ASKED = ['azima', 'azo', 'bartholomaus', 'bravo', 'bryher', 'camlin', 'dalzakk', 'darach',
         'darkness', 'degenhard', 'dhiadjhar', 'duskraven', 'dwende', 'else', 'excaliace',
         'ganmuul', 'gariri', 'gasharyad', 'ghahnis', 'jajaro', 'jalyaat', 'jasweem', 'kagetora',
         'karababa', 'karazahm', 'kilhwch', 'kurt', 'kyo', 'lerren', 'lewenhart', 'ludwig',
         'lutete']
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
print('  NM-flagged among the targets (named in the reply so they can come back): %s'
      % [k for k in targets if M[k].get('nm')])

print('\n=== CROSS-REFERENCES FROM SURVIVING RECORDS ===')
disp = {k: M[k]['n'] for k in targets}
hits = 0
for mk, mv in M.items():
    if mk in targets:
        continue
    blob = json.dumps(mv, ensure_ascii=False)
    for k, name in disp.items():
        if re.search(r'(?<![\w\'-])%s(?![\w\'-])' % re.escape(name), blob):
            print('  %-26s mentions %s' % (mk, name)); hits += 1
if not hits:
    print('  (none)')
for k in targets:
    del M[k]
print('  deleted %d of %d asked' % (len(targets), len(ASKED)))

# ==================================================================== GUARDS
bad = [(k, f) for k, mm in M.items() for f, val in mm.items() if val is None]
assert not bad, bad[:10]
zn = {x['name'] for x in json.load(open('app/src/main/assets/zones.json', encoding='utf-8'))['zones']}
FREE = {"brunhildes chamber", "gerhildes chamber", "ortlindes chamber"}   # Einherjar, not in zones.json
def norm(s): return s.replace('\u2019', "'").replace("'", '').lower()
zi = {norm(z) for z in zn} | FREE
FOLDED = ['boobrie', 'contemplator', 'gloomscale', 'gunther', 'hotupuku', 'idun', 'jackpot',
          'kanavid', 'ketos', 'krinahal', 'kumbaba', 'kusa', 'kutkha', 'lacerator', 'laila',
          'mammet-800', 'darrcuiln']
# free-text zones that legitimately are not in zones.json (U-zones / Einherjar chambers)
zi |= {'rala waterways [u]', 'walk of echoes', 'sea serpent grotto'}
for k in FOLDED:
    for z in (M[k].get('zones') or []):
        assert norm(z[0] if isinstance(z, list) else z) in zi, (k, z)
items = json.load(open('app/src/main/assets/ffxi_items.json', encoding='utf-8'))
inames = {v['n'] for v in items.values()}
for k in FOLDED:
    for dr in (M[k].get('drops') or '').split(', '):
        if dr:
            assert dr in inames, (k, dr)

json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)
print('\nmobs %d | abilities %d | bucket %d' % (
    len(M), len(AB), sum(1 for v in M.values() if not v.get('fam'))))
