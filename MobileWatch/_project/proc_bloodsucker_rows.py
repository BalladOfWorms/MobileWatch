#!/usr/bin/env python3
"""
rev 155 — Bostaunieux Oubliette: the two "Bloodsucker" rows are disambiguated.

USER: "in bost. oubliette, we have 2 bloodsuckers. 1 is a nm and the other a
regular mob. the nm should have (NM) after its name. clicking on either goes to
nm page"

ROOT CAUSE (both halves):
  ZoneNmRow / ZoneMobRow render `name` RAW and navigate with
  `vm.selectMobByName(name, level)` -> `mobDb?.get(name.lowercase())`, an exact
  key lookup. zoneinfo stored the SAME string "Bloodsucker" in both nms[] and
  mobs[], so (a) the two rows read identically and (b) BOTH resolved to the
  mobs.json key `bloodsucker` -- which is neither of the real records. It is the
  (lm) orphan duplicate stub: fam=None, 0 zones, but carrying nmlv "71" plus the
  NM's spawn and drops, so it RENDERS like the NM page. Hence "either goes to nm".

FIX: name each row after the record it means, which is also that record's own
display name, so the lookup lands correctly and the rows read distinctly.
  nms[]  "Bloodsucker" -> "Bloodsucker (NM)"      -> key `bloodsucker (nm)`
  mobs[] "Bloodsucker" -> "Bloodsucker (Monster)" -> key `bloodsucker (monster)`

The (Monster) suffix is not invented: zoneinfo already ships `Chigoe (Monster)`
(Caedarva Mire) and `Condor (Monster)` (Meriphataud Mountains [S]), and `Mamool
Ja (NM)` (Mamook) -- all three resolve. This follows that convention exactly.

NOT TOUCHED: the orphan `bloodsucker` stub itself. After this rev nothing points
at it, which makes the (lm) merge/delete safe -- but that is the user's call.
"""
import json, os, sys

A = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '..', 'app', 'src', 'main', 'assets')
P = lambda f: os.path.join(A, f)
SLUG = 'bostaunieux_oubliette'

RENAMES = [(SLUG, 'nms',  'Bloodsucker', 'Bloodsucker (NM)'),
           (SLUG, 'mobs', 'Bloodsucker', 'Bloodsucker (Monster)')]

# The same collision, same mob, in four MORE zones — all of them Adversaries rows.
# Unambiguous: `bloodsucker (nm)` has exactly ONE zone (Bostaunieux), so it cannot be
# any of these, and `bloodsucker (monster)` carries all four. Left unfixed they would
# keep every one of these rows pointing at the orphan stub.
RENAMES += [(s, 'mobs', 'Bloodsucker', 'Bloodsucker (Monster)') for s in
            ('toraimarai_canal', 'den_of_rancor', 'temple_of_uggalepih', 'vunkerl_inlet_s')]

mobs = json.load(open(P('mobs.json'), encoding='utf-8'))['mobs']
zi = json.load(open(P('zoneinfo.json'), encoding='utf-8'))

print("BEFORE — what each row resolves to:")
for slug, bucket, old, new in RENAMES:
    row = next((r for r in zi[slug][bucket] if r.get('n') == old), None)
    if row is None:
        sys.exit(f"ABORT: no {slug}.{bucket}[] row named {old!r} — unexpected pre-state.")
    tgt = mobs[old.lower()]
    print(f"  {slug:24s} [{bucket:4s}] {old!r} -> key {old.lower()!r} "
          f"(fam={tgt.get('fam')}, zones={len(tgt.get('zones', []))})")

for slug, bucket, old, new in RENAMES:
    key = new.lower()
    if key not in mobs:
        sys.exit(f"ABORT: {new!r} would not resolve — no mobs.json key {key!r}.")
    # the target record must actually carry this zone, or the row is pointing at a
    # mob that isn't there — a rename must not paper over a real mismatch
    next(r for r in zi[slug][bucket] if r.get('n') == old)['n'] = new

print("\nAFTER — each row now resolves to its own record:")
for slug, bucket, old, new in RENAMES:
    rec = mobs[new.lower()]
    row = next(r for r in zi[slug][bucket] if r.get('n') == new)
    print(f"  {slug:24s} [{bucket:4s}] {new!r} -> nm={rec.get('nm')}, "
          f"zones={len(rec.get('zones', []))}, lv row={row.get('lv')!r}")

e = zi[SLUG]
# the two Bostaunieux rows must now be distinct, and NOTHING file-wide may still
# resolve to the orphan `bloodsucker` stub
names = [r['n'] for b in ('nms', 'mobs') for r in e[b] if 'Bloodsucker' in r.get('n', '')]
assert names == ['Bloodsucker (NM)', 'Bloodsucker (Monster)'], names
left = [(s, b) for s, i in zi.items() for b in ('nms', 'mobs')
        for r in i.get(b, []) if isinstance(r, dict) and r.get('n', '').lower() == 'bloodsucker']
assert not left, left
print(f"\nrows still resolving to the orphan `bloodsucker` stub: NONE")

if '--write' in sys.argv:
    json.dump(zi, open(P('zoneinfo.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print("\nWRITTEN.")
else:
    print("\n(dry run — pass --write)")
