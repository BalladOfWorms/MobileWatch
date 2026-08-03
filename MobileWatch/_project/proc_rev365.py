#!/usr/bin/env python3
"""rev 365 — Section X batch 15: thirteen records across thirteen different families.

USER: "more" (9 BG pages, 4 AI panels). The long tail starts here — one record per family, so the
grid decision had to be made thirteen times. Page corroboration decided it first, cohort second:

  KEPT (5) — `wyrm` (page: weak Water + Thunder, strong Fire + Ice; the FAMILY grid says Lightning
  −95% RESIST, i.e. it contradicts the page outright), `tainted treant` and `sentry sapling` (both
  print "Weak to: Dark, Fire" and both store exactly `wk [Fire +25, Dark +25]`; Treant also has a
  healthy non-red-X holder, `modron's druid`), `faygorger sheep` (page "Weak to: Fire, Lightning",
  grid `wk [Fire +25, Lightning +25]`, plus two healthy holders — `incensed lucerewe` and
  `territorial lucerewe`), `sahagin patriarch` (page "Weak to: Lightning / Strong to: Water",
  grid `wk [Lightning +25] / st [Water -50]`).
  REPLACED (8) — sole holder, no page corroboration, or the family grid fits the page BETTER:
  `faygorger ram`'s page says weak to **Water** and its stored grid has no weakness at all, while
  the family grid carries Water +30 AND the Ice −15 it already had.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
REVIEW_X = "mobimages/review_x.png"

d = json.load(open(P, encoding="utf-8"))
mobs, abilities = d["mobs"], d["abilities"]
zone_names = {z["name"] for z in json.load(open(os.path.join(ASSETS, "zones.json"), encoding="utf-8"))["zones"]}

G = {  # family grids, only for the records being re-gridded
    "Yagudo":     ([["Fire","+30%"],["Lightning","+30%"],["Light","+30%"],["Ice","+50%"],["Water","+30%"],["Dark","+30%"]], []),
    "Xzomit":     ([["Fire","+30%"],["Lightning","+30%"],["Ice","+30%"],["Earth","+30%"],["Water","+30%"]], []),
    "Wyvern":     ([["Wind","+30%"],["Earth","+30%"],["Light","+30%"],["Dark","+50%"]], [["Fire","-50%"],["Lightning","-10%"]]),
    "Tonberry":   ([["Fire","+15%"],["Wind","+15%"],["Lightning","+30%"],["Ice","+50%"]], [["Light","-50%"],["Water","-15%"]]),
    "Snoll":      ([["Fire","+15%"]], [["Wind","-15%"],["Lightning","-42%"],["Light","-15%"],["Ice","-15%"],["Earth","-15%"],["Water","-15%"],["Dark","-15%"]]),
    "Slug":       ([["Fire","+15%"],["Lightning","+15%"],["Ice","+15%"]], [["Impact","-25%"],["H2H","-25%"]]),
    "Sabotender": ([["Fire","+30%"],["Lightning","+30%"],["Ice","+50%"],["Dark","+50%"]], [["Light","-50%"],["Water","-50%"]]),
    "Ram":        ([["Fire","+15%"],["Wind","+15%"],["Lightning","+30%"],["Light","+15%"],["Earth","+15%"],["Water","+30%"],["Dark","+15%"]], [["Ice","-15%"]]),
}
K = {
    "Yagudo":     ["Howl", "Parry", "Double Kick", "Feather Storm", "Sweep"],
    "Xzomit":     ["Dual Strike", "Ink Cloud", "Mantle Pierce", "Molluscous Mutation", "Saline Coat", "Siphon Discharge"],
    "Treant":     ["Drill Branch", "Entangle", "Pinecone Bomb", "Leafstorm"],
    "Tonberry":   None,  # filled below from the 63-member majority
    "Snoll":      ["Berserk", "Cold Wave", "Freeze Rush", "Hypothermal Combustion"],
    "Slug":       ["Corrosive Ooze", "Fuscous Ooze", "Purulent Ooze", "Mucilaginous Ooze"],
    "Sheep":      ["Lamb Chop", "Rage", "Sheep Charge", "Sheep Song", "Feeble Bleat", "Sheep Bleat"],
    "Sapling":    ["Slumber Powder", "Sprout Smack", "Sprout Spin"],
    "Sahagin":    ["Bubble Armor", "Hydroball", "Hydro Shot", "Spinning Fin"],
    "Sabotender": ["Needleshot", "Photosynthesis", "1000 Needles"],
    "Ram":        ["Great Bleat", "Rage", "Ram Charge", "Rumble", "Booming Bleat", "Petribreath"],
    # Wyvern: NO family kit exists — 40 of 47 members store no `ab` at all, so nothing is stamped.
    "Wyvern":     None,
    "Wyrm":       None,
}
import collections
K["Tonberry"] = json.loads(collections.Counter(
    json.dumps(v.get("ab"), ensure_ascii=False) for v in mobs.values()
    if v.get("fam") == "Tonberry").most_common(1)[0][0])
K["Wyrm"] = json.loads(collections.Counter(
    json.dumps(v.get("ab"), ensure_ascii=False) for v in mobs.values()
    if v.get("fam") == "Wyrm" and v.get("ab")).most_common(1)[0][0])

SUCCOR = "Quest (Succor to the Sidhe)"
PAGES = {
    "yagudo follower": dict(fam="Yagudo", regrid=1, crys="Wind", job="Samurai", nm=True,
        zones=[("Meriphataud Mountains", None), ("West Sarutabaruta", None)],
        spawn="Garrison (Meriphataud Mountains, West Sarutabaruta)"),
    "warder's xzomit": dict(fam="Xzomit", regrid=1, crys="Varies", det=["Sound"],
        zones=[("Escha RuAun", None)], content=["Geas Fete: Escha RuAun: Nazar"],
        spawn="Geas Fete (summoned by the Warder of Justice)", extra_ab=["Mijin Gakure"],
        notes=["Summoned about 15 seconds into the Warder of Justice fight and roughly every 30 "
               "seconds after, up to eight at once; each one goes for whoever pulled the parent.",
               "Uses Mijin Gakure at low HP or after it has been up for a while, and can be slept "
               "with a lullaby."]),
    "scorched-snout wyvern": dict(fam="Wyvern", regrid=1, crys="Wind",
        zones=[("Jade Sepulcher", "99")]),
    "wyrm": dict(fam="Wyrm", crys=None, nm=True, det=["True Sight"], agg=True,
        zones=[("Balgas Dais", None)], spawn="BCNM (Early Bird Catches the Wyrm)"),
    "tainted treant": dict(fam="Treant", crys="Earth", nm=True, zones=[("Jugner Forest [S]", None)],
        spawn=SUCCOR),
    "tonberry decimator": dict(fam="Tonberry", regrid=1, crys="Light", job="Ninja", nm=True,
        zones=[("Yhoator Jungle", None)], spawn="Garrison (Yhoator Jungle)",
        notes=["Drops no gil and cannot be mugged."]),
    "powdery snoll": dict(fam="Snoll", regrid=1, crys="Ice", job="Warrior", det=["Sight", "Magic"],
        agg=True, zones=[("Woh Gates", "124-126")]),
    "slinking slug": dict(fam="Slug", regrid=1, crys="Water", det=["Sound", "Scent"],
        zones=[("Dho Gates", "121-123")]),
    "faygorger sheep": dict(fam="Sheep", crys="Earth", nm=True, zones=[("East Ronfaure [S]", None)],
        spawn=SUCCOR, notes=["Spawned alongside Faytrapper Vashgash."]),
    "sentry sapling": dict(fam="Sapling", crys="Earth", nm=True, zones=[("Jugner Forest [S]", None)],
        spawn=SUCCOR),
    "sahagin patriarch": dict(fam="Sahagin", crys="Water", job="Monk", nm=True,
        zones=[("Yuhtunga Jungle", None)], spawn="Garrison (Yuhtunga Jungle)",
        extra_ab=["Hundred Fists"]),
    "sabotender mercenario": dict(fam="Sabotender", regrid=1, crys="Water",
        zones=[("Western Altepa Desert", None)],
        spawn="Voidwatch (summoned by Sabotender Campeador)", extra_ab=["Chupa Blossom"],
        notes=["Four appear during the Sabotender Campeador fight, at the planar rifts around "
               "G-10, H-5 and L-6.",
               "Its Needles attacks scale up as its HP falls, and Chupa Blossom drains stats and "
               "HP from the party to strengthen the main NM."]),
    "faygorger ram": dict(fam="Ram", regrid=1, crys="Earth", job="Warrior", nm=True, lnk=True,
        zones=[("East Ronfaure [S]", None)], spawn=SUCCOR,
        notes=["Spawned alongside Faytrapper Vashgash."]),
}

log, declined = [], []
for key, page in PAGES.items():
    m = mobs[key]
    fam = page["fam"]
    assert m.get("fam") == fam, (key, m.get("fam"))
    ch = []

    if m.get("img") == REVIEW_X:
        del m["img"]; ch.append("cleared review_x")

    if page.get("regrid"):
        wk, st = G[fam]
        m["wk"] = [r[:] for r in wk]
        m["st"] = [r[:] for r in st]
        ch.append("family grid")

    if page.get("crys") and not m.get("crys"):
        m["crys"] = page["crys"]; ch.append(f"crys={page['crys']}")

    if page.get("job") and not m.get("job"):
        m["job"] = page["job"]; ch.append(f"job={page['job']}")

    if not m.get("ab") and K.get(fam):
        m["ab"] = list(K[fam]) + list(page.get("extra_ab") or [])
        ch.append(f"ab={len(m['ab'])}")
    elif not m.get("ab"):
        declined.append(f"{key}: no family kit to stamp ({fam} has none)")
    elif page.get("extra_ab"):
        for a in page["extra_ab"]:
            if a not in m["ab"]:
                m["ab"].append(a); ch.append(f"ab+={a}")

    if page.get("det") and m.get("det") != page["det"]:
        declined.append(f"{key}: det {json.dumps(m.get('det'))} -> {json.dumps(page['det'])}")
        m["det"] = list(page["det"]); ch.append("det")

    if page.get("nm") and not m.get("nm"):
        m["nm"] = True; ch.append("nm=True")
    if page.get("lnk") and not m.get("lnk"):
        m["lnk"] = True; ch.append("lnk=True")
    if page.get("agg") and not m.get("agg"):
        m["agg"] = True; ch.append("agg=True")

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
    if page.get("content") and not m.get("content"):
        m["content"] = list(page["content"]); ch.append("content")

    if page.get("notes"):
        notes = m.setdefault("notes", [])
        for n in page["notes"]:
            if n not in notes:
                notes.append(n); ch.append("note")

    log.append(f"  {key:24s} {', '.join(ch)}")

# ---- guards -------------------------------------------------------------
bad = [(k, a) for k in PAGES for a in mobs[k].get("ab", []) if a not in abilities]
assert not bad, bad
assert not [k for m in mobs.values() for k, v in m.items() if v is None], "null poison"
assert not [k for k in PAGES if mobs[k].get("img") == REVIEW_X]
for k in PAGES:
    for zn, *_ in mobs[k].get("zones") or []:
        assert zn in zone_names, (k, zn)

json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("rev 365 — Section X batch 15 (13 records, 13 families)")
print("\n".join(log))
print("\nDECLINED / OVERRIDDEN:")
print("\n".join("  " + x for x in declined) or "  (none)")
print(f"\nreview_x remaining: {sum(1 for v in mobs.values() if v.get('img') == REVIEW_X)}")
