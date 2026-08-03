#!/usr/bin/env python3
"""Dynamis-Valkurm zone pass (rev 203) — BalladOfWorms / MobileWatch.

3 shots: 12-row NM table, 8-row Adversaries, and the curated NM summary.

ZONE IDENTIFIED FROM THE FILE, NOT FROM MEMORY. The page never names itself in the
crops; the eight already-stored records (Fairy Ring / Nant'ina / Stcemqestcint /
Cirrate Christelle / Arch Christelle) carry **Dynamis-Valkurm** with spawn strings
whose coords match this page cell for cell (J-6, J-7, J-7, G-9, C-7, G-7, E-7, G-9)
and the same ~80 / ~100 tildes. Valkurm it is.

Boss tiers by mechanic (rev-201): Cirrate Christelle drops Fiendish Tome II
(Chapter 1), one of four -> ": Mega"; Arch Christelle takes all four -> ": Arch Mega".
The page's own words are "Zone Boss" / "Zone Mega Boss" — a THIRD vocabulary.
"""
import json, sys, os

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
ZONE = "Dynamis-Valkurm"
TAG = "Dynamis: " + ZONE

d = json.load(open(P, encoding="utf-8"))
M = d["mobs"]

ROSTER = {
    "Goblin Statue": "~80", "Avatar Idol": "~80", "Adamantking Image": "~80",
    "Warchief Tombstone": "~80",
    "Fairy Ring": "~80", "Nant'ina": "~80", "Stcemqestcint": "~80",
    "Cirrate Christelle": "~80",
    "Lost Fairy Ring": "~100", "Lost Nant'ina": "~100",
    "Lost Stcemqestcint": "~100", "Arch Christelle": "~100",
}
ROLES = {"Cirrate Christelle": "Mega", "Arch Christelle": "Arch Mega",
         "Goblin Statue": "TE", "Avatar Idol": "TE",
         "Adamantking Image": "TE", "Warchief Tombstone": "TE"}
# Adversaries is 4 collective rows x 2 bands (75-77 / 95-97), job column "All" —
# no records, none created (the Goblin/Kindred Vanguard rule).
COLLECTIVE = ["Members of the %s Vanguard" % g
              for g in ("Goblin", "Quadav", "Orcish", "Yagudo")]

# The summary table's Job column beats a family default (Morbol -> Warrior)
JOBS = {"Cirrate Christelle": "Beastmaster", "Arch Christelle": "Beastmaster"}

missing, zone_added, lvl_filled, lv_union, tagged, role_set, job_set = [], [], [], [], [], [], []

for name, band in ROSTER.items():
    k = name.lower()
    m = M.get(k)
    if m is None:
        missing.append(name); continue

    zs = m.get("zones") or []
    hit = next((e for e in zs if e and e[0] == ZONE), None)
    if hit is None:
        zs.append([ZONE, band]); m["zones"] = zs; zone_added.append(name)
    elif len(hit) < 2 or not hit[1]:
        hit[:] = [ZONE, band]; lvl_filled.append(name)

    num = int("".join(c for c in band if c.isdigit()))
    cur = m.get("lv")
    if not cur:
        m["lv"] = [num, num]; lv_union.append((name, None, [num, num]))
    else:
        new = [min(cur[0], num), max(cur[1], num)]
        if new != cur:
            lv_union.append((name, list(cur), new)); m["lv"] = new

    if name in JOBS and m.get("job") != JOBS[name]:
        job_set.append((name, m.get("job"), JOBS[name])); m["job"] = JOBS[name]

    role = ROLES.get(name)
    want = TAG + (": " + role if role else "")
    ct = list(m.get("content") or [])
    old = [t for t in ct if t == TAG or t.startswith(TAG + ":")]
    if old != [want]:
        m["content"] = [t for t in ct if t not in old] + [want]
        (role_set if role else tagged).append(name)

assert not [k for m in M.values() for k, v in m.items() if v is None], "null poison"
assert not [e for m in M.values() for e in (m.get("zones") or []) if len(e) > 1 and not e[1]], "empty zone level"
json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("page rows        : 20 ( 12 NM + 8 adversary )")
print("MISSING          :", len(missing), missing)
print("collective rows  :", len(COLLECTIVE), "x2 bands -> no records, none created")
print("zone added       :", len(zone_added), sorted(zone_added))
print("zone level filled:", len(lvl_filled), sorted(lvl_filled))
print("lv unions        :", len(lv_union))
for n, a, b in lv_union: print("   ", n, a, "->", b)
print("job corrected    :", job_set)
print("content tagged   :", len(tagged), sorted(tagged))
print("roles set        :", len(role_set), sorted(role_set))
