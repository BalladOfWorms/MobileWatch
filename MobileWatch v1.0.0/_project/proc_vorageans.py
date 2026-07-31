#!/usr/bin/env python3
"""Vorageans ecosystem intake (rev 101): Murex, Limule, Clionid, Amoeban.
Author: BalladOfWorms. Base grids + weather-shifting Ephemeral members, kits,
zones, dets, jobs, NM flags; folds the 4 Kammavaca's <family> Odyssey orphans;
reassigns mis-filed eschan amoeban. USER: Amoeban has NO NM (on-page NM chart wrong)."""
import json, copy, sys

P='app/src/main/assets/mobs.json'
d=json.load(open(P))
m=d['mobs']; AB=d['abilities']
FE=d['family_eco']; FN=d['family_notes']

def norm(s):  # abbrev job expansion
    mp={'BLM':'Black Mage','WHM':'White Mage','RDM':'Red Mage','WAR':'Warrior','BLU':'Blue Mage'}
    parts=[mp.get(p.strip(),p.strip()) for p in s.split(',')]
    return ', '.join(parts)

# ---- family_eco ----
for fam in ('Murex','Limule','Clionid','Amoeban'):
    FE[fam]='Vorageans'

# ---- base grids (delta = wiki% - 100; st = resist neg, wk = weak pos) ----
GRID={
 'Murex':   dict(wk=[], st=[["Fire","-30%"],["Wind","-50%"],["Lightning","-50%"],["Light","-30%"],["Water","-30%"],["Dark","-30%"]]),
 'Limule':  dict(wk=[], st=[["Fire","-50%"],["Wind","-30%"],["Lightning","-30%"],["Light","-50%"],["Ice","-30%"]]),
 'Clionid': dict(wk=[], st=[["Magical","-25%"],["Wind","-30%"],["Lightning","-30%"],["Light","-50%"],["Ice","-30%"],["Earth","-50%"],["Water","-50%"],["Dark","-30%"]]),
 'Amoeban': dict(wk=[["Magical","+12.5%"]], st=[["Fire","-30%"],["Lightning","-30%"],["Ice","-30%"],["Earth","-50%"],["Water","-30%"],["Dark","-50%"]]),
}
# ephemeral Clionid: Magical flips from resist(-25) to weak(+25); elements unchanged
EPH_CLIONID=dict(wk=[["Magical","+25%"]], st=[["Wind","-30%"],["Lightning","-30%"],["Light","-50%"],["Ice","-30%"],["Earth","-50%"],["Water","-50%"],["Dark","-30%"]])

DET={'Murex':['Scent'],'Limule':['Sound','Blood'],'Clionid':['Blood'],'Amoeban':['Magic']}
KIT={'Murex':['Benthic Typhoon','Pelagic Tempest'],'Limule':['Blazing Bound','Molting Burst'],
     'Clionid':['Acrid Stream'],'Amoeban':['Osmosis','Nucleic Implosion']}

EPH_NOTE={
 'ephemeral murex':"Shifts resistances with the day's weather: absorbs Lightning in Thunder weather, Wind in Wind weather.",
 'ephemeral limule':"Shifts resistances with the day's weather: absorbs Fire in Fire weather, Light in Light weather.",
 'ephemeral clionid':"Shifts resistances with the day's weather: absorbs Ice in Ice weather, Water in Water weather; weak to magic (unlike standard Clionids).",
 'ephemeral amoeban':"Shifts resistances with the day's weather: absorbs Earth in Earth weather, Dark in Dark weather.",
}

# ---- abilities: FIX Blazing Bound (page contradicts existing def) ----
AB['Blazing Bound']={"d":"Deals fire damage and inflicts Burn (-53 INT).","el":"Fire","tgt":"AoE","fx":["Burn"],"r":"21.4~"}
# Molting Burst kept as-is (richer + consistent with page)
# CREATE 5 new (Type column "?" -> t/el unset except stated element)
NEW={
 'Benthic Typhoon':{"d":"Deals damage; additional effect lowers Defense and Magic Defense.","tgt":"Single","fx":["Defense Down","Magic Def. Down"]},
 'Pelagic Tempest':{"d":"Deals damage with an additional Terror effect.","fx":["Terror"]},
 'Acrid Stream':{"d":"Deals water damage and lowers the target's Magic Defense by 25.","el":"Water","tgt":"Conal","fx":["Magic Def. Down"]},
 'Osmosis':{"d":"Absorbs the target's HP and one beneficial effect.","tgt":"Conal","fx":["HP Drain","Dispel"]},
 'Nucleic Implosion':{"d":"Absorbs HP, fully dispels the target, and resets its job ability recast timers.","tgt":"AoE","fx":["HP Drain","Dispel"],"notes":"Used only by earth-based Amoeban."},
}
for k,v in NEW.items(): AB[k]=v
# Vacuole Discharge deliberately NOT created (no published description) -> family note only

# ---- fam reassignments / folds ----
m['eschan amoeban']['fam']='Amoeban'
for orphan,fam in [("kammavaca's murex",'Murex'),("kammavaca's limule",'Limule'),
                   ("kammavaca's clionid",'Clionid'),("kammavaca's amoeban",'Amoeban')]:
    m[orphan]['fam']=fam

# ---- zones (from Adversaries + trade-pop Listings) ----
Z={
 'ephemeral murex':('Abyssea-Attohwa',80,95),'escarp murex':('Abyssea-Misareaux',80,95),
 'river murex':('Abyssea-Vunkerl',80,95),'rock murex':('Abyssea-Attohwa',80,95),
 'hillock murex':('Abyssea-Grauberg',85,100),'iceberg murex':('Abyssea-Uleguerand',85,100),
 'sand murex':('Abyssea-Altepa',85,100),'eschan murex':('Escha RuAun',115,119),
 'gulch limule':('Abyssea-Tahrongi',75,90),'sods limule':('Abyssea-Konschtat',75,90),
 'gigadaphnia':('Abyssea-La Theine',75,90),'arid limule':('Abyssea-Altepa',85,99),
 'stream limule':('Abyssea-Grauberg',85,99),'crag limule':('Abyssea-Uleguerand',85,99),
 'eschan limule':('Escha RuAun',115,119),
 'eschan clionid':('Escha RuAun',115,119),
 'eschan amoeban':('Escha RuAun',115,119),
}
# Amoeban Abyssea adversaries (no lv column -> keep mob's existing lv for the pair)
AMO_Z={'crevice amoeban':'Abyssea-Attohwa','ephemeral amoeban':'Abyssea-Attohwa',
 'protoamoeban':'Abyssea-Misareaux','stream amoeban':'Abyssea-Vunkerl','floe amoeban':'Abyssea-Uleguerand',
 'pond amoeban':'Abyssea-Grauberg','oasis amoeban':'Abyssea-Altepa'}
TRADE={'vetehinen':'Abyssea-Tahrongi','halimede':'Abyssea-Tahrongi'}

NM_FLAG={'gigadaphnia'}  # named Abyssea NM in the adversaries table (open flag)

def stamp(fam):
    members=[k for k,v in m.items() if v.get('fam')==fam]
    for k in members:
        v=m[k]
        # eco already via family_eco; det uniform
        v['det']=list(DET[fam])
        # grid
        if k in EPH_NOTE:
            g = EPH_CLIONID if k=='ephemeral clionid' else GRID[fam]
        else:
            g = GRID[fam]
        v['wk']=copy.deepcopy(g['wk']); v['st']=copy.deepcopy(g['st'])
        # kit (additive family kit)
        cur=v.get('ab') or []
        for a in KIT[fam]:
            if a not in cur: cur.append(a)
        v['ab']=cur
        # jobs: expand abbrev; fill blanks on non-NM with Black Mage; keep NM job/None
        job=v.get('job')
        if job: v['job']=norm(job)
        elif not v.get('nm') and k not in NM_FLAG:
            v['job']='Black Mage'
        # nm flag
        if k in NM_FLAG: v['nm']=True
        # zones + lv align
        if k in Z:
            zn,lo,hi=Z[k]; v['zones']=[[zn,f"{lo}-{hi}"]]; v['lv']=[lo,hi]
        elif k in AMO_Z:
            lo,hi=v.get('lv',[None,None])[:2]
            rng=f"{lo}-{hi}" if lo is not None else None
            v['zones']=[[AMO_Z[k],rng]] if rng else [[AMO_Z[k]]]
        elif k in TRADE:
            lo,hi=v.get('lv',[None,None])[:2]
            v['zones']=[[TRADE[k],f"{lo}-{hi}" if lo is not None else None]]
        # ephemeral weather note
        if k in EPH_NOTE:
            notes=v.get('notes') or []
            if EPH_NOTE[k] not in notes: notes.append(EPH_NOTE[k])
            v['notes']=notes
    return members

counts={}
for fam in ('Murex','Limule','Clionid','Amoeban'):
    counts[fam]=len(stamp(fam))

# ---- family_notes ----
MOON="Passive by day, aggressive at night; the night aggression window widens with the moon phase (as narrow as 23:00-0:00 at the new moon, as wide as 18:00-5:00 at the full moon)."
FN['Murex']=[MOON,"Despoil yields Murex Spicule (Attack Down)."]
FN['Limule']=[MOON,"Despoil yields Limule Pincer (Accuracy Down)."]
FN['Clionid']=[MOON,"Despoil yields Clionid Wing (Evasion Down)."]
FN['Amoeban']=[MOON,"Despoil yields Amoeban Pseudopod (Evasion Down).",
 "Also uses Vacuole Discharge (no published description). Nucleic Implosion is used only by earth-based Amoeban."]

# ---- None-poison guard ----
bad=[k for mm in m.values() for k,v in mm.items() if v is None]
assert not bad, f"None-valued keys leaked: {bad}"

json.dump(d,open(P,'w'),separators=(', ',': '),ensure_ascii=False)
print("family counts:",counts)
print("abilities:",len(AB),"family_eco:",len(FE),"family_notes:",len(FN),"family_resist_sets:",len(d.get('family_resist_sets',{})))
