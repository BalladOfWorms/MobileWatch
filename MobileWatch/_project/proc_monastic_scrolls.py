#!/usr/bin/env python3
"""
rev 267 — RULE 41: the wiki writes spell scrolls as `Scroll of X`; ffxi_items.json
has NO "Scroll of ..." entry at all — every scroll is filed under the BARE SPELL
NAME (`Quake`, `Stone IV`, `Stun`, `Water Carol II`). Two Monastic Cavern NMs
carried the wiki form.

Measured file-wide first: only 3 records / 6 tokens use `Scroll of `. The third is
`arke` ("Scroll of Aeroja, Scroll of Aerora II") — NOT touched here: it is a
different zone's record, it has the same coffer-nesting shape as emperor arthro did,
and **`Aerora II` resolves to nothing at all** (the DB has Aero/Aeroga/Aeroja, no
Aerora), so it needs adjudication rather than a strip.
"""
import json, os, sys
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'src', 'main', 'assets')
m = json.load(open(os.path.join(A, 'mobs.json'), encoding='utf-8'))
items = json.load(open(os.path.join(A, 'ffxi_items.json'), encoding='utf-8'))
low = {v['n'].lower() for v in items.values() if isinstance(v, dict) and 'n' in v}

for k in ('orcish hexspinner', 'orcish warlord'):
    rec = m['mobs'][k]
    old = rec['drops']
    new = ', '.join(p.strip()[10:] if p.strip().lower().startswith('scroll of ') else p.strip()
                    for p in old.split(','))
    bad = [p.strip() for p in new.split(',') if p.strip().lower() not in low]
    assert not bad, bad
    rec['drops'] = new
    print(f"  {k:20s}\n    - {old}\n    + {new}")

if '--write' in sys.argv:
    json.dump(m, open(os.path.join(A, 'mobs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print("WRITTEN.")
else:
    print("(dry run)")
