#!/usr/bin/env python3
# MobileWatch — Apex / Locus content fill (rev 245)
# Source: BG-wiki Category:Apex_Monster zone tables (user screenshots + page text).
# Fills zones, level ranges, aggro, detection, job, spawn-count/accuracy notes; creates the
# missing Locus records; stamps families onto the King Ranperre's Tomb orphans.
import json, sys, os

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']

# ---------------------------------------------------------------- table data
# rows: (mob key, job, spawns, aggro, detects, accuracy-note-tail)
# detects use our vocabulary: page "HP" -> Blood, page "True Sound" -> True Sound.
TABLES = [
    # zone key,                 zone level band,  rows
    ('Moh Gates', '125-127', [
        ('apex eft',            'Warrior', '17', False, None, '1,029'),
        ('apex eruca',          'Warrior', '10', True,  ['Sound'], '1,029'),
        ('apex matamata',       'Warrior', '9',  True,  ['Sound'], '1,029'),
        ('apex raptor',         'Warrior', '10', True,  ['Sound'], '1,029'),
    ]),
    ('Sih Gates', '125-127', [
        ('apex chapuli',        'Warrior', '14', True,  ['Sight'], '1,029'),
        ('apex jagil',          'Warrior', '10', None,  None, '1,029'),
        ('apex leech',          'Warrior', '19', True,  ['Sound'], '1,029'),
        ('apex mandragora',     'Monk',    '16', True,  ['Sound'], '1,049'),
    ]),
    ('Dho Gates', '128-130', [
        ('apex bats',           'Warrior', '27', True,  ['Sound'], '1,113'),
        ('apex crab',           'Paladin', '25', True,  ['Sound'], '1,113'),
        ('apex craklaw',        'Warrior', '14', True,  ['Sound'], '1,113'),
        ('apex jagil',          'Warrior', '15', True,  ['Sound'], '1,113'),
    ]),
    ('Woh Gates', '131-133', [
        ('apex jagil',          'Warrior', '29', None,  None, '1,203'),
        ('apex toad',           'Warrior', '18', False, None, '1,203'),
        ('velkk abyssal',       'Dark Knight', '6', True, ['Sight'], '1,203'),
        ('velkk junglemancer',  'Black Mage', '6', True, ['Sight'], '1,192'),
        ('velkk mindmelter',    'Red Mage',  '2', True, ['Sight'], '1,192'),
        ('velkk tearlicker',    'Warrior',   '4', True, ['Sight'], '1,203'),
    ]),
    ('Outer RaKaznar', '134-136', [
        ('apex bat',            'Warrior', '16', False, None, '1,294'),
        ('apex twitherym',      'Warrior', '16', False, None, '1,282'),
        ('apex ironclad',       'Warrior', '4',  True,  ['Sight', 'Sound'], '1,294'),
    ]),
    ('RaKaznar Inner Court', '137-139', [
        ('apex bats',           'Warrior', '6',  True, ['Sound'], '1,384'),
        ('apex bhoot',          'Black Mage', '18', True, ['Sound', 'Blood'], '1,384'),
        ('apex cyhiraeth',      'Black Mage', '13', True, ['Sound', 'Blood'], '1,359'),
        ('apex draugar',        None,      '18', True, ['Sound', 'Blood'], None),
        ('apex poxhound',       'Warrior', '10', True, ['Sound', 'Blood'], '1,384'),
        ('apex umbril',         'Warrior', '22', True, ['Sight', 'Magic'], '1,384'),
        ('apex vodoriga',       'Warrior', '12', True, ['Sight'], None),
        ('disheveled naraka',   'Warrior', '2',  True, ['Sound', 'Blood'], '1,384'),
        ('enigmatic vampyr',    'Warrior', '1',  True, ['Sight', 'Sound', 'Blood'], '1,384'),
        ('inimical corse',      'Black Mage', '2', True, ['Sound', 'Blood'], '1,384'),
        ('powercrazed dvergr',  'Black Mage', '2', True, ['Sight', 'Magic'], '1,359'),
    ]),
    ('Promyvion-Mea', '139-142', [
        ('apex idle drifter',   'Warrior', None, True, ['True Sound'], None),
        ('apex woeful lamenter','Warrior', None, True, ['True Sound'], '1,542'),
        ('apex livid rager',    'Warrior', None, True, ['True Sound'], '1,542'),
    ]),
    ('Promyvion-Holla', '139-142', [
        ('apex idle drifter',   'Warrior', None, True, ['True Sound'], None),
        ('apex woeful lamenter','Warrior', None, True, ['True Sound'], '1,542'),
        ('apex livid rager',    'Warrior', None, True, ['True Sound'], '1,542'),
    ]),
    ('Promyvion-Dem', '139-142', [
        ('apex idle drifter',   'Warrior', None, True, ['True Sound'], None),
        ('apex woeful lamenter','Warrior', None, True, ['True Sound'], '1,542'),
        ('apex livid rager',    'Warrior', None, True, ['True Sound'], '1,542'),
    ]),
    ('Promyvion-Vahzl', '139-142', [
        ('apex idle drifter',   'Warrior', None, True, ['True Sound'], None),
        ('apex woeful lamenter','Warrior', None, True, ['True Sound'], '1,542'),
        ('apex livid rager',    'Warrior', None, True, ['True Sound'], '1,542'),
    ]),
    ('Alzadaal Undersea Ruins', '143-145', [
        ('apex archaic cog',    'Warrior', '18', True, ['True Sound', 'Magic'], '1,591'),
    ]),
    ('Alzadaal Undersea Ruins', '146-147', [
        ('apex archaic cogs',   'Warrior', '18', True, ['True Sound', 'Magic'], '1,668'),
    ]),
    ('Crawlers Nest [S]', None, [
        ('apex lugcrawler',        'Warrior', '2',  True, ['Sound'], '1,143'),
        ('locus lugcrawler',       'Warrior', '1',  True, ['Sound'], None),
        ('apex hornfly',           'Warrior', '41', True, ['Sound'], '1,203'),
        ('locus hornfly',          'Warrior', None, True, ['Sound'], None),
        ('apex worker lugcrawler', 'Warrior', '27', True, ['Sound'], '1,233'),
        ('locus worker lugcrawler','Warrior', None, True, ['Sound'], None),
        ('apex nest elytra',       'Paladin', '6',  True, ['Sight'], '1,233'),
        ('locus nest elytra',      'Paladin', None, True, ['Sight'], None),
        ('apex dragonfly',         'Warrior', '33', True, ['Sound'], '1,264'),
        ('locus dragonfly',        'Warrior', None, True, ['Sound'], None),
        ('apex soldier lugcrawler','Warrior', '4',  True, ['Sound'], '1,294'),
        ('apex blazer elytra',     'Paladin', '28', True, ['Sight'], '1,294'),
        ('locus blazer elytra',    'Paladin', None, True, ['Sight'], None),
        ('apex mycelar',           'Warrior', '25', True, ['Sound'], '1,354'),
        ('apex rumble lugcrawler', 'Warrior', '6',  True, ['Sound'], '1,354'),
        ('apex helm elytra',       'Paladin', '12', True, ['Sight'], '1,354'),
        ('apex doom scorpion',     'Warrior', '6',  True, ['Sound'], '1,354'),
        ('apex lugcrawler hunter', 'Warrior', '6',  True, ['Sound'], '1,384'),
        ('apex knight lugcrawler', 'Warrior', '6',  True, ['Sound'], '1,423'),
        ('apex water elemental',   'Black Mage', '2', True, ['Magic'], '1,182'),
        ('apex fire elemental',    'Black Mage', '2', True, ['Magic'], '1,182'),
    ]),
    # ---- Locus zones (per-row level ranges) ----
    ('Bhaflau Thickets', '133-135', [
        ('locus colibri',       'Red Mage', '50', False, None, '1,273'),
    ]),
    ('Bhaflau Thickets', '135-137', [
        ('locus wivre',         'Warrior', '11', False, None, '1,324'),
    ]),
    ('King Ranperres Tomb', '131-133', [
        ('locus tomb worm',     'Black Mage', '10', False, None, '1,203'),
    ]),
    ('King Ranperres Tomb', '133-135', [
        ('locus dire bat',      'Warrior', '90', False, None, '1,264'),
    ]),
    ('King Ranperres Tomb', '134-136', [
        ('locus armet beetle',  'Paladin', '16', False, None, '1,294'),
    ]),
    ('King Ranperres Tomb', '135-137', [
        ('locus cutlass scorpion', 'Warrior', '12', True, ['Sound'], '1,324'),
        ('locus hati',             'Warrior', '13', True, ['Sound', 'Blood'], '1,324'),
        ('locus spartoi sorcerer', 'Black Mage', '17', True, ['Sound', 'Blood'], '1,300'),
        ('locus spartoi warrior',  'Warrior', '17', True, ['Sound', 'Blood'], '1,324'),
        ('locus thousand eyes',    'Warrior', '10', True, ['Sound'], '1,324'),
    ]),
    ('King Ranperres Tomb', '137-138', [
        ('locus lemures',       'Black Mage', '2', True, ['Sound', 'Blood'], '1,324'),
    ]),
    ('Bibiki Bay', '135-137', [
        ('locus camelopard',    'Warrior', '22', False, None, '1,324'),
        ('locus hypnos eft',    'Warrior', '23', False, None, '1,324'),
        ('locus bight rarab',   'Warrior', '12', False, None, '1,324'),
    ]),
    ('Bibiki Bay', '137-139', [
        ('locus ghost crab',    'Rune Fencer', '64', False, None, '1,412'),
        ('locus fiddler crab',  'Rune Fencer', None, True, None, '1,412'),
    ]),
    ('Caedarva Mire', '134-136', [
        ('locus imp',           'Black Mage', '40', True, None, None),
    ]),
]

# New records to create, cloned from their Apex sibling (family kit + grid).
CREATE = {
    'locus lugcrawler':        ('Locus Lugcrawler', 'apex lugcrawler'),
    'locus hornfly':           ('Locus Hornfly', 'apex hornfly'),
    'locus worker lugcrawler': ('Locus Worker Lugcrawler', 'apex worker lugcrawler'),
    'locus nest elytra':       ('Locus Nest Elytra', 'apex nest elytra'),
    'locus dragonfly':         ('Locus Dragonfly', 'apex dragonfly'),
    'locus blazer elytra':     ('Locus Blazer Elytra', 'apex blazer elytra'),
}
CLONE_KEYS = ('fam', 'ab', 'crys', 'wk', 'st', 'im', 'ab_el', 'img', 'lnk')

# Family stamps for the King Ranperre's Tomb orphans (fam taken from the base mob's record).
ORPHAN_STAMP = {
    'locus hati':             ('hati',            ['fam', 'crys', 'ab', 'im']),
    'locus lemures':          ('lemures',         ['fam', 'crys', 'ab', 'im']),
    'locus spartoi warrior':  ('spartoi warrior', ['fam', 'crys', 'ab', 'im']),
    'locus spartoi sorcerer': ('spartoi warrior', ['fam', 'crys', 'ab', 'im']),
    'locus thousand eyes':    ('thousand eyes',   ['fam', 'crys', 'ab']),
}

# Per-mob level fixes the tables establish outright.
LEVELS = {
    'apex eruca': [125, 127],
    'apex archaic cog': [143, 145],
    'apex archaic cogs': [146, 147],
    'apex idle drifter': [139, 142],
    'apex woeful lamenter': [139, 142],
    'apex livid rager': [139, 142],
    'locus lemures': [137, 138],
    'locus camelopard': [135, 137],
    'locus bight rarab': [135, 137],
}

# Free-text notes that are genuinely player-facing (behaviour, not provenance).
EXTRA_NOTES = {
    'apex bat': ['Does not aggro or link.'],
    'apex twitherym': ['Does not aggro or link.'],
    'apex ironclad': ['Aggros from 10\u2032 by sound and 7.5\u2032 by sight.'],
    'apex jagil': ['Aggressive in Dho Gates; does not aggro in Sih Gates or Woh Gates.'],
    'apex water elemental': ['Only spawns during weather.'],
    'apex fire elemental': ['Only spawns during weather.'],
    'apex idle drifter': ['Gains elemental weaknesses and resistances from its Core colour.',
                          'Level does not scale with how high a floor you climb to.'],
    'apex vodoriga': ['1,384 accuracy for a 95% hit rate on the ground, 1,454 while flying.'],
    'apex draugar': ['95% hit rate: 1,359 vs the Black Mage, 1,384 vs the Dark Knight, 1,524 vs the Thief.'],
    'locus imp': ['95% hit rate: 1,211 at Lv134, 1,242 at Lv135, 1,271 at Lv136.'],
    'locus fiddler crab': ['Lottery spawn off Locus Ghost Crab.'],
}

created, stamped, touched = [], [], set()

# ---------------------------------------------------------------- create
for key, (name, src) in CREATE.items():
    if key in M:
        continue
    base = M[src]
    rec = {'n': name}
    for k in CLONE_KEYS:
        if k in base and base[k] is not None:
            rec[k] = json.loads(json.dumps(base[k]))
    M[key] = rec
    created.append(key)

# ---------------------------------------------------------------- orphan family stamp
for key, (src, fields) in ORPHAN_STAMP.items():
    m, base = M[key], M[src]
    for f in fields:
        if f in base and base[f] is not None and not m.get(f):
            m[f] = json.loads(json.dumps(base[f]))
            touched.add(key)
    stamped.append((key, m.get('fam')))

# ---------------------------------------------------------------- table apply
def add_zone(m, zone, band):
    zs = m.get('zones') or []
    for z in zs:
        if z[0] == zone:
            if band:
                if len(z) == 1:
                    z.append(band)
                else:
                    z[1] = band
            return
    zs.append([zone, band] if band else [zone])
    m['zones'] = zs

def add_note(m, text):
    ns = m.get('notes') or []
    if text not in ns:
        ns.append(text)
    m['notes'] = ns

multi = {}
for zone, band, rows in TABLES:
    for key, *_ in rows:
        multi[key] = multi.get(key, 0) + 1

for zone, band, rows in TABLES:
    for key, job, spawns, agg, det, acc in rows:
        m = M.get(key)
        if m is None:
            print('!! missing record:', key)
            continue
        touched.add(key)
        add_zone(m, zone, band)
        if job and not m.get('job'):
            m['job'] = job
        if agg is True:
            m['agg'] = True
        elif agg is False:
            m.pop('agg', None)          # page marks it explicitly non-aggressive
        if det:
            m['det'] = list(det)        # the table enumerates detection in full
        # spawn-count / accuracy bullet
        bits = []
        if spawns:
            bits.append('%s spawn%s' % (spawns, '' if spawns == '1' else 's'))
        if acc:
            bits.append('%s accuracy for a 95%% hit rate' % acc)
        if bits:
            line = ', '.join(bits) + '.'
            line = line[0].upper() + line[1:]
            add_note(m, ('%s: %s' % (zone, line)) if multi[key] > 1 else line)

# ---------------------------------------------------------------- level + extra notes
for key, lv in LEVELS.items():
    M[key]['lv'] = lv
    touched.add(key)
for key, notes in EXTRA_NOTES.items():
    for n in notes:
        add_note(M[key], n)
    touched.add(key)

# ---------------------------------------------------------------- guards
bad = [k for k, m in M.items() for kk, v in m.items() if v is None]
assert not bad, bad
for k in touched:
    m = M[k]
    for z in (m.get('zones') or []):
        assert isinstance(z, list) and 1 <= len(z) <= 2 and all(isinstance(x, str) for x in z), (k, z)

json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

al = [k for k in M if k.startswith('apex ') or k.startswith('locus ')]
nz = [k for k in al if not (M[k].get('zones'))]
nl = [k for k in al if not (M[k].get('lv'))]
print('created %d: %s' % (len(created), ', '.join(created)))
print('family-stamped orphans:', stamped)
print('records touched:', len(touched))
print('apex/locus total: %d | still zoneless: %d | still levelless: %d %s' % (len(al), len(nz), len(nl), sorted(nl)))
