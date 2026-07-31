#!/usr/bin/env python3
"""Vagary content tagging (rev 249).

USER: "vagary, new entry in content. banner needs white strip cropped off left side. mobs get
bestiary link"

Source: BG-wiki Category:Vagary (user screenshots). Tags the ten Vagary NMs so the guide page can
link them, normalizes the instanced-zone string (the page: "Vagary occurs in the instanced zone:
Outer Ra'Kaznar (U)"), adds Ra'Kaznar Turris for the five Alternative Battlefield bosses (Oct 2018),
and fills the two Rancibus materials the record was missing.

Tag shape Group: Section: Role -> Section = the gate (or "Additional NMs"), Role = the armor slot
for a Mega Boss and the wave/tier for everything else.
"""
import json, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']

ZONE = "Outer Ra'Kaznar [U]"
TURRIS = 'RaKaznar Turris'          # zones.json spelling
OLD_ZONES = ('Outer RaKaznar', ZONE)  # the non-instanced form some records carried

TAGS = {
    # Mega Bosses — role is the Reforged Empyrean slot they unlock
    'palloritus':    ('Vagary: Deathborne Gate: Head',  True),
    'putraxia':      ('Vagary: Duskbrood Gate: Hands',  True),
    'rancibus':      ('Vagary: Brash Gate: Feet',       True),
    'perfidien':     ('Vagary: Additional NMs: Legs',   True),
    'plouton':       ('Vagary: Additional NMs: Body',   True),
    # wave / tier NMs
    'lightreaper':   ('Vagary: Deathborne Gate: Wave 2', False),
    'blightslither': ('Vagary: Duskbrood Gate: Tier I',  False),
    'insidivo':      ('Vagary: Duskbrood Gate: Tier II', False),
    'murkcrawler':   ('Vagary: Brash Gate: Tier I',      False),
    'brimboil':      ('Vagary: Brash Gate: Tier II',     False),
}

# Rancibus published its two Mega Boss materials but the record held only the gear.
EXTRA_DROPS = {'rancibus': ['Plovid Effluvium', 'Plovid Flesh']}

items = json.load(open(P.replace('mobs.json', 'ffxi_items.json'), encoding='utf-8'))
src = items.get('items') if isinstance(items, dict) and 'items' in items else (
    items.values() if isinstance(items, dict) else items)
NAMES = {v['n'] for v in src if isinstance(v, dict) and 'n' in v}

missing, out = [], []
for k, (tag, mega) in TAGS.items():
    m = M.get(k)
    if m is None:
        missing.append(k)
        continue
    c = m.get('content') or []
    if tag not in c:
        c.append(tag)
    m['content'] = c
    m['nm'] = True
    # zones: one instanced-zone entry, level kept; Turris added for the alt-battlefield bosses
    lvl = None
    for z in (m.get('zones') or []):
        if z[0] in OLD_ZONES and len(z) > 1:
            lvl = z[1]
    lvl = lvl or (str(m['lv'][0]) if m.get('lv') else None)
    zs = [z for z in (m.get('zones') or []) if z[0] not in OLD_ZONES and z[0] != TURRIS]
    zs.append([ZONE, lvl] if lvl else [ZONE])
    if mega:
        zs.append([TURRIS, lvl] if lvl else [TURRIS])
    m['zones'] = zs
    out.append((k, tag, m['zones']))

for k, extra in EXTRA_DROPS.items():
    good = [n for n in extra if n in NAMES]
    bad = [n for n in extra if n not in NAMES]
    cur = [s.strip() for s in (M[k].get('drops') or '').split(',') if s.strip()]
    M[k]['drops'] = ', '.join(good + [c for c in cur if c not in good])
    print('drops %s -> %s%s' % (k, M[k]['drops'], '   (not in item DB: %s)' % bad if bad else ''))

assert not [kk for mm in M.values() for kk, v in mm.items() if v is None]
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

print('missing:', missing or '(none)')
print('tagged %d:' % len(out))
for k, tag, zs in out:
    print('  %-14s %-34s %s' % (k, tag, zs))
