#!/usr/bin/env python3
"""
proc_eald_tenzen_ouryu.py — Rev 119: Eald'narche, Tenzen, Ouryu.

Two Celestial/Warrior's Path Humanoid battlefield NMs (Eald'narche, Tenzen) +
the Wyrm-family BCNM Ouryu. Enriches all three (jobs, NM, grids, kits, drops,
zones, notes, renders); creates 14 abilities; and fixes the file-wide
misspelled 'Orche Blast' -> 'Ochre Blast' across the whole Wyrm family.

Author: BalladOfWorms
"""
import json

P = 'app/src/main/assets/mobs.json'
d = json.load(open(P))
M = d['mobs']; A = d['abilities']
before_ab = len(A)

# ---------------------------------------------------------------- NEW abilities
NEW = {
 # Eald'narche (Form 1 physical / Form 2 magical)
 "Gaea Stream":   {"d":"Inflicts damage to a single target.","t":"Physical","tgt":"Single","notes":"Form 1. Absorbable by Utsusemi."},
 "Uranos Cascade":{"d":"Inflicts damage to enemies in an area of effect.","t":"Physical","tgt":"AoE","notes":"Form 1. Absorbable by Utsusemi."},
 "Cronos Sling":  {"d":"Inflicts damage to enemies in a cone.","t":"Physical","tgt":"Cone AoE","notes":"Form 1. Absorbable by Utsusemi."},
 "Vortex":        {"d":"Inflicts damage and resets hate to enemies in an area of effect.","t":"Magical","tgt":"AoE","fx":["Terror","Bind"],"r":"~15' radial","notes":"Form 2. Absorbable by Utsusemi."},
 "Stellar Burst": {"d":"Inflicts damage to enemies in an area of effect.","t":"Magical","tgt":"AoE","fx":["Silence","Slow"],"notes":"Form 2. Absorbable by Utsusemi."},
 "Omega Javelin": {"d":"Inflicts damage and petrification to a single target.","tgt":"Single","fx":["Petrification"],"notes":"Form 2."},
 # Tenzen (Amatsu series = great-katana Tachi variants; Oisoya = ranged)
 "Amatsu: Kazakiri":  {"d":"Tachi: Jinpu variant. Inflicts damage to a single target.","t":"Physical","tgt":"Single"},
 "Amatsu: Torima":    {"d":"Tachi: Enpi variant. A two-hit attack that inflicts damage to a single target.","t":"Physical","tgt":"Single"},
 "Amatsu: Yukiarashi":{"d":"Tachi: Yukikaze variant. Inflicts damage to a single target.","t":"Physical","tgt":"Single","fx":["Blind"]},
 "Amatsu: Tsukioboro":{"d":"Tachi: Gekko variant. Inflicts damage to a single target.","t":"Physical","tgt":"Single","fx":["Silence"]},
 "Amatsu: Hanaikusa": {"d":"Tachi: Kasha variant. Inflicts damage to a single target.","t":"Physical","tgt":"Single","fx":["Paralysis"]},
 "Amatsu: Kamikaeshi":{"d":"Inflicts damage to a single target.","t":"Physical","tgt":"Single"},
 "Amatsu: Tsukikage": {"d":"Inflicts damage to a single target and closes the Cosmic Elucidation skillchain.","t":"Physical","tgt":"Single"},
 "Oisoya":            {"d":"Namas Arrow variant. A ranged attack that inflicts high damage to a single target.","t":"Physical","tgt":"Single","notes":"Ranged attack. Ignores Utsusemi."},
}
created = 0
for n, v in NEW.items():
    if n not in A:
        A[n] = v; created += 1
    else:
        print('ALREADY EXISTS (skipped create):', n)

# ---------------------------------------------------------------- enrich existing defs
# Phase Shift: broaden beyond "only Exoplates" — Eald'narche uses it Form 1 at 66/33/1%
A['Phase Shift']['notes'] = ("Used by Eald'narche in his first form at 66%, 33%, and 1% HP, and by his "
                             "Exoplates as a 33%-HP reaction; damage escalates each use (~600-1300).")
# Yaegasumi: it's not Bumba-only — Tenzen uses it too
A['Yaegasumi']['notes'] = ("A Samurai one-hour ability the NM borrows; used by Tenzen and Bumba "
                           "(lasts 45 seconds for Bumba).")

# ---------------------------------------------------------------- Wyrm-family typo fix: Orche Blast -> Ochre Blast
# 'Orche Blast' (misspelled) is referenced by the whole Wyrm family; 'Ochre Blast' (correct) had 0 refs.
# Keep the more complete def under the correct key, repoint every ref, drop the typo key.
A['Ochre Blast'] = {"d":"An earth storm deals damage to enemies in a 30' area of effect. Ignores shadows.",
                    "t":"Magical","el":"Earth","r":"30' radial","tgt":"AoE","notes":"Used by earth wyrms while airborne."}
repointed = 0
for m in M.values():
    ab = m.get('ab')
    if ab and 'Orche Blast' in ab:
        m['ab'] = ['Ochre Blast' if a == 'Orche Blast' else a for a in ab]
        repointed += 1
assert not any('Orche Blast' in (m.get('ab') or []) for m in M.values()), 'Orche Blast still referenced'
del A['Orche Blast']
print('Orche Blast -> Ochre Blast: repointed', repointed, 'mobs; typo key removed')

# ---------------------------------------------------------------- helper
def upd(key, **kw):
    m = M[key]
    for k, v in kw.items():
        if v is None:
            m.pop(k, None)
        else:
            m[k] = v

R15 = [[e, "-15%"] for e in ["Fire","Wind","Lightning","Light","Ice","Earth","Water","Dark"]]

# ---------------------------------------------------------------- EALD'NARCHE (fam=Humanoid)
upd("eald'narche",
    job="Black Mage", nm=True,
    ab=["Gaea Stream","Uranos Cascade","Cronos Sling","Phase Shift","Vortex","Stellar Burst","Omega Javelin"],
    sp=["Flare","Freeze","Tornado","Quake","Burst","Flood","Flare II","Freeze II","Tornado II","Quake II","Burst II","Flood II","Sleepga II","Bindga"],
    st=R15, wk=[],
    drops="Vanir Knife, Vanir Gun, Vanir Cotehardie, Vanir Battery, Vanir Boots",
    zones=[["The Celestial Nexus"],["Empyreal Paradox"]],
    img="mobimages/eald'narche.png",
    notes=[
      "The Celestial Nexus II — fought in The Celestial Nexus with a Celestial Nexus phantom gem (all members need the key item). Also fought at Empyreal Paradox during Apocalypse Nigh.",
      "Has two forms. Susceptible to Stun, Violent Flourish, Paralyze, and Slow.",
      "First form: assisted by Exoplates and two Orbitals — the Exoplates must be defeated before Eald'narche can be damaged. Orbitals have high evasion and can be slept (Lullaby/Light Shot/Sleep) but gain resistance over time.",
      "First form: Phase Shift at 66%, 33%, and 1% HP does high damage — mages/DD without Utsusemi should stand beyond 30'. Casts tier-1 Ancient Magic, Sleepga II, and Bindga; has high evasion.",
      "Once the Exoplates die he stops summoning Orbitals and using TP moves, and begins spamming tier-1 Ancient Magic.",
      "Second form: fast attack speed, still high evasion; warps around the room to whoever has hate (and sometimes at random). Casts tier-2 Ancient Magic and gains -ja spells at 25% (very high damage if unresisted).",
      "Vortex resets hate — running away after it may send him at someone else.",
      "Title: Dream Distiller (VD only).",
    ])

# ---------------------------------------------------------------- TENZEN (fam=Humanoid)
upd("tenzen",
    job="Samurai", nm=True,
    ab=["Amatsu: Kazakiri","Amatsu: Torima","Amatsu: Yukiarashi","Amatsu: Tsukioboro","Amatsu: Hanaikusa",
        "Amatsu: Kamikaeshi","Amatsu: Tsukikage","Oisoya","Yaegasumi","Meikyo Shisui"],
    st=[["Fire","-15%"]], wk=[],
    drops="Ginsen, Hangaku-no-Yumi, Seraphicaller, Divinator, Sukeroku Hachi., Battlecast Gaiters, Mizu. Kubikazari",
    zones=[["Sealions Den"]],
    img="mobimages/tenzen.png",
    notes=[
      "The Warrior's Path ★ — fought in Sealion's Den with a Warrior's Path phantom gem (all members need the key item).",
      "Eats a rice ball at ~50% HP or less, boosting all his stats and granting Damage Taken -25%.",
      "Switches between Great Katana and Bow; ranged attacks target the furthest player and can quickly kill mages.",
      "Uses Yaegasumi and Meikyo Shisui.",
      "Has an unnamed SP (~50% HP or less) that stops him taking physical damage; still takes magic damage. During it he stops moving and spams ~7-10 weapon skills on the player with the most hate — step back to take no damage.",
      "Assisted by the Chebukki siblings: Kukki (single/AoE elemental magic, Stun, Aspir, Drain, Sleepga, elemental DoTs, Meteor), Cherukkiki (Cure/Regen/Haste/Protect/Shell/Silence/Slow/Diaga/Holy/Banishga), and Makki (ranged). The Chebukki are susceptible to Sleepga and Lullaby; higher difficulties need more magic accuracy (Elemental Seal / Troubadour help).",
      "The non-★ fight is weak to all elements (+30%); the ★ fight resists Fire (-15%) and is neutral to the rest.",
      "Title: Unwavering Blaze (VD Clear).",
    ])

# ---------------------------------------------------------------- OURYU (fam=Wyrm, Dragon eco)
upd("ouryu",
    ab=["Bai Wing","Absolute Terror","Ochre Blast","Geotic Breath","Horrid Roar","Spike Flail","Touchdown","Invincible","Draw In"],
    sp=["Stoneskin","Stonega III","Breakga","Break"],
    det=["True Sound"],
    im=["Stun","Slow","Elegy"],
    zones=[["Riverne-Site A01","85"],["Riverne-Site B01"],["Monarch Linn"]],
    drops="Imanotsurugi, Tutelary, Herald's Gaiters, Hegira Wristbands, Ischemia Chasu., Metalsinger Belt",
    img="mobimages/ouryu.png",
    notes=[
      "Ouryu Cometh BCNM (Riverne-Site A01, up to 18 members, 1-hour limit): trade a Cloud Evoker to the Unstable Displacement at (I-9) to enter.",
      "Also fought in The Savage II battlefield (Monarch Linn, entered with a Savage's phantom gem).",
      "Uses Invincible multiple times; casts Stoneskin, Stonega III, Breakga, and Break; also Draw In and Auto-Regen.",
      "Stays grounded ~2 minutes then flies ~2 minutes; while airborne its attacks are Earth-based magic damage.",
      "Bai Wing has an added Slow effect.",
      "An Earth Elemental and a Water Elemental also aggro and build resistance to Sleep — use Elemental Seal to land Sleep reliably. Four Ziryu also aggro (they can be Charmed); position Ouryu so only one is in range.",
      "Touchdown resets Ouryu's TP to 0. Earth-based, so immune to Stun, Slow, and Elegy.",
      "Also yields Monarch's Orb (a key item for Monarch Linn battlefields).",
      "Title: Ouryu Overwhelmer.",
    ])

# ---------------------------------------------------------------- GUARDS
nulls = [k for m in M.values() for k, v in m.items() if v is None]
assert not nulls, ('NULL values: %r' % nulls[:20])
TOUCHED = ["eald'narche","tenzen","ouryu"]
undef = sorted({a for k in TOUCHED for a in (M[k].get('ab') or []) if a not in A})
assert not undef, ('UNDEFINED ability refs in edited mobs: %r' % undef)
# also: nothing anywhere should reference the removed typo key
assert 'Orche Blast' not in A and not any('Orche Blast' in (m.get('ab') or []) for m in M.values())

json.dump(d, open(P,'w'), separators=(', ', ': '), ensure_ascii=False)
print('created abilities:', created, '| total abilities:', len(A), '(was %d)' % before_ab)
print('mobs:', len(M), '| family_eco:', len(d['family_eco']), '| family_icons:', len(d['family_icons']))
print('GUARDS PASSED (no nulls, no undefined ab refs, Orche Blast fully removed)')
