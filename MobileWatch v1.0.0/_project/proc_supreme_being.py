import json
d=json.load(open('mobs.json')); m=d['mobs']; AB=d['abilities']

def A(name,**kw): AB[name]=kw

# ---- Promathia / Metus ----
A('Empty Salvation', d="AoE damage (~250) that dispels up to 3 beneficial effects.", tgt="AoE", fx=["Dispel"])
A('Pestilent Penance', d="Cone attack (~400 damage) with an additional Plague effect.", t="Physical", r="Front cone", tgt="Cone AoE", fx=["Plague"])
A('Malevolent Blessing', d="Cone attack (400-500 damage) with an additional Curse effect.", t="Physical", r="Front cone", tgt="Cone AoE", fx=["Curse"])
A('Infernal Deliverance', d="AoE damage plus Stun. Ignores Utsusemi.", tgt="AoE", fx=["Stun"])
A('Seal of Quiescence', d="AoE Mute lasting up to 75 seconds. Cannot be removed with Silena or Echo Drops.", tgt="AoE", fx=["Mute"])
A('Winds of Oblivion', d="AoE Amnesia lasting up to 75 seconds.", tgt="AoE", fx=["Amnesia"])
A('Bastion of Twilight', d="Grants the caster a Magic Shield that nullifies magic damage.", tgt="Self", notes="Ring beneath the boss glows green while the magic shield is up.")
A('Wheel of Impregnability', d="Grants the caster Invincible, nullifying physical damage.", tgt="Self", notes="Ring beneath the boss glows red while the physical shield is up.")
for c in ['Apathy','Arrogance','Cowardice','Envy','Rage']:
    A('Chains of '+c, d="A chain attack that appears to have no notable effect.", tgt="AoE")
A('Osmotic Wave', d="Effect not documented.", notes="Metus-exclusive.")
A('Censure', d="Effect not documented.", notes="Metus-exclusive.")

# ---- Cloud of Darkness ----
A('Celling Rupture', d="Conal damage with Bind, Max HP Down, and Knockback.", t="Magical", r="Front cone", tgt="Cone AoE", fx=["Bind","Max HP Down","Knockback"])
A('Destitution', d="Conal damage with Max HP Down and Terror.", t="Magical", r="Front cone", tgt="Cone AoE", fx=["Max HP Down","Terror"])
A('Essence Devour', d="Conal attack that drains HP and MP from a player and lowers all attributes for 30 seconds.", t="Magical", r="Front cone", tgt="Cone AoE", fx=["Drain","All Attributes Down"])
A('Shearing Undulation', d="AoE damage with Defense Down and Magic Defense Down (60s each).", t="Magical", el="Dark", tgt="AoE", fx=["Defense Down","Magic Defense Down"])
A('Primordial Surge', d="AoE that drains HP from all players, then absorbs incoming damage until its next TP move.", tgt="AoE", fx=["Drain"], notes="Head gem glows red while absorbing; deal no damage. Ends with Waning Vigor or Expunge.")
A('Waning Vigor', d="AoE damage scaled by the damage absorbed during Primordial Surge; applies Weakness (15s) to the primary target.", tgt="AoE", fx=["Weakness"], notes="Used after Primordial Surge.")
A('Expunge', d="AoE damage scaled by the damage absorbed during Primordial Surge, plus a full dispel.", tgt="AoE", fx=["Dispel"], notes="Used after Primordial Surge, below 25% HP.")

# ---- Hades / Plouton (shared 12) ----
A('Bane of Tartarus', d="Dispels all buffs including food; the primary target gains ~60s Weakness.", t="Magical", tgt="AoE", fx=["Dispel","Weakness"], notes="Used at 50% HP or below.")
A('Blast of Reticence', d="Damage and Silence.", t="Magical", el="Wind", tgt="AoE", fx=["Silence"], notes="Used below 90% HP.")
A('Ceaseless Surge', d="Damage and Stun.", t="Magical", el="Lightning", tgt="AoE", fx=["Stun"], notes="Used below 90% HP.")
A('Crippling Agony', d="Damage, Bind, and Knockback.", t="Magical", el="Ice", tgt="AoE", fx=["Bind","Knockback"], notes="Used below 90% HP.")
A('Demonfire', d="Damage and Burn (-19/tic).", t="Magical", el="Fire", tgt="AoE", fx=["Burn"], notes="Used below 90% HP.")
A('Ensepulcher', d="AoE damage and Petrification.", t="Magical", el="Earth", tgt="AoE", fx=["Petrification"], notes="Used below 90% HP.")
A('Eternal Misery', d="Damage, ~5-second Zombie, and an enmity reset.", t="Magical", el="Dark", tgt="AoE", fx=["Zombie"], notes="Used at 50% HP or below.")
A('Frozen Blood', d="Damage and Paralysis.", t="Magical", el="Ice", tgt="AoE", fx=["Paralysis"], notes="Used below 90% HP.")
A('Impudence', d="Conal damage, ~5-second Zombie, and an enmity reset.", t="Magical", el="Dark", r="Front cone", tgt="Cone AoE", fx=["Zombie"], notes="Used above 90% HP (the boss uses only this until 90%).")
A('Incessant Void', d="Damage.", t="Magical", tgt="AoE", notes="Used at 50% HP or below. On Hades it grants a Magic Barrier that a stagger removes.")
A('Tenebrous Grip', d="Damage and Blind.", t="Magical", el="Dark", tgt="AoE", fx=["Blind"], notes="Used below 50% HP.")
A('Torrential Pain', d="Damage and dispels 2 enhancements.", t="Magical", el="Water", tgt="AoE", fx=["Dispel"], notes="Used below 90% HP.")

# ---- Provenance Watcher ----
A('Prismatic Breath', d="AoE conal damage plus Inhibit TP (Store TP reduction).", t="Breath", r="Front cone", tgt="Cone AoE", fx=["Inhibit TP"])
A('Acicular Brand', d="AoE damage.", tgt="AoE")
A('Orogenesis', d="AoE damage with Weight, Choke, and Evasion Down.", tgt="AoE", fx=["Weight","Choke","Evasion Down"])
A('Diffractive Break', d="AoE damage with Amnesia, Muddle, and Silence.", tgt="AoE", fx=["Amnesia","Muddle","Silence"])
A('Euhedral Swat', d="High AoE damage and knockback with Attack Down and Defense Down; used when hate is pulled from behind.", tgt="AoE", fx=["Knockback","Attack Down","Defense Down"])
A('Crystallite Shower', d="AoE damage with Dia, Slow, and Addle.", tgt="AoE", fx=["Dia","Slow","Addle"], notes="Stance 2 (two wings open).")
A('Graviton Crux', d="AoE HP drain with random attribute absorb and a partial draw-in; the caster gains temporary Damage Spikes.", tgt="AoE", fx=["Drain"], notes="Stance 2 (two wings open).")
A('Phason Beam', d="AoE damage and Magic Defense Down.", tgt="AoE", fx=["Magic Defense Down"], notes="Stance 3 (four wings open).")
A('Crystal Bolide', d="AoE damage with Terror and Obliviscence (disables sub jobs).", tgt="AoE", fx=["Terror","Obliviscence"], notes="Stance 3 (four wings open).")
A('Fragor Maximus', d="AoE damage that applies Weakness; the caster gains a strong Killer (intimidation) effect for a time.", tgt="AoE", fx=["Weakness"], notes="Stance 3 (four wings open).")

# ---- Shinryu ----
A('Atomic Ray', d="AoE damage and -50% to all attributes. Prevented by cruor buffs.", t="Magical", el="Fire", tgt="AoE", fx=["All Attributes Down"], notes="Used only while wings are spread.")
A('Cataclysmic Vortex', d="AoE that reduces HP to 1 and resets the enmity of the highest-hate player.", tgt="AoE")
A('Cosmic Breath', d="Conal damage with Plague, Attack Down, Magic Attack Down, and Frost. Avoidable by standing to the side.", t="Breath", r="Front cone", tgt="Cone AoE", fx=["Plague","Attack Down","Magic Attack Down","Frost"])
A('Dark Matter', d="20' AoE damage with Terror (15+ seconds).", tgt="AoE", fx=["Terror"])
A('Gyre Charge', d="AoE damage with Paralysis and Knockback.", tgt="AoE", fx=["Paralysis","Knockback"])
A('Mighty Guard', d="Recovers ~15% HP, grants a dispellable 100 TP/tick Regain, and nullifies any damage under 300.", tgt="Self", fx=["Regain"])
A('Supernova', d="20' AoE percentage-based damage with a 10-count Doom.", tgt="AoE", fx=["Doom"], notes="Used below 50% HP while wings are down; not used on Very Easy/Easy.")
A('Protostar', d="20' AoE damage that resets the timers of all its unused abilities.", tgt="AoE", notes="Used below 50% HP while wings are spread.")

# ================= FAMILY =================
d['family_eco']['Supreme Being']='Unclassified'
d.setdefault('family_notes',{})['Supreme Being']=[
  "The Supreme Being family collects the 'deity'-class bosses of Vana'diel \u2014 beings defined only as gods, greater even than the Avatars (the wiki lists the family as Related to: Avatars).",
  "There is no shared resistance profile or kit \u2014 each member (Promathia/Metus, Cloud of Darkness, Hades/Plouton, Provenance Watcher, Shinryu) has its own."
]

def upd(k,**kw):
    v=m[k]
    for kk,vv in kw.items():
        if vv is None: continue
        v[kk]=vv

PROM_KIT=['Empty Salvation','Pestilent Penance','Malevolent Blessing','Infernal Deliverance',
          'Chains of Apathy','Chains of Arrogance','Chains of Cowardice','Chains of Envy','Chains of Rage',
          'Seal of Quiescence','Winds of Oblivion','Bastion of Twilight','Wheel of Impregnability']
HADES_KIT=['Impudence','Blast of Reticence','Ceaseless Surge','Crippling Agony','Demonfire','Ensepulcher',
           'Frozen Blood','Torrential Pain','Bane of Tartarus','Eternal Misery','Incessant Void','Tenebrous Grip']
PW_KIT=['Draw-In','Prismatic Breath','Acicular Brand','Orogenesis','Diffractive Break','Euhedral Swat',
        'Crystallite Shower','Graviton Crux','Phason Beam','Crystal Bolide','Fragor Maximus']
SHIN_KIT=['Draw-In','Atomic Ray','Cataclysmic Vortex','Cosmic Breath','Dark Matter','Gyre Charge','Mighty Guard','Supernova','Protostar']

upd('promathia', nm=True, ab=PROM_KIT, sp=['Comet','Meteor'],
    zones=[['Empyreal Paradox','']],
    drops="Fettering Blade, Venery Bow, Gyve Doublet, Gyve Trousers, Latria Sash, Laic Mantle",
    notes=["Final boss of Chains of Promathia (Mission 8-4: Dawn), fought in the Empyreal Paradox. First form ~8,000 HP; second form ~12,000 HP retains the first-form kit (minus Comet) and adds Meteor, the two shields, and the Mute/Amnesia seals.",
           "You can read its active shield from the ring beneath it: red = physical (Wheel of Impregnability / Invincible), green = magic (Bastion of Twilight / Magic Shield). Title Averter of the Apocalypse; Very Difficult clear adds Dawn's Delight."])

upd('metus', nm=True, ab=PROM_KIT+['Osmotic Wave','Censure'], sp=['Comet','Meteor'],
    zones=[['Empyreal Paradox','']],
    notes=["A copy of Promathia fought during the WotG mission The Winds of Time (Empyreal Paradox); uses Promathia's full kit plus two unique abilities, Osmotic Wave and Censure (effects undocumented)."])

upd('cloud of darkness', nm=True, job='Black Mage',
    st=[['Fire','-40%'],['Wind','-40%'],['Lightning','-40%'],['Light','-30%'],['Ice','-85%'],['Earth','-85%'],['Water','-85%'],['Dark','-95%']],
    ab=['Celling Rupture','Destitution','Essence Devour','Shearing Undulation','Primordial Surge','Waning Vigor','Expunge'],
    sp=['Absorb-Attri','Drain'],
    zones=[['Reisenjima Sanctorium','']],
    drops="Null Loop, Null Masque, Null Belt, Null Shawl",
    img='mobimages/cloud of darkness.png',
    notes=["Final boss of Rhapsodies of Vana'diel (Mission 3-34), fought in Reisenjima Sanctorium (The Orb's Radiance; enter with the Orb of Radiance phantom gem). ~1,300,000 HP (Difficult) to ~1,550,000 (Very Difficult). Title Eternal Master (VD Clear).",
           "Casts elemental magic keyed to the day and the arena's shifting weather (tier III-IV/-ga III above 50%; V/-ga IV/-ja below). Three auto-attack types: AoE damage + knockback, a ranged attack, and a hit that lowers TP by 25%.",
           "Primordial Surge draws players in, drains their HP and begins absorbing physical OR magic damage (its head gem glows red) \u2014 stop damaging it and switch damage types; the phase ends on Waning Vigor, or Expunge below 25%. Up to 10 dark spheres form auras that inflict gravity, slow, addle and paralysis."])

# Hades (second form) + Plouton share the render
upd('hades (second form)', nm=True, job='Black Mage',
    ab=HADES_KIT,
    zones=[['RaKaznar Turris','']],
    img='mobimages/hades (second form).png',
    notes=["Second (winged) form of the Seekers of Adoulin boss Hades (Mission 5-4-1: Abomination), fought in Ra'Kaznar Turris. HP bar is hidden. Its elemental resistances shift after it uses an elemental ability (e.g. after Demonfire it becomes weak to Water). Staggering it removes the Magic Barrier granted by Incessant Void."])

upd('plouton', nm=True, job='Black Mage', lv=[132,132],
    st=[['Fire','-50%'],['Wind','-50%'],['Lightning','-50%'],['Light','-50%'],['Ice','-50%'],['Earth','-50%'],['Water','-50%'],['Dark','-50%']],
    ab=HADES_KIT,
    zones=[['Outer RaKaznar [U1]','132'],['RaKaznar Inner Court','132']],
    drops="Dark Matter, Hades' Claw, Befouled Crown, Incarnation Sash, Odium, Tartarus Platemail",
    img='mobimages/hades (second form).png',
    notes=["The reforged Vagary form of Hades (~660,000 HP), spawned at the Duskbrood Gate ??? in Outer Ra'Kaznar after five skillchain+magic-burst finishers on separate elementals, a 6-step skillchain, and defeating five or more elementals with magic. Warps away if a player is KO'd or if left un-proc'd too long; defeating it extends the time limit 15 minutes. Title Plouton Pincer.",
           "Uses only Impudence until 90% HP, then Incessant Void once (its earring glows) and begins rotating its elemental \u2014 and later physical \u2014 weakness every 10-15%, marked by a cloud animation whose color is the element it currently resists (weak to the element two ascendant from it). Healing it inflicts Encumbrance and, if overdone, triggers Vivisection and a level-up; it builds extreme physical damage reduction if left un-proc'd. At 50% it gains wings and access to Tenebrous Grip, Bane of Tartarus, Eternal Misery and Incessant Void."])

upd('provenance watcher', nm=True,
    ab=PW_KIT,
    zones=[['Provenance','']],
    drops="Plenitas Virga, Sanus Ensis, Adamas, Drachenhorn, Hyaline Hat, Tessera Saio, C.Abjuration: Bd., F.Abjuration: Bd., L.Abjuration: Bd., S.Abjuration: Bd., T.Abjuration: Bd., Meteor, Arise",
    img='mobimages/provenance watcher.png',
    notes=["Voidwatch Notorious Monster of the Crystal Guardian path (~350,000 HP), fought in Provenance; entry needs the Beguiling, Maddening and Seductive petrifact key items (all consumed). As its HP drops it advances through three wing stances that raise its spell tiers and change which weakness triggers apply; on entering the four-wing stance it resets its weakness list.",
           "Physical hits vary by position \u2014 Stun from the front, Paralyze from the rear \u2014 and it uses Draw-In on out-of-range hate. Casting any spell can summon up to three Crystal Fetters (~5,000 HP, stationary, element-matched debuff auras) that cut the damage it takes by ~99%/80%/50% with three/two/one present; each Fetter is vulnerable only to physical or only to magic damage by its element."])

upd('shinryu', nm=True,
    wk=[], st=[['Fire','-40%'],['Wind','-40%'],['Lightning','-40%'],['Ice','-40%'],['Earth','-40%'],['Water','-40%'],['Light','-70%'],['Dark','-70%']],
    ab=SHIN_KIT, sp=['Meteor'],
    zones=[['Abyssea-Empyreal Paradox','']],
    drops="Twilight Cape, Twilight Knife, Twilight Scythe, Twilight Helm, Twilight Mail, Twilight Cloak, Twilight Torque, Twilight Belt, Crepuscular Knife, Crepuscular Scythe, Crepuscular Helm, Crepuscular Mail, Crepuscular Cloak, Crepuscular Pebble, Crepuscular Ring",
    img='mobimages/shinryu.png',
    notes=["The Wyrm God, an Abyssea Notorious Monster fought in Abyssea-Empyreal Paradox (~65,000 HP; ~800,000 on the Very Difficult \u2605 battlefield). Entry needs 10,000 cruor and a Crimson traverser stone. Title Wyrm God Defier.",
           "Swaps between spread and down wings every 3 minutes: while spread it gains Meteor and absorbs damage as it readies a weaponskill or spell; while down it gains Comet, takes 30% less damage, and casts quickly. Below 50% it adds Supernova (wings down) and Protostar (wings spread) and often repeats the same TP move or spell 3-5 times in a row. Its melee swings count as weaponskills for proc/stagger purposes."])

json.dump(d, open('mobs.json','w'), separators=(', ', ': '), ensure_ascii=False)

# guards
d2=json.load(open('mobs.json'))
assert not [k for mob in d2['mobs'].values() for k,v in mob.items() if v is None], 'NULL POISON'
undef=sorted({a for v in d2['mobs'].values() for a in (v.get('ab') or []) if a not in d2['abilities']})
newnames=[k for k in AB]  # names touched this run
mine_undef=[a for a in undef if a in ('Comet','Meteor','Holy','Draw-In')]  # spells shouldn't be in ab
print('abilities:',len(d2['abilities']),'| mobs:',len(d2['mobs']),'| family_eco:',len(d2['family_eco']),'| family_notes:',len(d2.get('family_notes',{})))
print('Supreme Being eco:', d2['family_eco'].get('Supreme Being'))
print('file-wide undefined refs:', len(undef))
for k in ['promathia','metus','cloud of darkness','hades (second form)','plouton','provenance watcher','shinryu']:
    v=d2['mobs'][k]; bad=[a for a in (v.get('ab') or []) if a not in d2['abilities']]
    print('  %-22s ab=%d sp=%s st=%d img=%s undef=%s' % (k,len(v.get('ab') or []),v.get('sp'),len(v.get('st') or []),bool(v.get('img')),bad))
