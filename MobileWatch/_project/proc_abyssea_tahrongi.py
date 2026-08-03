#!/usr/bin/env python3
"""Abyssea-Tahrongi roster correction + pop chains (rev 256). USER: "tonghri, or however its spelled"

Third zone through the rev-254 pass. Source: BG-wiki Abyssea-Tahrongi NM + Adversaries tables.
Tahrongi has the deepest chain of the three zones done so far — Lacovie sits behind BOTH Glavoid and
Chloris, each of which needs four feeders of its own.
"""
import json, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']
ZONE = 'Abyssea-Tahrongi'
TRADE = "Trade it to the ??? and the NM appears."
ORD = "drops from the zone's ordinary monsters."

NMS = {
    'abas': ["Eft Egg " + ORD + " " + TRADE + " (K-10)",
             "Feeds Alectryon — Abas drops the Quivering Eft Egg, one of its two pop items."],
    'adze': ["Timed pop — no items needed. It reappears every 10-15 minutes at (G-5).",
             "Feeds Glavoid — Adze drops the Sticky gnat wing, one of its four pop items."],
    'alectryon': ["Two pop items: a Chunk of Cockatrice Tailmeat " + ORD.rstrip('.') + ", and a Quivering Eft Egg off Abas (trade an Eft Egg at K-10).",
                  "Trade both to the ??? at (H-8).",
                  "Feeds Glavoid — Alectryon drops the Fat-lined cockatrice skin, one of its four pop items."],
    'bhumi': ["Timed pop across five spawn points, roughly every 20 minutes. It roams the zone."],
    'cannered noz': ["Baleful Skull " + ORD + " " + TRADE + " (F-6)",
                     "Feeds Treble Noctules — Cannered Noz drops the Exorcised Skull, one of its two pop items."],
    'chloris': ["A four-NM chain, and half of what Lacovie needs.",
                "Torn bat wing — Treble Noctules (Bloody Fang + an Exorcised Skull off Cannered Noz).",
                "Veinous hecteyes eyelid — Ophanim (Bloodshot Hecteye + Shriveled Wing off Halimede + Tarnished Pincer off Vetehinen).",
                "Mossy adamantoise shell — Chukwa, a timed pop at (F-4/5).",
                "Gory scorpion claw — Hedetet (Venomous Scorpion Stinger + Acidic Humus off Gancanagh).",
                "With all four, trade them to the ??? at (I-8).",
                "Feeds Lacovie — Chloris drops the Overgrown mandragora flower, one of its two pop items."],
    'chukwa': ["Timed pop — no items needed. It reappears every 10-15 minutes at (F-4/5).",
               "Feeds Chloris — Chukwa drops the Mossy adamantoise shell, one of its four pop items."],
    'cuelebre': ["Timed pop — no items needed. It reappears every 10-15 minutes at (F-8/9)."],
    'gancanagh': ["Alkaline Humus " + ORD + " " + TRADE + " (H-8)",
                  "Feeds Hedetet — Gancanagh drops the Acidic Humus, one of its two pop items."],
    'glavoid': ["The Tahrongi zone boss, and a four-NM chain.",
                "Luxuriant manticore mane — Muscaliet (Resilient Mane + Smooth Whisker off Tefenet).",
                "Fat-lined cockatrice skin — Alectryon (Chunk of Cockatrice Tailmeat + Quivering Eft Egg off Abas).",
                "Sticky gnat wing — Adze, a timed pop at (G-5).",
                "Sodden sandworm husk — Minhocao, a timed pop wandering around (I-6).",
                "With all four, examine the ??? at (I-5).",
                "Feeds Lacovie — Glavoid drops the Chipped sandworm tooth, one of its two pop items."],
    'halimede': ["High-quality Clionid Wing " + ORD + " " + TRADE + " (G-12)",
                 "Feeds Ophanim — Halimede drops the Shriveled Wing, one of its three pop items."],
    'hedetet': ["Two pop items: a Venomous Scorpion Stinger " + ORD.rstrip('.') + ", and an Acidic Humus off Gancanagh (trade an Alkaline Humus at H-8).",
                "Trade both to the ??? at (F-7).",
                "Feeds Chloris — Hedetet drops the Gory scorpion claw, one of its four pop items."],
    'iratham': ["Time-of-day pop — it appears between 17:00 and 21:00 game time and roams the zone. No items needed."],
    'lachrymater': ["Moaning Vestige " + ORD + " " + TRADE + " (G-10)",
                    "Needed for Myrmecoleon — drag Lachrymater on top of it to force the ambush."],
    'lacovie': ["The end of the Tahrongi chain, and the deepest one in Abyssea so far — it sits behind both of the zone's big pop-item NMs.",
                "Chipped sandworm tooth — Glavoid, which itself needs Muscaliet, Alectryon, Adze and Minhocao.",
                "Overgrown mandragora flower — Chloris, which itself needs Treble Noctules, Ophanim, Chukwa and Hedetet.",
                "With both, examine the ??? at (F-5)."],
    'manananggal': ["Timed pop — no items needed. It reappears every 10-15 minutes at (I-12)."],
    'mictlantecuhtli': ["Timed pop — no items needed. It reappears every 10-15 minutes at (F/G-4)."],
    'minhocao': ["Timed pop — no items needed. It reappears every 10-15 minutes and wanders widely around (I-6).",
                 "Feeds Glavoid — Minhocao drops the Sodden sandworm husk, one of its four pop items."],
    'muscaliet': ["Two pop items: a Resilient Mane " + ORD.rstrip('.') + ", and a Smooth Whisker off Tefenet (trade a Shocking whisker at G-6).",
                  "Trade both to the ??? at (J-6).",
                  "Feeds Glavoid — Muscaliet drops the Luxuriant manticore mane, one of its four pop items."],
    'myrmecoleon': ["No pop item — drag Lachrymater on top of it at (G-10) and it ambushes.",
                    "Lachrymater is itself a trade pop: a Moaning Vestige to the ??? at (G-10)."],
    'ophanim': ["Three pop items: a Bloodshot Hecteye " + ORD.rstrip('.') + ", a Shriveled Wing off Halimede (High-quality Clionid Wing at G-12), and a Tarnished Pincer off Vetehinen (High quality Limule Pincer at H-10).",
                "Trade all three to the ??? at (G-9).",
                "Feeds Chloris — Ophanim drops the Veinous hecteyes eyelid, one of its four pop items."],
    'quetzalli': ["Time-of-day pop — it appears between 9:00 and 21:00 game time and roams the zone. No items needed."],
    'rubicund adenium': ["Quest pop — it appears during A Sterling Specimen, around (H-7)."],
    'tefenet': ["Shocking whisker " + ORD + " " + TRADE + " (G-6)",
                "Feeds Muscaliet — Tefenet drops the Smooth Whisker, one of its two pop items."],
    'treble noctules': ["Two pop items: a Bloody Fang " + ORD.rstrip('.') + ", and an Exorcised Skull off Cannered Noz (trade a Baleful Skull at F-6).",
                        "Trade both to the ??? at (I-9).",
                        "Feeds Chloris — Treble Noctules drops the Torn bat wing, one of its four pop items."],
    'vetehinen': ["High quality Limule Pincer " + ORD + " " + TRADE + " (H-10)",
                  "Feeds Ophanim — Vetehinen drops the Tarnished Pincer, one of its three pop items."],
    'hungerer': ["First step of the demilune chain: rest anywhere in the zone holding a Clear demilune abyssite.",
                 "Drops the Colorful demilune abyssite, which is what spawns Yearner."],
    'yearner': ["Second step of the demilune chain: kill Hungerer for the Colorful demilune abyssite, then rest while holding it.",
                "Drops the Viridian demilune abyssite, which is what spawns Usurper."],
    'usurper': ["Last step of the demilune chain: Hungerer gives the Colorful abyssite, Yearner gives the Viridian one.",
                "Rest anywhere in the zone holding the Viridian demilune abyssite."],
}

ADVERSARIES = ['beholder', 'blood bat', 'bog body', 'canyon eft', 'canyon scorpion', 'caoineag',
               'cluckatrice', 'ephemeral clionid', 'ephemeral limule', 'gulch limule', 'gully clionid',
               'hieracosphinx', 'jaguarundi', 'lamenter', 'naul', 'nematocera', 'pachypodium',
               'sturdy pyxis', 'thalassinon', 'vermes carnium', 'wiederganger', 'abuscader antlion']
BOSS = 'glavoid'


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
print('was tagged: %d | now %d NMs + %d adversaries' % (len(prev), len(NMS), len(ADVERSARIES)))
print('NMs that had NO tag:', sorted(k for k in NMS if k not in prev))
print('Adversaries that were in the NM bucket:', sorted(k for k in ADVERSARIES if k in prev))
for t, n in sorted(c.items()):
    print('  %2d  %s' % (n, t))
