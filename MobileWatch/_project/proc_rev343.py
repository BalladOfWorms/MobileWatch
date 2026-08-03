# Rev 343 — fifteen Unknown-bucket records stamped from their own BG pages.
# Fill-blanks-only (rule 280); zones unioned, level-less entries filled, corrections logged.
# Family kits are COMPUTED LIVE from each family's modal `ab` set (rev-342 method), except
# where a page names a smaller set (§6) — then the page wins.
# Author: BalladOfWorms
import json, copy, collections

P = "app/src/main/assets/mobs.json"
d = json.load(open(P, encoding="utf-8"))
M = d["mobs"]; A = d["abilities"]; FAMS = set(d["families"]); ECO = d["family_eco"]
KEYS = ["morille mortelle", "ogler", "oppressor", "overseer", "poxhound", "procrustes",
        "scrutinizer", "sengann", "skinnymajinx", "skinnymalinks", "slabspitter jagil",
        "sodden bones", "stabnix skewerfinger", "suspended sculpture", "talacca clot"]
before = copy.deepcopy({k: M[k] for k in KEYS})
keyset_before = set(M)
log = []


def modal_kit(fam):
    c = collections.Counter()
    for v in M.values():
        if v.get("fam") == fam and v.get("ab"):
            c[tuple(sorted(v["ab"]))] += 1
    if not c:
        return [], 0, 0
    top, n = c.most_common(1)[0]
    return list(top), n, sum(c.values())


def setif(key, field, value):
    r = M[key]; cur = r.get(field)
    if cur in (None, "", [], {}):
        r[field] = value; log.append(f"  {key}: {field} = {value!r}")
    elif cur != value:
        log.append(f"  {key}: {field} KEPT {cur!r} (page said {value!r})")


def add_det(key, dets):
    r = M[key]; cur = list(r.get("det") or [])
    for x in dets:
        if x not in cur: cur.append(x)
    if cur != (r.get("det") or []):
        r["det"] = cur; log.append(f"  {key}: det -> {cur}")


def zone(key, name, levels=None, force=False):
    zs = M[key].setdefault("zones", [])
    for e in zs:
        if e[0] == name:
            if levels and len(e) == 1:
                e.append(levels); log.append(f"  {key}: zone {name} level filled {levels}")
            elif levels and len(e) > 1 and e[1] != levels:
                if force:
                    log.append(f"  {key}: zone {name} CORRECTED {e[1]!r} -> {levels!r}")
                    e[1] = levels
                else:
                    log.append(f"  {key}: zone {name} KEPT {e[1]!r} (page said {levels!r})")
            return
    zs.append([name, levels] if levels else [name])
    log.append(f"  {key}: zone ADDED {name} {levels or ''}")


def note(key, *texts):
    ns = M[key].setdefault("notes", [])
    for t in texts:
        if t not in ns:
            ns.append(t)


def stamp(key, fam, job=None, crys=None, kit=True, ab=None):
    """Family stamp: fam + optional page job/crystal + the family kit into an empty `ab`."""
    assert fam in FAMS and ECO.get(fam), (key, fam)
    setif(key, "fam", fam)
    if job: setif(key, "job", job)
    if crys: setif(key, "crys", crys)
    if ab is not None:
        setif(key, "ab", ab); log.append(f"  {key}: PAGE names a smaller kit -> {ab}")
    elif kit:
        k, n, tot = modal_kit(fam)
        if k: setif(key, "ab", k); log.append(f"    ({fam} modal kit {n}/{tot})")


# 1. Morille Mortelle — Funguar, Warrior, Dark. Page's Traits and Abilities names TWO moves.
stamp("morille mortelle", "Funguar", "Warrior", "Dark", ab=["Microspores", "Dark Spore"])
add_det("morille mortelle", ["Scent"])
note("morille mortelle",
     "Roughly 20,000 HP. Rages after 60 minutes and deaggros frequently when kited.",
     "Standard attacks carry Additional Effect: Plague.",
     "Microspores transfers its own negative status effects to everything in a 10' radius; 1-3 shadow images absorb it, and the effects do not transfer through an absorbed hit.",
     "Dark Spore is dark breath damage with Additional Effect: Blind, up to 1005 damage until it is below 15% HP; being a breath attack it can be resisted.",
     "Resistant if not immune to Weight, Bind, Sleep and Poison; susceptible to Paralyze, Blind and Slow.",
     "Placeholder is the Witch Hazel at the southern edge of (I-10) / northern edge of (I-11), the last one before the Puroboros room; Witch Hazels respawn every 16 minutes 10 seconds and Morille Mortelle spawns among the Puroboros.",
     "Window opens about 5 hours after its last time of death.")

# 2. Ogler — Ahriman, Warrior/Black Mage, Dark. Keep [S] 80-82 added, Baileys [S] filled 81-82.
stamp("ogler", "Ahriman", "Warrior / Black Mage", "Dark")
zone("ogler", "Castle Zvahl Baileys [S]", "81-82")
zone("ogler", "Castle Zvahl Keep [S]", "80-82")

# 3-4-7. The Bastion roster, one page at a time (rule 287/290 — NOT one family).
stamp("oppressor", "Chariot")
M["oppressor"]["nm"] = True; log.append("  oppressor: nm = True (Notorious Monster banner)")
note("oppressor", "Spawns during Bastion; only aggressive towards players with Pennant status.")

stamp("overseer", "Iron Giant", ab=["Ballistic Kick"])
setif("overseer", "im", ["Sleep"])
note("overseer",
     "Spawns during Bastion, but is a rare enemy — the conditions for it to appear are unknown.",
     "Only aggressive to players with Pennant status.",
     "Ballistic Kick is a conal attack that reduces HP to critical and inflicts 30-second Encumbrance plus moderate knockback; it reaches a long way but can be outrun, and -PDT gear reduces the damage.")
# scrutinizer: family HELD — see the block at the bottom.
setif("scrutinizer", "ab", ["Reactive Shield"])
note("scrutinizer", "Spawns during Bastion; only aggressive to players with Pennant status.")

# 5. Poxhound — Hound, Dark. Page adds Outer RaKaznar 118-121 (the deserter draugar pattern).
stamp("poxhound", "Hound", None, "Dark")
zone("poxhound", "Outer RaKaznar", "118-121")

# 6. Procrustes — Gigas, Black Mage. Forced spawn, level-capped fight.
stamp("procrustes", "Gigas", "Black Mage")
note("procrustes",
     "Spawned by selecting the Shredded Label at (G-4) in Vunkerl Inlet [S] while holding the Red-Labeled Crate key item; a level 70 cap is placed on the fight.",
     "Assisted by six Jotunn Ruffians and casts ice-based magic.",
     "Drops no gil and cannot be mugged.")

# 8. Sengann — Fomor, Samurai, Dark.
stamp("sengann", "Fomor", "Samurai", "Dark")
note("sengann",
     "Roughly 5,500-6,000 HP. Spawns between 20:00 and 22:00 at (F-8) on the cliff in Lufaise Meadows and despawns around 04:00.",
     "Has an innate Zanshin effect, and its accuracy rises as its HP falls.",
     "Uses Barbed Crescent regardless of TP, and nearly nonstop below 20% HP.",
     "Melee attacks carry an additional curse effect that cuts about a third of maximum HP.",
     "Immune or highly resistant to Bind, Sleep and Gravity, but not to Shadowbind; cannot be bound by Regurgitation.",
     "Only aggressive while you hold Fomor Hate — it will not aggro to resting or low HP once hate is reset.")

# 9-10-12. The Skeleton trio — Earth crystal, same grid, three different zones.
stamp("skinnymajinx", "Skeleton", "Black Mage", "Earth")
zone("skinnymajinx", "Inner Horutoto Ruins", "81-84", force=True)
stamp("skinnymalinks", "Skeleton", "Warrior", "Earth")
zone("skinnymalinks", "Inner Horutoto Ruins", "81-83")
stamp("sodden bones", "Skeleton", "Warrior", "Earth")

# 11. Slabspitter Jagil — AI answer panel, NOT BG: family only (rev-336 precedent).
stamp("slabspitter jagil", "Pugil")

# 13. Stabnix Skewerfinger — Goblin, Thief. Page notes A, L, S.
stamp("stabnix skewerfinger", "Goblin", "Thief")
M["stabnix skewerfinger"]["agg"] = True; log.append("  stabnix skewerfinger: agg = True")
note("stabnix skewerfinger",
     "Roughly 10,000 HP. Immune to sleep. Melee hits land for 100-220 and crit for over 400.",
     "Spawned for the quest Succor to the Sidhe, about 15' west of the Watchful Pixie, together with ten Pixie Impalers — it resummons them if they are defeated, heralded by jumping up and down.",
     "The Pixie Impalers share its hate and hit for 50-100. Using a weapon skill on any of the NMs makes them use Final Sting, which kills them if it lands; it misses a Paladin under Invincible.",
     "It uses Perfect Dodge around 60% HP and the Impalers copy it, then spam Sharp Sting.",
     "Goblin Rush hits a Paladin for around 500 and a damage dealer for up to 850.")

# 14. Suspended Sculpture — Structure. The page publishes NOTHING else: every other cell is '?'.
#     No kit stamp — only one Structure record carries `ab` at all, which is not a family kit.
stamp("suspended sculpture", "Structure", kit=False)

# 15. Talacca Clot — Slime, Warrior, Water. Level cell reads "Fished up" = the SKIP sentinel.
stamp("talacca clot", "Slime", "Warrior", "Water")
setif("talacca clot", "spawn", "Fished up")

# ---------------- guards ----------------
assert set(M) == keyset_before, "key set changed"
assert not [k for m in M.values() for k, v in m.items() if v is None], "null poison"
undef = {a for v in M.values() for a in (v.get("ab") or []) if a not in A}
assert len(undef) <= 14, f"this rev added undefined ability names: {sorted(undef)}"
for k in KEYS:
    f = M[k].get("fam")
    if f is not None:
        assert f in FAMS and ECO.get(f), (k, f, "family missing or has no eco")
for k, old in before.items():
    for fld, val in old.items():
        if isinstance(val, (str, int)) and fld not in ("agg", "lnk", "nm"):
            assert M[k].get(fld) == val, (k, fld, "clobbered")

json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)
print("\n".join(log))
print()
print("HELD:", [k for k in KEYS if not M[k].get("fam")])
print("mobs", len(M), "| orphans", sum(1 for v in M.values() if not v.get("fam")),
      "| NM-flagged", sum(1 for v in M.values() if v.get("nm")),
      "| undefined ability names", len(undef))
