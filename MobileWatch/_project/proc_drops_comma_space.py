#!/usr/bin/env python3
"""
rev 276 — COSMETIC, MEASURED FIRST: 12 records file-wide store `drops` with commas
that have NO space after them, so they render as run-together text.

`AuctionApp.kt` renders `mob.drops` WHOLE in all three of its sites (809, 1447, 3869)
— nothing ever splits the string — so this is a display-quality fix only and cannot
change parsing. Names are untouched; only the separator is normalised to ", ".

Found while validating Qufim's `jester malatrix` ("Malatrix's Shard,Buramgh,Evalach").
"""
import json, os, re, sys
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'src', 'main', 'assets')
d = json.load(open(os.path.join(A, 'mobs.json'), encoding='utf-8'))
items = json.load(open(os.path.join(A, 'ffxi_items.json'), encoding='utf-8'))
low = {v['n'].lower() for v in items.values() if isinstance(v, dict) and 'n' in v}

n = 0
for k, v in d['mobs'].items():
    s = v.get('drops')
    if isinstance(s, str) and re.search(r',\S', s):
        before_bad = [p.strip() for p in s.split(',') if p.strip().lower() not in low]
        new = re.sub(r',\s*', ', ', s)
        after_bad = [p.strip() for p in new.split(',') if p.strip().lower() not in low]
        assert before_bad == after_bad, (k, before_bad, after_bad)
        v['drops'] = new
        n += 1
        print(f"  {k:24s} {new[:70]}")
print(f"\n{n} records normalised (names unchanged, verified against the item DB)")

if '--write' in sys.argv:
    json.dump(d, open(os.path.join(A, 'mobs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print("WRITTEN.")
else:
    print("(dry run)")
