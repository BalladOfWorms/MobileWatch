#!/usr/bin/env python3
"""Dynamis-Xarcabard zone pass (rev 202) — BalladOfWorms / MobileWatch.

7 shots: NM table (42 rows) + Adversaries (27 rows).
  Lv is BLANK on the demon court, the Animated Weapons and the Dynamis Lord chain
  -> zone goes on level-less. Tildes kept verbatim (~80 Prototypes, ~95 Prototype
  Eye, ~90 Andras's Vouivre + Satellite Claymores) per the konjac precedent.

Boss tiers by MECHANIC (rev-201 rule, the page prints no tier label here):
  Dynamis Lord      drops Fiendish Tome: Chapter 26  -> ": Mega"
  Arch Dynamis Lord trade Chapters 26-30             -> ": Arch Mega"

The four Prototypes finally get a zone -> the ten Time-Extension mobs are all placed.
"""
import json, sys, os

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
ZONE = "Dynamis-Xarcabard"
TAG = "Dynamis: " + ZONE

d = json.load(open(P, encoding="utf-8"))
M = d["mobs"]

PROTO = ["Effigy Prototype", "Icon Prototype", "Tombstone Prototype", "Statue Prototype"]
COURT = ["Count Vine", "Count Zaebos", "Duke Berith", "Duke Gomory", "Duke Scox",
         "King Zagan", "Marquis Andras", "Marquis Cimeries", "Marquis Decarabia",
         "Marquis Gamygyn", "Marquis Nebiros", "Marquis Orias", "Marquis Sabnak",
         "Prince Seere", "Count Raum"]
ANIM = ["Animated " + w for w in ["Claymore", "Dagger", "Great Axe", "Gun", "Hammer",
        "Horn", "Kunai", "Knuckles", "Longbow", "Longsword", "Scythe", "Shield",
        "Spear", "Staff", "Tabar", "Tachi"]]
LORD = ["Dynamis Lord", "Duke Haures", "Marquis Caim", "Baron Avnas",
        "Count Haagenti", "Arch Dynamis Lord"]
SAT = ["Satellite " + s for s in ["Claymores", "Daggers", "Great Axes", "Guns",
       "Hammers", "Horns", "Knuckles", "Kunai", "Longbows", "Longswords", "Scythes",
       "Shield", "Spears", "Staves", "Tabars", "Tachi"]]
ADV_REST = ["Adamantking Effigy", "Andras's Vouivre", "Avatar Icon", "Caim's Vouivre",
            "Goblin Replica", "Haagenti's Avatar", "Nebiros's Avatar",
            "Serjeant Tombstone", "Vanguard Dragon", "Zagan's Wyvern"]

# name -> published Lv cell (None = blank/"-" -> level-less)
ROSTER = {}
for n in PROTO: ROSTER[n] = "~80"
ROSTER["Prototype Eye"] = "~95"
for n in COURT + ANIM + LORD + SAT + ADV_REST: ROSTER[n] = None
ROSTER["Andras's Vouivre"] = "~90"
ROSTER["Satellite Claymores"] = "~90"

# "Members of the Kindred Vanguard" (Lv 95-97, job column "All", 385 spawns) is a
# COLLECTIVE page row, not a mob — no record, none created (the Goblin Vanguard rule).
COLLECTIVE = ["Members of the Kindred Vanguard"]

ROLES = {"Dynamis Lord": "Mega", "Arch Dynamis Lord": "Arch Mega",
         "Prototype Eye": "TE"}
for n in PROTO: ROLES[n] = "TE"

missing, zone_added, lvl_filled, lv_widened, tagged, role_set = [], [], [], [], [], []

for name, band in ROSTER.items():
    k = name.lower()
    m = M.get(k)
    if m is None:
        missing.append(name); continue

    zs = m.get("zones") or []
    hit = next((e for e in zs if e and e[0] == ZONE), None)
    if hit is None:
        zs.append([ZONE] if band is None else [ZONE, band])
        m["zones"] = zs
        zone_added.append(name)
    elif band is not None and (len(hit) < 2 or not hit[1]):
        hit[:] = [ZONE, band]
        lvl_filled.append(name)

    if band:                                   # "~80" -> lv hi at least 80
        num = int("".join(c for c in band if c.isdigit()))
        cur = m.get("lv")
        if not cur:
            m["lv"] = [num, num]; lv_widened.append((name, None, [num, num]))
        elif num > cur[1]:
            new = [cur[0], num]
            lv_widened.append((name, list(cur), new)); m["lv"] = new

    role = ROLES.get(name)
    want = TAG + (": " + role if role else "")
    ct = list(m.get("content") or [])
    old = [t for t in ct if t == TAG or t.startswith(TAG + ":")]
    if old != [want]:
        m["content"] = [t for t in ct if t not in old] + [want]
        (role_set if role else tagged).append(name)

# Prototype Eye is the 20-minute extension, same as Rearguard Eye (rev 200)
if not (M["prototype eye"].get("drops") or "").strip():
    M["prototype eye"]["drops"] = "Time Extension (20 min.)"

assert not [k for m in M.values() for k, v in m.items() if v is None], "null poison"
assert not [e for m in M.values() for e in (m.get("zones") or []) if len(e) > 1 and not e[1]], "empty zone level"
json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("page rows        :", len(ROSTER) + len(COLLECTIVE), "( 42 NM + 27 adversary )")
print("MISSING          :", len(missing), missing)
print("collective rows  :", COLLECTIVE, "-> no record, none created")
print("zone added       :", len(zone_added))
print("  ->", ", ".join(sorted(zone_added)))
print("zone level filled:", len(lvl_filled), sorted(lvl_filled))
print("lv widened       :", len(lv_widened))
for n, a, b in lv_widened: print("   ", n, a, "->", b)
print("content tagged   :", len(tagged))
print("roles set        :", len(role_set), sorted(role_set))
