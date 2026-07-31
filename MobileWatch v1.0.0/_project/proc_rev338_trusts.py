# Builds assets/trusts.json — alter egos grouped by the role their spell icon
# carries on BG-wiki (Tank / Melee Fighter / Ranged Fighter / Caster / Healer /
# Support / Special). One entry per trust; the app renders it as its own page.
#   job / spells / abilities / ws  -> the stat block at the top of the page
#   acq / feat / syn               -> Acquisition, Special Features, Trust Synergy
# Bullet indentation is carried by leading spaces (2 per level).
# Author: BalladOfWorms
import json

T = []


def t(n, role, job, spells, abilities, ws, acq, feat, syn=None):
    e = {"n": n, "role": role, "job": job, "spells": spells,
         "abilities": abilities, "ws": ws, "acq": acq, "feat": feat}
    if syn:
        e["syn"] = syn
    T.append(e)


CIPHER = "Trade the Cipher: {} item to one of the beginning Trust quest NPCs, which may be acquired via:"

t("Amchuchu", "Tank", "Rune Fencer / Warrior",
  ["Flash", "Foil", "Stoneskin", "Refresh", "Phalanx", "Regen I - IV",
   "Protect I - V", "Shell I - V", "Bar-element spells"],
  ["Berserk", "Provoke", "Embolden", "Battuta", "Vallation", "Valiance",
   "Swordplay", "Vivacious Pulse", "Rune Enhancement", "One for All", "Swipe", "Lunge"],
  ["Dimidiation", "Power Slash", "Sickle Moon"],
  [CIPHER.format("Amchuchu"), "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Possesses Inspiration (50% Fast Cast effect during Vallation, is party-wide during Valiance). Converts 5% of Physical Damage Taken to MP.",
   "Only casts enhancing spells on herself.",
   "Uses Embolden when casting Protect.",
   "She can rapidly generate Volatile Enmity for initial threat or recovery from enmity reset attacks with a cornucopia of abilities and spells like Provoke, Flash, and Foil.",
   "Uses Runes resisting the element of the current day. After taking magic damage, uses the appropriate Bar-spell and changes runes.",
   "Uses One for All in response to enemies casting high-tier damaging spells.",
   "Magic Bursts Level 4 Light or Level 4 Darkness skillchains using Lunge.",
   "Berserk could be a risk when using Amchuchu outside of her role as a magic tank.",
   "Holds up to 3000 TP to close skillchains. Weapon skills are a lower priority."])

t("Ark Angel EV", "Tank", "Paladin / White Mage",
  ["Flash", "Phalanx", "Cure I - IV", "Enlight", "Reprisal"],
  ["Chivalry", "Palisade", "Sentinel", "Divine Emblem", "Rampart", "Shield Strike"],
  ["Chant du Cygne", "Vorpal Blade", "Dominion Slash (AoE)", "Arrogance Incarnate (AoE Spirits Within)"],
  [CIPHER.format("Ark Angel EV"),
   "  Complete Dawn and all its cutscenes.",
   "  Be in possession of the Bundle of scrolls key item.",
   "  Have obtained the additional following Trust spells: Rainemard, & Ark Angel GK.",
   "  Speak with Jamal in Ru'Lude Gardens (H-5).",
   "    After trading Ark Angel GK's cipher, speak to Jamal, zone, and speak to Jamal again to unlock the Objective for Cipher: Ark Angel EV. Be sure before zoning Jamal asks you to \"Please come by again later.\"",
   "  Complete the Records of Eminence Objective: Temper Your Arrogance.",
   "    Warp to Tu'Lia \u2192 Ru'Aun Gardens #4 to battle the Ark Angel with a Phantom gem of arrogance on any difficulty.",
   "Players will be unable to receive the alter ego when trading the Cipher if they have not completed the Rhapsodies of Vana'diel mission \"Exploring the Ruins.\" Completing that cutscene/mission will allow the cipher to be traded."],
  ["Possesses Fast Cast, Cure Potency Bonus +50%, Damage Taken -10%, HP+20%, MP+50%, Converts 5% of Damage Taken to MP.",
   "Lacks Provoke; however, AAEV's additional Fast Cast trait reduces the recast time on Flash and Reprisal for solid enmity control.",
   "  Recast times can be improved further by providing Haste.",
   "AAEV has improved Shield stats compared to other trusts, implied by the Nov 2021 Patch Notes. This would also make her Reprisal better.",
   "Ark Angel Elvaan doesn't use any WHM-only spells, but /WHM has Auto-Regen and Magic Defense Bonus, making her a good physical/magical hybrid tank.",
   "Uses Rampart when her target is under the effects of Chainspell, Manafont, or Astral Flow.",
   "Uses Shield Strike to interrupt enemies casting high tier spells.",
   "Holds up to 2000 TP to try to close skillchains.",
   "With two weapon skills that have no skillchain properties, tends to not interrupt skillchains performed by other party members."],
  ["ArkEV / ArkHM / ArkMR / ArkGK / ArkTT: When all 5 Ark Angels are summoned, they possess a Magic Evasion bonus (see: Resist).",
   "  Estimated 240 Magic Evasion, a 50% increase.",
   "  The bonus is a reference to the Accumulative Magic Resistance that was added to counter the strategy of clearing Divine Might with an alliance of Black Mages."])

t("Ark Angel HM", "Tank", "Ninja / Warrior",
  ["Migawari: Ichi", "Utsusemi: Ichi/Ni", "Hojo: Ichi/Ni", "Kurayami: Ichi/Ni"],
  ["Innin", "Yonin", "Provoke", "Berserk", "Warcry"],
  ["Chant du Cygne", "Swift Blade", "Cross Reaver (Unique Conal Stun)"],
  [CIPHER.format("Ark Angel HM"),
   "  Complete Dawn and all its cutscenes.",
   "  Be in possession of the Bundle of scrolls key item.",
   "  Have obtained the additional following Trust spells: Rainemard, Ark Angel GK, Ark Angel EV, Ark Angel MR, & Ark Angel TT.",
   "  Speak with Jamal in Ru'Lude Gardens (H-5).",
   "    After trading Ark Angel TT's cipher, you must speak to Jamal, zone, and speak to Jamal again to unlock the Objective for Cipher: Ark Angel HM. Be sure before zoning Jamal asks you to \"Please come by again later.\"",
   "    You may need to zone in again if you haven't talked to him since trading Ark Angel TT's cipher in order for him to unlock the Objective.",
   "  Complete the Records of Eminence Objective: Eliminate Your Apathy.",
   "    Warp to Tu'Lia \u2192 Ru'Aun Gardens #1 to battle the Ark Angel with a Phantom gem of apathy on any difficulty.",
   "Players will be unable to receive the alter ego when trading the Cipher if they have not completed the Rhapsodies of Vana'diel mission \"Exploring the Ruins.\" Completing that cutscene/mission will allow the cipher to be traded."],
  ["Possesses HP+20%.",
   "Possesses an Utsusemi +1 trait which grants AA HM an extra shadow.",
   "If there is a NIN, PLD, or RUN in the party, behaves as a damage dealer: Uses Innin, Berserk.",
   "If there are no other tanks in the party, behaves as a tank: Uses Yonin, Warcry.",
   "Uses Provoke in both situations in order to sub tank.",
   "Casts debuffs when does not have hate.",
   "Starts fights with Migawari if available.",
   "Uses weapon skills at 1000 TP and does not try to skillchain."],
  ["ArkEV / ArkHM / ArkMR / ArkGK / ArkTT: When all 5 Ark Angels are summoned, they possess a Magic Evasion bonus (see: Resist).",
   "  Estimated 240 Magic Evasion, a 50% increase.",
   "  The bonus is a reference to the Accumulative Magic Resistance that was added to counter the strategy of clearing Divine Might with an alliance of Black Mages."])

t("August", "Tank", "Paladin / Warrior",
  ["Cure I - IV", "Flash", "Holy II", "Reprisal"],
  ["Sentinel", "Provoke", "Divine Emblem", "Palisade", "Daybreak (Wings)"],
  ["Neutral: Alabaster Burst, Null Field, Tartaric Sigil",
   "Daybreak: Fulminous Fury, Noble Frenzy, No Quarter"],
  [CIPHER.format("August"), "  Sinister Reign", "  Mog Pell (Ochre)",
   "  Records of Eminence Quest Way Over Capacity"],
  ["Possesses HP+10%.",
   "Uses Divine Emblem to enhance Holy II.",
   "August's attacks are not affected by Sambas.",
   "August automatically applies all Killer Effects and high resistance to Terror.",
   "August wears the Founder's Gear and has significantly less damage.",
   "He can switch weapons at will while auto attacking and performing weapon skills; it is unknown if this changes his damage type or is merely cosmetic.",
   "He has been observed wielding H2H, Dagger and Axe, Bow (Auto Attacks), Great Axe and Scythe (Alabaster Burst), Great Sword (Tartaric Sigil), Dual Katanas and Great Katana (Noble Frenzy), Club and Staff (Fulminous Fury), and Flute (Daybreak) in addition to his default Sword and Shield.",
   "August is considered to be wielding a Great Sword for the purposes of Damage Limit+ and Inundation.",
   "Uses weapon skills at 1000 TP and does not try to skillchain.",
   "Daybreak (~3 min cooldown, ~1 min 30 sec duration):",
   "  When August's HP drops below a certain threshold (~66%), he uses Daybreak if it's available which partially restores some HP and MP, resets his TP, and activates an aura with wings of light.",
   "  Daybreak is a -50% PDT effect, full Erase, Stats boost, Regen, and Store TP.",
   "  During Daybreak, August's next weapon skill will be Fulminous Fury or Noble Frenzy, followed by No Quarter.",
   "  Daybreak is removed after the use of No Quarter.",
   "  Daybreak's cooldown may start when No Quarter is used (meaning it's about a 1.5 min cooldown)."])

t("Curilla", "Tank", "Paladin / Paladin",
  ["Cure I - IV", "Flash"],
  ["Sentinel"],
  ["(5) Red Lotus Blade", "(25) Seraph Blade", "(50) Swift Blade", "(60) Vorpal Blade"],
  ["Complete the initiation quest in San d'Oria.",
   "Must be Rank 3 or higher in any nation.",
   "  Speak with Curilla in Chateau d'Oraguille at (I-9)."],
  ["Possesses MP+30%, Guardian (Sentinel enmity loss -95%), Sentinel Recast merited (-50 sec), Cure Potency Bonus +25%, and Cure Casting Time Down.",
   "Does not use Provoke, but will use Flash. This leads to poor hate control.",
   "Uses TP randomly and does not try to skillchain.",
   "Cures players and trusts in yellow (<75%) HP."],
  ["Curilla: Rainemard casts Phalanx II (unlocked at level 75) only on Curilla and himself. His Phalanx, like his Enspells, also appears to benefit from his extremely high enhancing magic skill; his Phalanx II is -35 damage."])

t("Gessho", "Tank", "Ninja / Warrior",
  ["Utsusemi: Ichi/Ni", "Hojo: Ichi/Ni", "Kurayami: Ichi/Ni"],
  ["Provoke", "Yonin", "Shiko no Mitate (Yagudo Parry)", "Rinpyotosha (Yagudo Howl: Attack Boost)"],
  ["Happobarai (Yagudo Sweep)", "Hane Fubuki (Feather Storm)", "Shibaraku (AoE)"],
  ["Complete Passing Glory.", "  Examine the cushion in Aht Urhgan Whitegate (J-12)."],
  ["Will only use the highest tier debuff available, but will use both Utsusemi spells.",
   "Will maintain Yonin full time.",
   "Greatly benefits from capping magical haste as it will allow for better maintenance of Utsusemi shadows.",
   "Holds TP until 1500 to try to close skillchains.",
   "Gessho is a good tank choice for players trying to avoid Light-based damage since his weapon skills won't accidentally open Light skillchains.",
   "Special abilities:",
   "  Shiko no Mitate: Defense Boost + Stoneskin + Issekigan",
   "  Rinpyotosha: Party members gain a 3 minute Attack Boost (+25% Attack) effect. 5 minute cooldown."])

t("Mnejing", "Tank", "Paladin / Paladin \"Valoredge\"",
  [],
  ["Strobe I - II (Provoke)", "Shield Bash (Stun)", "Disruptor (Dispel)", "Flashbulb (Flash)"],
  ["Chimera Ripper", "String Clipper", "Shield Subverter (Conal AoE, Silence)"],
  [CIPHER.format("Mnejing"), "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Passive -37.5% Damage Taken Reduction.",
   "Possesses lower HP than most tanks, but takes significantly less damage.",
   "Possesses a moderate amount of MP, despite the fact he cannot use magic.",
   "Possesses Barrier Module (Increased Block Chance, Shield Mastery).",
   "Mnejing will hold up to 1500 TP to close skillchains; however, he will not always choose to close with a weapon skill which will create the highest tier skillchain possible.",
   "  (i.e. he will sometimes use Chimera Ripper to skillchain with Savage Blade to create a tier 1 skillchain instead of Savage Blade to create a tier 3 skillchain)",
   "Mnejing tries to interrupt TP abilities with Shield Bash.",
   "Mnejing will Flash its target using the Flashbulb (Mnejing's Flash generates considerable enmity).",
   "Mnejing can use the effects of his attachments (Strobe, Barrier Module, Flashbulb, and Disruptor) despite not having any maneuvers effects.",
   "Mnejing's Disruptor Dispel is highly accurate and he will use it against enemies others will not attempt to dispel due to M.ACC."],
  ["Nashmeira: Mnejing receives increased defense (+10%) and increased enmity (+10%) (not compatible with Nashmeira II)."])

t("Rahal", "Tank", "Paladin / Warrior",
  ["Cure I - IV", "Flash", "Phalanx", "Enlight"],
  ["Sentinel", "Berserk", "Provoke", "Shield Bash"],
  ["Fast Blade", "Seraph Blade", "Swift Blade", "Savage Blade"],
  [CIPHER.format("Rahal"), "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Possesses Dragon Killer.",
   "Rahal is an aggressive tank who uses Berserk.",
   "Prioritizes Flash over Provoke.",
   "Will only cast Cure when a party member is below 33% health and will use the highest tier available.",
   "Will only use Sentinel when he is below 33% health.",
   "He tries to interrupt TP abilities and high-tier spells with Shield Bash.",
   "Holds up to 2500 TP to close skillchains."])

t("Rughadjeen", "Tank", "Paladin / Paladin",
  ["Holy", "Flash", "Cure I - IV", "Raise"],
  ["Sentinel", "Divine Emblem", "Holy Circle", "Chivalry"],
  ["Power Slash", "Sickle Moon", "Ground Strike", "Victory Beacon (Conal AoE)"],
  [CIPHER.format("Rughadjeen"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Possesses Fast Cast, Cure Potency Received +30%, Damage Taken -5%, HP+20%, MP+20%.",
   "He wields the Algol and so has an enfire effect and a 3% triple attack rate.",
   "Uses Holy Circle if the enemy is Undead.",
   "Will only cast Cure I - IV when a party member is below 75% (yellow) HP or asleep.",
   "Tries to use weapon skills at 1000 TP, but it is lower priority.",
   "Uses Chivalry at 50% MP if it's available.",
   "Will cast Raise on KO'd party members in casting range."],
  ["Mihli Aliapoh / Gadalar / Zazarg / Najelith: Rughadjeen empowers the other serpent generals.",
   "  Mihli Aliapoh gains +25% Cure Potency increase.",
   "  Gadalar gains +25 Magic Attack Bonus. For a total +90 MAB at level 99 (+40 BLM job traits, +25 Gadalar trait, +25 Synergy).",
   "  Najelith gains +40 ranged accuracy and enhanced Barrage accuracy.",
   "  Zazarg gains ~5-15% damage.",
   "When any other serpent generals are in the party, Rughadjeen has Damage Taken -29% while in combat with a foe."])

t("Trion", "Tank", "Paladin / Warrior",
  ["Cure I - IV", "Flash"],
  ["Provoke", "Sentinel"],
  ["Red Lotus Blade", "Savage Blade", "Royal Bash (Shield Bash)", "Royal Savior (Palisade, Sentinel, Stoneskin)"],
  ["Complete the initiation quest in San d'Oria.",
   "Must be Rank 6 or higher in any nation.",
   "  Examine the \"Door: Prince Royal's Room\" in Chateau d'Oraguille at (H-7)."],
  ["Royal Bash is stronger than a normal Shield Bash. Royal Saviour is a secondary, stronger version of Sentinel. Trion alternates between this and the normal version of Sentinel.",
   "Trion tries to interrupt TP abilities with Royal Bash.",
   "Uses TP randomly and does not try to skillchain.",
   "With his two defensive TP moves, he's not likely to interrupt skillchains much."],
  ["Pieuje (UC) only uses Regen when healing his brother Trion."])

t("Valaineral", "Tank", "Paladin / Warrior",
  ["Cure I - IV", "Flash", "Protect IV - V", "Reprisal", "Enlight", "Phalanx"],
  ["Provoke", "Sentinel", "Majesty", "Defender", "Fealty", "Divine Emblem", "Chivalry", "Palisade", "Rampart"],
  ["Circle Blade", "Sanguine Blade", "Savage Blade", "Uriel Blade (AoE)"],
  [CIPHER.format("Valaineral"),
   "  Records of Eminence: Basic Tutorial Objective Reward",
   "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Possesses Enmity+, Cure Potency Bonus+50%, Spell interruption rate decrease, Refresh+ (+3mp/tick Auto Refresh, stacks with PLD trait), and Damage Taken -8%, HP+10%, MP+20%.",
   "Uriel Blade can be used under 1000 TP based on certain conditions, making him excellent at engaging multiple targets. He can even use it when engaging a single target and any time the player draws enmity. This makes him a good SC opener for Ark Angel GK, who can use that to close Light SCs right after engaging an enemy with no TP requirement for either of them.",
   "Very powerful at low levels due to his special ability letting him use Uriel Blade before he has access to it as a normal weapon skill (lv.50).",
   "Casts Protect spells on himself under the effect of Majesty with the added defense of Shield Barrier (defense varies by iM, up to 350), but does not attempt to overwrite other Protect effects even if he would gain more defense from doing so.",
   "Uses Divine Emblem before casting Flash if it is available.",
   "Rampart will be used when his target is under the effects of Chainspell, Manafont, or Astral Flow.",
   "  Against SMNs, Rampart trigger seems to be based on whether there's an avatar summoned. Certain Tonberry NMs have a Light Spirit or their avatar appears after Astral Flow, which could explain why Rampart didn't trigger.",
   "Fealty can be used under certain conditions including anticipating Mijin Gakure and negating its damage.",
   "Uses weapon skills randomly around 2000 TP and does not try to skillchains."])

ROLES = ["Tank", "Melee Fighter", "Ranged Fighter", "Caster", "Healer", "Support", "Special"]
out = {"roles": ROLES, "trusts": sorted(T, key=lambda x: x["n"])}
path = "/home/claude/android/app/src/main/assets/trusts.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, separators=(", ", ": "))

import collections
print("trusts:", len(T), collections.Counter(x["role"] for x in T))
bad = [x["n"] for x in T if x["role"] not in ROLES]
print("bad roles:", bad)
