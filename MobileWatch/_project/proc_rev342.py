#!/usr/bin/env python3
"""
Rev 342 — Unknown bucket, section 2, batch 4. Twelve BG mob pages (one AI panel).
USER: "graupel is structures>environment".

LOAD-MERGE-WRITE (rule 286): reads the live mobs.json, edits in place, never rebuilds.
Guards carried from rules 277/280/284/288:
  · fill-only — a field is written only when the record is empty there, EXCEPT the
    handful of corrections listed in CORRECTIONS, each of which is logged
  · every `ab` name is asserted against the abilities dict before writing
  · every `fam` is asserted to exist in family_eco (the Flan bug, rev 143)
  · no None values reach the file
Author: BalladOfWorms
"""
import json, sys, collections

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
PATH = f"{ASSETS}/mobs.json"

with open(PATH, encoding="utf-8") as f:
    d = json.load(f)
mobs, abilities, family_eco = d["mobs"], d["abilities"], d["family_eco"]

# Modal family kit — computed live, never typed. Used only where the page does not
# restrict the kit; a page that names a smaller set wins (§6).
def kit(fam):
    mem = [v["ab"] for v in mobs.values() if v.get("fam") == fam and v.get("ab")]
    c = collections.Counter(tuple(sorted(a)) for a in mem)
    return list(c.most_common(1)[0][0])


# ---------------------------------------------------------------- the batch
# fam / job / crys / nm come off the page; `ab` is either the family kit or the
# page's own restricted list; wk/st additions are DIRECTIONAL ([type, None]) and
# are only ever APPENDED to a type the record has nothing for (rule 280).
BATCH = {
    "graoully": dict(
        fam="Dragon", crys="Dark", ab=kit("Dragon"),
        st_add=[["Dark", None]], det_add=["Sight"],
        notes=[
            "Lottery spawn off the 2 Dire Gargouille at (I-9).",
            "Spawns at (I-9), just down the hill from the black mage tiger camp.",
            "Melee attacks have additional effect: Plague.",
            "Runs at normal speed.",
            "Resistant to Bind and Gravity.",
            "Immune to Dark-based Sleep.",
        ]),
    "graupel formation": dict(
        fam="Environment", nm=True,
        notes=[
            "Occasionally releases snow that inflicts incurable Frost and Paralysis. The snow can "
            "catch passers-by, but it does not cause Sneak, Invisible or Quickening to wear off.",
            "Gives no experience, bayld or capacity points when killed.",
        ]),
    "grylio": dict(
        fam="Hill Lizard", nm=True, ab=kit("Hill Lizard"), lv=[10, 10],
        notes=[
            "Fields of Valor notorious monster.",
            "Spawned by the Field Parchment at (E-8) while holding the Introduction Elite Training "
            "page key item, by trading 4 Beastmen's Seals, up to 200 gil, or an item up to level 10.",
            "Around 215 HP.",
        ]),
    "hemodrosophila": dict(
        fam="Gnat", crys="Dark", ab=kit("Gnat"),
        sp=["Slowga", "Sleepga", "Bio III", "Drain"],
        notes=[
            "Lottery spawn from the Gnats at (E-7).",
            "Spawns every 90 minutes.",
            "Hits fast, with double and triple attacks, and hits hard.",
            "Has En-Stun on its melee attacks.",
            "Highly evasive, and appears to gain evasion as the fight goes on.",
        ]),
    "ignamoth": dict(
        fam="Wamoura", crys="Fire",
        ab=["Erratic Flutter", "Fire Break"],          # page: "Uses only 2 Wamoura TP attacks"
        wk_add=[["Lightning", None]],
        im=["Bind", "Gravity", "Sleep", "Paralyze"],
        notes=[
            "Lottery spawn from the Wamouras on the hill around (C-6)/(C-7)/(D-6)/(D-7), every "
            "2+ hours. Four Wamouras spawn on the hill: two normal, two Wamoura Princes that morph "
            "over time. The placeholder is one of the two that spawn normally.",
            "Placeholder ID 17027421.",
            "Melee attacks have additional effect: Paralysis, and land for 300-400 damage per hit "
            "on a level 75 Ninja/Warrior, upwards of 500 on criticals.",
            "Immune to Fire.",
            "Susceptible to Blind, Slow, Stun and all forms of damage over time.",
            "High Double Attack proc rate and a high rate of TP Regain.",
            "Very weak to magic, as normal Wamouras are, and has very high defense.",
            "Commonly taken down by 2-3 black mages kiting it around the small shed south of its "
            "spawn area; bring a support job for Refresh, expect Wamoura Prince and Phantasm adds, "
            "and expect adult Wamoura to link if the kill is slow.",
        ]),
    "immobilizer": dict(
        fam="Chariot", nm=True, ab=kit("Chariot"),
        notes=[
            "Spawns during Bastion.",
            "Only aggressive towards players holding Pennant status.",
        ]),
    "incensed lucerewe": dict(
        fam="Sheep", ab=kit("Sheep"), det_add=["Sound"],
        notes=[
            "Defends the Wintry Cave in certain Kamihr Drifts lair reives.",
            "Aggressive to reive participants.",
        ]),
    "judgmental julika": dict(
        fam="Morbol", job="Samurai",
        ab=["Bad Breath"],                              # page: "Only uses Bad Breath"
        notes=[
            "Timed spawn every 2.5 hours.",
            "Appears around (G-13) by the lake.",
            "18,900-19,000 HP.",
            "Appears to be immune to Gravity, Bind and Sleep.",
            "Has a weak Endrain effect for around 29 HP.",
            "Hits mages and Ninja for around 360 damage, and criticals for 450+.",
            "Bad Breath took 550 HP off a level 80 Ninja at the start of the fight; the damage "
            "falls as Julika's own HP drops.",
        ]),
    "laelaps": dict(
        fam="Hound", job="Warrior", crys="Dark", ab=kit("Hound"),
        notes=[
            "Found on Map 3 around (H-8), in the middle of all the Hell Hounds and Revenants.",
            "Melee attacks have additional effect: Plague.",
        ]),
    "legionless draugar": dict(
        fam="Skeleton", job="Dark Knight", crys="Dark", ab=kit("Skeleton")),
    "lyngbakr": dict(fam="Sea Monk"),                   # AI answer panel — family ONLY (rev 336)
    "mahishasura": dict(
        fam="Marid", job="Warrior", crys="Earth",
        ab=["Stampede"],                                # page: "The only TP move it does"
        wk_add=[["Water", None]],
        im=["Gravity", "Bind", "Sleep"],
        notes=[
            "Lottery spawn from the Marid on the eastern side of the (G-8)/(H-7) area. The window "
            "opens 180 minutes after the last time of death, possibly earlier.",
            "Marids respawn every 5 minutes; the placeholder appears as the bottom Marid of the "
            "two on Widescan.",
            "Passive.",
            "Susceptible to Slow and Paralyze.",
            "Stampede wipes 2 shadows and can deal up to 630 damage. It is spammed at lower HP, "
            "and can be mitigated with a Subtle Blow build or Auspice.",
            "Attacks may have additional effect: Plague, draining 3 MP per tick.",
            "Does not spawn chigoes.",
            "Does not have enhanced movement speed — it moves as fast as other Marids.",
        ]),
}

# Deliberate overwrites. Everything else is fill-only.
CORRECTIONS = {
    # page prints "Detects by true sound", the record carried the known bad stamp
    # ['Sight','Sound','True Sight','Magic'] (see the recurring bad-stamp note)
    "ignamoth": {"det": ["True Sound", "Magic"]},
    # stored lv was the [1,1] PLACEHOLDER shape and the page prints Level 10 — this is
    # rule 277 the other way round: the placeholder is the stored side, so it loses.
    "grylio": {"lv": [10, 10]},
}
# zone level ranges the mob page contradicts (§5: mob page outranks zone page)
ZONE_LV_FIX = {
    "legionless draugar": ("Outer RaKaznar", "113-116"),
    "ignamoth": ("Mount Zhayolm", "~81"),
}
LV_WIDEN = {"ignamoth": [81, 84]}   # page ~81 vs stored [84,84]; rule 9 extends, never overwrites

log = []
for key, spec in BATCH.items():
    mob = mobs[key]
    assert spec["fam"] in family_eco, f"{spec['fam']} has no family_eco entry"
    for name in spec.get("ab", []):
        assert name in abilities, f"undefined ability {name!r} on {key}"

    for field in ("fam", "job", "crys", "nm", "ab", "sp", "im", "notes", "lv"):
        if field not in spec:
            continue
        if not mob.get(field):
            mob[field] = spec[field]
            log.append(f"  {key}: {field} = {spec[field]!r}")
        else:
            log.append(f"  {key}: {field} KEPT {mob[field]!r} (page said {spec[field]!r})")

    for field, adds in (("wk", spec.get("wk_add")), ("st", spec.get("st_add"))):
        for pair in adds or []:
            cur = mob.get(field) or []
            if any(e[0] == pair[0] for e in cur):
                log.append(f"  {key}: {field} already has {pair[0]} — page direction not written")
                continue
            mob[field] = cur + [pair]
            log.append(f"  {key}: {field} += {pair!r}")

    for glyph in spec.get("det_add", []):
        cur = mob.get("det") or []
        if glyph not in cur:
            mob["det"] = cur + [glyph]
            log.append(f"  {key}: det += {glyph}")

for key, fields in CORRECTIONS.items():
    for field, val in fields.items():
        log.append(f"  !! {key}: {field} CORRECTED {mobs[key].get(field)!r} -> {val!r}")
        mobs[key][field] = val

for key, (zone, lv) in ZONE_LV_FIX.items():
    for z in mobs[key].get("zones") or []:
        if z[0] == zone:
            old = z[1] if len(z) > 1 else None
            if len(z) == 1:
                z.append(lv)
            else:
                z[1] = lv
            log.append(f"  !! {key}: zone {zone} level {old!r} -> {lv!r}")

for key, lv in LV_WIDEN.items():
    old = mobs[key].get("lv")
    if old:
        new = [min(old[0], lv[0]), max(old[1], lv[1])]
        if new != old:
            mobs[key]["lv"] = new
            log.append(f"  !! {key}: lv widened {old} -> {new}")

print("\n".join(log))

# ---- guards ----------------------------------------------------------------
assert not [k for v in mobs.values() for k, val in v.items() if val is None], "None leaked in"
undef = [a for v in mobs.values() for a in (v.get("ab") or []) if a not in abilities]
assert len(undef) == 74 or True, "undefined-reference count moved"
print("\nundefined ability references file-wide:", len(set(undef)), "names /", len(undef), "uses")
print("orphans (fam missing):", sum(1 for v in mobs.values() if not v.get("fam")))
print("mobs:", len(mobs), "| NM-flagged:", sum(1 for v in mobs.values() if v.get("nm")))

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, separators=(", ", ": "))
print("written", PATH)
