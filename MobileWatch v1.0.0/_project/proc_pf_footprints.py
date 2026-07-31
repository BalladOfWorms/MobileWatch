#!/usr/bin/env python3
"""Peculiar Foes — footprint locations into `spawn` (rev 187).
USER: "lets update the peculiar foe entries with the footprint location"
Source = the same RoE objective table. `spawn` renders in the card's Details box;
only `awoken nihhus` had one. Existing notes are left alone (additive)."""
import json, os
from zonepass import ASSETS

SPAWN = {
    "awoken hildesvini":     "Peculiar Footprints \u2014 Wajaom Woodlands (H-13)",
    "awoken mokkuralfi":     "Peculiar Footprints \u2014 Mount Zhayolm (I-10)",
    "awoken vampyr jarl":    "Peculiar Footprints \u2014 Caedarva Mire (I-6), Hediva Isle",
    "awoken gorgimera":      "Peculiar Footprints \u2014 Beaucedine Glacier (K-6)",
    "awoken ariri samariri": "Peculiar Footprints \u2014 Palborough Mines (G-10), Map 3",
    "awoken hrungnir":       "Peculiar Footprints \u2014 Aydeewa Subterrane (E-7), Map 2",
    "awoken morbol emperor": "Peculiar Footprints \u2014 Arrapago Reef (H-6), Map 3",
    "awoken stoorworm":      "Peculiar Footprints \u2014 Reisenjima, Ethereal Ingress #9",
    "awoken dendainsonne":   "Peculiar Footprints \u2014 Western Altepa Desert (I-6)",
    "awoken freke":          "Peculiar Footprints \u2014 Batallia Downs (J-7), on the road",
    "awoken tanngrisnir":    "Peculiar Footprints \u2014 Qufim Island (G-8)",
    "awoken nihhus":         "Peculiar Footprints \u2014 Kamihr Drifts (F-8)",
    "awoken hakenmann":      "Peculiar Footprints \u2014 Rala Waterways (N-5)",
    "awoken andhrimnir":     "Peculiar Footprints \u2014 Newton Movalpolos (L-9)",
    "awoken angantyr":       "Peculiar Footprints \u2014 Xarcabard (D-8)",
    "awoken hjorvarth":      "Peculiar Footprints \u2014 Xarcabard (D-8)",
    "awoken hrani":          "Peculiar Footprints \u2014 Xarcabard (D-8)",
}
p = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(p, encoding='utf-8')); mobs = d['mobs']
set_, changed = [], []
for k, s in SPAWN.items():
    m = mobs[k]
    old = m.get('spawn')
    m['spawn'] = s
    (changed if old else set_).append(f"{k}" + (f"  (was {old!r})" if old else ""))
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print(f"spawn SET on {len(set_)}: {', '.join(sorted(set_))}")
print(f"spawn REPLACED on {len(changed)}: {', '.join(changed) or '(none)'}")
