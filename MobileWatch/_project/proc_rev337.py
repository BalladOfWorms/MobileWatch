#!/usr/bin/env python3
"""
MobileWatch mobs.json - rev 337
Author: BalladOfWorms

USER RULING: "ancestral rage is byrgen (elemental) family."

The file backs it: `byrgen`, `phlegmatic byrgen`, `stolid byrgen` and `unrepentant byrgen`
are all already `fam: Elemental`, so the Byrgen line lives inside the Elemental family and
`ancestral rage` joins it.  `gullin byrgen` is stamped with it - same name, same family, and
it carries the identical grid to `ancestral rage` (Light +25% / four physicals -75% / Dark
-25%), which is a different grid from the other four Byrgens.

Its measured `wk`/`st` are NOT touched (rule 280) - the page only shows icons and the record
already stores numbers.  `Entomb` and `Tenebral Crush` were both checked against the
abilities dict before writing: both defined, so this adds no undefined references.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

STAMP = {
    'ancestral rage': dict(
        fam='Elemental',
        job='Black Mage / Dark Knight / Red Mage',
        im=['Stun', 'Slow', 'Sleep', 'Silence'],
        ab=['Entomb', 'Tenebral Crush'],
        sp=['Stone V', 'Stone IV', 'Stonega III', 'Stoneja', 'Dread Spikes',
            'Sleepga II', 'Slowga', 'Drain', 'Aspir'],
        notes=["Spawned at (M-8/9) on the Overgrown Grave with a Lhaiso Neftereh's bell.",
               'Extremely high resistance to physical damage \u2014 Formless Strikes does not work on it.',
               'Entomb is AoE Earth damage with Slow, Petrify and a hate reset; Tenebral Crush is AoE Darkness damage with Defense Down.',
               'Hate resets become excessive below roughly 35% HP. Square Enix have stated its enmity accumulation is glitched, which makes the fight harder than intended.'],
    ),
    'gullin byrgen': dict(fam='Elemental'),
}


def main():
    with open(PATH, encoding='utf-8') as fh:
        data = json.load(fh)
    mobs, abil = data['mobs'], data['abilities']
    done, kept = [], []

    for k, fields in STAMP.items():
        mob = mobs[k]
        assert not mob.get('fam'), f'{k} already has a family'
        for a in fields.get('ab', []):
            assert a in abil, f'{a} is not a defined ability - would add an undefined reference'
        for f, v in fields.items():
            if f == 'notes':
                cur = list(mob.get('notes') or [])
                for nt in v:
                    if nt not in cur:
                        cur.append(nt)
                mob['notes'] = cur
            elif f not in mob or not mob.get(f):
                mob[f] = v
            else:
                kept.append((k, f, mob.get(f)))
        done.append((k, fields['fam']))

    assert not [k for m in mobs.values() for k, v in m.items() if v is None], 'null poison'
    undef = [a for v in mobs.values() for a in (v.get('ab') or []) if a not in abil]
    print('undefined ability references file-wide:', len(undef))

    with open(PATH, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, separators=(', ', ': '), ensure_ascii=False)

    print('== stamped:', done)
    if kept:
        print('== existing values kept (page value not written):')
        for r in kept:
            print('   ', r)
    print('== the Byrgen line now reads:')
    for k in ['byrgen', 'gullin byrgen', 'phlegmatic byrgen', 'stolid byrgen',
              'unrepentant byrgen', 'ancestral rage']:
        print(f'    {k:22s} fam={mobs[k].get("fam")}')
    print('== orphans now', sum(1 for v in mobs.values() if not v.get('fam')))


if __name__ == '__main__':
    main()
