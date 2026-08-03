#!/usr/bin/env python3
"""
REV 410 — `Mountain Peiste` is aggressive (user-reported), in BOTH datasets.

Two files, because the two datasets are independent copies:
  1. mobs.json           `agg: true` on the mob record
  2. InfoBar database.db `is_aggressive = 1` on its one row

CORROBORATION: it was the ONLY passive Peiste in either dataset. InfoBar has
11 Peiste-family rows and 10 of them are already is_aggressive=1, including
`Outlands Peiste` which shares Morimar Basalt Fields with it. mobs.json tells
the same story. A lone outlier inside an otherwise uniform family is what a
missed flag looks like.

KEY ORDER: `agg` is inserted in its canonical position rather than appended,
so the record reads like every other record and the diff stays legible.
"""
import json
import os
import sqlite3
import shutil

import jsonfmt

BASE = 'app/src/main/assets'
if not os.path.isdir(BASE):
    BASE = 'android/' + BASE
P = os.path.join(BASE, 'mobs.json')

# The canonical field order, taken from the records that carry every field.
ORDER = ['n', 'fam', 'lv', 'agg', 'lnk', 'nm', 'det', 'job', 'resp', 'spawn',
         'wk', 'st', 'im', 'crys', 'ab', 'drops', 'zones', 'content', 'img',
         'notes', 'nmlv']

d = json.load(open(P, encoding='utf-8'))
mobs = d['mobs']

KEY = 'mountain peiste'
rec = mobs[KEY]
print('=== REV 410 — Mountain Peiste is aggressive ===')
print('  before: agg=%r  lnk=%r  fam=%s  lv=%s  zones=%s'
      % (rec.get('agg'), rec.get('lnk'), rec['fam'], rec['lv'],
         [z[0] for z in rec.get('zones', [])]))

rec['agg'] = True
mobs[KEY] = {k: rec[k] for k in ORDER if k in rec} | \
            {k: v for k, v in rec.items() if k not in ORDER}
print('  after : agg=%r' % mobs[KEY].get('agg'))
print('  key order: %s' % ', '.join(mobs[KEY]))

# --- corroboration: how the rest of the family reads -------------------------
fam = [(k, v) for k, v in mobs.items() if v.get('fam') == 'Peiste']
passive = [k for k, v in fam if not v.get('agg')]
print('\n  Peiste family in mobs.json: %d mobs, %d aggressive, %d passive'
      % (len(fam), sum(1 for _, v in fam if v.get('agg')), len(passive)))
print('  still passive after this fix: %s' % (', '.join(passive) or 'none'))

# --- guards ------------------------------------------------------------------
assert rec.get('lnk') is None or isinstance(rec['lnk'], bool)
assert not [k for m in mobs.values() for k, v in m.items() if v is None], 'NULL POISON'
assert not [k for a in d['abilities'].values() for k, v in a.items() if v is None]
assert len(mobs) == 6810 and len(d['abilities']) == 1591
before = json.load(open(P, encoding='utf-8'))
changed = [k for k in mobs if mobs[k] != before['mobs'].get(k)]
assert changed == [KEY], 'unexpected records changed: %s' % changed
print('\n  records changed in mobs.json: %d (%s)' % (len(changed), changed[0]))

jsonfmt.dump(d, P)

# --- the InfoBar sqlite db ---------------------------------------------------
DB = 'InfoBar-database.db'
SRC = '/mnt/user-data/uploads/database.db'
if os.path.exists(SRC):
    # Work on a copy in a writable scratch dir. sqlite needs to create a
    # journal file NEXT TO the database, so editing in place under a mounted
    # output dir can fail with "attempt to write a readonly database" even when
    # the file itself looks writable. Copy the finished db out at the end.
    work = '/home/claude/' + DB
    shutil.copy(SRC, work)
    os.chmod(work, 0o644)
    con = sqlite3.connect(work)
    cur = con.cursor()
    rows = list(cur.execute(
        'SELECT id, name, zone, is_aggressive FROM monster WHERE name = ?',
        ('Mountain Peiste',)))
    print('\n=== InfoBar database.db ===')
    print('  matching rows: %d  %s' % (len(rows), rows))
    cur.execute('UPDATE monster SET is_aggressive = 1 WHERE name = ?',
                ('Mountain Peiste',))
    print('  rows updated: %d' % cur.rowcount)
    con.commit()
    after = list(cur.execute(
        'SELECT id, name, zone, is_aggressive FROM monster WHERE name = ?',
        ('Mountain Peiste',)))
    print('  after: %s' % after)
    assert all(r[3] == 1 for r in after)
    # the family, for context
    print('  Peiste rows now passive: %s'
          % (list(cur.execute("SELECT name, zone FROM monster "
                              "WHERE family = 'Peiste' AND is_aggressive = 0")) or 'none'))
    # untouched-elsewhere check
    n = cur.execute('SELECT COUNT(*) FROM monster').fetchone()[0]
    print('  monster rows total: %d (unchanged)' % n)
    con.close()
    out = os.path.join('/mnt/user-data/outputs', DB)
    shutil.copy(work, out)
    print('  written: %s (%d bytes)' % (out, os.path.getsize(out)))
else:
    print('\n(no database.db uploaded — skipping the InfoBar half)')
