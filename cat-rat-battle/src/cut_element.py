# Element cat re-cut (Jason 2026-10-19: the first cut had white spilling outside the lines).
# His drawing leaves the face open where the whiskers are, so two invisible guide lines close
# those gaps for the white fill only; the ink itself is untouched.
import os, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd
D = os.path.dirname(os.path.abspath(__file__)); SHEET = os.path.join(D, 'round2-sheet.png')
S = Image.open(SHEET).width / 2000
box = [int(v * S) for v in (50, 1095, 365, 1350)]
im = Image.open(SHEET).convert('RGBA'); bg = Image.new('RGBA', im.size, 'white'); bg.alpha_composite(im)
a = np.array(bg.convert('RGB')).astype(int)[box[1]:box[3], box[0]:box[2]]
ink = a.min(2) < 200
lab, n = nd.label(nd.binary_dilation(ink, iterations=2)); keep = np.zeros_like(ink)
for i, sl in enumerate(nd.find_objects(lab)):
    cy, cx = (sl[0].start + sl[0].stop) / 2, (sl[1].start + sl[1].stop) / 2
    if cx > 335 or cy > 275 or (sl[0].stop - sl[0].start) * (sl[1].stop - sl[1].start) < 30: continue  # weapon, name label, specks
    keep |= lab == i + 1
ink &= keep
guide = Image.new('L', (ink.shape[1], ink.shape[0])); g = ImageDraw.Draw(guide)
g.line([(138, 112), (136, 166)], fill=1, width=6); g.line([(301, 108), (309, 156)], fill=1, width=6); g.line([(124, 184), (124, 218)], fill=1, width=6)  # face sides, tail end
wall = ink | (np.array(guide) > 0)
body = nd.binary_fill_holes(nd.binary_closing(np.pad(wall, 6), iterations=3))[6:-6, 6:-6]
out = np.zeros(a.shape[:2] + (4,), np.uint8); out[..., :3] = 255; out[body, 3] = 255
dark = 255 - a.min(2)
near = nd.binary_dilation(ink, iterations=1)
out[near, :3] = a[near]; out[near, 3] = np.maximum(out[near, 3], np.clip(dark[near] * 2, 0, 255)).astype(np.uint8)
out[ink, 3] = 255
img = Image.fromarray(out); img = img.crop(img.getbbox())
img.save(os.path.join(D, '..', 'assets', 'cat_element.png')); print(img.size)
