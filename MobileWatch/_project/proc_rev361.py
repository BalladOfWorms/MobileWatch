#!/usr/bin/env python3
"""rev 361 — Section X batch 7: the eight Flock Bat records.

USER: "double check that some of these arent just spelling errors." (5 BG pages + 3 AI panels.)

The spelling audit ran first and its results are in the review; nothing was renamed or merged here,
because a rename is a key change and every candidate needs a ruling. What this script does:

  * clears the eight red-X markers
  * applies the rev-360 grid ruling — all eight carried the same Bat/Flock Bat import default
    (`wk [Piercing +25, Ice +12.5, Wind +25, Lightning +12.5, Light +25] / st [Dark -50]`), and
    rule 328's test already settled it: no healthy record holds that grid.
  * stamps crys/job/kit/zones and fixes what the pages contradict
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
REVIEW_X = "mobimages/review_x.png"

d = json.load(open(P, encoding="utf-8"))
mobs, abilities = d["mobs"], d["abilities"]
zone_names = {z["name"] for z in json.load(open(os.path.join(ASSETS, "zones.json"), encoding="utf-8"))["zones"]}

LEGACY_WK = [["Piercing", "+25%"], ["Ice", "+12.5%"], ["Wind", "+25%"],
             ["Lightning", "+12.5%"], ["Light", "+25%"]]
BAT_WK = [["Piercing", "+25%"], ["Ranged", "+25%"], ["Fire", "+30%"], ["Wind", "+50%"],
          ["Lightning", "+30%"], ["Light", "+50%"], ["Ice", "+15%"], ["Earth", "+30%"],
          ["Water", "+30%"]]
BAT_ST = [["Dark", "-70%"]]
FLOCK_KIT = ["Jet Stream", "Sonic Boom", "Slipstream", "Turbulence"]

PAGES = {
    "depthdiver bats":  dict(zones=[("Woh Gates", None)]),
    "deviling bats":    dict(job="Warrior", agg=False, zones=[("Toraimarai Canal", "95-97")]),
    "fetor bats":       dict(job="Warrior", agg=False, zones=[("Outer Horutoto Ruins", "81-83")], resp=300),
    "fortalice bats":   dict(job="Warrior", zones=[("Garlaige Citadel", "92-96")]),
    "fulvous bats":     dict(job="Warrior", agg=False, zones=[("Cirdas Caverns", "119-121")],
                             det=["Sound"], clear_nm=True),
    "hemorraghic bats": dict(zones=[("Sih Gates", None)]),
    "troika bats":      dict(job="Warrior", zones=[("Inner Horutoto Ruins", "78-82")]),
    "whitenoise bats":  dict(agg=True, zones=[("RaKaznar Inner Court", None)]),
}

log, declined = [], []
for key, page in PAGES.items():
    m = mobs[key]
    assert m.get("fam") == "Flock Bat", key
    ch = []

    if m.get("img") == REVIEW_X:
        del m["img"]; ch.append("cleared review_x")

    assert m["wk"] == LEGACY_WK, (key, m["wk"])
    m["wk"] = [r[:] for r in BAT_WK]
    m["st"] = [r[:] for r in BAT_ST]
    ch.append("family grid")

    if not m.get("crys"):
        m["crys"] = "Wind"; ch.append("crys=Wind")

    if page.get("job") and not m.get("job"):
        m["job"] = page["job"]; ch.append(f"job={page['job']}")

    if not m.get("ab"):
        m["ab"] = list(FLOCK_KIT); ch.append(f"ab={len(m['ab'])}")

    # documented recurring bad stamp: ['Sight', ..., 'True Sight']
    if page.get("det") and m.get("det") != page["det"]:
        declined.append(f"{key}: det {json.dumps(m.get('det'))} -> {json.dumps(page['det'])} (bad stamp)")
        m["det"] = list(page["det"]); ch.append("det cleaned")

    if page.get("clear_nm") and m.get("nm"):
        del m["nm"]
        declined.append(f"{key}: nm CLEARED — its page carries no Notorious Monster banner (rule 326)")
        ch.append("nm CLEARED")

    if page.get("agg") is False and m.get("agg"):
        del m["agg"]; ch.append("agg CLEARED")
    elif page.get("agg") is True and not m.get("agg"):
        m["agg"] = True; ch.append("agg=True")

    if page.get("resp") and m.get("resp") != page["resp"]:
        declined.append(f"{key}: resp {m.get('resp')} -> {page['resp']} (page prints 5 minutes)")
        m["resp"] = page["resp"]; ch.append("resp")

    newz = []
    for zn, lv in page["zones"]:
        assert zn in zone_names, f"{key}: zone {zn!r} not in zones.json"
        newz.append([zn, lv] if lv else [zn])
    if m.get("zones") != newz:
        if m.get("zones"):
            declined.append(f"{key}: zones {json.dumps(m['zones'])} -> {json.dumps(newz)} (mob page wins)")
        m["zones"] = newz; ch.append("zones")

    log.append(f"  {key:18s} {', '.join(ch)}")

# ---- guards -------------------------------------------------------------
bad = [(k, a) for k in PAGES for a in mobs[k].get("ab", []) if a not in abilities]
assert not bad, bad
assert not [k for m in mobs.values() for k, v in m.items() if v is None], "null poison"
assert not [k for k in PAGES if mobs[k].get("img") == REVIEW_X]
for k in PAGES:
    for zn, *_ in mobs[k].get("zones") or []:
        assert zn in zone_names, (k, zn)

json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("rev 361 — Section X batch 7 (Flock Bat, 8)")
print("\n".join(log))
print("\nDECLINED / OVERRIDDEN:")
print("\n".join("  " + x for x in declined) or "  (none)")
print(f"\nreview_x remaining: {sum(1 for v in mobs.values() if v.get('img') == REVIEW_X)}")
left = [k for k, v in mobs.items() if v.get("wk") == LEGACY_WK]
print(f"still on the Bat import grid: {len(left)} -> {left}")
