# Rev 340 — adds the SUPPORT and SPECIAL roles to assets/trusts.json, plus the general
# Trust reference sections (`info`) that head the Trusts tab.
# Author: BalladOfWorms
import json, collections

PATH = "/home/claude/android/app/src/main/assets/trusts.json"
d = json.load(open(PATH, encoding="utf-8"))
T = []

CIPHER = "Trade the Cipher: {} item to one of the beginning Trust quest NPCs, which may be acquired via:"
INCORPOREAL = "Incorporeal Trust: unaffected by all attacks, skills, and magic, and thus cannot die."
YGNAS = ["Ygnas: Ygnas will gain a 2/tick Indi-Refresh."]
BUFF_BY_JOB = [
    "Casts buffs on party members based on job:",
    "  Flurry II: RNG, COR",
    "  Haste II: WAR, MNK, THF, PLD, DRK, BST, SAM, NIN, DRG, BLU, PUP, DNC, RUN",
    "    Haste II grants 307/1024 Magical Haste.",
    "  Refresh II: WHM, BLM, RDM, PLD, SMN, GEO, RUN, SCH, or any character with WHM subjob.",
    "    Will stop casting Refresh on a SCH once they use Sublimation.",
]


def t(n, role, job, spells, abilities, ws, acq, feat, syn=None):
    e = {"n": n, "role": role, "job": job, "spells": spells,
         "abilities": abilities, "ws": ws, "acq": acq, "feat": feat}
    if syn:
        e["syn"] = syn
    T.append(e)


def incorporeal(n, acq, feat):
    """The Geomancer/Bard sphere trusts — no spells, no abilities, no weapon skills."""
    t(n, "Special", "Geomancer / Bard", [], [], [], acq, [INCORPOREAL] + feat)


# ============================ SUPPORT ============================
t("Arciela", "Support", "Red Mage / Paladin",
  ["Refresh/II", "Haste/II", "Protect I - V", "Shell I - V", "Slow/II", "Paralyze/II", "Addle", "Dispel"],
  ["Bellatrix of Light", "Bellatrix of Shadows"],
  ["Guiding Light (AoE Atk + Def + M.Atk + M.Def Up)", "Illustrious Aid", "Dynastic Gravitas"],
  ["Complete The Light Within.",
   "  Speak to Ploh Trishbahk at the castle gates in Eastern Adoulin.",
   "    Examine the \"Sandy Overlook\" in Ceizak Battlegrounds (J-10)."],
  ["Possesses MP+20%, Regain (25 TP/tick), RDM/PLD traits including Auto-Refresh I.",
   "Tends to behave more as a support as opposed to Arciela II.",
   "Uses Refresh and Haste only on the player and herself, prioritizing the player.",
   "Will always overwrite Haste with Haste II.",
   "Auto-attacks seem to be light elemental regardless of stance, and are affected by MAB/MDB.",
   "Bellatrix of Light \u2014 Enables enhancing magic and Illustrious Aid.",
   "Bellatrix of Shadows \u2014 Enables enfeebling magic and Dynastic Gravitas.",
   "  No cooldown on changing between the two stances; she will switch as needed to cast spells based on priority.",
   "Dynastic Gravitas \u2014 Inflicts amnesia on nearby enemies.",
   "Guiding Light \u2014 Nearby party members gain increased attack, defense, magic attack, and magic defense for 30 seconds. Usable from either stance. The effect overwrites and prevents application of Cocoon and Saline Coat.",
   "Illustrious Aid \u2014 Restores HP to nearby party members. Used when multiple party members are in yellow HP (<75%).",
   "Stationary behavior: will stay in place after engaging. If allies/enemies are out of her casting range and in line of sight, she will slowly inch toward them until they're in casting range.",
   "  Haste II grants 307/1024 Magical Haste."], YGNAS)

t("Arciela II", "Support", "Red Mage / Black Mage",
  ["Refresh/II", "Haste/II", "Flurry II", "Protect I - V", "Shell I - V", "Slow/II", "Paralyze/II",
   "Addle", "Dispel", "Single Target Elemental Nukes I - V"],
  ["Ascension", "Descension"],
  ["Light aura: Expunge Magic, Harmonic Displacement",
   "Darkness aura: Darkest Hour, Sight Unseen",
   "Neutral: Unceasing Dread (Paralyze), Dignified Awe (Amnesia), Naakual's Vengeance (Recover own HP + MP)"],
  [CIPHER.format("Arciela II"), "  Complete What He Left Behind."],
  ["Possesses MP+50%, increased Enhancing Magic duration (+25%).",
   "Tends to behave much more offensively as compared to Arciela I.",
   "Possesses an extremely potent Fast Cast; spells she casts appear to be cast instantly.",
   "She will often double magic burst with two tier 5 spells or a tier 5 and tier 4 spell.",
   "Uses weapon skills at 1000 TP.",
   "When at low HP, can use TP move Naakual's Vengeance to fully restore HP and MP. (5 minute cooldown.)",
   "Can have a tendency to run out of MP due to double magic bursting high tier elemental magic.",
   "Ascension (Light mode) \u2014 Enhancing magic, Healing Magic, Light based WSs, Light-aligned Elemental Magic.",
   "Descension (Dark mode) \u2014 Enfeebling magic, Darkness based WSs, Darkness-aligned Elemental Magic.",
   "  Spends about 90 seconds in each mode before switching."] + BUFF_BY_JOB, YGNAS)

t("Joachim", "Support", "Bard / White Mage",
  ["Sword/Blade Madrigal", "Battlefield/Carnage Elegy", "Advancing/Victory March",
   "Army's Paeon I - VI", "Mage's Ballad I - III", "Valor Minuet I - V", "Knight's Minne I - V",
   "Cure I - IV", "Erase", "-na Spells"],
  [], [],
  [CIPHER.format("Joachim"), "  Records of Eminence: Basic Tutorial Objective Reward",
   "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Doesn't melee but performs a throwing ranged attack (traverser stones?).",
   "By default he sings March and Madrigal (level permitting).",
   "Waits for his songs to expire before changing songs; does not overwrite songs.",
   "Song Priority:",
   "  Paeon x2 when Joachim's HP is below 90%. This is the only song he will double up.",
   "  Ballad when Joachim's MP is below 75%.",
   "  March: Unless another Bard is providing them, Victory March > Advancing March.",
   "  Madrigal: Unless another Bard is providing them, Blade Madrigal > Sword Madrigal.",
   "  Minuet: sometimes Ulmia plays both Marches, and Joachim does Valor Minuet V for his second song.",
   "  Minne: when both Marches and Madrigals are performed by other Bards, Knight's Minne V.",
   "Casting Cure takes higher priority than songs, so he's more likely to be using Ballad than Paeon.",
   "  Until the party's supports are out of MP, then he starts casting Paeons due to the resulting lack of healing.",
   "Victory March grants 155/1024 (15.14%) Magical Haste.",
   "Blade Madrigal grants +60 Accuracy.",
   "  None of Joachim's songs gain any instrument/equipment bonuses."])

t("King of Hearts", "Support", "Red Mage / White Mage",
  ["Refresh/II", "Haste/II", "Dia/II/III", "Temper", "Firaga IV", "Cure I - IV", "Phalanx/II",
   "-na Spells", "Erase"],
  [],
  ["Bludgeon", "Shuffle (Dispel)", "Deal Out (AoE)", "Double Down"],
  [CIPHER.format("King"), "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Possesses HP+25%, MP+80%.",
   "Benefits from a permanent Composure effect and gains +50% Enhancing Magic duration when casting on other targets than himself.",
   "Is considered Arcana, thus is susceptible to Monster Correlation effects.",
   "The King of Hearts mainly acts as a RDM but has access to spells of WHMs and BLMs.",
   "Opens the fight up with Dia before any other spells. (Will continually attempt to Dia an enemy even if the enemy is immune.)",
   "Will cast Cure on any players at 50% or less HP.",
   "Prioritizes Erase and -na spells above other spells. Will quickly cast these on any trust or party member immediately after being debuffed, starting with the master and itself.",
   "Casts Haste, Refresh, and Phalanx on the player regardless of their job or enmity.",
   "  Will not cast Haste or Refresh on other players or trusts.",
   "  King of Hearts thinks the player is his master, Ambassador Karababa (BLM).",
   "Casts Phalanx on the party member or alter ego with the highest enmity on King's current target's list. -35 dmg Phalanx at level 99.",
   "Will magic burst Firaga off of Liquefaction, Fusion, or Light skillchains.",
   "From time to time the King of Hearts may randomly \"Level Up\", which restores some HP and MP as well as unlocking access to Bludgeon. It doesn't seem to be actively triggered, but may occur at any time during combat.",
   "Uses TP randomly and does not try to skillchain.",
   "Prioritizes Shuffle when able to Dispel an enemy buff.",
   "  Haste II grants 307/1024 Magical Haste."],
  ["Shantotto: King of Hearts uses the full range of his enhancing spells on Shantotto in the same way as on himself and his player, and even prioritizes her over the player and himself. (Does not apply to Shantotto II or Domina Shantotto.)"])

t("Koru-Moru", "Support", "Red Mage / White Mage",
  ["Refresh/II", "Haste/II", "Flurry/II", "Protect I - V", "Shell I - V", "Phalanx II", "Slow/II",
   "Dia/II/III", "Distract/II", "Dispel", "Cure I - IV"],
  ["Convert"], [],
  [CIPHER.format("Koru-Moru"), "  Records of Eminence: Always Stand on 117 Objective Reward",
   "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Does not engage.",
   "Will only use Convert at very low MP, making him susceptible to DoT or AoE death.",
   "Will not cast a higher-tier debuff if the enemy already has a lower-tier applied.",
   "Will cast Phalanx II even if Phalanx is already applied. However, Phalanx II will not be cast over Barrier Tusk.",
   "  Koru-Moru's Phalanx II reduces damage received by 31 at level 99.",
   "Will cast Distract II on enemies with High Evasion as classified by the /check command for the PC."]
  + BUFF_BY_JOB + ["Does not overwrite Haste with Haste II or Flurry II."])

t("Qultada", "Support", "Corsair / Ranger", [],
  ["Triple Shot", "Double-Up", "Snake Eye", "Corsair's Roll", "Chaos Roll", "Hunter's Roll",
   "Evoker's Roll", "Fighter's Roll", "Light Shot", "Dark Shot"],
  ["Savage Blade", "Burning Blade", "Sniper Shot", "Detonator"],
  [CIPHER.format("Qultada"), "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Possesses Winning Streak (level 75: +100s Phantom Roll duration).",
   "Qultada dispels with Dark Shot and enhances Dia with Light Shot but never uses Quick Draw just to deal damage.",
   "Uses weapon skills at 1000 TP.",
   "Qultada's standard Phantom Rolls are Chaos Roll and Fighter's Roll.",
   "  He replaces Chaos Roll with Hunter's Roll if his player's accuracy against the currently fought enemy is under a certain threshold.",
   "  He replaces Fighter's Roll with Evoker's Roll if any party member has low MP (<66%).",
   "  He replaces Fighter's Roll with Corsair's Roll if his player has Dedication or Commitment active (excluding the special Dedication status from Cipher: Kupofried).",
   "Will Double-Up on any non-lucky roll value between 1 and 6 and can bust his rolls.",
   "He uses Snake Eye when he is one point away from a lucky roll or from 11.",
   "Doesn't perform weaponskills until finished applying Phantom Rolls.",
   "  When he has a busted roll, he doesn't WS until the bust effect expires."])

t("Sylvie (UC)", "Support", "Geomancer / White Mage",
  ["Cure I - IV", "-na Spells", "Erase", "Haste", "Indi-Haste", "Indi-Fury", "Indi-Precision",
   "Indi-Refresh", "Indi-Regen", "Indi-Acumen", "Indi-Languor"],
  ["Entrust"], ["(50) Nott"],
  ["Be a member of the Sylvie Unity Concord.",
   "  Obtain 5000 Unity Accolades through Records of Eminence objectives for a Partial Personal Evaluation of Spt."],
  ["Possesses Regain+50, Damage Taken-25%, enhanced Indicolure duration (6 minutes total, includes Entrust effects).",
   "Will change Indicolure spells based on accuracy requirements, and the main job of the player.",
   "Does not melee or cast spells on enemies, relying on Regain for TP.",
   "Follows the player or trust in front of her in the party lineup.",
   "Casts Haste on the player who summoned her (regardless of job) and any physical melee damage dealers in the party.",
   "Uses Entrust on the player unless their main job is GEO, where she will Entrust the first PLD, RUN, or NIN in the party instead.",
   "  Even if the player's Entrust is on that target, Sylvie will overwrite it with her Entrust.",
   "Will cast Indicolure spells based on the player's job and hit rate, ranged hit rate, or item level:",
   "  Indi-Fury (+37.5% Attack/Ranged Attack) or Indi-Precision (+56 Accuracy/Ranged Accuracy) and Entrust Indi-Frailty (-12.5% Defense): WAR, MNK, THF, BST, DRK, DRG, SAM, BLU, PUP, DNC based on hit rate; RNG, COR based on ranged hit rate.",
   "  Indi-Haste (+28.8% haste) and Entrust Indi-Refresh (+5/tick): PLD and RUN",
   "  Indi-Haste (+28.8% haste) and Entrust Indi-Regen (+3/tick): NIN",
   "  Indi-Acumen (+21 Magic Attack) or Indi-Focus (+55 Magic Accuracy) and Entrust Indi-Refresh (+5/tick): BLM, RDM, SCH, based on the difference between your level or item level and the enemy's level. Indi-Focus is used when the enemy's level is higher than the player's level by 5 or more.",
   "  Indi-Refresh (+8/tick) and Entrust Indi-Acumen (+21 Magic Attack): WHM, BRD, SMN",
   "  Indi-Refresh (+8/tick) and Entrust Indi-Languor (-41 Magic Evasion): GEO",
   "    Sylvie only uses Entrust with a player GEO who does not have an Indicolure on themself, but Sylvie's Indi-Languor will go on the first PLD, RUN, or NIN in the party.",
   "Below level 93, Sylvie won't use any of the above Indi- spells until everything's available, regardless of your job (i.e. she is waiting until Indi-Haste's level, whether you need it or not).",
   "  Indi-Regen available at Level 20. Provides about level+3 hp/tick, reaching the maximum +30hp @ 89. About equivalent potency to the highest level Regen Spells available.",
   "  Indi-Refresh available at Level 30. Used instead of Indi-Regen if your main job has MP: WHM, RDM, BLM, SCH, SMN, GEO, PLD, RUN, BLU, DRK. Provides +2mp @ 32, +3mp @ 58, +4mp @ 84, +5mp @ 98.",
   "Gains Geomancy+3 at level 99.",
   "Uses TP to recover MP."])

t("Ulmia", "Support", "Bard / Bard",
  ["Sword/Blade Madrigal", "Hunter's/Archer's Prelude", "Advancing/Victory March",
   "Valor Minuet I - V", "Mage's Ballad I - III", "Sentinel's Scherzo"],
  ["Pianissimo"], [],
  ["Complete Dawn.",
   "  Examine the Dilapidated Gate in Misareaux Coast (I-11).",
   "    Please note that there are two Dilapidated Gates in the zone.",
   "Players will be unable to receive the alter ego if the quest Storms of Fate is in progress after viewing the event at the Dilapidated Gate in Misareaux Coast (F-7), until the battlefield is completed."],
  ["Does not engage.",
   "Recasts her songs shortly before they wear off.",
   "Song Priority:",
   "  Ballad: Based on party composition, rate of MP usage, and a target party member's remaining MP percentage (details below).",
   "  March: Unless another Bard is providing them, Victory March and Advancing March.",
   "  Madrigal: Unless another Bard is providing them, Blade Madrigal and Sword Madrigal.",
   "  Minuet: when both Marches and Madrigals are performed by other Bards, plays the highest level Valor Minuets not currently on the party.",
   "Pianissimo will be used for the player under certain conditions after Ulmia has two songs on the party.",
   "  Scherzo after taking a large amount of damage, or afflicted with the Weakness status.",
   "  Ballad if the party's MP is under 75% and main job is WHM, BLM, RDM, SMN, GEO, or SCH.",
   "  Prelude and Minuet if main job is RNG or COR.",
   "Ballad logic:",
   "  Ulmia tracks rate of MP usage to determine the target party member spending the highest percentage of their MP.",
   "    It is possible for all party members to be at low MP and double Marches are still being played, due to failing this MP consumption check.",
   "    You can try forcing yourself to be the ballad target by resummoning Ulmia then pulling with a spell.",
   "  Cast Ballad if target party member's MP is below a certain threshold:",
   "    75% if 3 or more party members (out of 6) have native MP, based on main and sub job.",
   "    33% if 2 or fewer party members (out of 6) have native MP.",
   "    Can do double Ballads, depending on MP and timing of 2nd song expiration.",
   "Advancing March grants 108/1024 Magical Haste.",
   "Victory March grants 155/1024 Magical Haste."],
  ["Prishe: Prishe and Ulmia will prioritize supporting each other.",
   "  Ulmia will use Pianissimo and cast Sentinel's Scherzo on Prishe if she takes a large amount of damage in a single hit and two songs are already active. This seems to prevent the player from receiving Scherzo after AoE damage. (Doesn't apply to Prishe II.)",
   "  Prishe will cast Cure spells on Ulmia at yellow (75%) HP. (Other party members are healed at low HP.)",
   "  Prishe II normally only has access to Curaga spells, but will cast Cure spells on Ulmia."])

# ============================ SPECIAL ============================
incorporeal("Brygid",
  [CIPHER.format("Brygid"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Indi-CHR stacks with player Indi-CHR.",
   "This Indi-CHR grants a +9.7% Defense Bonus, +5 Magic Defense Bonus and +5 CHR at lv. 99."])

incorporeal("Cornelia",
  ["If you have completed the quest Trust, you will automatically obtain the alter ego upon logging in after the Tuesday, December 9th, 2025 version update.",
   "  No message will be displayed signifying that you have acquired the alter ego.",
   "If you have not completed the quest Trust, you must first complete it after the Tuesday, December 9th, 2025 version update and then relog or change areas.",
   "  No message will be displayed signifying that you have acquired the alter ego.",
   "Cornelia was/is only available during the following times:",
   "  From September 2017 until May 2018.",
   "  From May 2022 until November 2022.",
   "  From June 2024 until December 2024.",
   "  From December 2025 until March 2026."],
  ["Haste +20%, Accuracy +30, Ranged Accuracy +30, Magic Accuracy +30."])

incorporeal("Kupofried",
  [CIPHER.format("Kupofried"), "  Adventurer Appreciation Campaign",
   "  Adventurer Gratitude Campaign", "    Week three if not already obtained.",
   "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Grants a +20% dedication effect for both Experience Points and Capacity Points.",
   "This stacks with other forms of dedication such as that gained from a Capacity Ring."])

incorporeal("Kuyin Hathdenna",
  [CIPHER.format("Kuyin"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Indi-Precision stacks with player Indi-Precision.",
   "This Indi-Precision grants Accuracy+24, Ranged Accuracy+24, and DEX+5 at lv. 99.",
   "  The amount of DEX increases when Kuyin is employed in your Mog Garden, depending on unknown factors possibly including the ranks of Mog Garden locations and number or length of Kuyin contracts.",
   "  Up to +2 bonus."])

incorporeal("Moogle",
  [CIPHER.format("Moogle"), "  Adventurer Appreciation Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Indi-Refresh (3 MP/tick at lv. 99) stacks with player-cast Indi-Refresh.",
   "  This Indi-Refresh also grants an increase to magical skill gain rate."])

incorporeal("Sakura",
  [CIPHER.format("Sakura"), "  Repeat Login Campaign", "  Mog Pell (Ochre)"],
  ["Indi-Regen (6 HP/tick at lv. 99) stacks with player-cast Indi-Regen.",
   "  This Indi-Regen also grants an increase to physical combat skill gain rate."])

incorporeal("Star Sibyl",
  [CIPHER.format("S. Sibyl"), "  Repeat Login Campaign", "  Mog Pell (Red)", "  Mog Pell (Ochre)"],
  ["Has full time Indi-Acumen (Magic Attack Boost). +19 at level 99.",
   "This sphere effect also has a +19 Magic Accuracy boost at level 99.",
   "  The Magic Accuracy boost can raise trusts' M.ACC over breakpoints for certain spells like Dispel against some enemies."])

# ==================== general reference sections ====================
INFO = [
 {"title": "Alter Ego Statistics & Levels", "lines": [
  "Player level 99 or lower:",
  "  An Alter Ego's level is fixed and always matches the level of the player who called it forth. Levelling up while it is out does not improve it \u2014 re-call it to see the improvement.",
  "Players level 99 or above:",
  "  An Alter Ego's level is adjusted automatically while called forth, based on the calling player's average Item Level (shown under the Equipment menu). All Alter Egos adjust automatically when that changes. Item Level 119 is the initial cap.",
  "  Since the January 2017 version update, Haste+ is granted to Alter Egos called forth by players with an average Item Level of 100+. The exact value depends on the Trust's type.",
  "  Since the November 2021 version update, these Trusts called forth at Item Level 100+ gain increased defense and an increased Shield Block Activation Rate based on average Item Level: Kupipi, Curilla, Trion, Mihli Aliapoh, Valaineral, Mnejing, Lhu Mhakaracca, Rahal, August, Yoran-Oran.",
  "    Ark Angel EV is exempt \u2014 her defense power increases regardless of Item Level.",
  "  Master Levels have no additional effect on Trusts.",
  "Alter Egos have the same stat distribution as players, and appear to follow the distribution used for Adventuring Fellows and other NPCs.",
  "  Their equipment is mostly cosmetic, though a few pieces carry real effects \u2014 Valaineral's defense reduction resembles the Hauteclaire, and Ferreous Coffin has the WHM relic armor's Refresh+2, but his Cure potency matches Kupipi's, so stats like Healing Magic Skill+ and MND+ are not applied.",
  "  Player stats are more balanced between races from level 61 onward; Trusts did not get the same adjustment.",
  "  The base MP boost for a job without MP taking a subjob with MP is 33% higher for Trusts.",
 ]},
 {"title": "Further Improvements", "lines": [
  "The Rhapsody in Fuchsia raises an Alter Ego's derived stats by roughly one level, and grants Haste+ (2).",
  "  The \"Trust's Stats Up\" effect covers every base stat except HP and MP \u2014 calculated at about +20 to STR/DEX/AGI/VIT/INT/MND/CHR at level 99.",
  "  Square Enix described the increase as job-dependent (more Magic Accuracy for a ranged magic attacker, more Accuracy for a melee attacker); they have used accuracy and hit rate interchangeably before, so this may mean INT/MND/CHR and DEX.",
  "Monster Rearing's Cheer effects offer many further bonuses.",
  "Abyssea, Voidwatch, Geas Fete, Domain Invasion, Odyssey and other content each have their own ways of strengthening Alter Egos \u2014 see those content pages.",
  "  Alter Egos receive Atmas and similar effects such as Vorseals, but NOT Signet or Ionis.",
  "Three Trust NPCs in Ru'Lude Gardens (H-5) unlock new Records of Eminence categories, special Trusts, and Alter Ego Points respectively: Jamal, Marjory, Syndella.",
 ]},
 {"title": "Alter Ego Points", "lines": [
  "Alter Ego Points enhance a Trust's attributes \u2014 HP, STR, combat skills and so on \u2014 at Lv. 99.",
  "Earned mainly from monthly Deeds objectives in the Records of Eminence, Ambuscade rewards at 100 total Hallmarks, and occasional seasonal-event and Vana'Bout opportunities.",
  "Every stat can eventually be maxed, but points CANNOT be reassigned \u2014 choose upgrades carefully. Some Trusts have different HP/MP caps based on their traits.",
  "Unlocking:",
  "  Syndella provides a Cipher bracelet once you have completed one of the initiation Trust quests, possess the Job breaker, and your current main job is Level 99.",
  "Obtaining:",
  "  Trust Primer \u2014 Records of Eminence Deeds objectives (monthly) / Ambuscade 100 total Hallmarks (monthly) \u2014 20 points",
  "  Trust Tome \u2014 seasonal events / Vana'Bout \u2014 100 points",
  "  Marjory's Thesis \u2014 Marjory, after completing Way Over Capacity (one-time) \u2014 200 points",
  "Cost per level:",
  "  Levels 1-10: 1 point per level",
  "  Levels 11-20: 2 per level",
  "  Levels 21-30: 3 per level",
  "  Levels 31-40: 4 per level",
  "  Levels 41-50 (max): 5 per level",
  "  150 total points to take one attribute to the maximum of 50.",
  "Using:",
  "  Assigned only inside a Mog House or Mog Garden, like Merit Points, under Main Menu \u2192 Profile \u2192 Alter Ego Points.",
  "  All attributes can be upgraded eventually; the only limit is available points.",
 ]},
 {"title": "Alter Ego Equipment System", "lines": [
  "Currently under development.",
  "Square Enix have said the feature will let you select equipment for a Trust, giving it ability boosts beyond its base stats, working much the way puppetmaster attachments do. They intend the gear to be obtainable while playing solo and are exploring ways to tie it into existing content and crafting, so further detail is some way off.",
 ]},
 {"title": "Monthly Adventurer Campaigns", "lines": [
  "Two campaigns may run in any given month.",
  "Alter Ego Expo:",
  "  While active, Trusts receive various bonuses to their stats and performance.",
  "  Maximum HP and MP rise by +50% for every Trust you summon.",
  "    This is added on top of any always-on effect. Ferreous Coffin always has -10% max HP and +35% max MP, so during the campaign he has +40% max HP and +85% max MP.",
  "  All Trusts gain higher resistance to status effects.",
  "Alter Ego Expo Campaign \u2014 PLUS!:",
  "  While active, Trusts receive the above and a recovery effect.",
  "  A Trust reduced to 0 HP instead recovers HP and MP to maximum with no Weakened state. Status effects still remain.",
  "    Iroha is not eligible for this benefit.",
  "    Against the spell Death or the effect of Doom, Trusts will not recover and disappear as normal.",
 ]},
]

# ---- merge, guard, write --------------------------------------------------
existing = {x["n"] for x in d["trusts"]}
assert not [x["n"] for x in T if x["n"] in existing], [x["n"] for x in T if x["n"] in existing]
names = [x["n"] for x in T]
assert len(names) == len(set(names))
assert not [k for x in T for k, v in x.items() if v is None]
for x in T:
    assert x["role"] in d["roles"], (x["n"], x["role"])
    assert x["acq"] and x["feat"], x["n"]
for s in INFO:
    assert s["title"] and s["lines"] and all(isinstance(l, str) for l in s["lines"])

d["trusts"] = sorted(d["trusts"] + T, key=lambda x: x["n"])
d["info"] = INFO
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, separators=(", ", ": "))

c = collections.Counter(x["role"] for x in d["trusts"])
print("added", len(T), "-> total", len(d["trusts"]))
print({r: c.get(r, 0) for r in d["roles"]})
print("info sections:", [s["title"] for s in INFO])
