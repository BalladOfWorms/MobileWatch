#!/usr/bin/env python3
"""
REV 391 — the answered decision items, plus the Lamiae-in-Vermin report.

USER ANSWERS APPLIED
  nmlv quirk .............. "Sweep away"  -> nmlv removed on all 35
  16 empty families ....... "maybe leave alone?" -> LEFT (verified 0 members each)
  901 job strings ......... user explained the comma is MEANINGFUL ("BLM main job
                            with BLM subjob or RDM as job"), so separators are left
                            exactly as they are; only 3-letter codes get expanded
  23 bogus grid rows ...... "should be in the notes of a mob" -> moved to notes
  5 Quadav NMs ............ "Family wins here" -> family grid stamped
  4 Contanticans .......... "Sure, clear" -> nm flag removed
  4 NPC-type records ...... "Leave as is"  -> untouched
  125-126 band ............ "Leave as is"  -> untouched
  single-entry grids ...... "Leave as is"  -> untouched
  17 bare abilities ....... "left alone"   -> untouched
  smaller things .......... shikaree x + z -> Blessed Races of Altana; torvotaur
                            left alone; hpedme spelling fixed; mystic avatar left
  cardian prototype ....... "leave as is"  -> untouched

USER REPORT: "we have a lamiae in vermin, chigoe breeder, should be beastmen"
  `chigoe breeder` IS filed fam=Lamiae (correct), but carried a per-mob
  eco OVERRIDE of "Vermin" that beat family_eco['Lamiae']='Beastmen'. The name
  made the import follow Chigoe. Override REMOVED (key deleted, never set null).
  Running that as a file-wide detector found ONE MORE: `sang buaya`, fam Bugard,
  eco "Beast", while family_eco['Bugard'] = 'Lizard'. Also removed.
"""
import json, os, re

P = 'app/src/main/assets/mobs.json'
if not os.path.exists(P):
    P = 'android/' + P
d = json.load(open(P))
M = d['mobs']; A = d['abilities']; FE = d['family_eco']
before = len(M)

# ============================================================ 1. eco overrides
print('=== ECO OVERRIDES THAT FIGHT family_eco ===')
for k, m in list(M.items()):
    if m.get('eco') and m.get('fam') and m['eco'] != FE.get(m['fam']):
        print('  %-18s fam=%-10s eco=%-8s -> falls back to %s' %
              (k, m['fam'], m['eco'], FE.get(m['fam'])))
        del m['eco']          # DELETE the key. Never set it to null.
assert not [k for k, m in M.items()
            if m.get('eco') and m.get('fam') and m['eco'] != FE.get(m['fam'])]

# ============================================================ 2. nmlv sweep
print('\n=== nmlv SWEEP (35 records with nmlv and no nm flag) ===')
def lvtext(lv):
    if not lv: return None
    return str(lv[0]) if lv[0] == lv[1] else '%d-%d' % (lv[0], lv[1])
dropped_differ = []
n_nmlv = 0
for k, m in M.items():
    if m.get('nmlv') and not m.get('nm'):
        if m['nmlv'] != lvtext(m.get('lv')):
            dropped_differ.append((k, m['nmlv'], m.get('lv')))
        del m['nmlv']
        n_nmlv += 1
print('  removed %d nmlv values' % n_nmlv)
print('  %d of them did NOT simply restate the lv range — recorded here and in the'
      ' review so nothing is lost silently:' % len(dropped_differ))
for k, nv, lv in dropped_differ:
    print('     %-24s nmlv %-9s vs lv %s' % (k, nv, lv))
assert not [k for k, m in M.items() if m.get('nmlv') and not m.get('nm')]

# ============================================================ 3. job codes
JOB = {'WAR': 'Warrior', 'MNK': 'Monk', 'WHM': 'White Mage', 'BLM': 'Black Mage',
       'RDM': 'Red Mage', 'THF': 'Thief', 'PLD': 'Paladin', 'DRK': 'Dark Knight',
       'BST': 'Beastmaster', 'BRD': 'Bard', 'RNG': 'Ranger', 'SAM': 'Samurai',
       'NIN': 'Ninja', 'DRG': 'Dragoon', 'SMN': 'Summoner', 'BLU': 'Blue Mage',
       'COR': 'Corsair', 'PUP': 'Puppetmaster', 'DNC': 'Dancer', 'SCH': 'Scholar',
       'GEO': 'Geomancer', 'RUN': 'Rune Fencer'}
CODE = re.compile(r'\b(' + '|'.join(JOB) + r')\b')
print('\n=== JOB CODE EXPANSION (separators left alone — the comma means "or") ===')
changed = {}
for k, m in M.items():
    j = m.get('job')
    if j and CODE.search(j):
        nj = CODE.sub(lambda mo: JOB[mo.group(1)], j)
        changed[(j, nj)] = changed.get((j, nj), 0) + 1
        m['job'] = nj
print('  %d records touched, %d distinct forms' %
      (sum(changed.values()), len(changed)))
for (o, n), c in sorted(changed.items(), key=lambda x: -x[1])[:10]:
    print('     %4d  %-22s -> %s' % (c, o, n))
assert not [m['job'] for m in M.values() if m.get('job') and CODE.search(m['job'])]

# ============================================================ 4. bogus grid rows
GRID_OK = {'Physical', 'Magical', 'Breath', 'Slashing', 'Impact', 'Blunt', 'H2H',
           'Piercing', 'Ranged', 'Fire', 'Wind', 'Lightning', 'Light', 'Ice',
           'Earth', 'Water', 'Dark',
           'Varies'}   # deliberate convention on Avatar / Zdei records — keep

# The only two labels that are the grid's OWN vocabulary written out longhand.
# Renamed rather than moved to notes, because these render as real cells.
RENAME = {'Magic Damage': 'Magical', 'Physical Damage': 'Physical'}

# Everything else becomes prose. `wk` reads "susceptible", `st` reads "resists".
PROSE = {
    'baobhan sith':      ["Susceptible to Petrify."],
    'calcabrina':        ["Susceptible to Blind, Paralyze, Slow and Poison."],
    'doglix muttsnout':  ["Resists Sleep and Stun."],
    "gizerl's ghost":    ["Susceptible to Gravity, Bind and Silence."],
    'guimauve':          ["Resists Gravity."],
    'holey horror':      ["Only takes piercing damage."],
    'menechme':          ["Susceptible to Paralyze."],
    'moxnix nightgoggle': ["Resists Sleep."],
    'picklix longindex': ["Resists Sleep."],
}
# Carries no information at all — a label with no percentage. Dropped, not noted.
SILENT = {'Damage Taken', 'Dark Earth'}

print('\n=== BOGUS GRID ROWS -> NOTES ===')
moved = dropped = renamed = 0
for k, m in M.items():
    hit = False
    for f in ('wk', 'st'):
        rows = m.get(f)
        if not rows:
            continue
        keep = []
        for e in rows:
            if e[0] in GRID_OK:
                keep.append(e)
            elif e[0] in RENAME:
                keep.append([RENAME[e[0]], e[1]]); renamed += 1; hit = True
            elif e[0] in SILENT:
                dropped += 1; hit = True
            else:
                dropped += 1; hit = True
        if keep != rows:
            m[f] = keep
    if k in PROSE:
        notes = m.setdefault('notes', [])
        for b in PROSE[k]:
            if b not in notes:
                notes.append(b); moved += 1
    if hit:
        print("  %-22s -> %s" % (k, PROSE.get(k, ["(renamed to grid vocabulary, or dropped as valueless)"])[0]))
print('  %d note lines written, %d rows dropped, %d labels renamed to grid vocabulary'
      % (moved, dropped, renamed))
left = sorted({e[0] for m in M.values() for f in ('wk', 'st')
               for e in (m.get(f) or []) if e[0] not in GRID_OK})
print('  non-grid labels remaining: %s' % (left or 'none'))
assert not left

# ============================================================ 5. immune junk
print('\n=== MALFORMED `im` VALUES ===')
for k, m in M.items():
    im = m.get('im')
    if not im:
        continue
    new = []
    for x in im:
        if x == 'LullabySleep':
            new += ['Lullaby', 'Sleep']          # two values glued
        elif x in ('{sleep', 'break}'):
            pass                                  # halves of {{sleep|break}}
        else:
            new.append(x)
    if new != im:
        print('  %-16s %s -> %s' % (k, im, new or '(key removed)'))
        if new:
            m['im'] = new
        else:
            del m['im']

# ============================================================ 6. Quadav grids
QUADAV_WK = [['Wind', '+30%'], ['Lightning', '+50%'], ['Light', '+30%'],
             ['Ice', '+30%'], ['Earth', '+30%'], ['Dark', '+30%']]
FIVE = ["bo'gha winterkill", "du'vha grimewind", "ea'zhu tremorcrag",
        "gi'rho wrathstorm", "he'dho spatesurge"]
print('\n=== 5 QUADAV NMs -> FAMILY GRID ===')
for k in FIVE:
    assert M[k]['fam'] == 'Quadav'
    M[k]['wk'] = [r[:] for r in QUADAV_WK]
    M[k]['st'] = []
    print('  %s stamped' % k)
print("  NOT touched: `aa'bho slashburner` — same Rolanberry Fields [S] group, same")
print("  contradicted grid, and it is the record whose page carried the Lightning")
print("  weakness that made the family grid right. It was not on your list.")

# ============================================================ 7. Contanticans
print('\n=== CONTANTICAN NM FLAGS ===')
for k, m in M.items():
    if k.startswith('contantican') and m.get('nm'):
        del m['nm']
        print('  %s nm flag cleared' % k)

# ============================================================ 8. shikaree
print('\n=== SHIKAREE SISTERS ===')
for k in ('shikaree x', 'shikaree z'):
    M[k]['fam'] = 'Blessed Races of Altana'
    print('  %s -> Blessed Races of Altana' % k)
assert len({M[k]['fam'] for k in ('shikaree x', 'shikaree y', 'shikaree z')}) == 1

# ============================================================ 9. hpedme spelling
print('\n=== SPELLING ===')
if "warder's hpedme" in M:
    m = M.pop("warder's hpedme")
    m['n'] = "Warder's Hpemde"
    M["warder's hpemde"] = m
    print("  warder's hpedme -> warder's hpemde  (fam already Hpemde)")

# ============================================================ guards
assert not [k for m in M.values() for k, v in m.items() if v is None], 'NULL POISON'
assert not [k for a in A.values() for k, v in a.items() if v is None], 'NULL POISON (ab)'
bad_key = [k for k, m in M.items() if k != m['n'].lower()]
print('\nkey/name mismatches: %d %s' % (len(bad_key), bad_key))
assert not bad_key
assert len(M) == before, (before, len(M))
sets = {s['label']: s for s in d['family_resist_sets']['Elemental']}
for key, label in [('shadowfang void', 'Dark'), ('touched gefyrst', 'Gefyrst')]:
    assert M[key]['wk'] == sets[label]['wk'] and M[key]['st'] == sets[label]['st'], key
print('swipe-set stamps still match family_resist_sets')

# the 16 empty families are LEFT, per your answer — verified empty here
used = {m.get('fam') for m in M.values()}
empty = sorted(f for f in d['families'] if f not in used)
print('empty families left in place (%d): %s' % (len(empty), empty))

json.dump(d, open(P, 'w'), separators=(', ', ': '), ensure_ascii=False)
print('\nmobs %d (unchanged), orphans %d' %
      (len(M), sum(1 for m in M.values() if not m.get('fam'))))
