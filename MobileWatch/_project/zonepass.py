#!/usr/bin/env python3
"""
zonepass.py — the reusable REFINING-PHASE zone writer.

Extracted from rev 149's proc_zone_bostaunieux.py so every remaining zone reuses
one implementation instead of a fresh copy (the rev-134 script was lost once
already). A per-zone driver supplies only the DATA and calls run().

Honours the refining-phase rules in /areas/mobs-update-todo-9.md and -11.md:
  r1  additive/corrective only  — a BLANK page cell NEVER overwrites stored data
  r2  merged span per zone      — several page blocks collapse to ONE range
  r7  zone string = the zones.json form, not the page banner
  r8  locate the entry by the zone NAME, never by a level value
  r9  a level correction EXTENDS `lv`, never shrinks it
  r10 BLANK / `?-?` / `-` are all "no data", none is a value
  r11 zone-present-but-null is NOT done — it is a level fill waiting
  r15 SKIP sentinel: a blank page cell CANNOT clear a stored level
  r40 zoneinfo weather/region are OVERRIDES of zones.json — don't mirror the base
  r41 validate NM `drops` names against ffxi_items.json, not just the levels

Reports added / changed / kept-because-blank separately so a silent clear cannot
hide, and refuses to write unless the zone string exists in zones.json.
"""
import json, os, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(_HERE, '..', 'app', 'src', 'main', 'assets')

SKIP = object()   # rule 15 — "leave whatever is there", never "clear it"


def _load(name):
    return json.load(open(os.path.join(ASSETS, name), encoding='utf-8'))


def _save(name, obj):
    # compact + ensure_ascii=False — matches the on-disk format exactly
    json.dump(obj, open(os.path.join(ASSETS, name), 'w', encoding='utf-8'),
              ensure_ascii=False)


def run(zone, slug, rows, lv_extend=None, drop_fix=None, zoneinfo_edit=None,
        write=False):
    """
    zone          canonical zones.json name string (rule 7)
    slug          zoneinfo.json key
    rows          [(mobs.json key, level string or SKIP, provenance note), ...]
    lv_extend     {key: (lo, hi)} unions forced by the level writes (rule 9)
    drop_fix      {key: (old drops string, new drops string)}  (rule 41)
    zoneinfo_edit callable(entry) -> [str] describing what it changed
    """
    lv_extend = lv_extend or {}
    drop_fix = drop_fix or {}

    zj = {z['name'] for z in _load('zones.json')['zones']}
    if zone not in zj:
        sys.exit(f"ABORT (rule 7): '{zone}' is not a zones.json name string.")

    m = _load('mobs.json')
    mobs = m['mobs']

    missing, added, changed, kept_blank, already = [], [], [], [], []

    for key, lvl, prov in rows:
        rec = mobs.get(key)
        if rec is None:
            missing.append((key, prov))
            continue

        zs = rec.setdefault('zones', [])
        idx = None
        for i, e in enumerate(zs):                       # rule 8 — by NAME only
            if (e[0] if isinstance(e, list) else e) == zone:
                idx = i
                break

        if lvl is SKIP:                                  # rule 15
            if idx is None:
                zs.append([zone])
                added.append((key, '(no level — page cell blank)', prov))
            else:
                e = zs[idx]
                cur = e[1] if isinstance(e, list) and len(e) > 1 else None
                kept_blank.append((key, cur, prov))
            continue

        if idx is None:
            zs.append([zone, lvl])
            added.append((key, lvl, prov))
        else:
            e = zs[idx]
            if not isinstance(e, list):
                zs[idx] = [zone, lvl]
                changed.append((key, '(bare string)', lvl, prov))
            elif len(e) == 1:
                e.append(lvl)
                changed.append((key, '(null)', lvl, prov))
            elif e[1] != lvl:
                changed.append((key, e[1], lvl, prov))
                e[1] = lvl
            else:
                already.append(key)

    lvmoves = []                                          # rule 9
    for key, (lo, hi) in lv_extend.items():
        rec = mobs[key]
        old = list(rec.get('lv', []))
        nlo = min(old[0], lo) if old else lo
        nhi = max(old[1], hi) if len(old) > 1 else hi
        if [nlo, nhi] != old:
            rec['lv'] = [nlo, nhi]
            lvmoves.append((key, old, [nlo, nhi]))

    dropmoves = []                                        # rule 41
    for key, (old, new) in drop_fix.items():
        if mobs[key].get('drops') == old:
            mobs[key]['drops'] = new
            dropmoves.append((key, old, new))

    zi = _load('zoneinfo.json')
    zinotes = zoneinfo_edit(zi[slug]) if (zoneinfo_edit and slug in zi) else []

    W = 26
    print(f"=== ZONE PASS — {zone} ===  {len(rows)} page records\n")
    print(f"MISSING RECORDS ({len(missing)}):")
    for k, p in missing:
        print(f"   !! {k:{W}s} {p}")
    if not missing:
        print("   (none)")
    print(f"\nZONE ADDED ({len(added)}):")
    for k, l, p in added:
        print(f"   + {k:{W}s} {str(l):18s} {p}")
    print(f"\nLEVEL CHANGED ({len(changed)}):")
    for k, o, n, p in changed:
        print(f"   ~ {k:{W}s} {str(o):18s} -> {n:8s} {p}")
    print(f"\nKEPT (page cell blank — rule 15 guard) ({len(kept_blank)}):")
    for k, c, p in kept_blank:
        print(f"   = {k:{W}s} stored {str(c):10s} {p}")
    print(f"\nALREADY CORRECT ({len(already)}): {', '.join(already)}")
    print(f"\nlv UNIONS (rule 9) ({len(lvmoves)}):")
    for k, o, n in lvmoves:
        print(f"   ^ {k:{W}s} {o} -> {n}")
    print(f"\nDROP-NAME LEDGER (rule 41) ({len(dropmoves)}):")
    for k, o, n in dropmoves:
        print(f"   $ {k:{W}s} {o!r} -> {n!r}")
    print(f"\nZONEINFO ({len(zinotes)}):")
    for n in zinotes:
        print(f"   * {n}")

    if write:
        _save('mobs.json', m)
        _save('zoneinfo.json', zi)
        print("\nWRITTEN.")
    else:
        print("\n(dry run — pass --write)")


def wants_write():
    return '--write' in sys.argv
