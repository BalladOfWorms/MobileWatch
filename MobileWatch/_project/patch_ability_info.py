#!/usr/bin/env python3
"""Insert the abilities newly documented in mobs.json into WarnMe's ability_info.xml.

`gen_ability_info.py` is NOT in this container (it lived in the WarnMe session's workspace), so this
is a TARGETED INSERT rather than a regeneration: it reads the uploaded XML byte-for-byte, adds the
missing blocks in the file's own casefold-sorted position, and leaves every existing byte alone.

Name-only entries (no <id>/<cat>) — these are new bestiary transcriptions with no Windower res
cross-reference yet. `//wm audit` inside the addon will list them.

fx -> <effects> uses the XML's own canonical vocabulary: mobs.json 'Hate Reset' is written
'Enmity Reset', which is what the 1,740-entry file already uses.
"""
import json, re, sys

XML_IN = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/uploads/ability_info.xml'
XML_OUT = sys.argv[2] if len(sys.argv) > 2 else '/mnt/user-data/outputs/ability_info.xml'
MOBS = 'app/src/main/assets/mobs.json'

raw = open(XML_IN, encoding='utf-8', newline='').read()
pat = re.compile(r'    <ability>\r\n.*?    </ability>\r\n', re.S)
spans = [m.span() for m in pat.finditer(raw)]
assert spans, 'no ability blocks found'
head = raw[:spans[0][0]]
tail = raw[spans[-1][1]:]
blocks = [raw[a:b] for a, b in spans]
assert head + ''.join(blocks) + tail == raw, 'blocks are not contiguous — refusing to rewrite'
print('parsed %d blocks, head %d bytes, tail %d bytes' % (len(blocks), len(head), len(tail)))

def nameof(b):
    return re.search(r'<n>(.*?)</n>', b, re.S).group(1)

have = {nameof(b) for b in blocks}
AB = json.load(open(MOBS, encoding='utf-8'))['abilities']

# names the bestiary documents that the XML has no block for
SKIP = {'??? Needles', 'aerial', 'Bomb Toss (Dropped)'}   # not real game names
todo = [n for n in AB if n not in have and n not in SKIP]
print('to insert: %d %s' % (len(todo), todo))

EFFECT_MAP = {'Hate Reset': 'Enmity Reset'}

def block_for(name, a):
    tgt = (a.get('tgt') or '')
    self_t = tgt == 'Self'
    cone = 'Cone' in tgt or tgt == 'Conal'
    aoe = (not cone) and ('AoE' in tgt)
    L = ['    <ability>',
         '        <n>%s</n>' % name,
         '        <self_target>%s</self_target>' % str(self_t).lower(),
         '        <aoe>%s</aoe>' % str(aoe).lower(),
         '        <fan>false</fan>',
         '        <cone>%s</cone>' % str(cone).lower()]
    if a.get('r') == 'Gaze' or (a.get('tgt') or '') == 'Gaze':
        L.append('        <gaze>true</gaze>')
    if a.get('t'):
        L.append('        <type>%s</type>' % a['t'])
    if a.get('el'):
        L.append('        <element>%s</element>' % a['el'])
    fx = [EFFECT_MAP.get(x, x) for x in (a.get('fx') or [])][:6]
    L.append('        <effects>%s</effects>' % ', '.join(fx))
    L.append('    </ability>')
    return '\r\n'.join(L) + '\r\n'

added = []
for n in todo:
    b = block_for(n, AB[n])
    # the file is sorted casefold on <n>; insert before the first block that sorts after
    i = next((j for j, ex in enumerate(blocks) if nameof(ex).lower() > n.lower()), len(blocks))
    blocks.insert(i, b)
    added.append((n, i))
    print('  + %-22s at index %d' % (n, i))

out = head + ''.join(blocks) + tail
open(XML_OUT, 'w', encoding='utf-8', newline='').write(out)

# ---- verify
chk = open(XML_OUT, encoding='utf-8', newline='').read()
nb = pat.findall(chk)
names = [nameof(b) for b in nb]
assert len(nb) == len(blocks), (len(nb), len(blocks))
assert names == sorted(names, key=str.lower), 'ordering broken'
assert '\n' not in chk.replace('\r\n', ''), 'a bare LF crept in'
import xml.etree.ElementTree as ET
ET.fromstring(chk)
uniq = len(set(names))
print('\nwrote %s: %d blocks / %d unique names (was %d / %d), XML parses, CRLF clean' % (
    XML_OUT, len(nb), uniq, len(blocks) - len(added), len(have)))
gaps = [n for n in AB if n not in set(names)]
print('bestiary names still absent from the XML: %d %s' % (len(gaps), gaps))
