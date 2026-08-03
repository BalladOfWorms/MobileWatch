#!/usr/bin/env python3
"""rev 358 — Section X batches 3+4: the seven Acuex and four Pugil records.

USER: "pakacet's pugil is in escha ruann, pugil family" + 11 sources (7 BG pages, 4 AI panels).

Unlike Goblin/Demon these eleven already carry proper family GRIDS — the gap is kit, crystal,
job, zones and aggression. Drops are all crafting materials (Acuex Poison/Ore, Pugil Scales,
Fossilized Bone) and are omitted per the drops convention; no Acuex or Pugil record in the file
stores any of them, so that stays consistent.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
REVIEW_X = "mobimages/review_x.png"

d = json.load(open(P, encoding="utf-8"))
mobs, abilities = d["mobs"], d["abilities"]
zone_names = {z["name"] for z in json.load(open(os.path.join(ASSETS, "zones.json"), encoding="utf-8"))["zones"]}

ACUEX_KIT = ["Deadening Haze", "Foul Waters", "Pestilent Plume"]
PUGIL_KIT = ["Aqua Ball", "Intimidate", "Screwdriver", "Splash Breath", "Water Shield", "Water Wall"]

STONE_NOTES = [
    "Aggressive only to players taking part in the Reive.",
    "Guards the Knotted Roots during Woh Gates colonization reives.",
]
PAKECET_NOTES = [
    "A helper called out by Pakecet as its HP drops; killing Pakecet outright is usually faster "
    "than clearing the adds.",
]

PAGES = {
    # ---- Acuex (family kit / Water crystal / det [Sound]) --------------------
    "bilespouting acuex": dict(fam="Acuex", zones_add=[("Outer RaKaznar", "118-122")], agg=False),
    "coagulum acuex":     dict(fam="Acuex", zones_add=[("Cirdas Caverns", "120-122")], agg=True),
    "peevish acuex":      dict(fam="Acuex", agg=False),
    "pestiferous acuex":  dict(fam="Acuex", zones=[("Woh Gates", "121-124")]),
    "splotched acuex":    dict(fam="Acuex", zones=[("Moh Gates", None)]),
    "stonesoftener acuex": dict(fam="Acuex", nm=True, zones=[("Dho Gates", "110")],
                                spawn="Colonization Reive", notes=STONE_NOTES),
    "wheezing acuex":     dict(fam="Acuex", job="Warrior", zones=[("Woh Gates", "124-126")], agg=False),
    # ---- Pugil --------------------------------------------------------------
    "blackwater pugil":   dict(fam="Pugil", job="Warrior", agg=False),
    "gill pugil":         dict(fam="Pugil", job="Warrior", agg=True, spawn="Spawned by fishing"),
    "pakecet's pugil":    dict(fam="Pugil", zones=[("Escha RuAun", None)],
                               content=["Geas Fete: Escha RuAun: Tier 3"], notes=PAKECET_NOTES),
    "primordial pugil":   dict(fam="Pugil", zones=[("Bibiki Bay", None)]),
}
KIT = {"Acuex": ACUEX_KIT, "Pugil": PUGIL_KIT}

log, declined = [], []
for key, page in PAGES.items():
    m = mobs[key]
    fam = page["fam"]
    assert m.get("fam") == fam, (key, m.get("fam"))
    ch = []

    if m.get("img") == REVIEW_X:
        del m["img"]; ch.append("cleared review_x")

    if not m.get("crys"):
        m["crys"] = "Water"; ch.append("crys=Water")

    if page.get("job"):
        if m.get("job"):
            declined.append(f"{key}: job already {m['job']!r}")
        else:
            m["job"] = page["job"]; ch.append(f"job={page['job']}")

    if not m.get("ab"):
        m["ab"] = list(KIT[fam]); ch.append(f"ab={len(m['ab'])}")

    if page.get("nm") and not m.get("nm"):
        m["nm"] = True; ch.append("nm=True")

    # aggression — the Notes column's NA / A is explicit data
    if page.get("agg") is False and m.get("agg"):
        del m["agg"]
        ch.append("agg CLEARED (page prints NA)")
    elif page.get("agg") is True and not m.get("agg"):
        m["agg"] = True; ch.append("agg=True")

    def pair(zn, lv):
        assert zn in zone_names, f"{key}: zone {zn!r} not in zones.json"
        return [zn, lv] if lv else [zn]

    if page.get("zones"):
        newz = [pair(*z) for z in page["zones"]]
        if m.get("zones") != newz:
            if m.get("zones"):
                declined.append(f"{key}: zones {json.dumps(m['zones'])} -> {json.dumps(newz)} (mob page wins)")
            m["zones"] = newz; ch.append("zones")
    if page.get("zones_add"):
        z = m.setdefault("zones", [])
        for zn, lv in page["zones_add"]:
            if not any(r[0] == zn for r in z):
                z.append(pair(zn, lv)); ch.append(f"zones+={zn}")

    if page.get("spawn") and not m.get("spawn"):
        m["spawn"] = page["spawn"]; ch.append("spawn")

    if page.get("content") and not m.get("content"):
        m["content"] = list(page["content"]); ch.append("content")

    if page.get("notes"):
        notes = m.setdefault("notes", [])
        for n in page["notes"]:
            if n not in notes:
                notes.append(n); ch.append("note")

    log.append(f"  {key:22s} {', '.join(ch)}")

# ---- guards -------------------------------------------------------------
bad = [(k, a) for k in PAGES for a in mobs[k].get("ab", []) if a not in abilities]
assert not bad, bad
assert not [k for m in mobs.values() for k, v in m.items() if v is None], "null poison"
assert not [k for k in PAGES if mobs[k].get("img") == REVIEW_X]
for k in PAGES:
    for zn, *_ in mobs[k].get("zones") or []:
        assert zn in zone_names, (k, zn)

json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("rev 358 — Section X batches 3+4 (Acuex 7, Pugil 4)")
print("\n".join(log))
print("\nDECLINED / OVERRIDDEN:")
print("\n".join("  " + x for x in declined) or "  (none)")
print(f"\nreview_x remaining: {sum(1 for v in mobs.values() if v.get('img') == REVIEW_X)}")
