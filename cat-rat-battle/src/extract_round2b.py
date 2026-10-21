# Cut Jason's second Round 2 sheet (2026-10-21: Laboratory, Butterfly, Tiger, Tools, Cloud, Fish, Blow, Wizard, Queen).
# Boxes are in a 2000-wide view of the sheet, like extract_round2.py; it reuses cut() and despeck() from there.
import os, json
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, '..', 'assets')
src = open(os.path.join(D, 'extract_round2.py')).read()
ns = {'__file__': os.path.join(D, 'extract_round2.py')}
exec(src[:src.index('\nmeta = {}')], ns); cut, despeck = ns['cut'], ns['despeck']
SHEET = os.path.join(D, 'round2b-sheet.png'); S = Image.open(SHEET).width / 2000
CATS = {
 'lab': ((88, 212, 405, 472), []),
 'butterfly': ((722, 158, 1262, 458), []),
 'tiger': ((1522, 162, 1838, 462), []),
 'tools': ((88, 638, 422, 862), []),
 'cloud': ((808, 618, 1152, 872), []),
 'fish': ((1518, 632, 1902, 935), []),
 'blow': ((82, 1032, 402, 1322), []),
 'wizard': ((782, 1042, 1182, 1308), []),
 'queen': ((1512, 1062, 1838, 1318), []),
}
ITEMS = {'w_tube': (410, 300, 445, 384), 'w_cone': (428, 652, 480, 718), 'w_light': (502, 648, 548, 742), 'w_brick': (425, 730, 498, 798)}
meta = {}
for k, (box, ex) in CATS.items():
    im = despeck(cut(SHEET, box, ex, S)); im.save(f'{OUT}/cat_{k}.png'); meta['cat_' + k] = im.size
for k, box in ITEMS.items():
    im = despeck(cut(SHEET, box, [], S)); im.save(f'{OUT}/{k}.png'); meta[k] = im.size
print(json.dumps(meta))
