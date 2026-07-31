#!/usr/bin/env python3
"""Abyssea-Altepa roster correction + drop fills + pop chains (rev 260). USER: "altep"

Seventh zone through the rev-254 pass. Altepa is the first HEROES-tier zone in this sweep and it
breaks two habits: there are NO Bastion machines in its Adversaries table (Surveyor appears there
as an ordinary spawn instead), and its demilune chain FORKS — Earth Elemental and Fire Elemental
both pop off the Clear abyssite and both drop the Colorful one.

Two records are handled with care rather than force:
  * earth/fire elemental are the ORDINARY game-wide elemental records. They get the Altepa content
    tag and zone so the screen lists them, but their `nm`, `lv` and `spawn` are left alone — the
    demilune pop is written into `farm` with an explicit "In Abyssea-Altepa:" prefix instead.
  * sand pugil is a NAME COLLISION (the record is the level 18-20 North Gustaberg pugil). Tagged,
    but no level band written. Flagged for the user.
"""
import json, re, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']
ZI = json.load(open('app/src/main/assets/zoneinfo.json', encoding='utf-8'))['abyssea_altepa']
ZONE = 'Abyssea-Altepa'
BAND = '85-100'          # the Altepa Adversaries table publishes an exact band, not a "~" estimate
TRADE = "Trade it to the ??? and the NM appears."
ORD = "drops from the zone's ordinary monsters."

NMS = {
    'amarok': ["A three-item trade, and two of the three come off other NMs.",
               "High-quality Dhalmel Hide — " + ORD,
               "Tiger King's Hide — Ansherekh, a timed pop around (F/G-8).",
               "Sharabha Hide — Sharabha (trade a Sand-caked Fang at G-5).",
               "Trade all three to the ??? at (E-6).",
               "Feeds Orthrus — Amarok drops the Steaming cerberus tongue that spawns it."],
    'ansherekh': ["Timed pop — no items needed. It reappears every 10-15 minutes around (F/G-8).",
                  "Feeds Amarok — Ansherekh drops the Tiger King's Hide, one of its three trade items."],
    'battlerigged chariot': ["Timed pop — no items needed. It reappears every 10-15 minutes at (E-10)."],
    'bennu': ["The Altepa zone boss, and the shallowest boss in Abyssea — one feeder, nothing behind it.",
              "Resplendent roc quill — Ouzelum, a timed pop around (I/J-8/9).",
              "With the quill, examine the ??? at (I-8).",
              "Orthrus and Rani are both three levels deep — harder to reach than the zone boss."],
    'brulo': ["Last step of the demilune chain: Earth Elemental or Fire Elemental gives the Colorful abyssite, Koios gives the Emerald one.",
              "Rest anywhere in the zone holding the Emerald demilune abyssite."],
    'bugul noz': ["Sabulous Clay " + ORD + " " + TRADE + " (E-10), at the north-east corner of the square.",
                  "Feeds Emperador de Altepa — Bugul Noz drops the Oasis Water, one of its two trade items."],
    'chickcharney': ["High-quality Cockatrice Skin " + ORD + " " + TRADE + " (I-9)"],
    'cuijatender': ["Timed pop — no items needed. It reappears every 10-20 minutes around the oasis at (E-9), near Veridical Conflux #6."],
    'dragua': ["A one-NM chain.",
               "Bloodied dragon ear — Hazhdiha, a timed pop at (H-10).",
               "With the ear, examine the ??? at (G-9)."],
    'emperador de altepa': ["A two-item trade, one of which comes off another NM.",
                            "Oasis Water — Bugul Noz (trade Sabulous Clay at E-10).",
                            "Giant Mistletoe — " + ORD,
                            "Trade both to the ??? at (F-11)."],
    'hazhdiha': ["Timed pop — no items needed. It reappears every 10-15 minutes at (H-10).",
                 "Feeds Dragua — Hazhdiha drops the Bloodied dragon ear that spawns it."],
    'hedjedjet': ["Timed pop — no items needed. It reappears every 10-15 minutes around (G/H-5/6)."],
    'ironclad smiter': ["A two-item trade, one of which comes off another NM.",
                        "Tablilla Mercury — Tablilla (trade a Sandy Shard at C-11).",
                        "Smoldering Arm — " + ORD,
                        "Trade both to the ??? at (D-12).",
                        "Feeds Rani — the Smiter drops the Broken iron giant spike, one of its two pop items."],
    'koios': ["Third step of the demilune chain: kill Earth Elemental or Fire Elemental for the Colorful demilune abyssite, then rest while holding it.",
              "Drops the Emerald demilune abyssite, which is what spawns Brulo — guaranteed if you hold Rhapsody in Mauve.",
              "One of the zone's three abyssite drops — the Emerald abyssite of acumen."],
    'long-barreled chariot': ["Timed pop — no items needed. It reappears every 10-15 minutes around (D-11/12).",
                              "Feeds Rani — it drops the Rusted chariot gear, one of its two pop items.",
                              "One of the zone's three abyssite drops — the Emerald abyssite of fortune."],
    'orthrus': ["THREE LEVELS DEEP — the longest pop path in Altepa.",
                "Steaming cerberus tongue — Amarok, and Amarok is itself a three-item trade at (E-6).",
                "Amarok needs a High-quality Dhalmel Hide off ordinary monsters, a Tiger King's Hide off Ansherekh (timed, F/G-8), and a Sharabha Hide off Sharabha (trade a Sand-caked Fang at G-5).",
                "With the tongue, examine the ??? at (F-6/7). Three spawn points."],
    'ouzelum': ["Timed pop — no items needed. It reappears every 10-15 minutes around (I/J-8/9).",
                "Feeds Bennu — Ouzelum drops the Resplendent roc quill, the zone boss's only pop item."],
    'rani': ["THREE LEVELS DEEP, alongside Orthrus.",
             "Broken iron giant spike — Ironclad Smiter, itself a two-item trade at (D-12) needing a Tablilla Mercury off Tablilla (trade a Sandy Shard at C-11) and a Smoldering Arm off ordinary monsters.",
             "Rusted chariot gear — Long-Barreled Chariot, a timed pop around (D-11/12).",
             "With both, examine the ??? at (D-10)."],
    'sharabha': ["Sand-caked Fang " + ORD + " " + TRADE + " (G-5)",
                 "Feeds Amarok — Sharabha drops the Sharabha Hide, one of its three trade items."],
    'shaula': ["A two-item trade, one of which comes off another NM.",
               "Vadleany Fluid — Vadleany (trade a Ladybird Leaf at H-6).",
               "High-quality Scorpion Claw — " + ORD,
               "Trade both to the ??? at the north-east corner of (H-5)."],
    'tablilla': ["Sandy Shard " + ORD + " " + TRADE + " (C-11)",
                 "Feeds Ironclad Smiter — Tablilla drops the Tablilla Mercury, and the Smiter in turn feeds Rani."],
    'vadleany': ["Ladybird Leaf " + ORD + " " + TRADE + " (H-6)",
                 "Feeds Shaula — Vadleany drops the Vadleany Fluid, one of its two trade items."],
    'waugyl': ["Puppet's Blood " + ORD + " " + TRADE + " (F-9)",
               "One of the zone's three abyssite drops — the Emerald abyssite of sojourn."],
}

# Shared game-wide records: tag and zone only, never nm/lv/spawn.
ELEMENTALS = {
    'earth elemental': ["In Abyssea-Altepa: rest anywhere in the zone holding a Clear demilune abyssite.",
                        "Drops the Colorful demilune abyssite, which is what spawns Koios — guaranteed if you hold Rhapsody in Mauve.",
                        "Altepa's demilune chain forks here: the Fire Elemental pops the same way and drops the same abyssite."],
    'fire elemental': ["In Abyssea-Altepa: rest anywhere in the zone holding a Clear demilune abyssite.",
                       "Drops the Colorful demilune abyssite, which is what spawns Koios — guaranteed if you hold Rhapsody in Mauve.",
                       "Altepa's demilune chain forks here: the Earth Elemental pops the same way and drops the same abyssite."],
}

ADVERSARIES = ['akrab', 'arid limule', 'badlands crab', 'baelfyr', 'barrens treant', 'bonfire (monster)',
               'byrgen', 'camelopardalis', 'desert clionid', 'desert puk', 'dune cockatrice',
               'dune manticore', 'ergdrake', 'fear dearg', 'gastornis', 'gefyrst', 'manigordo',
               'nannakola', 'oasis amoeban', 'sand murex', 'sand pugil', 'sand sweeper', 'surveyor',
               'ungeweder']
BOSS = 'bennu'
FISHED = {'badlands crab': 'Fished up (Abyssea-Altepa, 5 in the zone)',
          'sand pugil': None}          # name collision — see COLLISION below
COLLISION = ['sand pugil']             # record is the level 18-20 North Gustaberg pugil
NO_BAND = set(COLLISION) | {'badlands crab'}

SPAWN_FIX = {
    # file named the landmark but dropped the square; table has the square. Keep both.
    'cuijatender': 'Timed (every 10-20 minutes) around the Oasis at (E-9), near Conflux #6',
    # file has the extra spawn count; normalise the stray "Abyssea - Altepa" spacing and the square
    'orthrus': 'Forced (examine ??? at (F-6/7) with a Steaming cerberus tongue) — 3 spawns, Abyssea-Altepa',
}


def split_drops(s):
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
filled, fixed, offband = [], [], []


def fill_drops(key, zi_key=None):
    have = split_drops(M[key].get('drops') or '')
    seen = {base(x) for x in have}
    add = [it for it in split_drops(zi_drops.get(zi_key or key, '')) if base(it) not in seen]
    if add:
        filled.append((key, add))
        M[key]['drops'] = ', '.join(have + add) if have else ', '.join(add)


for key, farm in NMS.items():
    M[key]['nm'] = True
    set_tag(key, 'Zone Boss' if key == BOSS else 'NM')
    ensure_zone(key)
    M[key]['farm'] = farm
    if key in SPAWN_FIX and M[key].get('spawn') != SPAWN_FIX[key]:
        fixed.append((key, M[key].get('spawn'), SPAWN_FIX[key]))
        M[key]['spawn'] = SPAWN_FIX[key]
    fill_drops(key)

for key, farm in ELEMENTALS.items():
    set_tag(key, 'NM')            # role for the zone screen only — `nm` flag untouched
    ensure_zone(key)
    M[key]['farm'] = farm
    fill_drops(key)

for key in ADVERSARIES:
    set_tag(key, 'Adversary')
    ensure_zone(key, None if key in NO_BAND else BAND)
    lv = M[key].get('lv')
    if lv and not (85 <= lv[0] and lv[1] <= 100):
        offband.append((key, lv))
    if key in FISHED and FISHED[key] and not M[key].get('spawn'):
        M[key]['spawn'] = FISHED[key]

assert not [kk for mm in M.values() for kk, v in mm.items() if v is None]
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

from collections import Counter
c = Counter(t for m in M.values() for t in (m.get('content') or []) if t.startswith('Abyssea: ' + ZONE))
print('was tagged: %d' % len(prev))
print('NMs that had NO tag:', sorted(k for k in list(NMS) + list(ELEMENTALS) if k not in prev))
print('Adversaries that were in the NM bucket:', sorted(k for k in ADVERSARIES if k in prev and M[k].get('nm')))
print('Adversaries that had NO tag:', sorted(k for k in ADVERSARIES if k not in prev))
print('NO Bastion table in this zone — Surveyor filed as an ordinary Adversary.')
print('\nrecords whose global lv sits outside the published %s band:' % BAND)
for k, lv in offband:
    print('  %-22s lv=%s' % (k, lv))
print('\nspawn strings corrected:')
for k, was, now in fixed:
    print('  %-22s %s\n  %-22s -> %s' % (k, was, '', now))
print('\ndrops filled in (%d):' % len(filled))
for k, add in filled:
    print('  %-22s + %s' % (k, ', '.join(add)))
print()
for t, n in sorted(c.items()):
    print('  %2d  %s' % (n, t))
