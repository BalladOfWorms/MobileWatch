#!/usr/bin/env python3
"""Dynamis-San d'Oria [D] (rev 210) — BalladOfWorms / MobileWatch.

14 shots: 5-row NM table, a 58-row Orc Adversaries block, and the 50-row Volte block.

THE FIRST DIVERGENCE ZONE. `Dynamis D` has been a wired-but-empty content group since
rev 192. 107 of the 113 page rows had NO RECORD AT ALL — but `zoneinfo.dynamis_san_doria_d`
has published the whole roster with levels since the original zone intake, so every level
here is corroborated by two sources and cross-check A pays for it.

Family stamps are uniform and were read off the existing members, not guessed:
  Orc    188/188 det ['Sight'], agg, lnk
  Fomor  146/146 det ['Sound','Blood','JA'], agg, lnk
"""
import json, sys, os

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = os.path.join(ASSETS, "mobs.json")
d = json.load(open(P, encoding="utf-8"))
M = d["mobs"]

ZONE = "Dynamis-San d'Oria [D]"
TAG = "Dynamis D: " + ZONE

ORC = dict(fam="Orc", agg=True, lnk=True, det=["Sight"])
FOM = dict(fam="Fomor", agg=True, lnk=True, det=["Sound", "Blood", "JA"])

# squad name -> (leader name, job pair)
PAIRS = [("Skullcrusher", "Ravager", "WAR", "DRK"), ("Pugilist", "Mendicant", "MNK", "PUP"),
         ("Fleetfoot", "Cutpurse", "THF", "DNC"), ("Evoker", "Invoker", "BLM", "GEO"),
         ("Enchanter", "Warlock", "RDM", "RUN"), ("Knight", "Stalwart", "PLD", "DRG"),
         ("Tamer", "Hunter", "BST", "RNG"), ("Medic", "Priest", "WHM", "SMN"),
         ("Troubador", "Minstrel", "BRD", "SAM"), ("Shinobi", "Kagemusha", "NIN", "BLU"),
         ("Pirate", "Canoneer", "COR", "SCH")]
VOLTE_R = ["Volte Beret", "Volte Gloves", "Volte Brais", "Volte Gaiters"]

V142 = [("Warrior", "WAR"), ("Monk", "MNK"), ("White Mage", "WHM"), ("Black Mage", "BLM"),
        ("Red Mage", "RDM"), ("Thief", "THF"), ("Paladin", "PLD"), ("Ninja", "NIN"),
        ("Dragoon", "DRG"), ("Corsair", "COR"), ("Bard", "BRD"), ("Summoner", "SMN"),
        ("Beastmaster", "BST"), ("Samurai", "SAM"), ("Dark Knight", "DRK"), ("Ranger", "RNG"),
        ("Scholar", "SCH"), ("Puppetmaster", "PUP"), ("Dancer", "DNC"),
        ("Rune Fencer", "RUN"), ("Blue Mage", "BLU"), ("Geomancer", "GEO")]
V146 = [("Cleaver", "WAR"), ("Fistfighter", "MNK"), ("Incanter", "BLM"), ("Priest", "WHM"),
        ("Duelist", "RUN"), ("Vagabond", "THF"), ("Crusader", "PLD"), ("Reaper", "DRK"),
        ("Trainer", "BST"), ("Conductor", "BRD"), ("Sniper", "RNG"), ("Mononofu", "SAM"),
        ("Shinobi", "NIN"), ("Highwind", "DRG"), ("Controller", "SMN"), ("Joiner", "BLU"),
        ("Sailor", "COR"), ("Manipulator", "PUP"), ("Twirler", "DNC"), ("Erudite", "SCH"),
        ("Communer", "GEO"), ("Illusionist", "RDM")]
VOLTE_DROPS = "Demon's Medal, Old I. Card, S. Astral Detritus"

NEW = []   # (name, lv, dict of fields)
NEW.append(("Corporal Tombstone", 127, dict(fam="Replica", agg=True, lnk=True, det=["Sight"])))

for sq, ld, j1, j2 in PAIRS:
    job = "%s / %s" % (j1, j2)
    NEW.append(("Squadron " + sq, 127, dict(ORC, job=job,
        drops="Footshard: %s, Footshard: %s, Rusted I. Card" % (j1, j2))))
    NEW.append(("Regiment " + sq, 134, dict(ORC, job=job,
        drops="Voidfoot: %s, Voidfoot: %s, Black. I. Card" % (j1, j2))))
    NEW.append((ld + " Leader", 129, dict(ORC, job=job, drops=", ".join(
        ["Footshard: " + j1, "Footshard: " + j2, "Torsoshard: " + j1, "Torsoshard: " + j2,
         "Beastmen's Medal", "Rusted I. Card"] + VOLTE_R))))
    NEW.append((ld + " Commander", 137, dict(ORC, job=job, drops=", ".join(
        ["Voidfoot: " + j1, "Voidfoot: " + j2, "Voidtorso: " + j1, "Voidtorso: " + j2,
         "Kindred's Medal", "Black. I. Card"] + VOLTE_R))))

PETS = [("Squadron's Avatar", 127, "Avatar"), ("Regiment's Avatar", 134, "Avatar"),
        ("Squadron's Rabbit", 127, "Rabbit"), ("Regiment's Coeurl", 134, "Coeurl"),
        ("Squadron's Wyvern", 127, "Wyvern (Dragoon Pet)"),
        ("Regiment's Wyvern", 134, "Wyvern (Dragoon Pet)"),
        ("Leader's Avatar", 129, "Avatar"), ("Commander's Avatar", 137, "Avatar"),
        ("Leader's Manticore", 129, "Manticore"), ("Commander's Pet", 137, None),
        ("Leader's Wyvern", 129, "Wyvern (Dragoon Pet)"),
        ("Commander's Wyvern", 137, "Wyvern (Dragoon Pet)")]
for n, lv, fam in PETS:
    f = dict(agg=True, lnk=True, det=["Sight"])
    if fam: f["fam"] = fam
    NEW.append((n, lv, f))

for nm, j in V142:
    NEW.append(("Volte " + nm, 142, dict(FOM, job=j, drops=VOLTE_DROPS)))
for n, lv, fam in [("Volte's Puppet", 142, "Automaton"), ("Volte's Avatar", 142, "Avatar"),
                   ("Volte's Pet", 142, None), ("Volte's Wyvern", 142, "Wyvern (Dragoon Pet)"),
                   ("Volte's Cluster", 146, "Cluster"), ("Volte's Automaton", 146, "Automaton")]:
    f = dict(agg=True, lnk=True, det=["Sight"])
    if fam: f["fam"] = fam
    NEW.append((n, lv, f))
for nm, j in V146:
    NEW.append(("Volte " + nm, 146, dict(FOM, job=j, drops=VOLTE_DROPS)))

created, skipped = [], []
for name, lv, fields in NEW:
    k = name.lower()
    if k in M:
        skipped.append(name); continue
    rec = {"n": name}
    rec.update({x: y for x, y in fields.items() if y})
    rec["lv"] = [lv, lv]
    rec["zones"] = [[ZONE, str(lv)]]
    rec["content"] = [TAG]
    M[k] = rec
    created.append(name)

# ---- the six that already existed
ROLES = {"disjoined elvaan": "Disjoined", "halphas": "Boss",
         "overseer's tombstone": "Midboss"}
EXIST = {"aurix": None, "halphas": 139, "overseer's tombstone": 132,
         "disjoined elvaan": 149, "disjoined elvaan ???": None, "elemental circle": None}
touched = []
for k, lv in EXIST.items():
    m = M[k]
    zs = m.get("zones") or []
    if not any(e and e[0] == ZONE for e in zs):
        zs.append([ZONE, str(lv)] if lv else [ZONE]); m["zones"] = zs
    want = TAG + (": " + ROLES[k] if k in ROLES else "")
    ct = [t for t in (m.get("content") or []) if not t.startswith("Dynamis D:")]
    ct.append(want); m["content"] = ct
    if lv and not m.get("lv"):
        m["lv"] = [lv, lv]
    touched.append(k)

# `overseer's tombstone` is the [D] mid-boss at 132 — a Divergence level. zoneinfo files
# it under dynamis_san_doria_d only, and rev 196 recorded that the CLASSIC San d'Oria page
# does not list it. Two sources against one stray entry (rule 107) -> drop the classic one.
ot = M["overseer's tombstone"]
ot["zones"] = [e for e in ot["zones"] if e[0] != "Dynamis-San d'Oria"]
ot["content"] = [t for t in ot["content"] if not t.startswith("Dynamis: Dynamis-San d'Oria")]

assert not [k for m in M.values() for k, v in m.items() if v is None], "null poison"
assert not [e for m in M.values() for e in (m.get("zones") or []) if len(e) > 1 and not e[1]], "empty zone level"
json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)

print("created :", len(created))
print("skipped (already existed):", skipped)
print("existing records updated :", touched)
print("roles    :", ROLES)
print("mobs now :", len(M))
