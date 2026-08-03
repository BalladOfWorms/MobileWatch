import json
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']

# fix fulmotondro crystal (Thunder -> Lightning per convention)
m['fulmotondro']['crys']='Lightning'
# create Pull In (Maere)
ab['Pull In']={"d":"Draws in the target from a very large range.","tgt":"Single"}

IMG={'gamayun','chione','brulo','maere','ogopogo','pavan','teles'}  # have renders; framed-card ones skipped

# ---------- Abyssea elemental NMs ----------
CFG={
 'gamayun':dict(zone="Abyssea-Grauberg",lv="85",drops="Celeritas Pole, Ravager's Earring",
   note="Roams a circular pattern north of Conflux #8 in Abyssea-Grauberg (~J-5, seen as low as J-11); 10-15 min respawn. Drops the Indigo abyssite line + a Battle trophy (4th echelon)."),
 'fulmotondro':dict(zone="Abyssea-Vunkerl",lv="85-87",drops="",
   note="Multiple instances roam Abyssea-Vunkerl (timed respawn, 5 spawns)."),
 'chione':dict(zone="Abyssea-Uleguerand",lv="85",drops="Creed Earring, Charis Earring",
   ab=["Rush","Heavenly Strike"],sp=["Blizzaga II","Blizzaga III","Freeze","Blizzard IV","Blizzard V"],
   note="Spawned by resting near a Colorful demilune abyssite in Abyssea-Uleguerand (G-8/H-8 among Mechanical Menace, or F-8/F-9 among Sub-zero Gear). Uses Rush and Heavenly Strike; casts Blizzaga II/III, Freeze, Blizzard IV/V (tier rises as HP drops); gains Ice Spikes while casting; counters with Rush if damaged mid-cast."),
 'bhumi':dict(zone="Abyssea-Tahrongi",lv="85",drops="",
   note="Wanders Abyssea-Tahrongi near Confluxes 01, 02, and 07 (5 spawns). Drops the Viridian abyssite of merit."),
 'brulo':dict(zone="Abyssea-Altepa",lv="85",drops="Maleficus, Flame Sachet, Clearview Earring",
   note="Respawns every 15-20 min; wanders Abyssea-Altepa between (E/F-10/11) and (G-11) near Conflux #5 among Sand Murex/Barrens Treant. Drops Colorless Soul + Atma of the Burning Effigy. Title: Brulo Extinguisher."),
 'jala':dict(zone="Abyssea-Misareaux",lv="85",drops="",
   note="Multiple copies roam Abyssea-Misareaux (20 min respawn, 5 spawns)."),
 'maere':dict(zone="Abyssea-Grauberg",lv="85",drops="Acinaces, Gifted Earring, Shadow Belt",
   ab=["Nightmare","Pull In","Nether Blast"],sp=["Aspir","Drain","Absorb-TP","Stun","Bio"],
   note="Respawns every 15-20 min; wanders Abyssea-Grauberg between (J-5) and (L-5) north of Conflux #8. Nightmare (AoE) has a 100% chance to Sleep + Bio for 60s (cannot be cured off; can repeat) and can Stun ~15s; uses AoE enfeebles (Aspir/Stun/Absorb-TP/Drain \u2014 Drain wakes you from Nightmare); Pull In has a very large range (used before Nightmare); Nether Blast hits ~900 with capped DT; En-drain melee. Drops Colorless Soul + Atma of the Endless Nightmare. Title: Maere Bestirrer."),
 'ogopogo':dict(zone="Abyssea-Uleguerand",lv="85",drops="Burattinaios, Aqua Belt, Siegel Sash",
   ab=["Tidal Wave"],
   note="Respawns every 15-20 min at the top of the mountain (F-9/H-8) in Abyssea-Uleguerand near Conflux #7. Remains at 1% HP until it uses Tidal Wave (~4000 damage before reduction). Drops Colorless Soul + Atma of the Lake Lurker. Title: Ogopogo Overturner."),
 'pavan':dict(zone="Abyssea-Konschtat",lv="85",drops="",
   note="20 min respawn, 5 spawns; wanders Abyssea-Konschtat near Confluxes #6 and #7. Drops the Azure abyssite of lenity."),
 'tejas':dict(zone="Abyssea-Attohwa",lv="85",drops="",
   note="Multiple copies roam Abyssea-Attohwa (20 min respawn, 5 spawns)."),
}
for k,c in CFG.items():
    v=m[k]
    v['zones']=[[c['zone'],c['lv']]]
    if c.get('ab'): v['ab']=c['ab']
    if c.get('sp'): v['sp']=c['sp']
    if c['drops']: v['drops']=c['drops']
    v['notes']=[c['note']]
    if k in IMG: v['img']=f"mobimages/{k}.png"

# ---------- TELES (fam=Siren, Geas Fete NM, Reisenjima lv150) ----------
t=m['teles']; t['job']='Bard / Black Mage, Paladin'; t['lv']=[150,150]
t['ab_el']=["Wind"]
t['st']=[["Breath","-25%"],["Slashing","-12.5%"],["Impact","-6.3%"],["Fire","-70%"],["Lightning","-70%"],["Water","-70%"],["Light","-95%"],["Earth","-95%"],["Ice","-50%"],["Dark","-50%"]]
t.pop('wk',None)
t['ab']=["Hysteric Assault","Lunatic Voice","Sonic Buffet","Entice","Clarsach Call"]
t['sp']=["Cure VI","Banish IV","Shell V","Protect V","Magic Finale","Wind Threnody II","Pining Nocturne","Massacre Elegy","Maiden's Virelai","Aero VI","Aeroja","Aeroga V","Impact","Death"]
t['zones']=[["Reisenjima","150"]]
t['img']="mobimages/teles.png"
t['drops']="Composer's Mitts, Composer's Sabots, Misanthropy, Sangoma"
t['notes']=[
 "Geas Fete NM (Reisenjima, lv150; Forced pop by examining ??? with Teles's hymn, all members need Tribulens/Radialens). Title: Teles Terrifier.",
 "Uses one of three SP abilities \u2014 Invincible, Soul Voice, or Manafont \u2014 at 79/59/39/29/19/9% HP (constantly at 9%), each with a ~25-30 yalm aura and a behavior/spell change: Invincible (~300/tick Dia aura; casts Protect V/Shell V/Banish IV/Cure VI), Soul Voice (Mute aura; casts Wind Threnody II/Magic Finale/Pining Nocturne/Massacre Elegy/Maiden's Virelai + gains Entice single-target Charm), Manafont (Magic Defense Down aura; casts Aero VI/Aeroja/Aeroga V/Impact/Death).",
 "Inflicting Ice or Darkness damage / status ailments right as an SP opening animation goes off can PROC Teles (weaponskills force an SP swap, pet abilities terminate the SP). Resets enmity on its current target when heavy ranged damage is dealt \u2014 favors Clarsach Call (high AoE wind damage + many offensive/defensive buffs on itself; dispel them; Distract III blocks its evasion boost) on the hate reset.",
]

for v in m.values():
    for k in [k for k,val in list(v.items()) if val is None]:
        del v[k]
json.dump(d,open('mobs.json','w'),separators=(', ', ': '),ensure_ascii=False)
print("written; abilities",len(ab))
d=json.load(open('mobs.json')); m=d['mobs']; ab=d['abilities']
bad=[(k,kk) for k,v in m.items() for kk,vv in v.items() if vv is None]; print("None:",len(bad))
allk=list(CFG)+['teles']
und=[a for k in allk for a in (m[k].get('ab') or []) if a not in ab]; print("undefined refs:",und)
for k in ['chione','maere','ogopogo','teles','gamayun']:
    v=m[k]; print(f"  {k}: zones={v.get('zones')} ab={v.get('ab')} img={v.get('img')!r} drops={(v.get('drops') or '')[:40]!r}")
