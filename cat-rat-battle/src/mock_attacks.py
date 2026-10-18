# Animated showcase of the six Common cats' attacks (GIF), from mock.py helpers and Jason's sprites.
import os, math
D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, 'mock.py')).read().split('# 1. Main page')[0])
OUT = os.path.join(D, '..', 'design', 'attacks'); os.makedirs(OUT, exist_ok=True)
FPS = 14; N = 84  # 6 s loop at 70 ms per frame
PW, PH = 420, 300
HAT = Image.open(f'{A}/hat.png').convert('RGBA')

def panel(f, name, title, sub, ratx, anchor, fx):
    p = Image.new('RGBA', (PW, PH), 'white'); d = ImageDraw.Draw(p); rnd.seed(hash(name) + f//3)
    G = 250; line(d, [(10, G), (PW-10, G)], 3, 1)
    cat = spr('cat_'+name, h=120); cx = 90
    st = {'hit': None, 'red': False, 'cat_off': 0, 'rat': 'rat_basic'}
    fx(f, d, p, st, cx, G, cat, ratx)
    put(p, cat, cx + st['cat_off'], G)
    if st['rat']:
        put(p, spr(st['rat'], h=st.get('rath', 60), red=st['red']), ratx, G)
    if st['hit']:
        k, txt = st['hit']; text(d, (ratx, G-80-k*3), txt, 28)
    text(d, (PW/2, 22), title, 30); text(d, (PW/2, 52), sub, 22)
    box(d, 2, 2, PW-3, PH-3, 3)
    return p

def ax(cat, cx, G, fx_, fy):  # anchor point on the sprite as fractions of its box
    return cx - cat.width/2 + cat.width*fx_, G + 4 - cat.height + cat.height*fy

# Cat: scratch at short range, 5 each
def fx_cat(f, d, p, st, cx, G, cat, rx):
    k = f % 10
    if k < 3: st['cat_off'] = 12
    if 1 <= k < 5:
        for i in range(3): line(d, [(rx-20+i*12, G-55), (rx-34+i*12, G-15)], 4, 0.5)
        st['red'] = True
    if 1 <= k < 9: st['hit'] = (k, '-5')

# Cool cat: laser from sunglasses, 5 per second
def fx_cool(f, d, p, st, cx, G, cat, rx):
    x0, y0 = ax(cat, cx, G, 0.68, 0.32); x1, y1 = rx-25, G-30
    w = 7 + (f % 2)*3
    d.line([(x0, y0), (x1, y1)], fill=INK, width=w); d.line([(x0, y0), (x1, y1)], fill='white', width=max(1, w-6))
    for i in range(3): a = f*0.9+i*2.1; d.line([(x1, y1), (x1+14*math.cos(a), y1+14*math.sin(a))], fill=INK, width=3)
    st['red'] = f % 4 < 2
    k = f % FPS
    if k < 9: st['hit'] = (k, '-5')

# Bad cat: spits a cigarette every 2 s, 10 each
def fx_bad(f, d, p, st, cx, G, cat, rx):
    k = f % (2*FPS); x0, y0 = ax(cat, cx, G, 0.55, 0.42); x1, y1 = rx-20, G-35
    if k < 8:
        t = k/8; x = x0+(x1-x0)*t; y = y0+(y1-y0)*t - math.sin(t*math.pi)*40; a = t*6
        pts = [(x+16*math.cos(a)*s+4*math.sin(a)*q, y+16*math.sin(a)*s-4*math.cos(a)*q) for s, q in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
        d.polygon(pts, fill='white', outline=INK, width=3)
        ex, ey = x+16*math.cos(a), y+16*math.sin(a); d.ellipse([ex-4, ey-4, ex+4, ey+4], fill=INK)
        st['cat_off'] = 4 if k < 2 else 0
    elif k < 16:
        st['hit'] = (k-8, '-10'); st['red'] = k < 12
        for i in range(5): a = i*1.25; r = (k-8)*4; line(d, [(x1+r*math.cos(a), y1+r*math.sin(a)), (x1+(r+8)*math.cos(a), y1+(r+8)*math.sin(a))], 3, 0)
    else:
        text(d, (cx+70, G-150), 'cooldown', 20)

# Gentlemat: throws the hat (held in hand), 6 each, 3 s cooldown; hat comes back
def fx_gent(f, d, p, st, cx, G, cat, rx):
    k = f % (3*FPS); x0, y0 = ax(cat, cx, G, 0.95, 0.5); x1, y1 = rx-10, G-40
    if k < 10: t = k/10
    elif k < 20: t = 1-(k-10)/10
    else: t = 0
    x = x0+(x1-x0)*t; y = y0+(y1-y0)*t - math.sin(t*math.pi)*50
    h = HAT.resize((48, 45)).rotate(-k*36 if 0 < k < 20 else 0, expand=True, resample=Image.BICUBIC)
    p.alpha_composite(h, (round(x-h.width/2), round(y-h.height/2)))
    if 0 < k < 20: line(d, [(x-30, y-8), (x-50, y-8)], 2, 0); line(d, [(x-30, y+6), (x-46, y+6)], 2, 0)
    if 10 <= k < 18: st['hit'] = (k-10, '-6'); st['red'] = k < 14
    if k >= 22: text(d, (cx+70, G-150), 'cooldown', 20)

# Daisy: flings petals nonstop at long range, 2 each
def fx_daisy(f, d, p, st, cx, G, cat, rx):
    x0, y0 = ax(cat, cx, G, 0.52, 0.12); x1, y1 = rx-20, G-35
    for s in range(0, 12, 3):
        t = ((f - s) % 12)/12; x = x0+(x1-x0)*t; y = y0+(y1-y0)*t - math.sin(t*math.pi)*30; a = (f+s)*0.8
        d.ellipse([x-10, y-6, x+10, y+6], fill='white', outline=INK, width=2)
        line(d, [(x, y), (x+5*math.cos(a), y+5*math.sin(a))], 2, 0)
    st['red'] = f % 3 == 0
    st['hit'] = (f % 6, '-2')

# Alert cat: no attack; boss coming makes the ball flash + alert sound, sometimes shields the team for 5 s
def fx_alert(f, d, p, st, cx, G, cat, rx):
    bx, by = ax(cat, cx, G, 0.6, 0.12)
    st['rat'] = 'rat_queen'; st['rath'] = 95
    flashing = f < 40
    if flashing and f % 6 < 3:
        for i in range(8):
            a = i*math.pi/4; d.line([(bx+12*math.cos(a), by+12*math.sin(a)), (bx+24*math.cos(a), by+24*math.sin(a))], fill=INK, width=3)
        text(d, (bx+70, by-10), 'BEEP!', 28)
    if f < 40: text(d, (PW/2, 90), 'BOSS INCOMING!', 26)
    else:
        r = 82 + (f % 4)
        d.arc([cx-r, G-1.6*r, cx+r, G+0.4*r], 180, 360, fill=INK, width=3)
        for a in range(190, 360, 25): d.arc([cx-r-8, G-1.6*r-8, cx+r+8, G+0.4*r+8], a, a+10, fill=INK, width=2)
        text(d, (cx+150, G-170), f'SHIELD {max(0, 5-(f-40)//FPS)}s', 22)
        if (f-40) % 14 < 6: text(d, (cx+100, G-90), 'blocked', 22)

specs = [('cat', 'Cat', 'Scratch  -  5 dmg, short range', 205, fx_cat),
         ('cool', 'Cool cat', 'Sunglasses laser  -  5 dmg / sec', 330, fx_cool),
         ('bad', 'Bad cat', 'Spits cigarettes  -  10 dmg, 2 s cooldown', 320, fx_bad),
         ('gentlemat', 'Gentlemat', 'Throws its hat  -  6 dmg, 3 s cooldown', 320, fx_gent),
         ('daisy', 'Daisy', 'Petals  -  2 dmg, no cooldown, long range', 365, fx_daisy),
         ('alert', 'Alert cat', 'No attack. Boss alert + random team shield', 330, fx_alert)]
frames = []
for f in range(N):
    c = Image.new('RGBA', (1300, 680), 'white'); d = ImageDraw.Draw(c)
    text(d, (650, 25), 'COMMON CATS  -  ATTACKS', 36)
    for i, (n, t, s, rx, fx) in enumerate(specs):
        c.alpha_composite(panel(f, n, t, s, rx, None, fx), (10 + (i % 3)*430, 50 + (i//3)*310))
    frames.append(c.convert('RGB').resize((1040, 544), Image.LANCZOS))
pal = [fr.quantize(32, method=Image.Quantize.MEDIANCUT) for fr in frames]
pal[0].save(f'{OUT}/common-attacks.gif', save_all=True, append_images=pal[1:], duration=1000//FPS, loop=0, optimize=True)
frames[5].save(f'{OUT}/common-attacks-still.png'); frames[50].save(f'{OUT}/common-attacks-still2.png')
print('ok')
