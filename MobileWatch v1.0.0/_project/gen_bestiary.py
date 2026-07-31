#!/usr/bin/env python3
"""
gen_bestiary.py — the whole bestiary as ONE readable, editable file.

Written rev 396, replacing the two bucket-review docs as the thing that ships
beside the zip. Output: MobileWatch-Bestiary.md

FORMAT RULES (keep these if you regenerate):
  - one fact per line, `- Label: value`, so any line can be edited or grepped
    without disturbing its neighbours
  - empty fields are OMITTED, never printed as "none" — absent means unrecorded
  - nothing is abbreviated or truncated; this file is the full record
  - ecosystem > family > mob, matching the app's own Family view
"""
import json, os, sys, collections
from datetime import date

ASSETS = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'MobileWatch-Bestiary.md'
d = json.load(open(os.path.join(ASSETS, 'mobs.json'), encoding='utf-8'))
M, A, FE = d['mobs'], d['abilities'], d['family_eco']
FN = d.get('family_notes', {})
SETS = d.get('family_resist_sets', {})

L = []
def w(s=''):
    L.append(s)

# --------------------------------------------------------------------- header
fams = sorted({m['fam'] for m in M.values()})
ecos = sorted({FE.get(f, 'Unclassified') for f in fams})
nm = sum(1 for m in M.values() if m.get('nm'))
zoned = sum(1 for m in M.values() if m.get('zones'))
used_ab = {a for m in M.values() for a in (m.get('ab') or [])}

w('# MobileWatch — the complete bestiary')
w()
w(f'Generated {date.today().isoformat()} from `mobs.json`. '
  f'**{len(M):,} monsters** across **{len(fams)} families** in **{len(ecos)} ecosystems**, '
  f'**{len(A):,} ability definitions**. {nm:,} are flagged notorious monsters; '
  f'{zoned:,} have at least one zone recorded.')
w()
w('This is the whole record in one file — nothing here is summarised or truncated. '
  'Part 1 is every ability definition, Part 2 is every monster.')
w()
w('## How to read it')
w()
w('**Resistances.** A number is the difference from neutral, the way the wiki writes it minus 100. '
  '`Fire +50%` means the wiki says 150% damage taken. `Ice -50%` means 50%. A weakness or resistance '
  'with **no number** is a direction the source stated without a magnitude — treat it as "weak" or '
  '"resistant" and nothing more.')
w()
w('**Damage types** are Physical, Magical, Breath, Slashing, Impact, H2H, Piercing and Ranged. '
  'Note the app draws Impact under the label **Blunt**; the data says `Impact`. A handful of families '
  'with a swipeable multi-element grid store the same row as `Blunt` so it matches their resist set — '
  'those are noted on the family.')
w()
w('**Detection** vocabulary: `Sight`, `Sound`, `Scent`, `Magic`, `JA` (job abilities), '
  '`Blood` (low HP — almost always an undead family), `True Sight` and `True Sound`. '
  '`True Sight` and `True Sound` see through Invisible and Sneak respectively.')
w()
w('**Flags.** `NM` notorious monster · `Aggressive` attacks on sight · `Links` calls its neighbours.')
w()
w('**Crystal** is the crystal the mob drops. `Varies` means it follows the mob\'s own element '
  '(the Aern, Ghrah and Craver classes); `None` means the page states it drops none.')
w()
w('**Zones** are `Zone (level band)`, semicolon separated. A zone with no band means the level '
  'was never recorded for that zone specifically.')
w()
w('**Absent fields are absent, not empty.** If a monster has no `Drops` line, nothing is recorded — '
  'it does not mean it drops nothing.')
w()
w('---')
w()

# ------------------------------------------------------- part 1: abilities
w('# Part 1 — Ability reference')
w()
w(f'{len(A):,} definitions, alphabetical. `Used by` counts the monsters whose ability list names it; '
  'a definition used by 0 monsters is still here because something else may reference it.')
w()
usage = collections.Counter(a for m in M.values() for a in (m.get('ab') or []))
for name in sorted(A, key=lambda x: x.lower()):
    v = A[name] if isinstance(A[name], dict) else {}
    w(f'### {name}')
    if v.get('d'):
        w(v['d'])
        w()
    bits = []
    if v.get('t'):   bits.append(f"Type: {v['t']}")
    if v.get('el'):  bits.append(f"Element: {v['el']}")
    if v.get('tgt'): bits.append(f"Target: {v['tgt']}")
    if v.get('r'):   bits.append(f"Range: {v['r']}")
    if bits:
        w('- ' + ' · '.join(bits))
    if v.get('fx'):
        w('- Effects: ' + ', '.join(v['fx']))
    if v.get('notes'):
        w('- Notes: ' + str(v['notes']))
    _u = usage.get(name, 0)
    w(f'- Used by: {_u} monster' + ('' if _u == 1 else 's'))
    w()

# undefined references, so the gap is visible in the same file
undef = collections.Counter(a for m in M.values() for a in (m.get('ab') or []) if a not in A)
if undef:
    w('### (names used by monsters with no definition here)')
    w()
    w('These are player job abilities and weapon skills that a monster genuinely uses; they are '
      'defined in the job and weapon-skill data rather than the ability table.')
    w()
    for n, c in sorted(undef.items()):
        w(f'- **{n}** — used by {c} monster' + ('s' if c != 1 else ''))
    w()

w('---')
w()

# ------------------------------------------------------- part 2: the bestiary
w('# Part 2 — The bestiary')
w()

def grid(rows):
    out = []
    for e in (rows or []):
        out.append(e[0] if len(e) < 2 or e[1] is None else f'{e[0]} {e[1]}')
    return ', '.join(out)

def zonetext(zs):
    out = []
    for z in (zs or []):
        name = z[0]
        band = z[1] if len(z) > 1 and z[1] else None
        out.append(f'{name} ({band})' if band else name)
    return '; '.join(out)

by_eco = collections.defaultdict(list)
for f in fams:
    by_eco[FE.get(f, 'Unclassified')].append(f)

for eco in sorted(by_eco):
    famlist = sorted(by_eco[eco])
    total = sum(1 for m in M.values() if m['fam'] in famlist)
    w(f'## Ecosystem: {eco}')
    w()
    w(f'{len(famlist)} famil' + ('ies' if len(famlist) != 1 else 'y') +
      f', {total:,} monsters — ' + ', '.join(famlist))
    w()
    for fam in famlist:
        members = sorted((k for k, m in M.items() if m['fam'] == fam),
                         key=lambda k: M[k]['n'].lower())
        w(f'### Family: {fam}')
        w()
        w(f'*Ecosystem {eco} · {len(members)} recorded*')
        w()
        if fam in SETS:
            labels = [s.get('label') for s in SETS[fam]]
            w(f'*Swipeable resist grid — {len(labels)} sets: ' + ', '.join(str(x) for x in labels) +
              '. Members whose grid matches a set show all of them; the rest show their own.*')
            w()
        for b in (FN.get(fam) or []):
            w(f'> {b}')
        if FN.get(fam):
            w()
        for k in members:
            m = M[k]
            w(f'#### {m["n"]}')
            lv = m.get('lv')
            if lv:
                w(f'- Level: {lv[0]}' + (f'-{lv[1]}' if lv[0] != lv[1] else ''))
            flags = []
            if m.get('nm'):  flags.append('NM')
            if m.get('agg'): flags.append('Aggressive')
            if m.get('lnk'): flags.append('Links')
            if flags:
                w('- Flags: ' + ', '.join(flags))
            if m.get('det'):   w('- Detects: ' + ', '.join(m['det']))
            if m.get('job'):   w(f"- Job: {m['job']}")
            if m.get('crys'):  w(f"- Crystal: {m['crys']}")
            if m.get('resp'):  w(f"- Respawn: {m['resp']}s")
            if m.get('wk'):    w('- Weak to: ' + grid(m['wk']))
            if m.get('st'):    w('- Resists: ' + grid(m['st']))
            if m.get('im'):    w('- Immune: ' + ', '.join(m['im']))
            if m.get('ab_el'): w('- Absorbs: ' + ', '.join(m['ab_el']))
            if m.get('ab'):    w('- Abilities: ' + ', '.join(m['ab']))
            if m.get('sp'):    w('- Spells: ' + ', '.join(m['sp']))
            if m.get('zones'): w('- Zones: ' + zonetext(m['zones']))
            if m.get('content'): w('- Content: ' + '; '.join(m['content']))
            if m.get('spawn'): w(f"- Spawn: {m['spawn']}")
            if m.get('drops'): w(f"- Drops: {m['drops']}")
            if m.get('img'):   w(f"- Image: {m['img']}")
            if m.get('notes'):
                w('- Notes:')
                for b in m['notes']:
                    w(f'    - {b}')
            w()

open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
size = os.path.getsize(OUT)
print(f'{OUT}: {len(L):,} lines, {size/1024/1024:.1f} MB')
print(f'  {len(M):,} monsters, {len(A):,} abilities, {len(fams)} families, {len(ecos)} ecosystems')
