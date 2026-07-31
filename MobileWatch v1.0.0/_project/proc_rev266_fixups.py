#!/usr/bin/env python3
"""
rev 266 fixups.

1) RULE 41 — `emperor arthro` drops carried the WIKI's long names and a one-off
   nesting syntax that exists nowhere else in the file:

     "Emperor Arthro's Coffer: Emperor Arthro's Shell, Sailfi Belt, ..."

   The DB has **`Arthro's Coffer`** and **`Arthro's Shell`** — the wiki prefixes the
   NM's full name, the DB doesn't (the Camahueto's Fur / Sleepy Mabel's Fur pattern).
   The 403 other drops strings containing ": " are all ITEM NAMES with a colon
   (`Aptant: Secan`, `Goetia Seal: Hd.`), never a container, so the nesting is
   flattened to the file's universal comma list. Nothing is lost.
   NOTE: whether a coffer belongs in `drops` at all is open item (ln) — not decided here.

2) ZONEINFO NOTE, user-authorised: *"the astroglobe from last screenshots, if there
   is no note in the zone section, then yes, go ahead and include a note"*.
   `the_eldieme_necropolis` has no `notes` key at all, so one is created with the
   info-box's access requirement, stored close to the page's wording.
   The rest of that footnote (the two G-9 block drops) is NOT harvested — the
   authorisation was for the astrolabe.
"""
import json, os, sys

A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'src', 'main', 'assets')
L = lambda f: json.load(open(os.path.join(A, f), encoding='utf-8'))
S = lambda f, o: json.dump(o, open(os.path.join(A, f), 'w', encoding='utf-8'), ensure_ascii=False)

m = L('mobs.json')
rec = m['mobs']['emperor arthro']
OLD = "Emperor Arthro's Coffer: Emperor Arthro's Shell, Sailfi Belt, Sailfi Belt +1, Augury Cuisses, Augury Cuisses +1, Water Carol II"
NEW = "Arthro's Coffer, Arthro's Shell, Sailfi Belt, Sailfi Belt +1, Augury Cuisses, Augury Cuisses +1, Water Carol II"
assert rec['drops'] == OLD, rec['drops']
rec['drops'] = NEW
print(f"  emperor arthro drops:\n    - {OLD}\n    + {NEW}")

zi = L('zoneinfo.json')
e = zi['the_eldieme_necropolis']
assert 'notes' not in e, "notes already present — user's condition was 'if there is no note'"
e['notes'] = ["Opening the doors in the area on your own requires a Magicked Astrolabe."]
print(f"\n  the_eldieme_necropolis.notes <- {e['notes']}")

items = L('ffxi_items.json')
low = {v['n'].lower() for v in items.values() if isinstance(v, dict) and 'n' in v}
bad = [p.strip() for p in NEW.split(',') if p.strip().lower() not in low]
print(f"\n  rule 41 recheck: {'CLEAN' if not bad else bad}")

assert not [k for mm in m['mobs'].values() for k, v in mm.items() if v is None], "null poison"

if '--write' in sys.argv:
    S('mobs.json', m)
    S('zoneinfo.json', zi)
    print("WRITTEN.")
else:
    print("(dry run — pass --write)")
