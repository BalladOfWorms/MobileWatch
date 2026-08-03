#!/usr/bin/env python3
"""rev 364 — Section X batches 11-14: Imp (3), Qiqirn (3), Rafflesia (3), Skeleton (3).

USER: "next" (12 sources — 8 BG pages, 4 AI panels). Four families in one rev, and the grid test
split them two-and-two:

  REPLACED — Imp and Qiqirn. Both minority cohorts are EXACTLY the three red-X records, richness
  0-1, with no healthy holder anywhere in the file. Import default (rule 328).
  KEPT — Rafflesia and Skeleton. Skeleton's minority grid has 13 non-red-X holders, several fully
  stamped (`vanquished einherjar`, `sodden bones`, `skinnymalinks`...), and the Macabre panel's
  "weak to Fire, Light and Blunt, resistant to piercing and slashing" fits it. Rafflesia's has
  `moly`, a stamped Voidwatch NM, and `snippy rafflesia`'s own Weak/Strong boxes are BLANK — no
  page evidence either way (rule 327 / the rev-363 Poroggo precedent).
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
REVIEW_X = "mobimages/review_x.png"

d = json.load(open(P, encoding="utf-8"))
mobs, abilities = d["mobs"], d["abilities"]
zone_names = {z["name"] for z in json.load(open(os.path.join(ASSETS, "zones.json"), encoding="utf-8"))["zones"]}

IMP_WK = [["Fire", "+15%"], ["Lightning", "+15%"], ["Light", "+30%"], ["Ice", "+15%"],
          ["Earth", "+15%"], ["Water", "+15%"]]
IMP_ST = [["Wind", "-30%"], ["Dark", "-70%"]]
QIQ_WK = [["Fire", "+15%"], ["Wind", "+30%"], ["Light", "+15%"], ["Ice", "+15%"], ["Water", "+15%"]]
QIQ_ST = [["Earth", "-30%"]]

IMP_KIT = ["Abrasive Tantara", "Deafening Tantara", "Frenetic Rip"]
QIQ_KIT = ["Cutpurse", "Dead Eye", "Faze", "Kibosh", "Sandspray"]
RAF_KIT = ["Seedspray", "Bloody Caress", "Floral Bouquet", "Rotten Stench", "Viscid Emission"]
SKE_KIT = ["Black Cloud", "Blood Saber", "Hell Slash", "Horror Cloud"]
SKE_IM = ["Drain", "Aspir", "Dark Sleep"]

HORN_NOTES = [
    "Only drops an Imp Horn if its horn was broken during the fight.",
    "It uses Frenetic Rip when its horn breaks, makes an unmarked gesture on noticing the loss, and "
    "a different gesture to recover it. The horn can come back at any time — seconds later, even — "
    "and Frenetic Rip is not a prerequisite.",
]

PAGES = {
    # ---- Imp: family grid replaces the import default -----------------------
    "elder's imp": dict(fam="Imp", regrid=(IMP_WK, IMP_ST), crys="Dark", kit=IMP_KIT,
                        det=["Sight", "Sound"], nm=True, zones=[("Mount Zhayolm", None)],
                        spawn="Voidwatch (summoned by Vanasarvik)", im=["Stun"],
                        notes=["Summoned once Vanasarvik recovers from its first stagger, and "
                               "resummoned a few minutes after it is killed.",
                               "Unlike Vanasarvik it is immune to Stun."]),
    "errand imp": dict(fam="Imp", regrid=(IMP_WK, IMP_ST), crys="Dark", kit=IMP_KIT,
                       job="Black Mage", det=["True Sight", "Sound"],
                       zones=[("Castle Zvahl Baileys [S]", "79-80"),
                              ("Castle Zvahl Keep [S]", "79-80")], notes=HORN_NOTES),
    "keep imp": dict(fam="Imp", regrid=(IMP_WK, IMP_ST), crys="Dark", kit=IMP_KIT,
                     job="Black Mage", det=["True Sight", "True Sound"],
                     zones=[("Castle Zvahl Keep [S]", "81-83")], notes=HORN_NOTES),
    # ---- Qiqirn: same, plus three NPC-type pages ----------------------------
    "qiqirn bewitcher": dict(fam="Qiqirn", regrid=(QIQ_WK, QIQ_ST), crys="Earth", kit=QIQ_KIT,
                             det=["Sight", "Sound"], spawn="Bastion",
                             notes=["Two spawn at the start of every Bastion battle.",
                                    "Casts Flash and Stun."]),
    "qiqirn freelance": dict(fam="Qiqirn", regrid=(QIQ_WK, QIQ_ST), crys="Earth", kit=QIQ_KIT,
                             det=["Sight", "Sound"], job="Ranger",
                             zones=[("Al Zahbi", None)], spawn="Besieged",
                             notes=["Only present in Al Zahbi when the Imperial Defense value is "
                                    "very low, around 30 or below, appearing in place of the "
                                    "Volunteers.",
                                    "Wields a dagger and a shortbow, and uses the standard Qiqirn "
                                    "attacks."]),
    "qiqirn trapper": dict(fam="Qiqirn", regrid=(QIQ_WK, QIQ_ST), crys="Earth", kit=QIQ_KIT,
                           det=["Sight", "Sound"], job="Ranger", spawn="Bastion",
                           notes=["Two spawn at the start of every Bastion battle."]),
    # ---- Rafflesia: GRIDS KEPT ---------------------------------------------
    "ravishing rafflesia": dict(fam="Rafflesia", crys="Earth", kit=RAF_KIT,
                                zones=[("Aydeewa Subterrane", None)],
                                spawn="Voidwatch (summoned by Morta)",
                                notes=["Spawns in groups of up to twelve shortly after Morta "
                                       "appears, and feeds into that fight's Full Bloom mechanic.",
                                       "Cannot be charmed, but its MP can be drained with Aspir."]),
    "snippy rafflesia": dict(fam="Rafflesia", crys="Earth", kit=RAF_KIT, det=["Sound"], agg=True,
                             zones=[("Cirdas Caverns", "123")],
                             notes=["Spawns around the west and east areas of map 2."]),
    "vir'ava's rafflesia": dict(fam="Rafflesia", crys="Earth", kit=RAF_KIT, det=["Sound"],
                                zones=[("Escha RuAun", None)],
                                content=["Geas Fete: Escha RuAun: Tier 3"],
                                spawn="Geas Fete (summoned by Vir'ava)",
                                notes=["Black Rafflesia adds that spawn during the Vir'ava fight; "
                                       "Vir'ava can eat them to recover, so they are usually pulled "
                                       "or slept rather than left standing."]),
    # ---- Skeleton: GRIDS KEPT ----------------------------------------------
    "lamia's skeleton": dict(fam="Skeleton", crys="Earth", kit=SKE_KIT, im=SKE_IM, job="Warrior",
                             zones=[("Arrapago Reef", None)], spawn="Assists Lamia No.19",
                             notes=["Does not respawn once killed.",
                                    "Unlike most enemy pets, it can aggro on its own."]),
    "macabre skeleton": dict(fam="Skeleton", crys="Earth", kit=SKE_KIT, im=SKE_IM, job="Black Mage",
                             zones=[("Reisenjima", "121-126")],
                             notes=["Appears at night only, near the hills between Survival Guides "
                                    "2 and 3."]),
    "skeleton escort": dict(fam="Skeleton", crys="Earth", kit=SKE_KIT, im=SKE_IM, job="Warrior",
                            det=["True Sound", "Blood"], agg=True, lnk=True,
                            zones=[("Beaucedine Glacier [S]", None), ("Xarcabard [S]", None)],
                            spawn="Spawned by a Siege Turret"),
}

log, declined = [], []
for key, page in PAGES.items():
    m = mobs[key]
    assert m.get("fam") == page["fam"], (key, m.get("fam"))
    ch = []

    if m.get("img") == REVIEW_X:
        del m["img"]; ch.append("cleared review_x")

    if page.get("regrid"):
        wk, st = page["regrid"]
        m["wk"] = [r[:] for r in wk]
        m["st"] = [r[:] for r in st]
        ch.append("family grid")

    if not m.get("crys"):
        m["crys"] = page["crys"]; ch.append(f"crys={page['crys']}")

    if page.get("job") and not m.get("job"):
        m["job"] = page["job"]; ch.append(f"job={page['job']}")

    if not m.get("ab"):
        m["ab"] = list(page["kit"]); ch.append(f"ab={len(m['ab'])}")

    if page.get("im") and not m.get("im"):
        m["im"] = list(page["im"]); ch.append(f"im={len(m['im'])}")

    if page.get("det") and m.get("det") != page["det"]:
        declined.append(f"{key}: det {json.dumps(m.get('det'))} -> {json.dumps(page['det'])}")
        m["det"] = list(page["det"]); ch.append("det")

    if page.get("nm") and not m.get("nm"):
        m["nm"] = True; ch.append("nm=True")
    if page.get("lnk") and not m.get("lnk"):
        m["lnk"] = True; ch.append("lnk=True")
    if page.get("agg") and not m.get("agg"):
        m["agg"] = True; ch.append("agg=True")

    if page.get("zones"):
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

print("rev 364 — Section X batches 11-14 (Imp 3, Qiqirn 3, Rafflesia 3, Skeleton 3)")
print("\n".join(log))
print("\nDECLINED / OVERRIDDEN:")
print("\n".join("  " + x for x in declined) or "  (none)")
print(f"\nreview_x remaining: {sum(1 for v in mobs.values() if v.get('img') == REVIEW_X)}")
