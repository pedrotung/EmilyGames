# Cut sprites out of Jason's sheets: ink kept as drawn, interior filled white, outside transparent.
import json, os, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, '..', 'assets'); os.makedirs(OUT, exist_ok=True)
S = 2275/2000  # cat sheet coords below are on a 2000-wide view
CATS = {  # name: (box, [exclude rects])
 'cat':((45,213,228,360),[]), 'cool':((327,210,510,360),[(388,345,510,390)]),
 'bad':((602,210,785,357),[(680,350,785,390)]), 'gentlemat':((908,203,1092,345),[(968,340,1102,380)]),
 'daisy':((1211,145,1395,333),[]), 'alert':((1458,147,1645,345),[(1530,312,1645,350)]),
 'rizz':((171,461,354,605),[(236,598,354,640)]), 'water':((472,461,655,603),[(542,598,628,640)]),
 'bleh':((762,464,945,603),[(850,595,920,632)]), 'ghost':((1091,436,1274,563),[]),
 'nurse':((1366,418,1560,565),[(1440,560,1520,595)]),
 'senpai':((283,700,472,836),[]), 'catkid':((640,668,877,818),[(712,818,800,855)]),
 'catcat':((956,642,1173,808),[]), 'poison':((1227,655,1442,798),[(1285,795,1395,832)]),
 'fairy':((482,884,726,1040),[(528,1035,650,1092)]), 'military':((754,883,1071,1026),[(800,1022,940,1072)]),
 'witch':((1080,852,1310,1034),[(1132,1030,1250,1068)]),
 'angel':((590,1128,941,1282),[]), 'devil':((957,1085,1205,1258),[(1010,1255,1150,1308)]),
 'coin':((1672,248,1712,292),[]),
}
RATS = {
 'basic':((9,132,145,207),[]), 'ball':((236,248,377,320),[]), 'spike':((748,236,907,293),[]),
 'queen':((9,314,165,412),[]), 'legged':((226,404,418,535),[],[(396,400,420,485)]),
 'clone':((402,432,559,543),[]), 'long':((591,429,722,622),[],[[(585,540),(663,540),(683,590),(687,625),(585,625)],(711,535,725,572)]),
 'rainbow':((738,430,931,560),[],[(735,522,762,565)]),
}
def cut(sheet, box, excl, scale, erase=()):
    box = [int(v*scale) for v in box]; excl = [[v*scale for v in r] for r in excl]
    im = Image.open(sheet).convert('RGBA'); bg = Image.new('RGBA', im.size, 'white'); bg.alpha_composite(im)
    a = np.array(bg.convert('RGB')).astype(int)[box[1]:box[3], box[0]:box[2]]
    for r in erase:  # pixel erase: rect (x0,y0,x1,y1) or polygon [(x,y),...] in sheet coords
        pts = r if isinstance(r, list) else [(r[0],r[1]),(r[2],r[1]),(r[2],r[3]),(r[0],r[3])]
        mk = Image.new('L', (a.shape[1], a.shape[0])); ImageDraw.Draw(mk).polygon([(x-box[0], y-box[1]) for x,y in pts], fill=1)
        a[np.array(mk) > 0] = 255
    sat = a.max(2) - a.min(2)
    ink = (a.min(2) < 200) | (sat > 60)
    lab, n = nd.label(nd.binary_dilation(ink, iterations=2))
    keep = np.zeros_like(ink)
    for i, s in enumerate(nd.find_objects(lab)):
        cy = (s[0].start+s[0].stop)/2 + box[1]; cx = (s[1].start+s[1].stop)/2 + box[0]
        if any(r[0] <= cx <= r[2] and r[1] <= cy <= r[3] for r in excl): continue
        if (s[0].stop-s[0].start)*(s[1].stop-s[1].start) < 30: continue
        keep |= (lab == i+1)
    ink &= keep
    # outlines are hand drawn with gaps: close progressively until the body fills
    for it in (4, 7, 10, 14):
        p = np.pad(ink, it+2); body = nd.binary_fill_holes(nd.binary_closing(p, iterations=it))[it+2:-it-2, it+2:-it-2]
        if body.sum() > 2.2*ink.sum(): break
    # trim wedges the closing pushed outside the outline
    inner = nd.binary_opening(body & ~ink, iterations=3)
    body = inner | (body & nd.binary_dilation(inner, iterations=2))
    out = np.zeros(a.shape[:2]+(4,), np.uint8); out[..., :3] = 255
    out[body, 3] = 255
    dark = 255 - a.min(2)  # ink strength
    out[ink, :3] = a[ink]; out[ink, 3] = 255
    soft = ink & (sat <= 60); out[soft, 3] = np.clip(dark[soft]*2, 0, 255)
    out[soft & body] = np.concatenate([a, np.full(a.shape[:2]+(1,),255)],2)[soft & body]
    img = Image.fromarray(out); bb = img.getbbox(); return img.crop(bb)
meta = {}
for k,v in CATS.items():
    im = cut(os.path.join(D,'cats-sheet.png'), *v[:2], S, *v[2:]); im.save(f'{OUT}/cat_{k}.png'); meta['cat_'+k]=im.size
for k,v in RATS.items():
    im = cut(os.path.join(D,'rats-sheet.png'), *v[:2], 1, *v[2:]); im.save(f'{OUT}/rat_{k}.png'); meta['rat_'+k]=im.size
print(json.dumps(meta))

# Gentlemat redrawn by Jason with the hat he throws (held in hand, not worn)
for k, v in {'cat_gentlemat': ((200, 140, 1010, 775), []), 'hat': ((1055, 150, 1370, 450), [])}.items():
    im = cut(os.path.join(D, 'gentlemat-hat-sheet.jpg'), *v, 1); im.thumbnail((240, 240) if k == 'cat_gentlemat' else (90, 90), Image.LANCZOS); im.save(f'{OUT}/{k}.png')

# New thinner-line rats from Jason's battlefield layout sketch (2000-wide view coords)
for k, b in {'rat_basic2': (1208, 343, 1378, 452), 'rat_ball2': (1512, 498, 1685, 618)}.items():
    im = cut(os.path.join(D, 'layout-sketch.png'), b, [], S); im.save(f'{OUT}/{k}.png')

# Senpai with its pen and Cat cat with its football, redrawn by Jason (972x489 sheet, real pixel coords)
for k, b in {'cat_senpai2': (70, 135, 428, 352), 'cat_catcat2': (445, 85, 778, 346), 'football': (798, 238, 908, 342)}.items():
    im = cut(os.path.join(D, 'senpai-catcat-sheet.jpg'), b, [], 1); im.save(f'{OUT}/{k}.png')
