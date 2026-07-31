#!/usr/bin/env python3
"""
proc_oplenty.py — build out `chest o'plenty` and `coffer o'plenty` (rev 303).

USER: "chest and coffer o plenty need entries, same family as mimic and gets mimic image"

Both records already existed as bare stubs (agg / lnk / det / st / wk only, no fam) and were
therefore sitting in the browser's Other > Unknown orphan pile (rule 17).

IMAGE: no Mimic member carries a `mobimages/` render and none exists on disk. `iconForMob` is
per-mob `img` > family icon `mobicons/<Family>.jpg`, so setting `fam = "Mimic"` is what routes
both records to `mobicons/Mimic.jpg` — the same path all 13 other artless Mimics already take.
No redundant per-mob `img` is written.

The Chest page states "Chest O'Plenty and Coffer O'Plenty have the same behavior", which is what
licenses applying the Coffer page's move list to both.

`Guilded Torpor` — the page spells it "Gilded". The file's existing def is `Guilded Torpor`
(one user, `lacquered mimic`). Pointing at the existing def rather than creating a second one;
the spelling discrepancy is FLAGGED, not resolved here.

Author: BalladOfWorms
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
MOBS = os.path.join(ASSETS, "mobs.json")

NEW_ABILITIES = {
    "Ka-thwack": {
        "d": "Instantly KOs every player and pet in range. A player in range who has Reraise "
             "has it dispelled and takes severe dark damage instead.",
        "tgt": "AoE",
        "fx": ["KO", "Dispel"],
        "notes": "Used at 100%, 69%, 39% and 9% HP. It also grants the user an aura whose "
                 "debuffs depend on its remaining HP: none above 69%, Avoidance Down and "
                 "Muddle between 69% and 9%, and potent Plague plus Avoidance Down and Muddle "
                 "below 9%. Enough damage of the correct element removes the aura.",
    },
    "Booby Prize": {
        "d": "Inflicts one randomly chosen debuff on targets in an area of effect.",
        "tgt": "AoE",
        "fx": ["Random Debuff"],
        "notes": "The roll is one of Defense Down, Magic Defense Down, Attack Down, "
                 "Magic Attack Down, Blind, Paralysis or Petrify.",
    },
    "Pandora's Gift": {
        "d": "Restores a moderate amount of HP to all players in range.",
        "tgt": "AoE",
        "fx": ["Heal"],
    },
    "Slam": {
        "d": "Deals damage to a single target.",
        "t": "Physical",
        "tgt": "Single",
        "fx": ["Damage"],
    },
}

# page-backed enrichment of two defs that already exist
ENRICH = {
    "Calamitous Collapse": {"t": "Physical"},   # currently unset; page says AoE physical
}
CURSE_NOTE = ("Drains roughly 700 HP per tick and lasts about 45 seconds; healers can remove "
              "the Bio component but not the attribute reduction.")

KIT = ["Death Trap", "Draw-In", "Calamitous Collapse", "Double Whammy", "Slam", "Ka-thwack",
       "Booby Prize", "Guilded Torpor", "Pandora's Gift", "Pandora's Curse", "Mighty Strikes"]

PHASES = ("Four phases, switching at 100%, 69%, 39% and 9% HP. Phase 1 is an ordinary NM fight "
          "with its full spell list, physical TP moves and Death Trap. In phase 2 it alternates "
          "between two magic-absorption modes, one absorbing all Light-skillchain damage "
          "(fire, thunder, wind) and the other all Dark-skillchain damage (ice, water, earth); "
          "the switch is triggered by consecutive weapon skills and may be answered with Death "
          "Trap. Phase 3 keeps the absorption, takes greatly reduced damage of every type and "
          "adds Pandora's Curse and Pandora's Gift. Phase 4 returns to phase-1 damage rules but "
          "with a far stronger Ka-thwack.")
MISTAKE = ("Death Trap is a retaliation for a mistake — healing through the wrong skillchain, "
           "or too many skillchains of the same type in a row.")
IMMUNE = "Immune to Stun and Silence; Lullaby lands."
PROC = ("Red procs remove its absorption mode; enough damage of the correct element procs blue "
        "and strips the aura Ka-thwack leaves behind in phases 1-3.")

RECORDS = {
    "chest o'plenty": {
        "fam": "Mimic",
        "crys": "Light",
        "job": "Black Mage",
        "nm": True,
        "nmlv": "99",
        "ab": KIT,
        "sp": ["Death", "Absorb-TP"],
        "spawn": "Special (failure condition of the A.M.A.N. Trove battlefield)",
        "zones": [["Balgas Dais", "99"], ["Waughroon Shrine", "99"], ["Horlais Peak", "99"]],
        "notes": [
            "Spawns when the A.M.A.N. Trove battlefield is failed, and uses Ka-thwack "
            "immediately — anyone in range without Reraise is KO'd and anyone out of range is "
            "drawn in first.",
            "Behaves identically to Coffer O'Plenty.",
            IMMUNE, PHASES, MISTAKE, PROC,
            "Also casts the -ga III elemental spells and Ancient Magic II.",
        ],
    },
    "coffer o'plenty": {
        "fam": "Mimic",
        "crys": "Light",
        "job": "Black Mage",
        "nm": True,
        "ab": KIT,
        "sp": ["Death", "Absorb-TP"],
        "spawn": "Battlefield (A.M.A.N. Trove — Venus)",
        "notes": [
            "The boss of the A.M.A.N. Trove (Venus) battlefield. Behaves identically to "
            "Chest O'Plenty.",
            IMMUNE, PHASES, MISTAKE, PROC,
            "Mighty Strikes is used at will and always follows the 9% Ka-thwack; in phase 4 it "
            "is reapplied as soon as it wears off.",
            "Also casts the -ga III elemental spells and Ancient Magic II.",
        ],
    },
}


def main():
    d = json.load(open(MOBS, encoding="utf-8"))
    mobs, abils = d["mobs"], d["abilities"]

    created = []
    for name, defn in NEW_ABILITIES.items():
        if name not in abils:
            abils[name] = defn
            created.append(name)

    enriched = []
    for name, patch in ENRICH.items():
        for k, v in patch.items():
            if not abils[name].get(k):
                abils[name][k] = v
                enriched.append((name, k, v))
    cur = abils["Pandora's Curse"]
    if CURSE_NOTE not in (cur.get("notes") or ""):
        cur["notes"] = (cur.get("notes", "") + " " + CURSE_NOTE).strip()
        enriched.append(("Pandora's Curse", "notes", "appended"))

    touched = []
    for key, fields in RECORDS.items():
        r = mobs[key]
        before = sorted(r)
        r.update(fields)
        touched.append((key, before, sorted(r)))

    # every referenced ability must have a def — this file's #1 quality problem is dangling refs
    dangling = [a for key in RECORDS for a in mobs[key]["ab"] if a not in abils]
    assert not dangling, f"dangling ability references: {dangling}"

    bad = [k for m in mobs.values() for k, v in m.items() if v is None]
    assert not bad, f"null-valued keys written: {bad[:5]}"
    json.dump(d, open(MOBS, "w", encoding="utf-8"),
              separators=(", ", ": "), ensure_ascii=False)

    print(f"ABILITY DEFS CREATED ({len(created)}): {created}")
    print(f"ABILITY DEFS ENRICHED ({len(enriched)}): {enriched}")
    print(f"abilities total: {len(abils)}")
    for key, before, after in touched:
        print(f"\n{key}")
        print(f"   fields before: {before}")
        print(f"   fields after : {after}")
        print(f"   fam={mobs[key]['fam']}  icon -> mobicons/Mimic.jpg (family fallback)")
        print(f"   zones={mobs[key].get('zones')}")
    print(f"\nDANGLING ABILITY REFS: 0")


if __name__ == "__main__":
    main()
