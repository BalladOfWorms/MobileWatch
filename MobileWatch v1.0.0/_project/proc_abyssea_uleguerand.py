#!/usr/bin/env python3
"""Abyssea-Uleguerand roster correction + drop fills + pop chains (rev 263). USER: "last abyssea zone"

THE NINTH AND FINAL ZONE. Every rev-260/261 prediction held: no Bastion block, Battle trophies missing
across the board, a trivial one-feeder zone boss beside two three-level side-chains, a forking demilune
chain, and a ninth unused colour that also matches the zone's NM abyssites.
"""
import json, re, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']
ZI = json.load(open('app/src/main/assets/zoneinfo.json', encoding='utf-8'))['abyssea_uleguerand']
ZONE = 'Abyssea-Uleguerand'
BAND = '85-100'
TRADE = "Trade it to the ??? and the NM appears."
ORD = "drops from the zone's ordinary monsters."

NMS = {
    'anemic aloysius': ["Whiteworm Clay " + ORD + " " + TRADE + " (K-7/8)"],
    'apademak': ["THREE LEVELS DEEP — the longest pop path in Uleguerand.",
                 "Torn khimaira wing — Dhorme Khimaira, itself a three-item trade at (F-6).",
                 "Dhorme Khimaira needs a Snow God Core off Upas-Kamuy (trade a Gelid Arm at G-5/6), a Sisyphus Fragment off Sisyphus (timed, F/G-6), and a High-quality Marid Hide off ordinary monsters.",
                 "With the wing, examine the ??? at (F-6) — the same square Dhorme Khimaira pops on."],
    'audumbla': ["High-quality Buffalo Horn " + ORD + " " + TRADE + " (J-10)",
                 "Feeds Yaguarogui — Audumbla drops the Audumbla Hide, one of its two trade items."],
    'awahondo': ["Timed pop — no items needed. It reappears every 10-15 minutes around (K-6)/(K-7), north-west of Veridical Conflux #5.",
                 "Feeds Resheph — Awahondo drops the Decaying diremite fang, the zone boss's only pop item."],
    'blanga': ["A two-item trade, one of which comes off another NM.",
               "Rimed Wing — Chillwing Hwitti (trade an Imp Sentry's Horn at E-9).",
               "Benumbed Eye — " + ORD + " (the Benumbed Vodoriga).",
               "Trade both to the ??? at (D-8)."],
    'chillwing hwitti': ["Imp Sentry's Horn " + ORD + " " + TRADE + " (E-9)",
                         "Feeds Blanga — Chillwing Hwitti drops the Rimed Wing, one of its two trade items."],
    'dhorme khimaira': ["A three-item trade, two of them off other NMs — and it is itself Apademak's only pop item.",
                        "Snow God Core — Upas-Kamuy (trade a Gelid Arm at G-5/6).",
                        "Sisyphus Fragment — Sisyphus, a timed pop around (F/G-6).",
                        "High-quality Marid Hide — " + ORD,
                        "Trade all three to the ??? at (F-6).",
                        "Feeds Apademak — Dhorme Khimaira drops the Torn khimaira wing."],
    'empousa': ["Timed pop — no items needed. It reappears every 10-15 minutes around (D/E-8/9)."],
    'impervious chariot': ["Timed pop — no items needed. It reappears every 10-15 minutes around (F-8/9).",
                           "Feeds Pantokrator — it drops the Dented chariot shield, one of its two pop items.",
                           "One of the zone's three abyssite drops — the Vermillion abyssite of kismet."],
    'indrik': ["Timed pop — no items needed. It reappears every 10-15 minutes around (J-10/11)."],
    'ironclad triturator': ["A two-item trade, one of which comes off another NM.",
                            "Bevel Gear — Koghatu (trade a Helical Gear at G-8).",
                            "Gear Fluid — " + ORD,
                            "Trade both to the ??? at (H-8).",
                            "Feeds Pantokrator — the Triturator drops the Warped iron giant nail, one of its two pop items."],
    'isgebind': ["A one-NM chain.",
                 "Begrimed dragon hide — Kur, a timed pop at (I-5).",
                 "With the hide, examine the ??? at (I-5) — Kur's own square."],
    'koghatu': ["Helical Gear " + ORD + " " + TRADE + " (G-8)",
                "Feeds Ironclad Triturator — Koghatu drops the Bevel Gear, and the Triturator in turn feeds Pantokrator."],
    'kur': ["Timed pop — no items needed. It reappears every 10-15 minutes at (I-5).",
            "Feeds Isgebind — Kur drops the Begrimed dragon hide that spawns it."],
    'pantokrator': ["THREE LEVELS DEEP, alongside Apademak.",
                    "Warped iron giant nail — Ironclad Triturator, itself a two-item trade at (H-8) needing a Bevel Gear off Koghatu (trade a Helical Gear at G-8) and a Gear Fluid off ordinary monsters.",
                    "Dented chariot shield — Impervious Chariot, a timed pop around (F-8/9).",
                    "With both, examine the ??? at (G-7)."],
    'refitted chariot': ["Timed pop — no items needed. It reappears every 10-15 minutes around (F/G-9).",
                         "The zone's other Chariot, and the one outside the chain — the Impervious feeds Pantokrator, the Refitted feeds nothing."],
    'resheph': ["The Uleguerand zone boss, and a single feeder — the third Heroes-tier boss in a row to cost exactly one step.",
                "Decaying diremite fang — Awahondo, a timed pop around (K-6)/(K-7), north-west of Veridical Conflux #5.",
                "With the fang, examine the ??? at (K-7).",
                "Apademak and Pantokrator are both three levels deep — harder to reach than the zone boss."],
    'sisyphus': ["Timed pop — no items needed. It reappears every 10-15 minutes around (F/G-6).",
                 "Feeds Dhorme Khimaira — Sisyphus drops its Fragment, and the Khimaira in turn feeds Apademak."],
    'upas-kamuy': ["Gelid Arm " + ORD + " " + TRADE + " (G-5/6)",
                   "Feeds Dhorme Khimaira — Upas-Kamuy drops the Snow God Core, and the Khimaira in turn feeds Apademak."],
    'veri selen': ["Ice Wyvern Scale " + ORD + " " + TRADE + " (H-5)",
                   "One of the zone's three abyssite drops — the Vermillion abyssite of guerdon."],
    'yaguarogui': ["A two-item trade, one of which comes off another NM.",
                   "Audumbla Hide — Audumbla (trade a High-quality Buffalo Horn at J-10).",
                   "High-quality Black Tiger Hide — " + ORD,
                   "Trade both to the ??? at (K-11)."],
    'chione': ["Third step of the demilune chain: kill Ice Elemental or Water Elemental for the Colorful demilune abyssite, then rest while holding it.",
               "Drops the Vermillion demilune abyssite, which is what spawns Ogopogo — guaranteed if you hold Rhapsody in Mauve.",
               "One of the zone's three abyssite drops — the Vermillion abyssite of perspicacity."],
    'ogopogo': ["Last step of the demilune chain: Ice Elemental or Water Elemental gives the Colorful abyssite, Chione gives the Vermillion one.",
                "Rest anywhere in the zone holding the Vermillion demilune abyssite."],
}

# Shared game-wide records — tag and zone only, `nm`/`lv`/`spawn` untouched (rev-260 pattern).
ELEMENTALS = {
    'ice elemental': ["In Abyssea-Uleguerand: rest anywhere in the zone holding a Clear demilune abyssite.",
                      "Drops the Colorful demilune abyssite, which is what spawns Chione — guaranteed if you hold Rhapsody in Mauve.",
                      "Uleguerand's demilune chain forks here: the Water Elemental pops the same way and drops the same abyssite."],
    'water elemental': ["In Abyssea-Uleguerand: rest anywhere in the zone holding a Clear demilune abyssite.",
                        "Drops the Colorful demilune abyssite, which is what spawns Chione — guaranteed if you hold Rhapsody in Mauve.",
                        "Uleguerand's demilune chain forks here: the Ice Elemental pops the same way and drops the same abyssite."],
}

ADVERSARIES = ['adasaurus', 'baelfyr', 'benumbed vodoriga', 'bluffalo', 'byrgen', 'crag limule',
               'ectozoon', 'ermit imp', 'floe amoeban', 'frost bomb mk-ii', 'gefyrst', 'hoarmite',
               'iceberg murex', 'mechanical menace', 'olyphant', 'range clionid', 'sierra tiger',
               'snowflake', 'spectator', 'sub-zero gear', 'svelldrake', 'ungeweder', 'verglas golem']
BOSS = 'resheph'
# The only quest-spawned Adversary in nine zones — every other oddball has been "Fished Up".
QUEST = {'frost bomb mk-ii': 'Quest spawn (Frozen Flame Radux), Abyssea-Uleguerand — 3 in the zone'}
NO_BAND = set(QUEST)

SPAWN_FIX = {'upas-kamuy': 'Forced (trade Gelid Arm to ??? at (G-5/6))'}


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


def fill_drops(key):
    have = split_drops(M[key].get('drops') or '')
    seen = {base(x) for x in have}
    add = [it for it in split_drops(zi_drops.get(key, '')) if base(it) not in seen]
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
    set_tag(key, 'NM')
    ensure_zone(key)
    M[key]['farm'] = farm
    fill_drops(key)

for key in ADVERSARIES:
    set_tag(key, 'Adversary')
    ensure_zone(key, None if key in NO_BAND else BAND)
    lv = M[key].get('lv')
    if lv and not (85 <= lv[0] and lv[1] <= 100):
        offband.append((key, lv))
    if key in QUEST and not M[key].get('spawn'):
        M[key]['spawn'] = QUEST[key]

assert not [kk for mm in M.values() for kk, v in mm.items() if v is None]
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

from collections import Counter
c = Counter(t for m in M.values() for t in (m.get('content') or []) if t.startswith('Abyssea: ' + ZONE))
print('was tagged: %d' % len(prev))
print('NMs that had NO tag:', sorted(k for k in list(NMS) + list(ELEMENTALS) if k not in prev))
print('Adversaries that were in the NM bucket:', sorted(k for k in ADVERSARIES if k in prev and M[k].get('nm')))
print('Adversaries that had NO tag:', sorted(k for k in ADVERSARIES if k not in prev))
print('NO Bastion table — 3rd Heroes zone, prediction held. Detector slot = Spectator.')
print('\nspawn strings corrected:')
for k, was, now in fixed:
    print('  %-22s %s\n  %-22s -> %s' % (k, was, '', now))
print('\nrecords whose global lv sits outside the published %s band:' % BAND)
for k, lv in offband:
    print('  %-22s lv=%s' % (k, lv))
print('\ndrops filled in (%d):' % len(filled))
for k, add in filled:
    print('  %-22s + %s' % (k, ', '.join(add)))
print()
for t, n in sorted(c.items()):
    print('  %2d  %s' % (n, t))
