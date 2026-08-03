#!/usr/bin/env python3
"""
rev 171 step 1 — REVERT the remaining info-box-derived zoneinfo writes.

USER: "continue reverting then, some info we had was wrong so we over rode those.
just mobs though going forward."

So the pre-existing overrides (the 91 `weather: "None"` entries, etc.) are deliberate
corrections to bad base data — mine were not, they were harvested from a screenshot
sent for orientation. rev 170 restored the 16 `weather` fields; this removes the
other info-box harvest: **15 `notes` lines across 10 zones**, every one lifted from a
footnote or bullet in a zone info box.

KEPT — mob data, which is the remit:
  * the Bloodsucker (NM)/(Monster) row renames across 5 zones (rev 155, fixed the
    reported "clicking either goes to the NM page" bug)
  * `Be'Hya Hundredwall` lv 80 -> 30 in Palborough (rev 152, the user's own ruling)
  * Bostaunieux `mobs[]` += the missing Bloodsucker row
  * two `nms[].drops` fills read off NM tables (Garbage Gel, Hugemaw Harold)

Restores `notes` from the ORIGINAL uploaded zip, so any note that was already there
stays exactly as it was.
"""
import json, os, sys

NEW = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', 'app', 'src', 'main', 'assets', 'zoneinfo.json')
ORIG = '/tmp/orig/android/app/src/main/assets/zoneinfo.json'

o = json.load(open(ORIG, encoding='utf-8'))
n = json.load(open(NEW, encoding='utf-8'))

removed, kept_zones = [], 0
for k in o:
    was, now = o[k].get('notes'), n[k].get('notes')
    if was == now:
        continue
    for line in (now or []):
        if line not in (was or []):
            removed.append((k, line))
    if was is None:
        n[k].pop('notes', None)          # the key did not exist before — take it away
    else:
        n[k]['notes'] = was
        kept_zones += 1

print(f"REMOVED {len(removed)} note lines across "
      f"{len({k for k, _ in removed})} zones:\n")
for k, line in removed:
    print(f"   {k:26s} {line[:88]}")

left = [k for k in o if o[k].get('notes') != n[k].get('notes')]
assert not left, left

print("\nzoneinfo now differs from the original ONLY in mob data:")
for k in sorted(o):
    for f in set(o[k]) | set(n[k]):
        if o[k].get(f) != n[k].get(f):
            print(f"   {k:26s} [{f}]")

if '--write' in sys.argv:
    json.dump(n, open(NEW, 'w', encoding='utf-8'), ensure_ascii=False)
    print("\nWRITTEN.")
else:
    print("\n(dry run — pass --write)")
