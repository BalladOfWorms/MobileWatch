#!/usr/bin/env python3
"""
rev 164 — (ml) CLOSED. USER: "both star mobs are beetle."

`starmite` was already `fam="Beetle"`; `starborer` was `fam="Wamouracampa"`.
Both sit on the Toraimarai Canal page as adjacent Adversaries rows with Genus
**Beetle**, which is what rev 163 flagged under rule 5. The user settles it.

ONE FIELD CHANGES: starborer.fam Wamouracampa -> Beetle.

WHY NOTHING ELSE MOVES (the rev-138 / (ky) precedent):
  * `family_eco` maps BOTH families to **Vermin**, so the browser heading the mob
    renders under does not change — only its family sub-heading does.
  * `family_icons["Beetle"] = "Beetle.jpg"` already exists and starborer carries
    no per-mob `img`, so it falls back to the Beetle icon automatically (rule 37).
    No icon key is needed (rule 24 satisfied).
  * `Wamouracampa` keeps 14 members, so no family empties and the inert
    `families` list needs no edit.
  * **The record still carries the WAMOURACAMPA family stamp** — ab (Amber Scutum,
    Cannonball, Heat Barrier, Thermal Pulse, Vitriolic Spray/Shower), det ["Sound"],
    the -12.5% physical `st` set, wk Wind/Light +15% Ice/Water +30%, resp 330 —
    against Beetle sibling `starmite`'s ab (Power Attack, Rhino Attack, Spoil,
    Rhino Guard, Hi-Freq Field), det ["Sight","Scent"], wk Light/Ice +50%.
    **Re-stamping is a family-pass action, not a zone-pass one** (the rev-138
    albumen's precedent: fam moved, no crys/job/det/kit stamp applied), and the
    page publishes none of those fields. Left alone and flagged.
"""
import json, os, sys

A = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '..', 'app', 'src', 'main', 'assets')
P = lambda f: os.path.join(A, f)
KEY, OLD, NEW = 'starborer', 'Wamouracampa', 'Beetle'

m = json.load(open(P('mobs.json'), encoding='utf-8'))
mobs = m['mobs']
rec = mobs[KEY]

if rec.get('fam') != OLD:
    sys.exit(f"ABORT: {KEY}.fam is {rec.get('fam')!r}, expected {OLD!r}.")
if NEW not in m['family_icons']:
    sys.exit(f"ABORT (rule 24): no family_icons entry for {NEW!r}.")

before = {f: len([k for k, v in mobs.items() if v.get('fam') == f]) for f in (OLD, NEW)}
rec['fam'] = NEW
after = {f: len([k for k, v in mobs.items() if v.get('fam') == f]) for f in (OLD, NEW)}

print(f"{KEY}.fam  {OLD!r} -> {NEW!r}")
print(f"  members  {OLD}: {before[OLD]} -> {after[OLD]}   {NEW}: {before[NEW]} -> {after[NEW]}")
print(f"  eco      {OLD}={m['family_eco'].get(OLD)!r}  {NEW}={m['family_eco'].get(NEW)!r}"
      f"   (unchanged heading: {m['family_eco'].get(OLD) == m['family_eco'].get(NEW)})")
print(f"  icon     resolves to mobicons/{m['family_icons'][NEW]} via fallback "
      f"(record has per-mob img: {'img' in rec})")
print(f"  families(fam) in use unchanged: {OLD} still has {after[OLD]} members")

print("\nSTILL CARRYING THE WAMOURACAMPA STAMP (flagged, NOT changed):")
sm = mobs['starmite']
for f in ('ab', 'det', 'wk', 'st', 'resp'):
    print(f"  {f:5s} starborer={str(rec.get(f))[:78]}")
    print(f"  {'':5s} starmite ={str(sm.get(f))[:78]}")

assert rec['fam'] == NEW and after[OLD] == before[OLD] - 1 and after[NEW] == before[NEW] + 1

if '--write' in sys.argv:
    json.dump(m, open(P('mobs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print("\nWRITTEN.")
else:
    print("\n(dry run — pass --write)")
