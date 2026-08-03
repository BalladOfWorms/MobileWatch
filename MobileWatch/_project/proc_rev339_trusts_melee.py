# Rev 339 — adds the MELEE FIGHTER role to assets/trusts.json (61 alter egos),
# transcribed from the BG-wiki "Alter Egos In-Depth" boxes. Loads the existing file
# and appends, so the Tank batch from rev 338 is preserved.
# Author: BalladOfWorms
import json, collections

PATH = "/home/claude/android/app/src/main/assets/trusts.json"
d = json.load(open(PATH, encoding="utf-8"))
T = []

CIPHER = "Trade the Cipher: {} item to one of the beginning Trust quest NPCs, which may be acquired via:"
RHAP = ("Players will be unable to receive the alter ego when trading the Cipher if they have not "
        "completed the Rhapsodies of Vana'diel mission \"Exploring the Ruins.\" Completing that "
        "cutscene/mission will allow the cipher to be traded.")
ARK = ["ArkEV / ArkHM / ArkMR / ArkGK / ArkTT: When all 5 Ark Angels are summoned, they possess a Magic Evasion bonus (see: Resist).",
       "  Estimated 240 Magic Evasion, a 50% increase.",
       "  The bonus is a reference to the Accumulative Magic Resistance that was added to counter the strategy of clearing Divine Might with an alliance of Black Mages."]
ALZ = ["Aldo / Lion / Zeid: When two or three of them are in a party together, they gain a power boost from each of the others in the party.",
       "  Aldo gains an \"enhances Dual Wield effect\" bonus (Requires level 20 or greater). Adds a chance for extra attacks instead of reducing delay: his TP gain is still multiples of 50 (similar to the Hattori Garb Set).",
       "  Lion gains an attack speed increase ~6%/~12%.",
       "  Zeid gains an attack bonus ~10%/~20%."]
MUMOR_UKA = ["Mumor / Uka Totlihn: By summoning them both at the same time, the stats of the abilities they use will increase.",
             "  Mumor gains ~10% enhanced samba duration. (Stacks with Saber Dance: 108s -> 120s)",
             "  Uka gains ~10% enhanced waltz potency. (Curing Waltz V: 1067 HP -> 1173 HP)"]
DARR_MORI = ["Morimar: Darrcuiln and Morimar will use TP moves more often when summoned together.",
             "  Darrcuiln will use TP moves with 1000 TP, regardless of whether Morimar is ready to complete a skillchain or not.",
             "  Note: If Morimar's aura is up, Darrcuiln behaves normally and saves its TP until 1500-2000."]
UNITY = ["Be a member of the {} Unity Concord.",
         "  Obtain 5000 Unity Accolades through Records of Eminence objectives for a Partial Personal Evaluation of Spt."]
TWELVE = ("Notice: Acquiring this trust is a long process of 12 quests; many of which have \"a game day "
          "of waiting\" between them. Setting aside a good amount of time is advised to see this done.")
MANDY = ("Summoning, Dismiss and death text can only be understood if the summoner is wearing (or "
         "lockstyled) mandragora costume gear (Mandragora Suit and Mansque, etc).")
SPECIAL_MOVES = ("Since his attacks are special moves, he does not benefit from Sambas or Haste, but "
                 "likewise is not affected by Slow or Spikes.")
HASTE_SAMBA = ("Uses Haste Samba when another party member is on a main job with access to Cure "
               "(WHM, RDM, SCH, PLD) or when the enemy is undead, otherwise uses Drain Samba.")


def unity(name):
    return [UNITY[0].format(name), UNITY[1]]


def t(n, job, spells, abilities, ws, acq, feat, syn=None):
    e = {"n": n, "role": "Melee Fighter", "job": job, "spells": spells,
         "abilities": abilities, "ws": ws, "acq": acq, "feat": feat}
    if syn:
        e["syn"] = syn
    T.append(e)


t("Abenzio", "Monk / Warrior", [], [],
  ["Blank Gaze (Conal paralysis)", "Antiphase (AoE silence)", "Uppercut", "Blow (Damage + Stun)"],
  [CIPHER.format("Abenzio"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Possesses HP+20%.",
   "Abenzio's job is Monk unlike most Goobbue, which are Warriors.",
   "  He has the normal MNK/WAR traits, but he does use Kick Attacks with his arm vines because Goobbue don't have a kick animation.",
   "Possesses a monstrous Max HP Boost among other Job Traits, but doesn't use Job Abilities.",
   "As a Plantoid, he intimidates beasts, is intimidated by vermin, and is subject to Plantoid Killer.",
   "Uses TP randomly and does not try to skillchain.", MANDY])

t("Abquhbah", "Warrior / Monk", [], ["Berserk", "Warcry", "Restraint"],
  ["Combo", "Backhand Blow", "Salaheem Spirit"],
  ["Trade the Cipher: Abquhbah item to one of the beginning Trust quest NPCs, which may be acquired by talking with Abquhbah in Aht Urhgan Whitegate (I-10) after completion of:",
   "  Complete President Salaheem.", "  Complete Ever Forward."],
  ["Salaheem Spirit:",
   "  All nearby party members receive a +24 bonus to all base attributes, i.e.: STR, DEX, etc. (Bonuses degrade over time: about a rate of -1 per tick. Usually +13 to +16 left when the effect ends based on initial duration.)",
   "  Duration is based on TP (~70 seconds @1500 TP, ~90 seconds @2000 TP, 120 seconds @3000 TP).",
   "  Salaheem Spirit's attribute bonus seems to be determined by your level + 4 (+18 @ level 72, +24 @ level 99).",
   "Holds up to 1500 TP to try to close skillchains.",
   "When not able to close a skillchain, uses Berserk + Warcry + random weapon skill.",
   "Without any conditions to increase Salaheem Spirit usage: maintaining the bonus is up to luck. External TP Bonuses and TP gain rate increases (Regain/Haste/Store TP/Double Attack) can help."])

t("Aldo", "Thief / Ninja", [], ["Bully", "Sneak Attack", "Assassin's Charge"],
  ["Lock and Load", "Shockstorm Edge (AoE)", "Iniquitous Stab", "Choreographed Carnage"],
  [CIPHER.format("Aldo"), "  Adventurer Appreciation Campaigns", "  Mog Pell (Ochre)", "  Mog Pell (Red)"],
  ["Possesses THF/NIN traits, limited to Treasure Hunter I.",
   "Holds up to 2000 TP in order to close skillchains. If he's not able to close a skillchain, will use Assassin's Charge in combination with the WS.",
   "Can be made to spam Shockstorm Edge (to close) by opening with a Weapon Skill that leaves no alternative (like Cyclone).",
   "Lock and Load is a marksmanship weapon skill, which Aldo seems to have a lower proficiency in since this weapon skill misses more often than others.",
   "Uses Sneak Attack regardless of positioning and does not try to combine it with weapon skills.",
   "  Will use Bully before Sneak Attack (to remove the directional requirement on Sneak Attack), so try readying a skillchain when you see Aldo use Bully.",
   "  Sneak Attack does not work on ranged or magic weapon skills.",
   "Gains TP quickly with Dual Wield and Triple Attack trait: 50 TP/hit x2."], ALZ)

t("Aldo (UC)", "Thief / Ninja", [], ["Bully", "Sneak Attack"], ["(50) Sarva's Storm"],
  unity("Aldo"),
  ["Possesses 5/5 Triple Attack Rate merits at lv75.",
   "Excellent skillchain partner with thieves using Rudra's Storm.",
   "Uses Sneak Attack when behind the target or after using Bully, but does not try to combine it with weapon skills.",
   "Uses Sarva's Storm whenever another party member has 1000 TP in order to open skillchains.",
   "If no other party members gain TP, will use Sarva's Storm at 3000 TP."])

t("Areuhat", "Warrior / Paladin", [], ["Aggressor", "Berserk", "Blood Rage"],
  ["Seraph Blade", "Vorpal Blade", "Savage Blade", "Hurricane Wing (AoE)", "Dragon Breath (Conal AoE)"],
  [CIPHER.format("Areuhat"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Possesses enhanced Blood Rage duration (60s duration, 5m cooldown).",
   "Areuhat is capable of wielding TP attacks commonly employed by wyrms.",
   "Even in her Elvaan form, she is susceptible to Monster Correlation: she can intimidate Demons and be intimidated by them in turn.",
   "She waits for Warcry effects to expire before using Blood Rage, but it will sometimes be immediately overwritten by other Warrior trusts using Warcry at the same time she casts Blood Rage since they tend to have the same buffing logic.",
   "Holds up to 2000 TP to close skillchains."])

t("Ark Angel GK", "Samurai / Dragoon", [],
  ["Hasso", "Konzen-ittai", "Hagakure", "Meditate", "Sekkanoki", "Jump", "High Jump"],
  ["Tachi: Fudo", "Tachi: Gekko", "Tachi: Kasha", "Tachi: Yukikaze", "Dragonfall (AoE Damage + Bind)"],
  [CIPHER.format("Ark GK"),
   "  Complete Dawn and all its cutscenes.",
   "  Complete Awakening and all its cutscenes.",
   "  Be in possession of the Bundle of scrolls key item.",
   "  Have obtained the additional following Trust spells: Rainemard.",
   "  Speak with Jamal in Ru'Lude Gardens (H-5).",
   "  Complete the Records of Eminence Objective: Quell Your Rage.",
   "    Warp to Tu'Lia \u2192 Ru'Aun Gardens #5 to battle the Ark Angel with a Phantom gem of rage on any difficulty.",
   RHAP],
  ["Possesses HP+20%.",
   "Occasionally able to use Weapon Skills without consuming TP. Can do this to close Skillchains under 1000 TP or to use Dragonfall twice at high TP.",
   "  There is a short delay before he can use it again.",
   "Has a high TP return on Jump (790 TP), uses it at low TP.",
   "Uses High Jump when in the top enmity slot.",
   "He will use Konzen-ittai if available when the player has 1000 TP but he does not. Never tries to close a Skillchain with it.",
   "Holds up to 3000 TP to try to close skillchains.",
   "If Sekkanoki and Meditate are available, self-skillchains at 2000 TP."], ARK)

t("Ark Angel MR", "Beastmaster / Thief", [], ["Sneak Attack", "Trick Attack"],
  ["Cloudsplitter", "Calamity", "Rampage", "Havoc Spiral (AoE)"],
  [CIPHER.format("Ark MR"),
   "  Complete Dawn and all its cutscenes.",
   "  Be in possession of the Bundle of scrolls key item.",
   "  Have obtained the additional following Trust spells: Rainemard, Ark Angel GK, & Ark Angel EV.",
   "  Speak with Jamal in Ru'Lude Gardens (H-5).",
   "    After trading Ark Angel EV's cipher, you must speak to Jamal, zone, and speak to Jamal again to unlock the Objective for Cipher: Ark MR. Be sure before zoning Jamal asks you to \"Please come by again later.\"",
   "  Complete the Records of Eminence Objective: Stifle Your Envy.",
   "    Warp to Tu'Lia \u2192 Ru'Aun Gardens #3 to battle the Ark Angel with a Phantom gem of envy on any difficulty.",
   RHAP],
  ["Possesses HP+20%, BST/THF Traits except TH is limited to Treasure Hunter I.",
   "Will Sneak Attack + Weapon Skill if behind the enemy.",
   "Will Trick Attack + Weapon Skill if behind a player or trust.",
   "If conditions for both are possible will Sneak Attack + Trick Attack + Weapon Skill.",
   "AAMR's Cloudsplitter can deal massive damage (~8000+) at ilvl119.",
   "Rarely ever uses Havoc Spiral which does AoE damage (~100-300) and Additional Effect: Sleep.",
   "Uses weapon skill as soon as Sneak Attack or Trick Attack are possible with 1000+ TP: favoring Calamity.",
   "When in front of the target without Trick Attack, uses weapon skill with 1000+ TP: favoring Cloudsplitter.",
   "Holds TP up to 3000 to wait for the previously mentioned conditions, does not try to skillchain."], ARK)

t("Ayame", "Samurai / Samurai", [], ["Meditate", "Hasso", "Third Eye"],
  ["(1) Tachi: Enpi", "(9) Tachi: Hobaku", "(23) Tachi: Goten", "(33) Tachi: Kagero",
   "(49) Tachi: Jinpu", "(55) Tachi: Koki", "(60) Tachi: Yukikaze", "(65) Tachi: Gekko",
   "(71) Tachi: Kasha"],
  ["Complete the initiation quest in Bastok.",
   "Must be Rank 3 or higher in any nation.",
   "  Speak with Ayame in Metalworks at (K-7)."],
  ["Skillchains:",
   "  Once the player uses a Weapon Skill with Ayame summoned, she will hold off using weapon skills until the player has 1000 or more TP.",
   "  This helps to open the highest level Skillchain possible determined by the previously used weapon skill.",
   "    She can open Light or Darkness skillchains to be closed by weapon skills with Fragmentation or Gravitation properties.",
   "  Ayame will always try to open a Skillchain rather than close it.",
   "  She will use Weapon Skills regardless how much HP is remaining on the current monster.",
   "  Holds TP until 3000 to open skillchains for the player.",
   "Uses Meditate, when the ability is ready, in situations where the player has TP but she does not.",
   "Only uses Third Eye when she pulls hate."])

t("Ayame (UC)", "Samurai / Warrior", [],
  ["Blade Bash", "Sengikori", "Hasso", "Third Eye", "Shikikoyo", "Meditate"],
  ["(5) Tachi: Jinpu", "(25) Tachi: Koki", "(50) Tachi: Mudo", "(60) Tachi: Kasha", "(70) Tachi: Ageha"],
  unity("Ayame"),
  ["Possesses 5/5 Shikikoyo merits at level 75 (shared TP +48%).",
   "Skillchains:",
   "  Specializes in two-person 3-step or 5-step skillchains with the player, resulting in higher Skillchain damage and Magic Burst Damage Bonus with each step.",
   "  Completes skillchains while using Sengikori if ready.",
   "  Only closes skillchains started by the player (or their pet). Waits at 3000 TP until conditions are met.",
   "  Always closes a higher level skillchain, ignores the skillchain if she can't.",
   "  Due to the weapon skills available, cannot close skillchains started with Distortion or Fusion.",
   "  Does not close Level 4 Light skillchains, Tachi: Mudo is only used to close Darkness.",
   "  Always chooses Tachi: Ageha following a Detonation opener.",
   "  Level 1 Chainbound (Status) will be closed by Tachi: Koki for Fragmentation.",
   "  Abilities are used based on skillchain level and battle condition, so she may Meditate before a weaponskill instead of waiting for you to reach 1000 TP.",
   "Ayame's consistent weapon skill choice and timing make her a good choice for parties who want to set up magic bursts of a specific element boosted by Sengikori (+25% Magic Burst Damage).",
   "High TP gain rate with Hasso/Zanshin and >250 TP per hit depending on level of SAM Store TP trait.",
   "Tachi: Ageha is the 2015 version.",
   "  Defense Down could mean more TP and Magic Accuracy than the player's version to land on high-level enemies.",
   "  Trust weapon skills have different IDs than the ones players use and have a separate implementation.",
   "When she has 2000+ TP, she uses Shikikoyo on the party leader after they use a weapon skill.",
   "  After summoning Ayame, if she reaches 2000 TP before the party leader has used a weapon skill, uses Shikikoyo immediately.",
   "If she gets hate, uses Third Eye.",
   "Stuns enemies with Blade Bash, only to interrupt spellcasting."])

t("Babban Mheillea", "Monk / Monk", [], [],
  ["Wild Oats", "Headbutt", "Photosynthesis (Grants Regen)", "Petal Pirouette (Resets foe's TP to zero) (AoE)"],
  [CIPHER.format("Babban"), "  Sunshine Seekers event (300 tiny seeds)", "  Mog Pell (Ochre)"],
  ["Possesses Job Traits but no Job Abilities. HP-10%.",
   "Guards and Counters melee attacks directed at her.",
   "As a Plantoid, she is subject to Plantoid Killer (intimidated by Vermin).",
   "Uses TP randomly and does not try to skillchain.",
   "Has a large HP pool common to non-humanoids.",
   "Petal Pirouette normally reduces enemy TP to 0, but it has a reduced effect on NMs: enemy's remaining TP will be written in the log.",
   "Photosynthesis will only be used during daytime (6:00-18:00).", MANDY])

t("Balamor", "Dark Knight / Black Mage", ["Absorb-STAT spells"], [],
  ["Feast of Arrows", "Last Laugh (Drain HP)", "Regurgitated Swarm", "Setting the Stage"],
  [CIPHER.format("Balamor"), "  Complete Pretender to the Throne."],
  ["Possesses HP+40%, MP+100%.",
   "Is Undead so he takes damage from Cure spells and cannot be healed by Curing Waltzes or Divine Waltz.",
   "  Regen spells, Indi-Regen, Blue Magic, and curative Blood Pacts all can heal him.",
   "Immune to Drain type spells and drain effects from TP moves such as Blood Saber but can still be damaged by them.",
   "Can use Last Laugh to drain HP from enemies.",
   "Uses TP randomly and does not try to skillchain.",
   "Auto-attack is dark elemental magic damage. May appear to be AoE even though it is not.",
   "  Since his attacks are special moves, he does not benefit from Sambas or Haste, but likewise is not affected by Slow or Spikes."])

t("Chacharoon", "Thief / Ranger", [], [],
  ["Sharp Eye (Conal)", "Tripe Gripe", "Pocket Sand (Conal)"],
  ["Complete Trial of the Chacharoon."],
  ["Possesses HP-10%, MP-10%.",
   "Very low delay, but also has relatively low base damage.",
   "Occasionally performs a throwing ranged attack on the enemy.",
   "Chacharoon's Sharp Eye resembles a Gaze attack but it has no directional requirement.",
   "The status effects Chacharoon applies could be used in kiting or evasion strategies.",
   "  The effect may be difficult to land on higher level enemies.",
   "  Gravity and Defense Down are wind-based status effects.",
   "  If half-resisted, duration will be halved.",
   "Uses weapon skills at 1000 TP.",
   "Tripe Gripe and Sharp Eye do not deal damage, only applying status effects:",
   "  Tripe Gripe applies Amnesia (30s) and Attack Boost effects to an enemy.",
   "  Sharp Eye applies Gravity II (60s) and 25% Defense Down (30s or 60s). The Defense Down effect will show in the log when Gravity is fully resisted.",
   "  Pocket Sand applies Blind (up to -50 Accuracy, 60s) and deals damage."],
  ["Zeid / Zeid II: Zeid can Absorb-Attri to steal the attack bonus granted by Chacharoon's Tripe Gripe."])

t("Cid", "Warrior / Ranger", [], ["Berserk", "Aggressor"],
  ["True Strike", "Hexa Strike", "Fiery Tailings (AoE)", "Critical Mass"],
  [CIPHER.format("Cid"), "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Both melees and shoots.",
   "Uses Aggressor hopefully augmented with Aggressive Aim merits.",
   "Saves up to 2500 TP waiting to close a skillchain.",
   "Will save Berserk until he is about to use a weapon skill."])

t("Darrcuiln", "Warrior / Red Mage \"Beast\"", [], [],
  ["Howling Gust", "Starward Yowl", "Righteous Rasp", "Aurous Charge", "Stalking Prey (AoE)"],
  [CIPHER.format("Darrcuiln"), "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Possesses HP+~42%.",
   "Has several auto-attack animations. Although none can miss, only the roar appears to do magic damage (element unknown). He will exclusively roar if the monster is out of range.",
   SPECIAL_MOVES,
   "Has a large HP pool common to non-humanoids.",
   "Can treat as a Warrior for job interaction purposes (buffs/behaviors of other trusts).",
   "Holds TP randomly between 1500-2000, but does not attempt to close skillchains."], DARR_MORI)

t("Excenmille", "Paladin / Paladin", ["Flash", "Cure I - IV"], ["Sentinel"],
  ["Double Thrust", "Leg Sweep", "Penta Thrust"],
  ["Complete the initiation quest in San d'Oria."],
  ["Uses TP randomly and does not try to skillchain.",
   "Uses Sentinel and Flash on cooldown for enmity.",
   "Casts Cure on party members in orange HP (<50%).",
   "Prioritizes healing if there is no WHM in the party.",
   "  Cure threshold changes to party members under <75%."])

t("Excenmille (S)", "Warrior / Paladin", [], ["Stag's Call"],
  ["Songbird Swoop", "Gyre Strike (Paralyze)", "Orcsbane (AoE)", "Stag's Charge"],
  [TWELVE + " The starting quest = Gifts of the Griffon and you don't need to be allied to San d'Oria (S) in order to start or obtain this trust.",
   "Be in possession of the Bundle of scrolls key item.",
   "  Complete Face of the Future which is the end of the 12 quest process.",
   "  Speak with Rholont in Southern San d'Oria (S) (E-7)."],
  ["Stag's Call is an AoE Haste +15%, Attack +15%, and MAB +15 buff which lasts for 3 minutes (recast is 5 minutes).",
   "  The attack buff does not overwrite Nature's Meditation.",
   "  The Haste buff is overwritten by Haste and Haste II. Other trust alter egos will cast over it.",
   "Uses weapon skills at 1000 TP."])

t("Fablinix", "Thief / Red Mage", ["Stun", "Enwater", "Cure I - IV"], [],
  ["Bomb Toss (AoE)", "Goblin Rush"],
  [CIPHER.format("Fablinix"), "  Adventurer Appreciation Campaigns", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Possesses MP+250%.",
   "Occasionally uses his crossbow in addition to dagger melee attacks. The long ranged attack delay can cause him to miss Stun opportunities.",
   "Casts Stun to interrupt enemy TP moves.",
   "Uses Cure spells on party members in orange HP (<50%) or asleep, with higher priority for the tank (<75%).",
   "Holds up to 1500 TP in order to close skillchains.",
   "Fablinix's high MP pool and access to Stun at the BLM level (lv.42) may give the impression that he is a BLM who has multiple main jobs. However, if you use him in an area with subjob restrictions he will have 0 MP. If you give him at least +8MP through AoE Food (before applying his +350%) or by raising your item level, he will still be able to cast Stun but none of the other spells. He might have a different version of Stun than players, which may explain reports of his Stun recast being shorter."])

t("Flaviria (UC)", "Dragoon / Warrior", [],
  ["Jump", "High Jump", "Super Jump", "Angon", "Berserk"],
  ["(5) Skewer", "(25) Impulse Drive", "(50) Celidon's Torment"],
  unity("Flaviria"),
  ["Possesses merits in Jump recast down, High Jump recast down, and Angon at level 75.",
   "Uses weapon skills at 1000 TP. Does not try to skillchain.",
   "Celidon's Torment is a Unity Leader version of Camlann's Torment which has a similar Ignores Defense property.",
   "Aggressive weapon skill usage and Jumps enhanced by Berserk, boosted Unity Leader stats (and Flaviria Unity Shirt), and early access to higher level weapon skills make Flaviria a strong physical damage dealer to have while leveling.",
   "  An advantage of the Piercing Damage Type is that enemies weak to it like Mandragora, Birds, and Flys are common across Vana'diel."])

t("Gilgamesh", "Samurai / Warrior", [], ["Hasso", "Third Eye", "Sekkanoki", "Hagakure"],
  ["Tachi: Goten", "Tachi: Kasha", "Iainuki", "Tachi: Kamai (AoE)"],
  [CIPHER.format("Gilgamesh"), "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Holds up to 2000 TP to close skillchains.",
   "If he has 2000 TP and Sekkanoki is ready, he self Skillchains."])

t("Halver", "Paladin / Warrior", ["Cure I - IV", "Flash"],
  ["Berserk", "Rampart", "Provoke", "Sentinel"],
  ["Penta Thrust", "Impulse Drive", "Raiden Thrust"],
  [CIPHER.format("Halver"),
   "  Speak to Halver in Chateau d'Oraguille (I-9) during Mission 2-3 for any nation (Journey Abroad / The Emissary / The Three Kingdoms).",
   "  Alternatively speak to Halver in Chateau d'Oraguille once the Rhapsodies of Vana'diel Mission 1-7 (The Path Untraveled) is complete."],
  ["Possesses MP+30%.",
   "Uses Berserk as often as possible.",
   "When party member's HP is low (under 40%), he acts as a tank and uses his abilities and magic more frequently.",
   "Uses Sentinel and Rampart as soon as he starts doing tank behavior.",
   "Uses weapon skills at 1000 TP, but it is lower priority."])

t("Ingrid II", "White Mage / Warrior", ["Banish I - III", "Cursna", "Holy"],
  ["Self-Aggrandizement"],
  ["Merciless Strike", "Moonlight", "Inexorable Strike", "Ruthlessness (Conal Drain)"],
  [CIPHER.format("Ingrid II"), "  Sinister Reign", "  Mog Pell (Ochre)", "  Filled to Capacity"],
  ["Possesses Undead Killer, Banish effectiveness vs Undead +10 (28/256).",
   "Saves up to 2500 TP while waiting to close a skillchain.",
   "Ingrid II's weapon skills are especially effective at creating Light-based skillchains.",
   "Ingrid II only casts spells in order to Magic Burst, doing so with the Banish line of Divine Magic.",
   "Moonlight use doesn't appear to be triggered by anything specific (such as her or party members lacking MP).",
   "Self-Aggrandizement: Recovers HP and removes one status ailment for the entire party. Used when 3 or more party members are in yellow HP (<75%) or a party member is asleep. Recast: 00:30.",
   "Ingrid II is especially effective against undead enemies due to her propensity to create Light skillchains and magic bursting with powerful Banish spells."])

t("Invincible Shield (UC)", "Warrior / Corsair", [],
  ["Provoke", "Aggressor", "Restraint", "Retaliation", "Warcry", "Blood Rage", "Tomahawk", "Savagery"],
  ["(5) Raging Rush", "(25) Steel Cyclone", "(50) Sotun's Fury"],
  unity("Invincible Shield"),
  ["Possesses Damage Taken -20%, WAR/traits.",
   "Depending on Unity Ranking: HP+20%~+30%.",
   "Uses Warcry then Blood Rage as soon as Warcry ends.",
   "Uses Tomahawk on Skeletons, Slimes, and Elementals.",
   "He is a damage dealer who Provokes.",
   "  When you don't need a tank, he'll do more damage with Retaliation.",
   "  To get the most out of Retaliation, this version of Giruvua does not have his shield.",
   "Holds up to 1500 TP to close skillchains.",
   "At item level, he gets the same ilvl stat increase as the tanks and Monberaux."])

t("Iroha", "Samurai / White Mage", ["Protectra V", "Shellra V"],
  ["Hagakure", "Hasso", "Meditate", "Third Eye", "Save TP (400)", "Blessing of Phoenix (one time Reraise)"],
  ["Amatsu: Hanadoki", "Amatsu: Choun", "Amatsu: Fuga", "Amatsu: Gachirin"],
  [CIPHER.format("Iroha"), "  Complete Nary a Cloud in Sight."],
  ["Possesses MP+50%.",
   "If Hagakure and Meditate are available, does not try to close skillchains created by other weapon skills or existing skillchains: focuses on making a solo skillchain at 2000 TP.",
   "  Iroha's skillchain is as follows: Hanadoki > Choun = Fuga > Gachirin = Gachirin.",
   "Holds up to 2500 TP to close skillchains.",
   "Has access to Protectra V and Shellra V at level 75 but no lower tier versions.",
   "Iroha possesses the blessing of Phoenix which will revive her at full HP if she is killed in battle (occurs only once per summoning)."])

t("Iroha II", "Samurai / White Mage", ["Protectra V", "Shellra V", "Flare II"],
  ["Hasso", "Save TP (400)", "Meditate", "Third Eye"],
  ["Amatsu: Kyori", "Amatsu: Hanadoki (+ Chance to Dispel)", "Amatsu: Suien", "Amatsu: Gachirin",
   "Rise From Ashes (AoE Restore HP + MP + Stoneskin)"],
  [CIPHER.format("Iroha II"), "  Complete The Orb's Radiance."],
  ["Possesses HP-5%, MP+250%.",
   "Gains 205 TP per hit.",
   "Has access to Protectra V and Shellra V but no lower tier versions.",
   "Iroha will normally hold her TP in order to close any potential skillchains.",
   "When Iroha has 2000+ TP and Meditate is ready, she will attempt to perform a 4 part Double Light skillchain.",
   "Iroha will magic burst fire-based skillchains using a near instant cast Flare II.",
   "This version of Iroha has taken on a fiery new appearance and the blessing of Phoenix was upgraded; her Reraise was replaced with the AoE healing skill, Rise From Ashes.",
   "Rise From Ashes is a weapon skill that restores 25% HP of all party members, restores MP, and provides a 500HP Stoneskin buff.",
   "  She will use Rise From Ashes if 3 or more party members are at yellow HP (75%) or if a party member is asleep."])

t("Iron Eater", "Warrior / Warrior", [], ["Provoke", "Berserk", "Restraint"],
  ["Shield Break", "Armor Break", "Steel Cyclone"],
  ["Complete the initiation quest in Bastok.",
   "Have obtained the following Trust spells: Naji, Ayame, & Volker.",
   "  Speak to Iron Eater in the Metalworks (J-8)."],
  ["Possesses 5/5 Double Attack merits, enhanced Double Attack rate, enhanced Store TP.",
   "Will only use Provoke if your HP is low.",
   "Will use Restraint and waits until 35~40 attacks have landed (long after reaching 3000 TP) to use a random weaponskill.",
   "While not using Restraint, uses TP as soon as he gets it."])

t("Jakoh Wahcondalo (UC)", "Thief / Warrior", [],
  ["Conspirator", "Trick Attack", "Sneak Attack", "Feint"],
  ["(5) Dancing Edge", "(25) Evisceration", "(50) Sarva's Storm"],
  unity("Jakoh Wahcondalo"),
  ["Uses weapon skills at >2000 TP with Trick Attack and/or Sneak Attack.",
   "  Holds up to 3000 TP to wait for positioning.",
   "  Weapon skill used is random. Does not try to close skillchains.",
   "Will open with Feint and uses it on cooldown.",
   "Wields a knife. Gains 55 TP on hit."])

t("Klara", "Warrior / Warrior", [], ["Berserk", "Provoke", "Warcry"],
  ["Fast Blade", "Vorpal Blade", "Savage Blade", "Temblor Blade (AoE)"],
  [TWELVE + " The starting quest = Better Part of Valor and you don't need to be allied to Bastok (S) in order to start or obtain this trust.",
   "Be in possession of the Bundle of scrolls key item.",
   "  Complete Bonds of Mythril which is the end of the 12 quest process.",
   "  Speak with Gentle Tiger in Bastok Markets (S) (H-6)."],
  ["Temblor Blade is a significantly stronger variant of Circle Blade.",
   "Uses TP as soon as she gets it.",
   "Provokes when the player is in orange (50%) HP."])

t("Lehko Habhoka", "Thief / Black Mage", ["Single-target elemental nukes I - II"], [],
  ["Iridal Pierce (AoE)", "Lunar Revolution (Conal)", "Debonair Rush", "Insprint (AoE HP+MP restore + Erase)"],
  [CIPHER.format("Lehko"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Possesses MP+150%, enhanced Magic Accuracy.",
   "Has an abnormally high Double/Triple attack rate.",
   "Tends to use a weapon skill right when he hits 1000 TP.",
   "Regularly uses a throwing Ranged Attack in conjunction with his auto-attacks.",
   "  Spells are used more frequently against enemies resistant to piercing damage, such as elementals.",
   "Occasionally uses elemental magic for moderate damage. (Does not attempt to magic burst.)",
   "Use of Insprint does not appear to be triggered by party condition (i.e. he can use it if everyone is at full HP)."])

t("Lhe Lhangavo", "Monk / Warrior", [],
  ["Dodge", "Chakra", "Impetus", "Focus", "Formless Strikes", "Provoke"],
  ["Backhand Blow", "Raging Fists", "Dragon Kick", "Asuran Fists"],
  [CIPHER.format("Lhe"), "  Repeat Login Campaigns", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Possesses Invigorate (Chakra + Regen).",
   "Uses Focus if accuracy is below a certain threshold.",
   "Provokes when the player who summoned her falls below half HP.",
   "Uses Dodge when in the top enmity slot.",
   "Uses Formless Strikes if the target is resistant to physical damage (leech, slime, elemental, ghost).",
   "Holds TP until 2000 to try to close skillchains."])

t("Lhu Mhakaracca", "Beastmaster / Warrior", [], ["Feral Howl", "Berserk", "Aggressor"],
  ["Spinning Axe", "Rampage", "Onslaught", "Decimation"],
  [CIPHER.format("Lhu"), "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Favors Spinning Axe.",
   "Gains 91 TP per hit.",
   "Uses TP as soon as she gets it.",
   "Uses Feral Howl when the enemy is < 20% HP, which can help to prevent abilities triggered by low HP (e.g. healing abilities, Final Sting), especially job abilities you wouldn't be able to Stun normally (e.g. Benediction, Mijin Gakure)."])

t("Lilisette", "Dancer / Dancer", [], [],
  ["Whirling Edge (AoE)", "Dancer's Fury", "Rousing Samba", "Sensual Dance", "Thorn Dance",
   "Vivifying Waltz (Divine Waltz II)"],
  [CIPHER.format("Lilisette"), "  Complete A Forbidden Reunion."],
  ["Even though she appears to Dual Wield, she only attacks with a single attack per round.",
   "Does not try to participate in skillchains.",
   "Waits until ~1500 TP to use a TP move; Vivifying Waltz and Thorn Dance are prioritized when conditions are met.",
   "Vivifying Waltz will be used @ 1500 TP when at least 2 party members are in yellow HP (<75%), or as soon as 1000 TP when a party member is in orange (<50%) HP. The amount healed varies with TP.",
   "Rousing Samba does not create samba animations on attacks, and will return 0 TP if not damaging to the enemy.",
   "All of Lilisette's abilities are considered TP moves and are AoE critical hit rate (10%).",
   "Sensual Dance is an AoE party attack (15%) and magic attack boost, but can miss party members due to positioning.",
   "  Sensual Dance affects other party members with Lilisette in their line of sight (like a beneficial Gaze attack), and does not include herself.",
   "  Sensual Dance can affect Lilisette, but the positioning is different. One way to do it is for Lilisette to be in front of the target and behind the player (the \"Trick Attack to the face\" position) and still close to the target. Then they would need to be facing each other to both receive the buff.",
   "  The two boosts applied during Sensual Dance can wear off at different times, one at ~50 seconds, the other at ~55 seconds.",
   "Thorn Dance is a self-targeted Defense Bonus used when taking the top enmity slot. She can prioritize this ability and use it under 1500 TP."])

t("Lilisette II", "Dancer / Warrior", [], ["Rousing Samba"],
  ["Whirling Edge", "Dancer's Fury", "Vivifying Waltz"],
  [CIPHER.format("Lilisette II"), "  Complete Ganged Up On."],
  ["Holds up to 2000 TP to close skillchains.",
   "Appears to have a very fast attack rate and TP gain even with low/moderate Haste.",
   "Like other Alter Ego II's, her weapon skills have been changed to single target.",
   "Vivifying Waltz changed to trigger when 3 party members are in yellow HP (<75%), and will be used with at least 1000 TP.",
   "Rousing Samba changed to a normal samba ability that casts 350 TP, so Lilisette II can easily maintain the effect.",
   "Rousing Samba is an AoE critical hit rate (10%).",
   "  She's valuable for party members using weapon skills with crit TP modifiers such as Victory Smite.",
   "If you avoid using weapon skills she can skillchain with (like Rudra's Storm), she will save TP for healing.",
   "Rousing Samba has a noticeably higher effect on Lilisette herself, granting her an extremely high critical hit rate (approx. 75%)."])

t("Lion", "Thief / Thief", [], [],
  ["Walk the Plank (AoE)", "Pirate Pummel", "Powder Keg (Conal)", "Grapeshot (Conal)"],
  [CIPHER.format("Lion"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Possesses THF traits such as Treasure Hunter I, Gilfinder, and Triple Attack.",
   "Uses TP as soon as she gets it.",
   "If the enemy is readying a TP move when she is ready to use a weapon skill, Lion will stun it with Grape Shot.",
   "Walk the Plank \u2014 AoE damage, bind, knock back, and dispel.",
   "Pirate Pummel \u2014 Damage and burn effect.",
   "Powder Keg \u2014 Conal damage, knock back, defense down, and magic defense down.",
   "Grape Shot \u2014 Conal damage and stun effect."], ALZ)

t("Lion II", "Thief / Ninja", ["Utsusemi: Ichi/Ni"], [],
  ["Walk the Plank", "Pirate Pummel", "Powder Keg", "Grapeshot"],
  [CIPHER.format("Lion II"), "  Complete A Land After Time."],
  ["Possesses THF/NIN traits such as Treasure Hunter I, Gilfinder, and Triple Attack.",
   "Lion II's weaponskills are single target versions of Lion's weaponskills, with the same name and animation.",
   "Holds up to 3000 TP to try to close skillchains.",
   "Walk the Plank \u2014 Damage, bind, knock back, and dispel.",
   "Pirate Pummel \u2014 Damage and burn effect.",
   "Powder Keg \u2014 Damage, knock back, defense down, and magic defense down.",
   "Grape Shot \u2014 Damage and stun effect."])

t("Luzaf", "Corsair / Ninja", [], ["Quick Draw", "Triple Shot"],
  ["(5) Bisection", "(25) Akimbo Shot", "(50) Leaden Salute", "(60) Grisly Horizon"],
  [CIPHER.format("Luzaf"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Possesses Skillchain Bonus, Magic Accuracy Bonus, Quick Draw Recast Down and Quick Draw Magic Accuracy from Merits, and A+ skill ranks on Sword, Dagger, and Gun.",
   "Does not use Phantom Roll.",
   "Dual wields and shoots, leading to high rate of TP gain.",
   "Uses Quick Draw to deal damage based on the enemy's elemental weakness(es).",
   "Holds up to 2500 TP waiting for the player to reach 1000 and then weapon skills in order to open a skillchain.",
   "Prefers to open skillchains for his player but will close skillchains opened by another party member or trust.",
   "Selects one of his weapon skills randomly upon summoning and uses it exclusively unless attempting to close a skillchain.",
   "Great choice for closing Distortion and Darkness skillchains with other trusts due to not having access to Light, Fusion or Fragmentation properties."])

t("Maat", "Monk / Thief", [], ["Mantra", "Perfect Counter", "Formless Strikes"],
  ["Asuran Fists", "One-Inch Punch", "Combo", "Dragon Kick", "Howling Fist", "Bear Killer (Conal)"],
  ["Complete Shattering Stars for six or more jobs.", "  Speak with Maat in Ru'Lude Gardens (H-5)."],
  ["Possesses Treasure Hunter.",
   "Mantra gives both an HP boost as well as Haste.",
   "Uses weapon skills at 1000 TP.",
   "Uses Formless Strikes for enemies resistant to blunt damage (slimes, leeches)."])

t("Maat (UC)", "Monk / Warrior", [], ["Chakra", "Counterstance", "Impetus"],
  ["(50) Hollow Smite"],
  unity("Maat"),
  ["Possesses increased Kick Attacks rate.",
   "Exclusively uses Hollow Smite as his weaponskill. If called below level 50, he will not have a way to spend TP.",
   "Uses Hollow Smite under any of the following conditions:",
   "  To open skillchains for the player when they have 1000 TP.",
   "  To close a skillchain started by other party members if possible.",
   "  When Maat (UC) has 3000 TP."])

t("Matsui-P", "Ninja / Black Mage",
  ["Utsusemi: Ichi/Ni/San", "Elemental Ninjutsu (San)", "Single-target elemental nukes I", "Burn",
   "Migawari: Ichi", "Kakka: Ichi", "Myoshu: Ichi", "Yurin: Ichi", "Aisha: Ichi", "Aspir", "Stun"],
  ["Innin", "Sange", "Elemental Seal", "Futae", "Mana Wall"],
  ["(1) Blade: Rin", "(9) Blade: Retsu", "(55) Blade: Ei", "(60) Blade: Jin", "(66) Blade: Ten",
   "(72) Blade: Ku", "(75) Blade: Kamu", "(85) Blade: Hi", "(91) Blade: Shun"],
  ["If you have completed the quest Trust: Windurst, Trust: Bastok, or Trust: San d'Oria, you will automatically obtain the alter ego upon logging in.",
   "  No message will be displayed signifying that you have acquired the alter ego.",
   "If you have not completed the quest Trust: Windurst, Trust: Bastok, or Trust: San d'Oria, you must first complete it and then relog or change areas.",
   "  No message will be displayed signifying that you have acquired the alter ego.",
   "Matsui-P was/is only available during the following times:",
   "  From December 2020 until May 2021.",
   "  From November 2022 until May 2023.",
   "  From March 2025 until September 2025."],
  ["Prioritizes elemental ninjutsu and black magic spells.",
   "Magic bursts skillchains with Ninjutsu tier San and elemental magic tier I enhanced by Futae.",
   "Under specific conditions outlined below, uses weapon skills when the player reaches 1000 TP in order to open skillchains.",
   "Has callouts in party chat, making him easy to use.",
   "  Announces when his TP is 1000.",
   "  Before using a weapon skill, he will announce the skillchain property you can follow up with for a Light or Darkness skillchain.",
   "  You can see these callouts when the Chat Filter option for \"Messages from alter egos\" says OFF.",
   "Casts Burn to lower enemy INT and prime them for Magical Damage.",
   "Casts Stun to interrupt enemy TP moves, and reduces monster TP gain with Myoshu.",
   "Generates TP rapidly with Daken, enhanced by Sange, though he often stops attacking to cast spells.",
   "High accuracy and damage for a trust.",
   "Prioritizes reapplying shadows and doesn't perform weaponskills if shadows are removed.",
   "Skillchains:",
   "  Once the player uses a Weapon Skill with Level 2 Skillchain Properties while Matsui-P is summoned, he will use weapon skills when the player has 1000 or more TP.",
   "  He only starts skillchains that would create Light or Darkness skillchains with the previously used weapon skill.",
   "  He has no Distortion weapon skills, so he has no reaction to players using Gravitation weapon skills.",
   "  Holds TP until 3000 to open skillchains for the player. Uses a random weapon skill at 3000 TP if conditions are not met.",
   "Matsui-P's skills and behavior were decided by the winner of the \"Alter Ego Design Campaign \u2014 One Venturous Tarutaru!\" competition."])

t("Maximilian", "Thief / Ninja", [], [],
  ["Fast Blade", "Vorpal Blade", "Swift Blade"],
  [CIPHER.format("Maximilian"), "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Dual Wields swords.",
   "Possesses typical THF/NIN traits such as Treasure Hunter I, Dual Wield, Triple Attack.",
   "Tries to open skillchains when the player reaches 1500 TP. Does not try to skillchain with other trusts.",
   "The weapon skill he opens with is random.",
   "Will close skillchains with players and other trusts if possible, otherwise uses a weapon skill at 2500 TP."])

t("Mayakov", "Dancer / Warrior", [],
  ["Drain Samba I - III", "Haste Samba", "Feather Step", "Saber Dance", "Climactic Flourish"],
  ["Coming Up Roses", "Fast Blade", "Swift Blade", "Vorpal Blade"],
  [CIPHER.format("Mayakov"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Possesses 5/5 Haste Samba Effect merits (10% job ability Haste).",
   "Uses Saber Dance upon engaging and refreshes it as often as possible.",
   HASTE_SAMBA,
   "Debuffs enemies using Feather Step while building Finishing moves to perform Climactic Flourish.",
   "Tends not to weapon skill very frequently due to spending TP on Feather Step as often as possible.",
   "Weapon skills more frequently once Feather Step's Daze reaches level 10; only occasionally using Feather Step to maintain the Daze effect.",
   "If he has enough TP for a weapon skill, uses Climactic Flourish first.",
   "Holds up to 2000 TP to wait for Climactic Flourish recast; does not try to skillchain."])

t("Mildaurion", "Paladin / Samurai", [], [],
  ["Light Blade (Physical)", "Stellar Burst (Magical)", "Great Wheel (Physical AoE + Knockback)",
   "Vortex (Magical Wind)"],
  [CIPHER.format("Mildaurion"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Possesses MP+100% (but doesn't use MP), Double Attack.",
   "Attacks with palm blasts that are blunt damage (tested on warder of temperance).",
   "Her attacks and abilities are Zilartian themed: uses the fighting stance of the Mammets and weapon skills of Kam'lanaut and Eald'narche with some differences.",
   "Tries to open skillchains when the player reaches 1500 TP. Does not try to skillchain with other trusts.",
   "The weapon skill she opens with is random. Easy to skillchain with: all of her weapon skills have level 2 properties.",
   "Will close skillchains with players and other trusts if possible, otherwise uses a weapon skill at 3000 TP."])

t("Morimar", "Warrior / Beastmaster", [], ["Vehement Resolution"],
  ["12 Blades of Remorse (AoE)", "Into the Light", "Arduous Decision (Silence)",
   "Camaraderie of the Crevasse"],
  [CIPHER.format("Morimar"), "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Possesses HP+10%.",
   "Vehement Resolution consumes Morimar's TP, fully heals him, erases his debuffs, and makes him glow. (3 minute cooldown.)",
   "Morimar will not attempt to close skillchains in his glow-state and his next WS will be 12 Blades of Remorse with 2000 TP.",
   SPECIAL_MOVES,
   "Saves up to 2000 TP waiting to close a skillchain."],
  DARR_MORI + ["Teodor: Unknown."])

t("Mumor", "Dancer / Warrior", [],
  ["Stutter Step", "Haste Samba", "Drain Samba/II/III", "Saber Dance", "Violent Flourish"],
  ["Skullbreaker"],
  [CIPHER.format("Mumor"),
   "  Sunbreeze Festival",
   "    Fully finish Fantastic Fraulein Mumor: Dynamic Doppelgangers twice, wearing this year's garments the second time, and talk with a Moogle at: Northern San d'Oria (G-8) / Bastok Markets (I-7) / Windurst Walls (G-11). You will obtain the Trust spell automatically during the cutscene.",
   "  Mog Pell (Ochre)"],
  ["Always uses Saber Dance and does not use waltzes.",
   "Will attempt to use Violent Flourish to stun TP moves.",
   "Once Stutter Step is at daze lv.5, only re-applies it when it's <10s from expiring.",
   "Uses Skullbreaker when at 1000 TP.",
   HASTE_SAMBA], MUMOR_UKA)

t("Naja Salaheem", "Monk / Warrior", [], ["Focus", "Dodge", "Counterstance"],
  ["True Strike", "Black Halo", "Hexa Strike", "Peacebreaker"],
  [CIPHER.format("Naja"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Peacebreaker is a single-target, low damage weaponskill with an additional effect of 20% Defense Down and 20% Magic Defense Down (lasts up to 30s).",
   "Naja gains 100 TP per hit.",
   "Uses weapon skills at 1000 TP."])

t("Naja Salaheem (UC)", "Monk / Warrior", [], [],
  ["(5) Peacebreaker", "(25) Hexa Strike", "(50) Nott", "(60) Black Halo", "(70) Justicebreaker"],
  unity("Naja Salaheem"),
  ["Possesses Quadruple Attack, Triple Attack, Store TP, and Gilfinder traits.",
   "On summoning will pick a club weapon skill from her list and use that exclusively; re-summoning her will randomize the choice of weapon skill again, in this way you can \"pick\" her weapon skill.",
   "200 TP per hit.",
   "Uses weapon skills when another party member has 1000 TP, otherwise holds TP indefinitely.",
   "Her multi-attack rate is very high. She can be a great skillchain partner for other trusts or yourself.",
   "But the damage is low to balance out the number of swings, and you may worry about feeding TP (Monster TP Gain).",
   "Peacebreaker applies a 20% Defense Down and 20% Magic Defense Down to the target for up to 30 seconds.",
   "Justicebreaker applies a 10% Defense Down and 10% Magic Defense Down to the target for up to 60 seconds.",
   "She has no MP so Nott only serves to restore her HP, which can make her very survivable if she has the required accuracy.",
   "With another party member like Ajido-Marujido who builds but doesn't spend TP, you may get Naja to self-skillchain Darkness with Justicebreaker."])

t("Naji", "Warrior / Warrior", [], ["Provoke"],
  ["Burning Blade", "Red Lotus Blade", "Vorpal Blade"],
  ["Complete the initiation quest in Bastok."],
  ["Uses weapon skills at 1000 TP, does not try to skillchain.", "Provokes on cooldown."])

t("Nanaa Mihgo", "Thief / Thief", [], ["Despoil"],
  ["Wasp Sting", "Dancing Edge", "King Cobra Clamp (AoE)"],
  ["Complete the initiation quest in Windurst.",
   "Must be Rank 3 or higher in any nation.",
   "  Complete Mihgo's Amigo.",
   "    After completing this quest, zone and/or wait one game day. If you happen to pick up the Rock Racketeer quest, then it means next visit to Nanaa Mihgo will be for the Trust of her.",
   "  Speak with Nanaa Mihgo in Windurst Woods at (J-3)."],
  ["Possesses Treasure Hunter I.",
   "King Cobra Clamp stuns the target(s).",
   "Despoil places the stolen item in the summoner's inventory.",
   "Can be resummoned to reset the Despoil timer (5 minutes) after use.",
   "Uses TP as soon as she gets it."])

t("Nashmeira", "Puppetmaster / White Mage", ["-na spells", "Cure I - IV"], [],
  ["Imperial Authority (Stun)"],
  ["Complete Eternal Mercenary.", "  Examine the Imperial Whitegate in Aht Urhgan Whitegate (L-9)."],
  ["Possesses MP+70%.",
   "Uses Imperial Authority at 1000 TP.",
   "Casts Cure on party members at low HP (<33%)."],
  ["Grants trust synergy bonuses to her automaton companions Mnejing and Ovjang.",
   "  Mnejing receives increased defense (+10%) and increased enmity (+10%).",
   "  Ovjang receives reduced enmity (-10%) and increased magic damage (+10%)."])

t("Noillurie", "Samurai / Paladin", ["Cure I - IV"],
  ["Hasso", "Third Eye", "Meditate", "Sekkanoki"],
  ["Tachi: Jinpu", "Tachi: Yukikaze", "Tachi: Gekko", "Tachi: Kasha", "Tachi: Kaiten"],
  [CIPHER.format("Noillurie"), "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Possesses MP+65%.",
   "Favors Tachi: Kaiten, but will use other weapon skills to close a Skillchain (however, she favors opening skillchains most times).",
   "Noillurie will perform Tachi: Kaiten on an existing Light skillchain in order to create a double Light skillchain (she can accomplish this even if she opened the initial skillchain thanks to her high rate of TP gain).",
   "Will attempt to perform a 4-step double Light self-skillchain based on Sekkanoki recast:",
   "  Tachi: Yukikaze > Tachi: Gekko > Tachi: Kasha > Tachi: Kaiten",
   "When Sekkanoki is on cooldown, uses weapon skills at 1000 TP.",
   "Uses Cure spells on party members <50% HP or asleep.",
   "Learns her weapon skills at low levels: has Tachi: Jinpu by level 30 or earlier, Tachi: Kaiten by level 50."],
  ["Excellent skillchain partner with Iroha II due to her frequency in opening Light skillchains with Tachi: Kaiten."])

t("Prishe", "Monk / White Mage", ["Cure I - IV"], [],
  ["Knuckle Sandwich (damage)", "Nullifying Dropkick", "Auroral Uppercut (damage)"],
  ["Complete Dawn, including the final cutscene in Lufaise Meadows.",
   "  Examine the Walnut Door in Tavnazian Safehold (K-7, Top floor).",
   "Players will be unable to receive the alter ego if the quests Storms of Fate or Shadows of the Departed are in progress, or if Apocalypse Nigh is in progress and the event scene occurring in Sealion's Den is not completed."],
  ["Possesses HP-5%, MP+75%.",
   "Will only cast Cure when a party member is at very low health.",
   "Uses TP as soon as she gets it."],
  ["Ulmia: Prishe and Ulmia will prioritize supporting each other.",
   "  Ulmia will cast Pianissimo and Sentinel's Scherzo on Prishe if she takes a large amount of damage in a single hit and two songs are already active. This seems to prevent the player from receiving Scherzo after AoE damage. (Doesn't apply to Prishe II.)",
   "  Prishe will cast Cure spells on Ulmia at yellow (75%) HP."])

t("Prishe II", "White Mage / Monk", ["Curaga I - V"], ["Psychoanima", "Hysteroanima"],
  ["Knuckle Sandwich", "Nullifying Dropkick", "Auroral Uppercut"],
  [CIPHER.format("Prishe II"), "  Complete Call to Serve."],
  ["Possesses HP+10%, MP+10%.",
   "Psychoanima: Prishe gains physical damage immunity for <5 seconds. Used when brought to low HP with a physical attack, only available once per summon.",
   "Hysteroanima: Prishe gains magical damage immunity for <5 seconds. Used preemptively in response to her target starting to cast a high-tier damaging AoE spell, only available once per summon.",
   "  Log will read \"Prishe resists the effects of the spell!\"",
   "Prishe will cast Curaga spells to wake up any players/trusts affected by sleep or when players are in critical HP.",
   "Uses TP as soon as she gets it.",
   "Does damage equivalent to a melee fighter trust, but as a WHM it may be difficult to get support spells like Haste II."],
  ["Ulmia: Prishe II can cast Cure I - IV only on Ulmia."])

t("Rainemard", "Red Mage / Paladin",
  ["Enspells", "Haste/II", "Distract/II", "Frazzle/II", "Phalanx/II", "Protect I - V", "Shell I - V", "Refresh"],
  ["Composure"],
  ["Burning Blade", "Red Lotus Blade", "Vorpal Blade", "Savage Blade"],
  [CIPHER.format("Rainemard"),
   "  Be in possession of the Bundle of scrolls key item.",
   "  Speak with Shanene in Batallia Downs (S) (J-7)."],
  ["Will only cast Haste II and other enhancing magic spells on himself.",
   "Casts Enspells on himself based on the enemy's weaknesses (Note: he may change his Enspell each time he engages with a different enemy family).",
   "Rainemard's Enspells are extremely powerful, capable of dealing 50-350+ damage depending on his level/item level and stat buffs (MAB, etc).",
   "Casts Refresh when he falls below 50% MP."],
  ["Curilla: Rainemard casts Phalanx II (unlocked at level 75) only on Curilla and himself. His Phalanx, like his Enspells, also appears to benefit from his extremely high enhancing magic skill; his Phalanx II is -35 damage."])

t("Romaa Mihgo", "Thief / Warrior", [], ["Feint", "Aura Steal", "Sneak Attack", "Trick Attack"],
  ["Fast Blade", "Vorpal Blade", "Savage Blade", "Cobra Clamp (Conal AoE, Stun, Paralyze)"],
  [TWELVE + " The starting quest = The Tigress Stirs and you don't need to be allied to Windurst (S) in order to start or obtain this trust.",
   "Be in possession of the Bundle of scrolls key item.",
   "  Complete At Journey's End.",
   "  Speak with Romaa Mihgo in Windurst Waters (S) (G-11)."],
  ["Will use Aura Steal to take buffs off mobs. This can Steal items also, which will be added to the player's inventory.",
   "Will only use Trick Attack and Sneak Attack when positioned correctly with the player, does not try to combine with weapon skills.",
   "Uses TP as soon as she gets it."],
  ["Nanaa Mihgo / Lehko Habhoka"])

t("Rongelouts", "Warrior / Warrior", [], ["Berserk", "Aggressor", "Warcry"],
  ["Tongue Lash (AoE Terror)", "Red Lotus Blade", "Savage Blade", "Seraph Blade"],
  [CIPHER.format("Rongelouts"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Possesses enhanced Warcry duration (50 seconds).",
   "Has a unique Beastmen Killer trait.",
   "Gains 75 TP on hit.",
   "Uses TP as soon as he gets it.",
   "Tongue Lash causes an AoE Terror effect. Seems to have a short duration (~2 seconds)."])

t("Selh'teus", "Paladin / Samurai", [], [],
  ["Luminous Lance", "Rejuvenation (HP + MP + TP restore)", "Revelation"],
  [CIPHER.format("Selh'teus"), "  Complete Call of the Void."],
  ["Has 50 Regain. MP+100% (but doesn't use MP).",
   "Uses unique weaponskill Rejuvenation in response to the player taking a hit that depletes them to at least yellow HP or when the player is asleep. Restores HP, MP, TP to the entire party. Used every 30 seconds.",
   "Be aware that he will not move into range to engage in combat on his own; it is recommended to summon him early in your trust order to ensure he will be in range to attack.",
   "Holds TP until 3000 to close skillchains.",
   "Luminous Lance is a ranged weapon skill.",
   "Is treated as a Paladin: does not use Paladin abilities, but impacts behavior of trust supports or off-tanks like Ark HM and behavior of certain enemies like Bozetto Necronura."])

t("Shikaree Z", "Dragoon / White Mage", ["Cure I - IV", "Haste", "-na Spells", "Erase"],
  ["Jump", "High Jump", "Super Jump", "Ancient Circle"],
  ["Raiden Thrust", "Skewer", "Wheeling Thrust", "Impulse Drive"],
  ["Complete Three Paths.",
   "  Speak to Perih Vashai in Windurst Woods (K-7). Note: you must have the Windurst Trust Permit.",
   "  If you are on some Promathia Missions after 5-3 (8-2 for sure) you will not be able to acquire this trust until completing those missions."],
  ["Possesses HP-10%, MP+100%.",
   "Uses Ancient Circle if the enemy is a dragon.",
   "Super Jump is used when Shikaree Z is in the top enmity slot.",
   "Gains 205 TP on hit; has high TP return on Jump (655 TP) and High Jump (1065 TP).",
   "Holds TP to 2000 to try to close skillchains.",
   "Saves Cure for party members under 50% HP or affected by Sleep.",
   "Prioritizes Haste over other spells, except to cast Erase when Slow would prevent Haste."])

t("Tenzen", "Samurai / Samurai", [],
  ["Hasso", "Save TP (400)", "Meditate", "Hagakure", "Third Eye"],
  ["Amatsu: Torimai", "Amatsu: Kazakiri", "Amatsu: Yukiarashi", "Amatsu: Tsukioboro",
   "Amatsu: Hanaikusa", "Amatsu: Tsukikage"],
  [CIPHER.format("Tenzen"), "  Records of Eminence: Basic Tutorial Objective Reward",
   "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Gains 203 TP per hit.",
   "Holds TP until 1500 to try to close skillchains.",
   "If Meditate and Hagakure are both available, can do 3-step self-skillchains.",
   "Nearly all of Tenzen's weapon skills are variants of normal Great Katana weapon skills.",
   "Amatsu: Tsukikage is a unique weapon skill only usable by Tenzen."])

t("Teodor", "Black Mage / Dark Knight", ["-ja Spells", "-ga Spells (Magic Burst only)"],
  ["Start from Scratch"],
  ["Sinner's Cross", "Ravenous Assault (Drain)", "Frenzied Thrust", "Open Coffin",
   "Hemoclasis (Restores Teodor's HP)"],
  [CIPHER.format("Teodor"), "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Possesses HP+35%, MP+50%.",
   "Teodor cannot be healed via curative magic. (Trusts with healing magic will not attempt to heal him.)",
   "  Regen spells, Indi-Regen, Blue Magic, and curative Blood Pacts all can heal him.",
   "Normal attacks have different attributes depending on their motion.",
   "  A slash with his cane is slashing.",
   "  An attack causing an explosion with his left hand is a darkness attribute special attack.",
   "  Horizontal striking attack has a Silence Additional Effect.",
   "Since his attacks are treated as special techniques, his attack interval is not affected or influenced by Haste, Slow, En-spell, Samba, Spikes, etc.",
   "Uses TP randomly and does not try to skillchain.",
   "Uses Start from Scratch under 50%, which consumes TP, erases negative status effects, and gives him a dark aura.",
   "When he has the dark aura on, he will build TP to 2000 and use Hemoclasis, and loses the aura.",
   "Only uses his elemental magic to magic burst."],
  ["Morimar: Unknown."])

t("Uka Totlihn", "Dancer / Warrior", [],
  ["Quickstep", "Drain Samba/II/III", "Reverse Flourish", "Haste Samba", "Curing Waltz I - V", "Healing Waltz"],
  ["Judgment"],
  [CIPHER.format("Uka"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Heals party members with Curing Waltzes when they're below 66% HP.",
   "Builds finishing moves using Quickstep and expends them on Reverse Flourish to gain TP.",
   "Once Quickstep is at daze lv.5, only re-applies it when it's <10s from expiring.",
   "Uses Reverse Flourish only with 5 finishing moves and when TP is low.",
   "When above 2000 TP, uses Judgment. Does not try to skillchain.",
   "Has Healing Waltz but only removes status effects from herself.",
   HASTE_SAMBA], MUMOR_UKA)

t("Volker", "Warrior / Warrior", [],
  ["Aggressor", "Berserk", "Defender", "Provoke", "Retaliation", "Warrior's Charge", "Warcry"],
  ["Berserk-Ruf (Attack Boost)", "Fast Blade", "Savage Blade", "Spirits Within", "Vorpal Blade"],
  ["Complete the initiation quest in Bastok.",
   "Must be Rank 6 or higher in any nation.",
   "  Speak to Lucius in the Metalworks at (I-9)."],
  ["If there is a NIN, PLD, or RUN in the party, behaves as a damage dealer: uses Aggressor, Berserk.",
   "If there are no other tanks in the party, behaves as a tank: uses Defender, Retaliation.",
   "Uses Provoke in either role to maintain enmity as a tank or off-tank.",
   "Uses weapon skills at 2000 TP with Warrior's Charge if it's available; does not try to skillchain."])

t("Zazarg", "Monk / Monk", [], ["Focus"],
  ["Howling Fist", "Dragon Kick", "Asuran Fists", "Meteoric Impact"],
  ["Complete Fist of the People.",
   "  Speak with Fari-Wari in Aht Urhgan Whitegate (K-12).",
   "Players will be unable to receive the alter ego if he is being held prisoner by beastmen forces in Besieged."],
  ["Uses the unique weapon skill Meteoric Impact.",
   "Focuses when needed based on high enemy evasion.",
   "Uses TP as soon as he gets it."],
  ["Rughadjeen empowers the other serpent generals.",
   "  Zazarg gains ~5-15% damage.",
   "  Rughadjeen has Damage Taken -29% while in combat with a foe."])

t("Zeid", "Dark Knight / Dark Knight",
  ["Absorb spells (includes Absorb-Attri and Absorb-TP)", "Endark", "Drain/Aspir I/II", "Stun"],
  ["Last Resort", "Nether Void", "Souleater"],
  ["Freezebite", "Ground Strike", "Abyssal Drain (Drain)", "Abyssal Strike (Stun)"],
  [CIPHER.format("Zeid"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["At low HP, uses HP draining weapon skills and Nether Void for Drain II.",
   "Uses Absorb-TP in the second half of the battle (when an enemy has TP).",
   "Only uses Souleater when a healer is present (Automaton doesn't count).",
   "Uses TP as soon as he gets it.",
   "If the enemy is readying a TP move when he is ready to use a weapon skill, attempts to stun it with Abyssal Strike.",
   "Casts Stun to interrupt enemy TP moves."], ALZ)

t("Zeid II", "Dark Knight / Warrior", ["Stun", "Absorb-Attri"], ["Last Resort", "Souleater"],
  ["Ground Strike"],
  [CIPHER.format("Zeid II"), "  Complete Volto Oscuro."],
  ["Will exclusively use Ground Strike for his Weapon Skill (Note: he will not know Ground Strike until a specific level (appears to be level 50), leading him to hold 3000 TP indefinitely if summoned below said level).",
   "Tries to Skillchain with others, otherwise saves TP to 3000 and then uses it.",
   "  Due to Ground Strike's skillchain properties, Zeid can close level 3 skillchains with weapon skills that possess Fusion or Gravitation properties.",
   "Uses Stun to stop enemy abilities.",
   "Only uses Souleater when a healer is present (Automaton doesn't count).",
   "Tends to gain TP very fast due to Desperate Blows while using Last Resort."],
  ["Chacharoon: Zeid can Absorb-Attri to steal the attack bonus granted by Chacharoon's Tripe Gripe."])

# ---- merge, guard, write --------------------------------------------------
existing = {x["n"] for x in d["trusts"]}
dupes = [x["n"] for x in T if x["n"] in existing]
assert not dupes, dupes
names = [x["n"] for x in T]
assert len(names) == len(set(names)), [n for n in names if names.count(n) > 1]
assert not [k for x in T for k, v in x.items() if v is None]
for x in T:
    assert x["role"] in d["roles"]

d["trusts"] = sorted(d["trusts"] + T, key=lambda x: x["n"])
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, separators=(", ", ": "))

c = collections.Counter(x["role"] for x in d["trusts"])
print("added", len(T), "-> total", len(d["trusts"]))
print(dict(c))
