#!/usr/bin/env python3
"""Abyssea roster correction + Konschtat pop chains (rev 254).

USER: "mobs in abyssea, lets make sure we have them correct in content and json. levels when we can,
pop locations and items, and if possible, a farming guide in each mobs entry showing the path to
spawning them. kons. first. also, zone bosses go to top of list."

Source: BG-wiki Abyssea-Konschtat NM + Adversaries tables and the community farming map (screenshots).

1. All nine Abyssea Zone Bosses get the role segment "Zone Boss" so the page can float them.
2. Konschtat's roster is corrected: the 2-segment tags become
   "Abyssea: Abyssea-Konschtat: <Zone Boss|NM|Adversary>". SEVEN ordinary Adversaries were tagged as
   though they were NMs, and SIX real NMs had no tag at all.
3. Every Konschtat NM gets its pop location/item confirmed and a new `farm` list — the actual path to
   spawning it, including which NM the pop item comes from and what its own drop unlocks next.
"""
import json, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']

ZONE = 'Abyssea-Konschtat'

ZONE_BOSSES = {
    'bennu': 'Abyssea-Altepa', 'itzpapalotl': 'Abyssea-Attohwa', 'amphitrite': 'Abyssea-Grauberg',
    'kukulkan': 'Abyssea-Konschtat', 'briareus': 'Abyssea-La Theine', 'cirein-croin': 'Abyssea-Misareaux',
    'glavoid': 'Abyssea-Tahrongi', 'resheph': 'Abyssea-Uleguerand', 'sedna': 'Abyssea-Vunkerl',
}

# key -> (pop line for `spawn` when the record has none, farm lines)
# Pop items that come off another NM are named with their source; everything else drops from the
# zone's ordinary monsters.
TRADE = 'Trade it to the ??? and the NM appears.'
NMS = {
    'alkonost': ('Forced (trade a Giant Bugard Tusk to the ??? at (H-6))', [
        'Giant Bugard Tusk drops from the zone\'s ordinary monsters. ' + TRADE,
        'Feeds Kukulkan — Alkonost drops the Tattered hippogryph wing, one of its three pop items.']),
    'arimaspi': ('Forced (trade a Clouded Lens to the ??? at (K-6))', [
        'Clouded Lens drops from the zone\'s ordinary monsters. ' + TRADE,
        'Feeds Kukulkan — Arimaspi drops the Mucid Ahriman eyeball, one of its three pop items.']),
    'ashtaerh the gallvexed': ('Forced (trade a Murmuring Globe to the ??? at (J-11))', [
        'Murmuring Globe drops from the zone\'s ordinary monsters. ' + TRADE]),
    'bakka': ('Timed (10-15 min.) at (J/K-5)', [
        'Timed pop — no items needed. It reappears on its own every 10-15 minutes at (J/K-5).']),
    'balaur': ('Timed (10-15 min.) at (L-7)', [
        'Timed pop — no items needed. It reappears on its own every 10-15 minutes at (L-7).']),
    'bloodeye vileberry': ('Forced (examine the ??? at (K-4) with a Twisted Tonberry crown)', [
        'Kill Tonberry Lieje, a timed pop at (K-4), for the Twisted Tonberry crown.',
        'Examine the ??? at (K-4) holding the crown.']),
    'bloodguzzler': ('Forced (trade Eft Blood to the ??? at (G-5))', [
        'Eft Blood drops from the zone\'s ordinary monsters. ' + TRADE,
        'Useful for Fistule — Bloodguzzler is one of the three NMs that can be dragged to it.']),
    'bombadeel': ('Forced (trade Snakeskin Moss to the ??? at (F-9))', [
        'Snakeskin Moss drops from the zone\'s ordinary monsters. ' + TRADE]),
    'clingy clare': ('Forced (trade a Tiny Morbol Vine to the ??? at (J-8))', [
        'Tiny Morbol Vine drops from the zone\'s ordinary monsters. ' + TRADE,
        'Feeds Eccentric Eve — Clingy Clare drops the Decaying morbol tooth, one of its five pop items.']),
    'depths digester': ('Forced (rest with a Colorful demilune abyssite) — roams the zone', [
        'Second step of the demilune chain: kill Meanderer for the Colorful demilune abyssite, then rest anywhere in the zone while holding it.',
        'Drops the Azure demilune abyssite, which is what spawns Hadal Satiator.']),
    'eccentric eve': ('Forced (examine the ??? at (I-7) with a Fragrant treant petal, Fetid rafflesia stalk, Decaying morbol tooth, Turbid slime oil and Venomous peiste claw)', [
        'The end of the Konschtat chain — five pop items off five different NMs.',
        'Fragrant treant petal — Gangly Gean (timed, E/F-10). Fetid rafflesia stalk — Raskovnik (timed, F/G-7).',
        'Decaying morbol tooth — Clingy Clare (trade a Tiny Morbol Vine at J-8). Turbid slime oil — Fistule (timed at G-3, needs an NM dragged to it).',
        'Venomous peiste claw — Kukulkan, which itself needs Alkonost, Arimaspi and Keratyrannos killed first.',
        'With all five, examine the ??? at (I-7).']),
    'fear gorta': ('Forced (trade Moonglow Cloth to the ??? at (L-5/6))', [
        'Moonglow Cloth drops from the zone\'s ordinary monsters. ' + TRADE]),
    'fistule': ('Timed (15-20 min.) at (G-3) — cannot be engaged until an NM is brought to it', [
        'Timed pop, but it will not aggro on its own: drag Bloodguzzler, Guimauve or Lentor next to it at (G-3).',
        'Bloodguzzler needs Eft Blood, Lentor needs a Giant Slug Eyestalk, Guimauve is a lottery pop off Licorice.',
        'Feeds Eccentric Eve — Fistule drops the Turbid slime oil, one of its five pop items.']),
    'gangly gean': ('Timed (10-15 min.) at (E/F-10)', [
        'Timed pop — no items needed. It reappears on its own every 10-15 minutes at (E/F-10).',
        'Feeds Eccentric Eve — Gangly Gean drops the Fragrant treant petal, one of its five pop items.']),
    'guimauve': ('Lottery (Licorice) at (G-4)', [
        'Lottery pop — kill the Licorice flans around (G-4) until it appears.',
        'Useful for Fistule — Guimauve is one of the three NMs that can be dragged to it.']),
    'hadal satiator': ('Forced (rest with an Azure demilune abyssite) — roams the zone', [
        'Last step of the demilune chain: Meanderer gives the Colorful abyssite, Depths Digester gives the Azure one.',
        'Rest anywhere in the zone holding the Azure demilune abyssite.']),
    'hexenpilz': ('Forced (trade an Oblivispore to the ??? at (G-8))', [
        'Oblivispore drops from the zone\'s ordinary monsters. ' + TRADE]),
    'keratyrannos': ('Forced (trade an Armored Dragonhorn to the ??? at (G-6))', [
        'Armored Dragonhorn drops from the zone\'s ordinary monsters. ' + TRADE,
        'Feeds Kukulkan — Keratyrannos drops the Cracked wivre horn, one of its three pop items.']),
    'khalamari': ('Timed (10-15 min.) at (E-7)', [
        'Timed pop — no items needed. It reappears on its own every 10-15 minutes at (E-7).']),
    'kukulkan': (None, [
        'The Konschtat zone boss, and a three-NM chain.',
        'Tattered hippogryph wing — Alkonost (trade a Giant Bugard Tusk at H-6).',
        'Cracked wivre horn — Keratyrannos (trade an Armored Dragonhorn at G-6).',
        'Mucid Ahriman eyeball — Arimaspi (trade a Clouded Lens at K-6).',
        'With all three, examine the ??? at (H-5).',
        'Feeds Eccentric Eve — Kukulkan drops the Venomous peiste claw, one of its five pop items.']),
    'lentor': ('Forced (trade a Giant Slug Eyestalk to the ??? at (F-6))', [
        'Giant Slug Eyestalk drops from the zone\'s ordinary monsters. ' + TRADE,
        'Useful for Fistule — Lentor is one of the three NMs that can be dragged to it.']),
    'meanderer': ('Forced (rest with a Clear demilune abyssite) — roams the zone', [
        'First step of the demilune chain: rest anywhere in the zone holding a Clear demilune abyssite.',
        'Drops the Colorful demilune abyssite, which is what spawns Depths Digester.']),
    'pavan': ('Timed (20 min., 5 spawn points) — roams the zone', [
        'Timed pop across five spawn points, roughly every 20 minutes. No items needed.']),
    'raskovnik': ('Timed (10-15 min.) at (F/G-7)', [
        'Timed pop — no items needed. It reappears on its own every 10-15 minutes at (F/G-7).',
        'Feeds Eccentric Eve — Raskovnik drops the Fetid rafflesia stalk, one of its five pop items.']),
    'sarcophilus': ('Forced (trade a Ripped Eft Skin to the ??? at (G-9))', [
        'Ripped Eft Skin drops from the zone\'s ordinary monsters. ' + TRADE]),
    'siranpa-kamuy': ('Forced (trade a Rotting Eyeball to the ??? at (J-8))', [
        'Rotting Eyeball drops from the zone\'s ordinary monsters. ' + TRADE]),
    'tonberry lieje': ('Timed (10-15 min.) at (K-4)', [
        'Timed pop — no items needed. It reappears on its own every 10-15 minutes at (K-4).',
        'Feeds Bloodeye Vileberry — Tonberry Lieje drops the Twisted Tonberry crown that spawns it.']),
    'turul': ('Timed (10-15 min.) — roams the zone', [
        'Timed pop — no items needed. It roams, so sweep the zone rather than camping one spot.']),
}

ADVERSARIES = ["ab'xzomit", 'cryptonberry occultist', 'dapifer imp', 'deep eye', 'dybbuk',
               'ephemeral clionid', 'ephemeral limule', 'gneiss leech', 'gunge slug', 'hadal mirror',
               'highland rafflesia', 'highland treant', 'hoary ragwort', 'lesser arimaspi',
               'ley clionid', 'licorice', 'mesa wivre', 'morboling', 'pustule', 'qaitu', 'razorback',
               'shadow funguar', 'shadow lizard', 'sods limule', 'sturdy pyxis',
               'tonberry bedeviler', 'trotting sapling', 'viridis wyvern', 'ypotryll']


def set_tag(key, zone, role):
    m = M[key]
    tags = [t for t in (m.get('content') or []) if not t.startswith('Abyssea: ' + zone)]
    tags.append('Abyssea: %s: %s' % (zone, role))
    m['content'] = tags


def ensure_zone(key, band=None):
    m = M[key]
    zs = m.get('zones') or []
    for z in zs:
        if z[0] == ZONE:
            if band and len(z) == 1:
                z.append(band)
            return
    zs.append([ZONE, band] if band else [ZONE])
    m['zones'] = zs


report = {'boss': [], 'nm': [], 'adv': [], 'spawn': [], 'farm': [], 'zone': []}

# 1. zone bosses everywhere
for key, zone in ZONE_BOSSES.items():
    set_tag(key, zone, 'Zone Boss')
    M[key]['nm'] = True
    report['boss'].append(key)

# 2/3. Konschtat NMs
for key, (spawn, farm) in NMS.items():
    m = M[key]
    m['nm'] = True
    if key != 'kukulkan':
        set_tag(key, ZONE, 'NM')
        report['nm'].append(key)
    ensure_zone(key)
    if spawn and not m.get('spawn'):
        m['spawn'] = spawn
        report['spawn'].append(key)
    m['farm'] = farm
    report['farm'].append(key)

# 4. adversaries — role, zone entry with their own level band
for key in ADVERSARIES:
    set_tag(key, ZONE, 'Adversary')
    lv = M[key].get('lv')
    ensure_zone(key, '%d-%d' % (lv[0], lv[1]) if lv else None)
    report['adv'].append(key)
    if not (M[key].get('zones') or []):
        report['zone'].append(key)

assert not [kk for mm in M.values() for kk, v in mm.items() if v is None]
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

from collections import Counter
c = Counter(t for m in M.values() for t in (m.get('content') or []) if t.startswith('Abyssea: ' + ZONE))
print('zone bosses tagged: %d' % len(report['boss']))
print('Konschtat NMs: %d | adversaries: %d' % (len(report['nm']) + 1, len(report['adv'])))
print('spawn filled where empty: %s' % (report['spawn'] or '(all already had one)'))
print('farm written for %d NMs' % len(report['farm']))
for t, n in sorted(c.items()):
    print('  %2d  %s' % (n, t))
