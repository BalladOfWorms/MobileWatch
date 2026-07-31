#!/usr/bin/env python3
"""Unity Mobs (UNM) content tags + levels + zones (rev 194).
USER: "unm mobs in 2nd and 3rd image"

Source = the Unity wanted-target table: Level | Accolades | NM | Zone | Category.
In remit: `content: ["Unity Mobs"]`, the published LEVEL (rule 9 — union, never shrink),
and the zone entry where the record lacks it.
`Kubool Ja'a Mhuufya` on the page keys as `kubool ja's mhuufya` in the file (rule 65).
"""
import json, os
from zonepass import ASSETS

UNM = [  # (key, level, zone)
    ("bounding belinda", 75, "South Gustaberg"), ("hugemaw harold", 75, "East Ronfaure"),
    ("prickly pitriv", 75, "East Sarutabaruta"), ("ironhorn baldurno", 99, "La Theine Plateau"),
    ("sleepy mabel", 99, "Konschtat Highlands"), ("serpopard ninlil", 99, "Tahrongi Canyon"),
    ("abyssdiver", 119, "Buburimu Peninsula"), ("immanibugard", 119, "Lufaise Meadows"),
    ("intuila", 119, "Bibiki Bay"), ("jester malatrix", 119, "Qufim Island"),
    ("orcfeltrap", 119, "Carpenters Landing"), ("sybaritic samantha", 119, "Yuhtunga Jungle"),
    ("valkurm imperator", 119, "Valkurm Dunes"), ("cactrot veloz", 122, "Eastern Altepa Desert"),
    ("emperor arthro", 122, "Jugner Forest"), ("garbage gel", 122, "Bostaunieux Oubliette"),
    ("joyous green", 122, "Pashhow Marshlands"), ("keeper of heiligtum", 122, "The Sanctuary of Zi'Tah"),
    ("tiyanak", 122, "Misareaux Coast"), ("voso", 122, "Labyrinth of Onzozo"),
    ("warblade beak", 122, "Meriphataud Mountains"), ("woodland mender", 122, "Yhoator Jungle"),
    ("arke", 125, "Sauromugue Champaign"), ("ayapec", 125, "The Boyahda Tree"),
    ("azure-toothed clawberry", 125, "Temple of Uggalepih"), ("bakunawa", 125, "Sea Serpent Grotto"),
    ("beist", 125, "Xarcabard"), ("centurio xx-i", 125, "Quicksand Caves"),
    ("coca", 125, "Ifrit's Cauldron"), ("douma weapon", 125, "Ro'Maeve"),
    ("king uropygid", 125, "Western Altepa Desert"), ("kubool ja's mhuufya", 125, "Wajaom Woodlands"),
    ("largantua", 125, "Beaucedine Glacier"), ("lumber jill", 125, "Batallia Downs"),
    ("mephitas", 125, "Garlaige Citadel"), ("muut", 125, "Attohwa Chasm"),
    ("specter worm", 125, "Kuftal Tunnel"), ("strix", 125, "Rolanberry Fields"),
    ("vermillion fishfly", 125, "Lufaise Meadows"), ("azrael", 128, "Den of Rancor"),
    ("borealis shadow", 128, "Fei'Yin"), ("camahueto", 128, "Uleguerand Range"),
    ("carousing celine", 128, "Fei'Yin"), ("grand grenade", 128, "Mount Zhayolm"),
    ("vedrfolnir", 128, "Cape Teriggan"), ("vidmapire", 128, "Alzadaal Undersea Ruins"),
    ("volatile cluster", 128, "Misareaux Coast"), ("glazemane", 128, "Cape Teriggan"),
    ("wyvernhunter bambrox", 128, "Gustav Tunnel"), ("hidhaegg", 135, "The Boyahda Tree"),
    ("sovereign behemoth", 135, "Behemoth's Dominion"), ("tolba", 135, "Valley of Sorrows"),
    ("thu'ban", 135, "Wajaom Woodlands"), ("sarama", 135, "Mount Zhayolm"),
    ("shedu", 135, "Caedarva Mire"), ("tumult curator", 145, "Aydeewa Subterrane"),
]
TAG = "Unity Mobs"

p = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(p, encoding='utf-8')); mobs = d['mobs']
zj = {z['name'] for z in json.load(open(os.path.join(ASSETS, 'zones.json'), encoding='utf-8'))['zones']}

tagged, lv_made, lv_union, zone_added, zone_filled, missing = [], [], [], [], [], []
for k, lv, zone in UNM:
    m = mobs.get(k)
    if m is None:
        missing.append(k); continue
    tags = m.get('content') or []
    if TAG not in tags:
        m['content'] = tags + [TAG]; tagged.append(k)
    old = m.get('lv')
    if old is None:
        m['lv'] = [lv, lv]; lv_made.append(f"{k} -> [{lv},{lv}]")
    elif lv < old[0] or lv > old[1]:
        new = [min(lv, old[0]), max(lv, old[1])]
        m['lv'] = new; lv_union.append(f"{k} {old} -> {new}")
    if zone not in zj:
        print(f"  !! {zone!r} not in zones.json — skipped for {k}"); continue
    zs = m.setdefault('zones', [])
    hit = next((e for e in zs if (e[0] if isinstance(e, list) else e) == zone), None)
    if hit is None:
        zs.append([zone, str(lv)]); zone_added.append(f"{k} -> {zone} {lv}")
    elif isinstance(hit, list) and (len(hit) == 1 or not hit[1]):
        hit[:] = [zone, str(lv)]; zone_filled.append(f"{k} -> {zone} {lv}")

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
for label, rows in (("tagged", tagged), ("lv CREATED", lv_made), ("lv UNION", lv_union),
                    ("zone ADDED", zone_added), ("zone level FILLED", zone_filled)):
    print(f"{label} ({len(rows)}): {', '.join(rows) if label != 'tagged' else len(rows)}")
print("missing records:", missing or "(none)")
