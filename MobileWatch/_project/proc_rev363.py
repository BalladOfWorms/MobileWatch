#!/usr/bin/env python3
"""rev 363 — Section X batch 10: the five Poroggo records.

USER: "next" (5 BG pages — two of them NPC-type pages).

GRIDS LEFT ALONE, and this is the first time the two grid tests DISAGREE. All five carry
`wk [Ice +12.5, Lightning +12.5] / st [Water -50, Light -50]`, a cohort of exactly the five red-X
records — rule 328's import-default signature. BUT rule 327 outranks it here: **`poroggo gourmand`'s
page prints "Weak to: Ice, Lightning" and "Strong to: Water", which matches THIS grid and
contradicts the 15-member family grid** (`wk [Lightning +15] / st [Light -70, Ice -30, Earth -15,
Water -80]` — Ice is a RESIST there). Overwriting would replace a grid the page agrees with by one
the page contradicts. Left as-is and filed as an open.
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

KIT5 = ["Frog Cheer", "Frog Song", "Magic Hammer", "Providence", "Water Bomb"]
KIT6 = KIT5 + ["Frog Chorus"]

GOURMAND_NOTES = [
    "Spawned for the quest Succor to the Sidhe, alongside six Poroggo's Toady.",
    "Low defence and easy to kite — it stops every few seconds to cast Poisonga and Drown.",
    "Frog Song (single-target Charm) while its HP is high, Frog Chorus (area Charm, about 25 yalms) "
    "once it is low. Either move revives every Toady that has been killed.",
    "The Toadies are easily slept.",
]
PRINCE_NOTES = [
    "Appears in campaign battles if a Poroggo Servant has been successfully influenced, assisted by "
    "three Servants.",
    "Casts assorted black magic; after Providence it gains extra spells including Death and Breakga.",
    "Frog Cheer reaches every player and allied force in range.",
]
SERVANT_NOTES = [
    "Influenced by trading it a Lufaise Fly; to trade more you must zone into Windurst Waters (S) "
    "and back out.",
    "Once allied, it fights in campaign battles alongside the Poroggo Prince.",
    "Uses no TP moves and casts no spells, but attacks quickly with Additional Effect: Weight.",
]

PAGES = {
    "poroggo excavator": dict(job="Black Mage", kit=KIT5, det=["True Sound"], agg=False,
                              zones=[("Toraimarai Canal", "97-99")],
                              notes=["Non-aggressive, but links with Flume Toads."]),
    "poroggo gourmand":  dict(job="Black Mage", kit=KIT6, det=["True Sound"], agg=True, lnk=True,
                              nm=True, zones=[("West Sarutabaruta [S]", None)],
                              spawn="Quest (Succor to the Sidhe)", notes=GOURMAND_NOTES),
    "poroggo prince":    dict(job="Black Mage", kit=KIT5,
                              zones=[("Windurst Waters [S]", None)],
                              spawn="Campaign", notes=PRINCE_NOTES),
    "poroggo servant":   dict(empty_kit=True,
                              zones=[("West Sarutabaruta [S]", None), ("Windurst Waters [S]", None)],
                              spawn="Campaign", notes=SERVANT_NOTES),
    "wretched poroggo":  dict(job="Black Mage", kit=KIT5, det=["Sight"], agg=True,
                              zones=[("Reisenjima", "122-124")],
                              drops=["Fern Stone", "Taupe Stone"],
                              notes=["Spawns among the Lentic Toads in rainy weather, and links "
                                     "with them."]),
}

log, declined = [], []
for key, page in PAGES.items():
    m = mobs[key]
    assert m.get("fam") == "Poroggo", key
    ch = []

    if m.get("img") == REVIEW_X:
        del m["img"]; ch.append("cleared review_x")

    if not m.get("crys"):
        m["crys"] = "Water"; ch.append("crys=Water")

    if page.get("job") and not m.get("job"):
        m["job"] = page["job"]; ch.append(f"job={page['job']}")

    if page.get("empty_kit"):
        # BLANK vs "None": the page states it outright, so an explicit [] is the right value
        if not m.get("ab"):
            m["ab"] = []; ch.append("ab=[] (page: uses no TP moves)")
        if not m.get("sp"):
            m["sp"] = []; ch.append("sp=[] (page: casts no spells)")
    elif not m.get("ab"):
        m["ab"] = list(page["kit"]); ch.append(f"ab={len(m['ab'])}")

    if page.get("det") and m.get("det") != page["det"]:
        declined.append(f"{key}: det {json.dumps(m.get('det'))} -> {json.dumps(page['det'])}")
        m["det"] = list(page["det"]); ch.append("det")

    if page.get("nm") and not m.get("nm"):
        m["nm"] = True; ch.append("nm=True")
    if page.get("lnk") and not m.get("lnk"):
        m["lnk"] = True; ch.append("lnk=True")

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
            declined.append(f"{key}: zones {json.dumps(m['zones'])} -> {json.dumps(newz)}")
        m["zones"] = newz; ch.append("zones")

    if page.get("spawn") and not m.get("spawn"):
        m["spawn"] = page["spawn"]; ch.append("spawn")

    if page.get("drops"):
        for it in page["drops"]:
            assert it in items, f"{key}: drop {it!r} not in ffxi_items.json"
        if not m.get("drops"):
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
assert not [k for k in PAGES if mobs[k].get("img") == REVIEW_X]
for k in PAGES:
    for zn, *_ in mobs[k].get("zones") or []:
        assert zn in zone_names, (k, zn)

json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("rev 363 — Section X batch 10 (Poroggo, 5)")
print("\n".join(log))
print("\nDECLINED / OVERRIDDEN:")
print("\n".join("  " + x for x in declined) or "  (none)")
print(f"\nreview_x remaining: {sum(1 for v in mobs.values() if v.get('img') == REVIEW_X)}")
