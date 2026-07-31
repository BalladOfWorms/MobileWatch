#!/usr/bin/env python3
"""
audit_zone_xcheck.py — the (lo) cross-check, file-wide.

zoneinfo.json's per-zone `nms[]` / `mobs[]` lists and mobs.json's per-record
`zones[]` describe the same facts from two different intakes, and NOTHING has
ever compared them. Three zone passes in a row (rev 149-151) found cases where
zoneinfo held the right level and mobs.json did not, so this measures the whole
class in one go.

Read-only. Buckets:
  A  zoneinfo names a mob with NO mobs.json record        -> missing-mob flags
  B  record exists but does not carry the zone            -> zone adds
  C  zone present with NO level, zoneinfo publishes one   -> level fills (rule 11)
  D  both carry a level and they DISAGREE                 -> adjudicate on the page
  E  mobs.json carries the zone but zoneinfo never lists it

Bucket D is the interesting one: it is where a zone pass changes data, so it is
also where a bad automated backfill would do damage. NOTHING here is written.
"""
import json, os, collections

A = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '..', 'app', 'src', 'main', 'assets')
L = lambda f: json.load(open(os.path.join(A, f), encoding='utf-8'))

mobs = L('mobs.json')['mobs']
zinf = L('zoneinfo.json')
slug2name = {z['slug']: z['name'] for z in L('zones.json')['zones']}

# mobs.json keys are the lowercased display name
key_of = {}
for k, v in mobs.items():
    key_of.setdefault(k, k)
    n = v.get('n')
    if n:
        key_of.setdefault(n.lower(), k)


def resolve(name):
    n = name.lower().strip()
    for cand in (n, n.replace("'", "\u2019"), n.replace("\u2019", "'")):
        if cand in key_of:
            return key_of[cand]
    return None


def zone_entry(rec, zone):
    for e in rec.get('zones', []):
        if (e[0] if isinstance(e, list) else e) == zone:
            return e
    return None


def lvl_of(e):
    return e[1] if isinstance(e, list) and len(e) > 1 else None


A_, B_, C_, D_, E_ = [], [], [], [], []
zones_seen = 0

for slug, info in zinf.items():
    zone = slug2name.get(slug)
    if not zone:
        continue
    zones_seen += 1
    listed = set()
    for bucket in ('nms', 'mobs'):
        for row in info.get(bucket, []):
            nm = row.get('n') if isinstance(row, dict) else str(row)
            if not nm:
                continue
            zlv = (row.get('lv') or '').strip() if isinstance(row, dict) else ''
            key = resolve(nm)
            if key is None:
                A_.append((zone, nm, bucket))
                continue
            listed.add(key)
            e = zone_entry(mobs[key], zone)
            if e is None:
                B_.append((zone, key, zlv, bucket))
                continue
            mlv = lvl_of(e)
            if zlv and not mlv:
                C_.append((zone, key, zlv, bucket))
            elif zlv and mlv and zlv != mlv:
                D_.append((zone, key, mlv, zlv, bucket))
    for key, rec in mobs.items():
        if zone_entry(rec, zone) is not None and key not in listed:
            E_.append((zone, key))

print(f"=== (lo) ZONEINFO <-> MOBS.JSON CROSS-CHECK — {zones_seen} zones ===\n")
print(f"A  zoneinfo names a mob with NO record .......... {len(A_)}")
print(f"B  record exists, zone MISSING .................. {len(B_)}")
print(f"C  zone present, level MISSING (zoneinfo has it)  {len(C_)}")
print(f"D  both have a level and they DISAGREE .......... {len(D_)}")
print(f"E  mobs.json has the zone, zoneinfo never lists it {len(E_)}")

print("\n--- A: no record at all (candidate missing mobs) ---")
for z, n, b in A_[:40]:
    print(f"   {z:28s} {n:34s} [{b}]")
if len(A_) > 40:
    print(f"   ... and {len(A_)-40} more")

print("\n--- B: zone adds, by zone (top 20) ---")
cb = collections.Counter(z for z, *_ in B_)
for z, c in cb.most_common(20):
    print(f"   {z:32s} {c}")

print("\n--- C: level fills, by zone (top 20) ---")
cc = collections.Counter(z for z, *_ in C_)
for z, c in cc.most_common(20):
    print(f"   {z:32s} {c}")

print("\n--- D: LEVEL DISAGREEMENTS, sub-classified ---")


def span(s):
    """'52-58, 65-68' -> (52,68); '~43' -> (43,43); '' -> None"""
    lo = hi = None
    for blk in s.split(','):
        b = blk.strip().lstrip('~')
        if not b:
            continue
        p = b.split('-')
        try:
            a = int(p[0]); z = int(p[-1])
        except ValueError:
            return None
        lo = a if lo is None else min(lo, a)
        hi = z if hi is None else max(hi, z)
    return None if lo is None else (lo, hi)


d1, d2, d3, dx = [], [], [], []
for z, k, mlv, zlv, b in D_:
    sm, sz = span(mlv), span(zlv)
    if sm is None or sz is None:
        dx.append((z, k, mlv, zlv, b))
    elif ',' in zlv and sm == sz:
        d1.append((z, k, mlv, zlv, b))      # rule-2 merged span — CONSISTENT
    elif sm[0] <= sz[0] and sm[1] >= sz[1]:
        d2.append((z, k, mlv, zlv, b))      # mobs.json is the wider read
    else:
        d3.append((z, k, mlv, zlv, b))      # genuine conflict


print(f"   D1 rule-2 merged span, spans MATCH (not a conflict) . {len(d1)}")
print(f"   D2 mobs.json span CONTAINS zoneinfo's ............... {len(d2)}")
print(f"   D3 GENUINE CONFLICT (adjudicate on the page) ........ {len(d3)}")
print(f"   DX unparseable on one side ......................... {len(dx)}")

print("\n   --- D3, the ones that actually need a page (first 50) ---")
for z, k, mlv, zlv, b in d3[:50]:
    print(f"   {z:26s} {k:26s} mobs={mlv:10s} zoneinfo={zlv:10s} [{b}]")
if len(d3) > 50:
    print(f"   ... and {len(d3)-50} more")
if dx:
    print("\n   --- DX ---")
    for z, k, mlv, zlv, b in dx[:15]:
        print(f"   {z:26s} {k:26s} mobs={mlv:10s} zoneinfo={zlv:10s} [{b}]")

print(f"\n--- E: by zone (top 15) ---")
ce = collections.Counter(z for z, _ in E_)
for z, c in ce.most_common(15):
    print(f"   {z:32s} {c}")
