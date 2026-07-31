#!/usr/bin/env python3
"""Dynamis-Bastok pass + boss + TE, and the Omen Caturae order (rev 198).
USER: "for omen bosses, ou first but then the other caturae next above glassy mobs.
caturae are all level 139. dynamis bastok, arch is zone boss."
"""
import json, os
from zonepass import ASSETS

p = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(p, encoding='utf-8')); mobs = d['mobs']

# ---- Omen: the five non-Ou Caturae get the Midboss role and their published 139 -----
CATURAE = ["fu", "gin", "kei", "kin", "kyou"]
lv_set, role_set = [], []
for k in CATURAE:
    m = mobs[k]
    if m.get('lv') != [139, 139]:
        m['lv'] = [139, 139]; lv_set.append(k)
    for e in m.get('zones', []):
        if isinstance(e, list) and (e[0] == 'Reisenjima Henge') and (len(e) == 1 or e[1] != '139'):
            e[:] = ['Reisenjima Henge', '139']
    tags = [t for t in (m.get('content') or []) if t != "Omen: Bosses"]
    if "Omen: Bosses: Midboss" not in tags:
        tags.append("Omen: Bosses: Midboss"); role_set.append(k)
    m['content'] = tags

# ---- Dynamis-Bastok ------------------------------------------------------------------
ZONE = "Dynamis-Bastok"
TAG, BOSS_TAG, TE_TAG = f"Dynamis: {ZONE}", f"Dynamis: {ZONE}: Boss", f"Dynamis: {ZONE}: TE"
BOSS, TE = "arch gu'dha effigy", "adamantking effigy"
PAGE = ["gi'pha manameister", "gu'nhi noondozer", "ko'dho cannonball", "ze'vho fallsplitter",
        "gu'dha effigy", "zo'pha forgesoul", "ra'gho darkfount", "va'zhe pummelsong",
        "bu'bho truesteel", "arch gu'dha effigy", "adamantking effigy", "adamantking image",
        "ra'gho's avatar", "vanguard beasttender", "vanguard constable", "vanguard defender",
        "vanguard drakekeeper", "vanguard hatamoto", "vanguard kusa", "vanguard mason",
        "vanguard militant", "vanguard minstrel", "vanguard protector", "vanguard purloiner",
        "vanguard thaumaturge", "vanguard undertaker", "vanguard vigilante", "vanguard vindicator",
        "vanguard's avatar", "vanguard's scorpion", "vanguard's wyvern"]

zoned = []
for k in PAGE:
    m = mobs[k]
    zs = m.setdefault('zones', [])
    if not any((e[0] if isinstance(e, list) else e) == ZONE for e in zs):
        zs.append([ZONE]); zoned.append(k)
    want = BOSS_TAG if k == BOSS else TE_TAG if k == TE else TAG
    tags = [t for t in (m.get('content') or []) if t != TAG or want == TAG]
    if want not in tags: tags.append(want)
    m['content'] = tags

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print(f"Caturae lv set to [139,139]: {', '.join(lv_set) or '(all already)'}")
print(f"Caturae given the Midboss role: {', '.join(role_set)}")
print(f"Dynamis-Bastok zone added (level-less) to {len(zoned)}: {', '.join(zoned)}")
print("boss:", mobs[BOSS]['content'], "| TE:", mobs[TE]['content'])
