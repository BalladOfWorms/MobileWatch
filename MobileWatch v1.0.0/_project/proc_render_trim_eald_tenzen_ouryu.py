#!/usr/bin/env python3
# proc_render_trim_eald_tenzen_ouryu.py — composite-onto-white (renders have alpha) then white-trim
# Eald'narche / Tenzen / Ouryu renders into mobimages/. Author: BalladOfWorms
from PIL import Image
import numpy as np
jobs = [
  ("uploads/588px-Eald_narche_1.png", "mobimages/eald'narche.png"),
  ("uploads/800px-Tenzen_1.png",      "mobimages/tenzen.png"),
  ("uploads/Wyrm__Ouryu_.png",        "mobimages/ouryu.png"),
]
for src, dst in jobs:
    im = Image.open(src)
    if 'A' in im.mode:
        bg = Image.new('RGBA', im.size, (255,255,255,255))
        im = Image.alpha_composite(bg, im.convert('RGBA')).convert('RGB')
    else:
        im = im.convert('RGB')
    a = np.asarray(im)
    nonwhite = (a.max(2).astype(int) - a.min(2).astype(int) > 18) | (a.min(2) < 235)
    ys, xs = np.where(nonwhite); pad = 6
    im.crop((max(0,xs.min()-pad), max(0,ys.min()-pad),
             min(a.shape[1], xs.max()+1+pad), min(a.shape[0], ys.max()+1+pad))).save(dst)
