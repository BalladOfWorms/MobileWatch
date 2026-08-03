#!/usr/bin/env python3
"""Nightmare zone fills from the stagger-proc charts (rev 207) — BalladOfWorms.

The two new shots are DYNAMIS-QUFIM, not Tavnazia:
  - the "Monsters Found Here" note names **Delkfutt's Tower**, which is Qufim Island
  - the nine Nightmare rows (Snoll/Stirge/Weapon, Gaylas/Kraken/Roc, Diremite/Raptor/
    Tiger) are exactly `zoneinfo.dynamis_qufim.procs`, same three stagger groups, same
    currencies; six of the nine already carry Dynamis-Qufim in mobs.json.
Tavnazia's Nightmares are a different set entirely (Antlion, Bugard, Cluster, Hornet,
Leech, Makara, Taurus, Worm) and were all placed at rev 206.

So the shot fills three holes at Qufim — and the SAME projection works at Valkurm from
a chart that has been sitting in zoneinfo all along (the rev-192 "check whether the
roster is already derivable" trick).
"""
import json, sys, os

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
PM = os.path.join(ASSETS, "mobs.json")
PZ = os.path.join(ASSETS, "zoneinfo.json")

d = json.load(open(PM, encoding="utf-8"))
M = d["mobs"]
Z = json.load(open(PZ, encoding="utf-8"))

FILLS = {
    "Dynamis-Qufim": ["nightmare roc", "nightmare raptor", "nightmare tiger"],
    "Dynamis-Valkurm": ["nightmare goobbue", "nightmare manticore", "nightmare sheep"],
}

added = []
for zone, keys in FILLS.items():
    tag = "Dynamis: " + zone
    for k in keys:
        m = M[k]
        zs = m.get("zones") or []
        if not any(e and e[0] == zone for e in zs):
            zs.append([zone]); m["zones"] = zs
        ct = list(m.get("content") or [])
        if tag not in ct:
            ct.append(tag); m["content"] = ct
        added.append((k, zone))

# the shot spells it "Nightmare Weapon"; the stored proc row reads "Weapom"
fixed = []
for row in Z["dynamis_qufim"]["procs"]:
    if "Weapom" in row["t"]:
        row["t"] = row["t"].replace("Weapom", "Weapon"); fixed.append(row["t"])

# "Monsters Found Here" note, zone-qualified because the record is shared across 5 zones
note = "In Dynamis-Qufim the Goblin statues are found near Delkfutt's Tower and in the tunnels."
ns = M["goblin statue"].get("notes") or []
noted = note not in ns
if noted:
    ns.append(note); M["goblin statue"]["notes"] = ns

assert not [k for m in M.values() for k, v in m.items() if v is None], "null poison"
assert not [e for m in M.values() for e in (m.get("zones") or []) if len(e) > 1 and not e[1]], "empty zone level"
json.dump(d, open(PM, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)
json.dump(Z, open(PZ, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

for k, z in added: print("  zoned  %-22s -> %s" % (k, z))
print("procs typo fixed :", fixed)
print("goblin statue note:", noted)

# what is still unplaced
print()
print("Nightmare records with NO zone:")
for k in sorted(M):
    if k.startswith("nightmare") and not M[k].get("zones"):
        print("   ", k, M[k].get("lv"))
print()
print("procs chart rows per Dreamland zone:")
for s in ("dynamis_valkurm", "dynamis_buburimu", "dynamis_qufim", "dynamis_tavnazia"):
    print("   %-18s %d" % (s, len(Z[s].get("procs") or [])))
