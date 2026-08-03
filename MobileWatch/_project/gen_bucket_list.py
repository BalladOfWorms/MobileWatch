# Writes a plain, scannable list of every remaining fam=None record, for the user to mark up.
import json, collections, re
A='/home/claude/android/app/src/main/assets'
d=json.load(open(f'{A}/mobs.json')); M=d['mobs']
TR={t['n'].lower() for t in json.load(open(f'{A}/trusts.json'))['trusts']}
orph={k:v for k,v in M.items() if not v.get('fam')}

def tag(v):
    b=[]
    if v.get('lv'):
        lo,hi=v['lv']; b.append(f'lv {lo}' if lo==hi else f'lv {lo}-{hi}')
    if v.get('wk') or v.get('st'): b.append('grid')
    if v.get('ab'): b.append('kit')
    if v.get('sp'): b.append('spells')
    if v.get('nm'): b.append('NM')
    return ', '.join(b) or '—'

groups=collections.OrderedDict(); seen=set()
def take(title, note, pred):
    got=sorted(k for k,v in orph.items() if k not in seen and pred(k,v))
    seen.update(got); groups[title]=(note,got)

take('TRUST-NAMED — fightable ally versions','Only Darrcuiln is left — the other 12 went at r382. He was held back from that delete because he is a real Sinister Reign boss in Rala Waterways [U] with a grid, a kit, drops and an NM flag, not a bare NPC stub. He still needs a family.',
     lambda k,v: k in TR)
take('ZODIAC CASTER SET','Shared naming scheme; I could not place them.',
     lambda k,v: 'caster' in k)
take("PETS AND ADDS (\"X's Y\")",'Each belongs to whatever its owner is.',
     lambda k,v: "'s " in k or k.endswith("'s"))
take('HERD ANIMALS','bull / calf / cow, numbered herds.',
     lambda k,v: '[herd' in k)
take('SINGLE-WORD PROPER NOUNS','Mostly battlefield and quest opponents. The Humanoid ruling would cover most of these.',
     lambda k,v: len(k.split())==1)
take('EVERYTHING ELSE','',lambda k,v: True)

TITLE = ('# MobileWatch — the unknown bucket, plain list' if orph
         else '# MobileWatch — open decisions (the unknown bucket is EMPTY)')
LEDE = (f'**{len(orph)} records still have no family.** Mark up anything you can place and send it back.'
        if orph else
        '**Every record in mobs.json now has a family.** The Other > Unknown bucket reached 0 at rev 390 — '
        'the browser has no unfamilied group left, and the Content tab has no unfamilied roster rows left either. '
        'What remains is the decision list below: all optional cleanup, none of it blocking.')

L=[TITLE,
   '',
   LEDE,
   f'Deleted so far, 166 records in all: 3 junk/duplicate stubs (r362, r366), 24 NPC/structure (r374), 5 zodiac + 9 herd (r375), 14 general/volunteer/wildcat/scylla-brigade (r376), patriarch protector (r377), 12 Trust-named NPCs (r382), 31 single-word A-Lutete records (r385), 13 more M-S records (r386), 14 S-Z records (r387), `vampyr wolf` + the 3 pets (r388), 18 knights/fiends/officials from the A-L slice (r389), 18 more from the M-Z slice (r390). **Three came BACK at r383** — Binding / Paralyzing / Silencing Tube were filed as structures at r374 and the Tubes category page proves they are real mobs.',
   '']
for title,(note,ks) in groups.items():
    if not ks: continue
    L += [f'## {title}  ({len(ks)})']
    if note: L += ['', f'*{note}*']
    L += ['']
    for k in ks: L.append(f'- **{M[k]["n"]}** — {tag(M[k])}')
    L += ['']

# ---------------------------------------------------------------- decisions block
# Every count here is measured live so the section can never go stale.
TR_ORPH=[k for k in orph if k in TR]
legacy=sum(1 for v in M.values() if v.get('wk') and len(v['wk'])==1 and not v.get('st'))
badjob=sum(1 for v in M.values() if v.get('job') and (',' in v['job'] or v['job'].isupper()))
phantom=sorted(f for f in d['families'] if not any(v.get('fam')==f for v in M.values()))
quadav=[k for k in ["bo'gha winterkill","du'vha grimewind","ea'zhu tremorcrag",
                    "gi'rho wrathstorm","he'dho spatesurge"]
        if M.get(k,{}).get('wk') and M[k]['wk'][0][0]=='Piercing']
conta=[k for k,v in M.items() if k.startswith('contantican') and v.get('nm')]
cirdas=[k for k,v in M.items() if v.get('lv')==[125,126]]
npcs=[k for k in ('poroggo prince','qiqirn ceramist','qiqirn treasure hunter','patrol worm') if k in M]
pets=[k for k in orph if "'s " in k or k.endswith("'s")]
undef=sorted({a for v in M.values() for a in (v.get('ab') or []) if a not in d['abilities']})
proper=[k for k in orph if len(k.split())==1 and k not in TR]

D=[]
SHOW_CLOSED = False   # ruled on at rev 391; kept in the source for history
def item(head, body): D.append((head, body))

if proper:
    item(f'The Humanoid pattern does NOT generalise — how do you want the last {len(proper)} handled?',
         f'I have to walk this one back. Through r381 every person-named page that came through was '
         f'`Humanoid`, sixteen for sixteen, and I was asking you to bless a blanket stamp on the whole '
         f'single-word group. **The r385 batch broke it: of sixteen pages, only four were Humanoid** '
         f'(Gunther, Krinahal, Kusa, Laila) **and twelve were not** — Contemplator is a Thinker, '
         f'Hotupuku a Bugard, Idun a Ghost, Jackpot a Magic Pot, Ketos a Pugil, Kumbaba a Treant, '
         f'Kutkha a Lesser Bird, Lacerator a Crab, Mammet-800 a Mammet, Boobrie an Amphiptere, '
         f'Gloomscale a Zilant, Kanavid a Sea Monk. **Idun and Kutkha are person-shaped names and '
         f'still came back as creatures**, so "does it look like a person" is not a safe test either. '
         f'What DID hold every time is narrower: **a named opponent in a battlefield, limit-break or '
         f'quest event is Humanoid.** The remaining {len(proper)} are a mixed bag and I would rather '
         f'keep taking pages than stamp them. Tell me if you would rather I stamp the obvious '
         f'battlefield ones and leave the rest.')

_nmlv=[k for k,v in M.items() if v.get('nmlv') and 'nm' not in v]
if _nmlv:
    item(f'{len(_nmlv)} records show no level on the card because of an `nmlv` quirk',
         'These carry an `nmlv` value but no `nm` flag. The card prefers `nmlv` over the normal '
         'level line, so their real level range never renders — the row just looks blank. Either '
         'the `nm` flag is missing on all of them, or `nmlv` is stale and should go. One sweep '
         'either way.')

if SHOW_CLOSED: item(f'Delete {len(phantom)} empty families? ({len(phantom)} entries, 0 members each)',
     'These sit in the family list with nothing pointing at them, so they may render as empty '
     'families in the browser: ' + ', '.join(f'`{f}`' for f in phantom) + '. Note `treant` and '
     '`weapon` are lowercase, so they look like stray keys rather than real families.')

if SHOW_CLOSED: item(f'Normalise {badjob} malformed `job` strings?',
     'These use commas where the rest of the file uses slashes, or keep un-expanded three-letter '
     'codes like `WAR, DRK, BLM, SMN`. Fifty-two Worm records say `Black Mage / Black Mage, Red Mage` '
     '— the same job twice. All of it renders verbatim on the card. One sweep fixes them, but it '
     'touches a lot of records, so it is your call.')

if pets:
    item(f'The last {len(pets)} pets and adds — delete, or tell me what they are?',
         'Each of these names an owner but not a family, so I cannot place them: '
         + ', '.join(f'`{M[k]["n"]}`' for k in sorted(pets)) + '. The pattern that resolved the '
         'others was the *second* word naming a family — `schah\'s gaja` is a Caturae, '
         '`commander\'s wyvern` is a Wyvern. These have nothing to go on. **One thing to know before you say delete:** all three are ZONED with levels, so they are not bare stubs — `Assassin\'s Apprentice` lv 80 in Arrapago Reef with its own grid and notes, `Commander\'s Pet` lv 137 and `Volte\'s Pet` lv 142, both content-tagged to Dynamis Divergence areas, so deleting them drops rows from those area rosters.')

if 'darrcuiln' in orph:
    item('What family is Darrcuiln?',
         'He was on your delete list but I held him back: he is a real Sinister Reign boss in Rala '
         'Waterways [U] with his own resist grid, a five-move kit, four drops and an NM flag — not a '
         'bare NPC stub like the other twelve. He is the last Trust-named record without a family, and '
         'I would rather not guess between Coeurl and something bespoke. Delete him anyway if you want '
         'him gone.')

GOODLBL={'Physical','Magical','Breath','Slashing','Blunt','Impact','H2H','Piercing','Ranged',
         'Fire','Wind','Lightning','Light','Ice','Earth','Water','Dark','Varies'}
badlbl=collections.Counter()
_badim=collections.Counter(x for _v in M.values() for x in (_v.get('im') or [])
                           if '{' in x or '}' in x or x!=x.strip() or re.search(r'[a-z][A-Z]', x))
for _k,_v in M.items():
    for _e in (_v.get('wk') or [])+(_v.get('st') or []):
        if _e[0] not in GOODLBL: badlbl[_e[0]]+=1
if badlbl:
    item(f'{sum(badlbl.values())} resist-grid rows use a label that is not a damage type or element',
         'The grid only knows the eight damage types and eight elements. These rows carry something '
         'else and cannot render as a real cell: ' + ', '.join(f'`{k}` x{v}' for k,v in badlbl.most_common()) + '. Most look like status effects that belong in the immune list instead, '
         'and a few are prose that leaked in from a page.' + (f' The immune list has the same problem in miniature: ' + ', '.join(f'`{k}` x{v}' for k,v in _badim.most_common()) + ' — `{sleep` and `break}` are halves of a wiki template that got split.' if _badim else '') + ' Say the word and I will clear them.')

if quadav: item(f'Fix {len(quadav)} Quadav NMs wearing a grid their own family contradicts?',
     'All in Rolanberry Fields [S]: ' + ', '.join(f'`{M[k]["n"]}`' for k in quadav) + '. A sibling\'s '
     'page proved the family grid is right and theirs is wrong. They already have families so they '
     'are outside the unknown pass, but it is a one-line fix.')

if conta:
    item(f'Clear the NM flag on {len(conta)} Contanticans?',
         'They are flagged as notorious monsters and are not. The mechanism was confirmed a while '
         'back; only the ruling is missing.')

if SHOW_CLOSED: item(f'Delete the last {len(npcs)} NPC-type records?',
     'Same question you already answered for the gates and troopers, just these leftovers: '
     + ', '.join(f'`{M[k]["n"]}`' for k in npcs) + '. All four are stamped normally right now.')

if SHOW_CLOSED: item(f'{len(cirdas)} records share the level band `125-126` with no zone',
     'Every page that has turned up for one of these measured 119-122 in Cirdas Caverns instead, so '
     'the band looks like an import default: ' + ', '.join(f'`{M[k]["n"]}`' for k in cirdas) + '. '
     'The open question underneath it is whether `Cirdas Caverns [U]` should exist as a zone.')

if SHOW_CLOSED: item(f'{legacy} records still carry a single-entry resist grid',
     'One weakness, no resistances — the shape that predates the family grids. Down from about 150. '
     'They are harmless, just thin.')

# item 10 is now a "where do these live" question, not a gap — resolve each name against the
# player-side tables so the text can never claim a bestiary gap that isn't one.
J=json.load(open(f'{A}/jobs.json'))
_ja={x[kk] for lst in J['abilities'].values() for x in lst if isinstance(x,dict)
     for kk in ('n','name') if isinstance(x.get(kk),str)}
_si=set(J['spellinfo']); _ws=set()
def _walk(o):
    if isinstance(o,dict):
        if isinstance(o.get('n'),str): _ws.add(o['n'])
        for v in o.values(): _walk(v)
    elif isinstance(o,list):
        for v in o: _walk(v)
_walk(json.load(open(f'{A}/weaponskills.json')))
runes=[a for a in undef if a in _ja]; blu=[a for a in undef if a in _si]
wsk=[a for a in undef if a in _ws]; loose=[a for a in undef if a not in _ja|_si|_ws]
if undef:
    body=(f'All {len(undef)} are **player** abilities, so they are not bestiary gaps — but they still '
          f'render as bare names on the mob card, because the card only reads the `abilities` table. '
          + (f'{len(runes)} are player job abilities ({", ".join("`"+a+"`" for a in runes)}), each on a '
             f'mob whose job really has it. ' if runes else '')
          + (f'{len(wsk)} are Sword weapon skills ({", ".join("`"+a+"`" for a in wsk)}). ' if wsk else '')
          + (f'{len(blu)} is Blue Magic ({", ".join("`"+a+"`" for a in blu)}), on 32 Flan-type mobs. '
             if blu else '')
          + ('**The question is a Kotlin one:** should the card fall back to `jobs.json` and '
             '`weaponskills.json` when a name is not in `abilities`? That would light up all of them '
             'at once.')
          + (f' Still unexplained: {", ".join("`"+a+"`" for a in loose)}.' if loose else
             ' Nothing is left unexplained.'))
    if SHOW_CLOSED: item(f'{len(undef)} abilities render as bare names — a Kotlin fallback would fix all of them', body)

if SHOW_CLOSED: item('Four smaller things, whenever you feel like it',
     "**`torvotaur`** still has the bad `[Sight, True Sight]` detection stamp. "
     "**`shikaree y`** is filed `Blessed Races of Altana` while `shikaree x` and `shikaree z` are "
     "`Humanoid` — one of the three sisters is the odd one out. "
     "**`warder's hpedme`** is spelled wrong; the file's other four records say `hpemde`. "
     "**`mystic avatar`** wants a `Limbus: Temenos` tier tag but its page never named the tier. **Two record KEYS were misspelled and are now fixed** — `demishagin white mage` -> `demisahagin white mage` (its three siblings spell it right) and `onycophora's sandworm` -> `onychophora's sandworm`; a key/name equality check now runs in every proc script and reads 0.")

if SHOW_CLOSED: item('One thing I chose not to guess at',
     "**`cardian prototype`** resists every element at -25% while "
     "the other 53 Cardians are *weak* to every element at +30%; I kept its own grid rather than "
     "overwrite it.")

# --- rev-390 confirmations: two calls made this session that you can reverse ---
XW = M.get("xuan wu") or {}
QUARTET = [k for k in ("bai hu","qing long","zhu que","xuan wu") if k in M]
D[0:0] = [] if not SHOW_CLOSED else [
 ("Confirm: I held `xuan wu` back from your delete list",
  "It was on the M-Z screenshot, but it is the fourth of the four Voidwatch guardians Qilin "
  "summons and the other three are all filed — `bai hu` (Tiger) and `qing long` (Wyvern) were "
  "stamped in an earlier pass, and this same batch folded `zhu que` off its panel. All four sit "
  "at level 98-99, all four are NM-flagged, and all four carry the same `Summoned by Qilin "
  "(1 per Qilin)` spawn line in The Shrine of RuAvitau. Deleting one of four identical siblings "
  f"while filing the other three is the mistake `shayaam` taught us, so I folded it instead — to "
  f"**{XW.get('fam','?')}**, because Xuan Wu is the Black Tortoise and the file already files that "
  "same guardian under his other name, `genbu`, as Adamantoise. **Say the word and it goes.**"),
 ("Confirm: the untitled panel was `the keeper`, not `the briars`",
  "That screenshot is cropped above the page title — it starts at *Battle Info* — and both names "
  "were in the bucket, so I had to pick one. I read it as **The Keeper**, on three counts: your "
  "delete screenshot lists `The Briars` and does not list `The Keeper`, so this reading gives all "
  "34 records exactly one instruction and no double-booking; the page says it is *stronger than "
  "Mistdagger, The Briars (Galka) and The Briars (Elvaan)*, and `mistdagger` and `the briars` are "
  "both level 108 while `the keeper` is 110; and the page says Job: Scholar and names Kaustra, "
  "which fits `the keeper`'s stored nuke list rather than `the briars`' enhancing list. "
  "**If I got it backwards, `the briars` is the one that needs the page and `the keeper` is gone.**"),
]


if SHOW_CLOSED: item("The sixth Rolanberry Quadav — do you want `aa'bho slashburner` too?",
     "You said *family wins here* and the five you listed now carry the Quadav family grid. "
     "**`aa'bho slashburner` sits in the same Rolanberry Fields [S] group with the same "
     "contradicted grid** (`Piercing +25%`, `Fire +12.5%`, `Light +12.5%`, `Dark -12.5%`) — plus a "
     "bare `Lightning` weakness, which is exactly the row that made the family grid right in the "
     "first place. It was not on your list so I left it, but leaving one of six behind re-creates "
     "the inconsistency the fix was for.")

item("For the record: 8 of the 35 swept `nmlv` values were not just a restatement of `lv`",
     "You said sweep them away and all 35 are gone. Twenty-seven simply repeated the record's own "
     "level range, so nothing was lost. **These eight held a different number, and this is the only "
     "place they now exist:** `foul meat` 43-45 (lv 43-47) \u00b7 `hilltroll mirror guard` 82-83 "
     "(lv 81-82) \u00b7 `magnes quadav` 43-45 (lv 43-79) \u00b7 `minotaur` ? (lv 46-48) \u00b7 "
     "`mountain worm` 73 (lv 66-70) \u00b7 `nickel quadav` 43-45 (lv 43-75) \u00b7 `odontotyrannus` "
     "52 (lv 52-70) \u00b7 `orobon` 70 (lv 68-78). Mountain Worm is already a known case where the "
     "category table and the mob page disagree. Nothing to do unless one of these looks wrong to you.")


_trunc = sorted(k for k,v in d['abilities'].items()
                if isinstance(v,dict) and str(v.get('notes','')).rstrip().endswith(':'))
if _trunc and SHOW_CLOSED:
    item(f'{len(_trunc)} ability notes stop mid-sentence on a colon',
         'Each promises something it never delivers \u2014 `Lamb Chop` and `Sheep Charge` both end '
         '*\u201cit\u2019s imbued with the following Skillchain Attributes:\u201d*, `Horrid Roar` ends *\u201cthe effect '
         'varies slightly by which wyrm used this ability:\u201d*, and `Dust Cloud` does the same. The wiki '
         'had a table at that point and the scrape stopped at it. **They read as broken on the card.** '
         'Four pages would fill them in, or I can just trim the dangling sentence \u2014 your call which.')


if 'the briars' not in M and 'the briars (galka)' not in M and SHOW_CLOSED:
    item('Do you want the two `The Briars` variants back as records?',
         "Your screenshots settled decision item 2 the clean way: **`The Briars (Galka)` and "
         "`The Briars (Elvaan)` are two separate pages**, each noting *\u201cIn battle, he is simply "
         "named The Briars\u201d*, and the untitled panel names BOTH as things it is stronger than \u2014 so "
         "the panel was `the keeper` and that fold stands. **But the file now has neither Briars.** "
         "The single `the briars` record went with the M-Z delete list, and these two are real "
         "Notorious Monster / Mission Boss entries in Rala Waterways [U] \u2014 Behind the Sluices, "
         "1 spawn, A / L / T(S), Humanoid, sitting alongside `mistdagger` and `the keeper` which the "
         "file does carry. Say the word and I will add them as two records the way `mistdagger` is "
         "filed; their pages give no level, job or grid, so they would be thin until a fuller page "
         "turns up.")


if "will-o'the-wisp" in M and "will-o'-the-wisp" in M:
    _a, _b = M["will-o'-the-wisp"], M["will-o'the-wisp"]
    item("Delete `will-o'the-wisp`? It looks like a misspelling of the record beside it",
         "The file has both **`Will-o'-the-Wisp`** and **`Will-o'the-Wisp`** \u2014 the second is "
         "missing a hyphen, and that is not a spelling the wiki uses. Both are Bomb, both weak to "
         "Fire +50% with the same seven -50% resistances, both `det [Sight, Magic]`, both crystal "
         f"Fire, both a five-move kit. **The properly spelled one is the complete record**: lv 22-36, "
         f"Dark Knight, a 330s respawn and {len(_a.get('zones') or [])} zones. **The typo one has no "
         f"level, no respawn and no zones**, and calls itself Warrior. Same shape as the "
         "`demishagin` key and the `vampyr wolf` duplicate. I have not touched it \u2014 deleting a "
         "record that already has a family needs your word.")

L += ['---','', f'# Decisions I need from you  ({len(D)})','',
      'Ordered by how much they clear. Everything here is measured from the current file, so the',
      'numbers move on their own as we go.','']
for n,(head,body) in enumerate(D,1):
    L += [f'### {n}. {head}','', body,'']


L += ['','---','','## Settled at rev 391-395 — your answers, and what each one did','',
 "- **The two Briars variants are back** (rev 395) \u2014 `The Briars (Galka)` and `The Briars (Elvaan)`, filed on the `mistdagger` template: Humanoid, NM, mission boss, one spawn in Behind the Sluices, A / L / T(S). **Two things were carried over from the single record deleted at rev 390** rather than thrown away: its level 108 (which matches Mistdagger, the other boss in that battlefield), and its six-spell list. **The spells were measured on the single record, so there is no way to tell which variant they came from or whether both share them** \u2014 both carry them, flagged here. Neither page states a job or a resist grid, so those stay unset.",
 "- **`will-o'the-wisp` deleted** (rev 395) \u2014 the hyphen-less duplicate. Family, crystal, detection, both halves of the resist grid and the five-move kit were byte-identical to the properly spelled record; the only thing it held that the survivor did not was the job string `Warrior` against `Dark Knight`, and it had no level, no respawn and none of the eight zones. Nothing referenced it.",
 "- **A file-wide sanity sweep** (rev 394) \u2014 you asked for another look for anything obviously out of place. **The important result is a negative one:** a detector for *the mob's name names a family but `fam` says something else* returns 79 records, and checking every one against an independent witness \u2014 its own ability kit \u2014 shows the kit agrees with the family it is filed under in **all 79**. `harpeia (nm)` really carries the Khimaira kit, `seed goblin` really carries the Orc kit, `phlebotomic slug` really carries the Leech kit. **There is no second Lamiae; the family column is sound.** What the sweep did fix was vocabulary and shape: **63 `crys` values** that were not the file's own words (`Light Crystal` \u2192 `Light` x32, `Earth Crystal` x11, `Fire Crystal` x10, `Thunder` \u2192 `Lightning` x2, a truncated `N` \u2192 `None` x7, and one `Element`), **2 level ranges starting at 0** (`black baron`, `seed crystal`), **one stray `Escha - Ru'Aun`** against 77 records spelling it `Escha RuAun`, **35 `zones` entries stored as bare strings** instead of one-element lists (`elemental circle` had both shapes inside one record), and **one glued spell string on `guimauve`** that was eight spells run together. All five now have a live line in `audit.py` and all five read 0.",
 "- **`xuan wu` is Genbu type** (rev 393) \u2014 confirmed, so the Adamantoise fold stands. The Qilin summon list you sent names all four: Xuan Wu (Genbu), Bai Hu (Byakko), Qing Long (Seiryu), Zhu Que (Suzaku). All four picked up their aura, their spell line and the note about pulling each summon away from the group.",
 "- **The untitled panel was `the keeper`** (rev 393) \u2014 confirmed. `The Briars (Galka)` and `The Briars (Elvaan)` are two separate pages and the panel names BOTH as things it is stronger than, so it is neither. See the open question about putting those two back.",
 "- **`aa'bho slashburner`** (rev 393) \u2014 its own page prints *Weak to: Lightning*, which is the Quadav family table's +50% and a row the contradicted grid did not have. Stamped to match the other five. The page also names all six as one spawn set, so they all now carry the shared mechanic, the Rolanberry Fields [S] zone and the Succor to the Sidhe spawn line. **The five had no NM flag and Aa'Bho did \u2014 I set them to match; one line reverses it.**",
 "- **The four dangling ability notes** (rev 393) \u2014 **trimmed to complete sentences rather than deleted**, since each states something true without the table the scrape lost. `Dust Cloud` also got corrected outright: it was stored as a 10' *cone*, and the table's Area column reads AoE with Conal listed separately as a value it could have used. `Horrid Roar` moved from the non-BG type `Enfeebling` to `Magical` and now says it wipes shadows.",
 "- **`Amorphic Spikes`** (rev 392) \u2014 defined from the page you sent: *Delivers a fivefold attack. Damage varies with TP.*, Physical, single target, with the skillchain properties and weapon-skill numbers in its notes. **That was the single biggest entry in the bare-name list \u2014 32 Flan-type mobs \u2014 so undefined references dropped from 49 to 17.** The 16 names left are all player job abilities and Sword weapon skills, which you said to leave alone.",
 "- **`nmlv` quirk** — *\"Sweep away\"*. All 35 stale `nmlv` values removed; those cards render their level again. Eight held a value that differed from `lv`, listed above so nothing vanished silently.",
 "- **16 empty families** — *\"they are not showing in the app, so maybe leave alone?\"*. Left in place; I verified all 16 have zero members, so they are inert either way. One line removes them whenever you want.",
 "- **`job` strings** — you explained the format: *BLM main job with BLM subjob, or RDM as job*. **So the comma is real and I did not touch it.** I only expanded the three-letter codes to long form, 759 records, separators untouched. `Black Mage / Black Mage, Red Mage` stays exactly as written.",
 "- **Bogus resist-grid rows** — *\"these things should be in the notes of a mob\"*. Nine records got a prose note (`Susceptible to Petrify`, `Resists Sleep and Stun`, `Only takes piercing damage`, and so on) and every non-grid label is gone; the detector now reads zero. Two exceptions worth naming: the seven `Damage Taken` / `Dark Earth` rows carried **no percentage at all**, so there was nothing to write down and they were simply dropped; and `jailer of fortitude`'s `Magic Damage` / `Physical Damage` were **renamed to `Magical` / `Physical`**, which are the grid's own labels, so they now render as real cells instead of becoming prose.",
 "- **Malformed immune values** — `mahuika` and `nga manawa` now read `Lullaby`, `Sleep` instead of the glued `LullabySleep`; `purson`'s `{sleep` / `break}` were the two halves of a wiki template and are gone.",
 "- **5 Quadav NMs** — *\"Family wins here\"*. Stamped, and the sixth followed at rev 393 once its own page turned up.",
 "- **4 Contanticans** — *\"Sure, clear\"*. NM flags removed.",
 "- **4 NPC-type records, the 125-126 band, the single-entry grids, the 17 bare abilities, `cardian prototype`** — *leave as is*. Untouched.",
 "- **The Shikaree sisters** — *\"change x and z to blessed race\"*. Both moved; all three now sit in `Blessed Races of Altana`.",
 "- **`torvotaur`** — *\"toro is fine\"*. Detection stamp left alone. **`mystic avatar`** — left alone. **`warder's hpedme`** — respelled to `warder's hpemde`.",
 "- **The Lamiae in Vermin** — `chigoe breeder` is filed `Lamiae` correctly, but carried a per-mob `eco` override of `Vermin` that beat the family's `Beastmen`; the name had made the import follow Chigoe. Override removed. **Running that as a file-wide check turned up one more:** `sang buaya`, filed `Bugard` but overriding its eco to `Beast` when Bugard is `Lizard`. Also removed. Those were the only two in the file.",
 '']

open('/home/claude/android/MobileWatch-Bucket-List.md','w',encoding='utf-8').write('\n'.join(L))
print(f'{len(orph)} orphans ->', {t:len(v[1]) for t,v in groups.items()})
