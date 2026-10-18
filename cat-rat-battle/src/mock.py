# Design mockups for Meow Brigade, built from Jason's own sprites (assets/).
import math, os, random
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(D, '..', 'assets'); OUT = os.path.join(D, '..', 'design')
os.makedirs(OUT, exist_ok=True)
W, H = 1280, 720
INK = (30, 32, 34); RED = (255, 150, 150)
FONT = os.path.join(D, 'fonts', 'patrick-hand-latin-400-normal.woff')
def F(sz): return ImageFont.truetype(FONT, sz)
rnd = random.Random(7)

def spr(name, h=None, w=None, red=False, flip=False):
    im = Image.open(f'{A}/{name}.png').convert('RGBA')
    if h: im = im.resize((round(im.width*h/im.height), h), Image.LANCZOS)
    elif w: im = im.resize((w, round(im.height*w/im.width)), Image.LANCZOS)
    if red:  # white body -> light red, ink untouched
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                if a and min(r, g, b) > 150 and max(r, g, b)-min(r, g, b) < 40:
                    t = (min(r, g, b)-150)/105; px[x, y] = (round(r*(1-t)+RED[0]*t), round(g*(1-t)+RED[1]*t), round(b*(1-t)+RED[2]*t), a)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im

def put(c, im, x, ground):  # x = centre, sits on the ground line
    c.alpha_composite(im, (round(x-im.width/2), round(ground-im.height+4)))

def line(d, pts, w=4, j=1.2):
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(2, int(math.hypot(x1-x0, y1-y0)/14))
        for i in range(n):
            t = i/n; out.append((x0+(x1-x0)*t+rnd.uniform(-j, j), y0+(y1-y0)*t+rnd.uniform(-j, j)))
    out.append(pts[-1]); d.line(out, fill=INK, width=w, joint='curve')

def box(d, x0, y0, x1, y1, w=4, fill=None):
    if fill: d.rectangle([x0, y0, x1, y1], fill=fill)
    line(d, [(x0, y0), (x1, y0+1), (x1-1, y1), (x0+1, y1-1), (x0, y0)], w)

def text(d, xy, s, sz, anchor='mm', fill=INK):
    d.text(xy, s, font=F(sz), fill=fill, anchor=anchor)

def circle(d, cx, cy, r, w=4, fill=None):
    if fill: d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill)
    line(d, [(cx+r*math.cos(a/40*2*math.pi), cy+r*math.sin(a/40*2*math.pi)) for a in range(42)], w, 0.8)

def coins(c, d, x, y, n, sz=36):
    ci = spr('cat_coin', h=sz); c.alpha_composite(ci, (x, y-sz//2)); text(d, (x+sz+8, y), n, sz, 'lm')

def top_bar(c, d, coin='1,250'):
    box(d, 20, 18, 128, 62); line(d, [(36, 44), (50, 30), (64, 44)], 3); line(d, [(40, 42), (40, 54), (60, 54), (60, 42)], 3)
    text(d, (96, 40), 'Home', 24)
    box(d, 1110, 18, 1260, 62); text(d, (1185, 40), 'Full screen', 24)
    coins(c, d, 940, 40, coin)

def hp_bar(d, cx, y, frac, w=90, h=14):
    d.rectangle([cx-w/2, y, cx-w/2+w*frac, y+h], fill=INK); box(d, cx-w/2, y, cx+w/2, y+h, 3)

def ground(d, y=600):
    line(d, [(0, y), (W, y+2)], 4, 1.5)
    for x in range(30, W, 180): line(d, [(x, y+30), (x+40, y+30)], 2, 1)

def save(c, name):
    c.convert('RGB').save(f'{OUT}/{name}.png'); print(name)

# 1. Main page ---------------------------------------------------------------
c = Image.new('RGBA', (W, H), 'white'); d = ImageDraw.Draw(c); top_bar(c, d)
text(d, (W/2, 130), 'MEOW BRIGADE', 110)
line(d, [(380, 190), (900, 194)], 3)
for i, (lab, sub) in enumerate([('PLAY', 'Level 3 / 5'), ('SPIN', 'Get new cats'), ('MY CATS', '7 / 20 found')]):
    x = 300 + i*340; box(d, x-140, 240, x+140, 380, 5)
    text(d, (x, 295), lab, 64); text(d, (x, 350), sub, 26)
ground(d, 640)
put(c, spr('cat_cool', h=170), 200, 640)
put(c, spr('rat_basic', h=58), 760, 640); put(c, spr('rat_ball', h=58), 920, 640); put(c, spr('rat_queen', h=110), 1110, 640)
text(d, (200, 455), 'Cool cat', 28)
save(c, 'mockup-1-main')

# 2. Gameplay (level 2) ---------------------------------------------------------
c = Image.new('RGBA', (W, H), 'white'); d = ImageDraw.Draw(c); top_bar(c, d, '1,265')
text(d, (W/2, 40), 'LEVEL 2', 40)
box(d, 470, 70, 810, 88, 3); d.rectangle([472, 72, 470+340*0.45, 86], fill=INK); text(d, (W/2, 108), 'Rats left: 6', 24)
for x, y in [(230, 210), (880, 190)]:  # doodle clouds: three bumps on a flat base
    pts = [(x, y)]
    for bx, br in [(30, 30), (80, 42), (130, 30)]:
        pts += [(x+bx+br*math.cos(math.pi-a*math.pi/8), y-br*math.sin(a*math.pi/8)*0.9) for a in range(9)]
    pts += [(x+160, y), (x, y)]; line(d, pts, 3, 0.6)
G = 560; ground(d, G)
cat = spr('cat_cat', h=170); put(c, cat, 300, G); hp_bar(d, 300, G-200, 0.8)
for k in range(3):  # paw swipe
    r = 70+k*16; line(d, [(390+r*math.cos(a/10), G-95+r*math.sin(a/10)) for a in range(-9, 8, 2)], 3, 0.5)
put(c, spr('rat_basic', h=78, red=True), 540, G); text(d, (540, G-125), '-5 hp', 32, fill=INK)
hp_bar(d, 540, G-95, 0.4, 70, 10)
put(c, spr('rat_basic', h=78), 730, G); hp_bar(d, 730, G-95, 1, 70, 10)
put(c, spr('rat_ball', h=78), 920, G); hp_bar(d, 920, G-95, 1, 70, 10)
put(c, spr('rat_ball', h=78), 1120, G); hp_bar(d, 1120, G-95, 1, 70, 10)
for cx, lab in [(90, '<'), (210, '>')]:
    circle(d, cx, 650, 46); text(d, (cx, 646), lab, 54)
circle(d, 1060, 650, 46); text(d, (1060, 650), 'JUMP', 28)
circle(d, 1185, 640, 56); text(d, (1185, 640), 'SWIPE', 30)
save(c, 'mockup-2-gameplay')

# 3. Boss fight (level 5) -------------------------------------------------------
c = Image.new('RGBA', (W, H), 'white'); d = ImageDraw.Draw(c); top_bar(c, d, '2,040')
text(d, (W/2, 34), 'LEVEL 5  -  BOSS', 34)
d.rectangle([342, 66, 340+600*0.7, 92], fill=INK); box(d, 340, 64, 940, 94, 4)
text(d, (W/2, 120), 'RAINBOW RAT   420 / 600 hp', 28)
G = 560; ground(d, G)
put(c, spr('cat_military', h=150, red=True), 320, G); hp_bar(d, 280, G-180, 0.55); text(d, (280, G-215), '-20 hp', 32)
put(c, spr('rat_spike', h=66), 620, G); hp_bar(d, 620, G-80, 1, 70, 10)
put(c, spr('rat_rainbow', h=250), 960, G)
for cx, lab in [(90, '<'), (210, '>')]:
    circle(d, cx, 650, 46); text(d, (cx, 646), lab, 54)
circle(d, 1060, 650, 46); text(d, (1060, 650), 'JUMP', 28)
circle(d, 1185, 640, 56); text(d, (1185, 640), 'SWIPE', 30)
save(c, 'mockup-3-boss')

# 4. Spin page --------------------------------------------------------------------
c = Image.new('RGBA', (W, H), 'white'); d = ImageDraw.Draw(c); top_bar(c, d)
tabs = ['COMMON', 'RARE', 'EPIC', 'LEGENDARY', 'SECRET']
for i, t in enumerate(tabs):
    x = 130 + i*200; box(d, x-90, 85, x+90, 135, 5 if i == 0 else 3, fill=(225, 225, 225) if i == 0 else None); text(d, (x, 110), t, 30)
cx, cy, R = 400, 420, 240
circle(d, cx, cy, R, 5)
names = ['cat', 'cool', 'bad', 'gentlemat', 'daisy', 'alert']
for i, n in enumerate(names):
    a = i/6*2*math.pi - math.pi/2
    line(d, [(cx, cy), (cx+R*math.cos(a), cy+R*math.sin(a))], 3)
    m = a + math.pi/6; im = spr('cat_'+n, h=90)
    c.alpha_composite(im, (round(cx+R*0.6*math.cos(m)-im.width/2), round(cy+R*0.6*math.sin(m)-im.height/2)))
circle(d, cx, cy, 18, 4, fill='white')
line(d, [(cx-20, cy-R-34), (cx+20, cy-R-34), (cx, cy-R+8), (cx-20, cy-R-34)], 4)
box(d, 760, 180, 1180, 470, 4)
text(d, (970, 215), 'You got:', 32)
put(c, spr('cat_daisy', h=170), 970, 420); text(d, (970, 450), 'Daisy  (NEW!)', 30)
box(d, 790, 520, 1150, 620, 5); text(d, (920, 570), 'SPIN', 56)
ci = spr('cat_coin', h=40); c.alpha_composite(ci, (995, 550)); text(d, (1045, 570), 'x 50', 40, 'lm')
save(c, 'mockup-4-spin')
