#!/usr/bin/env python3
"""rev 412 — push the Puk repair into OmniWatch's mob_individuals.json.

That file was rebuilt from bestiary rev 409, so it inherited both faults:
`abilities: []` on 20 of the 24 Puks, and the swapped element cells
(modifiers.lightning 1.3 + absorbs Ice, where the page reads Ice 130% and a
WIND absorb).  Its family fallback list was seeded from the older
mob_abilities scrape and never had Zephyr Mantle, White Wind or Somnial
Durance.

!! THIS EDITS THE TEXT, NOT THE PARSED OBJECT. !!  mob_individuals.json is
written by OmniWatch's own pretty-printer (2-space indent, CRLF, containers
inline up to ~110 columns, numeric dicts and string lists packed greedily to
96 columns).  Re-serialising with json.dump would reformat all 258,000 lines
and bury a 24-record change in a whole-file diff.  So every edit here is a
line replacement, and the guard at the bottom re-parses the result and
compares it against the object the edits were supposed to produce.

Idempotent — safe to re-run over its own output.

Usage: proc_rev412_puk_omniwatch2.py <mob_individuals.json> <mobs.json>

Author: BalladOfWorms
"""
import json, sys, copy
from datetime import date

OW, MOBS = sys.argv[1], sys.argv[2]
INLINE_MAX, PACK_WIDTH = 110, 96

raw = open(OW, encoding='utf-8', newline='').read()
lines = raw.split('\r\n')
assert len(lines) > 100000, 'expected CRLF line endings'

obj = json.loads(raw)
want = copy.deepcopy(obj)                      # the target, built in parallel
src = json.load(open(MOBS, encoding='utf-8'))['mobs']
puks = {k: v for k, v in src.items() if v.get('fam') == 'Puk'}
assert len(puks) == 24, len(puks)


# ----------------------------------------------------------------- rendering
def _pack(items, ind):
    out, cur = [], ''
    for i, it in enumerate(items):
        piece = it + (',' if i < len(items) - 1 else '')
        cand = (cur + ' ' + piece) if cur else piece
        if len(ind) + len(cand) <= PACK_WIDTH:
            cur = cand
        else:
            out.append(ind + cur)
            cur = piece
    out.append(ind + cur)
    return out


def render(key, value, indent, comma):
    """Render `"key": value` the way this file's writer would."""
    tail = ',' if comma else ''
    ind = ' ' * indent
    inline = ind + json.dumps(key, ensure_ascii=False) + ': ' \
        + json.dumps(value, ensure_ascii=False, separators=(', ', ': ')) + tail
    if len(inline) <= INLINE_MAX:
        return [inline]
    if isinstance(value, dict):
        items = ['%s: %s' % (json.dumps(k, ensure_ascii=False),
                             json.dumps(v, ensure_ascii=False)) for k, v in value.items()]
        open_c, close_c = '{', '}'
    else:
        items = [json.dumps(v, ensure_ascii=False) for v in value]
        open_c, close_c = '[', ']'
    head = ind + json.dumps(key, ensure_ascii=False) + ': ' + open_c
    return [head] + _pack(items, ' ' * (indent + 2)) + [ind + close_c + tail]


def block(start, indent):
    """Index one past the last line of the container opened on line `start`."""
    close = ' ' * indent + '}'
    i = start + 1
    while not lines[i].startswith(close) and not lines[i].startswith(' ' * indent + ']'):
        i += 1
    return i


def find(text, after=0):
    for i in range(after, len(lines)):
        if lines[i] == text:
            return i
    raise KeyError(text)


def replace_field(rec_start, rec_end, key, value, indent):
    """Swap the `key` field inside a record for a freshly rendered one."""
    head = ' ' * indent + json.dumps(key) + ': '
    for i in range(rec_start, rec_end):
        if lines[i].startswith(head):
            end = i + 1
            if not lines[i].rstrip().endswith((',', '}', ']')) or lines[i].rstrip().endswith(('[', '{')):
                end = block(i, indent) + 1
            comma = lines[end - 1].rstrip().endswith(',')
            lines[i:end] = render(key, value, indent, comma)
            return
    raise KeyError(key)


# --------------------------------------------------------- 1. the 24 records
ind_start = find('  "individuals": {')
kits = grids = 0
for key, m in sorted(puks.items()):
    s = find('    %s: {' % json.dumps(key, ensure_ascii=False), ind_start)
    e = block(s, 4)
    rec = obj['individuals'][key]
    tgt = want['individuals'][key]

    if rec['abilities'] != m['ab']:
        tgt['abilities'] = list(m['ab'])
        replace_field(s, e, 'abilities', tgt['abilities'], 6)
        kits += 1

    mod = dict(rec['modifiers'])
    if mod.get('lightning') == 1.3 and mod.get('ice') == 1.0:
        mod['lightning'], mod['ice'] = 1.0, 1.3
    if key == "amymone's peapuk" and mod.get('piercing') == 1.25:
        # still the pre-rev-68 junk stamp; give it the family grid
        mod.update({'piercing': 1.125, 'ranged': 1.125, 'fire': 1.15, 'ice': 1.3,
                    'earth': 1.15, 'water': 1.15, 'light': 1.15, 'dark': 1.15})
    if mod != rec['modifiers']:
        tgt['modifiers'] = mod
        replace_field(s, e, 'modifiers', mod, 6)
        grids += 1

    if rec['absorbs'] == ['Ice'] or (key == "amymone's peapuk" and rec['absorbs'] == []):
        tgt['absorbs'] = ['Wind']
        replace_field(s, e, 'absorbs', ['Wind'], 6)

# --------------------------------------------- 2. the family fallback list
fam_start = find('  "family_abilities": {')
fam = sorted({a for m in puks.values() for a in m['ab']} | {'Somnial Durance'})
if obj['family_abilities']['puk'] != fam:
    want['family_abilities']['puk'] = fam
    replace_field(fam_start, block(fam_start, 2), 'puk', fam, 4)

# ------------------------------------------------- 3. ability_details blocks
det_start = find('  "ability_details": {')
det_end = block(det_start, 2)
LIGHT = 'Light-based (inflicts Flash).'
patches = {
    'Zephyr Mantle':   {'family': 'Puk', 'range': 'Self'},
    'White Wind':      {'family': 'Puk'},
    'Somnial Durance': {'family': 'Puk', 'range': 'AoE'},
}
notes = obj['ability_details']['Obfuscate']['notes']
if LIGHT not in notes:                                   # must no-op on its own output
    patches['Obfuscate'] = {'notes': notes.rstrip('. ') + '. ' + LIGHT}
for name, fields in patches.items():
    s = find('    %s: {' % json.dumps(name), det_start)
    assert s < det_end
    e = block(s, 4)
    for k, v in fields.items():
        want['ability_details'][name][k] = v
        replace_field(s, e, k, v, 6)

# ------------------------------------------------------------------ 4. _meta
if 'patched_from' not in obj['_meta']:
    anchor = find('    "rebuilt_from": %s' % json.dumps(obj['_meta']['rebuilt_from']))
    want['_meta']['patched_at'] = str(date.today())
    want['_meta']['patched_from'] = 'MobileWatch bestiary rev 412 (Puk kit + element-row fix)'
    lines[anchor] = lines[anchor].rstrip(',') + ','
    lines[anchor + 1:anchor + 1] = [
        '    "patched_at": %s,' % json.dumps(want['_meta']['patched_at']),
        '    "patched_from": %s' % json.dumps(want['_meta']['patched_from']),
    ]
    if lines[anchor].endswith(',') and not lines[anchor + 3].strip().startswith('}'):
        pass

# ----------------------------------------------------------------- 5. guards
out = '\r\n'.join(lines)
got = json.loads(out)                                   # syntax check
assert got == want, 'patched text does not match the intended object'
old = raw.split('\r\n')
changed = sum(1 for a, b in zip(old, lines) if a != b) + abs(len(lines) - len(old))
# only OUR lines have to obey the width rule — long single strings elsewhere cannot wrap
touched = set(lines) - set(old)
over = [l for l in touched if len(l) > INLINE_MAX]
assert not over, over[:3]
for k, v in got['individuals'].items():                 # nothing outside the family moved
    if v.get('family') != 'Puk':
        assert v == obj['individuals'][k], k

open(OW, 'w', encoding='utf-8', newline='').write(out)
print('kits set %d · grids corrected %d · lines touched ~%d' % (kits, grids, changed))
print('family list:', fam)
