#!/usr/bin/env python3
"""rev 362 — Section X batches 8+9: Bomb and Velkk.

USER: "completely remove iron and nail bomb, not relevant to bestiary" + 5 sources (1 BG page,
4 AI panels).

  * DELETE `iron bomb` and `nail bomb` outright — they were stubs (`lv [1, 80]` / `[1, 70]`
    placeholder bands, det [Sound] against the family's [Sight, Magic], nothing else).
  * `vulcanian bomb` — GRID KEPT. Rule 327's test passes: `kaboom`, a fully-stamped Bomb with a
    kit, crystal, job and a zone, holds the identical `wk [Fire +25] / 7-entry st`. A healthy
    record on the grid means it is a real variant, not the import default.
  * the four Velkk — GRID REPLACED. Rule 328's test fails hard, and the reason is decisive:
    their `wk [Wind +25] / st [Earth -50, Dark -50]` is the **ANTICA** import default. The only
    other holders are 4 Contanticans and 5 fam=None `hastatus`/`sagittarius` orphans. No Velkk
    outside these four has ever carried it; 27 of 33 hold the real family grid.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
REVIEW_X = "mobimages/review_x.png"

d = json.load(open(P, encoding="utf-8"))
mobs, abilities = d["mobs"], d["abilities"]
zone_names = {z["name"] for z in json.load(open(os.path.join(ASSETS, "zones.json"), encoding="utf-8"))["zones"]}
items = {v["n"] for v in json.load(open(os.path.join(ASSETS, "ffxi_items.json"), encoding="utf-8")).values()
         if isinstance(v, dict) and "n" in v}

log, declined = [], []

# ------------------------------------------------ 1. DELETIONS (user request)
for k in ["iron bomb", "nail bomb"]:
    assert mobs[k].get("img") == REVIEW_X, k
    del mobs[k]
    log.append(f"  {k:20s} DELETED (user: not relevant to the bestiary)")

# ------------------------------------------------ 2. family constants
BOMB_KIT = ["Berserk", "Self-Destruct", "Heat Wave", "Vulcanian Impact", "Hellstorm"]
VELKK_KIT = ["Death Spin", "Velkkan Pygmachia", "Glutinous Dart"]
VELKK_WK = [["Lightning", "+30%"], ["Ice", "+30%"]]
VELKK_ST = [["Water", "-50%"], ["Dark", "-30%"]]
ANTICA_IMPORT_WK = [["Wind", "+25%"]]
ANTICA_IMPORT_ST = [["Earth", "-50%"], ["Dark", "-50%"]]

VULC_NOTES = [
    "In the Apkallu Breeding assault it is susceptible to Lullaby and Sleep.",
    "In Operation: Black Pearl it appears in the third phase of each wave — very low HP and easy "
    "to clear with area damage, but it casts high-tier Fire magic.",
]

PAGES = {
    "vulcanian bomb":    dict(fam="Bomb", kit=BOMB_KIT, crys="Fire", job="Black Mage",
                              zones=[("Lebros Cavern", None)], notes=VULC_NOTES),
    "velkk archmagus":   dict(fam="Velkk", kit=VELKK_KIT, crys="Fire", regrid=True,
                              det=["Sight"], zones=[("Dho Gates", None)], drops=["Velkk Mask"]),
    "velkk cyclonicist": dict(fam="Velkk", kit=VELKK_KIT, crys="Fire", regrid=True,
                              det=["Sight"], zones=[("Dho Gates", None)], drops=["Velkk Mask"]),
    "velkk dreadnought": dict(fam="Velkk", kit=VELKK_KIT, crys="Fire", regrid=True,
                              det=["Sight"], zones=[("Dho Gates", "121-123"),
                                                    ("Marjami Ravine", "121-123")]),
    "velkk trampler":    dict(fam="Velkk", kit=VELKK_KIT, crys="Fire", regrid=True,
                              det=["Sight"], zones=[("Dho Gates", None)],
                              drops=["Voay Sword -1", "Velkk Necklace"]),
}

for key, page in PAGES.items():
    m = mobs[key]
    assert m.get("fam") == page["fam"], (key, m.get("fam"))
    ch = []

    if m.get("img") == REVIEW_X:
        del m["img"]; ch.append("cleared review_x")

    if page.get("regrid"):
        assert m["wk"] == ANTICA_IMPORT_WK and m["st"] == ANTICA_IMPORT_ST, (key, m["wk"], m["st"])
        m["wk"] = [r[:] for r in VELKK_WK]
        m["st"] = [r[:] for r in VELKK_ST]
        ch.append("family grid (was the ANTICA import default)")

    if page.get("det") and m.get("det") != page["det"]:
        declined.append(f"{key}: det {json.dumps(m.get('det'))} -> {json.dumps(page['det'])} "
                        f"(same import cohort as the grid; 27 of 33 Velkk are [Sight])")
        m["det"] = list(page["det"]); ch.append("det")

    if not m.get("crys"):
        m["crys"] = page["crys"]; ch.append(f"crys={page['crys']}")

    if page.get("job") and not m.get("job"):
        m["job"] = page["job"]; ch.append(f"job={page['job']}")

    if not m.get("ab"):
        m["ab"] = list(page["kit"]); ch.append(f"ab={len(m['ab'])}")

    newz = []
    for zn, lv in page["zones"]:
        assert zn in zone_names, f"{key}: zone {zn!r} not in zones.json"
        newz.append([zn, lv] if lv else [zn])
    if m.get("zones") != newz:
        if m.get("zones"):
            declined.append(f"{key}: zones {json.dumps(m['zones'])} -> {json.dumps(newz)}")
        m["zones"] = newz; ch.append("zones")

    if page.get("drops"):
        for it in page["drops"]:
            assert it in items, f"{key}: drop {it!r} not in ffxi_items.json"
        if m.get("drops"):
            declined.append(f"{key}: drops already {m['drops']!r}")
        else:
            m["drops"] = ", ".join(page["drops"]); ch.append(f"drops={len(page['drops'])}")

    if page.get("notes"):
        notes = m.setdefault("notes", [])
        for n in page["notes"]:
            if n not in notes:
                notes.append(n); ch.append("note")

    log.append(f"  {key:20s} {', '.join(ch)}")

# ---- guards -------------------------------------------------------------
bad = [(k, a) for k in PAGES for a in mobs[k].get("ab", []) if a not in abilities]
assert not bad, bad
assert not [k for m in mobs.values() for k, v in m.items() if v is None], "null poison"
assert "iron bomb" not in mobs and "nail bomb" not in mobs
for k in PAGES:
    for zn, *_ in mobs[k].get("zones") or []:
        assert zn in zone_names, (k, zn)

json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("rev 362 — Section X batches 8+9 (Bomb 3->1 kept, Velkk 4)")
print("\n".join(log))
print("\nDECLINED / OVERRIDDEN:")
print("\n".join("  " + x for x in declined) or "  (none)")
print(f"\nmobs: {len(mobs)} | review_x remaining: "
      f"{sum(1 for v in mobs.values() if v.get('img') == REVIEW_X)}")
