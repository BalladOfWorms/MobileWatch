#!/usr/bin/env python3
"""Omen content tags (rev 194).
USER: "omen, including sweetwater mobs and bosses. we need 2 sections, bosses and sweetwater mobs"

`Reisenjima Henge` is Omen's zone, so the roster is projected like Dynamis/Abyssea.
Section `Bosses`: Ou (`: Boss`, the final Caturae), the other five Caturae, and the three
Glassy midbosses of the 3rd area. Section `Sweetwater Mobs`: nothing to tag yet — the Omen
page names the regular mobs only by FAMILY (Tigers, Flies, Beetles, Leeches, Skeletons,
Corpselights, Ghosts, Dolls, Chapuli, Treants, Mantises, Doomed, Elementals, Slimes, Lucani,
Worms, Frogs, Raptors, Mosquitos, Bats, Hippogryphs, Goobbues, Faaz, Pugils, Rabbits,
Mandragoras, Lizards, Birds, Ladybugs, Porxies, Panopts, Pixies) and no per-mob record exists.
"""
import json, os
from zonepass import ASSETS

BOSSES = {"ou": "Omen: Bosses: Boss"}
DEFAULT = "Omen: Bosses"
ROSTER = ["ou", "fu", "gin", "kei", "kin", "kyou", "glassy craver", "glassy gorger", "glassy thinker"]

p = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(p, encoding='utf-8')); mobs = d['mobs']
out = []
for k in ROSTER:
    m = mobs[k]
    tag = BOSSES.get(k, DEFAULT)
    tags = m.get('content') or []
    if tag not in tags:
        m['content'] = tags + [tag]; out.append(f"{k} -> {tag}")
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print(f"tagged {len(out)}:")
for r in out: print("  ", r)
