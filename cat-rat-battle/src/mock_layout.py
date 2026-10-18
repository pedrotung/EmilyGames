# Battlefield layout mockups based on Jason's layout sketch: open field, cats staggered on the left, rats scattered on the right.
import os, math
D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, 'mock.py')).read().split('# 1. Main page')[0])
OUT = os.path.join(D, '..', 'design', 'layout'); os.makedirs(OUT, exist_ok=True)

def hp_bar(d, cx, y, frac, w=70, h=8):  # light grey fill with a thin ink outline (Jason: the solid black bars were too heavy)
    x0 = cx - w/2
    if frac > 0: d.rounded_rectangle([x0, y, x0 + w*frac, y + h], radius=h/2, fill=(170, 170, 170))
    d.rounded_rectangle([x0, y, x0 + w, y + h], radius=h/2, outline=INK, width=2)

# 5 team slots in a zigzag (feet position): melee in the front column, ranged + Nurse in the back column
SLOTS = [('rizz', 'Rizz cat', 520, 320, 'front'), ('water', 'Water', 220, 375, 'back'), ('bleh', 'Bleh', 610, 465, 'front'),
         ('nurse', 'Nurse', 220, 625, 'back'), ('ghost', 'Ghost cat', 520, 625, 'front')]
HP = {'rizz': 1, 'bleh': 0.7, 'water': 1, 'ghost': 0.85, 'nurse': 1}
# rats scattered in a loose staggered grid, entering from the right
RATS = [('rat_basic2', 880, 285), ('rat_basic2', 1130, 275), ('rat_ball2', 1060, 360), ('rat_basic2', 840, 470),
        ('rat_basic2', 1100, 540), ('rat_ball2', 940, 640), ('rat_basic2', 1220, 650), ('rat_ball2', 1210, 400)]

def scene(annotate):
    c = Image.new('RGBA', (W, H), 'white'); d = ImageDraw.Draw(c); rnd.seed(3)
    top_bar(c, d, '1,295'); text(d, (W/2, 34), 'LEVEL 3', 38); text(d, (W/2, 72), 'Rats left: 12', 24)
    c.alpha_composite(spr('cat_nurse', h=40), (900, 74)); text(d, (965, 96), 'Heals left: 1', 24, 'lm')
    if annotate:  # zones
        def dash_box(x0, y0, x1, y1):
            for x in range(x0, x1, 24): d.line([(x, y0), (min(x+12, x1), y0)], fill=INK, width=2); d.line([(x, y1), (min(x+12, x1), y1)], fill=INK, width=2)
            for y in range(y0, y1, 24): d.line([(x0, y), (x0, min(y+12, y1))], fill=INK, width=2); d.line([(x1, y), (x1, min(y+12, y1))], fill=INK, width=2)
        dash_box(40, 150, 380, 680); dash_box(400, 150, 720, 680); dash_box(760, 150, 1270, 680)
        text(d, (210, 168), 'BACK: ranged + Nurse', 24); text(d, (560, 168), 'FRONT: melee', 24); text(d, (1015, 168), 'RATS: come in from the right', 24)
    items = [('cat', *s) for s in SLOTS] + [('rat', r[0], None, r[1], r[2], None) for r in RATS]
    for kind, name, label, x, y, role in sorted(items, key=lambda t: t[4]):
        if kind == 'cat':
            im = spr('cat_'+name, h=105); put(c, im, x, y)
            hp_bar(d, x, y - 122, HP[name], 64, 8)
            if annotate: circle(d, x - 70, y - 100, 14, 2); text(d, (x - 70, y - 101), str(SLOTS.index((name, label, x, y, role)) + 1), 20)
        else:
            im = spr(name, h=62); put(c, im, x, y); hp_bar(d, x, y - 70, 1, 44, 6)
    if annotate:
        text(d, (W/2, 702), 'Slots 1-5: you choose which cat goes where before the battle', 24)
    else:
        text(d, (W/2, 702), 'Cats fight on their own.  Tap a hurt cat to use a Nurse heal.', 24)
    c.convert('RGB').save(f'{OUT}/layout-{"zones" if annotate else "battle"}.png')

scene(False); scene(True); print('ok')
