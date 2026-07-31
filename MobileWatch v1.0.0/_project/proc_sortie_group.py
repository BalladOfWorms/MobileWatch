#!/usr/bin/env python3
"""Rev 123 — Sortie NM group: Aita, Degei (new builds) + Leshonn/Gartell grid fixes
+ renders on all six. Author: BalladOfWorms."""
import json, sys, os

ASSETS = sys.argv[1] if len(sys.argv) > 1 else 'android/app/src/main/assets'
P = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(P))
m = d['mobs']

def E(*pairs):
    return [[e, mag] for e, mag in pairs]

ALL8_M95 = E(("Fire","-95%"),("Wind","-95%"),("Lightning","-95%"),("Light","-95%"),
             ("Ice","-95%"),("Earth","-95%"),("Water","-95%"),("Dark","-95%"))
HUMANOID_KIT = ["Eroding Flesh","Flaming Kick","Flashflood","Fulminous Smash","Icy Grasp","Vivisection"]
MACUIL_KIT   = ["Chokehold","Concussive Shock","Shrieking Gale","Tearing Gust",
                "Undulating Shockwave","Zap"]

# ---------------------------------------------------------------- AITA (build)
m['aita'] = {
  "n": "Aita", "fam": "Humanoid", "job": "Rune Fencer / Dark Knight", "nm": True,
  "lv": [145,145], "nmlv": "145",
  "wk": [], "st": ALL8_M95, "ab": list(HUMANOID_KIT),
  "zones": [["Outer Ra'Kaznar [U]", "145"]],
  "drops": "Ra'Kaznar Frag. #4, Ra'Kaz. Starstone, Old Case, Old Case +1",
  "img": "mobimages/aita.png",
  "spawn": "Sortie: found past Diaphanous Gadget #H in Outer Ra'Kaznar [U]. A Ra'Kaznar Shard #H is needed to access it.",
  "notes": [
    "Sortie NM. Found past Diaphanous Gadget #H; needs a Ra'Kaznar Shard #H to access. EVA 1,613. Title: Aita Abnegater. Traits: Cumulative WS Resistance, INT 494, MND 427. Also awards 10,000 Gallimaufry.",
    "Changes its elemental weakness based on the TP move it uses; counter with the opposing element's magic damage to proc blue (!!): Flaming Kick (Fire) -> counter with Water; Flashflood (Water) -> counter with Thunder; Icy Grasp (Ice) -> counter with Fire; Eroding Flesh (Earth) -> counter with Wind; Fulminous Smash (Lightning) -> counter with Earth. Even 0-damage subjob Elemental Magic will proc it. Using an elemental TP move after the first summons fetter(s) that deal damage and an element-based DoT; the number of fetters grows as HP drops.",
    "Resistance ranking: 150% (very weak) to the last TP move's element, 70% (weak) to its current elemental weakness, and 5% (near-immune) to every other element. Geomancy 50%. It gains -5% Damage Taken for each 30 seconds it remains un-proc'd after a TP move (e.g. Flaming Kick -> -DT vs Water until proc'd), retained for the rest of the fight; proccing does NOT reset accumulated DT.",
    "Vivisection is used every 3 minutes and generally kills everyone within its 20+ yalm range. Elemental Sforzo / Liement / Perfect Defense / Mana Wall / Annuls Damage procs stop its damage; Valiance and other magic-damage-reduction effects reduce it. Correctly proccing blue reduces Vivisection's damage and, below a threshold, removes its wings (and slows the seal decay). Vivisection can also be triggered by healing Aita with the last TP move's Elemental Magic or a matching skillchain. Vivisection resets the elemental weakness — a new TP move must be used before it is vulnerable again.",
    "On a full wipe, accumulated DT is NOT reset unless you leave the battle area, wait a while, then re-enter. During a wipe/recovery the timer does not stop; after three idle minutes the first move Aita uses is Vivisection, and it must hit a target before the timer resets (you may not bind and run away while the timer passes)."
  ]
}

# --------------------------------------------------------------- DEGEI (build)
m['degei'] = {
  "n": "Degei", "fam": "Humanoid", "job": "Rune Fencer / Dark Knight", "nm": True,
  "lv": [135,135], "nmlv": "135",
  "wk": [], "st": ALL8_M95, "ab": list(HUMANOID_KIT),
  "zones": [["Outer Ra'Kaznar [U]", "135"]],
  "drops": "Ra'Kaznar Shard #H, Ra'Kaz. Sapphire, Old Case, Old Case +1",
  "img": "mobimages/degei.png",
  "spawn": "Sortie: found past Diaphanous Gadget #D in Outer Ra'Kaznar [U]. A Ra'Kaznar Shard #D is needed to access it.",
  "notes": [
    "Sortie NM. Found past Diaphanous Gadget #D; requires a Ra'Kaznar Shard #D to access. EVA 1,249. Also awards 2,000 Gallimaufry.",
    "Enrages after fighting for 3 minutes, after which it takes 1/4 damage and only uses Vivisection. Rage is not removed by regenning back to 100% HP.",
    "Changes its elemental weakness based on the TP move used, and heals to the current element; casting magic of the opposing element procs blue (!!): Flaming Kick (Fire) -> counter with Water; Flashflood (Water) -> counter with Thunder; Icy Grasp (Ice) -> counter with Fire; Eroding Flesh (Earth) -> counter with Wind; Fulminous Smash (Lightning) -> counter with Earth. Any appropriate magic triggers the proc, even Threnody or subjob Elemental Magic.",
    "Gains Damage Resistance (~-5% DT, retained) for each 30 seconds it stays un-proc'd after changing elements.",
    "Vivisection is used roughly every 3 minutes, and can be triggered early by healing Degei with the wrong Elemental Magic or a wrong skillchain and failing to proc in time (higher heal amounts may need more procs). After Vivisection it keeps the Damage Taken accumulated from not proccing and has no weakness — feed it TP quickly so it uses one of the five elemental moves again. On a wipe/recover the first move is Vivisection. Wrong skillchains heal Degei, so it is best to avoid skillchains entirely in a melee zerg."
  ]
}

# ---------------------------------------------------- LESHONN (fix grid+notes)
lesh = m['leshonn']
lesh['job'] = "Monk / Black Mage"
lesh['lv'] = [135,135]; lesh['nmlv'] = "135"
lesh['ab_el'] = ["Wind","Lightning"]                     # grid A on Wind + Thunder
lesh['wk'] = []
lesh['st'] = E(("Fire","-95%"),("Light","-95%"),("Ice","-95%"),
               ("Earth","-95%"),("Water","-95%"),("Dark","-95%"))
lesh['zones'] = [["Outer Ra'Kaznar [U]", "135"]]
lesh['drops'] = "Ra'Kaznar Shard #F, Ra'Kaz. Sapphire, Old Case, Old Case +1"
lesh['img'] = "mobimages/leshonn.png"
lesh['nm'] = True
lesh['notes'] = [
  "Sortie NM. Found past Diaphanous Gadget #B; needs a Ra'Kaznar Shard #B to access. Level 135, ~870,000 HP; uses Counter in excess of 500+ HP per hit. Also awards 2,000 Gallimaufry.",
  "Abilities and elemental resistances depend on which hand element is showing. Thunder hand -> Zap / Concussive Shock / Undulating Shockwave (Ra'Kaznar Metal B prevents the Stun rider on auto-attacks); Undulating Shockwave changes it to Wind hands after. Wind hand -> Chokehold / Tearing Gust / Shrieking Gale (Metal B prevents the Gravity rider); Shrieking Gale changes it to Thunder hands after.",
  "Absorbs Wind and Lightning (its two hand elements). Its Wind hand opens an Ice weakness (~70%) and its Thunder hand opens an Earth weakness (~70%); everything else stays near-immune (~5%). Dealing elemental damage (including skillchains) matching the currently displayed element heals it for extreme amounts.",
  "Zap copies a debuff from Leshonn to all party members on each use — extremely dangerous with Paralyze or Helix. Chokehold steals a buff from each party member and transfers it to Leshonn; a wipe is nearly guaranteed if it lands (block with Asylum).",
  "Gains a stacking DT effect (~5%) and a stacking damage-up (~5%) each time it uses a nameless attack (it looks like it is sucking in the air around it). Any elemental damage opposing its current element has a chance to proc blue (higher damage almost always procs); a proc removes the DT/damage-up stacks and can disable the oldest elemental aura it has in effect. It appears to gain resistance to repeated procs from the same source — alternating SC > MB helps. Its hands can be locked out by defeating all enemies of a certain type in the area."
]

# ---------------------------------------------------- GARTELL (fix grid+notes)
gar = m['gartell']
gar['job'] = "Monk / Black Mage"
gar['lv'] = [145,145]; gar['nmlv'] = "145"
gar.pop('ab_el', None)                                   # page shows resist, NOT absorb
gar['wk'] = []
gar['st'] = list(ALL8_M95)
gar['zones'] = [["Outer Ra'Kaznar [U]", "145"]]
gar['drops'] = "Ra'Kaznar Frag. #2, Ra'Kaz. Starstone, Old Case, Old Case +1"
gar['img'] = "mobimages/gartell.png"
gar['nm'] = True
gar['notes'] = [
  "Sortie NM. Found past Diaphanous Gadget #F; needs a Ra'Kaznar Shard #F to access, and a Ra'Kaznar Metal F to limit its abilities. Level 145, 1,600,000 HP; uses Counter in excess of 500+ HP per hit. EVA 1,613. Title: Gartell Grinder. Traits: INT 350, MND 394. Also awards 10,000 Gallimaufry.",
  "Its usable TP moves and elemental Resistance Rank depend on which hand element is showing. Thunder hand -> Zap / Concussive Shock / Undulating Shockwave (Undulating Shockwave changes it to Wind hands after); resistance rank 70% Earth, 5% every other element. Wind hand -> Chokehold / Tearing Gust / Shrieking Gale (Shrieking Gale changes it to Thunder hands after); resistance rank 70% Ice, 5% every other element. With both hands up only Ice damage is effective. Geomancy 50%.",
  "Zap copies one debuff from Gartell to all party members in range — avoid applying strong DoTs (it may transfer them; a magic-bursted Helix practically guarantees a 1-shot on anyone inflicted). Chokehold steals one buff from each party member in range and transfers it to Gartell; absorbing Shell V makes nuking much harder, so cancel and re-apply Shell/Protect (Gartell seems to prioritize Shell and Protect). Tearing Gust inflicts a heavy Magic Defense Down — remove it (Erase/Panacea) or Gartell's attacks do increased damage. Shrieking Gale is heavy Wind damage plus knockback.",
  "Dealing elemental damage (including skillchains) matching the current element heals it for extreme amounts and forces a rage — use the opposing element to proc blue (magic-burst for best odds). This also applies to Level 3 skillchains: do not use a Light skillchain, or you will force the Wind AND Thunder alignment procs.",
  "After 3:00 it begins summoning a Gyve on the top-enmity player; these deal Wind or Thunder damage (the Gyve's colour indicates which) and inflict a very strong Shock and Choke effect of about -296 each — move the tank out of them and Erase/Panacea, since Gartell does much more damage with your VIT and MND reduced this much. Gains a stacking ~5% DT and ~5% damage-up per nameless attack, which also applies to its Gyve (dangerous if Gartell is left un-proc'd, especially with Choke's VIT down).",
  "Any elemental damage opposing its currently selected element has a chance to proc blue (magic bursting strongly advised); a proc removes the DT/damage-up stacks and can disable the oldest elemental aura. Per SE, proccing multiple times can force a change of hands and will delay its use of 'special abilities'."
]

# --------------------------------------------- SKOMORA / DHARTOK (render only)
m['skomora']['img'] = "mobimages/skomora.png"           # was falling back to family icon
m['dhartok']['img'] = "mobimages/dhartok.png"           # re-affirm

# ---- guards ----------------------------------------------------------------
assert not [ (k,f) for k,mob in m.items() for f,v in mob.items() if v is None ], "null value leaked"
for k in ['aita','degei','leshonn','skomora','dhartok','gartell']:
    mob = m[k]
    assert isinstance(mob.get('ab_el', []), list), (k,'ab_el must be list')
    for a in mob.get('ab', []):
        assert a in d['abilities'], (k, 'undefined ability', a)

json.dump(d, open(P,'w'), ensure_ascii=False, separators=(', ', ': '))
print("rev123 written OK")
for k in ['aita','degei','leshonn','gartell','skomora','dhartok']:
    mob=m[k]
    print(f"  {k:9} img={mob.get('img'):25} ab_el={mob.get('ab_el',[])} drops={mob.get('drops')}")
