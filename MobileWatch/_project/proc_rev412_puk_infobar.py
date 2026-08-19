#!/usr/bin/env python3
"""rev 412 — push the Puk grid correction into InfoBar's database.db.

Same finding as proc_rev412_puk.py: the BG-wiki element row is
Fire / Wind / Lightning / Light / Ice / Earth / Water / Dark, so the +30% cell
belongs to ICE, not Lightning (InfoBar spells Lightning as "Thunder").
InfoBar has no absorb column, so the Wind absorb cannot be represented here —
only the weakness string changes.  Abilities are not on the bar at all, so the
kit stamp does not reach this file.

Idempotent: re-running is a no-op (the rev-409 lesson — every transform in an
InfoBar script must survive a second run).

Usage: proc_rev412_puk_infobar.py <database.db>   (edit a WRITABLE copy —
sqlite needs to create its journal beside the file)

Author: BalladOfWorms
"""
import sqlite3, sys

DB = sys.argv[1]
OLD, NEW = '(Thunder +30)', '(Ice +30)'

c = sqlite3.connect(DB)
rows = c.execute("SELECT id, weaknesses FROM monster WHERE family = 'Puk'").fetchall()
assert len(rows) == 32, len(rows)

changed = 0
for rid, wk in rows:
    if not wk or OLD not in wk:
        continue                              # already converted, or the odd junk row
    c.execute("UPDATE monster SET weaknesses = ? WHERE id = ?", (wk.replace(OLD, NEW), rid))
    changed += 1

# Amymone's Peapuk still carried the pre-rev-68 junk stamp in both datasets
cur = c.execute("UPDATE monster SET weaknesses = ? WHERE family = 'Puk' AND weaknesses = ?",
                ('(Ice +30)(Fire/Earth/Water/Light/Dark +15)(Pier/Rngd +12.5)', '(Pier +25)(Ice +12.5)'))
changed += cur.rowcount
c.commit()

left = c.execute("SELECT COUNT(*) FROM monster WHERE family = 'Puk' AND weaknesses LIKE ?",
                 ('%Thunder%',)).fetchone()[0]
assert left == 0, left
print(f"rows changed {changed}; Puk rows still naming Thunder: {left}")
print(c.execute("SELECT COUNT(*) FROM monster").fetchone()[0], "rows total")
c.close()
