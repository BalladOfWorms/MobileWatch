#!/usr/bin/env python3
"""rev-121 — Shinryu + Perfidien + Plouton + Palloritus + Putraxia + Rancibus.
Six Abyssea/Vagary story NMs. Most pre-exist; this pass completes data + installs renders.
Run from android/_project/ ; edits ../app/src/main/assets/mobs.json in place.
"""
import json, os, sys
import numpy as np
from PIL import Image

ASSETS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'src', 'main', 'assets'))
UP = '/mnt/user-data/uploads'
MOBIMG = os.path.join(ASSETS, 'mobimages')
mp = os.path.join(ASSETS, 'mobs.json')
d = json.load(open(mp))
M, A = d['mobs'], d['abilities']

# ---------- render install ----------
def white_trim(src, dst):
    im = Image.open(src).convert('RGB'); a = np.asarray(im)
    nonwhite = (a.max(2).astype(int) - a.min(2).astype(int) > 18) | (a.min(2) < 235)
    ys, xs = np.where(nonwhite)
    if len(xs) == 0:
        im.save(dst); return im.size
    im2 = im.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1)); im2.save(dst); return im2.size

def as_is(src, dst):
    im = Image.open(src).convert('RGB'); im.save(dst); return im.size

renders = {
    'shinryu':    ('Shinryu.jpg',   as_is),      # dark space bg -> as-is
    'perfidien':  ('perfiden.jpg',  white_trim),
    'plouton':    ('plouton.jpg',   white_trim),
    'palloritus': ('pallatorus.jpg',white_trim),
    'putraxia':   ('putraxia.jpg',  white_trim),
    'rancibus':   ('ranbicus.jpg',  white_trim),
}
print('=== renders ===')
for key,(fn,fnc) in renders.items():
    sz = fnc(os.path.join(UP,fn), os.path.join(MOBIMG,f'{key}.png'))
    print(f'  {key}.png <- {fn} {sz}')

# ---------- helpers ----------
def enrich_ab(name, **kw):
    a = A.setdefault(name, {})
    for k,v in kw.items():
        if v is not None: a[k] = v

# ================= SHINRYU =================
# grid already correct (base box, all resists). Drops good ("Crepuscular Earring" is DB-absent -> not added).
s = M['shinryu']
s['img'] = 'mobimages/shinryu.png'
if 'Comet' not in s['sp']:
    s['sp'] = s['sp'] + ['Comet']         # notes: gains Comet wings-down; Meteor already present

# ================= PERFIDIEN (bare stub -> full build) =================
p = M['perfidien']
p['job'] = None                            # box Job row blank -> leave unset (delete key below)
p.pop('job', None)
p['nm'] = True
p['lv'] = [130, 130]
p['st'] = [[e,'-50%'] for e in ['Fire','Wind','Lightning','Light','Ice','Earth','Water','Dark']]
p['wk'] = []
p['ab'] = ['Eroding Flesh','Flaming Kick','Flashflood','Fulminous Smash','Icy Grasp','Vivisection']
p['zones'] = [["Outer Ra'Kaznar [U]", '130'], ["Ra'Kaznar Inner Court", '130']]
p['drops'] = "Tartarian Chain, Tartarian Soul, Count's Cuffs, Count's Garb, Enervating Earring, Etiolation Earring"
p['img'] = 'mobimages/perfidien.png'
p['notes'] = [
    "Perfidien Paindealer, a Vagary NM (~630,000 HP, Level 130) fought at the Duskbrood Gate ??? in Outer Ra'Kaznar and, via Alternative Vagary, in Ra'Kaznar Inner Court (which grants the Reforged Empyrean Armor +1 legs upgrade). To spawn: defeat elementals with tier IV/V spells matching their weakness (or the 8 hybrid Blue Magic elemental spells) five times, perform a 4-step skillchain, and defeat elementals with magic bursts five times. Warps away if a player is KO'd or if left un-proc'd too long; each defeat extends the time limit by 15 minutes.",
    "From 90% HP it rotates its elemental (and eventually physical) weakness every 10-15%, shown by a cloud animation whose color is the element it currently resists \u2014 its weakness is the two elements ascendant from that color. The susceptible element shifts to 130% while the opposite affinity is absorbed. A !! proc and /emote fire when the weakness is first inflicted, and a !!! proc lands after ~23,000 damage of the weak element; the weakness then changes ~2 minutes later or after enough HP is depleted. Healing Perfidien inflicts Encumbrance (scaled to the heal) and, if overdone, triggers Vivisection and a level-up. Light/Dark skillchains feed the element it is currently absorbing.",
]
# enrich the 6 kit stubs from the Ability Information table
enrich_ab('Eroding Flesh',   t='Magical', el='Earth',    tgt='AoE',      d='AoE damage and Slow.')
enrich_ab('Flaming Kick',    t='Magical', el='Fire',     tgt='Cone AoE', d='Conal damage and Burn.')
enrich_ab('Flashflood',      t='Magical', el='Water',    tgt='AoE',      d='AoE damage that dispels multiple enhancements.')
enrich_ab('Fulminous Smash', t='Magical', el='Lightning',tgt='AoE',      d='AoE damage with Stun and Knockback.')
enrich_ab('Icy Grasp',       t='Magical', el='Ice',      tgt='Cone AoE', d='Conal damage with Paralysis and Terror.')
enrich_ab('Vivisection',     t='Magical', el=None,       tgt='AoE',      d='AoE damage and a full Dispel. Used when it levels up.')

# ================= PLOUTON =================
pl = M['plouton']
if 'Vivisection' not in pl['ab']:
    # insert Vivisection alongside the other <90% moves (before the 50%-tier block)
    pl['ab'] = ['Impudence','Blast of Reticence','Ceaseless Surge','Crippling Agony','Demonfire',
                'Ensepulcher','Frozen Blood','Torrential Pain','Vivisection',
                'Bane of Tartarus','Eternal Misery','Incessant Void','Tenebrous Grip']
pl['zones'] = [["Outer Ra'Kaznar [U]", '132'], ["Ra'Kaznar Inner Court", '132']]  # was 'Outer RaKaznar [U1]'/'RaKaznar Inner Court'
pl['img'] = 'mobimages/plouton.png'        # was 'hades (second form).png' -> own render now

# ================= PALLORITUS =================
pa = M['palloritus']
pa['zones'] = [["Outer Ra'Kaznar [U]", '128'], ["Ra'Kaznar Inner Court", '128']]
pa['img'] = 'mobimages/palloritus.png'
reg = 'Regular attacks are one of four abilities, all Magical/Dark: Orb Toss (AoE damage + Bio, removes shadows), Claw Attack (damage + Stun), Orb Backhand (damage + Blind), and Kick (AoE damage + Knockback).'
if reg not in pa['notes']:
    pa['notes'].append(reg)

# ================= PUTRAXIA (grid FIX + lv + zones + render) =================
pu = M['putraxia']
# FIX: record had Ice-80 / Lightning-15 swapped. Shot (OCR-confirmed) = Ice 85% (-15) / Lightning 20% (-80).
pu['st'] = [['Fire','-50%'],['Wind','-80%'],['Lightning','-80%'],['Light','-30%'],
            ['Ice','-15%'],['Earth','-30%'],['Water','-30%'],['Dark','-95%']]
pu['lv'] = [128,128]
pu['job'] = 'Monk / Black Mage'
pu['zones'] = [["Outer Ra'Kaznar [U]", '128'], ["Ra'Kaznar Inner Court", '128']]
pu['img'] = 'mobimages/putraxia.png'
regp = 'Regular attacks are one of three abilities: Gust (Wind damage, choke -18 HP/tic, knockback; goes through shadows), Lightning (Lightning damage, shock -18 HP/tic, stun; removes all shadows), and Triple Attack (3-hit damage, absorbed by three shadows).'
if regp not in pu['notes']:
    pu['notes'].insert(1, regp)

# ================= RANCIBUS =================
ra = M['rancibus']
ra['zones'] = [["Outer Ra'Kaznar [U]", '128'], ["Ra'Kaznar Inner Court", '128']]
ra['img'] = 'mobimages/rancibus.png'
regr = 'Regular attacks are one of three abilities: Jumping Slam (AoE damage + poison), Tongue Lash (single-target damage + poison), and Spit (conal Water damage + poison).'
if regr not in ra['notes']:
    ra['notes'].insert(1, regr)

# ---------- guards ----------
bad = [k for m in M.values() for k,v in m.items() if v is None]
assert not bad, f'NULL scalar written: {bad[:5]}'
for n,a in A.items():
    assert not isinstance(a.get('el'), list), f'{n} el is list'
    assert isinstance(a.get('ab_el', []), list), f'{n} ab_el not list'
for k,m in M.items():
    assert not isinstance(m.get('ab_el'), str), f'{k} ab_el is bare string'

json.dump(d, open(mp,'w'), separators=(', ', ': '), ensure_ascii=False)
print('\n=== summary ===')
print('mobs', len(M), 'abilities', len(A))
for key in ['shinryu','perfidien','plouton','palloritus','putraxia','rancibus']:
    m=M[key]; print(f'  {key}: fam={m.get("fam")} nm={m.get("nm")} lv={m.get("lv")} img={m.get("img")} zones={m.get("zones")}')
