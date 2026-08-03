#!/usr/bin/env python3
"""Dynamis-Qufim zone pass (rev 205) — BalladOfWorms / MobileWatch.

3 shots: 12-row NM table, 8-row Adversaries (4 collectives x 2 bands), curated summary.

!! THE NM LISTING'S Lv COLUMN IS THE WRONG ONE ON THIS PAGE. It prints ~80 for all
twelve rows, including the Lost tier and the Arch. Everything else says ~100 for those
four: the summary table, their own `lv` [100,100], lost scolopendra's already-corrected
"~100" zone entry, and the Valkurm/Buburimu precedent where the Lost tier is always the
~100 tier. zoneinfo.json also says ~80 but is NOT independent — it was built from this
same listing during the original zone intake. Four sources to one: the Lost tier is ~100.

Boss tiers by mechanic (rule 105): Antaeus drops Fiendish Tome II (Chapter 10), one of
four -> ": Mega"; Arch Antaeus takes Chapters 10-13 -> ": Arch Mega".
"""
import json, sys, os

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
ZONE = "Dynamis-Qufim"
TAG = "Dynamis: " + ZONE

d = json.load(open(P, encoding="utf-8"))
M = d["mobs"]

TE = ["Goblin Statue", "Avatar Idol", "Adamantking Image", "Warchief Tombstone"]
ROSTER = {n: "~80" for n in TE}
for n in ["Stringes", "Scolopendra", "Suttung", "Antaeus"]:
    ROSTER[n] = "~80"
for n in ["Lost Stringes", "Lost Scolopendra", "Lost Suttung", "Arch Antaeus"]:
    ROSTER[n] = "~100"

ROLES = {n: "TE" for n in TE}
ROLES["Antaeus"] = "Mega"
ROLES["Arch Antaeus"] = "Arch Mega"

COLLECTIVE = ["Members of the %s Vanguard" % g
              for g in ("Goblin", "Quadav", "Orcish", "Yagudo")]

# summary Notes column — the three weakening items, each on the mob that drops it
NOTES = {
    "scolopendra": "Its Sea Monk Venom removes Antaeus' massive auto-regen.",
    "stringes": "Its Perforated Wing reduces Antaeus' massive attack power.",
    "suttung": "Its Undying Moiety removes Antaeus' per-hit damage cap, on both magic and physical damage.",
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

for k, text in NOTES.items():
    ns = M[k].get("notes") or []
    if text not in ns:
        ns.append(text); M[k]["notes"] = ns; noted.append(k)

assert not [k for m in M.values() for k, v in m.items() if v is None], "null poison"
assert not [e for m in M.values() for e in (m.get("zones") or []) if len(e) > 1 and not e[1]], "empty zone level"
json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("page rows        : 20 ( 12 NM + 8 adversary )")
print("MISSING          :", len(missing), missing)
print("collective rows  :", len(COLLECTIVE), "x2 bands -> no records, none created")
print("zone added       :", len(zone_added), sorted(zone_added))
print("zone level filled:", len(lvl_filled), sorted(lvl_filled))
print("zone level reset :", lvl_reset)
print("lv unions        :", len(lv_union))
for n, a, b in lv_union: print("   ", n, a, "->", b)
print("content tagged   :", len(tagged), sorted(tagged))
print("roles set        :", len(role_set), sorted(role_set))
print("notes added      :", noted)
print()
print("!! CHAPTER COLLISION:")
for k in ("lost stringes", "lost scolopendra", "lost suttung"):
    print("   %-18s %s" % (k, M[k]["drops"]))
