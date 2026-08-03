#!/usr/bin/env python3
"""Rev 124 — rest of the Sortie NM group: AMINON (final boss, build) + FETID IXION grid fix
+ Haughty Tulittia / Gyvewrapped Naraka / Triboulex finish. Author: BalladOfWorms."""
import json, sys, os

ASSETS = sys.argv[1] if len(sys.argv) > 1 else 'android/app/src/main/assets'
P = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(P)); m = d['mobs']; AB = d['abilities']

def E(*pairs): return [[e, mag] for e, mag in pairs]

# --------------------------------------------------------------- AMINON (build)
# Grid: top row all 100% except Ranged 5% (-95); bottom = 5% floor on all 8
# (6 wheel elements rotate to 70/150, Light/Dark fixed 5%). wk [].
AMINON_KIT = ["Bane of Tartarus","Blast of Reticence","Ceaseless Surge","Crippling Agony",
              "Demonfire","Ensepulcher","Eternal Misery","Frozen Blood","Impudence",
              "Incessant Void","Tenebrous Grip","Torrential Pain"]
m['aminon'] = {
  "n": "Aminon", "fam": "Humanoid", "job": "Rune Fencer / Dark Knight", "nm": True,
  "lv": [149,149], "nmlv": "149",
  "wk": [], "st": E(("Ranged","-95%"),
                    ("Fire","-95%"),("Wind","-95%"),("Lightning","-95%"),("Light","-95%"),
                    ("Ice","-95%"),("Earth","-95%"),("Water","-95%"),("Dark","-95%")),
  "ab": list(AMINON_KIT),
  "zones": [["Outer Ra'Kaznar [U]", "149"]],
  "drops": "Ra'Kaz. Starstone, Old Case +1",
  "img": "mobimages/aminon.png",
  "spawn": "Sortie: the final battlefield. Requires all four Ra'Kaznar Fragments; entered via the Diaphanous Gadget in Sector E (up the ramp west of the 12 Flan room).",
  "notes": [
    "Sortie NM — the final boss. Level 149, ~5,500,000 HP. Title: Aminon Apprehender. Also awards 30,000 Gallimaufry. Requires all four Ra'Kaznar Fragments to access; entered via the Diaphanous Gadget in Sector E (up the ramp west of the 12 Flan room).",
    "If anyone in the party has a stage-4 Prime Weapon, a second option appears: Normal mode 'Forward!' (Mesosiderite will NOT drop) vs Hard mode 'To the deepest dark!' (Mesosiderite has a chance to drop only for stage-4 players). Aminon is locked into hard mode for the rest of the run, so choose carefully. It always opens the fight with Incessant Void a few moments after aggro/pull (usually about 2 melee rounds).",
    "Changes its elemental weakness based on the TP move used; counter with the opposing element's magic damage to proc blue (!!): Demonfire (Fire) -> counter with Water; Torrential Pain (Water) -> counter with Thunder; Frozen Blood (Ice) -> counter with Fire; Ensepulcher (Earth) -> counter with Wind; Ceaseless Surge (Lightning) -> counter with Earth; Blast of Reticence (Wind) -> counter with Ice. Even 0-damage subjob Elemental Magic procs it; countering with the correct element five times in a row procs a stronger !! and removes active fetters. Unaffected by Slow/Elegy.",
    "Resistance ranking: 5% (near-immune) to any element that is not its last TP move's element, 150% (very weak) to the corresponding element (Fire after Demonfire, etc.), and 70% to its current elemental weakness. Geomancy 50%; it also resists Ranged attacks at 5%. It gains -5% Damage Taken for each 30 seconds it stays un-proc'd after a TP move, retained for the rest of the fight; proccing does NOT reset accumulated DT, and the DT is not reset even after leaving the battle area and returning.",
    "Bane of Tartarus is used every 4 minutes from the start of battle: it Dispels all buffs including food, inflicts Death and a ~60-second weakness, and generally KOs everyone within its ~20+ yalm range. The Death effect can be resisted with Resist Death gear; a proc delays the timer. Unlike Setting the Stage it can be stopped by Elemental Sforzo (though it still fully dispels and weakens); Perfect Defense and Mana Wall also work; Valiance and other magic-damage-reduction reduce it; possessing a Ra'Kaznar Seal reduces its power (potentially survivable with Scherzo/Migawari/Earthen Armor, though testing is needed). It can also be triggered by healing Aminon with the matching Elemental Magic or skillchain to the last TP move. On a wipe/recovery the timer does not stop; after three idle minutes the first move is Bane of Tartarus, which must hit a target before the timer resets (you may not bind and run away while the timer passes).",
    "Possessing a Ra'Kaznar Seal changes several abilities: Bane of Tartarus prevents its Death; Blast of Reticence inflicts Silence instead of Mute; Crippling Agony prevents equipment removal; Demonfire inflicts Burn (-19/tic) instead of Plague; Ensepulcher inflicts Slow instead of Petrification; Eternal Misery and Impudence inflict Haunt with no enmity reset; Incessant Void prevents its Dispel; Tenebrous Grip prevents Reraise removal; Torrential Pain inflicts Poison instead of Taint."
  ]
}

# --------------------------------------------------- FETID IXION (grid override)
# Its own page grid differs from the standard Monocero set -> per-mob override.
fi = m['fetid ixion']
fi['job'] = "Warrior"
fi['nm'] = True
fi['lv'] = [135,135]; fi['nmlv'] = "135"
fi['wk'] = E(("Dark","+30%"))
fi['st'] = E(("Fire","-40%"),("Wind","-40%"),("Lightning","-40%"),("Light","-80%"),
             ("Ice","-15%"),("Earth","-15%"),("Water","-15%"))
fi['zones'] = [["Outer Ra'Kaznar [U]", "135"]]
fi['img'] = "mobimages/fetid ixion.png"
fi['spawn'] = "Sortie (Outer Ra'Kaznar [U]) — spawns in the #F section maps."
fi['notes'] = [
  "Sortie NM, ~616,000 HP, M.DEF 100. Spawns in the #F section maps of Sortie.",
  "Weak to Dark (+30%) and Light-vulnerable is inverted here from the standard Ixion form — it resists Light heavily (-80%) and is weak to Dark instead. Uses the Monocero (Ixion) TP moveset."
]

# ------------------------------------------- HAUGHTY TULITTIA (kit + render)
ht = m['haughty tulittia']
if "Wildwood Indignation" not in ht['ab']:
    ht['ab'].append("Wildwood Indignation")     # page's named move (debuff-copy)
ht['nmlv'] = "142"
ht['img'] = "mobimages/haughty tulittia.png"
# grid kept: page resistances are ALL '?' -> keep the Leafkin family stamp.

# ------------------------------------------- GYVEWRAPPED NARAKA (render + HP)
gn = m['gyvewrapped naraka']
gn['nmlv'] = "140"
gn['img'] = "mobimages/gyvewrapped naraka.png"
gn['notes'] = [
  "Sortie NM, ~700,000 HP. Spawns in the #G section maps of Sortie.",
  "Resistances are undocumented (the page lists every cell as unknown); the grid shown is the Naraka family default."
]
# grid + kit kept: page resistances are ALL '?' -> keep the Naraka family stamp.

# ------------------------------------------------------ TRIBOULEX (render only)
m['triboulex']['img'] = "mobimages/triboulex.png"   # already built + grid-correct; re-affirm render

# ---- guards ----------------------------------------------------------------
assert not [ (k,f) for k,mob in m.items() for f,v in mob.items() if v is None ], "null leaked"
for k in ['aminon','fetid ixion','haughty tulittia','gyvewrapped naraka','triboulex']:
    for a in m[k].get('ab', []):
        assert a in AB, (k,'undefined ability',a)
    assert isinstance(m[k].get('ab_el', []), list)

# spot-check the shared Aminon-kit defs are real (not empty stubs)
print("--- Aminon kit def sanity ---")
for a in ["Bane of Tartarus","Incessant Void","Impudence","Torrential Pain"]:
    print("  ", a, '::', AB[a].get('t'), AB[a].get('el'), '|', (AB[a].get('d') or '')[:60])

json.dump(d, open(P,'w'), ensure_ascii=False, separators=(', ', ': '))
print("\nrev124 written OK")
for k in ['aminon','fetid ixion','haughty tulittia','gyvewrapped naraka','triboulex']:
    mob=m[k]
    print(f"  {k:19} nm={mob.get('nm')} lv={mob.get('lv')} img={mob.get('img'):27} #ab={len(mob.get('ab',[]))}")
