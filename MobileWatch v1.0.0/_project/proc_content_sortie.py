#!/usr/bin/env python3
# MobileWatch — Sortie content tagging (rev 246)
# Source: BG-wiki Category:Sortie (user screenshots).
# Tags the 8 minor NMs, 8 major NMs and Aminon into the content section, normalizes the Sortie
# zone string, and applies the page's blanket "All foes in Sortie are aggressive" rule.
import json, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M = d['mobs']

ZONE = "Outer Ra'Kaznar [U]"

MINOR = ['abject obdella', 'biune porxie', 'cachaemic bhoot', 'demisang deleterious',
         'esurient botulus', 'fetid ixion', 'gyvewrapped naraka', 'haughty tulittia']
MAJOR = ['ghatjot', 'leshonn', 'skomora', 'degei', 'dhartok', 'gartell', 'triboulex', 'aita']
APEX = ['aminon']

TAGS = [(MINOR, 'Sortie: Bosses: Minor'), (MAJOR, 'Sortie: Bosses: Major'),
        (APEX, 'Sortie: Bosses: Aminon')]

missing, touched = [], []
for keys, tag in TAGS:
    for k in keys:
        m = M.get(k)
        if m is None:
            missing.append(k)
            continue
        c = m.get('content') or []
        if tag not in c:
            c.append(tag)
        m['content'] = c
        m['nm'] = True                       # every one of these is an NM
        m['agg'] = True                      # page: "All foes in Sortie are aggressive."
        # zone: fold the free-text 'Sortie' entries onto the real zone string, keep the level
        zs = m.get('zones') or []
        lvl = None
        for z in zs:
            if z[0] in ('Sortie', ZONE) and len(z) > 1:
                lvl = z[1]
        lvl = lvl or m.get('nmlv') or (str(m['lv'][0]) if m.get('lv') else None)
        zs = [z for z in zs if z[0] not in ('Sortie', ZONE)]
        zs.append([ZONE, lvl] if lvl else [ZONE])
        m['zones'] = zs
        touched.append(k)

assert not [k for m in M.values() for k, v in m.items() if v is None]
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

print('missing:', missing)
print('tagged %d' % len(touched))
for k in touched:
    m = M[k]
    print('  %-24s %-28s lv=%s zones=%s' % (k, m['content'][-1], m.get('lv'), m.get('zones')))
