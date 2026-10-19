# Cut the Round 2 cats (and the weapons they throw) out of Jason's round2-sheet.png.
# Boxes are in a 2000-wide view of the sheet; exclude rects drop the hand-written names and "weap" labels.
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, '..', 'assets')
import importlib.util
spec = importlib.util.spec_from_file_location('ex', os.path.join(D, 'extract.py'))
src = open(os.path.join(D, 'extract.py')).read(); cut_src = src[src.index('def cut('):src.index('meta = {}')]
ns = {}; exec('import numpy as np\nfrom PIL import Image, ImageDraw\nfrom scipy import ndimage as nd\n' + cut_src, ns); cut = ns['cut']
SHEET = os.path.join(D, 'round2-sheet.png'); S = Image.open(SHEET).width / 2000
CATS = {
 'vampire': ((48, 275, 435, 568), [(130, 515, 290, 562)]),
 'samurai': ((468, 262, 742, 506), [(560, 490, 742, 540)]),
 'ninja': ((826, 275, 1102, 508), []),
 'musician': ((1200, 260, 1482, 490), [(1290, 470, 1440, 520)]),
 'artist': ((1578, 268, 1858, 502), []),
 'alien': ((45, 690, 380, 920), []),
 'dragon': ((465, 648, 782, 893), []),
 'unicat': ((786, 685, 1218, 918), []),
 'weather': ((1248, 538, 1532, 868), []),
 'warp': ((1575, 655, 1895, 886), []),
 'element': ((65, 1110, 340, 1338), []),
 'supercat': ((482, 1098, 810, 1328), []),
 'jedi': ((845, 1110, 1118, 1338), [(940, 1320, 1080, 1360)]),
 'warrior': ((1218, 1095, 1488, 1302), []),
 'tnt': ((1590, 1035, 1874, 1332), []),
}
WEAPONS = {
 'w_katana': (744, 268, 785, 428), 'w_star': (1100, 356, 1172, 425), 'w_notes': (1490, 300, 1567, 375),
 'w_brush': (1862, 352, 1980, 448), 'w_element': (345, 1158, 436, 1300), 'w_saber': (1124, 1114, 1164, 1274),
 'w_sword': (1499, 1092, 1553, 1284), 'w_tnt': (1882, 1162, 1968, 1268),
}
def despeck(im):  # drop little bits of the label brackets that sit on the crop edge
    import numpy as np
    from scipy import ndimage as nd
    a = np.array(im); lab, n = nd.label(a[..., 3] > 0); sizes = nd.sum(np.ones_like(lab), lab, range(1, n + 1))
    for i, sl in enumerate(nd.find_objects(lab)):
        edge = sl[0].start == 0 or sl[1].start == 0 or sl[0].stop == a.shape[0] or sl[1].stop == a.shape[1]
        if edge and sizes[i] < 0.02 * sizes.max(): a[lab == i + 1] = 0
    im = Image.fromarray(a); return im.crop(im.getbbox())
SPECKY = {'cat_jedi', 'cat_warrior', 'w_star', 'w_tnt', 'w_sword', 'w_katana', 'w_notes', 'w_element'}
meta = {}
for k, (box, ex) in CATS.items():
    im = cut(SHEET, box, ex, S)
    if 'cat_' + k in SPECKY: im = despeck(im)
    im.save(f'{OUT}/cat_{k}.png'); meta['cat_' + k] = im.size
for k, box in WEAPONS.items():
    im = cut(SHEET, box, [], S)
    if k in SPECKY: im = despeck(im)
    im.save(f'{OUT}/{k}.png'); meta[k] = im.size
print(json.dumps(meta))
