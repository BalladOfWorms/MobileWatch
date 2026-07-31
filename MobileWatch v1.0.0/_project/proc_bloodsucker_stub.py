#!/usr/bin/env python3
"""
rev 173 — the `bloodsucker` stub removed, and the user's naming rule applied to the pair.

USER: "there is also a blank entry in other>unknown for bloodsucker, which i dont
think is needed" -> "do it", plus the standing rule "for mobs that have a nm and a
regular mob of same name, nm gets (NM) behind it, regular mob gets nothing."

THE STUB IS VERIFIED REDUNDANT, FIELD BY FIELD. Everything in `mobs["bloodsucker"]`
is either identical to a twin or a degraded copy of one:
    det   ["Sound"]                       identical to both twins
    nmlv  "71"                             identical to the NM
    agg   true                             identical to the (monster) record
    spawn "Timed (1 hr, anywhere on Map 3)"  the NM says the same thing, better worded
    drops "Bloodbead Ring, Pigeon's Blood Ruby"
          -> the NM has "Bloodbead Ring, Pigeon's Blood, Beastman Blood": one more
             item, and the CORRECT DB spelling ("Pigeon's Blood Ruby" is not an item,
             so the stub is also one of the 305 invalid drop entries)
    wk    1 row  (Light +25%)              both twins carry 3 rows
    st    3 rows                           both twins carry 4 (the stub omits Dark -30%)
    lv    [53,80]                          matches NEITHER (NM is 71, regular is 52-68)
and it has no fam, ab, img, crys, job, notes or zones at all.

Rule-18 clearances: no zones / ab / img / nm, and after rev 155 renamed the zoneinfo
rows NOTHING resolves to it.

THEN THE RENAME, per the naming rule:
    bloodsucker (monster) -> bloodsucker        (the regular mob, no suffix)
    bloodsucker (nm)      -> unchanged           (already `Bloodsucker (NM)`)
plus the five zoneinfo rows that read `Bloodsucker (Monster)`.

ONLY THIS PAIR. The other 14 bare records that look like stubs are NOT redundant —
each holds at least one field its twin lacks entirely, and three carry `nm: true`.
"""
import json, os, sys

A = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '..', 'app', 'src', 'main', 'assets')
P = lambda f: os.path.join(A, f)

m = json.load(open(P('mobs.json'), encoding='utf-8'))
mobs = m['mobs']
zi = json.load(open(P('zoneinfo.json'), encoding='utf-8'))
items = {v['n'] for v in json.load(open(P('ffxi_items.json'), encoding='utf-8')).values() if 'n' in v}

STUB, MON, NM = 'bloodsucker', 'bloodsucker (monster)', 'bloodsucker (nm)'
for k in (STUB, MON, NM):
    if k not in mobs:
        sys.exit(f"ABORT: {k!r} missing — file is not in the expected pre-state.")

# --- guard: the stub must hold nothing the twins lack ---------------------
lost = [f for f, v in mobs[STUB].items()
        if f != 'n' and mobs[MON].get(f) is None and mobs[NM].get(f) is None]
if lost:
    sys.exit(f"ABORT: deleting {STUB!r} would lose {lost}")
print(f"guard passed — {STUB!r} holds no field that both twins lack\n")

# --- 1. delete the stub ---------------------------------------------------
before = len(mobs)
del mobs[STUB]
print(f"DELETED  mobs[{STUB!r}]          mobs {before} -> {len(mobs)}")

# --- 2. rename the regular mob to the bare key, preserving key order -------
mobs2 = {}
for k, v in mobs.items():
    if k == MON:
        v['n'] = 'Bloodsucker'
        mobs2[STUB] = v
    else:
        mobs2[k] = v
m['mobs'] = mobs = mobs2
print(f"RENAMED  {MON!r} -> {STUB!r},  n -> 'Bloodsucker'")
print(f"KEPT     {NM!r}, n = {mobs[NM]['n']!r}")

# --- 3. the zoneinfo rows that name it ------------------------------------
n = 0
for slug, e in zi.items():
    for bucket in ('nms', 'mobs'):
        for row in e.get(bucket, []):
            if isinstance(row, dict) and row.get('n') == 'Bloodsucker (Monster)':
                row['n'] = 'Bloodsucker'
                n += 1
                print(f"         zoneinfo {slug:24s} [{bucket}] -> 'Bloodsucker'")
print(f"{n} zoneinfo rows renamed")

# --- verification ---------------------------------------------------------
assert STUB in mobs and mobs[STUB]['n'] == 'Bloodsucker' and mobs[STUB].get('fam') == 'Leech'
assert MON not in mobs and mobs[NM]['n'] == 'Bloodsucker (NM)'
for slug, e in zi.items():
    for bucket in ('nms', 'mobs'):
        for row in e.get(bucket, []):
            if isinstance(row, dict) and 'Bloodsucker' in str(row.get('n')):
                key = row['n'].lower()
                assert key in mobs, f"{slug}/{bucket}: {row['n']!r} resolves to nothing"
print("\nevery zoneinfo Bloodsucker row resolves; the regular mob is bare, the NM keeps (NM)")
bad = [p.strip() for p in mobs[STUB]['drops'].split(',')] if mobs[STUB].get('drops') else []
print("regular mob drops:", mobs[STUB].get('drops'), "| NM drops:", mobs[NM]['drops'])

if '--write' in sys.argv:
    json.dump(m, open(P('mobs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump(zi, open(P('zoneinfo.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print("\nWRITTEN.")
else:
    print("\n(dry run — pass --write)")
