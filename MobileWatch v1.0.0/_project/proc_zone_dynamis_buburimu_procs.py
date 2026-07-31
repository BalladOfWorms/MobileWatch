#!/usr/bin/env python3
"""Dynamis-Buburimu stagger chart (rev 209) — BalladOfWorms.

The chart asked for at rev 207. It closes both halves of that open item at once:
  - zoneinfo.dynamis_buburimu.procs was the only empty Dreamland chart -> 3 rows
  - four unzoned Nightmares are named on it -> Buburimu's nine are complete

Row order follows the stored convention in the other three zones (by currency:
T. Whiteshell, 1 Byne Bill, O. Bronzepiece), not the page's own order, and `t` uses
the short family name without the "Nightmare " prefix — same as Valkurm and Qufim.
"""
import json, sys, os

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
PM = os.path.join(ASSETS, "mobs.json")
PZ = os.path.join(ASSETS, "zoneinfo.json")
d = json.load(open(PM, encoding="utf-8"))
M = d["mobs"]
Z = json.load(open(PZ, encoding="utf-8"))

ZONE = "Dynamis-Buburimu"
TAG = "Dynamis: " + ZONE
FILL = ["nightmare bunny", "nightmare eft", "nightmare mandragora", "nightmare dhalmel"]

added = []
for k in FILL:
    m = M[k]
    zs = m.get("zones") or []
    if not any(e and e[0] == ZONE for e in zs):
        zs.append([ZONE]); m["zones"] = zs
    ct = list(m.get("content") or [])
    if TAG not in ct:
        ct.append(TAG); m["content"] = ct
    added.append(k)

PROCS = [
    {"t": "Crab, Dhalmel, Scorpion", "w1": "WS", "w2": "MA", "w3": "JA",
     "cur": "T. Whiteshell", "jobs": "PLD, BRD, DRG, MNK"},
    {"t": "Crawler, Raven, Uragnite", "w1": "JA", "w2": "WS", "w3": "MA",
     "cur": "1 Byne Bill", "jobs": "DRK, BLU, RDM, NIN"},
    {"t": "Bunny, Eft, Mandragora", "w1": "MA", "w2": "JA", "w3": "WS",
     "cur": "O. Bronzepiece", "jobs": "PUP, BLM, RNG, WAR"},
]
before = len(Z[ZONE.lower().replace("-", "_")].get("procs") or [])
Z["dynamis_buburimu"]["procs"] = PROCS

assert not [k for m in M.values() for k, v in m.items() if v is None], "null poison"
json.dump(d, open(PM, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)
json.dump(Z, open(PZ, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("zoned to", ZONE, ":", added)
print("procs rows: %d -> %d" % (before, len(PROCS)))
print()
print("Buburimu Nightmares now:")
for k in sorted(M):
    if k.startswith("nightmare") and any(e[0] == ZONE for e in (M[k].get("zones") or [])):
        print("   %-24s lv=%s" % (k, M[k].get("lv")))
print()
print("Nightmare records STILL with no zone:")
for k in sorted(M):
    if k.startswith("nightmare") and not M[k].get("zones"):
        print("   %-24s lv=%s" % (k, M[k].get("lv")))
print()
print("procs rows per Dreamland zone:")
for s in ("dynamis_valkurm", "dynamis_buburimu", "dynamis_qufim", "dynamis_tavnazia"):
    print("   %-18s %d" % (s, len(Z[s].get("procs") or [])))
