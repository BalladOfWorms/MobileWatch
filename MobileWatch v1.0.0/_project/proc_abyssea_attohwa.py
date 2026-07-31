#!/usr/bin/env python3
"""Abyssea-Attohwa roster correction + pop chains (rev 257). USER: "attohwa"

Fourth zone through the rev-254 pass. Source: BG-wiki Abyssea-Attohwa NM + Adversaries tables.
Attohwa is the first zone whose Adversaries table also carries the Bastion machines, so they get
their own role rather than being lumped in with the ordinary spawns.
"""
import json, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']
ZONE = 'Abyssea-Attohwa'
TRADE = "Trade it to the ??? and the NM appears."
ORD = "drops from the zone's ordinary monsters."

NMS = {
    'aggressor antlion': ["Timed pop — no items needed. It reappears every 10-15 minutes at (E-7/8)."],
    'amun': ["Timed pop — no items needed. It reappears every 10-15 minutes around (H/I-8/9).",
             "Feeds Ulhuadshi — Amun drops the Shriveled hecteyes stalk, one of its two pop items."],
    'berstuk': ["Extended Eyestalk " + ORD + " " + TRADE + " (G-9)"],
    'blazing eruca': ["Eruca Egg " + ORD + " " + TRADE + " (J-10)",
                      "Feeds Itzpapalotl — Blazing Eruca drops the Bulbous crawler cocoon, one of its three pop items."],
    'drekavac': ["Wailing Rags " + ORD + " " + TRADE + " (G-7)",
                 "Feeds Titlacauan — Drekavac drops the Writhing ghost finger, one of its four pop items."],
    'gaizkin': ["Undying Ooze " + ORD + " " + TRADE + " (H-8/9)",
                "Feeds Titlacauan — Gaizkin drops the Blotched doomed tongue, one of its four pop items."],
    'gieremund': ["Timed pop — no items needed. It reappears every 10-15 minutes at (F-6).",
                  "Feeds Titlacauan — Gieremund drops the Rusted hound collar, one of its four pop items."],
    'granite borer': ["Withered Cocoon " + ORD + " " + TRADE + " (K-10)",
                      "Feeds Itzpapalotl — Granite Borer drops the Venomous wamoura feeler, one of its three pop items."],
    'ironclad cleaver': ["Timed pop — no items needed. It reappears every 10-15 minutes at (G-9)."],
    'itzpapalotl': ["The Attohwa zone boss, and a three-NM chain.",
                    "Venomous wamoura feeler — Granite Borer (trade a Withered Cocoon at K-10).",
                    "Bulbous crawler cocoon — Blazing Eruca (trade an Eruca Egg at J-10).",
                    "Distended chigoe abdomen — Tunga, a timed pop at (K-9/10).",
                    "With all three, examine the ??? at (K-10)."],
    'kampe': ["Gory Pincer " + ORD + " " + TRADE + " (F-10)"],
    'kharon': ["Bone Chips " + ORD + " " + TRADE + " (F-7)",
               "Feeds Titlacauan — Kharon drops the Cracked skeleton clavicle, one of its four pop items."],
    'maahes': ["Coeurl Round " + ORD + " " + TRADE + " (J-9)"],
    'mielikki': ["Great Root " + ORD + " " + TRADE + " (K-8)"],
    'nightshade': ["Withered Bud " + ORD + " " + TRADE + " (K-8)"],
    'pallid percy': ["Blanched Silver " + ORD + " " + TRADE + " (J-7)",
                     "Feeds Ulhuadshi — Pallid Percy drops the Mucid worm segment, one of its two pop items."],
    'smok': ["A one-NM chain: kill Svarbhanu for the Hollow dragon eye, then examine the ??? at (E-9).",
             "Svarbhanu is itself a trade pop — a Cracked Dragonscale to the ??? at (E-9)."],
    'svarbhanu': ["Cracked Dragonscale " + ORD + " " + TRADE + " (E-9)",
                  "Feeds Smok — Svarbhanu drops the Hollow dragon eye that spawns it."],
    'tejas': ["Timed pop across five spawn points, roughly every 20 minutes. It roams the zone."],
    'titlacauan': ["A four-NM chain, all of them trade or timed pops rather than deeper chains.",
                   "Blotched doomed tongue — Gaizkin (trade Undying Ooze at H-8/9).",
                   "Cracked skeleton clavicle — Kharon (trade Bone Chips at F-7).",
                   "Writhing ghost finger — Drekavac (trade Wailing Rags at G-7).",
                   "Rusted hound collar — Gieremund, a timed pop at (F-6).",
                   "With all four, examine the ??? at (F-7)."],
    'tunga': ["Timed pop — no items needed. It reappears every 10-15 minutes around (K-9/10).",
              "Feeds Itzpapalotl — Tunga drops the Distended chigoe abdomen, one of its three pop items."],
    'ulhuadshi': ["A two-NM chain.",
                  "Mucid worm segment — Pallid Percy (trade Blanched Silver at J-7).",
                  "Shriveled hecteyes stalk — Amun, a timed pop around (H/I-8/9).",
                  "With both, examine the ??? at (J-7)."],
    'warbler': ["Timed pop — no items needed. It reappears every 10-15 minutes at (E-7)."],
    'wherwetrice': ["Mangled Cockatrice Skin " + ORD + " " + TRADE + " (I-8)"],
    'whiro': ["Timed pop — no items needed. It reappears every 10-15 minutes around (K-8/9)."],
    'yaanei': ["Time-of-day pop — it appears at 15:00 game time around (J-8/9). No items needed."],
    "at'euvhi": ["First step of the demilune chain: rest anywhere in the zone holding a Clear demilune abyssite.",
                 "Drops the Colorful demilune abyssite, which is what spawns Es'euvhi."],
    "es'euvhi": ["Second step of the demilune chain: kill At'euvhi for the Colorful demilune abyssite, then rest while holding it.",
                 "Drops the Jade demilune abyssite, which is what spawns Lusca."],
    'lusca': ["Last step of the demilune chain: At'euvhi gives the Colorful abyssite, Es'euvhi gives the Jade one.",
              "Rest anywhere in the zone holding the Jade demilune abyssite."],
}

ADVERSARIES = ['amuckatrice', 'chasm coeurl', 'chasm gnat', 'crevice amoeban', 'decayed flesh',
               'defile scorpion', 'entozoon', 'ephemeral amoeban', 'ephemeral murex', 'funnel antlion',
               'gullycampa', 'hannequet', 'ignis eruca', 'inugami', 'murrain chigoe', 'myriadeyes',
               'rift dragon', 'rift treant', 'rock murex', 'schnitter', 'spuk', 'sturdy pyxis',
               'terminus eft', 'treacle slug']
# The Bastion machines share the Adversaries table but are their own thing.
BASTION = ['custodian', 'decontaminator', 'disassembler', 'earth mover', 'edifier', 'immobilizer',
           'oppressor', 'overseer', 'ravager chariot', 'scrutinizer', 'surveyor', 'vigilant gear',
           'vigilant gears']
BOSS = 'itzpapalotl'


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
missing = []

for key, farm in NMS.items():
    M[key]['nm'] = True
    set_tag(key, 'Zone Boss' if key == BOSS else 'NM')
    ensure_zone(key)
    M[key]['farm'] = farm
for key in ADVERSARIES:
    set_tag(key, 'Adversary')
    lv = M[key].get('lv')
    ensure_zone(key, '%d-%d' % (lv[0], lv[1]) if lv else None)
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
print('Adversaries that were in the NM bucket:', sorted(k for k in ADVERSARIES if k in prev))
print('Bastion machines with no record (skipped):', missing or '(none)')
for t, n in sorted(c.items()):
    print('  %2d  %s' % (n, t))
