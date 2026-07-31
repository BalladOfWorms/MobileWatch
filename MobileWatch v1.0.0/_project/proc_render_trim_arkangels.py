# proc_render_trim_arkangels.py — white-trim Ark Angel/Kam/Shadow renders. Author: BalladOfWorms
from PIL import Image
import os
ASSET='.'
def bbox_nonwhite(im):
    im=im.convert('RGB')
    px=im.load(); W,H=im.size
    minx,miny,maxx,maxy=W,H,-1,-1
    for y in range(H):
        for x in range(W):
            r,g,b=px[x,y]
            mx=max(r,g,b); mn=min(r,g,b)
            if (mx-mn>18) or (mn<235):
                if x<minx:minx=x
                if y<miny:miny=y
                if x>maxx:maxx=x
                if y>maxy:maxy=y
    if maxx<0: return None
    return (minx,miny,maxx+1,maxy+1)
def trim(src,dst,pad=6):
    im=Image.open('/mnt/user-data/uploads/'+src).convert('RGB')
    bb=bbox_nonwhite(im)
    if bb is None: raise SystemExit('all white '+src)
    l,t,r,b=bb
    l=max(0,l-pad); t=max(0,t-pad); r=min(im.size[0],r+pad); b=min(im.size[1],b+pad)
    out=im.crop((l,t,r,b))
    out.save(dst,'PNG')
    return out.size
jobs=[
 ('669px-Kam_lanaut_1.png',"mobimages/kam'lanaut.png"),
 ('800px-Shadow_Lord_1.png','mobimages/shadow lord.png'),
 ('800px-Ark_Angel_Hume_1.png','mobimages/ark angel hm.png'),
 ('800px-Ark_Angel_Tarutaru_1.png','mobimages/ark angel tt.png'),
 ('800px-Ark_Angel_Mithra_1.png','mobimages/ark angel mr.png'),
 ('800px-Ark_Angel_Elvaan_1.png','mobimages/ark angel ev.png'),
 ('800px-Ark_Angel_Galka_1.png','mobimages/ark angel gk.png'),
]
for s,d in jobs:
    print(d, trim(s,d))
# Shadow Lord family icon: trimmed render, capped to ~256 on long side, JPG
sl=Image.open('mobimages/shadow lord.png').convert('RGB')
mx=max(sl.size); scale=256/mx if mx>256 else 1.0
ic=sl.resize((max(1,round(sl.size[0]*scale)),max(1,round(sl.size[1]*scale))))
ic.save('mobicons/Shadow Lord.jpg','JPEG',quality=90)
print('mobicons/Shadow Lord.jpg', ic.size)
