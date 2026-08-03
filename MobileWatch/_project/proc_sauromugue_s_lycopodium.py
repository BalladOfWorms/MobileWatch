#!/usr/bin/env python3
"""
rev 273 — RULE 99, SECOND INSTANCE. The bucket-E check returned four rows and one is
a dropped ` [S]` suffix:

    lycopodium (monster)   bare `Sauromugue Champaign` 28-31

Every other zone on that record is an [S] zone — Fort Karugo-Narugo [S] 22-25,
Batallia Downs [S] 28-31, Rolanberry Fields [S] 28-31, Meriphataud Mountains [S]
31-34 — and `sauromugue_champaign_s.mobs[]` lists **Lycopodium at exactly 28-31**,
while the present-day page's 37-row adversary list has no Lycopodium at all.
Same three proofs as the rev-264 Eldieme goblins.

Retarget only; the level string is unchanged and no zone is removed.
"""
import json, os, sys
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'src', 'main', 'assets', 'mobs.json')
d = json.load(open(A, encoding='utf-8'))
zs = d['mobs']['lycopodium (monster)']['zones']
OLD, NEW = "Sauromugue Champaign", "Sauromugue Champaign [S]"
assert not any((e[0] if isinstance(e, list) else e) == NEW for e in zs), "already has [S]"
for e in zs:
    if (e[0] if isinstance(e, list) else e) == OLD:
        e[0] = NEW
print('  lycopodium (monster) ->', zs)
if '--write' in sys.argv:
    json.dump(d, open(A, 'w', encoding='utf-8'), ensure_ascii=False)
    print("WRITTEN.")
else:
    print("(dry run)")
