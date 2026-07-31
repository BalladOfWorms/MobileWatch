#!/usr/bin/env python3
"""Abyssea-Misareaux roster correction + drop fills + pop chains (rev 258). USER: "misareux next"

Fifth zone through the rev-254 pass. Source: BG-wiki Abyssea-Misareaux NM + Adversaries tables.
Three things happen here:
  1. roster: 3-segment content tags, Zone Boss / NM / Adversary / Bastion
  2. drops: ten NMs were missing the very key item that makes them worth killing (the pop item
     for the next NM up the chain, or the zone's Sapphire abyssite). Reconciled against the
     zoneinfo row for the same NM, which was authored from the same table with the DB's labels.
  3. farm: a pop path in all 28 NM entries, written from both ends.
"""
import json, re, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
ZP = 'app/src/main/assets/zoneinfo.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']
ZI = json.load(open(ZP, encoding='utf-8'))['abyssea_misareaux']
ZONE = 'Abyssea-Misareaux'
TRADE = "Trade it to the ??? and the NM appears."
ORD = "drops from the zone's ordinary monsters."

NMS = {
    'abyssic cluster': ["Timed pop — no items needed. It reappears every 10-15 minutes at (E-7).",
                        "Feeds Ironclad Pulverizer — Abyssic Cluster drops the Blazing cluster soul, one of its two pop items."],
    'amhuluk': ["A three-NM chain — every feeder is one step away, none of them chain further.",
                "Jagged apkallu beak — Funereal Apkallu (trade Apkallu Down at H-7).",
                "Clipped bird wing — Manohra (trade Avian Remex at H-9).",
                "Bloodied bat fur — Asanbosam, a timed pop at (G-8/9).",
                "With all three, examine the ??? at (G-9)."],
    'asanbosam': ["Timed pop — no items needed. It reappears every 10-15 minutes around (G-8/9).",
                  "Feeds Amhuluk — Asanbosam drops the Bloodied bat fur, one of its three pop items."],
    'athamas': ["Timed pop — no items needed. It reappears every 10-15 minutes at (I-7)."],
    'avalerion': ["Mocking Beak " + ORD + " " + TRADE + " (G-8)"],
    'cep-kamuy': ["Orobon Cheekmeat " + ORD + " " + TRADE + " (F-4/5)",
                  "Feeds Cirein-croin — Cep-Kamuy drops the Glistening orobon liver, one of its two pop items."],
    'cirein-croin': ["The Misareaux zone boss, and a two-NM chain — the shallowest boss in Abyssea so far.",
                     "Glistening orobon liver — Cep-Kamuy (trade Orobon Cheekmeat at F-4/5).",
                     "Doffed Poroggo hat — Heqet, a timed pop at (I-6).",
                     "With both, examine the ??? at (G/H-5)."],
    'flame skimmer': ["Timed pop — no items needed. It reappears every 10-15 minutes around (G-5/6).",
                      "One of the zone's three abyssite drops — the Sapphire abyssite of furtherance."],
    'funereal apkallu': ["Apkallu Down " + ORD + " " + TRADE + " (H-7)",
                         "Feeds Amhuluk — Funereal Apkallu drops the Jagged apkallu beak, one of its three pop items."],
    'gukumatz': ["Timed pop — no items needed. It reappears every 10-15 minutes at (J-11).",
                 "Feeds Sobek — Gukumatz drops the Molted peiste skin, one of its three pop items."],
    'heqet': ["Timed pop — no items needed. It reappears every 10-15 minutes at (I-6).",
              "Feeds Cirein-croin — Heqet drops the Doffed Poroggo hat, one of its two pop items."],
    'ironclad observer': ["Spheroid Plate " + ORD + " " + TRADE + " (F-8)",
                          "Feeds Ironclad Pulverizer — Ironclad Observer drops the Scalding ironclad spike, one of its two pop items."],
    'ironclad pulverizer': ["A two-NM chain, both feeders one step away.",
                            "Scalding ironclad spike — Ironclad Observer (trade a Spheroid Plate at F-8).",
                            "Blazing cluster soul — Abyssic Cluster, a timed pop at (E-7).",
                            "With both, examine the ??? at (F-7/8)."],
    'ironclad severer': ["Timed pop — no items needed. It reappears every 10-15 minutes at (D-6).",
                         "The one Ironclad outside the chain — the Observer feeds the Pulverizer, the Severer feeds nothing."],
    'jala': ["Timed pop — no items needed. It roams the zone across five spawn points, roughly every 20 minutes."],
    'karkatakam': ["The zone's only two-item trade off ordinary monsters: a High-quality Crab Meat and a High-quality Rock Salt, both " + ORD,
                   "Trade both to the ??? at (H/I-5)."],
    'kutharei': ["Timed pop — no items needed. It reappears every 20-60 minutes around (G-10/11), and it tracks by sight."],
    'manohra': ["Avian Remex " + ORD + " " + TRADE + " (H-9)",
                "Feeds Amhuluk — Manohra drops the Clipped bird wing, one of its three pop items."],
    'minax bugard': ["Bewitching Tusk " + ORD + " " + TRADE + " (J/K-11)",
                     "Feeds Sobek — Minax Bugard drops the Bloodstained bugard fang, one of its three pop items."],
    'nehebkau': ["Hardened Raptor Skin " + ORD + " " + TRADE + " (I-11)"],
    'nonno': ["Worm-Eaten Bud " + ORD + " " + TRADE + " (L-12)"],
    'npfundlwa': ["Black Rabbit Tail " + ORD + " " + TRADE + " (J-8)",
                  "One of the zone's three abyssite drops — the Sapphire abyssite of fortune."],
    'sirrush': ["Molt Scraps " + ORD + " " + TRADE + " (I-12)",
                "Feeds Sobek — Sirrush drops the Gnarled lizard nail, one of its three pop items."],
    'sobek': ["A three-NM chain — the mirror of Amhuluk's, down at the south-east end of the zone.",
              "Bloodstained bugard fang — Minax Bugard (trade a Bewitching Tusk at J/K-11).",
              "Gnarled lizard nail — Sirrush (trade Molt Scraps at I-12).",
              "Molted peiste skin — Gukumatz, a timed pop at (J-11).",
              "With all three, examine the ??? at (J-12)."],
    'tuskertrap': ["Spotted Flyfrond " + ORD + " " + TRADE + " (G-4)",
                   "One of the zone's three abyssite drops — the Sapphire abyssite of lenity."],
    "mi'ghrah": ["First step of the demilune chain: rest anywhere in the zone holding a Clear demilune abyssite.",
                 "Drops the Colorful demilune abyssite, which is what spawns Mx'ghrah — guaranteed if you hold Rhapsody in Mauve."],
    "mx'ghrah": ["Second step of the demilune chain: kill Mi'ghrah for the Colorful demilune abyssite, then rest while holding it.",
                 "Drops the Sapphire demilune abyssite, which is what spawns Tristitia — guaranteed if you hold Rhapsody in Mauve."],
    'tristitia': ["Last step of the demilune chain: Mi'ghrah gives the Colorful abyssite, Mx'ghrah gives the Sapphire one.",
                  "Rest anywhere in the zone holding the Sapphire demilune abyssite."],
}

ADVERSARIES = ['abyssobugard', 'ancient orobon', 'atrociraptor', 'boartrap', 'brine crab', 'buzzfly',
               'coastal colibri', 'crabtrap', 'dusk lizard', 'dynamo cluster', 'ephemeral amoeban',
               'ephemeral murex', 'escarp murex', 'frigatebird', 'gasher', 'gore bats', 'limestone hare',
               'maritime peiste', 'observer', 'orapodium', 'overking apkallu', 'protoamoeban',
               'shore spider', 'slasher', 'squib', 'sturdy pyxis']
BASTION = ['custodian', 'decontaminator', 'disassembler', 'earth mover', 'edifier', 'immobilizer',
           'oppressor', 'overseer', 'ravager chariot', 'scrutinizer', 'surveyor', 'vigilant gear',
           'vigilant gears']
BOSS = 'cirein-croin'
FISHED = ['brine crab', 'crabtrap']

# mobs.json spawn strings that disagree with the wiki table (and with our own zoneinfo row,
# which was written from that table). The table wins — a card must not contradict itself.
SPAWN_FIX = {
    'minax bugard': 'Forced (trade a Bewitching Tusk to ??? at (J/K-11)), Abyssea-Misareaux',
    'sirrush': 'Forced (trade Molt Scraps to ??? at (I-12)), Abyssea-Misareaux',
    'cirein-croin': 'Forced (examine ??? at (G/H-5) with Glistening orobon liver and Doffed Poroggo hat)',
    'cep-kamuy': 'Forced (trade Orbn. Cheekmeat to ??? at (F-4/5))',
    'flame skimmer': 'Timed (10-15 min.) around (G-5/6), Abyssea-Misareaux',
}


def split_drops(s):
    """Comma-split that respects parentheses — 'Sobek's Skin (1G, 2C)' is one item."""
    out, buf, depth = [], '', 0
    for ch in s:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if ch == ',' and depth == 0:
            out.append(buf.strip()); buf = ''
        else:
            buf += ch
    if buf.strip():
        out.append(buf.strip())
    return out


def base(name):
    return re.sub(r'\s*\(.*', '', name).strip().lower()


def set_tag(key, role):
    tags = [t for t in (M[key].get('content') or []) if not t.startswith('Abyssea: ' + ZONE)]
    tags.append('Abyssea: %s: %s' % (ZONE, role))
    M[key]['content'] = tags


def ensure_zone(key, band=None):
    zs = M[key].get('zones') or []
    for z in zs:
        if z[0] == ZONE:
            if band and len(z) == 1:
                z.append(band)
            return
    zs.append([ZONE, band] if band else [ZONE])
    M[key]['zones'] = zs


prev = {k for k, v in M.items() if any(t.startswith('Abyssea: ' + ZONE) for t in (v.get('content') or []))}
zi_drops = {r['n'].lower(): r.get('drops') or '' for r in ZI.get('nms', [])}
filled, fixed, missing = [], [], []

for key, farm in NMS.items():
    M[key]['nm'] = True
    set_tag(key, 'Zone Boss' if key == BOSS else 'NM')
    ensure_zone(key)
    M[key]['farm'] = farm
    if key in SPAWN_FIX and M[key].get('spawn') != SPAWN_FIX[key]:
        fixed.append((key, M[key].get('spawn'), SPAWN_FIX[key]))
        M[key]['spawn'] = SPAWN_FIX[key]
    # Reconcile drops against the zoneinfo row: append anything the table lists that the
    # bestiary record is missing, keep every extra the record already has.
    have = split_drops(M[key].get('drops') or '')
    seen = {base(x) for x in have}
    add = [it for it in split_drops(zi_drops.get(key, '')) if base(it) not in seen]
    if add:
        filled.append((key, add))
        M[key]['drops'] = ', '.join(have + add) if have else ', '.join(add)

for key in ADVERSARIES:
    set_tag(key, 'Adversary')
    lv = M[key].get('lv')
    ensure_zone(key, '%d-%d' % (lv[0], lv[1]) if lv else None)
    if key in FISHED and not M[key].get('spawn'):
        M[key]['spawn'] = 'Fished up (Abyssea-Misareaux, 5 in the zone)'

for key in BASTION:
    if key not in M:
        missing.append(key)
        continue
    set_tag(key, 'Bastion')
    ensure_zone(key)

assert not [kk for mm in M.values() for kk, v in mm.items() if v is None]
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

from collections import Counter
c = Counter(t for m in M.values() for t in (m.get('content') or []) if t.startswith('Abyssea: ' + ZONE))
print('was tagged: %d' % len(prev))
print('NMs that had NO tag:', sorted(k for k in NMS if k not in prev))
print('Adversaries that were in the NM bucket:', sorted(k for k in ADVERSARIES if k in prev and M[k].get('nm')))
print('Adversaries that had NO tag:', sorted(k for k in ADVERSARIES if k not in prev))
print('Bastion machines with no record (skipped):', missing or '(none)')
print('\nspawn strings corrected:')
for k, was, now in fixed:
    print('  %-20s %s\n  %-20s -> %s' % (k, was, '', now))
print('\ndrops filled in (%d NMs):' % len(filled))
for k, add in filled:
    print('  %-20s + %s' % (k, ', '.join(add)))
print()
for t, n in sorted(c.items()):
    print('  %2d  %s' % (n, t))
