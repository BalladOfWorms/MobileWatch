#!/usr/bin/env python3
"""
Rebuilds MobileWatch-Unknown-Bucket-Review.md from live mobs.json.

The bucket is every record with no `fam` — what the Bestiary shows under Other > Unknown.
Sections are DISJOINT and assigned in precedence order, so they always sum to the bucket:

  2  zoned reals        — has a `zones` entry. Real bestiary gaps; needs a page.
  3  name-guessable     — no zone, but a family word appears in the name. One script.
     (CLASSIFIER: a family word anywhere in the name outranks an NPC keyword — that is
      what keeps `orcish fighterchief` out of the NPC pile.)
  4  NM-shaped, no zone — no zone, `nm` set.
  5  grid or kit        — no zone, not NM, but carries wk/st/ab/sp: real mob data.
  6  NPC-shaped / bare  — everything left. Needs a RULING, not screenshots.

Usage: python3 gen_unknown_review.py [assets_path] [out.md]
Author: BalladOfWorms
"""
import json, sys, re

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
OUT = sys.argv[2] if len(sys.argv) > 2 else "MobileWatch-Unknown-Bucket-Review.md"

with open(f"{ASSETS}/mobs.json", encoding="utf-8") as f:
    d = json.load(f)
mobs, families, family_eco = d["mobs"], d["families"], d["family_eco"]
abilities = d["abilities"]

# Family words to look for in a name. The file's own family list, plus the plural and
# a few forms BG uses that our taxonomy spells differently.
WORDS = {}
for fam in families:
    w = fam.lower()
    WORDS[w] = fam
    WORDS[w + "s"] = fam
    if w.endswith("y"):
        WORDS[w[:-1] + "ies"] = fam
EXTRA = {
    "lizard": "Hill Lizard", "lizards": "Hill Lizard", "gecko": "Hill Lizard",
    "bird": "Lesser Bird", "crow": "Lesser Bird", "raven": "Lesser Bird", "vulture": "Lesser Bird",
    "toad": "Frog", "frog": "Frog", "bones": "Skeleton", "draugar": "Skeleton",
    "hound": "Hound", "wyvern": "Wyvern", "dragon": "Dragon", "worm": "Worm",
    "crab": "Crab", "pugil": "Pugil", "leech": "Leech", "slime": "Slime", "bat": "Bat",
    "bee": "Bee", "beetle": "Beetle", "spider": "Spider", "scorpion": "Scorpion",
    "goblin": "Goblin", "orc": "Orc", "quadav": "Quadav", "yagudo": "Yagudo",
    "gigas": "Gigas", "fomor": "Fomor", "ghost": "Ghost", "skeleton": "Skeleton",
    "funguar": "Funguar", "mandragora": "Mandragora", "sapling": "Sapling", "treant": "Treant",
    "tiger": "Tiger", "sheep": "Sheep", "rabbit": "Rabbit", "raptor": "Raptor",
    "elemental": "Elemental", "golem": "Golem", "doll": "Doll", "bomb": "Bomb",
    "ahriman": "Ahriman", "morbol": "Morbol", "marid": "Marid", "chariot": "Chariot",
}
WORDS.update(EXTRA)
NPC_HINT = re.compile(
    r"\b(guard|soldier|trooper|sentry|officer|adventurer|mercenary|knight|dragoon|"
    r"ranger|monk|thief|bard|corsair|mage|healer|priest|acolyte|scholar|witness|"
    r"lieutenant|captain|commander|sergeant|general|colonel|major|private|recruit|"
    r"attendant|servant|merchant|trader|apprentice|initiate|pilgrim|scout|watcher)\b")


def family_word(name):
    for tok in re.split(r"[\s'\-,.]+", name):
        if tok in WORDS:
            return WORDS[tok]
    return None


# The rev-141 review marker. These records are NOT in the bucket any more — they were moved
# OUT of Other > Unknown by the literal-name sweep and stamped with a red X as their per-mob
# `img` so they stay obvious in the browser until the user has eyeballed them.
REVIEW_X = "mobimages/review_x.png"
xmarked = {k: v for k, v in mobs.items() if v.get("img") == REVIEW_X}

bucket = {k: v for k, v in mobs.items() if not v.get("fam")}
sec = {2: [], 3: [], 4: [], 5: [], 6: []}
for k, v in sorted(bucket.items()):
    guess = family_word(k)
    if v.get("zones"):
        sec[2].append((k, v, guess))
    elif guess:
        sec[3].append((k, v, guess))
    elif v.get("nm"):
        sec[4].append((k, v, guess))
    elif v.get("wk") or v.get("st") or v.get("ab") or v.get("sp"):
        sec[5].append((k, v, guess))
    else:
        sec[6].append((k, v, guess))

assert sum(len(x) for x in sec.values()) == len(bucket)


def row(k, v, guess):
    lv = v.get("lv")
    lv = f"[{lv[0]}, {lv[1]}]" if lv else "None"
    zone = (v.get("zones") or [[""]])[0][0]
    nm = "NM" if v.get("nm") else "  "
    tail = f" -> {guess}" if guess else ""
    return f"{k:<32}lv={lv:<16}{nm} {zone:<28}{tail}"


TITLES = {
    2: "Section 2 — zoned reals still needing a family",
    3: "Section 3 — family guessable from the name alone",
    4: "Section 4 — NM-shaped, no zone yet",
    5: "Section 5 — grid or kit, no zone, not NM-flagged",
    6: "Section 6 — NPC-shaped or bare (no zone, no grid, no kit)",
}
BLURB = {
    2: "On a zone page with a level, drops or resists. **These are bestiary gaps, not junk.** "
       "Each needs its own BG page — that is the screenshot pipeline.",
    3: "A family word sits in the name. One script could stamp the lot; the risk is the "
       "`Hill Lizard` / `Lesser Bird` class of trap, where BG's plural is not our family name.",
    4: "Flagged `nm` but with nothing else to place them. Most are battlefield or quest bosses "
       "that never appear on a zone roster.",
    5: "Carries real measured data — a resist grid, a kit or a spell list — but no zone. "
       "The biggest pile and the least examined.",
    6: "Nothing to go on: no zone, no grid, no kit, no family word. **Needs a ruling, not "
       "screenshots** — most look like allied NPCs rather than monsters.",
}

lines = [
    "# MobileWatch — Other > Unknown (fam=None) — working list",
    "",
    f"**Regenerated from live mobs.json at rev 365. Bucket: {len(bucket)} records.**",
    "",
    "**This file replaced the rev-by-rev handoff at rev 353** (user: *\"we are finalizing this project, not sure we need the handoff anymore, just finding unknowns\"*). Everything still open now lives in **Section A** (abilities needing definitions) and **Section B** (rulings, gaps and carried debt) at the bottom. It is regenerated from live `mobs.json` every rev, so it cannot drift.",
    "Sections are disjoint and assigned in precedence order (zone > name > NM > data > nothing), "
    "so they sum exactly to the bucket. Rebuild with `_project/gen_unknown_review.py`.",
    "",
    "## State of play",
    "",
    "| section | count | status |",
    "|---|---:|---|",
    "| 1 — duplicates | 0 | **CLOSED** at rev 335 — 37 records merged into their survivors, then "
    "deleted. A rev-361 typo scan turned up ~15 misspelled look-alikes elsewhere in the file; "
    "**the user reviewed and declined them (rev 362) — do not re-raise.** |",
    f"| 2 — zoned reals | **{len(sec[2])}** | **CLOSED at rev 344, reworked at rev 347.** The page "
    "batches ran rev 335 to rev 344; rev 347 took the last five that had pages. The residue is "
    "`boobrie` (two AI panels, neither names its family) plus four the user searched for and could "
    "not find — awaiting a delete/keep ruling. |",
    f"| 3 — name-guessable | {len(sec[3])} | **NINE OF TWELVE RESOLVED AT REV 347 — and the name "
    "guess was WRONG on three of them.** `muut's hound warrior` is a Skeleton, not a Hound; "
    "`vampyr wolf` is a Hound, not a Vampyr; `dragzagg's wyvern` is `Wyvern (Dragoon Pet)`, not "
    "`Wyvern`. Do not one-script the last three. |",
    f"| 4 — NM-shaped, no zone | {len(sec[4])} | **OPEN — worked from rev 348.** Most are "
    "battlefield, Voidwatch, Assault, Garrison or quest bosses that never appear on a zone "
    "roster; the summoner's own record often names both the zone and the family. |",
    f"| 5 — grid or kit, no zone | {len(sec[5])} | untouched |",
    f"| 6 — NPC-shaped or bare | {len(sec[6])} | untouched — needs a ruling |",
    f"| X — marked for review | {len(xmarked)} | **CLOSED at rev 368.** All 138 red-X records were "
    "cleared from screenshots between rev 356 and rev 368 — every one a full family stamp, not an "
    "`img` sweep. Two were deleted as junk (`iron bomb`, `nail bomb`) and one as a duplicate "
    "(`hydra`). See the last section for what the pass settled. |",
    "",
    "---",
    "",
    "## Rules this pass settled — carry these forward",
    "",
    "1. **Never overwrite a measured value with a directional one.** If the record stores "
    "`Ice +12.5%` and the page says only \"weak against Ice\", the numbers win. The stamp writes "
    "a field only where the record is empty, and logs everything it declines.",
    "2. **Un-numbered weak/strong text goes in as `[type, null]`** — a bare green Weak / red Res "
    "on the card, never a guessed magnitude.",
    "3. **Check every `ab` name against the abilities dict before writing it.** It is an assert "
    "in every stamp script now; the undefined-reference pile has not moved in five revs.",
    "4. **The mob page outranks the zone page.**",
    "5. **BG pluralises where we do not** — Elementals, Hounds, Orcs, Chariots, Gargouilles.",
    "6. **Grep the MOB KEYS before believing a page has named a new family, then check whether "
    "the word is an ECOSYSTEM.** BG's \"Lizards\" is our `Hill Lizard`, \"Birds\" is our "
    "`Lesser Bird`, \"Toads\" is our `Frog`, \"Bat Trio\" is our `Flock Bat`, \"Skeletons\" is "
    "our `Skeleton`, \"Cyhiraeth\" was already `Corpselight`. A "
    "`family_eco[\"Lizard\"]` lookup returns None and looks exactly like a missing family.",
    "7. **\"Delete\" means merge-then-delete** — the orphan side is usually where the level lives.",
    "7b. **THE `X's pet` SHAPE RESOLVES TO THE PET'S OWN FAMILY, AND WE ALREADY HAVE FAMILIES FOR "
    "IT.** Rev 141 held nine literal name matches back because the head noun disagreed with the "
    "family word. Rev 347 read their pages and every single held record went somewhere OTHER than "
    "the name guess. `Wyvern (Dragoon Pet)` already holds 26 `X's wyvern` records; `Flock Bat` "
    "already holds `gigas's bats`, `nosferatu bats`, `regiment's bats`. **Grep the roster for the "
    "name SHAPE, not just the family word.**",
    "8. **Guard placeholder levels, in both directions.** An `lv` of `[1, n]` is a placeholder: "
    "never union it over a measured band, and never let it survive a page that prints a real one.",
    "9. **Fuzzy-search before declaring a record missing.** `du'vha grimwind` is filed "
    "`du'vha grimewind`; `he'dho spatsurge` is `he'dho spatesurge`.",
    "10. **A page can name a family for mobs other than its own subject** — Aa'Bho Slashburner's "
    "page calls its five battle partners \"the other 5 quadavs\", which stamped all five.",
    "11. **A RED-X RECORD IS NOT JUST A MISSING ICON — IT IS A WHOLE UNSTAMPED RECORD.** The 138 "
    "were moved into their families at rev 141 by a NAME rule, long after those families had "
    "already been stamped, so they never got the family pass. All fourteen Goblins arrived at "
    "rev 356 with no `ab`, no `crys`, no `job` and a one-entry resist grid. **Clearing the marker "
    "without reading the page would have left fourteen blank records wearing the right icon.** "
    "Budget a real stamp per batch, not a one-line sweep.",
    "",
    "---",
    "",
]
for n in (2, 3, 4, 5, 6):
    lines += [f"## {TITLES[n]} ({len(sec[n])})", "", BLURB[n], "", "```"]
    lines += [row(*x) for x in sec[n]]
    lines += ["```", ""]

# ---------------------------------------------------------------- the X pile
byfam = {}
for k, v in sorted(xmarked.items()):
    byfam.setdefault(v["fam"], []).append(k)

# ---------------------------------------------------------------------------
# Section A — abilities we still need info on.
# Part 1 is computed live from mobs.json. Part 2 is the curated list of moves a
# page NAMED for a specific mob that the dict has never held: the proc scripts gate
# every `ab` write on the abilities dict, so these were written to `notes` instead
# and would otherwise be invisible. Add a name to ABIL_WANTED when a page names one.
# ---------------------------------------------------------------------------
undef = {}
for k, v in mobs.items():
    for a in (v.get("ab") or []):
        if a not in abilities:
            undef.setdefault(a, []).append(k)

# name -> (the mob whose page named it, what we know)
ABIL_WANTED = [
    ("Salamander Flame", "counselor gadalar",  "Gadalar's signature move, used alongside Manafont."),
    ("Typhonic Arrow",   "counselor najelith", "Listed in Special Abilities beside Eagle Eye Shot."),
    ("Victory Beacon",   "counselor rughadjeen", "Used alongside Invincible."),
    ("Meteoric Impact",  "counselor zazarg",   "Used alongside Hundred Fists."),
    ("Cataclysm",        "larzos",             "Favoured with TP; strong area-of-effect dark damage."),
    ("Forlorn Impact",   "larzos",             "Moderate radial AoE with knockback and paralysis."),
    ("Shield Bash",      "magic shields",      "Used constantly; the mob does not melee at all."),
    ("Trance",           "lilisette",          "Standard dancer ability, used repeatedly."),
    ("Sensual Dance",    "lilisette",          "Attack bonus for the user, attack down for its targets."),
    ("Thorned Stance",   "lilisette",          "Defense and magic defense bonus for the user."),
    ("Vivifying Waltz",  "lilisette",          "Heals HP."),
    ("Whirling Edge",    "lilisette",          "Damage."),
    ("Dancer's Fury",    "lilisette",          "Damage."),
    ("Pirate Pummel",    "lion",               "Single-target damage with a high damage-over-time Burn."),
    ("Powder Keg",       "lion",               "Conal damage with defense and magic defense down."),
    ("Grapeshot",        "lion",               "Conal damage, stun."),
    ("Walk the Plank",   "lion",               "Low-HP only, after a Gilgamesh prompt: AoE damage, knockback, bind, dispel."),
    ("Melancholy Jig",   "portia",             "Her two-hour; inflicts area-of-effect Doom."),
    ("Curing Waltz",     "portia",              "Dancer job ability, used on herself and others."),
    ("Healing Waltz",    "portia",              "Used when enfeebled \u2014 kiters should take care."),
    ("Sanguine Blade",   "ragelise",           "Sword weapon skill \u2014 a player WS the dict has never held."),
    ("Rancor Smash",     "ragelise",           "His two-hour; damage, knockback and Amnesia."),
    ("Evisceration",     "shikaree x",         "Dagger weapon skill (BG prints it \"Eviscoration\")."),
    ("Impulse Drive",    "shikaree z",         "Polearm weapon skill."),
    ("Ground Strike",    "zeid",               "Great sword weapon skill; the move he favours."),
    ("Abyssal Strike",   "zeid",               "Ranged attack with an additional effect of Stun."),
    ("Abyssal Drain",    "zeid",               "A fairly potent Drain skill."),
    ("Levin Wind",       "boobrie",            "Built up over the fight; creates area-of-effect hazards if left unchecked."),
    ("Becut",            "\u2014",                 "Carried debt from an earlier rev; needs creating."),
]
still_missing = [t for t in ABIL_WANTED if t[0] not in abilities]
_top2 = sum(len(undef.get(n, [])) for n in ("Amorphic Spikes", "Gush o' Goo"))

lines += [
    "## Section A \u2014 abilities we need info on",
    "",
    "Two separate problems. **Part 1 is already broken data**; **part 2 is data we chose not to "
    "write** rather than create a broken reference.",
    "",
    f"### Part 1 \u2014 names already referenced in `ab` that the dict does not define "
    f"({len(undef)} names, {sum(len(v) for v in undef.values())} uses)",
    "",
    "These render as a dead ability row in the app. **This count has been held flat for nine revs** "
    "\u2014 every proc script gates `ab` writes on the dict, so the pile has not grown; nothing has "
    "cleared it either.",
    "",
    "| ability | uses | example mobs |",
    "|---|---|---|",
]
for a in sorted(undef, key=lambda a: (-len(undef[a]), a)):
    ks = sorted(undef[a])
    lines.append(f"| `{a}` | {len(undef[a])} | {', '.join(ks[:3])}{' \u2026' if len(ks) > 3 else ''} |")

lines += [
    "",
    "Two names are almost the whole problem: **`Amorphic Spikes`** and **`Gush o' Goo`** account for "
    f"{_top2} of the {sum(len(v) for v in undef.values())} uses. The eleven single-use names on `zurko-bazurko` are "
    "a Rune Fencer's own weapon skills, runes and job ability (Fast Blade, Savage Blade, Seraph Blade; "
    "Ignis, Gelus, Flabra, Tellus, Sulpor, Unda, Lux; Lunge) "
    "\u2014 they may belong in `sp` or nowhere rather than in `ab`.",
    "",
    f"### Part 2 \u2014 named on a mob's page, deliberately NOT written ({len(still_missing)})",
    "",
    "A page named the move for a specific mob and the dict has never held it. Writing it to `ab` "
    "would have grown part 1, so it went to that mob's `notes` instead. **Every one of these is "
    "sourced and ready to define** \u2014 the mob it belongs to is in the table.",
    "",
    "| ability | named on | what the page says |",
    "|---|---|---|",
]
for a, mob, what in still_missing:
    lines.append(f"| **{a}** | `{mob}` | {what} |")
lines += [
    "",
    "Most of part 2 is job-NPC kits \u2014 the four Mercenary Camp counselors' signature moves, and "
    "Lilisette's and Lion's entire Heroines' Holdfast kits. **Defining these clears the whole block "
    "at once**; they are all sourced from one screenshot batch each.",
    "",
]

# ---------------------------------------------------------------------------
# Section B — everything still open that is NOT a bucket record. This lived in the
# handoff until rev 353; the handoff is no longer generated, so it lives here.
# ---------------------------------------------------------------------------
lines += [
    "## Section B \u2014 decision log and project history",
    "",
    "> **The list of things actually waiting on you now lives at the bottom of `MobileWatch-Bucket-List.md`**, written plainly and counted live. This section is the audit trail: every call made during the pass, why it was made, and what was deliberately left alone. Read it when you want to know *why* something is the way it is, not what to do next.",
    "",
    "**Calls made, and the reasoning behind them**",
    "",
    "- **REV 394 — A FILE-WIDE SWEEP FOR THE LAMIAE CLASS, AND THE HEADLINE IS A NEGATIVE RESULT.** The detector: *the mob's name contains a family name as a whole word, but `fam` says something else.* Raw, it returns 346 — useless, because **the 16 empty families are pure noise generators** (`Elementals`, `Lizard`, `weapon`, `treant` match half the file) and because a family whose name CONTAINS the hit is not a mismatch (Flock Bat vs Bat, Hill Lizard vs Lizard, Wyvern (Dragoon Pet) vs Wyvern). Excluding both leaves **79**. Every one was then tested against an INDEPENDENT witness — the record's own ability kit — and **in all 79 the kit matches the family it is filed under and not the family its name suggests.** `harpeia (nm)` carries the Khimaira kit, not the Harpeia one; `seed goblin` carries the Orc kit; `phlebotomic slug` the Leech kit; `belladonna (nm)` the Rafflesia kit; `bat eye` the Ahriman kit. **THE FAMILY COLUMN IS SOUND. The Lamiae case was never a family error at all — it was an eco override, which is a different bug.**",
    "- **A NAME-BASED DETECTOR IS ONLY AS GOOD AS ITS EXCLUSIONS, AND THE KIT IS THE WITNESS THAT SETTLES IT.** 346 → 79 came from two exclusions; 79 → 0 came from having a second, independent signal to check against. **Do not adjudicate a family from a name; adjudicate it from the kit, which the family stamp writes and the name does not touch.** (Same instrument as rule 420, where Mortobello's kit identified the family the page would not name.)",
    "- **WHAT THE SWEEP DID FIND WAS VOCABULARY AND SHAPE — values that are not wrong about the mob, but wrong for this file, so they render badly.** **63 `crys` values** outside the file's own set of eight elements plus `Varies`/`None`: `Light Crystal` x32, `Earth Crystal` x11, `Fire Crystal` x10 (the word “Crystal” leaked in from the page), `Thunder` x2 (this file calls that element `Lightning`), a truncated `N` x7, and a lone `Element`. **2 level ranges starting at 0** — `black baron` [0,75] and `seed crystal` [0,77] were rendering as “Lv 0-75”. **One stray `Escha - Ru'Aun`** against 77 records spelling it `Escha RuAun`, the same class as the `Qu'Bia Arena` stray at rev 389. **35 `zones` entries stored as bare strings** — never a crash risk (MobDb.kt:187 falls back to `e.toString() to null`), but `elemental circle` held BOTH shapes inside one record's list, which is the tell that it is an artifact. And **one glued spell string on `guimauve`**, eight spells run together; the split reconstructs the original byte for byte and every part is a name 43-501 other mobs already use.",
    '- **ALL FIVE NOW HAVE A LIVE LINE IN `audit.py`.** Non-vocabulary `crys`, reversed-or-below-1 level ranges, string-shaped `zones` entries, keys differing from `n.lower()`, and per-mob `eco` fighting `family_eco` — five new counters, all reading 0. **The rev-391 eco bug and the rev-389 key bug were both found by hand and could both have recurred silently; now they cannot.**',
    "- **ONE THING FOUND AND DELIBERATELY NOT FIXED.** The file has both `will-o'-the-wisp` and `will-o'the-wisp` — the second missing a hyphen, which is not a spelling the wiki uses. Same family, same grid, same detection, same crystal, same five-move kit; the properly spelled one has lv 22-36, Dark Knight, a 330s respawn and eight zones, the typo one has no level, no respawn and no zones. It is the `demishagin` / `vampyr wolf` shape. **Deleting a record that already has a family needs your word, so both stand and it is decision item 3.**",
    '- **REV 393 — THREE MORE ITEMS CLOSED, AND BOTH OF THE REV-390 CALLS HELD UP.** *“xuan wu, genbu type”* plus ten panels. **Item 1: confirmed.** The Qilin summon paragraph names all four in one line — Xuan Wu (Genbu), Bai Hu (Byakko), Qing Long (Seiryu), Zhu Que (Suzaku) — which is exactly the mapping the fold was derived from, so the Adamantoise stamp stands and all four picked up their aura and spell line from the same paragraph.',
    "- **ITEM 2 WAS CONFIRMED BY EVIDENCE THAT NEVER MENTIONS THE ANSWER.** `The Briars (Galka)` and `The Briars (Elvaan)` turn out to be **two separate pages**, each noting *“In battle, he is simply named The Briars”*. The untitled Battle Info panel names **both** as things it is stronger than, so it cannot be either one — and `the keeper` was right. **The identification never needed the cropped title; it needed the pages the panel pointed AT.** When a page compares itself to named siblings, the siblings' pages identify it by elimination. **Consequence raised as a new decision item: the file now carries neither Briars**, because the single `the briars` record went with the M-Z delete list and these two are real mission bosses in the same battlefield as `mistdagger` and `the keeper`.",
    "- **THE SIXTH QUADAV ANSWERED ITSELF.** `aa'bho slashburner`'s page prints **Weak to: Lightning** — the Quadav family table's biggest weakness at +50%, and a row the contradicted grid it was wearing did not have. That is independent confirmation of the *family wins here* ruling rather than a second application of it. Its page also names all six as one spawn set, so the shared mechanic (each casts one element; spells escalate Tier IV → Ancient Magic II → -aga III → an enfeebling or enhancing -ga as the others die) went on all six, along with the zone and spawn line the five were missing. **The five had no `nm` flag and Aa'Bho does; I set them to match and said so** — the page names all six as one set and every other Succor to the Sidhe spawn in the file is nm-flagged.",
    '- **TRIM A DANGLING SENTENCE, DO NOT DELETE IT.** The four ability notes that ended on a colon each stated something TRUE before the colon — `Lamb Chop` and `Sheep Charge` really do gain skillchain attributes under a Beastmaster\'s Ready, and `Horrid Roar` really does vary by wyrm. Those became complete sentences; only `Dust Cloud`, whose entire `notes` value was a bare `":"`, lost its note. **The tables did not contain the missing detail either, so the fix was always going to be editorial — but discarding the sentence would have thrown away the part that survived.**',
    "- **THE ABILITY TABLES ALSO CAUGHT A WRONG SHAPE NOBODY WAS LOOKING FOR.** `Dust Cloud` was stored as a **10' cone** with `tgt: Cone AoE`. Its table's Area column reads **AoE**, and the same table's legend lists `Conal` as a separate value it could have used — so the cone was invented somewhere upstream. Corrected to a 10' AoE. `Horrid Roar` also moved off `Enfeebling`, which is not one of BG's four categories, to `Magical` per its Type icon, and its description gained *wipes shadows*. **A panel fetched to answer one question is worth reading for the fields you did not ask about.**",
    '- **REV 392 — `Amorphic Spikes` DEFINED, AND LOOKING FOR A HOUSE STYLE TO COPY TURNED UP SOMETHING WORSE.** The ask was one def: 32 Flan-type mobs pointed at a name the `abilities` dict did not have, so undefined references fell 49 → 17 and distinct names 17 → 16 in one write. **But grepping existing defs for a Blue-Magic-shaped example found two whose `d` field was AN INTERWIKI LINK INSTEAD OF A DESCRIPTION**: `Magic Fruit` read `de:Magische Frucht`, and `Sheep Song` read `de:Schafliedja...Category:MagicCategory:Blue MagicCategory:Mob Abilities`. **That is the sixth flavour of leaked wiki markup, and `audit.py` could not see either one** — every pattern in its regex wants brackets, and an interwiki prefix has none. It had been scoring 0 file-wide with these sitting in it.',
    "- **NEITHER FIX WAS A GUESS.** `Magic Fruit` already carried the real description in its `notes` (*heals 3000+ HP, erases status, resets the hate of the highest-hate player*) — that was promoted into `d` and the now-duplicate note dropped. `Sheep Song`'s own structured fields already said what it does — `t: Magical`, `tgt: AoE`, `fx: [Sleep I]` — so its description was written from those. **When a description is garbage, look at the rest of the record before looking anything up; the fact is usually already in the file, just in the wrong field.**",
    '- **EXTENDING THE DETECTOR IMMEDIATELY PRODUCED A FALSE POSITIVE, AND THAT WAS ALSO A REAL BUG.** The new interwiki pattern flagged `Lamb Chop`, `Sheep Charge` and `Horrid Roar` — because audit.py concatenates `d` + `notes` + `r` + `tgt` **with no separator**, so a note ending *“Skillchain Attributes:”* followed by `r: Melee` reads as `es:M`, an interwiki prefix. Fixed by joining the fields with a newline. **Then the false positive turned out to be pointing at something true:** those notes END ON A COLON because the wiki had a table there and the scrape stopped. A dedicated check now counts them and finds **four** — the fourth, `Dust Cloud`, was invisible while the concatenation bug was masking the boundary. New decision item.',
    '- **REV 391 — YOUR ANSWERS APPLIED. The decision list went from 14 items to 4.** Closed: the `nmlv` sweep, the bogus grid labels, the malformed immune values, the 5 Quadav grids, the 4 Contantican NM flags, the Shikaree sisters, the hpedme spelling, and six *leave as is* rulings. **What is still open is two confirmations from rev 390 and two things this rev surfaced.**',
    '- **THE `job` COMMA WAS NEVER MALFORMED — I HAD READ A REAL FORMAT AS A TYPO.** I had been asking to normalise 901 `job` strings because they “use commas where the rest of the file uses slashes”, and singled out the 52 Worm records reading `Black Mage / Black Mage, Red Mage` as “the same job twice”. **USER: “It is saying BLM main job with BLM subjob or RDM as job.”** The slash is main/sub and the comma is *or* — so that string is three correct facts, not one duplicated one. **Only the three-letter codes were expanded (759 records); every separator was left exactly as written.** LESSON: before calling a recurring format malformed, check whether it encodes something the reader knows and you do not — a pattern that repeats 52 times is more likely a convention than a typo.',
    "- **A PER-MOB `eco` OVERRIDE BEATS `family_eco`, AND THAT IS HOW A LAMIA ENDED UP IN VERMIN.** USER: *“we have a lamiae in vermin, chigoe breeder, should be beastmen”*. The record's `fam` was already `Lamiae` and correct — the bug was a per-mob `eco` of `Vermin`, which the card reads as `mob.eco ?: familyEcoMap[fam]`, so the override won and the browser filed it under Vermin. The NAME had made the import follow Chigoe. **Fixed by DELETING the key, never by setting it null** (the Yggdreant lesson). **Turning the symptom into a file-wide detector — per-mob eco that disagrees with its family's eco — found exactly one more: `sang buaya`, filed `Bugard` but overriding to `Beast` when Bugard is `Lizard`.** The other 188 per-mob eco keys agree with their family and are harmless. **A user-reported symptom is worth generalising into a detector; the second one is free.**",
    "- **“PUT IT IN THE NOTES” HAD THREE DIFFERENT ANSWERS, NOT ONE.** You ruled that the non-grid resist rows belong in a mob's notes. Nine became prose (`Susceptible to Petrify`, `Only takes piercing damage`, `Resists Sleep and Stun`). But **seven rows — the five `Damage Taken` on the Replica prototypes and `Dark Earth` on `malodorous mort` — carried no percentage at all**, so there was no fact to move and writing “takes damage” would have invented one; they were dropped and reported. And **`jailer of fortitude`'s `Magic Damage` / `Physical Damage` were RENAMED to `Magical` / `Physical`** — the grid's own labels written longhand, so they now render as real cells instead of being demoted to prose. That is the one place I did not follow the instruction literally, and it is called out in the doc.",
    "- **THE `nmlv` SWEEP LOST NOTHING SILENTLY.** All 35 removed per your answer; 27 simply restated the record's own `lv`. **The other 8 held a different number and the doc now carries them, because after the sweep the doc is the only place they exist:** foul meat, hilltroll mirror guard, magnes quadav, minotaur (its value was `?`, which was never data), mountain worm, nickel quadav, odontotyrannus, orobon. **Mountain Worm is already on the category-table-is-staler-than-the-mob-page list.** When a sweep is authorised, print what differs before deleting it — the instruction was right and the record still deserves to survive somewhere.",
    "- **THE FIVE QUADAV GRIDS WERE STAMPED AND THE SIXTH WAS NOT, ON PURPOSE.** You said *family wins here* about the five you listed. **`aa'bho slashburner` is in the same Rolanberry Fields [S] group with the identical contradicted grid**, and it is the record whose page carried the bare `Lightning` weakness that made the family grid right in the first place. Scoping to your list and asking about the sixth beat quietly widening the sweep — but leaving one of six behind re-creates exactly the inconsistency the fix was for, so it is now decision item 3.",
    "- **REV 390 \u2014 THE BUCKET IS AT ZERO.** 15 panels + a 19-name delete screenshot. 19 + 15 = 34 "
    "= the entire bucket, so every surviving record got exactly one instruction. Final shape: "
    "**16 folded, 18 deleted** \u2014 the two numbers differ from 15/19 because of the hold and the "
    "panel-identification call below. **`fam=None` now reads 0 in audit \u00a71, the browser has no "
    "unfamilied group, and `mobsForContent` has no unfamilied roster rows.**",
    "- **THE UNTITLED PANEL: I READ IT AS `the keeper`, AND THE WHOLE BATCH TURNS ON THAT.** The "
    "screenshot is cropped above the page title \u2014 it opens at *Battle Info* \u2014 and BOTH `the "
    "briars` and `the keeper` were in the bucket. Three independent checks agree: (a) the delete "
    "screenshot names The Briars and not The Keeper, so this reading is the only one where all 34 "
    "records get exactly one instruction and nothing is double-booked \u2014 the rule-419 test, run "
    "forwards; (b) the page says *stronger than Mistdagger, The Briars (Galka) and The Briars "
    "(Elvaan)*, and `mistdagger` and `the briars` are both lv 108 while `the keeper` is lv 110; "
    "(c) the page says Job: Scholar and names Kaustra, which fits `the keeper`\u2019s stored elemental "
    "nuke list, not `the briars`\u2019 WHM/RDM enhancing list. **Recorded as decision item 2 so it is "
    "reversible.** `the keeper` was built on `mistdagger`\u2019s template \u2014 same battlefield, same "
    "spawn line, same Humanoid family.",
    "- **`xuan wu` WAS ON THE DELETE SCREENSHOT AND I HELD IT (rule 419, second occurrence).** It is "
    "the fourth of the four Voidwatch guardians Qilin summons, and the other three were all "
    "accounted for: `bai hu` (Tiger) and `qing long` (Wyvern) were stamped in an earlier pass with "
    "zones, `ab: []` and a `Summoned by Qilin (1 per Qilin)` spawn line, and this same batch folded "
    "`zhu que` off its own panel. All four are lv 98-99, NM-flagged, in The Shrine of RuAvitau. "
    "**Folded to Adamantoise** \u2014 Xuan Wu is the Black Tortoise, and the file already files that "
    "same guardian under his other name, `genbu`, as Adamantoise. Its water spell list (Water IV, "
    "Waterga III, Flood, Drown) agrees. Decision item 1; one line reverses it.",
    "- **THE FOUR GUARDIANS RESOLVE THROUGH THEIR OTHER NAMES, AND ALL FOUR AGREE.** `zhu que` = "
    "Suzaku \u2192 Greater Bird; `xuan wu` = Genbu \u2192 Adamantoise; `bai hu` = Byakko \u2192 Tiger; "
    "`qing long` = Seiryu \u2192 Wyvern. **Zhu Que got a second, independent route: its page says "
    "`Family: Rocs`, and `Roc` is not a family in this file \u2014 but `roc` and `simurgh` are both "
    "filed `Greater Bird`.** Two unrelated derivations landing on the same family is as close to "
    "proof as this pass gets. (Same shape as rule 426: a page\u2019s family label is a word, resolve "
    "it through the members.)",
    "- **A DARK KINDRED BATTALION\u2019S TROOPS DO NOT SHARE THEIR LEADER\u2019S FAMILY \u2014 THREE OF FOUR "
    "DIFFER.** The four leaders were filed at rev 387: `shadowbreath` is a **Vampyr** but "
    "`shadowbreath defiler` is a Demon; `shadowfang` is a **Demon** but `shadowfang void` is an "
    "Elemental; `shadowsoul` is a **Demon** but `shadowsoul devourer` is a Dragon. Only "
    "`shadowwing` / `shadowwing infuriator` match (both Gargouille). **Do not infer a battalion "
    "member\u2019s family from its leader.** Related loose end: `shadowhind machinator` is the one "
    "battalion record whose page carries no *Led by* line, and there is no `shadowhind` record in "
    "the file \u2014 either that leader was never imported or the unit has none.",
    "- **TWO ELEMENTALS WERE STAMPED WITH SWIPE SETS, AND THE SCRIPT ASSERTS THE MATCH.** "
    "`shadowfang void` (page: weak Light, strong Dark) took the **Dark** set and `touched gefyrst` "
    "(page: *Elementals, Water/Ice themed*) took the **Gefyrst** hybrid set, whose Ice -95%% / "
    "Water -95%% is that description exactly. **This only works if the member\u2019s grid matches a set "
    "BYTE FOR BYTE** \u2014 the guard at AuctionApp.kt ~589 drops a non-matching member back to a plain "
    "grid \u2014 which is why both use `Blunt` and not `Impact`. The script asserts equality against "
    "`family_resist_sets` before writing. **Follow-up: `bergschrund gefyrst` and `gullin gefyrst` "
    "still carry the thin \u00b125%% import shape and will NOT swipe.**",
    "- **THE r357 GARRISON RULING WAS APPLIED TO THREE RECORDS AND DELIBERATELY WITHHELD FROM TWO.** "
    "`orcish colonel`, `orcish fighterchief` and `sagittarius xiii-xxvi` are Garrison records with "
    "the one-entry `+25%%` import grid, so the family table won \u2014 that is the ruling verbatim. "
    "**`monarca de altepa` kept its own grid**: it is Fields of Valor rather than Garrison, and its "
    "two entries (Ice, Dark) are exactly the two weaknesses its page prints. **`treefeller snogrog` "
    "kept its own grid too, and this one is a real conflict**: the Orc family table is weak to six "
    "elements, while its page prints only *Weak to: Water* and a player note saying it *seems "
    "extremely resistant to elemental magic*. Both of its own signals point away from the family "
    "table, so I left it and wrote the note.",
    "- **A CROSS-REFERENCE CHECK THAT SEARCHES WHOLE RECORDS PRODUCES FALSE POSITIVES.** The "
    "pre-flight flagged `royal knight` as referenced \u2014 the hit was `ancient royal knight`, a "
    "different Skeleton whose own `n` contains the string. **A mob\u2019s own name is not a reference "
    "to another mob.** The check now searches only `notes` / `spawn` / `drops`. It also now "
    "separates prose mentions written in the same rev: `the keeper`\u2019s new note names *The Briars "
    "(Galka)* and *The Briars (Elvaan)*, which are the wiki\u2019s race variants and not the plain "
    "`the briars` record being deleted \u2014 reported, not blocking.",
    "- **`swamp muck` AND `go\u2019rha sludgewater` CONFIRMED EACH OTHER FROM OPPOSITE DIRECTIONS.** The "
    "Quadav was filed long ago with the note *Assisted by ten Swamp Mucks*; the Swamp Muck panel "
    "says it spawns with Go\u2019Rha Sludgewater and shows 10 spawns. With `treefeller snogrog` this "
    "batch and `laa heha` / `laa vaqu` last rev, the **Succor to the Sidhe** set is now 36 records "
    "across 19 families, every one of them in an `[S]` zone.",
    "- **REV 389 \u2014 THE A-L SLICE: 12 PANELS FOLDED, 18 DELETED, AND THE UNION CHECK PASSED "
    "CLEANLY THIS TIME.** Rule 419 (the `shayaam` collision) says to check the delete screenshot "
    "against the panel batch before touching anything. Here the two sets are disjoint: the "
    "screenshot is the bucket slice `Aragoneu Knight` \u2192 `Luminous Coalescence` (29 records) "
    "with the 11 panel names lifted out of it, leaving 18, and `Malodorous Mort` is the 12th panel "
    "sitting one row past the end of the slice. 18 + 12 = 30, no overlap, all 30 inside the 64. "
    "**The arithmetic reproducing exactly is what licensed the batch.**",
    "- **`Structures` IS NOT A FAMILY IN THIS FILE, SO TWO PAGES THAT BOTH SAY `Family: Structures` "
    "LANDED IN DIFFERENT FAMILIES.** The Structures *ecosystem* holds five families \u2014 Gyve, "
    "Structure, Obstacle, Lair, Environment \u2014 and the wiki\u2019s single label maps onto whichever "
    "one the mob behaves like. **`brittle rock` \u2192 Obstacle** (a destructible wall, exactly "
    "`bedrock crag` / `icy palisade` / `monolithic boulder`); **`esoteric scrivening` \u2192 Gyve** "
    "(an immobile boss-summoned hazard field whose element matches the summoner \u2014 which is "
    "`crystal fetter`\u2019s definition word for word, down to the elemental aura). **A page\u2019s "
    "family label is a word, not a key; resolve it through the members.** Same shape as rule 420 "
    "(Kindred \u2192 Demon).",
    "- **THE ESOTERIC SCRIVENING GRID WAS REPLACED, AND THAT IS THE ONE CALL HERE WORTH ARGUING "
    "WITH.** It stored the 8-elements-at--50%% import default \u2014 byte-identical to `bedrock crag`\u2019s "
    "\u2014 while **its own notes, written from its own page, say it is extremely physically resistant "
    "and highly vulnerable to magic.** The Gyve family grid says exactly that (weak to all eight "
    "elements, strong to all six physical types). So the stored grid contradicted the record\u2019s own "
    "prose, and the family grid agreed with it. Swapped to the Gyve grid. **If the import default "
    "was actually measured, this is the line to revert.**",
    "- **A MISSPELLED KEY HID A RECORD FROM ITS OWN SIBLINGS.** `demishagin white mage` sat orphaned "
    "in the bucket while `demisahagin bard`, `demisahagin dragoon` and `demisahagin monk` sat "
    "complete and stamped Sahagin \u2014 same level, same zone, same Expeditionary Force spawn line, "
    "same four-move kit. The page title spells it `Demisahagin`, so three siblings and the source "
    "all outvote the file. Key and `n` both corrected, and the White Mage inherited the sibling "
    "template wholesale. **A key/name equality guard now runs in the proc script; it found exactly "
    "one more file-wide, `onycophora\u2019s sandworm` \u2192 `onychophora\u2019s sandworm`, also fixed. "
    "The check now reads 0.** This is the r200 lesson pointed the other way: fuzzy-search before "
    "declaring a mob missing, *and* check whether the file is the thing that is wrong.",
    "- **THE BAD `[Sight, True Sight]` STAMP WAS CLEARED ON THREE MORE RECORDS, BUT `lnk` WAS NOT "
    "TOUCHED \u2014 AND THE DIFFERENCE MATTERS.** `bopa greso`, `cha lebagta` and `malodorous mort` all "
    "print a Notes column that names its detection explicitly (`A, L, T(S)` twice, `A, T(S)` once), "
    "so `det` became `[\"True Sight\"]` on all three. That is the documented per-family cleanup of a "
    "known-bad import stamp, not an inference from silence. **`malodorous mort` carries `lnk: true` "
    "and its Notes column does not print `L` \u2014 that flag was left alone**, because there is no "
    "known-bad `lnk` stamp and omission is not contradiction (the Simorg precedent). Same reasoning "
    "left `fourth spitewarden`\u2019s imported `det` in place: its column prints only `A`.",
    "- **`Essence Jack` DEFINED FROM THE PAGE, WITH `t` AND `el` LEFT UNSET.** The Fourth Spitewarden "
    "page describes what it does in full \u2014 Terror plus all-stats-down on the cloned player, and a "
    "damage spike on the Spitewarden that looks like it absorbs what it drains \u2014 but never names a "
    "Type or an element. Those stay unset (the Quake Blast / Gravitic Horn precedent). The "
    "out-of-range chase behaviour went in the def\u2019s `notes`, where the page put it: it is not a hate "
    "reset and it stops the moment the ability lands. **Undefined ability references did not move: "
    "49 across 17 names, before and after.**",
    "- **THE TWO ABILITIES I DID NOT ADD.** `Asuran Fists` (Atori-Tutori) and `Evisceration` "
    "(Bopa Greso, Cha Lebagta) are player weapon skills, and putting them in `ab` would have "
    "manufactured three fresh bare names \u2014 the exact class decision item 10 is asking you to fix "
    "with a Kotlin fallback. Both went into the notes instead, where they read fine and cost "
    "nothing. **Do not grow item 10 while item 10 is still open.**",
    "- **`incandescent baelfyr` WAS THE ONLY NM-FLAGGED DELETE, AND IT TOOK DECISION ITEM 8 DOWN "
    "WITH IT.** It was one of the six records sharing the suspicious `125-126` band with no zone; "
    "that item now measures **5**. It also carried a hybrid-elemental name \u2014 `Baelfyr` is one of "
    "the four hybrid resist sets in the Elemental family (with Gefyrst, Ungeweder, Byrgen) \u2014 and "
    "`touched gefyrst` is still sitting in the bucket at `121-122`. **If those two were a pair, half "
    "the pair is now gone.** Flagging it rather than quietly not mentioning it; the record itself "
    "held nothing but a spell list, a grid and a level.",
    "- **ONE STRAY ZONE STRING NORMALISED.** 49 records store `QuBia Arena` (the `zones.json` form) "
    "and exactly one stored `Qu\u2019Bia Arena`, which would have split the arena into two headers in "
    "the Zone view. Folded into this rev because the Atori-Tutori fold was writing that zone anyway.",
    "- **The eight rev-347 leftovers were never deleted.** You said the residue \"can be removed\"; "
    "six of the eight carry measured data that exists only in that record. `darrcuiln` is the "
    "richest \u2014 5 abilities, 4 drops, Rala Waterways [U], a Sinister Reign spawn line and **its own "
    "art at `mobimages/darrcuiln.png`**; its own note reads *\"Likely classified as a Beast.\"* "
    "`cardian prototype` holds a 39-spell list and **`Cardian` is a live family**, so it may be a "
    "stamp rather than a delete. **`savage hound condottiere` is the only clean delete** \u2014 "
    "`det: [Sight]` and a name.",
    "- **`vampyr wolf` vs `vampyr dog` \u2014 probable duplicate, not merged.** The panel's own text says "
    "the term *\"most accurately refers to the Vampyr Dog\"*; both are lv [75, 80] `nm` Hound "
    "Einherjar records. But their stored grids and `det` differ, so merging would destroy measured "
    "data. **CLOSED at rev 388** \u2014 you confirmed the Dog is real and the Wolf is not; the Dog was filled from its panel and the Wolf deleted as the thinner duplicate.",
    "- **THE ONE-ENTRY LEGACY RESIST GRID — RULED ON AT REV 357, AND ~150 RECORDS STILL CARRY IT.** "
    "The rev-356 open asked whether `wk: [[Light, +25%]]` on the red-X Goblins was measured data. "
    "**USER: keep the family resist table for Garrison-type mobs — they are low level and old, so "
    "they were not re-tuned for the event.** So the one-entry `+25%` grid is an IMPORT DEFAULT, not "
    "a measurement, and the family table wins. Applied at rev 357 to the 15 Garrison records "
    "(11 Goblin, 4 Antica) and to both Section-X batches. **~150 records file-wide still hold a "
    "one-entry `+25%` grid** — the big blocks are 73 unfamilied (they have no family table to fall "
    "back to), 21 Replica, 6 Adversary Avatar, 6 Orc, 5 Elemental, 4 Velkk. **The ruling generalises "
    "but was NOT swept**: outside Garrison, some of those may be genuine content re-tunes. Wants a "
    "sweep decision per family, not one script.",
    "- **TEN DEMON PAGES CONTRADICT THE REV-56 FAMILY `det` STAMP, AND THE PAGES OUTNUMBER IT.** "
    "Rev 56 stamped `det: [Sight, Sound]` on all 112 Demons off an icon crop of the category page. "
    "All ten red-X Demons carry `[Sight, Scent]` from the import — and every one of their ten mob "
    "pages prints **A, L, S, Sc** in the Notes column, whose legend separates `S` (sight), `H` "
    "(sound) and `Sc` (scent) explicitly. Rule 4 says the mob page wins, so rev 357 left the ten at "
    "`[Sight, Scent]`. **That leaves the family split 112 / 10 on a fact that should be uniform.** "
    "Either the rev-56 speaker-vs-flame icon read was wrong (and 112 records need correcting), or "
    "the Notes column and the Detects box mean different things. Wants one clean look at a Demon "
    "category Detects box.",
    "- **The four Contanticans are flagged `nm` and should not be — REV 359 CONFIRMED THE MECHANISM, "
    "only the ruling is missing.** Their banner reads \"Expeditionary Force\", not \"Notorious "
    "Monster\", and rev 359 saw both banners side by side inside one family: four Gigas pages print "
    "**Expeditionary Force** in the red slot (Beastmaster, Monk, Ranger, Warrior — none NM-flagged, "
    "and they carry the identical `Beastman's Banner` spawn string as the Contanticans) while three "
    "print **Notorious Monster** (Clearcutter, Hillrazer, Overseer — all NM). **The red line is a "
    "banner slot, not an NM marker.** Still folded into the carried \"clear the 23 ADVERSARIES-row "
    "`nm` flags\" sweep rather than cleared ad hoc.",
    "- **`pakecet` IS FILED `Pteraketos`, BUT THE PANEL FOR IT SAYS PUGIL.** Rev 358 zoned its add "
    "`pakecet's pugil` to Escha RuAun on the user's ruling that the ADD is a Pugil (it already was). "
    "The same panel calls **Pakecet itself** *a massive Pugil (fish family)*, while our record has it "
    "as `Pteraketos` with a full measured grid and a Tier 3 Geas Fete tag. **Pakecet was NOT touched** "
    "— a panel does not outrank a page-built record. Flagged only because a summoner and its add "
    "sitting in different families is worth one look.",
    "- **THE ANTICA IMPORT GRID LEAKED ACROSS FAMILIES, AND IT NAMES FIVE ORPHANS.** Rev 362 found "
    "the four red-X Velkk wearing `wk [Wind +25] / st [Earth -50, Dark -50]` — the **Antica** "
    "default, not a Velkk grid (27 of 33 Velkk hold `wk [Lightning +30, Ice +30] / st [Water -50, "
    "Dark -30]`). Replaced. **The other holders of that grid are the tell:** the 4 Contanticans "
    "(Antica) and **five fam=None orphans — `hastatus xiii-xxv`, `xiii-lxxv`, `xiii-xcvi`, "
    "`xiii-cxxviii` and `sagittarius xiii-xxvi`.** Those five match the `<Roman rank> XIII-<numeral>` "
    "shape of `centurio xiii-v`, `decurio xiii-lv`, `princeps xiii-lxxxix` and `triarius xiii-lix`, "
    "all four already **Antica** Garrison records. **Name AND grid agree — the double corroboration "
    "rev 360 said was the combination worth acting on.** Five records, one word from you; NOT "
    "stamped, since no page was supplied.",
    "- **!! SIX NPC-TYPE RECORDS SIT IN THE BESTIARY — DELETE THEM TOO?** `poroggo prince` and "
    "`poroggo servant` (rev 363) and `qiqirn bewitcher`, `qiqirn freelance`, `qiqirn trapper` "
    "(rev 364) are all headed **Type: NPC** on BG, with a Location line instead of a zone table "
    "and an Affiliation field — campaign allies, Bastion resistance fighters and an Al Zahbi "
    "mercenary, not spawns you fight. **The Qiqirn three even carry an `Occupation` field.** "
    "**Rev 367 adds a sixth: `patrol worm`, headed Type: Campaign Battle NPC**, Location Fort Karugo-Narugo [S], Affiliation Windurst [S] — a squadron of Nyumomo pets that never moves. "
    "Rev 362 deleted `iron bomb`/`nail bomb` as *not relevant to the bestiary*; this is the same "
    "question, six records wide. **All six stamped normally rather than removed** — the call is "
    "yours, and undoing a stamp is cheaper than undoing a delete.",
    "- **`poroggo servant` IS FILED UNDER `Bestiary: Toad` ON ITS OWN PAGE, NOT Poroggo.** Its "
    "infobox says Toad (our `Frog`, review rule 6) while `poroggo prince`'s infobox on the very next "
    "page says **Poroggo**. Two members of one campaign group filed in two families by BG itself. "
    "**NOT re-stamped** — a family move is your call, and the name plus the Prince both point the "
    "other way. (`poroggo's toady` and `flume toad` are already `Frog`, so the split is real.)",
    "- **THE POROGGO GRID IS THE FIRST CASE WHERE THE TWO GRID TESTS DISAGREE — LEFT ALONE.** All "
    "five red-X Poroggo carry `wk [Ice +12.5, Lightning +12.5] / st [Water -50, Light -50]`, a "
    "cohort of exactly those five, which is the import-default signature. **But `poroggo gourmand`'s "
    "page prints \"Weak to: Ice, Lightning\" and \"Strong to: Water\" — matching THIS grid and "
    "contradicting the 15-member family grid, where Ice is a −30% RESIST.** Overwriting would have "
    "swapped a page-corroborated grid for a page-contradicted one. The other four have no readable "
    "grid data (two are NPC pages, one box is blank, one set of icons is unreadable). Wants a "
    "ruling: is this a real variant grid for the five, or a coincidence?",
    "- **THE CIRDAS `[125, 126]` PATTERN — FIVE RECORDS NOW, ACROSS FIVE FAMILIES.** "
    "`wetscale toad`'s page measures **119-121 in Cirdas Caverns**, `coagulum acuex`'s (rev 358) "
    "says **120-122**, `drearyeyed bat`'s (rev 360) says **119-121** and `fulvous bats`'s (rev 361) "
    "says **119-121** — and all four records held exactly **`lv [125, 126]`** with NO zone stored. "
    "Frog, Acuex, Bat and Flock Bat: an IMPORT artifact, not a family quirk. `Cirdas Caverns [U]` "
    "is a separate zone and is **not in zones.json**, so a [U] roster had nowhere to land — which "
    "is exactly how a [U] band ends up glued onto a base-zone record with no zone. **No `lv` was "
    "overwritten until rev 366, which broke that habit for the first time:** `plodding funguar`'s "
    "page prints **119-121 in Cirdas Caverns** and its record held `[125, 126]` with no zone at "
    "all, so the band WAS replaced and the zone written. Five for five now, every page measuring "
    "119-122. One ruling covers the rest: grep the file for `lv == [125, 126]`, decide whether "
    "they are Cirdas Caverns [U] bands, and decide whether [U] needs to exist in zones.json.",
    "- **A GRID FINGERPRINT CAN NAME AN ORPHAN'S FAMILY — 87 of the 337 hold a grid that exactly "
    "one family holds.** Found at rev 360 while ruling on the Bat grid. Biggest blocks: Orc 11, "
    "Sheep 10, Tonberry 8, Goblin 8, Elemental 6, Gigas 5. Many corroborate on the NAME as well "
    "(`demisahagin bard`→Sahagin, `halforc dragoon`→Orc, `giant monk`→Gigas, `cow/bull/calf [herdN]`"
    "→Sheep, `cook fulberry`→Tonberry), which is the combination worth acting on. **TWO REAL FAILURE "
    "MODES, so this is a lead generator and NOT a stamp script:** (1) a grid held by only ONE member "
    "is unique, not a fingerprint; (2) if the cohort holding a grid is itself unstamped the pointer "
    "goes to the wrong family — `balayang` and `desmodus` now point at **Flock Bat** purely because "
    "rev 360 moved the eight red-X Bats off that import grid and left the Flock Bats sitting on it. "
    "Both are almost certainly **Bat** (`desmodont` already is). Worth a pass; worth screenshots more.",
    "- **!! I MOVED A MOB BETWEEN FAMILIES ON THE PAGE'S WORD — `pixie impaler` IS NOW A `Bee`, "
    "NOT A `Pixie`.** Rev 363 declined exactly this for `poroggo servant` because the evidence "
    "conflicted. Here it does not: its BG infobox reads **Family: Bees**, its grid twin is "
    "`flitting bee` (already `Bee`), and the file ALREADY does this for the same quest — "
    "**`pixietrap` is filed `Flytrap`** and `stabnix skewerfinger`, the mob it spawns beside, is "
    "filed `Goblin`. *Succor to the Sidhe* uses \"Pixie\" as a THEME PREFIX across several "
    "families, so the word in the name is not a family claim. **Say the word and it goes back.**",
    "- **`hydra` WAS A DUPLICATE OF `hydra (nm)` AND WAS MERGED THEN DELETED (review rule 7).** "
    "The screenshots were the *Hydra (Notorious Monster)* page, and `hydra (nm)` already held that "
    "page's exact resist grid, kit, crystal, job and notes — while the red-X `hydra` held the same "
    "monster's level, respawn, spawn line and `nmlv` and nothing else. Those four fields moved "
    "across first. **mobs 6970 → 6969.** Hydra was one of the old `fam=None` orphans, which is "
    "how the pair got made in the first place.",
    "- **THE `wk [Piercing +25, Ice +25]` GRID IS CLOSED — BOTH HOLDERS WERE IMPORT DEFAULTS.** "
    "`pixie impaler` (rev 366) and `flitting bee` (rev 367) were its only two records, and both "
    "sources name Ice and Piercing as the weaknesses — which are exactly the two LARGEST entries "
    "in the 57-member **Bee** family grid (`Ice +50`, `Piercing +25`). A two-entry grid that names "
    "the family grid's top two is a truncation of it, not a variant. Both now carry the family grid.",
    "- **A PANEL AND A RECORD DISAGREE ON A LEVEL: `warder's phuabo`.** The panel says **120**, the "
    "record says **123**. Neither was touched — a panel does not outrank a stored band (the "
    "`pakecet` precedent). Its siblings `warder's xzomit` (123) and `warder's ghrah` (124) suggest "
    "the stored value is right and the panel is rounding to the content tier.",
    "- **!! ~130 RECORDS CARRY A COMMA-SEPARATED OR DOUBLED `job` STRING, AND 52 OF THEM SAY THE SAME "
    "JOB TWICE.** Found at rev 367 while stamping the Worms. **52 Worm records store "
    "`\"Black Mage / Black Mage, Red Mage\"`** — Black Mage listed on both sides of the slash. Others: "
    "`Dark Knight, Black Mage` (20), `Black Mage, Warrior` (16), `Black Mage, Thief, Dark Knight, "
    "Dragoon` (16), `WAR, DRK, BLM, SMN` (12), `Dark Knight, Black Mage / Black Mage, Thief` (7). The "
    "documented long form is slash-separated full job names, so this is three defects in one class: "
    "commas instead of slashes, three-letter abbreviations that were supposed to be expanded, and a "
    "duplicated job. **Every one renders verbatim on the card.** The two Worms stamped this rev got "
    "the clean `Black Mage` (10 members already hold it) rather than the malformed majority. Wants "
    "one normalisation sweep, which is cheap — but it rewrites ~130 records, so it is your call.",
    "- **REPLACING THE RAAZ GRID DISSOLVED A FINGERPRINT POINTER — THE REV-360 FAILURE MODE, AGAIN.** "
    "`sharptusk raaz` and `famished raaz` shared `wk [Fire +25, Lightning +25] / st [Ice -12.5]` with "
    "**three fam=None orphans: `darrcuiln`, `lerren` and `rahskhas’s pet`.** Before rev 367 that "
    "cohort looked like it named those three as **Raaz** — `darrcuiln` is a Section-2 record and its "
    "own note guesses *\"Likely classified as a Beast\"*, so it mattered. But the two Raaz were "
    "themselves unstamped, so the pointer was an artifact of the cohort, exactly as with "
    "`balayang`/`desmodus`. **The three orphans are now the only holders and point at nothing.** "
    "Not evidence either way; they still want pages.",
    "- **A LEDGER GAP: wiki `Aster Yggrete Shard I` HAS NO CLEAN DB MATCH.** The DB holds "
    "`Aster Yggrete` (no numeral) and `Aster Yggzi I`…`V` as separate lines, so the wiki form could "
    "map to either and the numeral fits only one of them. **Omitted from `snowpelt rabbit` as a "
    "consumable rather than guessed** (the same call as Snoll Arm and Slug Eye). One look at the "
    "item settles the ledger entry for the whole Yggrete class.",
    "- **`eschan il’aern’s wynav`’s PANEL SAYS `Family: Aern`; WE FILE IT `Wynav`. NOT MOVED.** "
    "Unlike the rev-366 Pixie/Bee case, nothing corroborates the panel: `Wynav` is a real 3-member "
    "family here, all three share one grid, and its sibling `aern’s wynav` is filed the same way. A "
    "panel does not outrank a family that already exists (the `pakecet` precedent). Same shape as "
    "`eschan il’aern’s euvhi`, which is `Euvhi` and stayed there at rev 366.",
    "- **`ravager chariot`’S PAGE PRINTS `Crystal: None` — THE FIRST EXPLICIT ONE.** Its 20 family-mates "
    "all carry `Light`, but a Bastion Chariot drops no crystal and the page says so in words. **No "
    "`crys` was written** (an empty string is noise, per the empty-string discipline) and the fact "
    "went in the notes instead. If you want \"None\" to render as a value rather than a blank row, "
    "that is a Kotlin change, not a data one.",
    "- **RULE 332's SUSPICIOUS PAIR IS RESOLVED: `vigilant gear` AND `vigilant gears` ARE BOTH REAL.** "
    "Rev 361 flagged them as the shape most likely to be a typo duplicate — same family, same level "
    "band, singular/plural. **BG publishes a separate page for each**, byte-identical in content: "
    "Family Gears, Crystal None, NM, the same three Abyssea zones, 4 spawns, Bastion, Pennant-only "
    "aggression. Both stamped, neither merged. The other same-family same-level pairs from rule 332 "
    "(`archaic`/`gyroscopic`/`imperial gear` vs `gears`) are almost certainly the same story.",
    "- **TWO PANELS DISAGREE ON THE LEECH ECOSYSTEM AND OUR FILE ALREADY HAS THE ANSWER.** "
    "`quiescent leech`'s panel says *Leech / Aquan*; `liquidbone leech`'s says *Leech (Amorph)*. "
    "`family_eco[\"Leech\"]` is **Amorph**, matching the second. Nothing changed — recorded only "
    "because it is a clean demonstration that these panels get taxonomy wrong roughly half the time.",
    "- **SIX RECORDS NOW CARRY A `[\"Varies\", null]` RESIST ENTRY, AND IT RENDERS AS TEXT, NOT A CELL.** "
    "`mystic avatar` and `fantoccini avatar` joined the four Adversary Avatars already using that "
    "shape, because their pages literally print *Weak to: Varies*. `Varies` is not one of the 16 grid "
    "types, so `RES_KNOWN` in AuctionApp.kt drops it out of the grid and lists it as leftover text "
    "below — which is arguably the right display for an avatar whose element changes. **Checked, not "
    "a bug.** If you would rather it read differently, that is a Kotlin change.",
    "- **`mystic avatar` HAS NO CONTENT TAG AND PROBABLY WANTS ONE.** It lives in Temenos across the "
    "Eastern Tower and the Central 2nd and 4th floors, and the file already has "
    "`Limbus: Temenos: Tier 1/2/3` tags on seven records — but its page never names a tier, so "
    "**none was guessed**. One word from you tags it.",
    "- **A SIXTH RED-BANNER VALUE, AND IT IS AN NM: \"Empty Notorious Monster\".** `fantoccini avatar`'s "
    "banner reads that, for the ENM *Pulling the Strings*; the record was not NM-flagged and now is. "
    "Running list for rule 326: *Notorious Monster* ✔ · *Voidwatch Notorious Monster (Zilart Stage I)* "
    "✔ · *Kindred's Seal Notorious Monster* ✔ · **Empty Notorious Monster ✔** · *Expeditionary Force* "
    "✘ · *Dark Kindred* ✘. Grep the banner for the words \"Notorious Monster\" and it has been right "
    "six times out of six.",
    "- **TWO MORE LEDGER ENTRIES: wiki `Ancient Beastcoin` → DB **`Anct. Beastcoin`**, and wiki "
    "`Vial of Fiend Blood` → DB **`Fiend Blood`** (the same drop-the-vial pattern as `Vial of Odious "
    "Blood` → `Odious Blood`). Both found by the per-word fallback after an exact match missed.",
    "- **!! THE `balayang`/`desmodus` GRID WAS REAL ALL ALONG — REV 360's READING WAS THE WRONG ONE.** "
    "Their shared `wk [Piercing +25, Ice +12.5, Wind +25, Lightning +12.5, Light +25] / st [Dark -50]` "
    "was treated as a suspect cohort. **Both BG pages now confirm it in words** — Balayang: *Weak "
    "against: Wind, Light / Resistant to: Dark*; Desmodus: *Weak to: Wind, Light / Strong to: Dark* "
    "— and its third holder is `vampyr bats`, a healthy Flock Bat. **Grid KEPT on both.** The "
    "lesson cuts against rule 358: a cohort of unstamped records is not automatically an import "
    "default. It is only an artifact when NOTHING outside the cohort corroborates it.",
    "- **!! BG FILES BOTH UNDER `Family: Giant Bats`, AND WE HAVE NO SUCH FAMILY.** We have `Bat` (89) "
    "and `Flock Bat`, so BG's bat sub-categories ARE already modelled separately here — which is "
    "exactly why a third one is plausible. **Both were filed `Bat`** (single named bats, not swarms) "
    "and given the Bat family kit, crystal and job. If Giant Bats should be its own family, say so "
    "and it is a small migration; the two records' own grids already differ from the Bat stamp and "
    "would carry over untouched.",
    "- **AMNAF's PAGE NAMES `Imperial Gears` AND `triple gears` — BOTH PLURAL — WHICH BACKS RULE 359.** "
    "It summons Imperial Gears in round one and triple gears in round two. We hold BOTH "
    "`imperial gear` and `imperial gears` (identical: Gear, 75, Nyzul Isle), and **neither "
    "`triple gear` nor `triple gears` exists at all** — a genuinely missing mob. Combined with "
    "`vigilant gear`/`gears` both having real pages, the singular/plural gear pairs look real, not "
    "duplicated.",
    "- **FOUR `noctonberry` RECORDS ARE OBVIOUSLY TONBERRIES AND ARE STILL ORPHANS.** "
    "`noctonberry black mage`, `noctonberry ninja`, `noctonberry summoner`, `noctonberry thief` share "
    "the exact grid the four Cooks had before rev 369 stamped them, and their names carry their jobs. "
    "They are orphans because the rev-141 fold needed a WHOLE-WORD family match and \"Noctonberry\" "
    "only contains \"tonberry\" as a substring — the same reason `cook nalberry` was one. "
    "**Four records, one word from you, no page needed.**",
    "- **`demisahagin white mage` HAS A PANEL BUT NO RECORD IN THE FILE.** Its three siblings (bard, "
    "dragoon, monk) are all here and were stamped this rev. The panel gives family, job, crystal, "
    "weakness and behaviour, and the siblings supply the grid, kit, level and zone — so it could be "
    "created cleanly. **Not created**, because adding a mob on a panel's word is a bigger step than "
    "stamping one. Say the word.",
    "- **`Scouring Bubbles` HAD NO DEFINITION AND NOW DOES — SOURCED FROM `trusts.json`.** Counselor "
    "Mihli's page names it alongside Benediction, and the guard refused the undefined reference. "
    "**Mihli Aliapoh's Trust entry lists `Scouring Bubbles (AoE)` under her weapon skills**, so the "
    "def was written from that in-file source (description + AoE target only; no type or element was "
    "guessed). Worth remembering: `trusts.json` is a usable source for ability defs.",
    "- **THE `sp`/`abilities` NAME OVERLAP IS NOT A DEFECT — CHECKED AND CLOSED.** 459 mobs hold an "
    "`sp` entry that is also an ability name. 421 are `Burst` (the Black Mage spell colliding with a "
    "TP move); almost all the rest are **Blue Mages holding Blue Magic**, which shares its names with "
    "the mob moves it is learned from (`bashdeel` has 27 such). `amnaf`'s `Tail Slap` and `Hysteric "
    "Barrage` were briefly moved to `ab` this rev and **moved straight back** — Amnaf is a Blue Mage "
    "and those are its spells. Do not \"fix\" this.",
    "- **A SPELL-LIST CONFLICT ON `curilla`, RESOLVED BY MERGE, NOT REPLACE.** Her page names Flash, "
    "Protect III, **Shell II** and Cure IV; the stored list also had Holy and Banish II and said "
    "**Shell III**. Final list keeps Holy and Banish II and takes the page's Shell II. Flagging it "
    "because a page's \"will cast X, Y, Z\" line is a sample, not an inventory — **never let it "
    "overwrite a longer stored list.**",
    "- **ONE THIRD OF THE rev-358 ORPHAN TRIO IS ANSWERED: `rahskhas's pet` IS A **TIGER**.** Gnashfang "
    "Rahskhas's page reads *Assisted by: Rahskhas's Pet x5* and *Accompanied by five pet tigers*. It "
    "was one of the three fam=None records sharing the grid the two Raaz wore before rev 367, and "
    "**rule 358 was right about this one** — the shared grid was NOT a Raaz pointer. `darrcuiln` and "
    "`lerren` are still orphans on that grid and still want pages. Note how this sits against rev 369's "
    "`balayang`/`desmodus` correction: a cohort of unstamped records proves nothing either way, and "
    "only an outside source settles it.",
    "- **A SEVENTH RED-BANNER VALUE, AND IT IS AN NM: \"Fields of Valor Notorious Monster\"** "
    "(`eraser`). Rule 326's list is now: *Notorious Monster* ✔ · *Voidwatch NM (Zilart Stage I)* ✔ · "
    "*Kindred's Seal NM* ✔ · *Empty NM* ✔ · **Fields of Valor NM ✔** · *Expeditionary Force* ✘ · "
    "*Dark Kindred* ✘. Seven for seven on \"contains the words Notorious Monster\".",
    "- **!! FIVE STAMPED QUADAV NMs ARE ON A GRID THEIR OWN FAMILY CONTRADICTS.** `go'rha sludgewater`'s "
    "page says **Weak to: Lightning**; its stored grid had `Piercing +25, Fire +12.5, Light +12.5` and "
    "no Lightning at all, so the 153-member Quadav family grid (Lightning +50 is its largest) "
    "replaced it. **`bo'gha winterkill`, `du'vha grimewind`, `ea'zhu tremorcrag`, `gi'rho wrathstorm` "
    "and `he'dho spatesurge` — all Rolanberry Fields [S], all already filed Quadav — still wear the "
    "same wrong grid.** They are not orphans, so they are outside this pass; one line fixes all five "
    "if you want it.",
    "- **A PAGE CAN OVERRIDE BOTH THE STORED GRID AND THE FAMILY GRID: `fay` and `feeorin`.** Their "
    "pages read *Weak to: Fire, Light, Slashing / Strong to: Wind*. The stored grid resisted all "
    "twelve types at -62.5%, and the **Pixie family grid resists Fire and Light** — both contradict "
    "the page. Written as `[type, null]` pairs, which render a bare green Weak or red Res with no "
    "number — the documented way to record a direction the page gives without a magnitude. "
    "**Neither got the Pixie ability kit**: Fay's page says it casts nothing and only melees, and "
    "Feeorin's says it barely melees at all. Their real moves are in `sp` and the notes.",
    "- **FOUR MORE FAE-NAMED ORPHANS SIT ON THE GRID `fay` AND `feeorin` JUST LEFT.** `bucca`, "
    "`faerie`, `puca` and `titania` — all fam=None, all wearing the same -62.5%-across-the-board "
    "shape, and all Pixie names. Same situation as the four `noctonberry` records: the family is "
    "obvious from the name, no page needed. **Eight records now waiting on one word from you.**",
    "- **`fantoccini` AND `fantoccini monster` ARE A PAIR AND I DID NOT MERGE THEM.** Both are now "
    "`Humanoid` in Mine Shaft 2716 for the same ENM, at levels 55 and 49. `fantoccini monster` has "
    "the BG page; `fantoccini` is the name the ENM enemy table uses. Given rule 359 — where the "
    "`vigilant gear`/`gears` pair turned out to be two real mobs — **neither was deleted.** There is "
    "also a third, `fantoccini avatar` (stamped rev 368), which is presumably the pet of a Summoner "
    "Fantoccini, since the ENM's Fantoccini copies your main job.",
    "- **`fantoccini monster` LOST ITS `wk` ENTIRELY.** It was wearing a Rabbit import default (its "
    "three other holders are `snowpelt`, `snowpaw` and `alpine rabbit`), its page's Weak line is "
    "blank, and **`Humanoid` has no family grid to stamp** — 23 of its 40 members carry none. Removing "
    "it beat leaving a rabbit's resistances on a puppet.",
    "- **`yazquhl` IS STILL AN ORPHAN AND IS `gowam`'s QUEST PARTNER.** Gowam's page: *Spawned for "
    "quest Against All Odds along with Yazquhl.* Same level, same zone shape, same flags. No page for "
    "it yet.",
    "- **!! A PHANTOM FAMILY: `Elementals` IS IN `families` WITH ZERO MEMBERS.** The real one is "
    "`Elemental` (71 members, eco Elemental). `Elementals` has no members and **no `family_eco` "
    "entry either**, so it is a stray key that survived some earlier pass — almost certainly BG's "
    "plural leaking in, the same way `Family: Gears`, `Family: Crabs` and `Family: Dolls` do. Worth "
    "checking whether it renders as an empty family in the browser. **One-line delete if you want "
    "it gone**; nothing points at it.",
    "- **FIVE MORE `hobgoblin <job>` RECORDS ARE ORPHANS AND THREE SIBLING PAGES SETTLE THEM.** "
    "`hobgoblin ranger`, `hobgoblin red mage`, `hobgoblin thief`, `hobgoblin warrior` and "
    "`hobgoblin white mage` all carry the same `lv [30, 80]`, the same `wk [Light +25]` and the same "
    "A/L/S flags as the three stamped this rev, whose pages all read **Family: Goblins, "
    "Expeditionary Force**. The nine OTHER hobgoblins in the file (`alastor`, `angler`, `animalier`, "
    "`blagger`, `fascinator`, `martialist`, `physician`, `toreador`, `venerer`) are already Goblin — "
    "only the job-named Expeditionary Force set was missed. **Thirteen orphans now waiting on one "
    "word**, counting the four `noctonberry` and four fae records.",
    "- **`gullin baelfyr` IS FIXED (rev 372, your call) — IT WAS WEARING GEFYRST'S ICE GRID.** It now reads "
    "`wk [Water +25] / st [phys -75, Fire -25, Ice -25]`, copied verbatim from **`nocuous inferno`**, "
    "which is a fire elemental at the same battlefield scale and using the same `Impact` label. "
    "**The other three check out**, and the file's own Ulbuka naming settles it: the 6-member `baelfyr` "
    "group is FIRE (resists Fire -95), the 7-member `gefyrst` group is ICE, `byrgen` is EARTH/DARK and "
    "`ungeweder` is WIND/LIGHTNING. Gullin Gefyrst, Byrgen and Ungeweder each carry the right element "
    "for their name — Byrgen and Ungeweder carry only half of their hybrid pair, which is narrow but "
    "not wrong. **Confirmed the same rev: `roc` is correctly filed `Greater Bird`.**",
    "- **`gullinkambi` GOT ITS NM FLAG FROM A PANEL, NOT A BANNER — THE FIRST TIME.** Rule 326 has "
    "always keyed on BG's red banner text. Here the only source is an AI panel calling it a "
    "*Roc-type battlefield boss* with a six-person cap and a fifteen-minute limit, which is an NM in "
    "every sense this file uses the flag. **Flagging it because it is a precedent, not because I "
    "doubt it.** Its family came the same way: no `Roc` family exists here and `roc` itself is filed "
    "`Greater Bird`.",
    "- **FOUR MORE ORPHANS SIT ON GRIDS VACATED THIS REV.** `touched gefyrst` and `ice fiend` share "
    "the Gullin ice-elemental grid; `kyo` and `pya` were the only other holders of the grid "
    "`gullinkambi` just gave up. None has a page. Listing them because this pass keeps proving that "
    "a grid cohort is a lead worth *looking at* and never a conclusion on its own.",
    "- **REV 373 CLEARED THE DETERMINISTIC NAME FOLDS — 28 DONE, AND 5 REJECTED AS FALSE MATCHES.** "
    "Folded: **7 `metaquadav *` → Quadav**, **7 `theoyagudo *` → Yagudo**, **4 `noctonberry *` → "
    "Tonberry**, **5 `hobgoblin <job>` → Goblin**, **`bucca`/`faerie`/`puca`/`titania` → Pixie**, "
    "`cardian prototype` → Cardian. Jobs came from the names, crystals and kits from the families. "
    "**The 5 rejected are the reason this is not scriptable:** `umarid` (glued inside \"uMARIDs\"), "
    "`pixiebane` (a pixie-BANE kills pixies), `yrvaulair s cousseraux` (glued inside \"yrvauLAIR\"), "
    "`savage hound condottiere` (an esquire/condottiere PvP rank, not a Hound), and "
    "`eschan il’aern’s spirit` (its siblings are filed Euvhi and Wynav, not Aern). **A 17% "
    "false-positive rate on pure substring matching** — the same order as the Section-3 name guesses.",
    "- **!! I OVERSTATED THE NPC PILE. THE HARD NPC/STRUCTURE SET IS 24 RECORDS, NOT ~135.** Sorted "
    "by shape, the 254 remaining orphans break down as: **structures** (9 — `bastion gate`, "
    "`city gate`, `dilapidated gate`, `allied belfry`, `allied mantelet`, `royal banneret`, and the "
    "`binding`/`paralyzing`/`silencing tube` trio) · **allied and imperial NPC units** (9 — "
    "`bastion fighter`, `bastion mage`, `imperial trooper`, `immortal guard`, `field musician "
    "guard`, `confederate +d568`, and the `cobra`/`crocodile`/`python mercenary` trio) · "
    "**esquire/condottiere PvP ranks** (6). That is the whole delete-or-keep question. **The other "
    "230 are real mobs that want families, not deletion.**",
    "- **THE BIG REMAINING WIN IS THE HUMANOID PATTERN, NOT THE NPC RULING.** 20 orphans are named "
    "for **Trusts** (`maat`, `prishe`, `volker`, `ayame`, `trion`, `naja salaheem`, `excenmille`, "
    "`ferreous coffin`, `qultada`, `klara`, `elivira`, `noillurie`, `rainemard`, `romaa mihgo`, "
    "`leonoyne`, `lhu mhakaracca`, `kayeel-payeel`, `maximilian`, `areuhat`, `darrcuiln`) — the "
    "fightable versions from Maat’s Test, Divine Might and the CoP battlefields. Another **100** are "
    "single-word proper nouns of the same shape. **Every person-named battlefield opponent whose "
    "page has come through is Humanoid — nine for nine** (`amnaf`, `bashdeel`, `counselor mihli`, "
    "`curilla`, `danzo`, `ghayaraan`, `gowam`, `habraheem`, `hkadouf`). One ruling covers ~120 "
    "records.",
    "- **AN UNRESOLVED SET WORTH ONE LOOK: the five zodiac `caster` records** — `aquarian`, "
    "`ariesian`, `capricornian`, `libran` and `piscean caster`. They share a naming scheme and are "
    "all bare. I could not place them from the file alone and did not guess.",
    "- **`cardian prototype` KEPT ITS GRID even though it was folded.** It is the sole holder of an "
    "**all-elements -25% RESIST**, while the 53-member Cardian family grid is all-elements **+30% "
    "weak** — opposite directions. An all-resist shape is not the generic +12.5/+25 import default, "
    "so replacing it on cohort logic alone would have been a guess. Flagged rather than overwritten.",
    "",
    "**Known gaps**",
    "",
    "- **Panels that name the WRONG mob's family.** `boobrie` (names Erynys's Amphiptere) and "
    "`assassin's apprentice` (names Dimgruzub's Qutrub) both need a real page, not another panel.",
    "- **`prishe`** carries the identical `Master Trials: Heroines Combat II` tag as `lilisette` and "
    "`lion`, both now stamped Humanoid. It is the third of the three and wants one screenshot.",
    "- **`aquila` and `haudrale`** are named on Larzos's page as fellow Spitewardens of Lady Lilith "
    "and **neither exists in the file at all.**",
    "- **THE THREE SHIKAREE SISTERS ARE SPLIT ACROSS TWO FAMILIES.** `shikaree x` and `shikaree z` "
    "both print `Family: Humanoids` and were stamped **Humanoid** at rev 355 \u2014 but **`shikaree y` is "
    "filed `Blessed Races of Altana`**, alongside `shantotto`, `arciela`, `zurko-bazurko` and five "
    "others. Both families map to eco `Unclassified`; Humanoid holds 31 records, Blessed Races 9. "
    "One of the two buckets is wrong for this class of mob and it wants a ruling \u2014 not a silent "
    "re-stamp of a record whose page we have not seen.",
    "- **`counselor mihli`'s bad stamp is FIXED (rev 369)** — her page prints A, L, T(H), so the "
    "`[Sight, True Sight]` stamp became `[\"True Sound\"]` and she folded into `Humanoid`. "
    "**`torvotaur` still carries it** and is still out of scope.",
    "- **The Content tab still shows six unfamilied records.** `HIDE_UNFAMILIED` covers the mob "
    "browser only \u2014 `mobsForContent` and `mobsByNamePrefix` call `mobDb.all()` directly, on "
    "purpose, because dropping a real mob out of a Dynamis-D roster makes the roster wrong. The six: "
    "`commander's pet`, `volte's pet` (Dynamis D); `lilisette`, `lion`, `prishe` (Master Trials); "
    "`kanavid` (Unity). Lilisette and Lion are now stamped, so this is down to four.",
    "",
    "**Carried project debt**",
    "",
    "- Zones remaining: **Ra'Kaznar Turris \u00b7 Mount Kamihr \u00b7 Rala Waterways \u00b7 Leafallia \u00b7 "
    "Reisenjima Henge \u00b7 Reisenjima Sanctorium.**",
    "- The ` (nm)` ability class; 36 flat-string zone entries wanting conversion to pairs; the "
    "generic-elemental sweep; an `audit.py` \"lv outside every zone range\" section; Nyzul Isle on all "
    "41 layout mobs; the per-class lv-stamp sweep; a ruling on `[U1]`/`[U2]`/`[U3]` plus moving the "
    "21 free-text instanced zones into `audit.py`'s `FREE_ZONES`.",
    "- **Awaiting compile:** 201, 210, 211-263, 278, rev 311's SortieScreen, rev 333's "
    "GeasFeteScreen, rev 334's UltimateWeaponsScreen, rev 338's Trusts tab + WS reference, rev 341's "
    "Trust info sections, rev 345's `TopLevelRow`/`SectionToggleRow` + Trusts fold, **rev 350's "
    "`HIDE_UNFAMILIED`**.",
    "",
]

lines += [
    f"## Section X — marked with the red X, awaiting your review ({len(xmarked)})",
    "",
    "**These are not orphans.** They were moved out of Other > Unknown at **rev 141** and each was "
    "given `mobimages/review_x.png` as its per-mob `img`, which overrides the family icon, so every "
    "one of them shows a red X in the browser until you have looked at it.",
    "",
    '> *"go through the rest of the unknown section and move mobs that look like they should be '
    'somewhere else. no guesses, but things like rabbit should go in rabbit. mark these with the x '
    'icon here so i can look at them later."*',
    "",
    "**The rule was literal, not inferred:** a record moved only if its own name contains an "
    "existing family name **as a whole word**, with the last match winning when several appear "
    "(`naraka bat` → Bat, not Naraka). A statistical trailing-token rule was built first and thrown "
    "away — it produced things like `aquarian caster` → Scorpion off a single coincidental "
    "co-occurrence.",
    "",
    "**Nine literal matches were hand-excluded** because the family word is in the name but the head "
    "noun says otherwise — the `X's pet` shape (`vampyr wolf` is not a Vampyr). Those nine are still "
    "orphans and are sitting in Section 3 above.",
    "",
    f"**Clearing the marker itself is one line** — set `img` to absent wherever it equals `{REVIEW_X}` "
    "— and the record falls straight back to its family icon. **None of them had art to lose;** "
    "that was verified before the marker was written. **But see rule 11 — the marker is the cheap "
    "part.** Rev 356 cleared the fourteen Goblins and every one of them also needed its job, "
    "crystal, zone, Garrison spawn line and the family ability kit written in from its page.",
    "",
    "**Cleared so far:** r356 Goblin(14) · r357 Demon(10) · r358 Acuex(7)+Pugil(4) · r359 Gigas(9) · r360 Bat(8) · r361 Flock Bat(8) · r362 Bomb(1 kept, 2 deleted)+Velkk(4) · r363 Poroggo(5) · r364 Imp(3)+Qiqirn(3)+Rafflesia(3)+Skeleton(3) · r365 **13 records across 13 families** · r366 **13 stamped + 1 deleted as a duplicate, across 14 families** · r367 **15 records across 9 families** · r368 **the last 12, across 6 families — SECTION X IS EMPTY**.",
    "",
    (f"{len(xmarked)} records across {len(byfam)} families:" if xmarked else
     "**Nothing left in this section.** The red X no longer appears anywhere in the browser; "
     "every record that wore it now carries its family icon, kit, crystal, job, detection and "
     "resist grid. The live work moves back to the bucket sections above."),
    "",
]
if xmarked:
    lines += ["```"]
for fam in sorted(byfam, key=lambda f: (-len(byfam[f]), f)):
    ks = byfam[fam]
    lines.append(f"{fam}  ({len(ks)})")
    for k in ks:
        lines.append(f"    {k}")
if xmarked:
    lines += ["```"]
lines += [""]

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("bucket", len(bucket), {n: len(sec[n]) for n in sec}, "| x-marked", len(xmarked), "->", OUT)
