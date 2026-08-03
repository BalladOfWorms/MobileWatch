#!/usr/bin/env python3
"""Abyssea-La Theine roster correction + pop chains (rev 255). USER: "la theine"

Same pass as rev-254's Konschtat: correct the roster, split NM from Adversary, and write the `farm`
path into every NM. Source: BG-wiki Abyssea-La Theine NM + Adversaries tables (screenshots).

The roster was wrong the same way Konschtat's was — EIGHT real NMs untagged and SIX ordinary
Adversaries sitting in the NM bucket.
"""
import json, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']
ZONE = 'Abyssea-La Theine'
TRADE = "Trade it to the ??? and the NM appears."
ORD = "drops from the zone's ordinary monsters."

NMS = {
    'adamastor': ["Trophy Shield " + ORD + " " + TRADE + " (C-4)",
                  "Feeds Briareus — Adamastor drops the Dented Gigas shield, one of its three pop items."],
    'akash': ["Timed pop across five spawn points, roughly every 20 minutes. It roams, so sweep the zone."],
    'baba yaga': ["Piceous Scale " + ORD + " " + TRADE + " (H-7)",
                  "Feeds Carabosse — Baba Yaga drops the Shimmering pixie pinion, one of its two pop items."],
    'briareus': ["The La Theine zone boss, and a three-NM chain.",
                 "Dented Gigas shield — Adamastor (trade a Trophy Shield at C-4).",
                 "Warped Gigas armband — Pantagruel (trade an Oversized Sock at F-7).",
                 "Severed Gigas collar — Grandgousier (trade a Massive Armband at F-10).",
                 "With all three, examine the ??? at (G-6).",
                 "Feeds Hadhayosh — Briareus drops the Blood-smeared Gigas helm, one of its four pop items."],
    'carabosse': ["A two-NM chain.",
                  "Pellucid fly eye — La Theine Liege (trade a Transparent Insect Wing at I-7).",
                  "Shimmering pixie pinion — Baba Yaga (trade a Piceous Scale at H-7).",
                  "With both, examine the ??? at (H-7).",
                  "Feeds Hadhayosh — Carabosse drops the Glittering pixie choker, one of its four pop items."],
    'chasmic hornet': ["Timed pop — no items needed. It reappears every 10-15 minutes at (F-8)."],
    'dozing dorian': ["Dried Chigoe " + ORD + " " + TRADE + " (L-6)"],
    'grandgousier': ["Massive Armband " + ORD + " " + TRADE + " (F-10)",
                     "Feeds Briareus — Grandgousier drops the Severed Gigas collar, one of its three pop items."],
    'hadhayosh': ["The end of the La Theine chain — four pop items off four different NMs.",
                  "Blood-smeared Gigas helm — Briareus, which itself needs Adamastor, Pantagruel and Grandgousier killed first.",
                  "Glittering pixie choker — Carabosse, which needs La Theine Liege and Baba Yaga first.",
                  "Bloodied saber tooth — Megantereon (trade a Gargantuan Black Tiger Fang at C-7).",
                  "Marbled mutton chop — Trudging Thomas (trade an R. Mutton Chop at J-8).",
                  "With all four, examine the ??? at (J-8)."],
    'irrlicht': ["Timed pop — no items needed. It reappears every 10-15 minutes at (G-9)."],
    'karkinos': ["Fished up at (H-7) — bait with a Dried Squid while holding a Smoldering crab shell.",
                 "Dried Squid comes off Poroggo Dom Juan (trade a Bug-eaten Hat at J-11); the Smoldering crab shell comes off Nahn, which is itself fished up at the same pond."],
    'keesha poppo': ["Timed pop — no items needed. It reappears every 10-15 minutes at (L-7)."],
    'la theine liege': ["Transparent Insect Wing " + ORD + " " + TRADE + " (I-7)",
                        "Feeds Carabosse — La Theine Liege drops the Pellucid fly eye, one of its two pop items."],
    'lugarhoo': ["Filthy Gnole Claw " + ORD + " " + TRADE + " (H-11)"],
    'mangy-tailed marvin': ["Timed pop — no items needed. It reappears every 10-15 minutes at (E-5)."],
    'megamaw mikey': ["Timed pop — no items needed. It reappears every 10-15 minutes at (L-8)."],
    'megantereon': ["Gargantuan Black Tiger Fang " + ORD + " " + TRADE + " (C-7)",
                    "Feeds Hadhayosh — Megantereon drops the Bloodied saber tooth, one of its four pop items."],
    'nahn': ["Fished up from the pond at (H-7) — no pop item needed.",
             "Feeds Karkinos — Nahn drops the Smoldering crab shell needed to fish it up."],
    'nguruvilu': ["Winter Puk Egg " + ORD + " " + TRADE + " (I-12)"],
    'ovni': ["Timed pop — no items needed. It reappears every 15-20 minutes at (K-5)."],
    'pantagruel': ["Oversized Sock " + ORD + " " + TRADE + " (F-7)",
                   "Feeds Briareus — Pantagruel drops the Warped Gigas armband, one of its three pop items."],
    'piasa': ["Timed pop — no items needed. It reappears every 10-15 minutes around the (E/F-7/8) corner."],
    'poroggo dom juan': ["Bug-eaten Hat " + ORD + " " + TRADE + " (J-11)",
                         "Feeds Karkinos — Poroggo Dom Juan drops the Dried Squid used as bait to fish it up."],
    'toppling tuber': ["Giant Agaricus " + ORD + " " + TRADE + " (F-7)"],
    'trudging thomas': ["R. Mutton Chop " + ORD + " " + TRADE + " (J-8)",
                        "Feeds Hadhayosh — Trudging Thomas drops the Marbled mutton chop, one of its four pop items."],
    'meditator': ["First step of the demilune chain: rest anywhere in the zone holding a Clear demilune abyssite.",
                  "Drops the Colorful demilune abyssite, which is what spawns Brooder."],
    'brooder': ["Second step of the demilune chain: kill Meditator for the Colorful demilune abyssite, then rest while holding it.",
                "Drops the Scarlet demilune abyssite, which is what spawns Ruminator."],
    'ruminator': ["Last step of the demilune chain: Meditator gives the Colorful abyssite, Brooder gives the Scarlet one.",
                  "Rest anywhere in the zone holding the Scarlet demilune abyssite."],
}

ADVERSARIES = ['angler tiger', 'bathyal gigas', 'black merino', 'brae opo-opo', 'cankercap', 'crapaudy',
               'crepuscule puk', 'demersal gigas', 'ephemeral clionid', 'ephemeral limule', 'farfadet',
               'geier', 'gigadaphnia', 'great wasp', 'hadal gigas', 'hammering ram', 'irate sheep',
               'luison', 'pasture funguar', 'plateau glider', 'plateau hare', 'poroggo seducteur',
               'psychopomp', 'rock grinder', 'veld clionid', 'sentinel crab']

BOSS = 'briareus'


def set_tag(key, role):
    m = M[key]
    tags = [t for t in (m.get('content') or []) if not t.startswith('Abyssea: ' + ZONE)]
    tags.append('Abyssea: %s: %s' % (ZONE, role))
    m['content'] = tags


def ensure_zone(key, band=None):
    zs = M[key].get('zones') or []
    for z in zs:
        if z[0] == ZONE:
            if band and len(z) == 1:
                z.append(band)
            return
    zs.append([ZONE, band] if band else [ZONE])
    M[key]['zones'] = zs


was = {k: [t for t in (v.get('content') or []) if t.startswith('Abyssea: ' + ZONE)] for k, v in M.items()}
prev = {k for k, v in was.items() if v}

for key, farm in NMS.items():
    M[key]['nm'] = True
    set_tag(key, 'Zone Boss' if key == BOSS else 'NM')
    ensure_zone(key)
    M[key]['farm'] = farm
for key in ADVERSARIES:
    set_tag(key, 'Adversary')
    lv = M[key].get('lv')
    ensure_zone(key, '%d-%d' % (lv[0], lv[1]) if lv else None)

assert not [kk for mm in M.values() for kk, v in mm.items() if v is None]
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

from collections import Counter
c = Counter(t for m in M.values() for t in (m.get('content') or []) if t.startswith('Abyssea: ' + ZONE))
print('was tagged: %d | now: %d NMs + %d adversaries' % (len(prev), len(NMS), len(ADVERSARIES)))
print('NMs that had NO tag before:', sorted(k for k in NMS if k not in prev))
print('Adversaries that were in the NM bucket:', sorted(k for k in ADVERSARIES if k in prev))
for t, n in sorted(c.items()):
    print('  %2d  %s' % (n, t))
