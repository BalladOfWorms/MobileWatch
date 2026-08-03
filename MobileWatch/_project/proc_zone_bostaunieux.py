#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Bostaunieux Oubliette  (rev 149)

Sources: 4 uploaded shots of the BG-wiki zone page
  (1) zone info box, (2) Notorious Monsters table, (3)+(4) Adversaries table.

Honours the refining-phase rules in /areas/mobs-update-todo-9.md:
  r1  additive/corrective only  — a BLANK page cell never overwrites stored data
  r2  merged span per zone      — several page blocks collapse to ONE range
  r7  zone string = zones.json form ("Bostaunieux Oubliette")
  r8  test for the zone NAME, never for a level value
  r9  a level correction EXTENDS lv, never shrinks it
  r11 zone-present-but-null is NOT done — it is a level fill waiting
  r15 SKIP sentinel: a blank page cell CANNOT clear a stored level

Reports three buckets separately: added / changed / kept-because-blank.
"""
import json, os, sys

A = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
MOBS = os.path.join(A, 'mobs.json')
ZINF = os.path.join(A, 'zoneinfo.json')

ZONE = "Bostaunieux Oubliette"      # rule 7 — exactly the zones.json string
SLUG = "bostaunieux_oubliette"
SKIP = object()                      # rule 15 — "leave whatever is there"

# ---------------------------------------------------------------- page rows
# (mobs.json key, level string or SKIP, page-table provenance)
ROWS = [
    # --- Notorious Monsters ---------------------------------------------
    ("arioch",                   "~62",   "NM  Lottery(Werebat)"),
    ("sewer syrup",              "64-65", "NM  Lottery(Mousse)"),
    ("shii",                     "70",    "NM  Lottery(Garm)"),
    ("bloodsucker (nm)",         "71",    "NM  Timed 1hr Map 3"),
    ("drexerion the condemned",  "72-73", "NM  Timed 60-72hr"),
    ("phanduron the condemned",  "72-73", "NM  Timed 60-72hr"),
    ("manes",                    "72",    "NM  Lottery(Gespenst)"),
    ("bodach",                   SKIP,    "NM  Quest — Lv cell BLANK"),
    ("garbage gel",              "122",   "NM  UNM 1,800 accolades"),
    # --- Adversaries (ground + Fished-Up merged per rule 2) --------------
    ("dark aspic",               "52-54", "ADV 52-54"),
    ("funnel bats",              "52-55", "ADV 52-55"),
    ("werebat",                  "55-59", "ADV 55-59"),
    ("hecatomb hound",           "56-59", "ADV 56-59"),
    ("mousse",                   "58-68", "ADV ground 58-62 + fished 60-62 + fished 66-68"),
    ("haunt",                    "60-63", "ADV 60-63"),
    ("garm",                     "64-66", "ADV 64-66"),
    ("bloodsucker (monster)",    "52-68", "ADV fished 52-54 + fished 56-58 + ground 65-68"),
    ("gespenst",                 "68-70", "ADV 68-70"),
    ("dabilla",                  "94-97", "ADV 94-97"),
    ("panna cotta",              "94-97", "ADV 94-97"),
    ("blind bat",                "95-97", "ADV 95-97"),
    ("nachtmahr",                "96-97", "ADV 96-97"),
    ("wurdalak",                 "97-99", "ADV 97-99"),
    ("acid grease",              "52-54", "ADV Fished-Up 52-54"),
]

# rule 9 — lv unions forced by the corrections above
LV_EXTEND = {
    "mousse":                (58, 73),   # was [60,73]; zone min drops to 58
    "bloodsucker (monster)": (52, 68),   # was [52,62]; ground block reaches 68
    "panna cotta":           (94, 97),   # was [95,96]; page publishes 94-97
}

# abbreviation-ledger correction (rule 29 shape: found only by searching "crossbow")
DROP_FIX = {
    "drexerion the condemned": ("Flagellant's Crossbow, Shadow Mask",
                                "Flagel. Crossbow, Shadow Mask"),
}


def main():
    m = json.load(open(MOBS, encoding='utf-8'))
    mobs = m['mobs']

    missing, added, changed, kept_blank, already = [], [], [], [], []

    for key, lvl, prov in ROWS:
        rec = mobs.get(key)
        if rec is None:
            missing.append((key, prov))
            continue

        zs = rec.setdefault('zones', [])
        # rule 8 — locate by the zone NAME only, never by a level value
        idx = None
        for i, e in enumerate(zs):
            nm = e[0] if isinstance(e, list) else e
            if nm == ZONE:
                idx = i
                break

        if lvl is SKIP:
            if idx is None:
                zs.append([ZONE])
                added.append((key, '(no level — page cell blank)', prov))
            else:
                cur = zs[idx][1] if isinstance(zs[idx], list) and len(zs[idx]) > 1 else None
                kept_blank.append((key, cur, prov))
            continue

        if idx is None:
            zs.append([ZONE, lvl])
            added.append((key, lvl, prov))
        else:
            e = zs[idx]
            if not isinstance(e, list):
                zs[idx] = [ZONE, lvl]
                changed.append((key, '(bare string)', lvl, prov))
            elif len(e) == 1:
                e.append(lvl)
                changed.append((key, '(null)', lvl, prov))
            elif e[1] != lvl:
                changed.append((key, e[1], lvl, prov))
                e[1] = lvl
            else:
                already.append(key)

    # ---- rule 9 lv unions ------------------------------------------------
    lvmoves = []
    for key, (lo, hi) in LV_EXTEND.items():
        rec = mobs[key]
        old = list(rec.get('lv', []))
        nlo = min(old[0], lo) if old else lo
        nhi = max(old[1], hi) if len(old) > 1 else hi
        if [nlo, nhi] != old:
            rec['lv'] = [nlo, nhi]
            lvmoves.append((key, old, [nlo, nhi]))

    # ---- drop-name ledger fix -------------------------------------------
    dropmoves = []
    for key, (old, new) in DROP_FIX.items():
        rec = mobs[key]
        if rec.get('drops') == old:
            rec['drops'] = new
            dropmoves.append((key, old, new))

    # ---- zoneinfo --------------------------------------------------------
    zi = json.load(open(ZINF, encoding='utf-8'))
    e = zi[SLUG]
    zinotes = []

    # page publishes Weather: None; zones.json base is the bogus Sunshine/Clouds
    # pair. 91 other zones already carry exactly this override.
    if not e.get('weather'):
        e['weather'] = 'None'
        zinotes.append("weather override '' -> 'None'")

    # the Adversaries list was missing Bloodsucker entirely (all three blocks)
    if not any(x.get('n') == 'Bloodsucker' for x in e.get('mobs', [])):
        pos = next((i for i, x in enumerate(e['mobs']) if x.get('n') == 'Acid Grease'), 0)
        e['mobs'].insert(pos + 1, {"n": "Bloodsucker", "lv": "52-58, 65-68"})
        zinotes.append("mobs[] += Bloodsucker 52-58, 65-68")

    for nmrow in e.get('nms', []):
        if nmrow.get('n') == 'Garbage Gel' and not nmrow.get('drops'):
            nmrow['drops'] = ("Garbage's Coffer, G. Gel's Mucus, Gelatinous Ring, "
                              "Gelatinous Ring +1, Emeici, Emeici +1")
            zinotes.append("nms[Garbage Gel].drops filled")

    # ---- report ----------------------------------------------------------
    W = 26
    print(f"=== ZONE PASS — {ZONE} ===  {len(ROWS)} page rows\n")
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

    print(f"\nKEPT (page cell blank — rule 15 guard fired) ({len(kept_blank)}):")
    for k, c, p in kept_blank:
        print(f"   = {k:{W}s} stored {c}   {p}")

    print(f"\nALREADY CORRECT ({len(already)}): {', '.join(already)}")

    print(f"\nlv UNIONS (rule 9) ({len(lvmoves)}):")
    for k, o, n in lvmoves:
        print(f"   ^ {k:{W}s} {o} -> {n}")

    print(f"\nDROP-NAME LEDGER ({len(dropmoves)}):")
    for k, o, n in dropmoves:
        print(f"   $ {k:{W}s} {o!r} -> {n!r}")

    print(f"\nZONEINFO ({len(zinotes)}):")
    for n in zinotes:
        print(f"   * {n}")

    if '--write' in sys.argv:
        # compact, ensure_ascii=False — matches the on-disk format exactly
        json.dump(m, open(MOBS, 'w', encoding='utf-8'), ensure_ascii=False)
        json.dump(zi, open(ZINF, 'w', encoding='utf-8'), ensure_ascii=False)
        print("\nWRITTEN.")
    else:
        print("\n(dry run — pass --write)")


if __name__ == '__main__':
    main()
