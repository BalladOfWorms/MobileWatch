#!/usr/bin/env python3
"""Dynamis-Buburimu zone pass (rev 204) — BalladOfWorms / MobileWatch.

5 shots: 29-row NM table, 8-row Adversaries (4 collectives x 2 bands), curated summary.

Boss tiers by mechanic (rev-201 / rule 105): Apocalyptic Beast drops Fiendish Tome II
(Chapter 5), one of five -> ": Mega"; Arch Apocalyptic Beast takes Chapters 5-9 ->
": Arch Mega". The page's own words are "Zone Boss" / "Zone Mega Boss" (Valkurm's
vocabulary), which is the 4th wording seen for the same two ranks.

Also fixes two records that rev-198 flagged as stored-but-not-on-the-Bastok-page:
gi'bhe fleshfeaster and te'zha ironclad are on THIS page, and zoneinfo files both
under dynamis_buburimu only -> the Dynamis-Bastok entry is dropped.
"""
import json, sys, os

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
ZONE = "Dynamis-Buburimu"
TAG = "Dynamis: " + ZONE

d = json.load(open(P, encoding="utf-8"))
M = d["mobs"]

TE = ["Goblin Statue", "Avatar Idol", "Adamantking Image", "Warchief Tombstone"]
LOTTERY = ["Woodnix Shrillwhistle", "Shamblix Rottenheart", "Gosspix Blabblerlips",
    "Flamecaller Zoeqdoq", "Elvaansticker Bxafraff", "Hamfist Gukhbuk",
    "Lyncean Juwgneg", "Qu'Pho Bloodspiller", "Gi'Bhe Fleshfeaster",
    "Va'Rhu Bodysnatcher", "Te'Zha Ironclad", "Ree Nata the Melomanic",
    "Koo Rahi the Levinblade", "Doo Peku the Fleetfoot", "Baa Dava the Bibliophage"]
TIMED = ["Barong", "Alklha", "Aitvaras", "Stihi"]
LOST = ["Lost Barong", "Lost Alklha", "Lost Aitvaras", "Lost Stihi"]

ROSTER = {n: "~80" for n in TE + LOTTERY + TIMED}
ROSTER["Apocalyptic Beast"] = "~80"
for n in LOST: ROSTER[n] = "~100"
ROSTER["Arch Apocalyptic Beast"] = "~100"

ROLES = {n: "TE" for n in TE}
ROLES["Apocalyptic Beast"] = "Mega"
ROLES["Arch Apocalyptic Beast"] = "Arch Mega"

# 8 adversary rows = 4 collectives x 2 bands, job column "All" -> no records.
COLLECTIVE = ["Members of the %s Vanguard" % g
              for g in ("Goblin", "Quadav", "Orcish", "Yagudo")]

# rev-198's open: on the Bastok page these two never appeared. They are on THIS page,
# and zoneinfo files both under dynamis_buburimu ONLY.
MISFILED_BASTOK = ["gi'bhe fleshfeaster", "te'zha ironclad"]

missing, zone_added, lvl_filled, lvl_reset, lv_union, tagged, role_set = [], [], [], [], [], [], []

for key in MISFILED_BASTOK:
    m = M[key]
    m["zones"] = [e for e in (m.get("zones") or []) if e[0] != "Dynamis-Bastok"]
    m["content"] = [t for t in (m.get("content") or [])
                    if not t.startswith("Dynamis: Dynamis-Bastok")]
    if not m["zones"]: del m["zones"]
    if not m["content"]: del m["content"]

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
    elif hit[1] != band:
        lvl_reset.append((name, hit[1], band)); hit[:] = [ZONE, band]

    num = int("".join(c for c in band if c.isdigit()))
    cur = m.get("lv")
    if not cur:
        m["lv"] = [num, num]; lv_union.append((name, None, [num, num]))
    else:
        new = [min(cur[0], num), max(cur[1], num)]
        if new != cur:
            lv_union.append((name, list(cur), new)); m["lv"] = new

    role = ROLES.get(name)
    want = TAG + (": " + role if role else "")
    ct = list(m.get("content") or [])
    old = [t for t in ct if t == TAG or t.startswith(TAG + ":")]
    if old != [want]:
        m["content"] = [t for t in ct if t not in old] + [want]
        (role_set if role else tagged).append(name)

# summary-table detail worth keeping (player-facing)
ab = M["apocalyptic beast"]
note = "Assisted by Dragon's Avatar during Astral Flow, and summons Dragon's Wyvern with Call Wyvern."
ns = ab.get("notes") or []
if note not in ns:
    ns.append(note); ab["notes"] = ns

assert not [k for m in M.values() for k, v in m.items() if v is None], "null poison"
assert not [e for m in M.values() for e in (m.get("zones") or []) if len(e) > 1 and not e[1]], "empty zone level"
json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("page rows        : 37 ( 29 NM + 8 adversary )")
print("MISSING          :", len(missing), missing)
print("collective rows  :", len(COLLECTIVE), "x2 bands -> no records, none created")
print("Bastok entry dropped from:", MISFILED_BASTOK)
print("zone added       :", len(zone_added), sorted(zone_added))
print("zone level filled:", len(lvl_filled), sorted(lvl_filled))
print("zone level reset :", lvl_reset)
print("lv unions        :", len(lv_union))
for n, a, b in lv_union: print("   ", n, a, "->", b)
print("content tagged   :", len(tagged), sorted(tagged))
print("roles set        :", len(role_set), sorted(role_set))
