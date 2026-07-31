#!/usr/bin/env python3
"""
Rev 342 — one-line correction to trusts.json.

Lehko Habhoka's box (re-sent in the rev-342 batch) reads **Inspirit**, not "Insprint".
The ability name appears twice: once in `ws`, once in the Special Features bullet.
LOAD-MERGE-WRITE (rule 286) — reads the live file, edits in place.
Author: BalladOfWorms
"""
import json, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
PATH = f"{ASSETS}/trusts.json"

with open(PATH, encoding="utf-8") as f:
    d = json.load(f)

hits = 0
for t in d["trusts"]:
    if t["n"] != "Lehko Habhoka":
        continue
    for field in ("ws", "feat"):
        new = [s.replace("Insprint", "Inspirit") for s in t[field]]
        hits += sum(1 for a, b in zip(t[field], new) if a != b)
        t[field] = new

assert hits == 2, f"expected 2 replacements, made {hits}"
assert not [k for t in d["trusts"] for k, v in t.items() if v is None]
print("replacements:", hits, "| trusts:", len(d["trusts"]))

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, separators=(", ", ": "))
print("written", PATH)
