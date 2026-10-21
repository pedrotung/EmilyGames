# Cut Jason's Round 4 rat sheet (2026-10-21): small rainbow rat, thrower rat, Rat Rat, and bosses Poop, Wriggly, Dash, Flying, Heartfelt.
# Boxes are in sheet pixels (1353x698); reuses cut() and despeck() from extract_round2.py.
import os, json
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, '..', 'assets')
src = open(os.path.join(D, 'extract_round2.py')).read()
ns = {'__file__': os.path.join(D, 'extract_round2.py')}
exec(src[:src.index('\nmeta = {}')], ns); cut, despeck = ns['cut'], ns['despeck']
SHEET = os.path.join(D, 'round4-rats-sheet.png')
RATS = {  # name: (box, erase rects)
 'rainbow_small': ((838, 108, 1026, 206), []),
 'thrower': ((592, 226, 738, 312), [(610, 308, 740, 330)]),
 'ratrat': ((1106, 318, 1262, 428), [(1180, 300, 1295, 336)]),
 'poop': ((2, 256, 214, 382), []),
 'wriggly': ((290, 256, 500, 354), []),
 'dash': ((508, 405, 750, 516), []),
 'flying': ((780, 466, 1030, 598), [(845, 455, 945, 506)]),
 'heartfelt': ((1080, 510, 1240, 642), []),
}
meta = {}
for k, (box, er) in RATS.items():
    im = despeck(cut(SHEET, box, [], 1, er)); im.save(f'{OUT}/rat_{k}.png'); meta['rat_' + k] = im.size
print(json.dumps(meta))
