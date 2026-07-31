# Builds assets/weaponskills.json — the full player weapon-skill reference,
# transcribed from the BG-wiki Weapon Skill tables. Skillchain properties are NOT
# stored here: the screen resolves them by name out of skillchains.json so there is
# one source of truth for chain data.
#   req : weapon skill level required, or the unlock class (Quest/Relic/Empyrean/
#         Aeonic/Mythic/Ergon/Prime)
#   np  : true when the wiki prints "No Property" (no skillchain properties at all)
# Author: BalladOfWorms
import json, collections

W = []


def w(type_, jobs, rows, note=None):
    ws = []
    for r in rows:
        e = {"n": r[0], "req": r[1]}
        if len(r) > 2 and r[2]:
            e["np"] = True
        ws.append(e)
    d = {"type": type_, "jobs": jobs, "ws": ws}
    if note:
        d["note"] = note
    W.append(d)


w("Hand-to-Hand", ["MNK", "PUP", "DNC", "WAR", "THF", "NIN", "RDM", "DRK", "BST"], [
    ("Combo", "5"), ("Shoulder Tackle", "40"), ("One Inch Punch", "75"),
    ("Backhand Blow", "100"), ("Raging Fists", "125"), ("Spinning Attack", "150"),
    ("Howling Fist", "200"), ("Dragon Kick", "225"), ("Asuran Fists", "Quest"),
    ("Tornado Kick", "300"), ("Shijin Spiral", "Aeonic"), ("Final Heaven", "Relic"),
    ("Victory Smite", "Empyrean"), ("Ascetic's Fury", "Mythic"),
    ("Stringing Pummel", "Mythic"), ("Maru Kala", "Prime"),
])

w("Dagger", ["THF", "COR", "DNC", "RDM", "WAR", "RNG", "BRD", "BST", "NIN", "PUP",
             "DRK", "PLD", "BLM", "SCH", "SAM", "DRG", "SMN", "GEO"], [
    ("Wasp Sting", "5"), ("Gust Slash", "40"), ("Shadowstitch", "70"),
    ("Viper Bite", "100"), ("Cyclone", "125"), ("Energy Steal", "150", True),
    ("Energy Drain", "175", True), ("Dancing Edge", "200"), ("Shark Bite", "225"),
    ("Evisceration", "Quest"), ("Aeolian Edge", "290"), ("Exenterator", "Aeonic"),
    ("Mercy Stroke", "Relic"), ("Rudra's Storm", "Empyrean"),
    ("Mandalic Stab", "Mythic"), ("Mordant Rime", "Mythic"),
    ("Pyrrhic Kleos", "Mythic"), ("Ruthless Stroke", "Prime"),
])

w("Sword", ["PLD", "BLU", "RUN", "WAR", "RDM", "COR", "DRK", "SAM", "NIN", "DRG",
            "BRD", "THF", "RNG", "DNC", "BST"], [
    ("Fast Blade", "5"), ("Burning Blade", "30"), ("Red Lotus Blade", "50"),
    ("Flat Blade", "75"), ("Shining Blade", "100"), ("Seraph Blade", "125"),
    ("Circle Blade", "150"), ("Spirits Within", "175", True), ("Vorpal Blade", "200"),
    ("Swift Blade", "225"), ("Savage Blade", "Quest"), ("Sanguine Blade", "300", True),
    ("Requiescat", "Aeonic"), ("Knights of Round", "Relic"),
    ("Chant du Cygne", "Empyrean"), ("Death Blossom", "Mythic"),
    ("Atonement", "Mythic"), ("Expiacion", "Mythic"), ("Imperator", "Prime"),
])

w("Great Sword", ["RUN", "DRK", "WAR", "PLD"], [
    ("Hard Slash", "5"), ("Power Slash", "30"), ("Frostbite", "70"),
    ("Freezebite", "100"), ("Shockwave", "150"), ("Crescent Moon", "175"),
    ("Sickle Moon", "200"), ("Spinning Slash", "225"), ("Ground Strike", "Quest"),
    ("Herculean Slash", "290"), ("Resolution", "Aeonic"), ("Scourge", "Relic"),
    ("Torcleaver", "Empyrean"), ("Dimidiation", "Ergon"), ("Fimbulvetr", "Prime"),
])

w("Axe", ["BST", "WAR", "DRK", "RNG", "RUN"], [
    ("Raging Axe", "5"), ("Smash Axe", "40"), ("Gale Axe", "70"),
    ("Avalanche Axe", "100"), ("Spinning Axe", "150"), ("Rampage", "175"),
    ("Calamity", "200"), ("Mistral Axe", "225"), ("Decimation", "Quest"),
    ("Bora Axe", "290"), ("Ruinator", "Aeonic"), ("Onslaught", "Relic"),
    ("Cloudsplitter", "Empyrean"), ("Primal Rend", "Mythic"), ("Blitz", "Prime"),
])

w("Great Axe", ["WAR", "RUN", "DRK"], [
    ("Shield Break", "5"), ("Iron Tempest", "40"), ("Sturmwind", "70"),
    ("Armor Break", "100"), ("Keen Edge", "150"), ("Weapon Break", "175"),
    ("Raging Rush", "200"), ("Full Break", "225"), ("Steel Cyclone", "Quest"),
    ("Fell Cleave", "300"), ("Upheaval", "Aeonic"), ("Metatron Torment", "Relic"),
    ("Ukko's Fury", "Empyrean"), ("King's Justice", "Mythic"), ("Disaster", "Prime"),
])

w("Scythe", ["DRK", "WAR", "BST", "BLM"], [
    ("Slice", "5"), ("Dark Harvest", "30"), ("Shadow of Death", "70"),
    ("Nightmare Scythe", "100"), ("Spinning Scythe", "125"), ("Vorpal Scythe", "150"),
    ("Guillotine", "200"), ("Cross Reaper", "225"), ("Spiral Hell", "Quest"),
    ("Infernal Scythe", "300"), ("Entropy", "Aeonic"), ("Catastrophe", "Relic"),
    ("Quietus", "Empyrean"), ("Insurgency", "Mythic"), ("Origin", "Prime"),
])

w("Polearm", ["DRG", "WAR", "SAM", "PLD"], [
    ("Double Thrust", "5"), ("Thunder Thrust", "30"), ("Raiden Thrust", "70"),
    ("Leg Sweep", "100"), ("Penta Thrust", "150"), ("Vorpal Thrust", "175"),
    ("Skewer", "200"), ("Wheeling Thrust", "225"), ("Impulse Drive", "Quest"),
    ("Sonic Thrust", "300"), ("Stardiver", "Aeonic"), ("Geirskogul", "Relic"),
    ("Camlann's Torment", "Empyrean"), ("Drakesbane", "Mythic"), ("Diarmuid", "Prime"),
])

w("Katana", ["NIN"], [
    ("Blade: Rin", "5"), ("Blade: Retsu", "30"), ("Blade: Teki", "70"),
    ("Blade: To", "100"), ("Blade: Chi", "150"), ("Blade: Ei", "175"),
    ("Blade: Jin", "200"), ("Blade: Ten", "225"), ("Blade: Ku", "Quest"),
    ("Blade: Yu", "290"), ("Blade: Shun", "Aeonic"), ("Blade: Metsu", "Relic"),
    ("Blade: Hi", "Empyrean"), ("Blade: Kamu", "Mythic"), ("Zesho Meppo", "Prime"),
])

w("Great Katana", ["SAM", "NIN"], [
    ("Tachi: Enpi", "5"), ("Tachi: Hobaku", "30"), ("Tachi: Goten", "70"),
    ("Tachi: Kagero", "100"), ("Tachi: Jinpu", "150"), ("Tachi: Koki", "175"),
    ("Tachi: Yukikaze", "200"), ("Tachi: Gekko", "225"), ("Tachi: Kasha", "Quest"),
    ("Tachi: Ageha", "300"), ("Tachi: Shoha", "Aeonic"), ("Tachi: Kaiten", "Relic"),
    ("Tachi: Fudo", "Empyrean"), ("Tachi: Rana", "Mythic"), ("Tachi: Mumei", "Prime"),
])

w("Club", ["PLD", "WHM", "GEO", "BLU", "WAR", "MNK", "SMN", "SCH", "BLM", "DRK",
           "RDM", "BRD", "BST", "PUP", "THF", "RNG", "SAM", "DRG", "NIN"], [
    ("Shining Strike", "5"), ("Seraph Strike", "40"), ("Brainshaker", "70"),
    ("Starlight", "100", True), ("Moonlight", "125", True), ("Skullbreaker", "150"),
    ("True Strike", "175"), ("Judgment", "200"), ("Hexa Strike", "220"),
    ("Black Halo", "Quest"), ("Flash Nova", "290"), ("Realmrazer", "Aeonic"),
    ("Randgrith", "Relic"), ("Dagan", "Empyrean", True), ("Mystic Boon", "Mythic", True),
    ("Exudation", "Ergon"), ("Dagda", "Prime"),
])

w("Staff", ["PLD", "WAR", "MNK", "SMN", "DRG", "BLM", "WHM", "BRD", "SCH", "GEO",
            "RDM", "BST"], [
    ("Heavy Swing", "5"), ("Rock Crusher", "40"), ("Earth Crusher", "70"),
    ("Starburst", "100"), ("Sunburst", "150"), ("Shell Crusher", "175"),
    ("Full Swing", "200"), ("Spirit Taker", "215", True), ("Retribution", "Quest"),
    ("Cataclysm", "290"), ("Shattersoul", "Aeonic"), ("Gate of Tartarus", "Relic"),
    ("Myrkr", "Empyrean", True), ("Vidohunir", "Mythic"), ("Garland of Bliss", "Mythic"),
    ("Omniscience", "Mythic"), ("Oshala", "Prime"),
])

w("Archery", ["RNG", "SAM", "THF", "RDM", "WAR", "NIN", "PLD", "DRK", "BST"], [
    ("Flaming Arrow", "5"), ("Piercing Arrow", "40"), ("Dulling Arrow", "80"),
    ("Sidewinder", "175"), ("Blast Arrow", "200"), ("Arching Arrow", "225"),
    ("Empyreal Arrow", "Quest"), ("Refulgent Arrow", "290"), ("Apex Arrow", "Aeonic"),
    ("Namas Arrow", "Relic"), ("Jishnu's Radiance", "Empyrean"), ("Sarv", "Prime"),
])

w("Marksmanship", ["RNG", "COR", "THF", "WAR", "NIN", "DRK"], [
    ("Hot Shot", "5"), ("Split Shot", "40"), ("Sniper Shot", "80"),
    ("Slug Shot", "175"), ("Blast Shot", "200"), ("Heavy Shot", "225"),
    ("Detonator", "Quest"), ("Numbing Shot", "290"), ("Last Stand", "Aeonic"),
    ("Coronach", "Relic"), ("Wildfire", "Empyrean"), ("Trueflight", "Mythic"),
    ("Leaden Salute", "Mythic"), ("Terminus", "Prime"),
])

w("Automaton", ["Harlequin", "Stormwaker", "Sharpshot", "Valoredge"], [
    ("Slapstick", "0"), ("String Clipper", "0"), ("Chimera Ripper", "0"),
    ("Knockout", "150"), ("Cannibal Blade", "150"), ("Magic Mortar", "225"),
    ("Bone Crusher", "245"), ("String Shredder", "324"), ("Arcuballista", "(0)"),
    ("Daze", "(150)"), ("Armor Piercer", "(245)"), ("Armor Shatterer", "(324)"),
], note="Automaton skill values in brackets are ranged; the rest are melee. Frames replace the job columns.")

out = {"weapons": W}
path = "/home/claude/android/app/src/main/assets/weaponskills.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, separators=(", ", ": "))

# cross-check every WS name against skillchains.json so a typo can't ship silently
sc = json.load(open("/home/claude/android/app/src/main/assets/skillchains.json"))
known = {x["name"] for x in sc["weaponskills"]}
missing = []
for grp in W:
    for e in grp["ws"]:
        if e["n"] not in known and not e.get("np") and grp["type"] != "Automaton":
            missing.append((grp["type"], e["n"]))
print("weapons:", len(W), "ws rows:", sum(len(g["ws"]) for g in W))
print("no skillchain entry (unexpected):", missing)
print("no-property rows:", sum(1 for g in W for e in g["ws"] if e.get("np")))
