# Rev 340 — six Unknown-bucket records stamped from their own BG pages.
# Fill-blanks-only (rule 280): a field is written ONLY when the record is empty there.
# Zones are unioned; a level-less existing zone entry may be FILLED, never overwritten.
# Author: BalladOfWorms
import json, copy

P = "/home/claude/android/app/src/main/assets/mobs.json"
d = json.load(open(P, encoding="utf-8"))
M = d["mobs"]
ABIL = d["abilities"]
FAMS = set(d["families"])
ECO = d["family_eco"]
before = copy.deepcopy({k: M[k] for k in
                        ["bonesoaked bandit", "bufobrawler", "dolorous cyhiraeth",
                         "doom lens", "earth mover", "enshrouded cyhiraeth"]})
log = []


def setif(key, field, value):
    """Write only into an empty field (rule 280). Log what the page said either way."""
    r = M[key]
    cur = r.get(field)
    if cur in (None, "", [], {}):
        r[field] = value
        log.append(f"  {key}: {field} = {value!r}")
    elif cur != value:
        log.append(f"  {key}: {field} KEPT {cur!r} (page said {value!r})")


def add_det(key, dets):
    r = M[key]
    cur = list(r.get("det") or [])
    for x in dets:
        if x not in cur:
            cur.append(x)
    if cur != (r.get("det") or []):
        r["det"] = cur
        log.append(f"  {key}: det -> {cur}")


def zone(key, name, levels=None):
    """Add a zone, or fill a level-less entry. Never overwrite a stored range."""
    r = M[key]
    zs = r.setdefault("zones", [])
    for e in zs:
        if e[0] == name:
            if levels and len(e) == 1:
                e.append(levels)
                log.append(f"  {key}: zone {name} level filled {levels}")
            elif levels and len(e) > 1 and e[1] != levels:
                log.append(f"  {key}: zone {name} KEPT {e[1]!r} (page said {levels!r})")
            return
    zs.append([name, levels] if levels else [name])
    log.append(f"  {key}: zone ADDED {name} {levels or ''}")


def note(key, text):
    ns = M[key].setdefault("notes", [])
    if text not in ns:
        ns.append(text)
        log.append(f"  {key}: note + {text!r}")


# --- 1. Bonesoaked Bandit — Family: Skeletons, Job: Warrior. Rala Waterways [U], Skirmish.
#        Notes A, L, T(S), T(H), HP  ->  aggressive, links, True Sight, True Sound, Blood.
setif("bonesoaked bandit", "fam", "Skeleton")
setif("bonesoaked bandit", "job", "Warrior")
M["bonesoaked bandit"]["agg"] = True
M["bonesoaked bandit"]["lnk"] = True
add_det("bonesoaked bandit", ["True Sight", "True Sound", "Blood"])

# --- 2. Bufobrawler — Family: Toads (= our Frog family), Job: Warrior. Notes A, L, T(S), T(H).
setif("bufobrawler", "fam", "Frog")
setif("bufobrawler", "job", "Warrior")
M["bufobrawler"]["agg"] = True
M["bufobrawler"]["lnk"] = True
add_det("bufobrawler", ["True Sight", "True Sound"])

# --- 3. Dolorous Cyhiraeth — Family: Corpselight, Crystal: Dark. Outer RaKaznar 117-120.
#        Page Job field is BLANK (not "None") -> family default fills it.
setif("dolorous cyhiraeth", "fam", "Corpselight")
setif("dolorous cyhiraeth", "job", "Black Mage")
setif("dolorous cyhiraeth", "crys", "Dark")
zone("dolorous cyhiraeth", "Outer RaKaznar", "117-120")

# --- 4. Enshrouded Cyhiraeth — family from an AI answer panel, NOT BG: take the family only,
#        and it agrees with all five Corpselight siblings. Its 113-115 is NOT written over the
#        stored [113,116] / "113-116" (weaker source).
setif("enshrouded cyhiraeth", "fam", "Corpselight")
setif("enshrouded cyhiraeth", "job", "Black Mage")
setif("enshrouded cyhiraeth", "crys", "Dark")

# --- 5. Doom Lens — Job Warrior/Black Mage, Family: Ahriman, Crystal: Dark.
#        Castle Zvahl Baileys [S] 84-85 (22 spawns) · Castle Zvahl Keep [S] 82-83 (6 spawns),
#        both respawn 16 min (= the stored resp 960). Notes A, L, S, H already match.
#        Drops (Ahriman Lens/Tears/Wing) are crafting materials -> omitted per the drops rule;
#        no Ahriman-family record stores them.
setif("doom lens", "fam", "Ahriman")
setif("doom lens", "job", "Warrior / Black Mage")
setif("doom lens", "crys", "Dark")
zone("doom lens", "Castle Zvahl Baileys [S]", "84-85")
zone("doom lens", "Castle Zvahl Keep [S]", "82-83")

# --- 6. Earth Mover — Family: ACROLITHS, not Chariots. Same Bastion roster as `edifier`
#        (identical lv [85,87] + the same three Abyssea zones + the same content tags), so the
#        roster spans MORE THAN ONE FAMILY. Page carries the red Notorious Monster banner.
#        Crystal: None -> the file expresses that by ABSENCE, never the string "None".
#        Weak/Resistant cells are '?' -> not data, nothing written.
setif("earth mover", "fam", "Acrolith")
M["earth mover"]["nm"] = True
log.append("  earth mover: nm = True (page carries the Notorious Monster banner)")
note("earth mover", "Spawns during Bastion; only aggressive to players with Pennant status.")
note("earth mover", "Four spawns across Abyssea-Attohwa, Abyssea-Misareaux and Abyssea-Vunkerl.")

# ---------------- guards ----------------
assert not [k for m in M.values() for k, v in m.items() if v is None], "null poison"
# The file carries a pre-existing pile of undefined ability names (rule 282), so the guard is
# "this rev added none", not "there are none".
UNDEF_BEFORE = 74
undef = {a for v in M.values() for a in (v.get("ab") or []) if a not in ABIL}
assert len(undef) <= UNDEF_BEFORE, f"this rev added undefined ability refs: {len(undef)}"
for k in before:
    f = M[k].get("fam")
    assert f in FAMS, (k, f)
    assert ECO.get(f), (k, f, "family has no eco -> would render under Other")
for k, old in before.items():
    for fld, val in old.items():
        if isinstance(val, (str, int)) and fld not in ("agg", "lnk", "nm"):
            assert M[k].get(fld) == val, (k, fld, "clobbered")

json.dump(d, open(P, "w", encoding="utf-8"), separators=(", ", ": "), ensure_ascii=False)
print("\n".join(log))
print()
orphans = sum(1 for v in M.values() if not v.get("fam"))
print("mobs", len(M), "| orphans", orphans, "| NM-flagged", sum(1 for v in M.values() if v.get("nm")))
