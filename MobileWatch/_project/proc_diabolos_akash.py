import json
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']
items={v.get('n') for v in json.load(open('ffxi_items.json')).values() if isinstance(v,dict) and v.get('n')}

# ---------- Titan Prime image (data done last pass) ----------
m['titan prime']['img']="mobimages/titan prime.png"

# ---------- CREATE 12 Diabolos blood-pact defs ----------
ab['Cacodemonia']={"d":"An area-of-effect attack that deals dark damage and inflicts Curse.","t":"Magical","el":"Dark","tgt":"AoE","fx":["Curse"]}
ab['Nightmare']={"d":"Puts targets in an area into a deep (hyper) sleep.","t":"Magical","el":"Dark","tgt":"AoE","fx":["Sleep"]}
ab['Hypnogenesis']={"d":"Deals dark damage (a large single-target hit, or an AoE Throat Stab depending on the caster).","el":"Dark"}
ab['Daydream']={"d":"Charms a single target.","tgt":"Single","fx":["Charm"],"notes":"Used incrementally after Nightmare (once after the first, twice after the second, and so on)."}
ab['Ultimate Terror']={"d":"Drains 2-4 of the target's stats by 22 and steals one beneficial effect from targets in range.","tgt":"AoE"}
ab['Noctoshield']={"d":"Grants Diabolos a Phalanx effect.","tgt":"Self","fx":["Phalanx"]}
ab['Dream Shroud']={"d":"Grants Diabolos a Magic Attack and Magic Defense boost.","tgt":"Self"}
ab['Nether Blast']={"d":"Heavy single-target dark damage (1100+).","t":"Magical","el":"Dark","tgt":"Single"}
ab['Camisado']={"d":"Dark damage; the AoE version deals 500-700 with a 10' knockback.","el":"Dark"}
ab['Somnolence']={"d":"Low-to-moderate damage that inflicts Gravity.","tgt":"Single","fx":["Gravity"]}
ab['Sweeping Somnolence']={"d":"Area-of-effect damage.","tgt":"AoE"}
ab['Nether Tempest']={"d":"Area-of-effect damage.","tgt":"AoE"}

# ---------- Diabolos aspects: per-aspect kit / sp / zone / drops / notes ----------
DYN="Dynamis-Tavnazia"
def gear(*names): return ", ".join(n for n in names if n in items)
ASP={
 'diabolos club':   dict(ab=["Ruinous Omen","Cacodemonia","Nightmare"], sp=["Blindga"], lv="85",
   note="Dynamis-Tavnazia. Traded via Herald's Juju at (I-5); the version that spawns is random among Diabolos Heart/Spade/Club/Diamond. Casts AoE enfeebles (Blindga). Uses Ruinous Omen (AoE darkness), Cacodemonia (AoE Curse), and Nightmare (hyper-sleep). Title: Nightmare Awakener.",
   drops="Fiendish Tome (14), 100 Byne Bill"),
 'diabolos diamond':dict(ab=["Ruinous Omen","Cacodemonia","Hypnogenesis","Daydream"], sp=["Blindga"], lv="85",
   note="Dynamis-Tavnazia (Herald's Juju random spawn). Casts AoE enfeebles + dark magic. Uses Ruinous Omen, Cacodemonia, and Hypnogenesis (large single-target); Daydream single-target charm incrementally after Nightmare. Title: Nightmare Awakener.",
   drops="Fiendish Tome (14), 100 Byne Bill"),
 'diabolos heart':  dict(ab=["Ultimate Terror","Noctoshield","Dream Shroud"], sp=["Sleepga II","Death"], lv="85",
   note="Dynamis-Tavnazia (Herald's Juju random spawn). Casts Sleepga II and Death. Uses Ultimate Terror (stat drain), Noctoshield (Phalanx), and Dream Shroud (MAB/MDB boost). Title: Nightmare Awakener.",
   drops="Fiendish Tome (14), 100 Byne Bill"),
 'diabolos spade':  dict(ab=["Ruinous Omen","Noctoshield"], sp=[], lv="85",
   note="Dynamis-Tavnazia (Herald's Juju random spawn). Uses Ruinous Omen (AoE darkness) and Noctoshield (Phalanx). Title: Nightmare Awakener.",
   drops="Fiendish Tome (14), 100 Byne Bill"),
 'diabolos letum':  dict(ab=["Cacodemonia","Nightmare","Daydream","Hypnogenesis"], sp=["Blindga","Death","Drainga"], lv="100",
   note="Dynamis-Tavnazia (traded via Fnd. Tome II 14-17 at I-5, first floor; random among Nox/Umbra/Somnus/Letum). Does NOT melee but can draw-in. Opens with Cacodemonia (AoE -50% HP/MP curse). Casts Blindga/Death/Drainga (800+ per target). A successful spell cast triggers Nightmare, then Daydream (charm) \u2014 un-equip weapons for that. Hypnogenesis is an AoE Throat Stab. Spells/TP can be stunned but high resist from DRK99 (subbed stuns resisted); weaponskill interrupts are reliable. Title: Nightmare Illuminator.",
   drops="Portus Collar, Portus Ring, Portus Annulet, Alucinor Mitts, 100 Byne Bill"),
 'diabolos nox':    dict(ab=["Ultimate Terror","Dream Shroud"], sp=["Kaustra","Death"], lv="100",
   note="Dynamis-Tavnazia (Fnd. Tome II random spawn). Casts Kaustra (AoE, sometimes repeatedly) and Death. Spams Ultimate Terror and Dream Shroud (need Magic Finale to strip). Title: Nightmare Illuminator.",
   drops="Portus Collar, Portus Ring, Portus Annulet, Alucinor Mitts, 100 Byne Bill"),
 'diabolos somnus': dict(ab=["Noctoshield","Sweeping Somnolence","Nether Tempest","Ruinous Omen"], sp=[], lv="100",
   note="Dynamis-Tavnazia (Fnd. Tome II random spawn). Uses Noctoshield on spawn; Sweeping Somnolence and Nether Tempest are AoEs; Ruinous Omen around 50% HP. Fairly resistant to damage (sometimes becoming immune \u2014 possibly tied to TP usage). Title: Nightmare Illuminator.",
   drops="Portus Collar, Portus Ring, Portus Annulet, Alucinor Mitts, 100 Byne Bill"),
 'diabolos umbra':  dict(ab=["Cacodemonia","Ruinous Omen","Nightmare","Nether Blast","Ultimate Terror","Somnolence","Camisado"], sp=["Blindga","Dispelga","Kaustra"], lv="100",
   note="Dynamis-Tavnazia (Fnd. Tome II random spawn). Very high defense (likely -PDT; ~half damage from magic). Casts Blindga/Dispelga/Kaustra (~650 dmg). Opens with Cacodemonia; Ruinous Omen at 80% summons a Diabolos' Vestige (untargetable, one TP move then gone); Nightmare (~40-50%) summons a 2nd Vestige. Nether Blast hits 1100+ (deadly if a Vestige uses it on the same target). Ultimate Terror lowers 2-4 stats by 22 + steals a buff; Somnolence adds Gravity; AoE Camisado 500-700 + 10' knockback. Title: Nightmare Illuminator.",
   drops="Portus Collar, Portus Ring, Portus Annulet, Alucinor Mitts, 100 Byne Bill"),
 "diabolos's shard":dict(ab=["Camisado"], sp=[], lv="85", nm=False,
   note="Assists Diabolos Club in Dynamis-Tavnazia; uses Camisado (single-target). No longer spawned since the 2011 Dynamis changes.",
   drops=""),
}
for k,cfg in ASP.items():
    v=m[k]
    v['ab']=cfg['ab']
    if cfg['sp']: v['sp']=cfg['sp']
    v['zones']=[[DYN,cfg['lv']]]
    if cfg['drops']: v['drops']=cfg['drops']
    else:
        v.pop('drops',None)
    v['notes']=[cfg['note']]
    # crys Dark / jobs kept from import; nm kept (shard stays None)

# ---------- AKASH (Abyssea-La Theine NM) ----------
a=m['akash']
a['zones']=[["Abyssea-La Theine","85"]]
a['drops']="Forbidden Key"
a['img']="mobimages/akash.png"
a['notes']=[
 "Wanders Abyssea-La Theine (~lv85, 5 spawns); its spawn rate seems tied to how many monsters players are killing. Gives 16/32/64/128 Amber Light when killed with a magical weapon skill. Drops the Forbidden Key.",
]

for v in m.values():
    for k in [k for k,val in list(v.items()) if val is None]:
        del v[k]
json.dump(d,open('mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print("written; abilities",len(ab))
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']
bad=[(k,kk) for k,v in m.items() for kk,vv in v.items() if vv is None]; print("None:",len(bad))
allk=list(ASP)+['akash']
und=[a for k in allk for a in (m[k].get('ab') or []) if a not in ab]; print("undefined refs:",und)
print("titan prime img:",m['titan prime'].get('img'))
for k in ['diabolos umbra',"diabolos's shard",'akash']:
    v=m[k]; print(f"  {k}: ab={v.get('ab')} zones={v.get('zones')} drops={v.get('drops')!r} img={v.get('img')!r}")
