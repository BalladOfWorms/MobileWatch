#!/usr/bin/env python3
"""
Rev 344 — Unknown bucket, section 2, batch 6. CLOSES SECTION 2.
14 BG mob pages (one AI panel) + two user rulings:
  "wintry cave is a reive, should be in environment"
  "the bastion chariot block are family chariot"

The Bastion ruling is applied ONLY to the records with no page of their own
(`custodian`, `scrutinizer`). `earth mover` (Acrolith) and `overseer` (Iron Giant)
were stamped from their OWN pages at revs 341/343 — rule 287 — and are left alone.

LOAD-MERGE-WRITE (rule 286). Guards: fill-only except the logged CORRECTIONS;
every `ab` name asserted against the abilities dict (284); every `fam` asserted to
exist in family_eco (143); no None values.
Author: BalladOfWorms
"""
import json, sys, collections

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
PATH = f"{ASSETS}/mobs.json"

with open(PATH, encoding="utf-8") as f:
    d = json.load(f)
mobs, abilities, family_eco = d["mobs"], d["abilities"], d["family_eco"]


def kit(fam):
    """Modal `ab` set of a family — computed live, never typed (rev-342 method)."""
    mem = [v["ab"] for v in mobs.values() if v.get("fam") == fam and v.get("ab")]
    c = collections.Counter(tuple(sorted(a)) for a in mem)
    return list(c.most_common(1)[0][0])


SIDHE = "Spawned for the quest Succor to the Sidhe."

BATCH = {
    # ---------------------------------------------------------------- pages
    "tiffenotte": dict(
        fam="Pixie", job="White Mage", crys="Wind", agg=True,
        ab=["Spring Breeze", "Lethe Arrows"],      # page: "alternates between" these two
        sp=["Banishga II", "Holy", "Flash"],
        wk_add=[["Ice", None]],
        notes=[
            "Spawns at (G-5). Respawns roughly 2 hours to 2 hours 20 minutes after the last time "
            "of death, very rarely exceeding a 10 minute window.",
            "Casts Divine magic including Banishga II, Holy and Flash.",
            "Appears to have very high magic accuracy — most spells land unresisted even on Carbuncle.",
            "Does not appear to have very strong physical attacks.",
            "Alternates between Spring Breeze and Lethe Arrows, using Spring Breeze constantly but "
            "not spamming it.",
            "Does not follow normal Pixie behaviour (curing and raising adventurers), and pixies "
            "will not shun an adventurer who fights or slays it.",
            "Soloable on Dancer 77 / Ninja 37 despite Spring Breeze's TP reduction; Trance covers "
            "the amnesia from Lethe Arrows.",
        ]),
    "torvotaur": dict(
        fam="Taurus", job="Warrior", agg=True, ab=kit("Taurus"),
        notes=[
            "Spawned with Megalotaur for the quest Succor to the Sidhe.",
            "Very highly resistant, probably immune, to any form of Sleep even with Elemental Seal.",
            "Two blink tanks are recommended to handle both taurs.",
            "Uses its two-hour ability and TP moves in unison with Megalotaur.",
            "Hate is reset when Mortal Ray and Mighty Strikes are used.",
            "Highly resistant to magic — Ancient Magic II landed for roughly 80-140 damage.",
            "Completely resistant to Shadowbind.",
            "Ranged attacks are highly effective, as is a Summoner using Leviathan's Spinning Dive "
            "alongside a shadow kiter.",
        ]),
    "viseclaw": dict(
        fam="Crab", crys="Water", agg=True, ab=kit("Crab"),
        notes=["Spawns in the water around (E-9) to (F-12) on Map 3.", "8 spawn points."]),
    "voirloup": dict(
        fam="Gnole", job="Monk", crys="Dark", agg=True,
        ab=["Nox Blast"],                          # page: "Only uses Nox Blast"
        notes=[
            "Spawns on the north side at (G-9); the placeholder is the first Decrepit Gnole north "
            "of the watchtower.",
            "Respawn time is unattested — one camper measured 3 hours 38 minutes after the first "
            "time of death and 3 hours 44 minutes after the second.",
            "16,500-17,000 HP and effectively no MP — Aspir returns 0.",
            "Resistant to Stun, Gravity and Bind.",
            "Has Double Attack and an Enstun effect.",
        ]),
    "warabouc": dict(
        fam="Bugard", crys="Fire", agg=True,
        ab=["Bone Crunch", "Tusk"],                # page: "Uses ... TP moves only"
        notes=[
            "Located around (I-9).",
            "Two-hour timed spawn, with roughly a 10 minute window opening 2 hours after death.",
            "Around 8,500 HP.",
            "Hits extremely hard — 200-280 on normal hits against decently geared Monk, Samurai "
            "and Beastmaster.",
            "Resists Gravity and Sleep.",
            "Unlike normal Bugards, its Bone Crunch and Tusk are almost instant.",
        ]),
    "wayward bhoot": dict(
        fam="Ghost", ab=kit("Ghost"),
        notes=["Spawns at (L-3) on Map 1.", "2 spawn points."]),
    "wintry cave": dict(                            # USER RULING (BG says family "Lairs")
        fam="Environment", nm=True,
        notes=[
            "Periodically spawns enemies which protect the cave.",
            "Can be fought during Lair Reives — one per reive.",
            "Cannot be damaged without the Fragmenting skill.",
        ]),
    "yal-un eke": dict(
        fam="Cluster", job="Warrior",
        ab=["Sling Bomb"],                          # page: "Only uses Sling Bomb TP move"
        notes=[
            "Spawns in the clearing at (I-8)/(I-9)/(J-8)/(J-9), south of Leremieu Lagoon, in place "
            "of one of the two Clusters during foggy weather. Foggy weather only occurs when no "
            "weather symbol is active.",
            "Around 5,000 HP; soloable by a prepared level 75 job.",
            "Seems to have Regain, or to gain TP extremely fast — used TP moves after only 4 hits "
            "from a level 75 Ninja.",
            "Has Double Attack.",
            "Can spawn on consecutive days, roughly 50 minutes apart, though rarely because of the "
            "weather condition.",
        ]),
    "aa'bho slashburner": dict(
        fam="Quadav", job="Black Mage", crys="Water", agg=True, ab=kit("Quadav"),
        zone_add=[["Rolanberry Fields [S]"]],
        wk_add=[["Lightning", None]],
        notes=[
            SIDHE + " Aa'Bho Slashburner, Bo'Gha Winterkill, Du'Vha Grimwind, Ea'Zhu Tremorcrag, "
            "Gi'Rho Wrathstorm and He'Dho Spatsurge all spawn.",
            "Like the other five quadavs in the battle he casts magic tied to one element — "
            "Aa'Bho uses Fire.",
            "Casts progressively stronger spells as the other quadavs die: tier 4s, then Ancient "
            "Magic II, then -aga III, then an enfeeble-ga or enhancing-ga.",
            "Casts Dispelga as its enfeeble-ga.",
        ]),
    "astika": dict(
        fam="Gargouille", agg=True, ab=kit("Gargouille"), sp=["Stun"],
        zone_add=[["Beaucedine Glacier [S]"]],
        notes=[SIDHE + " Astika, Kaliya, Shesha and Vasuki all spawn.", "Can cast Stun."]),
    "balamor's sycophant": dict(
        fam="Dullahan", agg=True, ab=kit("Dullahan"),
        zone_add=[["Rala Waterways [U]"]],
        det_add=["True Sight", "True Sound"],
        notes=[
            "Attacks player characters during Seekers of Adoulin Mission 4-32: Balamor's Ruse, "
            "while the Regicidal Dullahan attempts to assassinate Arciela.",
            "2 spawn; no drops and nothing to steal.",
        ]),
    "boobrie": dict(                                # AI panel names NO family — left unstamped
        zone_add=[["Reisenjima"]],
        notes=[
            "An add spawned as part of the Geas Fete fight with Erinys in Reisenjima — Erinys "
            "starts the battle with five Boobrie guards.",
            "The guards build TP over time to generate Levin Wind effects; leaving them alive "
            "causes heavy knockback and regain pressure across the battlefield.",
        ]),
    "chahnameed": dict(
        fam="Doomed", crys="Dark", agg=True, ab=kit("Doomed"),
        zone_add=[["Qu'Bia Arena"]],
        det_add=["True Sound"],
        notes=["Appears in the battlefield An Awful Autopsy."]),
    "cinderwing": dict(
        fam="Lesser Bird", agg=True, ab=kit("Lesser Bird"),
        zone_add=[["Sauromugue Champaign [S]"]],
        notes=[SIDHE, "4 spawn points."]),

    # ------------------------------------------------- USER RULING: Bastion block
    # Applied ONLY where no page of its own exists. earth mover (Acrolith, r341) and
    # overseer (Iron Giant, r343) were stamped from their own pages — rule 287.
    "custodian": dict(fam="Chariot", ab=kit("Chariot"),
                      notes=["Spawns during Bastion; only aggressive towards players with "
                             "Pennant status."]),
    "scrutinizer": dict(fam="Chariot"),             # closes rule 292's "Spheroids" hold

    # -------------------------------------- Succor to the Sidhe siblings, page-named
    # Aa'Bho's page calls them "the other 5 quadavs involved in this battle" — that is a
    # family STATEMENT, not a name guess. Both "missing" ones exist under a fuzzy spelling.
    "bo'gha winterkill": dict(fam="Quadav", agg=True, ab=kit("Quadav"),
                              zone_add=[["Rolanberry Fields [S]"]], notes=[SIDHE]),
    "du'vha grimewind": dict(fam="Quadav", agg=True, ab=kit("Quadav"),
                             zone_add=[["Rolanberry Fields [S]"]], notes=[SIDHE]),
    "ea'zhu tremorcrag": dict(fam="Quadav", agg=True, ab=kit("Quadav"),
                              zone_add=[["Rolanberry Fields [S]"]], notes=[SIDHE]),
    "gi'rho wrathstorm": dict(fam="Quadav", agg=True, ab=kit("Quadav"),
                              zone_add=[["Rolanberry Fields [S]"]], notes=[SIDHE]),
    "he'dho spatesurge": dict(fam="Quadav", agg=True, ab=kit("Quadav"),
                              zone_add=[["Rolanberry Fields [S]"]], notes=[SIDHE]),
    # zone anchors only — their families are NOT stated by any page in this batch
    "megalotaur": dict(zone_add=[["Xarcabard [S]"]],
                       notes=["Spawned with Torvotaur for the quest Succor to the Sidhe."]),
    "kaliya": dict(zone_add=[["Beaucedine Glacier [S]"]], notes=[SIDHE + " With Astika, Shesha and Vasuki."]),
    "shesha": dict(zone_add=[["Beaucedine Glacier [S]"]], notes=[SIDHE + " With Astika, Kaliya and Vasuki."]),
    "vasuki": dict(zone_add=[["Beaucedine Glacier [S]"]], notes=[SIDHE + " With Astika, Kaliya and Shesha."]),
}

# page level ~73 vs a stored [72,72]; rule 9 extends, never overwrites
LV_WIDEN = {"tiffenotte": [72, 73]}
ZONE_LV_FILL = {"tiffenotte": ("West Sarutabaruta [S]", "~73"),
                "voirloup": ("Jugner Forest [S]", "~88")}

log, declined = [], []
for key, spec in BATCH.items():
    mob = mobs[key]
    if "fam" in spec:
        assert spec["fam"] in family_eco, f"{spec['fam']} has no family_eco entry"
    for name in spec.get("ab", []):
        assert name in abilities, f"undefined ability {name!r} on {key}"

    for field in ("fam", "job", "crys", "nm", "agg", "ab", "sp", "im", "notes", "lv"):
        if field not in spec:
            continue
        if not mob.get(field):
            mob[field] = spec[field]
            log.append(f"  {key}: {field} = {spec[field]!r}")
        else:
            declined.append(f"  {key}: {field} KEPT {mob[field]!r} (page said {spec[field]!r})")

    for field, adds in (("wk", spec.get("wk_add")), ("st", spec.get("st_add"))):
        for pair in adds or []:
            cur = mob.get(field) or []
            if any(e[0] == pair[0] for e in cur):
                declined.append(f"  {key}: {field} already has {pair[0]} — page direction not written")
                continue
            mob[field] = cur + [pair]
            log.append(f"  {key}: {field} += {pair!r}")

    for glyph in spec.get("det_add", []):
        cur = mob.get("det") or []
        if glyph not in cur:
            mob["det"] = cur + [glyph]
            log.append(f"  {key}: det += {glyph}")

    for z in spec.get("zone_add", []):
        cur = mob.get("zones") or []
        if any(e[0] == z[0] for e in cur):
            declined.append(f"  {key}: already has zone {z[0]}")
            continue
        mob["zones"] = cur + [list(z)]
        log.append(f"  {key}: zone += {z[0]}")

for key, lv in LV_WIDEN.items():
    old = mobs[key].get("lv")
    new = [min(old[0], lv[0]), max(old[1], lv[1])] if old else lv
    if new != old:
        mobs[key]["lv"] = new
        log.append(f"  !! {key}: lv widened {old} -> {new}")

for key, (zone, lv) in ZONE_LV_FILL.items():
    for z in mobs[key].get("zones") or []:
        if z[0] == zone and len(z) == 1:
            z.append(lv)
            log.append(f"  !! {key}: zone {zone} level filled {lv!r}")

print("\n".join(log))
print("\nDECLINED (fill-only guard held):")
print("\n".join(declined) or "  none")

assert not [k for v in mobs.values() for k, val in v.items() if val is None], "None leaked in"
undef = [a for v in mobs.values() for a in (v.get("ab") or []) if a not in abilities]
print("\nundefined ability references:", len(set(undef)), "names /", len(undef), "uses")
print("orphans (fam missing):", sum(1 for v in mobs.values() if not v.get("fam")))
print("mobs:", len(mobs), "| NM-flagged:", sum(1 for v in mobs.values() if v.get("nm")))

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, separators=(", ", ": "))
print("written", PATH)
