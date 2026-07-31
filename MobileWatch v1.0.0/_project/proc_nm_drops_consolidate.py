#!/usr/bin/env python3
"""
rev 157 step 3 — NM DROPS CONSOLIDATED ONTO ONE ENTRY.

USER: "nm across multiple zones, 1 entry listing valuable drops and zone section
lists all zones"

So a Notorious Monster stays ONE record no matter how many zones (or how many
page rows) it appears in; that record lists the valuable drops, and `zones`
carries every zone. This CLOSES (ly) as "do not split" — the four conflated
original/[S] NM records stay single and get their drops merged instead.

Two groups:
  A) King Ranperre's Tomb NMs whose stored `drops` held only part of what the
     page's Drops column publishes — including HAHAVA, which the page lists in
     TWO rows (a short Voidwatch row and a fuller one).
  B) The four (ly) records, merged from the two zoneinfo `nms[]` halves that
     already hold each era's drops separately.

RULES OBSERVED
  * every written name is verified present in ffxi_items.json (rule 41). One new
    abbreviation-ledger entry: wiki "Cashmere Thread" -> DB `Cashmere Thrd.`,
    found only by sweeping "cashmere".
  * KEY ITEMS STAY OUT of `drops` (the KI/container convention): `Ranperre Chest
    Key`, `Empyrean Head Seals`, `Atmacite of Eminence` have no DB entry and are
    not written. Nor are the prose rows ("Level 76-90 spell scrolls", "Various
    crafting materials").
  * A **Steal** is not a drop: Spook's `Cotton Cloth` is left out.
  * ADDITIVE ONLY — existing names are kept and the merge is a union, never a
    replacement (rule 1).
"""
import json, os, sys

A = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '..', 'app', 'src', 'main', 'assets')
P = lambda f: os.path.join(A, f)

# key -> the full valuable-drop list for the single consolidated entry
CONSOLIDATE = {
    # --- A: this zone's page ---------------------------------------------
    "cemetery cherry": ["Divine Log", "Living Rod", "Petrified Log", "Rosewood Log"],
    "vrtra": ["Cashmere Thrd.", "Cashmere Wool", "Damascene Cloth", "Dragon Blood",
              "Dragon Meat", "Dragon Scales", "Reviler's Helm", "Wyrm Horn"],
    "hahava": ["Mextli Harness", "Ganesha's Mask", "Ganesha's Mala", "Hahava's Mail",
               "Silver Mirror", "Riftsand", "Crystal Petrifact"],
    # --- B: the four (ly) conflated original/[S] NMs ----------------------
    "zhuu buxu the silent": ["Parana Shield", "Sangoma Lappa"],
    "ashmaker gotblut": ["Hermit's Wand", "Priest's Robe", "Marabout Sandals"],
    "hawkeyed dnatbat": ["Archer's Knife", "Assassin's Bow", "Grand Crossbow"],
    "da'dha hundredmask": ["Mithran Scimitar", "Parrying Knife", "Patrician's Cuffs"],
}

m = json.load(open(P('mobs.json'), encoding='utf-8'))
mobs = m['mobs']
items = {v['n'] for v in json.load(open(P('ffxi_items.json'), encoding='utf-8')).values() if 'n' in v}

bad = {k: [n for n in v if n not in items] for k, v in CONSOLIDATE.items()}
bad = {k: v for k, v in bad.items() if v}
if bad:
    sys.exit(f"ABORT (rule 41): names not in ffxi_items.json -> {bad}")

changed = []
for k, names in CONSOLIDATE.items():
    rec = mobs[k]
    old = rec.get('drops', '') or ''
    have = [p.strip() for p in old.split(',') if p.strip()]
    # union, additive: keep everything already stored, append what is new, in page order
    merged = have + [n for n in names if n not in have]
    new = ', '.join(merged)
    if new != old:
        rec['drops'] = new
        changed.append((k, old, new, len(merged) - len(have)))

print("NM DROPS CONSOLIDATED — one entry, valuable drops, all zones kept\n")
for k, old, new, added in changed:
    print(f"  {k}")
    print(f"     was  ({len(old.split(',')) if old else 0}): {old or '(none)'}")
    print(f"     now  ({len(new.split(','))}, +{added}): {new}")
    print(f"     zones ({len(mobs[k].get('zones', []))}): "
          f"{[e[0] if isinstance(e, list) else e for e in mobs[k].get('zones', [])]}")
    print()
print(f"{len(changed)} records changed; no record was split, no zone was removed.")

if '--write' in sys.argv:
    json.dump(m, open(P('mobs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print("WRITTEN.")
else:
    print("(dry run — pass --write)")
