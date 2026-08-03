#!/usr/bin/env python3
"""Abyssea-Vunkerl roster correction + drop fills + pop chains (rev 259). USER: "vunkerl"

Sixth zone through the rev-254 pass, and the second to run the rev-258 drop reconciliation
against zoneinfo before writing the farm paths.
"""
import json, re, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']
ZI = json.load(open('app/src/main/assets/zoneinfo.json', encoding='utf-8'))['abyssea_vunkerl']
ZONE = 'Abyssea-Vunkerl'
TRADE = "Trade it to the ??? and the NM appears."
ORD = "drops from the zone's ordinary monsters."

NMS = {
    'armillaria': ["Shockshroom " + ORD + " " + TRADE + " (F-7)",
                   "One of the zone's three abyssite drops — the Crimson abyssite of acumen."],
    'ayravata': ["Timed pop — no items needed. It reappears every 10-15 minutes at (I-8).",
                 "Feeds Karkadann — Ayravata drops the Malodorous marid fur, one of its two pop items."],
    'bukhis': ["A three-NM chain, and one of the two NMs in this zone that take more feeders than the zone boss does.",
               "Ingrown taurus nail — Khalkotaur (trade a Gnarled Taurus Horn at H-10).",
               "Ossified gargouille hand — Quasimodo (trade a Gargouille Stone at F/G-11).",
               "Imbrued vampyr fang — Lord Varney, a lottery pop off the Slough Bats around (G-10)/(H-10).",
               "With all three, examine the ??? at (G-10)."],
    'chhir batti': ["Djinn Ashes " + ORD + " " + TRADE + " (F-6)"],
    'div-e sepid': ["Timed pop — no items needed. It reappears every 10-15 minutes at (E-11).",
                    "Feeds Durinn — Div-e Sepid drops the Chipped imp's olifant, one of its three pop items."],
    'durinn': ["A three-NM chain, the mirror of Bukhis's — both take three feeders where the zone boss takes two.",
               "Decayed dvergr tooth — Dvalinn (trade a Dented Skull at D-11).",
               "Pulsating soulflayer beard — Kadraeth the Hatespawn (trade a Stiffened Tentacle at E-10).",
               "Chipped imp's olifant — Div-e Sepid, a timed pop at (E-11).",
               "With all three, examine the ??? at (E-12)."],
    'dvalinn': ["Dented Skull " + ORD + " " + TRADE + " (D-11)",
                "Feeds Durinn — Dvalinn drops the Decayed dvergr tooth, one of its three pop items."],
    'fulmotondro': ["Timed pop — no items needed. It roams the zone across five spawn points, roughly every 20 minutes."],
    'gnawtooth gary': ["High-quality Rabbit Hide " + ORD + " " + TRADE + " (F-12)"],
    'hanuman': ["Timed pop — no items needed. It reappears every 10-15 minutes at (H-7)."],
    'hrosshvalur': ["Timed pop — no items needed. It reappears every 10-15 minutes around (J/K-6).",
                    "Feeds Sedna — Hrosshvalur drops the Shimmering pugil scale, one of its two pop items."],
    'iktomi': ["Timed pop — no items needed. It reappears every 10-15 minutes at (I-11).",
               "One of the zone's three abyssite drops — the Crimson abyssite of destiny."],
    'iku-turso': ["Moonbeam Clam " + ORD + " " + TRADE + " (J-7), near Veridical Conflux #3.",
                  "Feeds Sedna — Iku-Turso drops the Glossy sea monk sucker, one of its two pop items."],
    'ironclad executioner': ["Timed pop — no items needed. It reappears every 10-15 minutes around (H/I-8).",
                             "Vunkerl's Ironclad stands alone — it neither needs a chain nor feeds one."],
    'kadraeth the hatespawn': ["Stiffened Tentacle " + ORD + " " + TRADE + " (E-10)",
                               "Feeds Durinn — Kadraeth drops the Pulsating soulflayer beard, one of its three pop items."],
    'karkadann': ["A two-NM chain, both feeders one step away.",
                  "Warped smilodon choker — Rakshas (trade a Black Whisker at G-8).",
                  "Malodorous marid fur — Ayravata, a timed pop at (I-8).",
                  "With both, examine the ??? at (G-7/8)."],
    'khalkotaur': ["Gnarled Taurus Horn " + ORD + " " + TRADE + " (H-10)",
                   "Feeds Bukhis — Khalkotaur drops the Ingrown taurus nail, one of its three pop items."],
    'lord varney': ["Lottery pop off the Slough Bats around (G-10)/(H-10), every 10-15 minutes. No items needed.",
                    "Feeds Bukhis — Lord Varney drops the Imbrued vampyr fang, one of its three pop items."],
    'pascerpot': ["Crawler Floatstone " + ORD + " " + TRADE + " (G-12)",
                  "One of the zone's three abyssite drops — the Crimson abyssite of confluence."],
    'quasimodo': ["Gargouille Stone " + ORD + " " + TRADE + " (F/G-11)",
                  "Feeds Bukhis — Quasimodo drops the Ossified gargouille hand, one of its three pop items."],
    'rakshas': ["Black Whisker " + ORD + " " + TRADE + " (G-8)",
                "Feeds Karkadann — Rakshas drops the Warped smilodon choker, one of its two pop items."],
    'sedna': ["The Vunkerl zone boss, and a two-NM chain — easier to reach than either Bukhis or Durinn, which take three feeders each.",
              "Glossy sea monk sucker — Iku-Turso (trade a Moonbeam Clam at J-7).",
              "Shimmering pugil scale — Hrosshvalur, a timed pop around (J/K-6).",
              "With both, examine the ??? at (K-6), near Veridical Conflux #3."],
    'seps': ["Opaque Wing " + ORD + " " + TRADE + " (G-13)"],
    'sippoy': ["Spawn conditions unrecorded — the NM table lists neither a timer nor a pop item, only the location (E-7).",
               "Treat it as a roam-and-look until someone confirms the trigger."],
    'xan': ["Fortune Wing " + ORD + " " + TRADE + " (I-12)"],
    "vu'zdei": ["First step of the demilune chain: rest anywhere in the zone holding a Clear demilune abyssite.",
                "Drops the Colorful demilune abyssite, which is what spawns Hm'zdei — guaranteed if you hold Rhapsody in Mauve."],
    "hm'zdei": ["Second step of the demilune chain: kill Vu'zdei for the Colorful demilune abyssite, then rest while holding it.",
                "Drops the Crimson demilune abyssite, which is what spawns Ketea — guaranteed if you hold Rhapsody in Mauve."],
    'ketea': ["Last step of the demilune chain: Vu'zdei gives the Colorful abyssite, Hm'zdei gives the Crimson one.",
              "Rest anywhere in the zone holding the Crimson demilune abyssite."],
}

ADVERSARIES = ['aestutaur', 'blademaw pugil', 'clammy imp', 'coccinelle', 'daggertooth pugil', 'devegetator',
               'ephemeral amoeban', 'ephemeral murex', 'gruesome gargouille', 'helter-skelter', 'jasconius',
               'morose marid', 'peapuk', 'pneumaflayer', 'river murex', 'russet rarab', 'scythemaw jagil',
               'shewriwhile', 'slaughterous smilodon', 'slough bats', 'speltercap', 'spitting spider',
               'stream amoeban', 'sturdy pyxis', 'wily opo-opo']
BASTION = ['custodian', 'decontaminator', 'disassembler', 'earth mover', 'edifier', 'immobilizer',
           'oppressor', 'overseer', 'ravager chariot', 'scrutinizer', 'surveyor', 'vigilant gear',
           'vigilant gears']
BOSS = 'sedna'
FISHED = ['daggertooth pugil', 'scythemaw jagil']

SPAWN_FIX = {
    # table widens the square; the file had only half of it
    'hrosshvalur': 'Timed (10-15 min.) (J/K-6)',
    # the file's lottery/placeholder detail beats the table's flat "Timed", so it is kept —
    # only the square is widened to hold both sources' readings
    'lord varney': 'Lottery — (G-10)/(H-10) among the Slough Bats, every 10-15 minutes',
    # the table publishes no trigger at all for this one; say so rather than leaving a bare square
    'sippoy': '(E-7) — spawn conditions unrecorded (the NM table shows neither a timer nor a pop item)',
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
filled, fixed, missing, nolv = [], [], [], []

for key, farm in NMS.items():
    M[key]['nm'] = True
    set_tag(key, 'Zone Boss' if key == BOSS else 'NM')
    ensure_zone(key)
    M[key]['farm'] = farm
    if key in SPAWN_FIX and M[key].get('spawn') != SPAWN_FIX[key]:
        fixed.append((key, M[key].get('spawn'), SPAWN_FIX[key]))
        M[key]['spawn'] = SPAWN_FIX[key]
    have = split_drops(M[key].get('drops') or '')
    seen = {base(x) for x in have}
    add = [it for it in split_drops(zi_drops.get(key, '')) if base(it) not in seen]
    if add:
        filled.append((key, add))
        M[key]['drops'] = ', '.join(have + add) if have else ', '.join(add)

for key in ADVERSARIES:
    set_tag(key, 'Adversary')
    lv = M[key].get('lv')
    if not lv:
        nolv.append(key)
    ensure_zone(key, '%d-%d' % (lv[0], lv[1]) if lv else None)
    if key in FISHED and not M[key].get('spawn'):
        M[key]['spawn'] = 'Fished up (Abyssea-Vunkerl, 5 in the zone)'

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
print('Adversaries with no lv:', nolv or '(none)')
print('Bastion machines with no record (skipped):', missing or '(none)')
print('\nspawn strings corrected:')
for k, was, now in fixed:
    print('  %-22s %s\n  %-22s -> %s' % (k, was, '', now))
print('\ndrops filled in (%d NMs):' % len(filled))
for k, add in filled:
    print('  %-22s + %s' % (k, ', '.join(add)))
print()
for t, n in sorted(c.items()):
    print('  %2d  %s' % (n, t))
