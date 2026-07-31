#!/usr/bin/env python3
"""
rev 158 step 1 — every PARENTHESISED zone string normalized to the bracket form.

Found by applying rule 57 (added last rev) before the East Sarutabaruta pass:
listing every `zones[]` string containing the zone's distinctive word turned up
`West Sarutabaruta (S)` alongside the canonical `West Sarutabaruta [S]`. Widening
the check to the whole file found 25 such entries across 13 strings on 12 records.

EVERY canonical bracket form already exists in zones.json, so all 25 are
unambiguous. `AuctionApp.kt:355` groups the Zone view by the LITERAL string with
no normalizer, so each parenthesised entry is a phantom one-mob bucket AND a mob
missing from the real zone's bucket.

`dark ixion` alone accounts for 7 of the 25 — it uses the parenthesised form for
ALL of its zones, i.e. one record written by one intake with the wrong
convention, not scattered typos (rule 58's fingerprint idea).

Guarded: a record that already holds BOTH forms of a zone would end up with the
zone twice, so those are reported and skipped rather than merged blindly.
"""
import json, os, re, sys

A = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '..', 'app', 'src', 'main', 'assets')
P = lambda f: os.path.join(A, f)
PAREN = re.compile(r'\((S|U|U1|U2|U3)\)\s*$')

m = json.load(open(P('mobs.json'), encoding='utf-8'))
zj = {z['name'] for z in json.load(open(P('zones.json'), encoding='utf-8'))['zones']}

changed, skipped, unknown = [], [], []
for k, v in m['mobs'].items():
    zones = v.get('zones', [])
    have = {(e[0] if isinstance(e, list) else e) for e in zones}
    for e in zones:
        name = e[0] if isinstance(e, list) else e
        if not PAREN.search(name):
            continue
        canon = PAREN.sub(lambda mm: f"[{mm.group(1)}]", name)
        if canon not in zj:
            unknown.append((k, name, canon))
            continue
        if canon in have:
            skipped.append((k, name, canon))
            continue
        if isinstance(e, list):
            e[0] = canon
        else:
            zones[zones.index(e)] = canon
        have.add(canon)
        changed.append((k, name, canon))

print(f"normalized {len(changed)} entries on {len({k for k, _, _ in changed})} records\n")
for k, old, new in sorted(changed):
    print(f"   {k:22s} {old!r:32s} -> {new!r}")
if skipped:
    print(f"\n!! SKIPPED (record already holds the canonical form — would duplicate): {skipped}")
if unknown:
    print(f"\n!! SKIPPED (canonical form not in zones.json): {unknown}")

left = [(k, e) for k, v in m['mobs'].items() for e in v.get('zones', [])
        if PAREN.search(e[0] if isinstance(e, list) else e)]
print(f"\nparenthesised entries remaining: {len(left)}  {left if left else ''}")
dup = [k for k, v in m['mobs'].items()
       if len({(e[0] if isinstance(e, list) else e) for e in v.get('zones', [])}) != len(v.get('zones', []))]
assert not dup, f"record(s) now hold a zone twice: {dup}"

if '--write' in sys.argv:
    json.dump(m, open(P('mobs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print("WRITTEN.")
else:
    print("(dry run — pass --write)")
