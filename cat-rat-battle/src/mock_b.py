# Branch B mockups: army battle (send cats down a lane against the rat hole), same sprites and helpers as mock.py.
import os
D = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(D, 'mock.py')).read().split('# 1. Main page')[0]
exec(src)
OUT = os.path.join(D, '..', 'design', 'branch-b'); os.makedirs(OUT, exist_ok=True)

def cat_base(d, x, g):  # hand-drawn cat house with ears
    line(d, [(x-70, g), (x-70, g-170), (x-40, g-230), (x-20, g-185), (x+20, g-185), (x+40, g-230), (x+70, g-170), (x+70, g)], 5)
    line(d, [(x-22, g), (x-22, g-60), (x+22, g-60), (x+22, g)], 4)
    text(d, (x, g-130), 'w', 40)

def rat_hole(d, x, g):  # wall with a mouse hole
    line(d, [(x-60, g), (x-60, g-260), (x+80, g-260)], 5)
    for yy in range(g-230, g, 45): line(d, [(x-60, yy), (x+80, yy)], 2, 1)
    d.pieslice([x-40, g-110, x+50, g+90], 180, 360, fill=INK)

def card(c, d, x, y, name, cost, ready=True, sel=False):
    box(d, x, y, x+120, y+120, 5 if sel else 3, fill=None)
    im = spr('cat_'+name, h=72); c.alpha_composite(im, (round(x+60-im.width/2), y+8))
    ci = spr('cat_coin', h=0) if False else None
    text(d, (x+60, y+100), f'{cost} fish', 24)
    if not ready:
        sh = Image.new('RGBA', (118, 60), (120, 120, 120, 150)); c.alpha_composite(sh, (x+1, y+59))

def fish_meter(d, x, y, frac, label):
    box(d, x, y, x+230, y+30, 3); d.rectangle([x+2, y+2, x+2+226*frac, y+28], fill=INK)
    text(d, (x+115, y+52), label, 26)

# B1. Army battle ------------------------------------------------------------------
c = Image.new('RGBA', (W, H), 'white'); d = ImageDraw.Draw(c); top_bar(c, d, '1,265')
text(d, (W/2, 40), 'LEVEL 3', 40)
G = 500; ground(d, G)
cat_base(d, 100, G); hp_bar(d, 100, G-270, 0.85, 120, 14); text(d, (100, G-290), '850 / 1000', 22)
rat_hole(d, 1180, G); hp_bar(d, 1190, G-300, 0.6, 120, 14); text(d, (1190, G-320), '600 / 1000', 22)
put(c, spr('cat_nurse', h=95), 300, G)
put(c, spr('cat_cool', h=110), 470, G)
put(c, spr('cat_cat', h=110, red=True), 600, G); text(d, (600, G-150), '-8 hp', 30)
put(c, spr('rat_basic', h=60, red=True), 720, G); text(d, (720, G-85), '-5 hp', 30)
put(c, spr('rat_ball', h=60), 820, G)
put(c, spr('rat_basic', h=60), 930, G)
put(c, spr('rat_clone', h=110), 1060, G)
text(d, (300, G-120), '+', 36); text(d, (330, G-105), '+', 28)
fish_meter(d, 20, 560, 0.55, 'Fish 165 / 300')
for i, (n, cost, rdy) in enumerate([('cat', 50, True), ('cool', 75, False), ('nurse', 100, True), ('military', 200, False), ('witch', 300, False)]):
    card(c, d, 290+i*140, 548, n, cost, rdy)
circle(d, 1160, 620, 70); text(d, (1160, 605), 'CAT', 34); text(d, (1160, 640), 'CANNON', 26)
save_b = lambda im, n: (im.convert('RGB').save(f'{OUT}/{n}.png'), print(n))
save_b(c, 'mockup-b1-army-battle')

# B2. Team setup before a level ---------------------------------------------------------
c = Image.new('RGBA', (W, H), 'white'); d = ImageDraw.Draw(c); top_bar(c, d)
text(d, (W/2, 40), 'LEVEL 4  -  YOUR TEAM', 40)
text(d, (W/2, 95), 'Pick up to 5 cats to take into battle', 28)
team = [('cat', 50), ('cool', 75), ('nurse', 100), ('military', 200), (None, 0)]
for i, (n, cost) in enumerate(team):
    x = 260+i*160
    if n: card(c, d, x, 130, n, cost, True, True)
    else: box(d, x, 130, x+120, 250, 3); text(d, (x+60, 190), 'empty', 28)
line(d, [(60, 290), (1220, 292)], 2)
text(d, (60, 320), 'My cats', 30, 'lm')
owned = ['cat', 'cool', 'bad', 'daisy', 'rizz', 'nurse', 'ghost', 'catkid', 'military', 'witch']
for i, n in enumerate(owned):
    x = 60+(i % 8)*145; y = 350+(i//8)*140
    box(d, x, y, x+125, y+125, 3); im = spr('cat_'+n, h=88); c.alpha_composite(im, (round(x+62-im.width/2), y+18))
box(d, 960, 600, 1220, 690, 5); text(d, (1090, 645), 'FIGHT!', 52)
text(d, (60, 660), 'Boss:', 30, 'lm'); im = spr('rat_long', h=110); c.alpha_composite(im, (140, 600))
text(d, (230, 660), 'Long rat  500 hp', 30, 'lm')
save_b(c, 'mockup-b2-team')
