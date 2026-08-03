#!/usr/bin/env python3
# Rev 122 — Sinister Reign NMs. Consolidates 3 split-dup pairs, fixes Sajj'aka's
# transposed grid, enriches/creates ability defs, installs renders.
import json, os
from PIL import Image

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets')
MJ = os.path.join(ASSETS, 'mobs.json')
IMG = os.path.join(ASSETS, 'mobimages')
U = '/mnt/user-data/uploads/'

d = json.load(open(MJ)); m = d['mobs']; A = d['abilities']

def setab(name, spec):
    A[name] = spec

# ---------- ABILITY DEFS ----------
# Arciela kit (create all 14)
setab("Dynastic Gravitas", {"d":"AoE physical attack. Additional effect: Amnesia.","t":"Physical","r":"10'","tgt":"AoE","fx":["Amnesia"]})
setab("Bellatrix of Light", {"d":"Self-buff: switches Arciela to light mode (higher magic evasion).","t":"Buff","tgt":"Self"})
setab("Bellatrix of Shadows", {"d":"Self-buff: switches Arciela to dark mode (magic accuracy bonus).","t":"Buff","tgt":"Self"})
setab("Guiding Light", {"d":"Grants Arciela and Ygnas Magic Defense Boost, Magic Attack Boost, Attack Boost, and Defense Boost.","t":"Buff","r":"10'","tgt":"Self","fx":["Magic Def. Boost","Magic Atk. Boost","Attack Boost","Defense Boost"]})
setab("Illustrious Aid", {"d":"Restores about 1200 HP to Arciela and Ygnas.","t":"Buff","r":"10'","tgt":"Self"})
setab("Darkest Hour", {"d":"Disables sub jobs for 30 seconds.","t":"Physical","tgt":"Single"})
setab("Ascension", {"d":"AoE damage; switches Arciela to light mode.","t":"Magical","el":"Light","tgt":"AoE"})
setab("Descension", {"d":"AoE damage; switches Arciela to dark mode.","t":"Magical","el":"Dark","tgt":"AoE"})
setab("Dignified Awe", {"d":"AoE. Additional effects: Amnesia and Bind.","r":"10'","tgt":"AoE","fx":["Amnesia","Bind"]})
setab("Expunge Magic", {"d":"Frontal-cone ability.","r":"Conal","tgt":"Single"})
setab("Sight Unseen", {"tgt":"AoE"})
setab("Unceasing Dread", {"tgt":"AoE"})
setab("Harmonic Displacement", {"d":"AoE ability.","tgt":"AoE"})
setab("Naakual's Vengeance", {"d":"Summons one of the six Naakuals to use a single ability.","t":"Magical","tgt":"AoE","notes":"Achuka \u2192 Incinerating Lahar; Colkhab \u2192 Incisive Apotheosis; Tchakka \u2192 Marine Mayhem; Yumcax \u2192 Tiiimbeeer; Hurkan \u2192 Static Prison; Kumhau \u2192 Glassy Nova."})

# Ingrid kit (create 5)
setab("Judgment", {"d":"Single-target magical attack.","t":"Magical","tgt":"Single"})
setab("Realmrazer", {"d":"Single-target physical attack.","t":"Physical","tgt":"Single"})
setab("Flash Nova", {"d":"Single-target magical attack.","t":"Magical","tgt":"Single"})
setab("Ruthlessness", {"d":"Frontal cone: drains about 1500 HP and inflicts Amnesia.","t":"Magical","r":"10'","tgt":"Single","fx":["Drain","Amnesia"]})
setab("Self-Aggrandizement", {"d":"Self-buff: restores about 1000 HP.","t":"Buff","tgt":"Self"})

# August kit (create 2)
setab("Daybreak", {"d":"AoE damage; starts the 60-second timer for No Quarter.","tgt":"AoE"})
setab("No Quarter", {"d":"Frontal line dealing up to 9999 damage, distributed among those hit. Used 60 seconds after Daybreak.","r":"Line","tgt":"AoE","notes":"Avoid by standing far from August, or by stunning No Quarter. If he is stunned at the 60-second mark he must recast Daybreak to reset the timer."})

# Darrcuiln kit (enrich existing stubs)
setab("Stalking Prey", {"d":"AoE hate reset. Additional effect: Terror.","t":"Physical","r":"10'","tgt":"AoE","fx":["Terror"]})
setab("Howling Gust", {"d":"AoE wind damage. Additional effects: Knockback, Silence, and Choke.","t":"Magical","el":"Wind","r":"10'","tgt":"AoE","fx":["Knockback","Silence","Choke"]})
setab("Starward Yowl", {"d":"AoE. Additional effects: Knockback and Bind.","t":"Physical","r":"10'","tgt":"AoE","fx":["Knockback","Bind"]})
setab("Righteous Rasp", {"d":"Frontal cone. Additional effects: Magic Defense Down and Defense Down.","t":"Physical","r":"Conal","tgt":"Single","fx":["Magic Def. Down","Defense Down"]})
setab("Aurous Charge", {"d":"Frontal cone. Additional effect: Flash.","t":"Physical","r":"Conal","tgt":"Single","fx":["Flash"]})

# Teodor kit (enrich existing stubs)
setab("Hemocladis", {"d":"Large AoE, deals about 800-1100 damage.","r":"L","tgt":"AoE"})
setab("Frenzied Thrust", {"d":"AoE, deals about 500-1200 damage.","tgt":"AoE"})
setab("Open Coffin", {"d":"AoE damage. Additional effect: Bio.","el":"Dark","tgt":"AoE","fx":["Bio"]})
setab("Ravenous Assault", {"d":"AoE Drain.","tgt":"AoE","fx":["Drain"]})
setab("Sinner's Cross", {"d":"AoE, deals about 500-700 damage.","tgt":"AoE"})
setab("Start From Scratch", {"d":"Removes all status ailments from the caster.","tgt":"Self"})

# ---------- MOB RECORDS ----------
# arciela
a = m['arciela']
a['nm'] = True
a['drops'] = "Himetsuruichimonji, Humility, Lengo Pants, Leyline Gloves, Taming Sari, Ochu, Witching Robe, Enticer's Pants"
a['zones'] = [["Rala Waterways [U]"]]
a['spawn'] = "Sinister Reign (Rala Waterways [U]) \u2014 first NM in Wave 1, third NM in Wave 3."
a['notes'] = [
 "Functions almost like the Arciela trust: her hits carry an added Stun effect and she sometimes puts up a Flash aura. Will not give chase and deals only magic damage.",
 "Magic evasion is naturally high (higher in light mode); dark mode instead grants a magic accuracy bonus. Uses Red Mage enfeebles, buffs, and tier V nukes.",
 "Assisted by Ygnas in Wave 1, and by the six Naakuals (Achuka, Colkhab, Tchakka, Yumcax, Hurkan, Kumhau) in Wave 3.",
]
a['img'] = "mobimages/arciela.png"

# darrcuiln — merge (npc) into base
a = m['darrcuiln']
a['n'] = "Darrcuiln"
a['nm'] = True
a['det'] = ["Sight", "Sound"]           # icon-verified; was [Scent] here / bad 4-stamp on (npc)
a['ab'] = ["Stalking Prey", "Howling Gust", "Starward Yowl", "Righteous Rasp", "Aurous Charge"]
a['drops'] = "Fleshcarvers, Koresuke, Amm Greaves, Ta'lab Trousers"
a['zones'] = [["Rala Waterways [U]"]]
a['spawn'] = "Sinister Reign (Rala Waterways [U])."
a['notes'] = [
 "His Stalking Prey does an AoE hate reset plus Terror.",
 "Has the poorest magic evasion of the Sinister Reign bosses \u2014 mages do exceptionally well and he is generally considered the easiest boss. Likely classified as a Beast.",
]
a['img'] = "mobimages/darrcuiln.png"
del m['darrcuiln (npc)']

# ingrid
a = m['ingrid']
a['nm'] = True
a['lv'] = [130, 130]
a['drops'] = "Malevolence, Purgation, Fanatic Gloves, Dampening Tam, Cipher: Ingrid II"
a['zones'] = [["Rala Waterways [U]"]]
a['spawn'] = "Sinister Reign (Rala Waterways [U]) \u2014 a Round 1 boss."
a['notes'] = [
 "The most aggressive of the Round 1 bosses and the only one that makes regular melee swings \u2014 and she has Counter.",
 "Uses Divine nukes (Banish IV, Holy II), Judgment, Realmrazer, and Flash Nova, plus the unique AoE Drain/Amnesia move Ruthlessness. Does not buff herself.",
]
a['img'] = "mobimages/ingrid.png"

# teodor
a = m['teodor']
a['nm'] = True
a['det'] = ["Sight", "Sound"]           # cleaned from [Sight,Sound,True Sight,True Sound]
a['drops'] = "Rubicundity, Samnuha Coat, Samnuha Tights, Vampirism"
a['zones'] = [["Rala Waterways [U]"]]
a['spawn'] = "Sinister Reign / SoA Mission 5-3-2 (Rala Waterways [U])."
a['notes'] = [
 "Uses Endspel and Ensilence; because his normal hits are TP moves, those two pass through Utsusemi shadows (though they do not wipe them).",
 "Uses Start From Scratch at 25% HP and Hemocladis roughly a minute later (under 10% HP in the mission fight).",
 "The mission fight drops the Aged Undying Naakual crest.",
]
a['img'] = "mobimages/teodor.png"

# morimar — merge (nm) into base
src = m['morimar (nm)']
a = m['morimar']
a['n'] = "Morimar"
a['nm'] = True
a['fam'] = src['fam']                    # Humanoid
a['ab'] = list(src['ab'])                # Into The Light, Camaraderie of the Crevasse, Arduous Decision, Vehement Resolution, 12 Blades of Remorse
a['img'] = "mobimages/morimar.png"
del m['morimar (nm)']

# rosulatia — already complete; add render
m['rosulatia']['img'] = "mobimages/rosulatia.png"

# august
a = m['august']
a['nm'] = True
a['drops'] = "Cipher: August, Founder's Corona, Founder's Gauntlets, Founder's Hose, Founder's Greaves"
a['zones'] = [["Rala Waterways [U]"]]
a['spawn'] = "Sinister Reign (Rala Waterways [U])."
a['notes'] = [
 "No Quarter is used 60 seconds after Daybreak and deals up to 9999 damage in a frontal cone, split among everyone it hits. Avoid it by standing far from August or by stunning No Quarter.",
 "If August is stunned at the 60-second mark he will not use No Quarter and must recast Daybreak to reset the timer.",
]
a['img'] = "mobimages/august.png"

# ygnas — keep kit (additive); add render
m['ygnas']['img'] = "mobimages/ygnas.png"

# sajj'aka — rename (nm)->base; FIX transposed grid; canonicalize zone; clean note
s = m.pop("sajj'aka (nm)")
s['n'] = "Sajj'aka"
s['nm'] = True
# grid per image 14: Light 5% (-95%), all others 50% (-50%), Dark 150% (+50% weak)
s['st'] = [["Fire","-50%"],["Wind","-50%"],["Lightning","-50%"],["Light","-95%"],["Ice","-50%"],["Earth","-50%"],["Water","-50%"]]
s['wk'] = [["Dark","+50%"]]
s['zones'] = [["Rala Waterways [U]"]]
s['spawn'] = "Sinister Reign, Wave 3 (Rala Waterways [U])."
s['notes'] = ["Breaking the scale on its chest with dark damage and dark skillchains significantly reduces the damage dealt by Denounce."]
s['img'] = "mobimages/sajjaka.png"
m["sajj'aka"] = s

# ---------- null-poison guard ----------
bad = [k for mm in m.values() for k,v in mm.items() if v is None]
assert not bad, ("NULL POISON", bad)
bad2 = [k for ab in A.values() for k,v in ab.items() if v is None]
assert not bad2, ("NULL POISON ABILITIES", bad2)

json.dump(d, open(MJ,'w'), separators=(', ', ': '), ensure_ascii=False)
print("mobs.json written. mobs=%d abilities=%d" % (len(m), len(A)))

# ---------- RENDERS ----------
def load(fn): return Image.open(U+fn).convert('RGB')
def cap(im, mx=400):
    w,h=im.size
    if max(w,h)<=mx: return im
    s=mx/max(w,h); return im.resize((round(w*s),round(h*s)), Image.LANCZOS)
def white_trim(im):
    import numpy as np
    a=np.asarray(im).astype(int); r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
    mx=np.maximum(np.maximum(r,g),b); mn=np.minimum(np.minimum(r,g),b)
    nonwhite=((mx-mn)>18)|(mn<235)
    ys,xs=np.where(nonwhite)
    if len(xs)==0: return im
    pad=4
    x0=max(0,xs.min()-pad); y0=max(0,ys.min()-pad)
    x1=min(im.width,xs.max()+1+pad); y1=min(im.height,ys.max()+1+pad)
    return im.crop((x0,y0,x1,y1))

os.makedirs(IMG, exist_ok=True)
jobs = [
 ('Arciela.png',        'arciela.png',   False),
 ('Darrcuiln.jpg',      'darrcuiln.png', False),
 ('Ingrid.jpg',         'ingrid.png',    False),
 ('Teodor.png',         'teodor.png',    False),
 ('Morimar.png',        'morimar.png',   False),
 ('Rosultatia.jpg',     'rosulatia.png', False),
 ('800px-August.png',   'august.png',    False),
 ('Category-Leafkin.jpg','ygnas.png',    True),   # white bg -> trim
 ('Sajjaka.jpg',        'sajjaka.png',   False),
]
for src_fn, out_fn, trim in jobs:
    im = load(src_fn)
    if trim: im = white_trim(im)
    im = cap(im, 400)
    im.save(os.path.join(IMG, out_fn))
    print(f"render {out_fn:16s} <- {src_fn:22s} {im.size}")
print("DONE")
