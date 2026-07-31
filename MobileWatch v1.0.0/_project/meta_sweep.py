#!/usr/bin/env python3
"""Strip PROVENANCE / WIKI-MECHANICS prose out of every note surface that RENDERS on a mob card.

USER 2026-07-16: "i dont need this kind of info in the notes. if a specific mob doesnt have a table,
just fall back to family table, but we dont need explanations of it in the mobs card."

Renders on the card: mob.notes + subtype notes + family_notes (General Notes section) AND every
ability def's `notes` (AuctionApp.kt:942, under the description when the row is expanded).

Works at SENTENCE level, not bullet level — most polluted bullets are "<game fact>. <meta sentence>."
Author: BalladOfWorms
"""
import json, re, sys

META = re.compile(r"""(
  # --- our pipeline talking about itself
    family\ stamp | the\ stamp\b | \bstamp\b | \bstamped\b | \bstamps\b | stamp\ stands
  | our\ record | its\ old\ record | the\ file\b | the\ file's | the\ record\ (has|had|is|carries)
  | the\ import\b | \bimported\b | import\ data | pre-existing | left\ as\ found | left\ additive
  | not\ page-(sourced|verified) | \bfiled\b | the\ values\ here | values\ here\ are
  | grid\ here | \bnot\ its\ own\b | the\ sub-type's | \brecorded\ here\b | the\ recorded\b
  | was\ undefined | \bundefined\b | was\ null | 0\ refs | \bis\ kept\b | \bwas\ kept\b
  | open\ item | open\ \([a-z]{1,3}\) | user's\ call | \bUSER: | 2026-07 | pending\ the
  | item\ DB | \bDB\ (has|form|abbrev)
  | as\ unknown | Target\ column | shadow\ column | Area\ column | Y'\ column | \bcolumn\ (reads|is|names)
  | NEEDS\ A\ REAL\ DEF | sourced\ from | was\ captured | no\ Area,\ Type
  | family\ grid\ unchanged | ^No\ (Job|level|resist\ grid|Area)\b | Its\ Class\ as
  | (Green|purple|red|blue)\ (Buff\ )?disc | Detects\ box | \bthe\ literal\ text\b
  | already\ on\ file | were\ wrong | \bmisspelling\b | Event\ table | folded\ into
  | the\ old\ def | old\ def's | the\ existing\ def | previous\ def
  | \bleft\ unset\b | rather\ than\ guessed | not\ guessed | precedent\) | \bhandoff\b
  | browser\ artifact | category\ read | \bType\ icon\b | \bthe\ row\ is\b | \brow\ reads\b
  | is\ written\ into\ the\ name\ cell | name\ cell | \bflags\ the\b | as\ uncertain
  | documented\ category\ colou?rs? | literal\ string | \bcopy\ of\ the\ table\b
  # --- the wiki's layout / publication talking
  | publish(es|ed|ing)?\b | unpublished | not\ published
  | \bpages?\b | \bwiki\b | \bBG\b | \bBG-wiki\b
  | category\ (ability\ )?table | category\ page | category\ grid | category\ list
  | category\ NM\ table | the\ category(?:'s)? | \bNM\ table\b | NM-summary
  | \bAdversaries\b | \bListings\b | \bBestiary\b | Event\ Appearances
  | Condition\ column | Type\ column | Abilities\ column | Spells\ column | Level\ cell
  | rose[- ]?shad | rose\ row | un-rose | \brose-shaded\b
  | Discussion | testimonial | \{\{ | ===  | info-icon | tooltip
  # --- measurement / method / cross-mob comparison
  | distance\ 0\.0 | \bNCC\b | \bIoU\b | corr\ \+ | pixel-identical | screenshot | colour-match
  | its\ (whole\ )?grid\ is | grid\ is\ (entirely|painted) | '\?' | \bnot\ data\b
  | Owners\ so\ far | each\ from\ its\ own | that\ publish | its\ own\ grid
  | the\ only\ .{0,24}\ that\ (publish|carr|list)
)""", re.I | re.X)

# ordinary game prose that trips a marker by accident — never strip these
KEEP = re.compile(r"(unconscious|arose|rose\ from|Rosethorn)", re.I)

# a surviving fragment that starts mid-thought, or has no words, was never a standalone fact
DANGLING = re.compile(r"^(?:[a-z]|\*|and\b|but\b|which\b|that\b|also\b|as\b|so\b|no\b|or\b)|[,;:]\s*$")

def sentences(text):
    """split on sentence enders, but never inside (F-8/9). / +1. / common abbreviations"""
    out, buf = [], ""
    text = text.replace("!!", "\u0001")          # FFXI proc marker, not punctuation
    for t in re.split(r'(?<=[.!?])\s+', text):
        buf = (buf + " " + t).strip() if buf else t
        if re.search(r"\b(approx|vs|e\.g|i\.e|incl|Lv|Mr|St|min|hrs?|ca|etc)\.$", buf):
            continue
        out.append(buf); buf = ""
    if buf: out.append(buf)
    return [x.replace("\u0001", "!!") for x in out]

ATTRIB = re.compile(r"""^\s*
   (?:
      (?:[A-Z][\w'\u2019.-]*(?:\ [A-Z][\w'\u2019.-]*){0,3}'s\ (?:own\ )?page)
    | (?:Its\ (?:own\ )?page(?:'s\ \w+\ column)?)
    | (?:The\ [\w' -]{0,18}category(?:\ ability)?\ table)
    | (?:The\ category(?:\ page)?)
    | (?:The\ wiki) | (?:BG(?:-wiki)?)
   )
   \s*(?:also\ )?
   (?:says|adds|notes|describes\ it\ as|describes|lists|calls\ it|calls|publishes\ the\ \w+\ as
     |publishes|gives|prints|states|reads|records|has)?
   \s*(?:that\ )?[:,]?\s*""", re.X)

def strip_attrib(s):
    """'Pakecet's page adds that X summons its adds' -> 'X summons its adds'"""
    m = ATTRIB.match(s)
    if not m or m.end() == 0: return s
    if s[m.end():m.end()+2] == "'s": return s      # we cut a possessive in half — leave it to META
    rest = s[m.end():].strip()
    if len(rest) < 12 or not re.search(r"[A-Za-z]{4}", rest): return s
    return rest[0].upper() + rest[1:]

CLAUSE = re.compile(r'\s*(?:;|\u2014)\s*')

def is_meta(s):
    return bool(META.search(s)) and not KEEP.search(s)

def strip_parens(s):
    """drop whole parentheticals that are pure provenance: '(not in item DB)', '(unnamed on the page)'"""
    def f(m):
        return "" if is_meta(m.group(0)) else m.group(0)
    return re.sub(r"\s*\([^()]*\)", f, s)

MARKUP_ONLY = re.compile(r"^\s*(\*+|\*See also:.*|_+|-+)\s*$")

def clean(text):
    """-> (cleaned_or_None, [dropped fragments]). Clause by clause, and a fragment is only
    style-judged when we actually cut something out of it."""
    if MARKUP_ONLY.match(text):
        return None, [text]
    kept, dropped, changed = [], [], False
    for sent in sentences(text):
        cut = False
        s2 = strip_parens(sent)
        if s2 != sent: cut = True
        s3 = strip_attrib(s2)
        if s3 != s2:
            if is_meta(s3):                       # the fact behind the attribution was meta too
                dropped.append(sent); continue
            s2, cut = s3, True
        clauses = CLAUSE.split(s2)
        good = [c for c in clauses if c.strip() and not is_meta(c)]
        if len(good) != len([c for c in clauses if c.strip()]): cut = True
        if not good:
            dropped.append(sent); continue
        out = "; ".join(x.strip().rstrip(",;") for x in good)
        if not out.endswith((".", "!", "?")): out += "."
        if cut and (DANGLING.search(out) or out.count('"') % 2):
            dropped.append(sent); continue        # what's left starts mid-thought
        if cut: changed = True
        kept.append(out if cut else sent)
    if not kept:
        return None, dropped
    if not dropped and not changed:
        return text, []                           # untouched — byte-identical
    out = re.sub(r"\s{2,}", " ", " ".join(kept)).strip()
    if DANGLING.search(out) or not re.search(r"[A-Za-z]{2}", out):
        return None, dropped + kept
    return out, dropped

def main(assets, apply=False):
    P = assets + "/mobs.json"
    d = json.load(open(P, encoding="utf-8"))
    M, A = d["mobs"], d["abilities"]
    rep = {"dropped_bullet": [], "trimmed": [], "ability_dropped": [], "ability_trimmed": []}

    # ---- mob.notes (list of strings)
    for k, v in M.items():
        ns = v.get("notes")
        if not ns: continue
        out = []
        for n in ns:
            c, dr = clean(n)
            if c is None:
                rep["dropped_bullet"].append((k, n))
            else:
                if c != n: rep["trimmed"].append((k, n, c))
                out.append(c)
        if out: v["notes"] = out
        elif "notes" in v: del v["notes"]

    # ---- family_notes (list of strings)
    for k, arr in list(d["family_notes"].items()):
        if not arr: continue
        out = []
        for n in arr:
            c, dr = clean(n)
            if c is None: rep["dropped_bullet"].append(("FAM:" + k, n))
            else:
                if c != n: rep["trimmed"].append(("FAM:" + k, n, c))
                out.append(c)
        if out: d["family_notes"][k] = out
        else: del d["family_notes"][k]

    # ---- subtype notes
    for k, arr in d["family_subtypes"].items():
        for s in (arr or []):
            ns = s.get("notes")
            if not ns: continue
            if isinstance(ns, str): ns = [ns]          # schema says list-of-bullets
            out = []
            for n in ns:
                c, dr = clean(n)
                if c is None: rep["dropped_bullet"].append(("SUB:%s/%s" % (k, s.get("name")), n))
                else:
                    if c != n: rep["trimmed"].append(("SUB:%s/%s" % (k, s.get("name")), n, c))
                    out.append(c)
            if out: s["notes"] = out
            elif "notes" in s: del s["notes"]

    # ---- ability notes (a STRING, not a list)
    for k, v in A.items():
        n = v.get("notes")
        if not n: continue
        c, dr = clean(n)
        if c is None:
            rep["ability_dropped"].append((k, n)); del v["notes"]
        elif c != n:
            rep["ability_trimmed"].append((k, n, c)); v["notes"] = c

    # ---- guards
    bad = [(k, kk) for k, m in M.items() for kk, x in m.items() if x is None]
    assert not bad, bad
    bad = [(k, kk) for k, a in A.items() for kk, x in a.items() if x is None]
    assert not bad, bad
    assert not [(k, kk) for k, m in M.items() for kk, x in m.items() if x == ""]

    if apply:
        json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)
    return rep

if __name__ == "__main__":
    assets = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
    apply = "--apply" in sys.argv
    r = main(assets, apply)
    print("bullets REMOVED entirely : %d" % len(r["dropped_bullet"]))
    print("bullets TRIMMED          : %d" % len(r["trimmed"]))
    print("ability notes REMOVED    : %d" % len(r["ability_dropped"]))
    print("ability notes TRIMMED    : %d" % len(r["ability_trimmed"]))
    print("APPLIED" if apply else "DRY RUN")
    with open("/home/claude/meta_report.txt", "w") as f:
        for tag in ("dropped_bullet", "ability_dropped"):
            f.write("\n===== %s (%d)\n" % (tag.upper(), len(r[tag])))
            for k, n in r[tag]: f.write("[%s] %s\n" % (k, n))
        for tag in ("trimmed", "ability_trimmed"):
            f.write("\n===== %s (%d)\n" % (tag.upper(), len(r[tag])))
            for k, a, b in r[tag]: f.write("[%s]\n  OLD %s\n  NEW %s\n" % (k, a, b))
    print("report -> /home/claude/meta_report.txt")
