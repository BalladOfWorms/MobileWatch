#!/usr/bin/env python3
"""Dynamis-Beaucedine zone pass (rev 200) — BalladOfWorms / MobileWatch.

Sources: BG-wiki Dynamis-Beaucedine page, 18 shots.
  imgs 1-7   NM table (Lv column BLANK on every row -> zone goes on level-less)
  imgs 8-17  Adversaries table (Lv `-` everywhere EXCEPT the Hydra Corps jobs,
             which publish TWO bands, 75-80 and 90-95 -> collapsed to one entry
             "75-80/90-95", the Members-of-the-Vanguard precedent)
  img 18     curated Notorious Monsters table -> Granules of Time droppers,
             Zone Boss (Angra Mainyu) and Mega Boss (Arch Angra Mainyu)
"""
import json, sys, os

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
ZONE = "Dynamis-Beaucedine"
TAG = "Dynamis: " + ZONE

d = json.load(open(P, encoding="utf-8"))
M = d["mobs"]

# ---------------------------------------------------------------- roster
NM_ROWS = ["Ascetox Ratgums", "Be'Zhe Keeprazer", "Bhuu Wjato the Firepool",
    "Bordox Kittyback", "Brewnix Bittypupils", "Caa Xaza the Madpiercer",
    "Cobraclaw Buchzvotch", "De'Bho Pyrohand", "Deathcaller Bidfbid",
    "Drakefeast Wubmfub", "Draklix Scalecrust", "Droprix Granitepalms",
    "Elvaanlopper Grokdok", "Foo Peku the Bloodcloak", "Ga'Fho Venomtouch",
    "Galkarider Retzpratz", "Gibberox Pimplebeak", "Go'Tyo Magenapper",
    "Gu'Khu Dukesniper", "Gu'Nha Wallstormer", "Guu Waji the Preacher",
    "Heavymail Djidzbad", "Hee Mida the Meticulous", "Humegutter Adzjbadj",
    "Jeunoraider Gepkzip", "Ji'Fhu Infiltrator", "Ji'Khu Towercleaver",
    "Knii Hoqo the Bisector", "Koo Saxu the Everfast", "Kuu Xuka the Nimble",
    "Lockbuster Zapdjipp", "Maa Zaua the Wyrmkeeper", "Mi'Rhe Whisperblade",
    "Mithraslaver Debhabob", "Moltenox Stubthumbs", "Morblox Chubbychin",
    "Mu'Gha Legionkiller", "Na'Hya Floodmaker", "Nee Huxa the Judgmental",
    "Nu'Bhi Spiraleye", "Puu Timu the Phantasmal", "Routsix Rubbertendon",
    "Ruffbix Jumbolobes", "Ryy Qihi the Idolrobber", "Shisox Widebrow",
    "Skinmask Ugghfogg", "Slinkix Trufflesniff", "So'Gho Adderhandler",
    "So'Zho Metalbender", "Soo Jopo the Fiendking", "Spinalsucker Galflmall",
    "Swypestix Tigershins", "Ta'Hyu Gallanthunter", "Taruroaster Biggsjig",
    "Tocktix Thinlids", "Ultrasonic Zeknajak", "Whistrix Toadthroat",
    "Wraithdancer Gidbnod", "Xaa Chau the Roctalon", "Xhoo Fuza the Sublime",
    "Angra Mainyu", "Fire Pukis", "Petro Pukis", "Poison Pukis", "Wind Pukis",
    "Dagourmarche", "Goublefaupe", "Mildaunegeux", "Quiebitiel", "Velosareon",
    "Taquede", "Pignonpausard", "Hitaume", "Cavanneche", "Arch Angra Mainyu"]

VG = ["Alchemist", "Ambusher", "Amputator", "Armorer", "Assassin", "Backstabber",
    "Beasttender", "Bugler", "Chanter", "Constable", "Defender", "Dollmaster",
    "Dragontamer", "Drakekeeper", "Enchanter", "Exemplar", "Eye", "Footsoldier",
    "Grappler", "Gutslasher", "Hatamoto", "Hawker", "Hitman", "Impaler",
    "Inciter", "Kusa", "Liberator", "Maestro", "Mason", "Mesmerizer", "Militant",
    "Minstrel", "Neckchopper", "Necromancer", "Ogresoother", "Oracle",
    "Partisan", "Pathfinder", "Persecutor", "Pillager", "Pitfighter", "Predator",
    "Prelate", "Priest", "Protector", "Purloiner", "Ronin", "Salvager",
    "Sentinel", "Shaman", "Skirmisher", "Smithy", "Thaumaturge", "Tinkerer",
    "Trooper", "Undertaker", "Vexer", "Vigilante", "Vindicator", "Visionary",
    "Welldigger"]

HYDRA = ["Hydra " + j for j in ["Bard", "Beastmaster", "Black Mage",
    "Dark Knight", "Dragoon", "Monk", "Ninja", "Paladin", "Ranger", "Red Mage",
    "Samurai", "Summoner", "Thief", "Warrior", "White Mage"]]

ADV_FLAT = (["Adamantking Effigy", "Adamantking Image", "Dagourmarche's Avatar",
    "Dagourmarche's Wyvern", "Avatar Icon", "Avatar Idol", "Goblin Replica",
    "Goblin Statue"]
    + ["Hydra's Avatar", "Hydra's Hound", "Hydra's Wyvern", "Rearguard Eye",
       "Serjeant Tombstone", "Taquede's Wyvern"]
    + ["Vanguard " + v for v in VG]
    + ["Vanguard's Avatar", "Vanguard's Crow", "Vanguard's Hecteyes",
       "Vanguard's Scorpion", "Vanguard's Slime", "Vanguard's Wyvern",
       "Warchief Tombstone"])

# name -> level string for the zone entry (None = level-less)
ROSTER = {n: None for n in NM_ROWS}
ROSTER.update({n: None for n in ADV_FLAT})
ROSTER.update({n: "75-80/90-95" for n in HYDRA})

ROLES = {"Angra Mainyu": "Boss", "Arch Angra Mainyu": "Mega",
         "Adamantking Image": "TE", "Avatar Idol": "TE", "Goblin Statue": "TE",
         "Warchief Tombstone": "TE", "Rearguard Eye": "TE"}

missing, zone_added, lvl_filled, lv_widened, tagged, role_set = [], [], [], [], [], []

for name, band in ROSTER.items():
    k = name.lower()
    m = M.get(k)
    if m is None:
        missing.append(name); continue

    # ---- zone entry
    zs = m.get("zones") or []
    hit = next((e for e in zs if e and e[0] == ZONE), None)
    if hit is None:
        zs.append([ZONE] if band is None else [ZONE, band])
        m["zones"] = zs
        zone_added.append(name)
    elif band is not None and (len(hit) < 2 or not hit[1]):
        hit[:] = [ZONE, band]
        lvl_filled.append(name)

    # ---- lv union from the Adversaries bands
    if band == "75-80/90-95":
        lo, hi = 75, 95
        cur = m.get("lv")
        if not cur:
            m["lv"] = [lo, hi]; lv_widened.append((name, None, [lo, hi]))
        else:
            new = [min(cur[0], lo), max(cur[1], hi)]
            if new != cur:
                lv_widened.append((name, list(cur), new)); m["lv"] = new

    # ---- content tag (+ role)
    role = ROLES.get(name)
    want = TAG + (": " + role if role else "")
    ct = [t for t in (m.get("content") or [])]
    existing = [t for t in ct if t == TAG or t.startswith(TAG + ":")]
    if existing != [want]:
        ct = [t for t in ct if t not in existing]
        ct.append(want)
        m["content"] = ct
        (role_set if role else tagged).append(name)

# --------------------------------------------- the mis-filed TE flags
# The Beaucedine NM table settles it: the Granules-of-Time droppers are the
# 1-spawn Image / Idol / Statue / Tombstone, not the 4-spawn decoys. The file
# agrees — only the Image/Idol carry `Time Extension (10 min.)`.
FIX_TE = [("adamantking effigy", "adamantking image", "Dynamis: Dynamis-Bastok"),
          ("avatar icon", "avatar idol", "Dynamis: Dynamis-Windurst")]
te_moved = []
for wrong, right, base in FIX_TE:
    w, r = M[wrong], M[right]
    w["content"] = [base if t == base + ": TE" else t for t in w["content"]]
    r["content"] = [base + ": TE" if t == base else t for t in r["content"]]
    te_moved.append((wrong, right, base))

# --------------------------------------------- small page facts
notes_added = []
def addnote(key, text):
    m = M[key]; ns = m.get("notes") or []
    if text not in ns:
        ns.append(text); m["notes"] = ns; notes_added.append(key)

# img 18 Notes column
addnote("goblin statue", "Spawns among the Goblin Vanguard. Can rarely spawn amongst the Yagudo Vanguard.")
addnote("angra mainyu", "Teleports around the area. A pet job is useful for keeping it targeted.")
addnote("arch angra mainyu", "Uses Chainspell and casts Death.")
for p, mv in [("fire pukis", "Flame Breath"), ("wind pukis", "Wind Breath"),
              ("petro pukis", "Petro Eyes"), ("poison pukis", "Poison Breath")]:
    addnote(p, "Spawned alongside Angra Mainyu; its signature move is %s." % mv)

# Rearguard Eye is the 20-minute extension (all four statues are 10)
if not (M["rearguard eye"].get("drops") or "").strip():
    M["rearguard eye"]["drops"] = "Time Extension (20 min.)"
    M["rearguard eye"]["spawn"] = M["rearguard eye"].get("spawn") or "Timed (short)"

# --------------------------------------------- guards
assert not [k for m in M.values() for k, v in m.items() if v is None], "null poison"
assert not [e for m in M.values() for e in (m.get("zones") or []) if len(e) > 1 and not e[1]], "empty zone level"

json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("page rows        :", len(ROSTER) + len(HYDRA) * 0, "(", len(NM_ROWS), "NM +", len(ADV_FLAT) + len(HYDRA), "adversary )")
print("MISSING          :", len(missing), missing)
print("zone added       :", len(zone_added))
print("  ->", ", ".join(sorted(zone_added)) or "-")
print("zone level filled:", len(lvl_filled), sorted(lvl_filled))
print("lv widened       :", len(lv_widened))
for n, a, b in lv_widened: print("   ", n, a, "->", b)
print("content tagged   :", len(tagged))
print("roles set        :", len(role_set), sorted(role_set))
print("TE flags moved   :", te_moved)
print("notes added      :", len(notes_added), sorted(set(notes_added)))
