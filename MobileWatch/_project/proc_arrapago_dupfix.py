#!/usr/bin/env python3
"""
proc_arrapago_dupfix.py — rev 302 in-pass correction.

Six of proc_zone_arrapago.py's 17 zone adds landed on the DOTTED half of a dotted/spaced
split-duplicate pair whose SPACED half was ALREADY holding `Arrapago Reef`. Writing both puts
the same mob in the Zone view twice — the exact outcome rev 283 refused for the Pso'Xja
Gargoyles ("zoning the hyphenated four would put EIGHT Gargoyles in the zone list").

So: revert the six adds, and where the page publishes a level the ZONED twin lacks, fill it
there instead — write to whichever half is actually in the Zone view.

NOTHING IS MERGED OR DELETED. The pair class is a ruling for the user.

Author: BalladOfWorms
"""
import json, os, sys

ZONE = "Arrapago Reef"
ASSETS = sys.argv[1] if len(sys.argv) > 1 else "app/src/main/assets"
PATH = os.path.join(ASSETS, "mobs.json")

# dotted half (revert my add)  ->  spaced/suffixed half that already holds the zone
REVERT = {
    "lamie no.7":   "lamie no 7",
    "lamie no.8":   "lamie no 8",
    "lamie no.9":   "lamie no 9",
    "lamie no.19":  "lamia no 19",
    "merrow no.5":  "merrow no 5",
    "giant orobon": "giant orobon (fished)",
}

# page levels to write onto the ZONED twin where it holds the zone with no level
TWIN_FILL = {
    "lamie no 9": "~80",
    "giant orobon (fished)": "78-83",
}


def zname(e):
    return e[0] if isinstance(e, list) else e


def main():
    d = json.load(open(PATH, encoding="utf-8"))
    mobs = d["mobs"]
    reverted, filled = [], []

    for dotted, twin in REVERT.items():
        r = mobs[dotted]
        zs = r.get("zones") or []
        new = [e for e in zs if zname(e) != ZONE]
        if len(new) != len(zs):
            r["zones"] = new
            if not new:
                del r["zones"]           # back to no `zones` key at all, as it was
            reverted.append((dotted, twin))

    for twin, lvl in TWIN_FILL.items():
        r = mobs[twin]
        zs = r["zones"]
        for i, e in enumerate(zs):
            if zname(e) == ZONE:
                cur = e[1] if isinstance(e, list) and len(e) > 1 else None
                if cur is None:
                    zs[i] = [ZONE, lvl]
                    filled.append((twin, lvl))
                elif cur != lvl:
                    filled.append((twin, f"NOT CHANGED (holds {cur}, page {lvl})"))

    bad = [k for m in mobs.values() for k, v in m.items() if v is None]
    assert not bad
    json.dump(d, open(PATH, "w", encoding="utf-8"),
              separators=(", ", ": "), ensure_ascii=False)

    print(f"REVERTED ({len(reverted)}) — dotted half unzoned again, spaced twin keeps the zone:")
    for a, b in reverted:
        print(f"   {a:16s} (twin already zoned: {b})")
    print(f"\nFILLED ON THE ZONED TWIN ({len(filled)}):")
    for a, b in filled:
        print(f"   {a:24s} -> {b}")

    print("\nVerification — one Arrapago entry per real mob:")
    for dotted, twin in REVERT.items():
        dz = [e for e in (mobs[dotted].get("zones") or []) if zname(e) == ZONE]
        tz = [e for e in (mobs[twin].get("zones") or []) if zname(e) == ZONE]
        print(f"   {dotted:16s} {str(dz):28s} | {twin:24s} {tz}")


if __name__ == "__main__":
    main()
