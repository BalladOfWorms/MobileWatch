#!/usr/bin/env python3
"""
rev 273 — `arke` finally lands inside a zone roster, so the rev-267 deferral closes.
Three separate problems in one drops string:

  before: "Arke's Coffer: Arke's Wing, Ababinili, Ababinili +1, Pukulatmuj,
           Pukulatmuj +1. Non-unique: Saffron Blossom, Coral Fragment,
           Scroll of Aeroja, Scroll of Aerora II"

  1. the coffer-nesting `Coffer: contents` syntax (rev-266 flattened the identical
     shape on emperor arthro — no other record uses it)
  2. the ". Non-unique:" prose qualifier splicing two lists together
  3. rule 103 — `Scroll of X`; the DB files scrolls under the bare spell name

  after:  "Arke's Coffer, Arke's Wing, Ababinili, Ababinili +1, Pukulatmuj,
           Pukulatmuj +1, Saffron Blossom, Coral Fragment, Aeroja, Aerora II"

Every name resolves EXCEPT **`Aerora II`, which is not an FFXI spell at all** — the
DB has Aero / Aero II-V / Aeroga / Aeroga II / Aeroga III / Aeroja and no Aerora.
The `Scroll of ` prefix is still stripped (that part is certain), but the name itself
is left exactly as found and flagged: it needs the user, not a guess.
"""
import json, os, sys
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'src', 'main', 'assets')
d = json.load(open(os.path.join(A, 'mobs.json'), encoding='utf-8'))
items = json.load(open(os.path.join(A, 'ffxi_items.json'), encoding='utf-8'))
low = {v['n'].lower() for v in items.values() if isinstance(v, dict) and 'n' in v}

rec = d['mobs']['arke']
old = rec['drops']
new = ("Arke's Coffer, Arke's Wing, Ababinili, Ababinili +1, Pukulatmuj, Pukulatmuj +1, "
       "Saffron Blossom, Coral Fragment, Aeroja, Aerora II")
rec['drops'] = new
print(f"  - {old}\n  + {new}")
print('  unresolved after fix:', [p.strip() for p in new.split(',') if p.strip().lower() not in low])

if '--write' in sys.argv:
    json.dump(d, open(os.path.join(A, 'mobs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print("WRITTEN.")
else:
    print("(dry run)")
