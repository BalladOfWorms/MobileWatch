#!/usr/bin/env python3
"""Archaic Machines ecosystem intake (rev 102): Chariot / Gear / Rampart.
Source = BG-wiki category screenshots. family_eco was MISSING for all three;
resist grids were legacy placeholders; Gear/Rampart had no kits."""
import json
P='app/src/main/assets/mobs.json'
d=json.load(open(P))
M=d['mobs']; A=d['abilities']; FE=d['family_eco']; FN=d['family_notes']

def g(v): return f"{v:+g}%"
def grid(dmg=None, elem=None):
    st=[]; wk=[]
    for src in (dmg or {}, elem or {}):
        for t,pct in src.items():
            delta=pct-100
            if delta<0: st.append([t,g(delta)])
            elif delta>0: wk.append([t,g(delta)])
    return st,wk

CH_ELEM_BASE={"Fire":70,"Wind":60,"Lightning":25,"Light":40,"Ice":60,"Earth":60,"Water":100,"Dark":60}
ALL7={"Magical":87.5,"Breath":87.5,"Slashing":87.5,"Impact":87.5,"H2H":87.5,"Piercing":87.5,"Ranged":87.5}
archaic  = grid({"Physical":100,**ALL7}, CH_ELEM_BASE)
battleclad=grid({"Magical":70}, CH_ELEM_BASE)
armored  = grid({"Physical":100,**ALL7}, {**CH_ELEM_BASE,"Ice":70})
longbowed= grid({"Magical":87.5}, CH_ELEM_BASE)
longarmed= grid({"Magical":65.5}, CH_ELEM_BASE)
CH_BASE=archaic
CH_OVERRIDE={"archaic chariot":archaic,"battleclad chariot":battleclad,"armored chariot":armored,
             "long-bowed chariot":longbowed,"long-armed chariot":longarmed}

gear = grid({"Piercing":125,"Ranged":125},
            {"Fire":100,"Wind":85,"Lightning":50,"Light":50,"Ice":85,"Earth":85,"Water":115,"Dark":85})
rampart = grid({"Magical":65,"Breath":65,"Slashing":65,"Impact":65,"H2H":65,"Piercing":65,"Ranged":65},
               {"Fire":150,"Wind":50,"Lightning":60,"Light":85,"Ice":85,"Earth":85,"Water":85,"Dark":85})

FAM={
 "Chariot":{"det":["Sound"],"job":"Warrior","crys":"Light",
   "ab":["Diffusion Ray","Inertia Stream","Discharge","Brainjack","Discoid","Homing Missle","Mortal Revolution"]},
 "Gear":{"det":["Sight","Sound","Scent","Magic"],"job":"Ranger","crys":"Light",
   "ab":["Artificial Gravity","Antigravity","Restoral","Rail Cannon"]},
 "Rampart":{"det":["Sound","Magic"],"job":"Beastmaster","crys":"Lightning",
   "ab":["Astral Gate","Reinforcements","Choke Chain","Roller Chain","Biomagnet"]},
}
for f in FAM: FE[f]="Archaic Machines"
FN["Rampart"]=["Links with other Archaic Machines."]

JOBEXP={"RNG":"Ranger","WAR":"Warrior","BLM":"Black Mage","SAM":"Samurai","PLD":"Paladin","BST":"Beastmaster"}

Z={
 "archaic chariot":["Bhaflau Remnants","Arrapago Remnants"],
 "armored chariot":["Arrapago Remnants"],"battleclad chariot":["Zhayolm Remnants"],
 "battledressed chariot":["Nyzul Isle"],"long-armed chariot":["Silver Sea Remnants"],
 "long-bowed chariot":["Bhaflau Remnants"],"long-gunned chariot":["Nyzul Isle"],
 "long-horned chariot":["Nyzul Isle"],"racing chariot":["Nyzul Isle"],"shielded chariot":["Nyzul Isle"],
 "imperial gear":["Nyzul Isle"],"imperial gears":["Nyzul Isle"],
 "archaic gear":["Bhaflau Remnants"],"archaic gears":["Bhaflau Remnants"],
 "gyroscopic gear":["Silver Sea Remnants"],"gyroscopic gears":["Silver Sea Remnants"],
 "archaic rampart":["Arrapago Remnants","Silver Sea Remnants","Zhayolm Remnants","Nyzul Isle"],
 "dormant rampart":["Bhaflau Remnants"],"first rampart":["Zhayolm Remnants"],
 "second rampart":["Zhayolm Remnants"],"third rampart":["Zhayolm Remnants"],
 "fourth rampart":["Zhayolm Remnants"],"reactionary rampart":["Bhaflau Remnants"],
}

NEWAB={
 "Homing Missle":{"d":"Deals damage equal to roughly 90% of the target's current HP and removes enmity.",
   "tgt":"AoE","r":"Targeted AoE","notes":"Only used by certain Notorious Monsters. Target must be in front."},
 "Artificial Gravity":{"d":"Deals physical damage and inflicts Weight.","tgt":"AoE","fx":["Weight"]},
 "Antigravity":{"d":"Deals physical damage and knocks back.","tgt":"AoE","fx":["Knockback"]},
 "Restoral":{"d":"Restores HP.","tgt":"Self"},
 "Rail Cannon":{"d":"Deals damage; the area scales with the number of linked Gears (3 Gears = AoE, 2 Gears = frontal cone, 1 Gear = single target).",
   "tgt":"AoE","notes":"Area depends on the number of linked Gears."},
 "Astral Gate":{"d":"Deals physical damage and knocks back.","tgt":"Single","fx":["Knockback"]},
 "Reinforcements":{"d":"Summons a monster.","tgt":"Self"},
 "Choke Chain":{"d":"Inflicts Bind, Silence, and Amnesia.","tgt":"Single","fx":["Bind","Silence","Amnesia"],
   "notes":"Used only when the door is closed."},
 "Roller Chain":{"d":"Deals physical damage and inflicts Bind.","tgt":"AoE","fx":["Bind"],
   "notes":"Used only when the door is closed."},
 "Biomagnet":{"d":"Draws in the target.","tgt":"Single"},
}
for k,v in NEWAB.items(): A[k]=v
if "Diffusion Ray" in A:
    A["Diffusion Ray"].setdefault("d","Deals damage and dispels a beneficial effect.")
    A["Diffusion Ray"]["fx"]=["Dispel"]

changed=0
for key,m in M.items():
    fam=m.get('fam')
    if fam not in FAM: continue
    spec=FAM[fam]
    if fam=="Chariot": st,wk=CH_OVERRIDE.get(key,CH_BASE)
    elif fam=="Gear":  st,wk=gear
    else:              st,wk=rampart
    m['st']=[list(x) for x in st]; m['wk']=[list(x) for x in wk]
    m['det']=list(spec['det']); m['ab']=list(spec['ab'])
    j=m.get('job')
    if not j: m['job']=spec['job']
    elif j in JOBEXP: m['job']=JOBEXP[j]
    if not m.get('crys'): m['crys']=spec['crys']
    if key in Z:
        lv=m.get('lv'); rng=f"{lv[0]}-{lv[1]}" if (isinstance(lv,list) and len(lv)==2) else None
        m['zones']=[[z,rng] if rng else [z] for z in Z[key]]
    changed+=1

bad=[(k,kk) for k,m in M.items() for kk,vv in m.items() if vv is None]
assert not bad, f"None written: {bad[:5]}"
json.dump(d, open(P,'w'), separators=(', ', ': '), ensure_ascii=False)
print("stamped",changed,"members")
print("family_eco Archaic Machines:",[f for f in FAM if FE[f]=='Archaic Machines'])
print("abilities:",len(A),"family_eco:",len(FE),"family_notes:",len(FN))
