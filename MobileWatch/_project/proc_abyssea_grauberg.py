#!/usr/bin/env python3
"""Abyssea-Grauberg roster correction + drop fills + pop chains (rev 261). USER: "grauberg"

The LAST of the nine Abyssea zones. Second Heroes-tier zone, and it confirms the rev-260 prediction:
no Bastion block in the Adversaries table. It also forks its demilune chain the same way Altepa does.
Air/Dark Elemental are shared game-wide records and get the Altepa treatment: tag and zone only.
"""
import json, re, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']
ZI = json.load(open('app/src/main/assets/zoneinfo.json', encoding='utf-8'))['abyssea_grauberg']
ZONE = 'Abyssea-Grauberg'
BAND = '85-100'
TRADE = "Trade it to the ??? and the NM appears."
ORD = "drops from the zone's ordinary monsters."

NMS = {
    'alfard': ["THREE LEVELS DEEP — the longest pop path in Grauberg.",
               "Venomous hydra fang — Ningishzida, itself a three-item trade at (I/J-7).",
               "Ningishzida needs a Jaculus Wing off Jaculus (timed, I-8/9), a Minaruja Skull off Minaruja (trade a Pursuer's Wing at I-10), and a High-quality Wivre Hide off ordinary monsters.",
               "With the fang, examine the ??? at (I/J-8)."],
    'amphitrite': ["The Grauberg zone boss, and a single feeder — the same one-step pop as Altepa's Bennu.",
                   "Variegated uragnite shell — Melo Melo, a timed pop among the Glen Crabs around (F/G-11), north of Veridical Conflux #4.",
                   "With the shell, examine the ??? at (F-10).",
                   "Alfard and Raja are both three levels deep — harder to reach than the zone boss."],
    'assailer chariot': ["Timed pop — no items needed. It reappears every 10-15 minutes at (K-7).",
                         "Feeds Raja — it drops the Warped chariot plate, one of its two pop items.",
                         "One of the zone's three abyssite drops — the Indigo abyssite of sojourn."],
    'azdaja': ["A one-NM chain.",
               "Vacant bugard eye — Deelgeed, a timed pop around (F-9/10).",
               "With the eye, examine the ??? at (C-8)."],
    'bomblix flamefinger': ["A two-item trade, one of which comes off another NM.",
                            "Goblin Gunpowder — Burstrox Powderpate (trade a Goblin Rope at I/J-12).",
                            "Goblin Oil — " + ORD,
                            "Trade both to the ??? at (J/K-11)."],
    'burstrox powderpate': ["Goblin Rope " + ORD + " " + TRADE + " (I/J-12)",
                            "Feeds Bomblix Flamefinger — Burstrox drops the Goblin Gunpowder, one of its two trade items."],
    'deelgeed': ["Timed pop — no items needed. It reappears every 10-15 minutes around (F-9/10).",
                 "Feeds Azdaja — Deelgeed drops the Vacant bugard eye that spawns it."],
    'fleshflayer killakriq': ["Timed pop — no items needed. It reappears every 10-15 minutes around (J-11/12)."],
    'fuath': ["Timed pop — no items needed. It reappears every 10-15 minutes around (F/G-5/6)."],
    'ika-roa': ["High-quality Pugil Scale " + ORD + " " + TRADE + " (H-10)"],
    'ironclad sunderer': ["A two-item trade, one of which comes off another NM.",
                          "Teekesselchen Fragment — Teekesselchen (trade a Bubbling Oil at I-5).",
                          "Darkflame Arm — " + ORD,
                          "Trade both to the ??? at (J-6).",
                          "Feeds Raja — the Sunderer drops the Shattered iron giant chain, one of its two pop items."],
    'jaculus': ["Timed pop — no items needed. It reappears every 10-15 minutes around (I-8/9).",
                "Feeds Ningishzida — Jaculus drops the Jaculus Wing, and Ningishzida in turn feeds Alfard."],
    'lorelei': ["Fay Teardrop " + ORD + " " + TRADE + " (F-6)",
                "Feeds Teugghia — Lorelei drops the Naiad's Lock, one of its two trade items."],
    'melo melo': ["Timed pop — no items needed. It reappears every 10-15 minutes among the Glen Crabs around (F/G-11), north of Veridical Conflux #4.",
                  "Feeds Amphitrite — Melo Melo drops the Variegated uragnite shell, the zone boss's only pop item."],
    'minaruja': ["Pursuer's Wing " + ORD + " " + TRADE + " (I-10)",
                 "Feeds Ningishzida — Minaruja drops the Minaruja Skull, and Ningishzida in turn feeds Alfard."],
    'ningishzida': ["A three-item trade, two of them off other NMs — and it is itself Alfard's only pop item.",
                    "Jaculus Wing — Jaculus, a timed pop around (I-8/9).",
                    "Minaruja Skull — Minaruja (trade a Pursuer's Wing at I-10).",
                    "High-quality Wivre Hide — " + ORD,
                    "Trade all three to the ??? at (I/J-7).",
                    "Feeds Alfard — Ningishzida drops the Venomous hydra fang."],
    'raja': ["THREE LEVELS DEEP, alongside Alfard.",
             "Shattered iron giant chain — Ironclad Sunderer, itself a two-item trade at (J-6) needing a Teekesselchen Fragment off Teekesselchen (trade a Bubbling Oil at I-5) and a Darkflame Arm off ordinary monsters.",
             "Warped chariot plate — Assailer Chariot, a timed pop at (K-7).",
             "With both, examine the ??? at (J-5)."],
    'rencounter chariot': ["Timed pop — no items needed. It reappears every 10-15 minutes at (L-5).",
                           "The zone's other Chariot, and the one outside the chain — the Assailer feeds Raja, the Rencounter feeds nothing."],
    'teekesselchen': ["Bubbling Oil " + ORD + " " + TRADE + " (I-5)",
                      "Feeds Ironclad Sunderer — Teekesselchen drops its Fragment, and the Sunderer in turn feeds Raja."],
    'teugghia': ["A two-item trade, one of which comes off another NM.",
                 "Naiad's Lock — Lorelei (trade a Fay Teardrop at F-6).",
                 "Unseelie Eye — " + ORD + " (the Unseelie).",
                 "Trade both to the ??? at (G-5)."],
    'xibalba': ["Decaying Molar " + ORD + " " + TRADE + " (D-8)",
                "One of the zone's three abyssite drops — the Indigo abyssite of merit."],
    'gamayun': ["Third step of the demilune chain: kill Air Elemental or Dark Elemental for the Colorful demilune abyssite, then rest while holding it.",
                "Drops the Indigo demilune abyssite, which is what spawns Maere — guaranteed if you hold Rhapsody in Mauve.",
                "One of the zone's three abyssite drops — the Indigo abyssite of the reaper."],
    'maere': ["Last step of the demilune chain: Air Elemental or Dark Elemental gives the Colorful abyssite, Gamayun gives the Indigo one.",
              "Rest anywhere in the zone holding the Indigo demilune abyssite."],
}

# Shared game-wide records — tag and zone only, `nm`/`lv`/`spawn` untouched (rev-260 pattern).
ELEMENTALS = {
    'air elemental': ["In Abyssea-Grauberg: rest anywhere in the zone holding a Clear demilune abyssite.",
                      "Drops the Colorful demilune abyssite, which is what spawns Gamayun — guaranteed if you hold Rhapsody in Mauve.",
                      "Grauberg's demilune chain forks here: the Dark Elemental pops the same way and drops the same abyssite."],
    'dark elemental': ["In Abyssea-Grauberg: rest anywhere in the zone holding a Clear demilune abyssite.",
                       "Drops the Colorful demilune abyssite, which is what spawns Gamayun — guaranteed if you hold Rhapsody in Mauve.",
                       "Grauberg's demilune chain forks here: the Air Elemental pops the same way and drops the same abyssite."],
}

ADVERSARIES = ['baelfyr', 'byrgen', 'deimobugard', 'faunus wyvern', 'frog prince', 'gefyrst',
               'glade wivre', 'glen crab', 'goblin meatgrinder', 'goblin plunderer', 'hillock murex',
               'knoll clionid', 'monitor', 'peak pugil', 'pond amoeban', 'putrid peapuk', 'seelie',
               'sensenmann', 'sinister seidel', 'spring pugil', 'stream limule', 'stygian djinn',
               'ungeweder', 'unseelie', 'vale crab']
BOSS = 'amphitrite'
FISHED = {'frog prince': 'Fished up (Abyssea-Grauberg, 4 in the zone)',
          'vale crab': 'Fished up (Abyssea-Grauberg, 3 in the zone)'}
COLLISION = ['spring pugil']       # record carries a level 16-52 band, not the 85-100 Grauberg one
NO_BAND = set(COLLISION) | set(FISHED)


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
filled, offband = [], []


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
    if key in FISHED and not M[key].get('spawn'):
        M[key]['spawn'] = FISHED[key]

assert not [kk for mm in M.values() for kk, v in mm.items() if v is None]
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

from collections import Counter
c = Counter(t for m in M.values() for t in (m.get('content') or []) if t.startswith('Abyssea: ' + ZONE))
print('was tagged: %d' % len(prev))
print('NMs that had NO tag:', sorted(k for k in list(NMS) + list(ELEMENTALS) if k not in prev))
print('Adversaries that were in the NM bucket:', sorted(k for k in ADVERSARIES if k in prev and M[k].get('nm')))
print('Adversaries that had NO tag:', sorted(k for k in ADVERSARIES if k not in prev))
print('NO Bastion table in this zone — rev-260 prediction CONFIRMED. Detector role filled by Monitor, not Surveyor.')
print('\nrecords whose global lv sits outside the published %s band:' % BAND)
for k, lv in offband:
    print('  %-22s lv=%s' % (k, lv))
print('\ndrops filled in (%d):' % len(filled))
for k, add in filled:
    print('  %-22s + %s' % (k, ', '.join(add)))
print()
for t, n in sorted(c.items()):
    print('  %2d  %s' % (n, t))
