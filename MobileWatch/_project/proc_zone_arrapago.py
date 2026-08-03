#!/usr/bin/env python3
"""
proc_zone_arrapago.py — rev 302. Three jobs in one script:

  1. Refining-phase zone pass: Arrapago Reef (75 page records, 17 NM + 59 ADV,
     `Lamia Palace Guard` appearing in BOTH tables).
  2. `dark rider` built out from its own mob page + USER: "the dark rider needs an entry
     and gets the odin image".
  3. RULE 138 CLOSED — the 7 unresolved abjuration rows, resolved structurally.

THE ABJURATION RULE (derived, verified 13/13 on the known families):
    ffxi_items.json abbreviates an abjuration family to its own FIRST TWO LETTERS when that
    two-letter prefix exists in the item list, and to the BARE FIRST LETTER otherwise. It never
    assigns both forms to one family. Aquarian/Dryadic/Earthen/Martial/Neptunal/Wyrmal have no
    Aq./Dr./Ea./Ma./Ne./Wy. entry so they take A./D./E./M./N./W.; Abyssal/Arean/Bushin/Grove/
    Jovian/Vale/Venerian all have their two-letter form and take it.
    => Cronian -> Cr.  ·  Cyllenian -> Cy.  ·  Shinryu -> Sh.  ·  Triton -> Tr.
    The bare C./S./T. sets belong to three families we have not met.

Rule 15 SKIP sentinel as always: a blank page cell can create a zone entry but never touch a level.

Author: BalladOfWorms
"""
import json, os, sys

SKIP = object()
ZONE = "Arrapago Reef"
ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
MOBS = os.path.join(ASSETS, "mobs.json")

# --- Notorious Monsters (17). `80-80`/`81-81`/`88-88`/`77-77` collapse to a point per the
# established convention (zoneinfo does the same).
ROWS = {
    "bloody bones": SKIP, "euryale": "~80", "giant orobon": "78-83",
    "lamie no.7": SKIP, "lamie no.8": SKIP, "lamie no.9": "~80", "lamie no.19": "78",
    "lil' apkallu": "80-85", "medusa": SKIP, "merrow no.5": "82-85", "nuhn": "80-90",
    "velionis": SKIP, "zareehkl the jubilant": "80-90", "bukki": SKIP,
    "ornery orobon": SKIP, "lamia palace guard": SKIP, "dimgruzub": SKIP,
    # --- Adversaries (59; Lamia Palace Guard shared with the NM table) ---
    "archaic mirror": SKIP, "arrapago apkallu": "70-72", "arrapago leech": "73-74",
    "ashakku": "71-74", "chimera clot": "75-76", "dark elemental": "80",
    "draugar servant": "79-81", "draugar's wyvern": "68-74", "emperor apkallu": "81-83",
    "ephramadian shade": "68-70", "fallen imperial trooper": "72-74",
    "fallen imperial wizard": "72-74", "fallen volunteer": "71-73", "heraldic imp": "72-74",
    "ice elemental": "80", "jnun": "72-77", "lahama": "76-79", "lamia bellydancer": "81",
    "lamia dancer": "73-75", "lamia dartist": "73-75", "lamia deathdancer": "73-75",
    "lamia exon": SKIP, "lamia fatedealer": "73-75", "lamia graverobber": "73-75",
    "lamia idolater": "79-81", "lamia necromancer": "81-83", "lamia toxophilite": "77-80",
    "lamia's avatar": SKIP, "lamia's elemental": SKIP, "lamia's skeleton": SKIP,
    "lamie bellydancer": "81-83", "lamie deathdancer": "77-80", "lamie necromancer": "81-83",
    "lamie toxophilite": "77-80", "llamhigyn y dwr": "76-78", "merrow bladedancer": "81-83",
    "merrow chantress": "73-75", "merrow icedancer": "73-75", "merrow kabukidancer": "73-75",
    "merrow shadowdancer": "73-75", "merrow songstress": "81-83",
    "merrow typhoondancer": "81-83", "merrow wavedancer": "81-83", "nergal": "88",
    "nipper": "72-73", "nix bladedancer": "81-83", "nix songstress": "81-83",
    "nix typhoondancer": "81-83", "nix wavedancer": "81-83", "phasma": "73-74",
    "purgatory bat": "72-73", "qiqirn trailer": "77", "qiqirn treasure hunter": "77",
    "qutrub": "73-74", "reserve draugar": "72-74", "seneschal imp": "77-78",
    "soulflayer": "79-82", "wootzshell": "70-71",
}

ABJ_FIX = {
    "ma":      [("Cronian Abjuration: Feet", "Cr.Abjuration: Ft."),
                ("Triton Abjuration: Hands", "Tr.Abjuration: Hn.")],
    "bia":     [("Cronian Abjuration: Hands", "Cr.Abjuration: Hn.")],
    "khun":    [("Shinryu Abjuration: Feet", "Sh.Abjuration: Ft.")],
    "naphula": [("Cyllenian Abjuration: Head", "Cy.Abjuration: Hd."),
                ("Shinryu Abjuration: Head", "Sh.Abjuration: Hd."),
                ("Triton Abjuration: Legs", "Tr.Abjuration: Lg.")],
}

DARK_RIDER_ZONES = ["Caedarva Mire", "Mount Zhayolm", "Wajaom Woodlands"]
DARK_RIDER_NOTES = [
    "Appears at random in its listed areas and despawns after a time.",
    "Summons Dark Esquire (Demon) and Dark Bugler (Imp), both of which aggro.",
    "May cast Death.",
    "No known method of damaging it exists; it appears for the Treasures of Aht Urhgan "
    "missions and is not meant to be defeated.",
]


def zname(e):
    return e[0] if isinstance(e, list) else e


def main():
    d = json.load(open(MOBS, encoding="utf-8"))
    mobs = d["mobs"]
    items = json.load(open(os.path.join(ASSETS, "ffxi_items.json"), encoding="utf-8"))
    NAMES = {v["n"] for v in items.values() if isinstance(v, dict) and "n" in v}

    missing, added, changed, filled, kept = [], [], [], [], []
    for key, lvl in ROWS.items():
        r = mobs.get(key)
        if r is None:
            missing.append(key)
            continue
        zs = r.get("zones")
        if not isinstance(zs, list):
            zs = []
        idx = next((i for i, e in enumerate(zs) if zname(e) == ZONE), None)
        if idx is None:
            zs.append([ZONE] if lvl is SKIP else [ZONE, lvl])
            added.append((key, None if lvl is SKIP else lvl, len(zs) == 1))
            r["zones"] = zs
            continue
        ent = zs[idx]
        cur = ent[1] if isinstance(ent, list) and len(ent) > 1 else None
        if lvl is SKIP:
            kept.append((key, cur))
        elif cur is None:
            zs[idx] = [ZONE, lvl]
            filled.append((key, lvl))
        elif cur != lvl:
            zs[idx] = [ZONE, lvl]
            changed.append((key, cur, lvl))

    # --- rule 138 closure -------------------------------------------------
    abj = []
    for key, pairs in ABJ_FIX.items():
        r = mobs.get(key)
        s = r.get("drops") or ""
        for old, new in pairs:
            assert new in NAMES, f"{new!r} not in ffxi_items.json"
            if old in s:
                s = s.replace(old, new)
                abj.append((key, old, new))
        r["drops"] = s

    # --- dark rider -------------------------------------------------------
    dr = mobs["dark rider"]
    dr_report = []
    if dr.get("fam") != "Avatar":
        dr["fam"] = "Avatar"
        dr_report.append("fam -> Avatar (page info box Family row; rule 19)")
    if dr.get("img") != "mobimages/odin prime.png":
        dr["img"] = "mobimages/odin prime.png"
        dr_report.append("img -> mobimages/odin prime.png (USER)")
    zs = dr.get("zones") or []
    have = {zname(e) for e in zs}
    for z in DARK_RIDER_ZONES:
        if z not in have:
            zs.append([z])
            dr_report.append(f"zone += {z}")
    dr["zones"] = zs
    notes = dr.get("notes") or []
    for n in DARK_RIDER_NOTES:
        if n not in notes:
            notes.append(n)
    dr["notes"] = notes
    dr_report.append(f"notes -> {len(notes)} bullets")
    sp = dr.get("sp") or []
    if "Death" not in sp:
        sp.append("Death")
        dr["sp"] = sp
        dr_report.append("sp += Death (page: 'May cast Death.')")

    bad = [k for m_ in mobs.values() for k, v in m_.items() if v is None]
    assert not bad, f"null-valued keys written: {bad[:5]}"
    json.dump(d, open(MOBS, "w", encoding="utf-8"),
              separators=(", ", ": "), ensure_ascii=False)

    print(f"=== {ZONE} — {len(ROWS)} page records")
    print(f"MISSING ({len(missing)}): {missing}")
    print(f"\nZONE ADDED ({len(added)})  [*] = record had NO zones at all before:")
    for k, v, first in added:
        print(f"   {'*' if first else ' '} {k:26s} {v}")
    print(f"\nLEVEL FILLED ({len(filled)}):")
    for k, v in filled:
        print(f"     {k:26s} -> {v}")
    print(f"\nLEVEL CHANGED ({len(changed)}):")
    for k, a, b in changed:
        print(f"     {k:26s} {a} -> {b}")
    print(f"\nKEPT, page cell blank ({len(kept)}):")
    for k, v in kept:
        print(f"     {k:26s} stored {v}")
    n_ok = len(ROWS) - len(added) - len(filled) - len(changed) - len(missing)
    print(f"\nAlready right (incl. blank keeps): {n_ok} of {len(ROWS)}")
    print(f"\n=== RULE 138 CLOSED — abjuration rewrites ({len(abj)}):")
    for k, a, b in abj:
        print(f"     {k:10s} {a!r} -> {b!r}")
    print(f"\n=== dark rider:")
    for line in dr_report:
        print("     " + line)


if __name__ == "__main__":
    main()
