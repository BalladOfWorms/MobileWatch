#!/usr/bin/env python3
"""
fz.py — fuzzy item-name search against ffxi_items.json.

ALWAYS run this before concluding a drop name is absent from the DB. An exact-match miss means
nothing: the DB abbreviates ("Orison Seal: Body" -> "Orison Seal: Bd.", "Nourishing Earring" ->
"Nourish. Earring") and it sometimes abbreviates THE MOB'S OWN NAME inside the drop ("Fistule
Discharge" -> "Fistl. Discharge", so search "Discharge", not "Fistule").

Usage:
    python3 fz.py <query> [more queries...]
    python3 fz.py --assets path/to/assets <query>

Author: BalladOfWorms
"""
import json, os, sys

args = sys.argv[1:]
assets = "app/src/main/assets"
if args and args[0] == "--assets":
    assets = args[1]
    args = args[2:]
if not args:
    print(__doc__)
    sys.exit(1)

items = json.load(open(os.path.join(assets, "ffxi_items.json")))
NAMES = sorted({v["n"] for v in items.values() if isinstance(v, dict) and "n" in v})
print(f"{len(NAMES)} item names loaded from {assets}/ffxi_items.json\n")

for q in args:
    exact = q in NAMES
    hits = [x for x in NAMES if q.lower() in x.lower()]
    print(f"=== {q!r}   exact={exact}   substring hits={len(hits)}")
    for h in hits:                      # NEVER truncate — a [:4] print once hid a valid item
        print(f"      {h}")
    if not hits:
        # try each word separately — the DB may abbreviate one of them
        for w in q.replace(":", " ").split():
            if len(w) < 4:
                continue
            sub = [x for x in NAMES if w.lower() in x.lower()]
            if sub:
                print(f"    word {w!r} -> {len(sub)} hits: {sub[:20]}")
    print()
