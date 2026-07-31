#!/usr/bin/env python3
"""rev 357 — Section X batch 2: the ten Demon records, plus the USER RULING on grids.

USER: "keep the family resist table for garrison type mobs, they are low level and old so im
sure they werent changed for the content. hanbis demon is a demon. all demons here are of the
red variety"

Three things:
  1. RULING — the rev-356 open closes. Garrison-event mobs take their family's resist table;
     the one-entry `+25%` grid was an import default, not a measurement. Applied to the 15
     Garrison records (11 Goblin + 4 Antica) AND to the rest of the two batches, which are
     ordinary field mobs with the same junk grid.
  2. RED DEMONS — the RED variant grid has sat unused since rev 56 ("HELD — user defines which
     mobs next"). The user has now named its first ten members. FIRST USE.
  3. Section X batch 2 — the ten Demon pages stamped like the Goblins were.
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

# ---------------------------------------------------------------- family grids
GOBLIN_WK = [["Fire", "+30%"], ["Wind", "+30%"], ["Lightning", "+30%"], ["Light", "+50%"],
             ["Ice", "+30%"], ["Earth", "+30%"], ["Water", "+30%"]]
GOBLIN_ST = []
ANTICA_WK = [["Fire", "+15%"], ["Wind", "+50%"], ["Lightning", "+15%"], ["Light", "+30%"],
             ["Ice", "+30%"], ["Water", "+15%"]]
ANTICA_ST = [["Earth", "-50%"], ["Dark", "-50%"]]
# rev-56 RED Demon set, parked unused until now
DEMON_RED_WK = [["Light", "+15%"]]
DEMON_RED_ST = [["Magical", "-25%"], ["Fire", "-15%"], ["Wind", "-15%"], ["Lightning", "-15%"],
                ["Ice", "-15%"], ["Earth", "-15%"], ["Water", "-15%"], ["Dark", "-15%"]]
DEMON_KIT = ["Demonic Howl", "Hecatomb Wave", "Soul Drain"]

log = []

# ============================================================ 1. THE GRID RULING
GOBLIN_14 = ["goblin boss", "goblin doctor", "goblin doyen", "goblin duelist", "goblin flesher",
             "goblin gaoler", "goblin guide", "goblin metallurgist", "goblin pirate",
             "goblin professor", "goblin swindler", "goblin swordmaker", "goblin thespian",
             "goblin trailblazer"]
ANTICA_GARRISON = ["centurio xiii-v", "decurio xiii-lv", "princeps xiii-lxxxix", "triarius xiii-lix"]

for k in GOBLIN_14:
    m = mobs[k]
    assert m["wk"] == [["Light", "+25%"]], (k, m["wk"])
    m["wk"], m["st"] = [r[:] for r in GOBLIN_WK], list(GOBLIN_ST)
log.append(f"  grid ruling: Goblin family table onto {len(GOBLIN_14)} records (7 weaknesses, no resists)")

for k in ANTICA_GARRISON:
    m = mobs[k]
    assert m["wk"] == [["Wind", "+25%"]], (k, m["wk"])
    assert m["st"] == ANTICA_ST, (k, m["st"])
    m["wk"] = [r[:] for r in ANTICA_WK]
log.append(f"  grid ruling: Antica family table onto {len(ANTICA_GARRISON)} Garrison records")

# ============================================================ 2+3. DEMON BATCH
CZB, CZK = "Castle Zvahl Baileys [S]", "Castle Zvahl Keep [S]"
HANBI_NOTES = [
    "Summoned by Hanbi during the fight, in response to certain of its special attacks.",
    "Every demon left alive raises Hanbi's attack power, so clear them quickly — area-of-effect "
    "damage is the usual answer when several are up.",
]

PAGES = {
    "deathwreaker demon": dict(job="Warrior",     zones=[(CZB, "85")]),
    "demon aristocrat":   dict(job="Warrior", nm=True, zones=[("Xarcabard", None)],
                               garrison="Xarcabard", extra_ab=["Mighty Strikes"]),
    "demon condemner":    dict(job="Summoner",    zones=[(CZB, "82-83"), (CZK, "82-83")]),
    "demon corrupter":    dict(job="Dark Knight", zones=[(CZB, "82-83"), (CZK, "82-83")]),
    "demon entomber":     dict(job="Black Mage",  zones=[(CZB, "82-83"), (CZK, "82-83")]),
    "demon suppressor":   dict(job="Warrior",     zones=[(CZB, "82-83"), (CZK, "82-83")]),
    "foredoomer demon":   dict(job="Summoner",    zones=[(CZB, "85-86")],
                               notes=["Assisted by a Demon's Elemental."]),
    "hanbi's demon":      dict(zones=[("Escha RuAun", None)],
                               content=["Geas Fete: Escha RuAun: Tier 2"], notes=HANBI_NOTES),
    "soulsearer demon":   dict(job="Black Mage",  zones=[(CZB, "85-86")], drops=["Fire IV"]),
    "woebringer demon":   dict(job="Dark Knight", zones=[(CZB, "85-86")]),
}

declined = []
for key, page in PAGES.items():
    m = mobs[key]
    assert m.get("fam") == "Demon", key
    ch = []

    if m.get("img") == REVIEW_X:
        del m["img"]; ch.append("cleared review_x")

    # RED grid — user ruling, first use of the rev-56 parked set
    assert m["wk"] == [["Light", "+25%"]], (key, m["wk"])
    m["wk"] = [r[:] for r in DEMON_RED_WK]
    m["st"] = [r[:] for r in DEMON_RED_ST]
    ch.append("RED grid")

    if page.get("job"):
        if m.get("job"):
            declined.append(f"{key}: job already {m['job']!r}")
        else:
            m["job"] = page["job"]; ch.append(f"job={page['job']}")

    if not m.get("crys"):
        m["crys"] = "Dark"; ch.append("crys=Dark")

    if page.get("nm") and not m.get("nm"):
        m["nm"] = True; ch.append("nm=True")

    if not m.get("ab"):
        m["ab"] = list(DEMON_KIT) + list(page.get("extra_ab") or [])
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
            declined.append(f"{key}: zones {json.dumps(m['zones'])} -> {json.dumps(newz)} (mob page wins)")
        m["zones"] = newz; ch.append("zones")

    if page.get("garrison") and not m.get("spawn"):
        m["spawn"] = f"Garrison ({page['garrison']})"; ch.append("spawn")

    if page.get("drops"):
        for it in page["drops"]:
            assert it in items, f"{key}: drop {it!r} not in ffxi_items.json"
        if m.get("drops"):
            declined.append(f"{key}: drops already {m['drops']!r}")
        else:
            m["drops"] = ", ".join(page["drops"]); ch.append("drops")

    if page.get("content") and not m.get("content"):
        m["content"] = list(page["content"]); ch.append("content")

    if page.get("notes"):
        notes = m.setdefault("notes", [])
        for n in page["notes"]:
            if n not in notes:
                notes.append(n); ch.append("note")

    log.append(f"  {key:22s} {', '.join(ch)}")

# ---- guards -------------------------------------------------------------
watched = set(PAGES) | set(GOBLIN_14) | set(ANTICA_GARRISON)
bad = [(k, a) for k in watched for a in mobs[k].get("ab", []) if a not in abilities]
assert not bad, bad
assert not [k for m in mobs.values() for k, v in m.items() if v is None], "null poison"
assert not [k for k in PAGES if mobs[k].get("img") == REVIEW_X]
for k in watched:
    for zn, *rest in mobs[k].get("zones") or []:
        assert zn in zone_names, (k, zn)

json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("rev 357 — Section X batch 2 (Demon, 10) + the Garrison grid ruling")
print("\n".join(log))
print("\nDECLINED / OVERRIDDEN:")
print("\n".join("  " + x for x in declined) or "  (none)")
print(f"\nreview_x remaining: {sum(1 for v in mobs.values() if v.get('img') == REVIEW_X)}")
one = [k for k, v in mobs.items() if (v.get('wk') or []) and len(v['wk']) == 1 and v['wk'][0][1] == '+25%']
print(f"one-entry +25% legacy grids remaining: {len(one)}")
