#!/usr/bin/env python3
"""
rev 157 step 1 — the King Ranperre's Tomb SPLIT BUCKET, normalized (rule 7 / the (le) class).

mobs.json stored TWO different strings for one zone:
    "King Ranperre's Tomb"   (apostrophe)  36 records
    "King Ranperres Tomb"    (zones.json)   8 records
`AuctionApp.kt:355` groups the Zone view by the LITERAL string and there is no
normalizer on that path, so the browser showed the zone TWICE — a 36-mob bucket
and an 8-mob bucket. zones.json (id 190) and both zoneinfo `connects[]` entries
use the apostrophe-less form, so that is canon.

THE SPLIT HAS A CLEAN INTAKE SIGNATURE: all 8 canon-form records are Goblins
(ambusher/butcher/gambler/leecher/mugger/thug/tinkerer/weaver) and all 36
apostrophe-form records are everything else — i.e. the Goblin family pass wrote
one form and every other pass wrote the other. No record carries both.
"""
import json, os, sys

A = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '..', 'app', 'src', 'main', 'assets')
P = lambda f: os.path.join(A, f)
BAD, CANON = "King Ranperre's Tomb", "King Ranperres Tomb"

zj = {z['name'] for z in json.load(open(P('zones.json'), encoding='utf-8'))['zones']}
if CANON not in zj or BAD in zj:
    sys.exit("ABORT: zones.json does not name the apostrophe-less form as canon.")

m = json.load(open(P('mobs.json'), encoding='utf-8'))
moved = []
for k, v in m['mobs'].items():
    for e in v.get('zones', []):
        name = e[0] if isinstance(e, list) else e
        if name == BAD:
            lvl = e[1] if isinstance(e, list) and len(e) > 1 else None
            moved.append((k, lvl))
            if isinstance(e, list):
                e[0] = CANON
            else:
                v['zones'][v['zones'].index(e)] = CANON

print(f"normalized {len(moved)} entries  {BAD!r} -> {CANON!r}")
for k, lvl in sorted(moved):
    print(f"   {k:26s} lv={lvl}")

# nothing may still carry the bad form, and no record may end up with the zone twice
left = [k for k, v in m['mobs'].items()
        if any((e[0] if isinstance(e, list) else e) == BAD for e in v.get('zones', []))]
assert not left, left
dup = [k for k, v in m['mobs'].items()
       if sum(1 for e in v.get('zones', []) if (e[0] if isinstance(e, list) else e) == CANON) > 1]
assert not dup, f"record(s) now hold the zone twice: {dup}"
total = sum(1 for v in m['mobs'].values()
            for e in v.get('zones', []) if (e[0] if isinstance(e, list) else e) == CANON)
print(f"\nrecords now under {CANON!r}: {total}  (was 8 + {len(moved)} split across two buckets)")

if '--write' in sys.argv:
    json.dump(m, open(P('mobs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print("WRITTEN.")
else:
    print("(dry run — pass --write)")
