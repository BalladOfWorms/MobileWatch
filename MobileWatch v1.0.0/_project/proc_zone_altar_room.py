#!/usr/bin/env python3
"""
REFINING PHASE — zone pass: Altar Room (rev 268). Engine = zonepass.py
MOBS ONLY — no zoneinfo_edit.

The smallest page of the sweep: 7 NMs, NO Adversaries table at all (zoneinfo's
`mobs[]` is [] and that is correct, not a gap — the room is the *A Moral Manifest?*
quest arena inside Castle Oztroja). Six of the seven publish no level.

**ALL SEVEN WERE MISSING THE ZONE**, which is what a one-room zone looks like when
nothing has ever passed over it: five records had ZERO zones, `yagudo avatar` had
only its Castle Oztroja timed-pop entry, and `duu masa the onecut` had only
`Castle Oztroja [S]` 83.
"""
from zonepass import run, wants_write, SKIP

ZONE = "Altar Room"
SLUG = "altar_room"

ROWS = [
    ("duu masa the onecut",     SKIP, "NM  Quest(A Moral Manifest?), SAM (G-8) — Lv BLANK; only Castle Oztroja [S] 83 before"),
    ("fee jugu the ramfist",    SKIP, "NM  Quest(A Moral Manifest?), MNK (G-8) — Lv BLANK, 0 zones before"),
    ("goo pake the bloodhound", SKIP, "NM  Quest(A Moral Manifest?), NIN (G-8) — Lv BLANK, 0 zones before"),
    ("kee taw the nightingale", SKIP, "NM  Quest(A Moral Manifest?), BRD (G-8) — Lv BLANK, 0 zones before"),
    ("laa yaku the austere",    SKIP, "NM  Quest(A Moral Manifest?), WHM (G-8) — Lv BLANK, 0 zones before"),
    ("poo yozo the babbler",    SKIP, "NM  Quest(A Moral Manifest?), BLM (G-8) — Lv BLANK, 0 zones before"),
    ("yagudo avatar",           "75", "NM  Quest(A Moral Manifest?), SMN (G-8) — 2nd zone; Castle Oztroja 75 kept"),
]

run(ZONE, SLUG, ROWS, write=wants_write())
