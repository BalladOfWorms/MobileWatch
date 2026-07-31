#!/usr/bin/env python3
"""rev 356 — Section X batch 1: the fourteen Goblin records marked with the red X.

User: "these are some mobs we had marked with an 'x' to look into more, they should be
good now and can get the regular icon" + 14 BG-wiki mob pages.

Per record: drop the review_x marker (falls back to mobicons/Goblin.jpg), then stamp
everything the page actually prints — job, crystal, zone, Garrison spawn, drops, NM flag,
the no-gil/no-mug note — plus the standard Goblin family kit (additive, none had `ab`).

NOT touched, deliberately:
  * `wk` — every one of these carries the legacy one-entry grid [["Light","+25%"]] while
    the family grid is 7 entries topped by Light +50%. Rule 1 (never overwrite a measured
    value) and the rev-355 Antica-Garrison precedent both say leave it; logged as an open.
  * `det` — pages print "A, L, S" = Sight, and the legend has a separate "Sc = Follows by
    Scent", so the page is not silently omitting Scent. Rule 4: mob page outranks family.
  * Animal Glue (Trailblazer) — crafting material, omitted per the drops convention.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
REVIEW_X = "mobimages/review_x.png"
KIT = ["Goblin Rush", "Bomb Toss", "Bomb Toss (Dropped)", "Smokebomb", "Crispy Candle"]
NOGIL = "Drops no gil and cannot be mugged."

d = json.load(open(P, encoding="utf-8"))
mobs, abilities = d["mobs"], d["abilities"]
zone_names = {z["name"] for z in json.load(open(os.path.join(ASSETS, "zones.json"), encoding="utf-8"))["zones"]}
items = {v["n"] for v in json.load(open(os.path.join(ASSETS, "ffxi_items.json"), encoding="utf-8")).values()
         if isinstance(v, dict) and "n" in v}

# key -> page facts.  zones = [(zone, level-range-or-None)]
PAGES = {
    "goblin boss":         dict(job="Warrior",    nm=True,  zones=[("Cape Teriggan", None)],       garrison="Cape Teriggan"),
    "goblin doctor":       dict(job="White Mage",           zones=[("Cape Teriggan", None)],       garrison="Cape Teriggan", nogil=True),
    "goblin doyen":        dict(                  nm=True,  zones=[("The Sanctuary of ZiTah", None)], garrison="The Sanctuary of ZiTah"),
    "goblin duelist":      dict(job="Red Mage",             zones=[("Cape Teriggan", None)],       garrison="Cape Teriggan"),
    "goblin flesher":      dict(job="Warrior",              zones=[("Inner Horutoto Ruins", "79-82")],
                                drops=["Scale Cuisses", "Faceguard", "Goblin Helm", "Goblin Mail"]),
    "goblin gaoler":       dict(job="Dark Knight",          zones=[("Valkurm Dunes", None)],       garrison="Valkurm Dunes", nogil=True),
    "goblin guide":        dict(job="Dark Knight",          zones=[("Buburimu Peninsula", None)],  garrison="Buburimu Peninsula", nogil=True),
    "goblin metallurgist": dict(                            zones=[("Inner Horutoto Ruins", "78-82")],
                                drops=["Goblin Mail", "Goblin Helm"]),
    "goblin pirate":       dict(job="Thief",                zones=[("Cape Teriggan", None)],       garrison="Cape Teriggan", nogil=True),
    "goblin professor":    dict(job="Black Mage",           zones=[("Cape Teriggan", None)],       garrison="Cape Teriggan"),
    "goblin swindler":     dict(job="Thief",                zones=[("Valkurm Dunes", None)],       garrison="Valkurm Dunes",
                                extra_ab=["Perfect Dodge"]),
    "goblin swordmaker":   dict(job="Warrior",              zones=[("Valkurm Dunes", None), ("Buburimu Peninsula", None)],
                                garrison="Valkurm Dunes, Buburimu Peninsula"),
    "goblin thespian":     dict(job="Red Mage",             zones=[("Buburimu Peninsula", None)],  garrison="Buburimu Peninsula", nogil=True),
    "goblin trailblazer":  dict(job="Ranger",               zones=[("Inner Horutoto Ruins", "78-82")],
                                drops=["Goblin Armor", "Goblin Mask", "Leather Bandana"]),
}

log, declined = [], []
for key, page in PAGES.items():
    m = mobs[key]
    assert m.get("fam") == "Goblin", key
    changes = []

    if m.get("img") == REVIEW_X:
        del m["img"]
        changes.append("cleared review_x")

    if page.get("job"):
        if m.get("job"):
            declined.append(f"{key}: job already {m['job']!r}, page says {page['job']!r}")
        else:
            m["job"] = page["job"]
            changes.append(f"job={page['job']}")

    if not m.get("crys"):
        m["crys"] = "Fire"
        changes.append("crys=Fire")

    if page.get("nm") and not m.get("nm"):
        m["nm"] = True
        changes.append("nm=True")

    if not m.get("ab"):
        m["ab"] = list(KIT) + list(page.get("extra_ab") or [])
        changes.append(f"ab={len(m['ab'])}")
    elif page.get("extra_ab"):
        for a in page["extra_ab"]:
            if a not in m["ab"]:
                m["ab"].append(a)
                changes.append(f"ab+={a}")

    # zones: mob page outranks the zone/adversaries table (rule 4)
    newz = []
    for zn, lv in page["zones"]:
        assert zn in zone_names, f"{key}: zone {zn!r} not in zones.json"
        newz.append([zn, lv] if lv else [zn])
    old = m.get("zones")
    if old != newz:
        if old:
            declined.append(f"{key}: zones {json.dumps(old)} -> {json.dumps(newz)} (mob page wins)")
        m["zones"] = newz
        changes.append("zones")

    if page.get("garrison") and not m.get("spawn"):
        m["spawn"] = f"Garrison ({page['garrison']})"
        changes.append("spawn")

    if page.get("drops"):
        for it in page["drops"]:
            assert it in items, f"{key}: drop {it!r} not in ffxi_items.json"
        if m.get("drops"):
            declined.append(f"{key}: drops already {m['drops']!r}")
        else:
            m["drops"] = ", ".join(page["drops"])
            changes.append(f"drops={len(page['drops'])}")

    if page.get("nogil"):
        notes = m.setdefault("notes", [])
        if NOGIL not in notes:
            notes.append(NOGIL)
            changes.append("note")

    log.append(f"  {key:24s} {', '.join(changes)}")

# ---- guards -------------------------------------------------------------
bad_ab = [(k, a) for k in PAGES for a in mobs[k].get("ab", []) if a not in abilities]
assert not bad_ab, bad_ab
assert not [k for m in mobs.values() for k, v in m.items() if v is None], "null poison"
assert not [k for k in PAGES if mobs[k].get("img") == REVIEW_X]

json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("rev 356 — Section X batch 1 (Goblin, 14)")
print("\n".join(log))
print("\nDECLINED / OVERRIDDEN:")
print("\n".join("  " + x for x in declined) or "  (none)")
print(f"\nreview_x remaining: {sum(1 for v in mobs.values() if v.get('img') == REVIEW_X)}")
