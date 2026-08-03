#!/usr/bin/env python3
"""
rev 278 — USER-SUPPLIED HOME POINT LABELS (they play these zones):

  east adoulin  HP2 = MH
  west adoulin  HP1 = AH, HP2 = MH
  norg          HP2 = AH  ("not A" — the stored label read "(A)")
  port jeuno    HP1 = Entrance, HP2 = MH
  whitegate     HP3 = AH, HP4 = MH

Label form follows the one already in the file, `Home Point #N (label)` — Norg's
existing "(A)" is the precedent, and the user's correction of it fixes the only
pre-existing one. Coordinates are untouched.
"""
import json, os, sys
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'src', 'main', 'assets')
p = os.path.join(A, 'zoneinfo.json')
zi = json.load(open(p, encoding='utf-8'))

EDITS = {
    'eastern_adoulin':      {'Home Point #2': 'Home Point #2 (MH)'},
    'western_adoulin':      {'Home Point #1': 'Home Point #1 (AH)',
                             'Home Point #2': 'Home Point #2 (MH)'},
    'norg':                 {'Home Point #2 (A)': 'Home Point #2 (AH)'},
    'port_jeuno':           {'Home Point #1': 'Home Point #1 (Entrance)',
                             'Home Point #2': 'Home Point #2 (MH)'},
    'aht_urhgan_whitegate': {'Home Point #3': 'Home Point #3 (AH)',
                             'Home Point #4': 'Home Point #4 (MH)'},
}

for slug, m in EDITS.items():
    for row in zi[slug]['travel']:
        if row['n'] in m:
            print(f"  {slug:22s} {row['n']!r} -> {m[row['n']]!r}   ({row.get('c')})")
            row['n'] = m[row['n']]
    left = [k for k in m if not any(r['n'] == m[k] for r in zi[slug]['travel'])]
    assert not left, (slug, left)

if '--write' in sys.argv:
    json.dump(zi, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    print("WRITTEN.")
else:
    print("(dry run)")
