#!/usr/bin/env python3
"""Dynamis-Tavnazia — the columns rev 206 left on the table (rev 208).

Rev 206 took the NAMES out of the Hydra / Kindred / Nightmare roster tables and zoned
them. It did not take the Location column, the Notable Drops column, or the two
floor-and-relic footers. This does.

Drops policy (§7): "Any Relic Legs -1" is a CLASS, not an item -> notes. Dynamis
currency is schema-homeless -> skipped (the procs chart already carries it per group).
Only real item names go in `drops`.
"""
import json, sys, os, re

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
d = json.load(open(P, encoding="utf-8"))
M = d["mobs"]

JOBS = ["Bard", "Beastmaster", "Black Mage", "Dark Knight", "Dragoon", "Monk",
        "Ninja", "Paladin", "Ranger", "Red Mage", "Samurai", "Summoner", "Thief",
        "Warrior", "White Mage"]
HYD = ["hydra " + j.lower() for j in JOBS] + ["hydra's hound", "hydra's wyvern", "hydra's avatar"]
KIN = ["kindred " + j.lower() for j in JOBS] + ["kindred's vouivre", "kindred's wyvern", "kindred's avatar"]

NOTES = {
    # Nightmare Location column
    "nightmare bugard": ["Spawns at the Phomiuna Aqueducts entrance, on the first floor.",
                         "Can drop any Relic Legs -1."],
    "nightmare cluster": ["Third floor, ring area.", "Can drop any Relic Body -1."],
    "nightmare hornet": ["Second floor, in the hallways.", "Can drop any Relic Legs -1."],
    "nightmare leech": ["Third floor, in the hallways.", "Can drop any Relic Body -1."],
    "nightmare makara": ["Second floor, underground past the Tauri.", "Can drop any Relic Legs -1."],
    "nightmare taurus": ["Second floor, in the side area leading underground near the Hydra.",
                         "Drops pieces from the Hydra Doublet, Jupon, Harness and Haubert sets."],
    "nightmare worm": ["Second floor, ring area.", "Can drop any Relic Legs -1."],
    # shared record -> zone-qualified
    "vanguard eye": ["In Dynamis-Tavnazia it spawns in the third-floor underground area."],
}
FOOTER_H = "In Dynamis-Tavnazia the Hydra are on the second floor, and can drop any Relic Armor from Dynamis-Beaucedine."
FOOTER_K = "In Dynamis-Tavnazia the Kindred are on the third floor, and can drop any Relic Armor from Dynamis-Xarcabard."
for k in HYD: NOTES.setdefault(k, []).append(FOOTER_H)
for k in KIN: NOTES.setdefault(k, []).append(FOOTER_K)

# wiki "Forgotten Thought" -> DB "Frgtn. Thought" (fuzzy-verified; exact match was 0 hits)
DROPS = {"nightmare worm": "Frgtn. Thought"}

# §5 first rule: provenance prose never goes in a notes field. This one is a
# resist-grid derivation note that leaked in during the Pugil pass.
PROVENANCE = re.compile(r'^This grid as "Pugil Resistances"')

noted, dropped, purged = [], [], []
for k, texts in NOTES.items():
    m = M[k]
    ns = m.get("notes") or []
    for t in texts:
        if t not in ns:
            ns.append(t); noted.append(k)
    m["notes"] = ns

for k, v in DROPS.items():
    cur = (M[k].get("drops") or "").strip()
    if v not in cur:
        M[k]["drops"] = (cur + ", " + v).lstrip(", ") if cur else v
        dropped.append((k, M[k]["drops"]))

for k, m in M.items():
    ns = m.get("notes")
    if not ns: continue
    keep = [t for t in ns if not PROVENANCE.match(t)]
    if len(keep) != len(ns):
        purged.append(k)
        if keep: m["notes"] = keep
        else: del m["notes"]

assert not [k for m in M.values() for k, v in m.items() if v is None], "null poison"
json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

from collections import Counter
print("notes added to  :", len(set(noted)), "records,", len(noted), "lines")
print("  nightmare/eye :", sorted(k for k in set(noted) if not k.startswith(("hydra", "kindred"))))
print("  hydra/kindred :", len([k for k in set(noted) if k.startswith(("hydra", "kindred"))]))
print("drops filled    :", dropped)
print("provenance note purged from:", purged)
