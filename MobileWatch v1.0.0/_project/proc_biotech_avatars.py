import json
d=json.load(open('mobs.json'))
m=d['mobs']; AB=d['abilities']
def setab(name,**kw):
    AB[name]=kw
def enrich(name,**kw):
    AB.setdefault(name,{}).update({k:v for k,v in kw.items() if v is not None})

# ================= ABILITIES =================
# --- Omega line: create missing ---
setab('Floodlight', d="Fires a searing light over a large area.", t="Magical", r="Front cone",
      tgt="AoE", fx=["Flash","Blind","Silence"],
      notes="Used by Proto-Omega and Arch-Omega (two-legged form).")
setab('Guided Missile II', d="Targets players around its current target with a missile. Additional effect: Bind.",
      t="Physical", r="Around target", tgt="AoE", fx=["Bind"],
      notes="Used by Proto-Omega and Arch-Omega (two-legged form). Ignores shadows.")
setab('Laser Shower', d="Rains laser fire on players in a fan-shaped area.", t="Physical",
      r="Front cone", tgt="AoE", notes="Used by Proto-Omega and Arch-Omega.")
setab('Pod Ejection', d="Ejects and deploys a Gunpod to assist it.", r="Self", tgt="Self",
      notes="Used periodically by Proto-Omega and Arch-Omega. Gunpods self-destruct with Electrocharge for severe AoE damage if not defeated quickly.")
setab('Rear Lasers', d="Fires lasers to the rear at players holding hate from behind. Additional effect: Petrification.",
      t="Physical", r="Rear cone", tgt="AoE", fx=["Petrification"],
      notes="Only used when hate is pulled from the rear.")
setab('Stun Cannon', d="Fires an energy cannon at players in a fan-shaped area. Additional effect: Paralysis.",
      t="Physical", r="Front cone", tgt="AoE", fx=["Paralysis"],
      notes="Used by Proto-Omega and Arch-Omega (two-legged form). Ignores shadows.")
# --- Ultima line: create missing ---
setab('Armor Buster', d="Deals damage to players in range. Additional effect: Weight.", t="Magical",
      tgt="AoE", fx=["Weight"], notes="Used by Proto-Ultima and Arch-Ultima. Can be absorbed by shadows.")
setab('Citadel Buster', d="Charges and unleashes a devastating light blast over a wide radius.", t="Magical",
      el="Light", r="30' radial", tgt="AoE",
      notes="Used below ~25% HP after a ~30-second charge (up to ~2600 damage); resets hate. Preceded by a warning countdown and mitigated by Sentinel's Scherzo, Migawari: Ichi, or Earthen Armor.")
setab('Citadel Siege', d="Instantly K.O.s a single player.", r="Single", tgt="Single",
      notes="Arch-Ultima only, at 49/39/29/19/9% HP. Avoidable by keeping distance; skipped while Arch-Ultima is readying Citadel Buster.")
setab('Dissipation', d="Emits a pulse that strips beneficial effects from players in range. Additional effect: Terror + Enmity reset.",
      t="Magical", tgt="AoE", fx=["Terror"], notes="Full dispel. Can be blocked with Asylum. Used at set HP intervals.")
setab('Energy Screen', d="Erects a barrier that nullifies physical damage.", t="Enhancing", r="Self",
      tgt="Self", fx=["Physical Shield"], notes="Cannot be active at the same time as Mana Screen.")
setab('Mana Screen', d="Erects a barrier that nullifies magical damage.", t="Enhancing", r="Self",
      tgt="Self", fx=["Magic Shield"], notes="Cannot be active at the same time as Energy Screen.")
setab('Wirecutter', d="Slashes a single player for high physical damage.", t="Physical", r="Melee",
      tgt="Single", notes="Can be absorbed by shadows or Third Eye. Consumes two shadows.")
setab('Catastrophic Malfunction', d="Deals damage to players in range and lowers their elemental resistances.",
      t="Magical", tgt="AoE",
      notes="Arch-Ultima only. Above 50% HP it is followed by a tier-V nuke or Comet; below 50% by a -ja nuke, Banishga IV, or Meteor.")
# --- Atomos (Avatar NM) ---
setab('Soul Vacuum', d="Drains attributes from all players within range, reducing each stat by roughly 50 points.",
      r="AoE", tgt="AoE", notes="Used by Atomos, immediately followed by Soul Infusion.")
setab('Soul Infusion', d="Transfers the attributes drained by Soul Vacuum to Cait Sith Ceithir.",
      r="Self", tgt="Self", notes="Used immediately after Soul Vacuum.")
# --- enrich existing conal elementals + others (el is a STRING) ---
enrich('Cryo Jet', el="Ice")
enrich('Flame Thrower', el="Fire")
enrich('High-Tension Discharger', el="Lightning")
enrich('Smoke Discharger', el="Earth")
enrich('Turbofan', el="Wind")
enrich('Hydro Canon', el="Water")
AB['Hydro Canon'].setdefault('fx',[])
if 'Poison' not in AB['Hydro Canon']['fx']: AB['Hydro Canon']['fx']=list(AB['Hydro Canon']['fx'])+['Poison']
# Antimatter: fix type (was Ranged) -> Magical single-target
AB['Antimatter'].update({'t':'Magical','tgt':'Single'})
AB['Antimatter']['notes']=(AB['Antimatter'].get('notes','')+' Ignores Utsusemi.').strip()
# Equalizer stub -> full
AB['Equalizer']={'d':"Deals physical damage to players in range. Additional effect: Knockback.",
                 't':'Physical','tgt':'AoE','fx':['Knockback'],'notes':'Used by Ultima and Proto-Ultima.'}
# Chemical Bomb: damage type Physical (table), keep Slow/Elegy
AB['Chemical Bomb']['t']='Physical'

# ================= PER-MOB =================
DET=['Sight','Sound']
def upd(key,**kw):
    v=m[key]
    for k,val in kw.items():
        if val is None: continue
        v[k]=val
    return v

# --- family taxonomy ---
d['family_eco']['Biotechnological Weapon']='Unclassified'
d.setdefault('family_notes',{})['Biotechnological Weapon']=[
  "Legendary machine weapons (\u4f1d\u8aac\u306e\u6a5f\u7363) of ancient Zilart design \u2014 the Omega and Ultima model lines and their Prototype, Arch, and Forerunner revisions.",
  "Omega models swap between a four-legged and a two-legged stance, each with its own TP-move set (four-legged resists physical damage, two-legged resists magical); Ultima models are stationary casters that follow Nuclear Waste with an elemental conal attack."
]

# ---- OMEGA (CoP, One to be Feared) ----
upd('omega', nm=True, det=DET, job='Warrior / Monk',
    ab=['Guided Missile','Rear Lasers','Ion Efflux','Target Analysis','Hyper Pulse','Discharger','Pile Pitch'],
    zones=[["Sealion's Den",""]],
    drops="Denouements, Culminus, Terminal Helm, Terminal Plate, Cessance Earring, Consumm. Torque",
    notes=["Fought in Sealion's Den during Promathia Mission 6-4 (One to be Feared, ~14,000 HP) and, in the reissue, with a Feared One phantom gem (One to be Feared II \u2014 every participant needs the key item to enter).",
           "Traits: Counter, Enstun."])

# ---- ULTIMA (CoP, One to be Feared) ----
upd('ultima', nm=True, det=DET, job='White Mage',
    ab=['Antimatter','Chemical Bomb','Cryo Jet','Equalizer','Flame Thrower','High-Tension Discharger','Hydro Canon','Nuclear Waste','Particle Shield','Smoke Discharger','Turbofan','Wirecutter'],
    zones=[["Sealion's Den",""]],
    drops="Denouements, Culminus, Terminal Helm, Terminal Plate, Cessance Earring, Consumm. Torque",
    notes=["Fought in Sealion's Den during Promathia Mission 6-4 (One to be Feared, ~15,000 HP) and, in the reissue, with a Feared One phantom gem (One to be Feared II \u2014 every participant needs the key item to enter).",
           "Traits: Auto Regen, Enparalyze."])

# ---- PROTO-OMEGA (Limbus) ----
upd('proto-omega', nm=True, det=DET,
    wk=[['Lightning','+15%']], st=[['Dark','-95%']],
    ab=['Guided Missile II','Hyper Pulse','Stun Cannon','Floodlight','Pod Ejection',
        'Guided Missile','Ion Efflux','Target Analysis','Pile Pitch','Rear Lasers',
        'Colossal Blow','Laser Shower'],
    zones=[['Apollyon','']],
    drops="Homam Zucchetto, Homam Manopolas, Homam Cosciales, Homam Gambieras, Homam Corazza",
    notes=["Central Apollyon Limbus boss (~26,000 HP). Walks on two and four legs, using a different TP-move set in each form: two-legged \u2014 Guided Missile II, Hyper Pulse, Stun Cannon, Floodlight, Pod Ejection; four-legged \u2014 Guided Missile, Ion Efflux, Target Analysis, Pile Pitch, Rear Lasers; adds Colossal Blow and Laser Shower below 25% HP.",
           "Drop cells (Omega's Eye/Foreleg/Hind Leg/Tail/Heart) craft the listed Homam armor set."])

# ---- PROTO-ULTIMA (Limbus) ----
upd('proto-ultima', nm=True, det=DET,
    wk=[['Lightning','+15%']], st=[['Magical','-30%']],
    ab=['Draw-In','Antimatter','Wirecutter','Chemical Bomb','Nuclear Waste','Hydro Canon','Turbofan',
        'Smoke Discharger','Flame Thrower','Cryo Jet','High-Tension Discharger','Equalizer',
        'Energy Screen','Mana Screen','Armor Buster','Dissipation','Citadel Buster'],
    zones=[['Temenos','']],
    drops="Nashira Turban, Nashira Gages, Nashira Seraweels, Nashira Crackows, Nashira Manteel",
    notes=["Central Temenos \u2013 4th Floor Limbus boss (~50,000 HP). Unlocks moves as its HP falls (Nuclear Waste + elemental conals under 80%, Equalizer under 60%, Energy/Mana Screen and Armor Buster under 40%, Citadel Buster under 25%). Uses Dissipation immediately on reaching 79/59/39/19% HP and casts Holy II on a random player.",
           "Under 25% its Citadel Buster charges ~30 seconds for up to ~2600 damage.",
           "Drop cells (Ultima's Cerebrum/Claw/Leg/Tail/Heart) craft the listed Nashira armor set."])

# ---- ARCH-OMEGA (Apollyon reissue) ----
upd('arch-omega', nm=True, det=DET,
    ab=['Guided Missile','Ion Efflux','Target Analysis','Pile Pitch','Rear Lasers',
        'Guided Missile II','Hyper Pulse','Stun Cannon','Floodlight','Colossal Blow','Laser Shower','Pod Ejection'],
    zones=[['Apollyon','']],
    drops="A.Omega Eye, A.Omega Foreleg, A.Omega Hind Leg, A.Omega Tail, A.Omega Heart",
    notes=["Central Apollyon II reissue (~100,000 HP). Immune to Stun but susceptible to Slow and Elegy; 100% Double Attack, so it uses two TP moves in a row.",
           "Four-legged form (100\u201375% HP) resists physical damage \u2014 Guided Missile, Ion Efflux, Target Analysis, Pile Pitch, Rear Lasers. Two-legged form (<75% HP) resists magical damage \u2014 Guided Missile II, Hyper Pulse, Stun Cannon, Floodlight, Colossal Blow, Laser Shower, Pod Ejection.",
           "Assisted by Gunpods (from Pod Ejection); unlike Proto-Omega's, these Gunpods have no drops. Ancient Beastcoins also drop.",
           "Title: Apollyon Razer."])

# ---- ARCH-ULTIMA (Temenos reissue) ----
upd('arch-ultima', nm=True, det=DET,
    ab=['Draw-In','Antimatter','Energy Screen','Mana Screen','Catastrophic Malfunction','Armor Buster',
        'Chemical Bomb','Equalizer','Wirecutter','Hydro Canon','Turbofan','Smoke Discharger','Flame Thrower',
        'Cryo Jet','High-Tension Discharger','Dissipation','Citadel Siege','Citadel Buster'],
    zones=[['Temenos','']],
    drops="A.Ultima Cerebrum, A.Ultima Claw, A.Ultima Leg, A.Ultima Tail, A.Ultima Heart",
    notes=["Central Temenos \u2013 4th Floor II reissue (~100,000 HP). Immune to Stun but susceptible to Slow and Elegy; uses draw-in on its hate target if it strays too far.",
           "Antimatter is single-target Light magic that ignores Utsusemi. Catastrophic Malfunction lowers elemental resistances and is chased by a tier-V nuke or Comet above 50% HP, or a -ja nuke / Banishga IV / Meteor below 50%.",
           "Citadel Siege (single-target instant K.O.) fires at 49/39/29/19/9% HP and can be dodged with distance; below 50% it charges Citadel Buster (30' severe light AoE) behind a warning countdown.",
           "Ancient Beastcoins also drop. Title: Temenos Emancipator."])

# ---- OMEGA FORERUNNER (CN Apollyon world boss) ----
upd('omega forerunner', nm=True, det=DET,
    ab=['Pod Ejection','Guided Missile II','Hyper Pulse','Stun Cannon','Floodlight','Colossal Blow','Laser Shower',
        'Guided Missile','Ion Efflux','Target Analysis','Pile Pitch','Rear Lasers','Discharger'],
    zones=[['Apollyon','']],
    notes=["Appears in CN Apollyon once all T3 objectives are met. Party-wide aggro \u2014 if any member of a party holds hate (even at 0 enmity) it will not reset until that whole party is defeated. Susceptible to all debuffs, but Discharger applies a perfect Magic Shield that makes debuffs fail while active.",
           "Every 10% HP it uses Pod Ejection and gradually spawns 12 Omega's Bit (Detector). Bits have high evasion and take all debuffs except Gravity, though Sleep/Bind/Break are easily broken. Bipedal mode: Bits keep loose enmity and switch targets. Quadrupedal mode: Bits spawn on a non-hate player and deal an unnamed ~20' AoE magic hit.",
           "As of December 2025, Defense, Damage Taken, and Shield damage reduction do not work correctly \u2014 Utsusemi and high-HP builds plus heavy direct healing and Geomancy are recommended. On defeat, upgrades Apollyon treasure chests to gold for the following 4-week cycle."])

# ---- ULTIMA FORERUNNER (CN Temenos Basement world boss) ----
upd('ultima forerunner', nm=True, det=DET,
    ab=['Draw-In','Antimatter','Wirecutter','Chemical Bomb','Nuclear Waste','Hydro Canon','Turbofan',
        'Smoke Discharger','Flame Thrower','Cryo Jet','High-Tension Discharger','Equalizer',
        'Energy Screen','Mana Screen','Armor Buster','Dissipation','Citadel Buster'],
    zones=[['Temenos','']],
    notes=["Appears in CN Temenos Basement once all T3 objectives are met. Party-wide aggro (as Omega Forerunner). Can double auto-attack. Uses Dissipation immediately on reaching 70/35/10% HP (blockable with Asylum), and Citadel Buster roughly every 3\u20135 minutes (mitigate with Sentinel's Scherzo, Migawari: Ichi, or Earthen Armor).",
           "Nuclear Waste spawns six Ultima's Zisurru (fetters) on a designated player \u2014 30' AoE, ~500 undodgeable damage per hit through walls, used roughly every 3\u20136% HP; the fetters despawn 30\u201360 seconds before the next Nuclear Waste. Gains Energy Screen or Mana Screen under 50% (only one at a time).",
           "As of December 2025, Defense, Damage Taken, and Shield reduction do not work correctly \u2014 favor Utsusemi and high-HP builds with heavy direct healing and Geomancy. On defeat, upgrades Apollyon treasure chests to gold for the following 4-week cycle."])

# ---- PANTOKRATOR (Abyssea NM) ----
p=m['pantokrator']
upd('pantokrator', nm=True, det=DET,
    ab=['Chainspell','Hundred Fists'],
    zones=[['Abyssea-Uleguerand','']],
    drops="Pan's Horn, Zelus Tiara, Torero Torque",
    notes=["Abyssea-Uleguerand NM (3 spawn). Examine the ??? at (G-7) while holding a Warped Iron Giant Nail and a Dented Chariot Shield.",
           "Like the other Omega models it swaps between a standing (two-legged) stance and a four-legged stance, and absorbs damage while casting or readying a TP move. Uses Chainspell repeatedly on four legs and Hundred Fists repeatedly while standing.",
           "Also drops the key items Atma of the Omnipotent and Battle Trophy: 1st Echelon. Title: Pantokrator Disprover."])

# ================= AVATAR NMs =================
# ---- BAHAMUT (Avatar NM) ----
upd('bahamut', fam='Avatar', nm=True, job='Black Mage', crys='Fire', det=['Sight'],
    lv=[83,85], zones=[['Riverne-Site B01','83-85']],
    drops="Bahamut's Staff, Dragon Staff, Bahamut's Mask, Bahamut's Hose, Bahamut Zaghnal",
    notes=["Riverne-Site B01 NM. Spawns during the Wings of the Goddess mission Storms of Fate (Lv 83) and the quest The Wyrmking Descends (Lv 85).",
           "A Black Mage that casts tier-V nukes plus Firaga IV, Flare II, Graviga, Silencega, and Dispelga, and self-buffs with Stoneskin, Phalanx, Protect V, and Shell V. Title: Wyrm Astonisher."])

# ---- ATOMOS (Avatar NM) ----
m['atomos']={
    'n':'Atomos','fam':'Avatar','nm':True,'det':['Sound'],
    'ab':['Soul Vacuum','Soul Infusion'],
    'zones':[['Ruhotz Silvermines','']],
    'notes':["Summoned by Cait Sith Ceithir during the Wings of the Goddess mission Distorter of Time, in Ruhotz Silvermines. Performs two moves in a row and then vanishes; there is no known way to stop it.",
             "Soul Vacuum drains every attribute (about 50 points each) from players in range; Soul Infusion then transfers all of that to Cait Sith Ceithir."]}

json.dump(d, open('mobs.json','w'), separators=(', ', ': '), ensure_ascii=False)

# guards
d2=json.load(open('mobs.json'))
bad=[k for mob in d2['mobs'].values() for k,v in mob.items() if v is None]
assert not bad, ('NULL POISON', bad[:5])
undef=sorted({a for v in d2['mobs'].values() for a in (v.get('ab') or []) if a not in d2['abilities']})
print('abilities:',len(d2['abilities']),'| mobs:',len(d2['mobs']),'| family_eco:',len(d2['family_eco']))
print('undefined refs (this pass targets):',[a for a in undef if a in
      ['Floodlight','Guided Missile II','Laser Shower','Pod Ejection','Rear Lasers','Stun Cannon','Armor Buster',
       'Citadel Buster','Citadel Siege','Dissipation','Energy Screen','Mana Screen','Wirecutter',
       'Catastrophic Malfunction','Soul Vacuum','Soul Infusion','Draw-In','Colossal Blow']])
print('total undefined refs file-wide:',len(undef))
print('Biotech eco:',d2['family_eco'].get('Biotechnological Weapon'),'| Avatar eco:',d2['family_eco'].get('Avatar'))
for k in ['proto-omega','proto-ultima','arch-ultima','omega forerunner','bahamut','atomos']:
    v=d2['mobs'][k]; print('  %-18s eco? fam=%s nm=%s ab=%d zones=%s' % (k,v.get('fam'),v.get('nm'),len(v.get('ab') or []),v.get('zones')))
