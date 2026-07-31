#!/usr/bin/env python3
"""
rev 152 — (lr) CLOSED. USER: "be hya is 30."

`be'hya hundredwall` carried lv [30,30] + a zone entry of 30, but nmlv "80".
`MobDb.levelText` renders "Lv $nmlv" whenever nmlv is set, so the mob showed
Lv 80 from the Family view and Lv 30 from the Zone view (rule 47). The user has
settled it at 30, so `nmlv` was the wrong field.

Two writes, and only two — `lv` and the zone entry were already right:
  mobs.json      be'hya hundredwall .nmlv                 "80" -> "30"
  zoneinfo.json  palborough_mines.nms[Be'Hya ...].lv      "80" -> "30"

The zoneinfo row must move too: its nms[].lv is a MIRROR of nmlv (844/877 = 96%
file-wide, rule 46), so leaving it would just re-create the same contradiction
from the other side.

nmlv is set to "30" rather than deleted: 611 of 899 nmlv-bearing records restate
`lv` exactly, so that is the file's convention for a single-level NM.
"""
import json, os, sys

A = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '..', 'app', 'src', 'main', 'assets')
P = lambda f: os.path.join(A, f)
KEY, SLUG, DISP = "be'hya hundredwall", 'palborough_mines', "Be'Hya Hundredwall"
OLD, NEW = '80', '30'

m = json.load(open(P('mobs.json'), encoding='utf-8'))
zi = json.load(open(P('zoneinfo.json'), encoding='utf-8'))
rec = m['mobs'][KEY]

print("BEFORE")
print(f"  mobs.json   lv={rec['lv']}  nmlv={rec.get('nmlv')!r}  zones={rec.get('zones')}")
row = next(r for r in zi[SLUG]['nms'] if r.get('n') == DISP)
print(f"  zoneinfo    lv={row.get('lv')!r}")

if rec.get('nmlv') != OLD or row.get('lv') != OLD:
    sys.exit("ABORT: file is not in the expected pre-state.")

rec['nmlv'] = NEW
row['lv'] = NEW

# consistency assertions — all three level facts must now agree
assert rec['lv'] == [30, 30], rec['lv']
assert rec['nmlv'] == NEW
assert row['lv'] == NEW
zone_lv = next(e[1] for e in rec['zones'] if e[0] == 'Palborough Mines')
assert zone_lv == NEW, zone_lv

print("AFTER")
print(f"  mobs.json   lv={rec['lv']}  nmlv={rec['nmlv']!r}  zones={rec['zones']}")
print(f"  zoneinfo    lv={row['lv']!r}")
print("  -> lv, nmlv, the zone entry and zoneinfo now all read 30")

if '--write' in sys.argv:
    json.dump(m, open(P('mobs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump(zi, open(P('zoneinfo.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print("\nWRITTEN.")
else:
    print("\n(dry run — pass --write)")
