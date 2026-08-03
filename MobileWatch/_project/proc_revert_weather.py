#!/usr/bin/env python3
"""
rev 170 — REVERT every zoneinfo `weather` override written this session.

USER: "have you been updating the weather? weather is good, we are just looking at
mobs with these screenshots. i send the zone info so you know which zone we are
working on"

I had been treating the info box as a data source and writing a `weather` override
on every zone whose page printed "None" (rule 40, added at rev 149). That was wrong:
the info box is there to identify the zone, not to be harvested. 16 zones were
changed, all from "" to "None", and all are restored to "" here.

Restores against the ORIGINAL uploaded zip rather than a hardcoded "" — so if any of
the 16 had held a real value beforehand it comes back, not a blanket blank.

Nothing else is touched: the `notes`, `mobs[]` and `nms[]` changes are listed but
left alone pending the user's word.
"""
import json, os, sys

NEW = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', 'app', 'src', 'main', 'assets', 'zoneinfo.json')
ORIG = '/tmp/orig/android/app/src/main/assets/zoneinfo.json'

o = json.load(open(ORIG, encoding='utf-8'))
n = json.load(open(NEW, encoding='utf-8'))

reverted, other = [], {}
for k in o:
    for f in set(o[k]) | set(n[k]):
        if o[k].get(f) == n[k].get(f):
            continue
        if f == 'weather':
            reverted.append((k, n[k].get('weather'), o[k].get('weather')))
            n[k]['weather'] = o[k]['weather']
        else:
            other.setdefault(f, []).append(k)

print(f"REVERTED {len(reverted)} weather overrides:\n")
for k, was, back in sorted(reverted):
    print(f"   {k:30s} {was!r} -> {back!r}")

# nothing may differ on `weather` any more
left = [k for k in o if o[k].get('weather') != n[k].get('weather')]
assert not left, left
print("\nzoneinfo entries still differing from the original, by field (NOT touched):")
for f, ks in sorted(other.items(), key=lambda t: -len(t[1])):
    print(f"   {f:8s} {len(ks):2d}  {', '.join(sorted(ks))}")

if '--write' in sys.argv:
    json.dump(n, open(NEW, 'w', encoding='utf-8'), ensure_ascii=False)
    print("\nWRITTEN.")
else:
    print("\n(dry run — pass --write)")
