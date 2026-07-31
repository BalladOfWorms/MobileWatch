#!/usr/bin/env python3
"""rev 359 — Section X batch 5: the nine Gigas records.

USER: "more" (9 BG pages = exactly the Gigas (9) block).

GRIDS LEFT ALONE, and this time that is the right call for a reason the pages supply: all nine
carry `wk [Earth +12.5] / st [Ice -12.5, Lightning -50]`, and every page prints
**"Strong to: Ice, Lightning"** — which matches that grid and NOT the 81-member family grid
(`wk [Earth +30] / st [Lightning -50]`, no Ice). Four unmarked Gigas NMs share the same grid.
So it is a real variant, not the rev-357 import default.

THE RED BANNER IS NOT ALWAYS "Notorious Monster": four of these print **Expeditionary Force** in
the same red slot. Only the three that literally say Notorious Monster are NM-flagged.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
REVIEW_X = "mobimages/review_x.png"

d = json.load(open(P, encoding="utf-8"))
mobs, abilities = d["mobs"], d["abilities"]
zone_names = {z["name"] for z in json.load(open(os.path.join(ASSETS, "zones.json"), encoding="utf-8"))["zones"]}

GIGAS_KIT = ["Grand Slam", "Ice Roar", "Impact Roar", "Power Attack", "Lightning Roar",
             "Catapult", "Moribund Hack", "Trebuchet", "Colossal Blow", "Mercurial Strike"]

EF_SPAWN = "Sometimes spawned from a Beastman's Banner during Expeditionary Force"
BEAU, XARC, GHOYU = "Beaucedine Glacier", "Xarcabard", "Ghoyus Reverie"
EF_ZONES = [(BEAU, "45"), (XARC, "50")]

PAGES = {
    "gigas beastmaster": dict(job="Beastmaster", zones=EF_ZONES, spawn=EF_SPAWN, notes=[
        "Summons a Gigas's Tiger. If the pet is killed it may try to charm a player instead."]),
    "gigas clearcutter": dict(job="Ranger", nm=True, zones=[(BEAU, None)],
                              spawn="Garrison (Beaucedine Glacier)", extra_ab=["Eagle Eye Shot"]),
    "gigas flanker":     dict(job="Warrior", zones=[(GHOYU, None)],
                              spawn="Battlefield (A Feast for Gnats)", notes=[
        "The Ghoyu's Reverie version appears part-way through the A Feast for Gnats battlefield to "
        "reinforce the Quadavs."]),
    "gigas hillrazer":   dict(job="Monk", nm=True, zones=[(BEAU, None)],
                              spawn="Garrison (Beaucedine Glacier)", extra_ab=["Hundred Fists"]),
    "gigas monk":        dict(job="Monk", zones=EF_ZONES, spawn=EF_SPAWN, extra_ab=["Hundred Fists"]),
    "gigas overseer":    dict(job="Warrior", nm=True, zones=[(BEAU, None)],
                              spawn="Garrison (Beaucedine Glacier)", extra_ab=["Mighty Strikes"]),
    "gigas ranger":      dict(job="Ranger", zones=EF_ZONES, spawn=EF_SPAWN, extra_ab=["Eagle Eye Shot"]),
    "gigas trebucket":   dict(job="Ranger", zones=[(GHOYU, None)],
                              spawn="Battlefield (A Feast for Gnats)", notes=[
        "The Ghoyu's Reverie version is spawned by the A Feast for Gnats battlefield."]),
    "gigas warrior":     dict(job="Warrior", zones=EF_ZONES, spawn=EF_SPAWN, extra_ab=["Mighty Strikes"]),
}

log, declined = [], []
for key, page in PAGES.items():
    m = mobs[key]
    assert m.get("fam") == "Gigas", key
    ch = []

    if m.get("img") == REVIEW_X:
        del m["img"]; ch.append("cleared review_x")

    if not m.get("crys"):
        m["crys"] = "Ice"; ch.append("crys=Ice")

    if m.get("job"):
        declined.append(f"{key}: job already {m['job']!r}")
    else:
        m["job"] = page["job"]; ch.append(f"job={page['job']}")

    # the red banner: "Notorious Monster" only. "Expeditionary Force" is NOT an NM marker.
    if page.get("nm"):
        if not m.get("nm"):
            m["nm"] = True; ch.append("nm=True")
    elif m.get("nm"):
        declined.append(f"{key}: record says nm but page shows no Notorious Monster banner")

    if not m.get("ab"):
        m["ab"] = list(GIGAS_KIT) + list(page.get("extra_ab") or [])
        ch.append(f"ab={len(m['ab'])}")
    elif page.get("extra_ab"):
        for a in page["extra_ab"]:
            if a not in m["ab"]:
                m["ab"].append(a); ch.append(f"ab+={a}")

    newz = []
    for zn, lv in page["zones"]:
        assert zn in zone_names, f"{key}: zone {zn!r} not in zones.json"
        newz.append([zn, lv] if lv else [zn])
    if m.get("zones") != newz:
        if m.get("zones"):
            declined.append(f"{key}: zones {json.dumps(m['zones'])} -> {json.dumps(newz)}")
        m["zones"] = newz; ch.append("zones")

    if page.get("spawn") and not m.get("spawn"):
        m["spawn"] = page["spawn"]; ch.append("spawn")

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
assert not [k for k in PAGES if mobs[k].get("img") == REVIEW_X]
for k in PAGES:
    for zn, *_ in mobs[k].get("zones") or []:
        assert zn in zone_names, (k, zn)

json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("rev 359 — Section X batch 5 (Gigas, 9)")
print("\n".join(log))
print("\nDECLINED / OVERRIDDEN:")
print("\n".join("  " + x for x in declined) or "  (none)")
print(f"\nreview_x remaining: {sum(1 for v in mobs.values() if v.get('img') == REVIEW_X)}")
