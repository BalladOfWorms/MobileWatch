#!/usr/bin/env python3
"""Omen Sweetwater + Transcendent mobs (rev 195) — RECORD CREATION.
USER: "using the families given, add an entry for each into their respective families.
they aggro by sight and do not link. sweetwater are 119 and transcendent are 125-128."

The Omen page names its regular mobs only by family, so one record per family per tier:
  Sweetwater <Family>   lv 119      regular mob
  Transcendent <Family> lv 125-128  nm (the page calls them "Transcendent NMs")
Both aggro by Sight, neither links. Zone = Reisenjima Henge, content = "Omen: Sweetwater Mobs"
(inside that section `nm` lifts the Transcendent rows above the Sweetwater ones).

`Mantises` -> the file's family is **Mantid**. `Faaz` has no family in the file and `Birds`
is ambiguous (Greater Bird / Lesser Bird) — both left out, pending one word from the user.
"""
import json, os
from zonepass import ASSETS

FAMS = ["Tiger", "Fly", "Beetle", "Leech", "Skeleton", "Corpselight", "Ghost", "Doll",
        "Chapuli", "Treant", "Mantid", "Doomed", "Elemental", "Slime", "Lucani", "Worm",
        "Frog", "Raptor", "Mosquito", "Bat", "Hippogryph", "Goobbue", "Pugil", "Rabbit",
        "Mandragora", "Lizard", "Ladybug", "Porxie", "Panopt", "Pixie"]
ZONE, TAG = "Reisenjima Henge", "Omen: Sweetwater Mobs"

p = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(p, encoding='utf-8')); mobs = d['mobs']
known = set(d['families']); icons = d.get('family_icons', {})
before = len(mobs)

made, skipped, no_icon = [], [], []
for fam in FAMS:
    if fam not in known:
        skipped.append(fam); continue
    if fam not in icons:
        no_icon.append(fam)
    for prefix, lv, band, nm in (("Sweetwater", [119, 119], "119", False),
                                 ("Transcendent", [125, 128], "125-128", True)):
        name = f"{prefix} {fam}"
        key = name.lower()
        if key in mobs:
            continue
        rec = {"n": name, "fam": fam, "lv": lv, "agg": True, "lnk": False,
               "det": ["Sight"], "zones": [[ZONE, band]], "content": [TAG]}
        if nm:
            rec["nm"] = True
        mobs[key] = rec
        made.append(key)

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print(f"created {len(made)} records  (mobs {before} -> {len(mobs)})")
print("  " + ", ".join(made[:6]) + " ...")
print("families skipped (not in the file):", skipped or "(none)")
print("families with no icon (would fall back):", no_icon or "(none)")
