#!/usr/bin/env python3
"""
rev 158 step 2 — EVERY UNAMBIGUOUS zone-string variant reconciled to zones.json.

Rule 57 says reconcile zone strings before a zone pass. Doing that for East
Sarutabaruta turned up `West Sarutabaruta (S)`; widening to the whole file found
that **795 zone entries across 79 strings are not zones.json names at all**.

`AuctionApp.kt:355` groups the Zone view by the LITERAL string and there is no
normalizer on that path, so each variant is a PHANTOM bucket in the browser and
its mobs are missing from the real zone's bucket.

This script fixes only the UNAMBIGUOUS ones: a variant is rewritten only when
stripping apostrophes (straight AND curly) and normalizing hyphens/whitespace
maps it onto EXACTLY ONE zones.json name. 35 strings / 464 entries qualify —
`Qu'Bia Arena`, `Crawlers' Nest`, `Ordelle's Caves`, `Pso'Xja`, `Fei'Yin`, the
three Delkfutt's Towers, the `Escha - Zi'Tah` / `Escha - Ru'Aun` / `Escha - Ru’Aun`
trio, the `Abyssea - X` spacing, and so on.

THE OTHER 44 STRINGS (331 entries) ARE LEFT ALONE — they have no zones.json
counterpart at all (Apollyon/Temenos sub-areas, the Valkyrie chambers, Sheol
A/B/Gaol, the bracketed U-zones, Maquette Abdhaljs-Legion, Incursion, Sortie).
Those need a real decision about what zones.json should contain, not a rewrite.

GUARDS: two zones.json names may never normalize to the same key (asserted); a
record that already holds both forms is skipped rather than given the zone twice.
"""
import json, os, re, sys, collections

A = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '..', 'app', 'src', 'main', 'assets')
P = lambda f: os.path.join(A, f)


def norm(s):
    s = s.replace('\u2019', "'").replace("'", "").replace('-', ' ')
    return re.sub(r'\s+', ' ', s).strip().lower()


m = json.load(open(P('mobs.json'), encoding='utf-8'))
zj = [z['name'] for z in json.load(open(P('zones.json'), encoding='utf-8'))['zones']]

collide = [k for k, v in collections.Counter(norm(z) for z in zj).items() if v > 1]
assert not collide, f"two zones.json names normalize alike — unsafe: {collide}"
canon = {norm(z): z for z in zj}
known = set(zj)

changed, skipped, nomatch = [], [], collections.Counter()
for k, v in m['mobs'].items():
    zones = v.get('zones', [])
    have = {(e[0] if isinstance(e, list) else e) for e in zones}
    for e in zones:
        name = e[0] if isinstance(e, list) else e
        if name in known:
            continue
        tgt = canon.get(norm(name))
        if tgt is None:
            nomatch[name] += 1
            continue
        if tgt in have:
            skipped.append((k, name, tgt))
            continue
        if isinstance(e, list):
            e[0] = tgt
        else:
            zones[zones.index(e)] = tgt
        have.add(tgt)
        changed.append((k, name, tgt))

bystr = collections.Counter(old for _, old, _ in changed)
print(f"NORMALIZED {len(changed)} entries across {len(bystr)} variant strings "
      f"on {len({k for k, _, _ in changed})} records\n")
for old, c in bystr.most_common():
    print(f"   {old!r:34s} x{c:<4} -> {canon[norm(old)]!r}")

if skipped:
    print(f"\n!! SKIPPED — record already holds the canonical form ({len(skipped)}):")
    for k, old, tgt in skipped:
        print(f"   {k:26s} {old!r} (already has {tgt!r})")

print(f"\nLEFT ALONE — no zones.json counterpart: "
      f"{len(nomatch)} strings / {sum(nomatch.values())} entries")
for n, c in nomatch.most_common(12):
    print(f"   {n!r:40s} x{c}")
if len(nomatch) > 12:
    print(f"   ... {len(nomatch)-12} more")

dup = [k for k, v in m['mobs'].items()
       if len({(e[0] if isinstance(e, list) else e) for e in v.get('zones', [])}) != len(v.get('zones', []))]
assert not dup, f"record(s) now hold a zone twice: {dup}"

if '--write' in sys.argv:
    json.dump(m, open(P('mobs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print("\nWRITTEN.")
else:
    print("\n(dry run — pass --write)")
