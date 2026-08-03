import json, os
import numpy as np
from PIL import Image
base="app/src/main/assets"
d=json.load(open(base+"/mobs.json"))
m=d['mobs']; ab=d['abilities']; fe=d['family_eco']; fic=d['family_icons']

# ---------- family_eco ----------
fe["Humanoid"]="Unclassified"      # Kam'lanaut + Ark Angel HM boxes: Type=Unclassified, Family=Humanoid
fe["Shadow Lord"]="Demon"          # Shadow Lord box: Type=Demons; align to existing Demon eco

# ---------- ABILITIES: create ----------
new_ab={
 "Light Blade":{"d":"A three-hit weaponskill dealing severe damage; the damage taken is reduced by kiting.","t":"Physical","tgt":"Single"},
 "Great Wheel":{"d":"A two-hit area-of-effect attack that also resets enmity.","t":"Physical","tgt":"AoE","fx":["Hate Reset"]},
 "Cross Reaver":{"d":"A unique weaponskill dealing cone damage (~500-900) with an additional Stun effect.","t":"Physical","tgt":"Cone AoE","fx":["Stun"]},
 "Swift Blade":{"d":"A single-target sword weaponskill.","t":"Physical","tgt":"Single"},
 "Chant du Cygne":{"d":"A three-hit sword weaponskill with a high critical hit rate.","t":"Physical","tgt":"Single"},
 "Damning Edict":{"d":"Signals the start of physical immunity and the end of magical immunity; the Shadow Lord's sword gains a purple aura and he favors Firaja while active.","notes":"First form, \u2605 battle only."},
 "Swath of Silence":{"d":"Signals the start of magical immunity and the end of physical immunity; the Shadow Lord's palm faces up and glows purple.","notes":"First form, \u2605 battle only."},
 "Bowels of Agony":{"d":"A limited-range attack used exclusively during the second form (\u2605), alongside Implosion.","tgt":"AoE"},
}
for k,v in new_ab.items():
    assert k not in ab, k
    ab[k]=v

# ---------- ABILITIES: enrich (all confirmed Shadow-Lord-only) ----------
ab["Dark Nova"]["el"]="Dark"
ab["Implosion"]["el"]="Dark"
if "Removes Utsusemi" not in ab["Implosion"]["d"]:
    ab["Implosion"]["d"]=ab["Implosion"]["d"].rstrip(". ")+". Removes Utsusemi."
for a in ("Giga Slash","Kick Back","Umbra Smash"):
    n=ab[a].get("notes","")
    if "Absorbable by Utsusemi" not in n:
        ab[a]["notes"]=(n.rstrip(". ")+". Absorbable by Utsusemi.").lstrip(". ")

# ================= KAM'LANAUT =================
k=m["kam'lanaut"]
k["job"]="Red Mage"
k["nm"]=True
k.pop("det",None)                                  # strip bad [Sight,Sound,True Sight] triple; no detect data in shots
k["ab"]=["Light Blade","Great Wheel"]
k["st"]=[[e,"-40%"] for e in ["Fire","Wind","Lightning","Light","Ice","Earth","Water","Dark"]]  # Return to Delkfutt's Tower * grid (all elems 60%); base all-?
k["wk"]=[]
k["drops"]="Mes'yohi Sword, Mes'yohi Rod, Mes. Haubergeon, Mes'yohi Slacks"
k["zones"]=[["Stellar Fulcrum","75-78"],["Empyreal Paradox","75-78"]]
k["notes"]=[
 "En-spells (Earth/Water/Wind/Fire/Frost/Lightning Blade): casting a nuke of the matching element heals him.",
 "Gravity (Graviga) is difficult to land without Elemental Seal.",
 "Title: Quieter of Ancient Thoughts (VD only).",
]
k["img"]="mobimages/kam'lanaut.png"

# ================= SHADOW LORD =================
s=m["shadow lord"]
s["fam"]="Shadow Lord"
s["job"]="Dark Knight"
s["nm"]=True
s["ab"]=["Giga Slash","Kick Back","Umbra Smash","Dark Nova","Implosion","Damning Edict","Swath of Silence","Bowels of Agony"]  # dropped junk 'Form 1:' / 'Form 2:'
s["st"]=[["Fire","-60%"],["Wind","-60%"],["Lightning","-60%"],["Ice","-60%"],["Earth","-60%"],["Water","-60%"],["Dark","-90%"]]  # Image-3 grid; Light 100% neutral
s["wk"]=[]                                          # page shows Light neutral, no weaknesses (was Light +12.5% / Light Stun)
s["drops"]="Lightreaver, Onimusha-no-Kote, Dread Jupon, Perdition Slops, Trepidity Mantle"
s["zones"]=[["Throne Room","60"]]
s["notes"]=[
 "Boss of Mission 5-2 (all three nations). Two forms, both must be defeated (first ~10,000 HP, second ~4,000 HP).",
 "First form alternates physical/magical immunity (\u2605: swaps every 60s or 20,000 damage). Physically immune while meleeing, magically immune while attacking with its glowing fist. Formless Strikes bypasses physical immunity; \u2605 favors Firaja during physical immunity.",
 "Second form uses only Implosion (~every 10s) and Bowels of Agony; no longer melees or casts. Make sure it is claimed near 1% or spoils are lost.",
 "Title: Shadow Banisher (Mission) / Brilliance Manifest (\u2605, VD only).",
]
s["img"]="mobimages/shadow lord.png"
m["shadow lord (s)"]["nm"]=True                     # WotG [S] Shadow Lord is an NM; same family
fic["Shadow Lord"]="Shadow Lord.jpg"

# ================= ARK ANGEL HM =================
a=m["ark angel hm"]
a["job"]="Warrior / Ninja"
a["nm"]=True
a["ab"]=["Mijin Gakure","Mighty Strikes","Brazen Rush","Cross Reaver","Swift Blade","Chant du Cygne"]
a["drops"]="Deacon Saber, Kerygma Belt, Bloodrain Strap, Lithelimb Cap"   # +Bloodrain Strap
a["zones"]=[["LaLoff Amphitheater","75-124"],["Escha RuAun","75-124"]]
a["notes"]=[
 "Uses Mijin Gakure (once, near 1% HP \u2014 a wipe risk if triggered at high HP), Mighty Strikes (repeatedly, often to open the fight), Brazen Rush, and the unique WS Cross Reaver (cone damage ~500-900 + Stun). Also uses Swift Blade and Chant du Cygne, and casts Ninjutsu (shadows + enfeebles).",
 "Entered at Home Point 1 in Ru'Aun Gardens with a Phantom Gem of Apathy; everyone must hold the key item to enter.",
 "Title: Ark Hume Humiliator (VD only) / Vanquisher of Apathy.",
]

# ---------- IMAGES ----------
def white_trim(src,dst):
    im=Image.open(src).convert("RGB")
    arr=np.asarray(im).astype(int); mx=arr.max(2); mn=arr.min(2)
    nonwhite=((mx-mn)>18)|(mn<235)
    ys,xs=nonwhite.nonzero()
    if len(xs):
        im=im.crop((int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1))
    im.save(dst); return im.size

sz1=white_trim("/mnt/user-data/uploads/669px-Kam_lanaut_1.png", base+"/mobimages/kam'lanaut.png")
sz2=white_trim("/mnt/user-data/uploads/800px-Shadow_Lord_1.png", base+"/mobimages/shadow lord.png")
ic=Image.open(base+"/mobimages/shadow lord.png").convert("RGB")
ic.save(base+"/mobicons/Shadow Lord.jpg","JPEG",quality=88)
print("kam img", sz1, "| shadow img", sz2, "| icon", ic.size)

# ---------- GUARDS ----------
bad=[(mk,fk) for mk,mv in m.items() for fk,vv in mv.items() if vv is None]
assert not bad, bad
undef=sorted({x for v in m.values() for x in (v.get('ab') or []) if x not in ab})
print("undefined ability refs (file-wide):", len(undef))
newmob_undef=[x for mk in ("kam'lanaut","shadow lord","ark angel hm") for x in m[mk]['ab'] if x not in ab]
print("undefined refs on the 3 edited mobs:", newmob_undef)

json.dump(d, open(base+"/mobs.json","w"), separators=(', ', ': '), ensure_ascii=False)
print("mobs",len(m),"abilities",len(ab),"family_eco",len(fe))
print("kam eco->", fe.get(m["kam'lanaut"]['fam']),
      "| shadow eco->", fe.get('Shadow Lord'), "| Humanoid eco->", fe.get('Humanoid'))
