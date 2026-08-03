#!/usr/bin/env python3
"""Dynamis boss-tier correction (rev 201) — BalladOfWorms / MobileWatch.

USER: "note the arch mega boss and mega boss"

BG-wiki's classic-Dynamis NM tables label TWO tiers, not one:
    Tzee Xicu Idol      Mega Boss        Arch Tzee Xicu Idol      Arch Mega Boss
    Overlord's Tombstone Mega Boss       Arch Overlord Tombstone  Arch Mega Boss
    Gu'Dha Effigy       Mega Boss        Arch Gu'Dha Effigy       (page says Mega Boss)
    Goblin Golem        Mega Boss        Arch Goblin Golem        (page says NM)
    Angra Mainyu        (page: Zone Boss) Arch Angra Mainyu       (page: Mega Boss)

STRUCTURE decides where the page wording wobbles: the plain statue is one of the five
Fiendish-Tome droppers, the Arch is spawned by trading all five. So the plain statue is
always the Mega Boss and the Arch is always the Arch Mega Boss.

Roles written: ": Mega" (rank -1) and ": Arch Mega" (rank -2), replacing rev-199's
": Boss" on the four city Archs and rev-200's ": Mega" on Arch Angra Mainyu.
"""
import json, sys, os

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
d = json.load(open(P, encoding="utf-8"))
M = d["mobs"]

PAIRS = [
    ("Dynamis-Windurst",    "tzee xicu idol",        "arch tzee xicu idol"),
    ("Dynamis-San d'Oria",  "overlord's tombstone",  "arch overlord tombstone"),
    ("Dynamis-Bastok",      "gu'dha effigy",         "arch gu'dha effigy"),
    ("Dynamis-Jeuno",       "goblin golem",          "arch goblin golem"),
    ("Dynamis-Beaucedine",  "angra mainyu",          "arch angra mainyu"),
]

changed = []
for zone, mega, arch in PAIRS:
    base = "Dynamis: " + zone
    for key, role in ((mega, "Mega"), (arch, "Arch Mega")):
        m = M[key]
        want = base + ": " + role
        old = [t for t in m["content"] if t == base or t.startswith(base + ":")]
        if old == [want]:
            continue
        m["content"] = [t for t in m["content"] if t not in old] + [want]
        changed.append((key, old[0] if old else "(none)", want))

assert not [k for m in M.values() for k, v in m.items() if v is None], "null poison"
json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

for k, o, n in changed:
    print("  %-26s %-40s -> %s" % (k, o, n))
print("changed:", len(changed))
