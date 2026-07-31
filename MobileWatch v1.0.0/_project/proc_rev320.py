#!/usr/bin/env python3
"""
MobileWatch mobs.json refining pass - rev 320
Author: BalladOfWorms

PART A - TWO ZONES: North Gustaberg [S] (16 NM + 36 ADV) + Grauberg [S] (11 NM + 42 ADV).
PART B - USER RULING: "for skirmish [u] zones, if we dont have a zone, still add mob to bestiary"
         -> build the 49 missing instanced-content records across Cirdas Caverns [U],
            Rala Waterways [U] and Outer Ra'Kaznar [U].

`fam` is set ONLY where a page published a Genus, except on the Rala Waterways [U] rows, whose
page carries no Genus column - there the family is derived from the family noun in the mob's own
name and the two that have none (Bufobrawler, Bonesoaked Bandit) are left unset rather than guessed.

Airlixir / Etched Memory / Codex of Etchings are NOT in ffxi_items.json (0 fuzzy hits for any of
them), so per the drops convention they go in `notes`, never in `drops`.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

SKIP = object()

NGUST = 'North Gustaberg [S]'
GRAU = 'Grauberg [S]'
CIRDAS_U = 'Cirdas Caverns [U]'
RALA_U = 'Rala Waterways [U]'
OUTER_U = "Outer Ra'Kaznar [U]"

NGUST_ROWS = {
    'gloomanita': '48',
    'sandworm': '~88',
    'quadav transporter': SKIP,
    'quadav guard': SKIP,
    'ankabut': '52',
    'olgoi-khorkhoi': '54',
    'peaseblossom': SKIP,
    'stabnix skewerfinger': SKIP,
    'pixie impaler': SKIP,
    'ushumgal': SKIP,
    'ground guzzler': SKIP,
    'globster': SKIP,
    'shoggoth': SKIP,
    'lamprey lord': SKIP,
    'blobdingnag': SKIP,
    'yilbegan': SKIP,
    'tunnel worm': '10-12',
    'walking sapling': '12-14',
    'river crab': '15-18',
    'vulture': '15-18',
    'huge hornet': '38-39',
    'maneating hornet': '40-42',
    'pixie': '51-54',
    'revenant': '38-40',
    'huge spider': '35-38',
    'ornery sheep': '25-28',
    'stone eater': '18-22',
    'rock eater': '32-35',
    'enchanted bones': '28-30',
    'ding bats': '26-28',
    'fledermaus': '26-28',
    'lesser wivre': '45-47',
    'rock lizard': '21-23',
    'drachenlizard': '93-94',
    'coppercap': '41-43',
    'black wolf': '33-35',
    'goblin patrolman': '56-59',
    'goblin franctireur': '56-59',
    'goblin draftee': '56-59',
    'goblin skirmisher': '56-59',
    "goblin's bee": '52-54',
    'young quadav': '61-64',
    'amber quadav': '61-64',
    'amethyst quadav': '61-64',
    'veteran quadav': '61-64',
    'onyx quadav': '61-64',
    'greater quadav': '61-64',
    'copper quadav': '61-64',
    'goblin chapman': '72-74',
    'goblin aidman': '72-74',
    'goblin freelance': '72-74',
    'goblin picaroon': SKIP,
}

GRAU_ROWS = {
    'dark ixion': '80-85',
    'kotan-kor kamuy': '80-82',
    'sarcopsylla': '70-72',
    'scitalis': '83',
    'vasiliceratops': '88-89',
    'migratory hippogryph': SKIP,
    'quadav transporter': SKIP,
    'quadav guard': SKIP,
    "ru'bha stonewall": SKIP,
    'sentinel wivre': SKIP,
    'ocythoe': SKIP,
    'air elemental': '75-80',
    'ajattara': '79-82',
    'amethyst quadav': '61-63',
    'black wolf': '49-51',
    'blood soul': '52-54',
    'brass quadav': '66-69',
    'brasscap': '59-61',
    'bronze quadav': '66-69',
    'chigoe': '43-46',
    'copper quadav': '61-63',
    'doom mage': '66-69',
    'doom soldier': '66-69',
    'feyweald sapling': '93-94',
    'fighting pugil': SKIP,
    'gill pugil': SKIP,
    'goblin blastmaster': '62-64',
    'goblin corpsman': '62-64',
    'goblin freesword': '62-64',
    'goblin pioneer': '62-64',
    'grauberg hippogryph': '73-75',
    'greater quadav': '61-63',
    'heliodor quadav': '66-69',
    'hill crab': SKIP,
    'knotty treant': '62-64',
    'old quadav': '66-69',
    'onyx quadav': '61-63',
    'peiste': '67-70',
    'pixie': '56-59',
    'pug pugil': SKIP,
    'river crab': SKIP,
    'rock eater': '33-35',
    'sapphirine quadav': '66-69',
    'sidhe': '75-77',
    'silver quadav': '66-69',
    'thunder elemental': '60',
    'vampire bat': '43-45',
    'veteran quadav': '61-63',
    'wandering sapling': '36-39',
    'war lizard': '41-43',
    'wingrats': '43-45',
    'wivre': '68-74',
    'young quadav': '61-63',
}

# Notorious-Monsters-table rows rendering as ordinary mobs
NM_SET = ['quadav transporter', 'quadav guard', 'vasiliceratops',
          "ru'bha stonewall", 'sentinel wivre']

# ---------------------------------------------------------------- PART B
DELVE_VEIL = {
    'Fugacious Beetle': ('Beetle', 'Ceizak Battlegrounds'),
    'Fugacious Bugard': ('Bugard', 'Morimar Basalt Fields'),
    'Fugacious Crab': ('Crab', 'Foret de Hennetiel'),
    'Fugacious Diremite': ('Diremite', 'Ceizak Battlegrounds'),
    'Fugacious Eft': ('Eft', 'Morimar Basalt Fields'),
    'Fugacious Eruca': ('Crawler', 'Ceizak Battlegrounds'),
    'Fugacious Kraken': ('Sea Monk', 'Foret de Hennetiel'),
    'Fugacious Lizard': ('Hill Lizard', 'Morimar Basalt Fields'),
    'Fugacious Luckybug': ('Ladybug', 'Ceizak Battlegrounds'),
    'Fugacious Toad': ('Frog', 'Foret de Hennetiel'),
    'Fugacious Wivre': ('Wivre', 'Morimar Basalt Fields'),
}
CIRDAS_SKIRMISH = {
    'Abrupta Spawn': 'Funguar',
    'Bloodcurdling Acuex': 'Acuex',
    'Brumeblister Obdella': 'Leech',
    'Crustguzzler Worm': 'Worm',
    'Doline Bats': 'Flock Bat',
    'Estavelle Acuex': 'Acuex',
    'Funguar Abrupta': 'Funguar',
    'Pustulous Obdella': 'Leech',
    'Recalcitrant Umbril': 'Umbril',
    'Rufescent Bat': 'Bat',
    'Sanguinary Clot': 'Slime',
}
RALA_NM = {
    'Photophobic Bat': 'Bat',
    'Woecroak Toad': 'Frog',
    'Skulking Spider': 'Spider',
    'Forsaken Obdella': 'Leech',
    'Sewer Tarichuk': 'Eft',
    'Karst Crab': 'Crab',
    'Sludgeslither Slime': 'Slime',
    'Crustnibbler Twitherym': 'Twitherym',
}
RALA_ADV = {
    'Anklebiter Slug': 'Slug',
    'Aquifer Leech': 'Leech',
    'Bufobrawler': None,
    'Bonesoaked Bandit': None,
    'Coreborn Spider': 'Spider',
    'Deft Eft': 'Eft',
}
RALA_NOTES = {
    'Woecroak Toad': ['Spawns x2, on Tiers I-V.',
                      'Its normal attacks apply a Poison dealing roughly 100-150 HP per tick.'],
    'Skulking Spider': ['Casts Break and Stonega IV.'],
    'Sewer Tarichuk': ['May take roughly triple damage from magic.'],
    'Sludgeslither Slime': ['Resists physical damage and takes extra magical damage.'],
    'Crustnibbler Twitherym': ['Spawns x1, on Tiers III-V.'],
    'Karst Crab': ['Spawns x2, on Tier V only.'],
}
OUTER_NM = {
    'Acrimonious Dullahan': 'Dullahan',
    'Burnished Mimic': 'Mimic',
    'Cantankerous Yztarg': 'Yztarg',
    'Jaunting Yeceux': 'Acuex',
    'Shambling Naraka': 'Naraka',
}
OUTER_SKIRMISH = {
    'Breathless Clansman': 'Skeleton',
    'Effluvial Acuex': 'Acuex',
    'Splenetic Umbril': 'Umbril',
}
OUTER_VAGARY = {
    'Ravaging Acuex': ('Acuex', 'Fire'),
    'Unabted Mush': ('Slime', 'Ice'),
    'Jaundiced Slime': ('Slime', 'Wind'),
    'Gangrenous Leeches': ('Leech', 'Lightning'),
    'Draery Obdella': ('Leech', 'Water'),
}


def band(s):
    if s.startswith('~'):
        s = s[1:]
    if not s or not s[0].isdigit():
        return None
    lo, _, hi = s.partition('-')
    try:
        return int(lo), int(hi or lo)
    except ValueError:
        return None


def apply_zone(mob, zone, lvl, log, key):
    zones = mob.setdefault('zones', [])
    entry = None
    for z in zones:
        if isinstance(z, list) and z and z[0] == zone:
            entry = z
            break
        if isinstance(z, str) and z == zone:
            log['kept_flat'].append(key)
            return
    if entry is None:
        zones.append([zone] if lvl is SKIP else [zone, lvl])
        log['added'].append((key, zone, None if lvl is SKIP else lvl))
        return
    if lvl is SKIP:
        log['blank_kept'].append((key, zone, entry[1] if len(entry) > 1 else None))
        return
    if len(entry) == 1:
        entry.append(lvl)
        log['filled'].append((key, zone, lvl))
    elif entry[1] != lvl:
        log['changed'].append((key, zone, entry[1], lvl))
        entry[1] = lvl
    else:
        log['same'].append((key, zone, lvl))


def widen(mob, lvl, log, key):
    if lvl is SKIP:
        return
    b = band(lvl)
    cur = mob.get('lv')
    if b is None or not isinstance(cur, list) or len(cur) != 2:
        return
    new = [min(cur[0], b[0]), max(cur[1], b[1])]
    if new != cur:
        log['lv_union'].append((key, list(cur), new))
        mob['lv'] = new


def build(mobs, log, name, fam, zone, zlvl=None, nm=False, spawn=None, notes=None):
    key = name.lower()
    if key in mobs:
        log['build_skipped'].append(key)
        return
    rec = {'n': name}
    if fam:
        rec['fam'] = fam
    if nm:
        rec['nm'] = True
    if spawn:
        rec['spawn'] = spawn
    if notes:
        rec['notes'] = list(notes)
    rec['zones'] = [[zone] if zlvl is None else [zone, zlvl]]
    mobs[key] = rec
    log['built'].append((key, fam, zone, zlvl))


def main():
    with open(PATH, encoding='utf-8') as fh:
        data = json.load(fh)
    mobs = data['mobs']

    log = {k: [] for k in
           ('added', 'filled', 'changed', 'blank_kept', 'same', 'lv_union',
            'nm_set', 'missing', 'kept_flat', 'built', 'build_skipped')}

    # ---- PART A
    for table, zone in ((NGUST_ROWS, NGUST), (GRAU_ROWS, GRAU)):
        for key, lvl in table.items():
            mob = mobs.get(key)
            if mob is None:
                log['missing'].append(key)
                continue
            apply_zone(mob, zone, lvl, log, key)
            widen(mob, lvl, log, key)
    for key in NM_SET:
        mob = mobs[key]
        if not mob.get('nm'):
            mob['nm'] = True
            log['nm_set'].append(key)

    # ---- PART B
    for name, (fam, veil) in DELVE_VEIL.items():
        build(mobs, log, name, fam, CIRDAS_U,
              spawn=f'Delve ({veil} Veil)',
              notes=['Standard Delve monster; yields 50 plasm per kill.',
                     'Drops an Airlixir.'])
    for name, fam in CIRDAS_SKIRMISH.items():
        build(mobs, log, name, fam, CIRDAS_U, zlvl='105+', spawn='Skirmish',
              notes=['Skirmish monster.'])
    for name, fam in RALA_NM.items():
        build(mobs, log, name, fam, RALA_U, nm=True, spawn='Skirmish',
              notes=RALA_NOTES.get(name))
    for name, fam in RALA_ADV.items():
        build(mobs, log, name, fam, RALA_U, spawn='Skirmish')
    for name, fam in OUTER_NM.items():
        build(mobs, log, name, fam, OUTER_U, nm=True, spawn='Skirmish')
    for name, fam in OUTER_SKIRMISH.items():
        build(mobs, log, name, fam, OUTER_U, spawn='Skirmish')
    for name, (fam, el) in OUTER_VAGARY.items():
        build(mobs, log, name, fam, OUTER_U, spawn='Vagary (Brash Gate)',
              notes=[f'Vagary: takes double damage from {el}.',
                     'Drops an Etched Memory and a Codex of Etchings.'])

    # ---- guards
    assert not [k for m in mobs.values() for k, v in m.items() if v is None], 'null poison'
    fe = data['family_eco']
    bad = sorted({m['fam'] for m in mobs.values() if m.get('fam') and m['fam'] not in fe})
    assert not bad, f'fam with no family_eco: {bad}'
    for k, m in mobs.items():
        for z in m.get('zones') or []:
            if isinstance(z, list):
                assert 1 <= len(z) <= 2 and isinstance(z[0], str), (k, z)
                assert len(z) == 1 or isinstance(z[1], str), (k, z)

    with open(PATH, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, separators=(', ', ': '), ensure_ascii=False)

    for name in ('added', 'filled', 'changed', 'lv_union', 'nm_set', 'built',
                 'build_skipped', 'missing', 'blank_kept', 'kept_flat'):
        rows = log[name]
        print(f'== {name} ({len(rows)})')
        for r in rows:
            print('   ', r)
    print(f'== same ({len(log["same"])})')


if __name__ == '__main__':
    main()
