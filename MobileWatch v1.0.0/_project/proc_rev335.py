#!/usr/bin/env python3
"""
MobileWatch mobs.json - rev 335
Author: BalladOfWorms

TWO JOBS from the Other > Unknown review:

1. SECTIONS 1a + 1b REMOVED.  USER: "completely remove 1a and 1b."
   22 `No.N` / `No N` Lamiae pairs + 15 spelling variants = 37 orphan records deleted.
   **They are MERGED first, then deleted** - a bare delete would have thrown away the `lv`
   on almost every one of them plus spell lists, spawn strings, drops and `nmlv` that only
   the orphan side carries.  The record is gone either way; the data is not.
   Survivor = the familied record.  Fold in every field it lacks, union zones/lv/notes.
   GUARD: a placeholder `lv` (low = 1, span > 20) is NOT unioned - `qiqirn mine`'s [1,75]
   would otherwise have destroyed `qiqirn miner`'s measured [68,68].

2. SECTION 2 STARTED - 13 mob pages, 13 families.
   The zoned orphans get their real family, job, crystal and resist direction from their own
   BG page.  Un-numbered "Weak to / Strong against" text is stored as [type, null], which
   renders as a bare green Weak / red Res - never a guessed magnitude.
   `ancestral rage` is HELD BACK: its page names family **Byrgena**, which does not exist in
   our 201 families.  Creating one needs a `family_eco` entry too (the Flan bug) - user's call.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

LAMIAE = ['lamia no.11', 'lamia no.13', 'lamia no.14', 'lamia no.15', 'lamia no.17',
          'lamia no.18', 'lamia no.19', 'lamia no.2', 'lamia no.21', 'lamia no.24',
          'lamia no.27', 'lamia no.3', 'lamia no.34', 'lamia no.4', 'lamia no.9',
          'lamie no.7', 'lamie no.8', 'lamie no.9', 'merrow no.11', 'merrow no.12',
          'merrow no.16', 'merrow no.5']

SPELLING = [('bathybic kulshedra', 'bathybic kulushedra'),
            ('eschan sorcerer', 'eschan sorceror'),
            ('exoplates', 'exoplate'),
            ('gargoyle-iota', 'gargoyle iota'),
            ('gargoyle-kappa', 'gargoyle kappa'),
            ('gargoyle-lambda', 'gargoyle lambda'),
            ('gargoyle-mu', 'gargoyle mu'),
            ('gii jaha the raucous', 'gii jaha the racous'),
            ('gosspix blabberlips', 'gosspix blabblerlips'),
            ('kulshedra', 'kulushedra'),
            ('qiqirn mine', 'qiqirn miner'),
            ('surmerdar the unbridled', 'surmerder the unbridled'),
            ('vermilion-eared noberry', 'vermillion-eared noberry'),
            ('vyurvarjur the nimble', 'vyuvarjur the nimble'),
            ("zo'dhu legslicer", "zo'dha legslicer")]

W = lambda *els: [[e, None] for e in els]

# key -> fields taken from that mob's own BG page
STAMP = {
    'bergschrund gefyrst': dict(fam='Elemental', crys=None,
                                notes=['Spawns during icy weather; despawns if left passive once the weather fades.']),
    'big bang': dict(fam='Djinn', crys='Fire', wk=W('Fire'),
                     st=W('Ice', 'Wind', 'Earth', 'Lightning', 'Water', 'Light', 'Dark')),
    'boll weevil': dict(fam='Beetle', job='Warrior', crys='Earth', wk=W('Ice', 'Light')),
    'burgeoning flames': dict(fam='Elemental', job='Black Mage / Red Mage',
                              wk=W('Water'), st=W('Fire', 'Ice')),
    'burlibix brawnback': dict(fam='Goblin', job='Warrior', crys='Fire', wk=W('Light')),
    'chelicerata': dict(fam='Chigoe', job='Thief', crys='Earth'),
    'croque-mitaine': dict(fam='Goobbue', job='Thief', crys='Water', wk=W('Fire', 'Lightning')),
    'demoiselle desolee': dict(fam='Fly', job='Warrior', crys='Wind', wk=W('Ice')),
    'deserter draugar': dict(fam='Skeleton', crys='Dark'),
    'dreadhound': dict(fam='Hound', crys='Dark'),
    'drowned bones': dict(fam='Skeleton', job='Black Mage', crys='Earth'),
    'drumskull zogdregg': dict(fam='Orc', job='Black Mage', crys='Fire', wk=W('Water')),
}

# zone work the same pages published: (key, zone, level) - fill or correct
ZONE_SET = [('bergschrund gefyrst', 'Woh Gates', '126-127'),      # stored 126
            ('boll weevil', 'Jugner Forest [S]', '56-57'),        # empty
            ('burlibix brawnback', 'Batallia Downs [S]', '~75'),  # empty
            ('deserter draugar', 'Outer RaKaznar', '118-121'),    # ADD - page zone we lacked
            ('dreadhound', 'Outer RaKaznar', '113-116'),          # stored 114-116
            ('drumskull zogdregg', 'Jugner Forest [S]', '78-80')] # empty

HELD = {'ancestral rage': 'page family "Byrgena" does not exist in our 201 families'}


def band(s):
    s = s.lstrip('~').rstrip('+')
    if not s or not s[0].isdigit():
        return None
    lo, _, hi = s.partition('-')
    try:
        return int(lo), int(hi or lo)
    except ValueError:
        return None


def placeholder(lv):
    return isinstance(lv, list) and len(lv) == 2 and lv[0] == 1 and lv[1] - lv[0] > 20


def union_zones(a, b):
    out = list(a or [])
    idx = {(z[0] if isinstance(z, list) else z): i for i, z in enumerate(out)}
    for z in (b or []):
        k = z[0] if isinstance(z, list) else z
        if k not in idx:
            out.append(z); idx[k] = len(out) - 1
        else:
            cur = out[idx[k]]
            if isinstance(z, list) and len(z) == 2 and not (isinstance(cur, list) and len(cur) == 2):
                out[idx[k]] = z
    return out


def merge_then_delete(mobs, orphan, survivor, log):
    o, s = mobs[orphan], mobs[survivor]
    folded, skipped = [], []
    for f, v in o.items():
        if f in ('n', 'zones', 'lv', 'notes'):
            continue
        if f not in s:
            s[f] = v; folded.append(f)
    z = union_zones(s.get('zones'), o.get('zones'))
    if z:
        s['zones'] = z
    olv, slv = o.get('lv'), s.get('lv')
    if isinstance(olv, list) and placeholder(olv) and isinstance(slv, list):
        skipped.append(f'lv {olv} (placeholder)')
    else:
        lv = [x for x in (slv, olv) if isinstance(x, list) and len(x) == 2]
        if lv:
            s['lv'] = [min(x[0] for x in lv), max(x[1] for x in lv)]
    notes = list(s.get('notes') or [])
    for nt in (o.get('notes') or []):
        if nt not in notes:
            notes.append(nt)
    if notes:
        s['notes'] = notes
    del mobs[orphan]
    log.append((orphan, survivor, folded, skipped, s.get('lv')))


def main():
    with open(PATH, encoding='utf-8') as fh:
        data = json.load(fh)
    mobs = data['mobs']
    before = len(mobs)
    lam_log, sp_log, stamped, zoned = [], [], [], []

    for k in LAMIAE:
        merge_then_delete(mobs, k, k.replace('no.', 'no '), lam_log)
    for a, b in SPELLING:
        merge_then_delete(mobs, a, b, sp_log)

    for k, fields in STAMP.items():
        mob = mobs[k]
        assert not mob.get('fam'), f'{k} already has a family'
        for f, v in fields.items():
            if v is None:
                continue                       # page said "Crystal: None" - store nothing
            if f == 'notes':
                mob['notes'] = list(mob.get('notes') or []) + [x for x in v
                                                               if x not in (mob.get('notes') or [])]
            else:
                mob[f] = v
        stamped.append((k, fields.get('fam'), fields.get('job'), fields.get('crys')))

    for k, zone, lvl in ZONE_SET:
        mob = mobs[k]
        zs = mob.setdefault('zones', [])
        ent = next((z for z in zs if isinstance(z, list) and z[0] == zone), None)
        if ent is None:
            zs.append([zone, lvl]); zoned.append((k, zone, 'ADD', lvl))
        elif len(ent) == 1:
            ent.append(lvl); zoned.append((k, zone, 'FILL', lvl))
        elif ent[1] != lvl:
            zoned.append((k, zone, f'CORRECT {ent[1]} ->', lvl)); ent[1] = lvl
        b = band(lvl); cur = mob.get('lv')
        if b and isinstance(cur, list) and len(cur) == 2:
            new = [min(cur[0], b[0]), max(cur[1], b[1])]
            if new != cur:
                zoned.append((k, 'lv union', cur, new)); mob['lv'] = new

    assert not [k for k in mobs if k in LAMIAE], 'a Lamiae orphan survived'
    assert not [k for k, _ in SPELLING if k in mobs], 'a spelling orphan survived'
    assert not [k for m in mobs.values() for k, v in m.items() if v is None], 'null poison'
    for k, mb in mobs.items():
        for z in mb.get('zones') or []:
            if isinstance(z, list):
                assert 1 <= len(z) <= 2 and isinstance(z[0], str), (k, z)
                assert len(z) == 1 or isinstance(z[1], str), (k, z)

    with open(PATH, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, separators=(', ', ': '), ensure_ascii=False)

    print(f'== 1a Lamiae merged+deleted ({len(lam_log)})')
    for o, s, f, sk, lv in lam_log:
        print(f'    {o:16s} -> {s:16s} folded={f} lv={lv} {sk}')
    print(f'== 1b spelling merged+deleted ({len(sp_log)})')
    for o, s, f, sk, lv in sp_log:
        print(f'    {o:26s} -> {s:26s} folded={f} lv={lv} {sk}')
    print(f'== families stamped ({len(stamped)})')
    for r in stamped:
        print('   ', r)
    print(f'== zone fills/corrections ({len(zoned)})')
    for r in zoned:
        print('   ', r)
    print(f'== HELD: {HELD}')
    print(f'== mobs {before} -> {len(mobs)}')


if __name__ == '__main__':
    main()
