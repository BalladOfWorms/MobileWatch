#!/usr/bin/env python3
"""rev 360 — Section X batch 6: the eight Bat records.

USER: "more" (6 BG pages + 2 AI panels = exactly the Bat (8) block).

GRID RULING APPLIED. All eight carried the minority grid
  wk [Piercing +25, Ice +12.5, Wind +25, Lightning +12.5, Light +25] / st [Dark -50]
against the 77-member family grid
  wk [Piercing +25, Ranged +25, Fire +30, Wind +50, Lightning +30, Light +50, Ice +15,
      Earth +30, Water +30] / st [Dark -70].
Rev 359's Gigas test says "does anything CORROBORATE the minority grid?" — and here nothing does.
The pages print only a directional "Weak to: Wind, Light / Strong to: Dark", true of BOTH. The
decider is the cohort: 19 records file-wide hold that grid and **every single one is a record that
missed its family pass** — 8 red-X Bats, 8 red-X Flock Bats, the 2 fam=None orphans `balayang` and
`desmodus`, and `vampyr bats` (a Flock Bat still missing its crystal). ZERO fully-stamped records
carry it. That is the rev-357 import-default signature, so the family table wins (rule 320).
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

LEGACY_WK = [["Piercing", "+25%"], ["Ice", "+12.5%"], ["Wind", "+25%"],
             ["Lightning", "+12.5%"], ["Light", "+25%"]]
BAT_WK = [["Piercing", "+25%"], ["Ranged", "+25%"], ["Fire", "+30%"], ["Wind", "+50%"],
          ["Lightning", "+30%"], ["Light", "+50%"], ["Ice", "+15%"], ["Earth", "+30%"],
          ["Water", "+30%"]]
BAT_ST = [["Dark", "-70%"]]
BAT_KIT = ["Blood Drain", "Ultrasonics", "Marrow Drain", "Subsonics", "Supersonics", "Soul Accretion"]

REIVE_NOTES = [
    "Aggressive only to players taking part in the Reive.",
    "Guards the Knotted Roots during Woh Gates colonization reives.",
]

PAGES = {
    "covin bat":      dict(job="Warrior", agg=False, zones=[("Inner Horutoto Ruins", "81-83")]),
    "donjon bat":     dict(job="Warrior", agg=False, zones=[("Garlaige Citadel", "91-96")]),
    "draftrider bat": dict(nm=True, agg=True, zones=[("Dho Gates", "110")],
                           spawn="Colonization Reive", notes=REIVE_NOTES),
    "drearyeyed bat": dict(agg=True, zones=[("Cirdas Caverns", "119-121")],
                           notes=["Spawns around the north-eastern part of map 2."]),
    "esurient bat":   dict(zones=[("Sih Gates", "119-122")],
                           notes=["Drops crest cards used for Escutcheons."]),
    "grimfang bat":   dict(zones=[("Woh Gates", None)], drops=["S. Kindred Crest"]),
    "naraka bat":     dict(zones=[("Arrapago Reef", "87+")]),
    "warren bat":     dict(job="Warrior", agg=False, zones=[("Maze of Shakhrami", "86-88")],
                           notes=["Found around J-8 on map 1."]),
}

log, declined = [], []
for key, page in PAGES.items():
    m = mobs[key]
    assert m.get("fam") == "Bat", key
    ch = []

    if m.get("img") == REVIEW_X:
        del m["img"]; ch.append("cleared review_x")

    assert m["wk"] == LEGACY_WK, (key, m["wk"])
    m["wk"] = [r[:] for r in BAT_WK]
    m["st"] = [r[:] for r in BAT_ST]
    ch.append("family grid")

    if not m.get("crys"):
        m["crys"] = "Wind"; ch.append("crys=Wind")

    if page.get("job"):
        if m.get("job"):
            declined.append(f"{key}: job already {m['job']!r}")
        else:
            m["job"] = page["job"]; ch.append(f"job={page['job']}")

    if not m.get("ab"):
        m["ab"] = list(BAT_KIT); ch.append(f"ab={len(m['ab'])}")

    if page.get("nm") and not m.get("nm"):
        m["nm"] = True; ch.append("nm=True")

    if page.get("agg") is False and m.get("agg"):
        del m["agg"]; ch.append("agg CLEARED")
    elif page.get("agg") is True and not m.get("agg"):
        m["agg"] = True; ch.append("agg=True")

    newz = []
    for zn, lv in page["zones"]:
        assert zn in zone_names, f"{key}: zone {zn!r} not in zones.json"
        newz.append([zn, lv] if lv else [zn])
    if m.get("zones") != newz:
        if m.get("zones"):
            declined.append(f"{key}: zones {json.dumps(m['zones'])} -> {json.dumps(newz)} (mob page wins)")
        m["zones"] = newz; ch.append("zones")

    if page.get("spawn") and not m.get("spawn"):
        m["spawn"] = page["spawn"]; ch.append("spawn")

    if page.get("drops"):
        for it in page["drops"]:
            assert it in items, f"{key}: drop {it!r} not in ffxi_items.json"
        if m.get("drops"):
            declined.append(f"{key}: drops already {m['drops']!r}")
        else:
            m["drops"] = ", ".join(page["drops"]); ch.append("drops")

    if page.get("notes"):
        notes = m.setdefault("notes", [])
        for n in page["notes"]:
            if n not in notes:
                notes.append(n); ch.append("note")

    log.append(f"  {key:16s} {', '.join(ch)}")

# ---- guards -------------------------------------------------------------
bad = [(k, a) for k in PAGES for a in mobs[k].get("ab", []) if a not in abilities]
assert not bad, bad
assert not [k for m in mobs.values() for k, v in m.items() if v is None], "null poison"
assert not [k for k in PAGES if mobs[k].get("img") == REVIEW_X]
for k in PAGES:
    for zn, *_ in mobs[k].get("zones") or []:
        assert zn in zone_names, (k, zn)

json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("rev 360 — Section X batch 6 (Bat, 8)")
print("\n".join(log))
print("\nDECLINED / OVERRIDDEN:")
print("\n".join("  " + x for x in declined) or "  (none)")
print(f"\nreview_x remaining: {sum(1 for v in mobs.values() if v.get('img') == REVIEW_X)}")
left = [k for k, v in mobs.items() if v.get("wk") == LEGACY_WK]
print(f"still on the Bat import grid: {len(left)} -> {left}")
