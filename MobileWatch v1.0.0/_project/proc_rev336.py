#!/usr/bin/env python3
"""
MobileWatch mobs.json - rev 336
Author: BalladOfWorms

Other > Unknown section 2, batch 2 - six more mob pages, six more families.

  edifier              -> Chariot      (page says "Chariots"; ours is singular)
  faytrapper vashgash  -> Orc
  flammeri             -> Flan
  fleshrending obdella -> Leech
  gharial              -> Wivre        (page "Wivres")
  grand'goule          -> Gargouille   (page "Gargouilles")

Un-numbered "Weak against / Resistant to" text is stored as [type, null] - a direction with
no magnitude, which is exactly what the card's bare Weak / Res rendering is for.

FLAGGED, NOT STAMPED: `edifier` sits in a SIX-RECORD BLOCK - `custodian`, `immobilizer`,
`oppressor`, `overseer`, `scrutinizer` all carry the identical shape (lv [85,87], the same
three Abyssea zones, no family) and all six are Bastion siege machines.  Only Edifier's page
was supplied, so only Edifier was stamped.  The other five are one word away.
"""
import json, os, sys

ASSETS = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
PATH = os.path.join(ASSETS, 'mobs.json')

W = lambda *els: [[e, None] for e in els]

STAMP = {
    'edifier': dict(fam='Chariot', im=['Sleep'],
                    notes=['Spawns during Bastion.',
                           'Only aggressive to players holding Pennant status.']),
    'faytrapper vashgash': dict(fam='Orc', job='Warrior', crys='Fire', wk=W('Water'),
                                notes=['Spawned for the quest Succor to the Sidhe, alongside four Faygorger Sheep and two Faygorger Rams.',
                                       'Uses Mighty Strikes at 25% HP, which sets every sheep and ram using it as well.']),
    'flammeri': dict(fam='Flan', job='Black Mage', crys='Water',
                     ab=['Amorphic Spikes'],
                     notes=['Timed pop around (C-7)/(H-7) on Halvung map 1.',
                            'Casts no magic at all and uses Amorphic Spikes exclusively.',
                            'High accuracy and strong Endarkness; high evasion and defence.']),
    'fleshrending obdella': dict(fam='Leech'),
    'gharial': dict(fam='Wivre', crys='Earth', wk=W('Wind', 'Ice'), st=W('Earth'),
                    notes=['Spawns at the bottom of (E-8) about two hours after death.',
                           'Stun, Blind, Paralyze and Slow all land; resistant or immune to Gravity and Bind.',
                           'Roughly 12% added movement speed and a very high Double Attack rate.']),
    "grand'goule": dict(fam='Gargouille', crys='Dark', wk=W('Dark'),
                        notes=['Lottery spawn from the Gargouille at (F-9).',
                               'Melee attacks carry an additional effect of Petrify.',
                               'Resists Gravity, Bind, Sleep and Requiem, and never leaves the ground.']),
}

# the block Edifier belongs to - identical lv, identical zones, no family
BASTION_BLOCK = ['custodian', 'immobilizer', 'oppressor', 'overseer', 'scrutinizer']


def main():
    with open(PATH, encoding='utf-8') as fh:
        data = json.load(fh)
    mobs = data['mobs']
    fams = {v['fam'] for v in mobs.values() if v.get('fam')}
    done, notes_only = [], []

    for k, fields in STAMP.items():
        mob = mobs[k]
        assert not mob.get('fam'), f'{k} already has a family'
        assert fields['fam'] in fams, f'{fields["fam"]} is not an existing family'
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
                notes_only.append((k, f, mob.get(f), v))
        done.append((k, fields['fam'], fields.get('job'), fields.get('crys')))

    assert not [k for m in mobs.values() for k, v in m.items() if v is None], 'null poison'
    for k, mb in mobs.items():
        for z in mb.get('zones') or []:
            if isinstance(z, list):
                assert 1 <= len(z) <= 2 and isinstance(z[0], str), (k, z)
                assert len(z) == 1 or isinstance(z[1], str), (k, z)

    with open(PATH, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, separators=(', ', ': '), ensure_ascii=False)

    print(f'== stamped ({len(done)})')
    for r in done:
        print('   ', r)
    if notes_only:
        print('== existing value KEPT, page value not written:')
        for r in notes_only:
            print('   ', r)
    print('== FLAGGED, not stamped - the Bastion Chariot block:')
    for k in BASTION_BLOCK:
        v = mobs[k]
        print(f'    {k:14s} lv={v.get("lv")} zones={[z[0] for z in v["zones"]]}')
    print('== orphans now', sum(1 for v in mobs.values() if not v.get('fam')))


if __name__ == '__main__':
    main()
