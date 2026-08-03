#!/usr/bin/env python3
"""
audit.py — MobileWatch mobs.json audit.
Reproduces every number quoted in MobileWatch-Mob-Project-Handoff.md from the live data.

Usage:  python3 audit.py [path/to/assets]
        (default: app/src/main/assets, relative to cwd)

Author: BalladOfWorms
"""
import json, os, re, sys
from collections import Counter, defaultdict

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
P = lambda f: os.path.join(ASSETS, f)

d = json.load(open(P("mobs.json")))
mobs = d["mobs"]
abils = d["abilities"]
fam_eco = d.get("family_eco", {})
fam_notes = d.get("family_notes", {})
fam_subs = d.get("family_subtypes", {})

items = json.load(open(P("ffxi_items.json")))
ITEM_NAMES = {v["n"] for v in items.values() if isinstance(v, dict) and "n" in v}
ZONES = {z["name"] for z in json.load(open(P("zones.json")))["zones"]}
ZONES_NORM = {re.sub(r"[^a-z0-9]", "", z.lower()) for z in ZONES}
try:
    SPELLS = set(json.load(open(P("jobs.json")))["spellinfo"].keys())
except Exception:
    SPELLS = set()

# Free-text zones with no zones.json entry (Odyssey / Einherjar / event sub-areas).
FREE_ZONES = {
    "Sheol A", "Sheol B", "Sheol C", "Sheol - Gaol",
    "Ninth Walk", "Maquette Abdhaljs-Legion",
    "Helmwige's Chamber", "Schwertleite's Chamber", "Waltraute's Chamber",
    "Grimgerde's Chamber", "Rossweisse's Chamber", "Siegrune's Chamber",
    "Silver Sea route to Nashmau", "Silver Sea route to Al Zahbi",
}
# Item classes the DB genuinely lacks — KEEP these drops, don't strip. See handoff §7.
DB_GAP = lambda x: "Chapter" in x

H = lambda s: print("\n" + "=" * 74 + "\n" + s + "\n" + "=" * 74)


# 1 ---------------------------------------------------------------- totals
H("1. TOTALS")
print(f"mobs                {len(mobs)}")
print(f"abilities           {len(abils)}")
print(f"families (fam)      {len(Counter(v.get('fam') for v in mobs.values() if v.get('fam')))}")
print(f"family_eco set      {len(fam_eco)}")
print(f"family_notes set    {len(fam_notes)}")
print(f"family_subtypes set {len(fam_subs)}")
print(f"NM-flagged mobs     {sum(1 for v in mobs.values() if v.get('nm'))}")
print(f"fam=None orphans    {sum(1 for v in mobs.values() if not v.get('fam'))}")


# 2 ------------------------------------------------------- integrity guards
H("2. INTEGRITY GUARDS  (all must be 0 — see handoff §4)")
nulls = [(k, kk) for k, v in mobs.items() for kk, vv in v.items() if vv is None]
print(f"mobs with a JSON-null value      {len(nulls)}   {nulls[:5]}")
anulls = [k for k, v in abils.items() if v is None]
print(f"abilities that ARE null          {len(anulls)}   {anulls[:8]}")
abel_str = [k for k, v in mobs.items() if isinstance(v.get("ab_el"), str)]
print(f"ab_el stored as a bare STRING    {len(abel_str)}   {abel_str[:5]}")
el_list = [k for k, v in abils.items() if isinstance(v, dict) and isinstance(v.get("el"), list)]
print(f"ability el stored as a LIST      {len(el_list)}   {el_list[:5]}")
empty_str = [(k, kk) for k, v in mobs.items() for kk, vv in v.items() if vv == ""]
print(f"empty-string values              {len(empty_str)}   {empty_str[:5]}")

# --- MobDb.load PARSE SIMULATOR ---------------------------------------------------------------
# Added rev 39. `AuctionViewModel` does `runCatching { MobDb.load(app) }.getOrNull()`, so ANY throw
# inside load() silently yields mobDb = null and the app shows ZERO mobs — browse, filter and search
# alike, with no crash and no log. `family_subtypes["Skeleton"]` shipped as an OBJECT instead of an
# ARRAY at rev 35 and did exactly that. org.json's get*() calls are strict where opt*() is not; this
# reproduces every one of them. IT MUST READ 0. If it doesn't, the app is bricked — fix before you zip.
def _throws_getString(v):
    return isinstance(v, (list, dict)) or v is None      # org.json coerces numbers/bools, not these

parse = []
for k, m in mobs.items():
    if not isinstance(m, dict):
        parse.append(("mobs.getJSONObject", k)); continue
    for f in ("im", "ab_el", "ab", "sp", "det"):                       # strList -> a.getString(i)
        if f in m:
            if not isinstance(m[f], list):
                parse.append(("strList optJSONArray", k, f))
            else:
                parse += [("strList getString", k, f, e) for e in m[f] if _throws_getString(e)]
    if isinstance(m.get("notes"), list):                               # notes -> arr.getString(i)
        parse += [("notes getString", k, e) for e in m["notes"] if _throws_getString(e)]
    for f in ("wk", "st"):                                             # modList -> a.getJSONArray(i)
        for e in (m.get(f) or []):
            if not isinstance(e, list) or not e or _throws_getString(e[0]):
                parse.append(("modList", k, f, e))
    for e in (m.get("zones") or []):                                   # zones -> e.getString(0)
        if isinstance(e, list) and (not e or _throws_getString(e[0])):
            parse.append(("zones getString(0)", k, e))
for k, v in abils.items():
    if not isinstance(v, dict):
        parse.append(("abilities.getJSONObject", k)); continue
    parse += [("fx getString", k, e) for e in (v.get("fx") or []) if _throws_getString(e)]
for f, v in d.get("family_icons", {}).items():                      # fo.getString(f)
    if _throws_getString(v):
        parse.append(("family_icons.getString", f))
for f, v in d.get("family_notes", {}).items():                      # no.getJSONArray(f)
    if not isinstance(v, list):
        parse.append(("family_notes.getJSONArray", f))
    else:
        parse += [("family_notes getString", f, e) for e in v if _throws_getString(e)]
for f, v in d.get("family_eco", {}).items():                        # eo.getString(f)
    if _throws_getString(v):
        parse.append(("family_eco.getString", f))
for f, v in d.get("family_subtypes", {}).items():                   # so.getJSONArray(f)  <-- rev 35 bug
    if not isinstance(v, list):
        parse.append(("family_subtypes.getJSONArray — NOT AN ARRAY", f, type(v).__name__)); continue
    for o in v:
        if not isinstance(o, dict):
            parse.append(("family_subtypes arr.getJSONObject", f)); continue
        for fl in ("wk", "st"):
            for e in (o.get(fl) or []):
                if not isinstance(e, list) or not e or _throws_getString(e[0]):
                    parse.append(("subtype modList", f, o.get("name"), fl, e))
        if isinstance(o.get("notes"), list):
            parse += [("subtype notes", f, e) for e in o["notes"] if _throws_getString(e)]
print(f"!! MobDb.load PARSE THROWS      {len(parse)}   {parse[:3]}")
if parse:
    print("   ^^ THE APP WILL SHOW ZERO MOBS. DO NOT SHIP. See handoff §4.")


# 3 ------------------------------------------------------------- abilities
H("3. ABILITIES")
undef = [a for v in mobs.values() for a in (v.get("ab") or []) if a not in abils]
print(f"UNDEFINED ability references     {len(undef)}  across {len(set(undef))} distinct names")
for n, c in Counter(undef).most_common(12):
    print(f"    {c:5d}  {n}")
stub = [k for k, v in abils.items() if isinstance(v, dict) and not v.get("d")]
print(f"\ndefs with no description (`d`)    {len(stub)}")
print(f"    {sorted(stub)[:14]}")
glued = [x for v in mobs.values() for x in (v.get("ab") or []) if re.search(r"[a-z][A-Z]", x)]
print(f"\nmalformed glued `ab` entries      {len(glued)}  ({len(set(glued))} distinct)")
glued_sp = [x for v in mobs.values() for x in (v.get("sp") or []) if re.search(r"[a-z][A-Z]", x)]
print(f"malformed glued `sp` entries      {len(glued_sp)}  {sorted(set(glued_sp))[:5]}")
# NOTE: "==" (not "===") catches ==How to Obtain== (Sinker Drill, rev 36); "'''" catches wiki bold
# (Tail Smash / Shell Charge); "^\*" catches a leaked bullet ("*Notes:" sat in Arm Cannon's *r* field,
# which is why r/tgt are scanned here too and not just d/notes.
markup = [k for k, v in abils.items() if isinstance(v, dict)
          and re.search(r"__NOTOC|==|\{\{|\[\[|File:|thumb\||\d+px|none\||'''|\{\||^\*|<br"
                        # rev 392: an INTERWIKI LINK has no brackets, so every
                        # pattern above missed "de:Magische Frucht" and
                        # "de:Schafliedja...Category:Mob Abilities" for the whole pass.
                        r"|Category:|(?:^|(?<=[a-z]))[a-z]{2}:[A-Z\u00c0-\u00ff\u3000-\u9fff]",
                        "\n".join(str(v.get(f, "")) for f in ("d", "notes", "r", "tgt")))]
print(f"defs with WIKI MARKUP in d/notes  {len(markup)}  {markup[:6]}")
# rev 392: some defs end their `notes` on a colon — the wiki had a table there and the
# scrape stopped at it, so the note promises information it does not deliver.
truncated = sorted(k for k, v in abils.items() if isinstance(v, dict)
                   and str(v.get("notes", "")).rstrip().endswith(":"))
print(f"defs whose `notes` ends on a colon {len(truncated)}  {truncated[:6]}")

# rev 394: the "Lamiae class" — a value that is fine about the mob but wrong for this
# file's vocabulary, so it renders badly on the card. All four must read 0.
OKC = {"Fire","Ice","Wind","Earth","Lightning","Water","Light","Dark","Varies","None"}
badcrys = sorted({v["crys"] for v in mobs.values() if v.get("crys") and v["crys"] not in OKC})
print(f"non-vocabulary `crys` values         {len(badcrys)}  {badcrys}")
badlv = [k for k, v in mobs.items() if v.get("lv") and (len(v["lv"]) != 2 or v["lv"][0] < 1 or v["lv"][0] > v["lv"][1])]
print(f"level ranges reversed or below 1     {len(badlv)}  {badlv[:6]}")
flatz = [k for k, v in mobs.items() for zz in (v.get("zones") or []) if not isinstance(zz, list)]
print(f"`zones` entries stored as strings    {len(flatz)}  {sorted(set(flatz))[:6]}")
badkey = [k for k, v in mobs.items() if k != v["n"].lower()]
print(f"keys that differ from n.lower()      {len(badkey)}  {badkey[:6]}")
ecobad = [k for k, v in mobs.items() if v.get("eco") and v.get("fam") and v["eco"] != fam_eco.get(v["fam"])]
print(f"per-mob `eco` fighting family_eco    {len(ecobad)}  {ecobad[:6]}")
print(f"\nability `t` vocabulary ({len(Counter(v.get('t') for v in abils.values() if isinstance(v,dict) and v.get('t')))} values — BG only has 4):")
for n, c in Counter(v.get("t") for v in abils.values() if isinstance(v, dict) and v.get("t")).most_common():
    print(f"    {c:5d}  {n}")


# 4 ----------------------------------------------------------------- drops
H("4. DROPS  (validated against ffxi_items.json key `n`)")
# rev 294: `drops` is a comma-joined STRING and 11 records hold an Abyssea name whose own
# parenthetical contains a comma — "Apademak Horn (1G, 2C)". A naive split tore each of those
# into "... (1G" + "2C)" and counted BOTH halves as invalid items. The Kotlin renders the whole
# string in one row (AuctionApp.kt:830), so the app was never affected — the CHECK was wrong.
def drop_parts(s):
    out = []
    for x in (s or "").split(", "):
        if out and out[-1].count("(") > out[-1].count(")"):
            out[-1] += ", " + x
        else:
            out.append(x)
    return [x for x in out if x]


bad = [(k, x) for k, v in mobs.items() for x in drop_parts(v.get("drops"))
       if x not in ITEM_NAMES]
gap = [t for t in bad if DB_GAP(t[1])]
real = [t for t in bad if not DB_GAP(t[1])]
print(f"invalid drop entries             {len(real)}  across {len(set(x for _, x in real))} distinct names")
print(f"  (+ known DB-gap, KEEP these)   {len(gap)}   {sorted(set(x for _,x in gap))[:3]}")
print("\ntop invalid names (belong in notes per the Drops convention):")
for n, c in Counter(x for _, x in real).most_common(12):
    print(f"    {c:5d}  {n}")


# 5 --------------------------------------------------- vocabulary pollution
H("5. VOCABULARY POLLUTION")
print("crystal:")
for n, c in Counter(v.get("crys") for v in mobs.values() if v.get("crys")).most_common():
    flag = "   <-- same crystal as Lightning" if n == "Thunder" else ("   <-- junk" if (n.islower() or len(n) < 3 or n in ("None", "Element", "Varies")) else "")
    print(f"    {c:5d}  {n!r}{flag}")
print("\njob — long form vs ABBREVIATION:")
jobs = Counter(v.get("job") for v in mobs.values() if v.get("job"))
abbrev = {j: c for j, c in jobs.items() if re.fullmatch(r"[A-Z]{3}", j or "")}
print(f"    mobs storing a bare 3-letter abbreviation: {sum(abbrev.values())}")
for n, c in sorted(abbrev.items(), key=lambda kv: -kv[1])[:10]:
    print(f"    {c:5d}  {n}")
print("\ndetection vocabulary:")
for n, c in Counter(x for v in mobs.values() for x in (v.get("det") or [])).most_common():
    print(f"    {c:5d}  {n}")
# rev 283: this check used to read z[0] on BARE-STRING zone entries too — and z[0] of a string is
# its FIRST CHARACTER, so every Behemoth-era flat string was reported as a junk single-letter zone.
# It printed a scary non-zero number every rev and never meant anything. List entries only now.
junkz = Counter(str(z[0]) for v in mobs.values() for z in (v.get("zones") or [])
                if isinstance(z, list) and len(str(z[0])) <= 2)
print(f"\njunk single-letter zone values:   {sum(junkz.values())}  {dict(junkz)}")
flatz = [(k, z) for k, v in mobs.items() for z in (v.get("zones") or []) if isinstance(z, str)]
print(f"bare-STRING zone entries (ok):    {len(flatz)}  across {len({k for k,_ in flatz})} mobs")
badz = sorted({z[0] for v in mobs.values() for z in (v.get("zones") or [])
               if re.sub(r"[^a-z0-9]", "", str(z[0]).lower()) not in ZONES_NORM
               and z[0] not in FREE_ZONES and len(str(z[0])) > 2})
# rev 318: this line used to print badz[:8] and `Outer Ra'Kaznar [U]` sat in the
# truncated tail for 30+ revs — 27 records pointing at a zone zones.json does not
# have (it has [U1]/[U2]/[U3]). Same lesson as fz.py: NEVER TRUNCATE A HIT LIST.
print(f"zones not resolving vs zones.json: {len(badz)}")
for z in badz:
    print(f"    {z}")
badsp = sorted({s for v in mobs.values() for s in (v.get("sp") or []) if SPELLS and s not in SPELLS})
print(f"spells not in jobs.json:          {len(badsp)}  {badsp[:8]}")
# rev 283: a STRING written where a LIST was expected gets iterated into single CHARACTERS.
# Found on the 3 Pso'Xja Millstones (25 one-char `notes` bullets each, rendered on the card).
# Same root cause as the junk single-letter zone check above and the bare-string `ab_el` class.
explode = {k: len(v[f]) for k, v in mobs.items() for f in ("notes", "ab", "sp", "det", "im")
           if isinstance(v.get(f), list) and len(v[f]) >= 3
           and all(isinstance(x, str) and len(x.strip()) <= 1 for x in v[f])}
print(f"CHARACTER-EXPLODED list fields:   {len(explode)}  {sorted(explode)[:6]}")


# 6 -------------------------------------------------------------- nm flags
H("6. NM FLAGS")
nmlv_no_nm = [k for k, v in mobs.items() if not v.get("nm") and v.get("nmlv")]
print(f"mobs with `nmlv` but NO `nm` key  {len(nmlv_no_nm)}   <-- nmlv OVERRIDES levelText, so lv is invisible on these")
print(f"    {sorted(nmlv_no_nm)[:12]}")
print(f"nm=True but no nmlv               {sum(1 for v in mobs.values() if v.get('nm') and not v.get('nmlv'))}")


# 7 ------------------------------------------------- zone coverage by eco
H("7. ZONE COVERAGE BY ECOSYSTEM  (std = non-NM)")
eco_of = lambda v: v.get("eco") or fam_eco.get(v.get("fam"))
agg = defaultdict(lambda: [0, 0, 0, 0])   # std_have, std_tot, nm_have, nm_tot
for v in mobs.values():
    e = eco_of(v) or "(unset)"
    i = 2 if v.get("nm") else 0
    agg[e][i + 1] += 1
    if v.get("zones"):
        agg[e][i] += 1
print(f"{'ecosystem':<14}{'std':>14}{'NM':>14}")
for e in sorted(agg):
    sh, st, nh, nt = agg[e]
    sp = f"{sh}/{st} ({100*sh//st if st else 0}%)"
    np_ = f"{nh}/{nt} ({100*nh//nt if nt else 0}%)"
    print(f"{e:<14}{sp:>14}{np_:>14}")


# 8 ------------------------------------------------------ per-family table
H("8. PER-FAMILY TABLE  (eco-set families only)")
print(f"{'family':<20}{'eco':<10}{'n':>4}{'NM':>4}{'zones':>7}{'ab':>5}{'grid':>6}{'subs':>6}  notes")
rows = []
for fam in sorted({v.get("fam") for v in mobs.values() if v.get("fam")}):
    mm = [v for v in mobs.values() if v.get("fam") == fam]
    if fam not in fam_eco:
        continue
    rows.append((fam, fam_eco.get(fam, "-"), len(mm),
                 sum(1 for v in mm if v.get("nm")),
                 sum(1 for v in mm if v.get("zones")),
                 # an EXPLICIT [] means "this family genuinely has no TP moves" (Frog) — that is
                 # filled data, not a hole. Count it; only an ABSENT key is a gap.
                 sum(1 for v in mm if v.get("ab") is not None),
                 sum(1 for v in mm if v.get("wk") or v.get("st")),
                 len(fam_subs.get(fam, [])),
                 "y" if fam in fam_notes else "-"))
for r in rows:
    print(f"{r[0]:<20}{r[1]:<10}{r[2]:>4}{r[3]:>4}{r[4]:>7}{r[5]:>5}{r[6]:>6}{r[7]:>6}  {r[8]}")
print(f"\n{len(rows)} families have family_eco set (= processed).")
print(f"{len({v.get('fam') for v in mobs.values() if v.get('fam')}) - len(rows)} families still have no eco (= not yet processed).")
print()
