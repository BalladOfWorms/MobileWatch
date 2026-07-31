#!/usr/bin/env python3
"""Dynamis-Tavnazia zone pass (rev 206) — BalladOfWorms / MobileWatch.

5 shots: 13-row NM table, 7-row Adversaries, the Hydra and Kindred rosters, the
Nightmare table, and the Diabolos/Time-Extension summary.

FIRST ZONE WITH MULTIPLE BOSSES AT EACH TIER: four Mega Bosses (Diabolos Club /
Diamond / Heart / Spade, one spawns at random from a Herald's Juju) and four Arch
Mega Bosses (Nox / Umbra / Somnus / Letum, one at random from Fnd. Tome II 14-17).
The page states both tiers outright, so no mechanic inference needed this time.

LEVELS FOR THE HYDRA AND KINDRED ROSTERS COME FROM THEIR COLLECTIVE ADVERSARY ROW.
"Members of the Hydra Vanguard" is 79-81 with **18 spawns** and the Hydra roster is
exactly 15 jobs + 3 pets = 18; "Members of the Kindred Vanguard" is 95-97 with 18
spawns against the same 15 + 3. The collective row is the Adversaries entry FOR those
mobs, and Adversaries is the level authority — so the band goes on the individuals.
"""
import json, sys, os

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
ZONE = "Dynamis-Tavnazia"
TAG = "Dynamis: " + ZONE

d = json.load(open(P, encoding="utf-8"))
M = d["mobs"]

JOBS = ["Bard", "Beastmaster", "Black Mage", "Dark Knight", "Dragoon", "Monk",
        "Ninja", "Paladin", "Ranger", "Red Mage", "Samurai", "Summoner", "Thief",
        "Warrior", "White Mage"]
PROTO = ["Effigy Prototype", "Icon Prototype", "Tombstone Prototype", "Statue Prototype"]
MEGA = ["Diabolos Club", "Diabolos Diamond", "Diabolos Heart", "Diabolos Spade"]
ARCH = ["Diabolos Nox", "Diabolos Umbra", "Diabolos Somnus", "Diabolos Letum"]
ADV = ["Manifest Icon", "Adamantking Effigy", "Goblin Replica", "Serjeant Tombstone",
       "Vanguard Eye"]
HYD = ["Hydra " + j for j in JOBS] + ["Hydra's Hound", "Hydra's Wyvern", "Hydra's Avatar"]
KIN = ["Kindred " + j for j in JOBS] + ["Kindred's Vouivre", "Kindred's Wyvern",
                                        "Kindred's Avatar"]
NIGHT = ["Nightmare " + n for n in ["Antlion", "Bugard", "Cluster", "Hornet", "Leech",
                                    "Makara", "Taurus", "Worm"]]

ROSTER = {}
for n in PROTO: ROSTER[n] = "~80"
ROSTER["Prototype Eye"] = "~95"
for n in MEGA: ROSTER[n] = "~80"
for n in ARCH: ROSTER[n] = "~100"
for n in ADV: ROSTER[n] = "79-81"
for n in HYD: ROSTER[n] = "79-81"
for n in KIN: ROSTER[n] = "95-97"
for n in NIGHT: ROSTER[n] = None          # the Nightmare table has no Lv column

ROLES = {n: "TE" for n in PROTO}
ROLES["Prototype Eye"] = "TE"
for n in MEGA: ROLES[n] = "Mega"
for n in ARCH: ROLES[n] = "Arch Mega"

COLLECTIVE = ["Members of the Hydra Vanguard", "Members of the Kindred Vanguard"]

NOTES = {
    "hydra's hound": "Hounds cast Blindga.",
    "hydra's avatar": "Keep the avatar asleep when Astral Flow goes off.",
    "kindred's avatar": "Keep the avatar asleep when Astral Flow goes off.",
    "nightmare cluster": "Large Nightmare Clusters will use Self-Destruct.",
    "nightmare hornet": "Uses Frenzy Pollen, which speeds up its attacks similarly to Hundred Fists.",
    "nightmare taurus": "Uses an enhanced Mortal Ray that can be avoided by facing away.",
}

missing, zone_added, lvl_filled, lvl_reset, lv_union, tagged, role_set, noted = [], [], [], [], [], [], [], []

for name, band in ROSTER.items():
    k = name.lower()
    m = M.get(k)
    if m is None:
        missing.append(name); continue

    zs = m.get("zones") or []
    hit = next((e for e in zs if e and e[0] == ZONE), None)
    if hit is None:
        zs.append([ZONE] if band is None else [ZONE, band])
        m["zones"] = zs; zone_added.append(name)
    elif band is not None and (len(hit) < 2 or not hit[1]):
        hit[:] = [ZONE, band]; lvl_filled.append(name)
    elif band is not None and hit[1] != band:
        lvl_reset.append((name, hit[1], band)); hit[:] = [ZONE, band]

    if band:
        nums = [int(x) for x in "".join(c if c.isdigit() else " " for c in band).split()]
        lo, hi = min(nums), max(nums)
        cur = m.get("lv")
        if not cur:
            m["lv"] = [lo, hi]; lv_union.append((name, None, [lo, hi]))
        else:
            new = [min(cur[0], lo), max(cur[1], hi)]
            if new != cur:
                lv_union.append((name, list(cur), new)); m["lv"] = new

    role = ROLES.get(name)
    want = TAG + (": " + role if role else "")
    ct = list(m.get("content") or [])
    old = [t for t in ct if t == TAG or t.startswith(TAG + ":")]
    if old != [want]:
        m["content"] = [t for t in ct if t not in old] + [want]
        (role_set if role else tagged).append(name)

for k, text in NOTES.items():
    ns = M[k].get("notes") or []
    if text not in ns:
        ns.append(text); M[k]["notes"] = ns; noted.append(k)

assert not [k for m in M.values() for k, v in m.items() if v is None], "null poison"
assert not [e for m in M.values() for e in (m.get("zones") or []) if len(e) > 1 and not e[1]], "empty zone level"
json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("page rows        :", len(ROSTER) + len(COLLECTIVE), "( 13 NM + 7 adversary + 36 Hydra/Kindred + 8 Nightmare )")
print("MISSING          :", len(missing), missing)
print("collective rows  :", COLLECTIVE, "-> no records; their bands applied to the 18+18 individuals")
print("zone added       :", len(zone_added))
print("  ->", ", ".join(sorted(zone_added)))
print("zone level filled:", len(lvl_filled), sorted(lvl_filled))
print("zone level reset :", len(lvl_reset), lvl_reset)
print("lv unions        :", len(lv_union))
for n, a, b in lv_union: print("   ", n, a, "->", b)
print("content tagged   :", len(tagged))
print("roles set        :", len(role_set), sorted(role_set))
print("notes added      :", len(noted), sorted(noted))
