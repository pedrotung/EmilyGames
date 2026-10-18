# Animated showcase of the Epic cats' attacks (GIF), same panel framework as mock_attacks_rare.py.
import os, math
D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, 'mock_attacks_rare.py')).read().split('# Rizz cat:')[0])
N = 140  # 10 s loop: fits Cat cat's two 5 s kicks and Poison cat's 8 s cloud + cooldown
BALL = Image.open(f'{A}/football.png').convert('RGBA')

def cooldown(d, k0, secs, k):  # countdown label once the attack is spent
    left = secs - (k - k0)//FPS
    if left > 0: text(d, (PW-80, 92), f'cooldown {left}s', 22)

# Senpai: lunges and stabs with the pen it holds, 5 dmg, 3 s cooldown
def fx_senpai(f, d, p, st, G, cat):
    k = f % (3*FPS); st['rat'] = 'rat_basic2'; st['rx'] = 330
    if k < 4: st['cx'] = 100 + k*12
    elif k < 8: st['cx'] = 148 - (k-4)*12
    else: st['cx'] = 100
    if 3 <= k < 6:
        st['red'] = True; px, py = at(cat, st, G, 0.99, 0.6)
        for i in range(4): a = -0.6 + i*0.4; d.line([(px+10*math.cos(a), py+10*math.sin(a)), (px+22*math.cos(a), py+22*math.sin(a))], fill=INK, width=2)
    if 3 <= k < 12: st['hit'] = (k-3, '-5')
    if k >= 12: cooldown(d, 0, 3, k)

# Cat kid: dashes in head first, 15 dmg to the rat and 2 to itself, 3 s cooldown
def fx_catkid(f, d, p, st, G, cat):
    k = f % (3*FPS); st['rat'] = 'rat_basic2'; rx = 320; st['hide_cat'] = True
    if k < 6: x = 90 + (rx-150-90)*k/6; tilt = -18*k/6
    elif k < 10: x = rx-150; tilt = -18
    elif k < 18: x = rx-150 - (rx-150-90)*(k-10)/8; tilt = -18*(1-(k-10)/8)
    else: x, tilt = 90, 0
    hurt = 6 <= k < 9
    im = spr('cat_catkid', h=120, red=hurt).rotate(tilt, expand=True, resample=Image.BICUBIC)
    st['pre'].append(lambda: p.alpha_composite(im, (round(x - im.width/2), round(G + 4 - im.height))))
    if 6 <= k < 14: st['rx'] = rx + (k-6)*5; st['red'] = k < 10
    elif k >= 14: st['rx'] = max(rx, rx + 40 - (k-14)*3)
    if 6 <= k < 10:
        bx, by = rx-80, G-95
        for i in range(6): a = i*math.pi/3; d.line([(bx+10*math.cos(a), by+10*math.sin(a)), (bx+22*math.cos(a), by+22*math.sin(a))], fill=INK, width=3)
    if 6 <= k < 15: st['hit'] = (k-6, '-15'); text(d, (x, G-150-(k-6)*2), '-2', 24)
    if k >= 18: cooldown(d, 0, 3, k)

# Cat cat: kicks the football at a rat, 8 dmg, small chance to miss, 5 s cooldown
def fx_catcat(f, d, p, st, G, cat):
    k = f % N; st['rat'] = 'rat_basic2'; rx = 330; st['rx'] = rx
    kick = 0 if k < 70 else 70; j = k - kick; miss = kick == 70
    if j < 3: st['cx'] = 90 + j*6
    elif j < 6: st['cx'] = 108 - (j-3)*6
    fx0, fy0 = at(cat, st, G, 0.85, 0.9)
    if j < 12:
        t = j/12; tx = rx - 30 if not miss else PW + 40
        bx = fx0 + (tx - fx0)*t; by = fy0 - 20 - math.sin(t*math.pi)*(45 if not miss else 120)
        b = BALL.resize((34, 34)).rotate(-j*40, resample=Image.BICUBIC)
        st['post'].append(lambda: p.alpha_composite(b, (round(bx-17), round(by-17))))
    if not miss and 11 <= j < 20: st['hit'] = (j-11, '-8'); st['red'] = j < 15
    if miss and 8 <= j < 20: text(d, (rx, G-110), 'miss!', 28)
    if j >= 14: cooldown(d, kick + 14, 5, k)

# Poison cat: sprays a small poison cloud; every rat inside loses 3 hp per second for 8 s; 8 s cooldown
def fx_poison(f, d, p, st, G, cat):
    k = f % N; st['rat'] = None
    rats = [190, 258, 326, 398]
    cx, cy, R = 262, G-48, 110   # bigger cloud: covers three rats, the far one stays out
    live = 12 <= k < 12 + 8*FPS
    def cloud():  # one puffy outline: outlined circles, then grey fill on top hides the inner lines
        if not live: return
        bumps = []
        for i in range(8):
            a = i*2*math.pi/8 + k*0.02; r = 40 + 5*math.sin(k*0.15 + i)
            bumps.append((cx + 85*math.cos(a), cy + 34*math.sin(a), r))
        for x, y, r in bumps: d.ellipse([x-r, y-r, x+r, y+r], outline=INK, width=3)
        for x, y, r in bumps: d.ellipse([x-r+3, y-r+3, x+r-3, y+r-3], fill=(228, 228, 228))
        d.ellipse([cx-85, cy-34, cx+85, cy+34], fill=(228, 228, 228))
        for i in range(20):
            x = cx - 100 + (i*37 + k*2) % 200; y = cy - 35 + (i*13 + k) % 70
            d.ellipse([x-2, y-2, x+2, y+2], fill=INK)
    st['pre'].append(cloud)
    def draw():
        for i, rx in enumerate(rats):
            inside = live and abs(rx - cx) < R
            hit = inside and (k - 12) % FPS < 3
            put(p, spr('rat_basic2', h=44, red=hit), rx, G)
            if inside and (k - 12) % FPS < 9: text(d, (rx + 10, G-75-((k-12) % FPS)*2), '-3', 22)
        if k < 12:  # spray puffs from the cat
            sx, sy = at(cat, st, G, 0.75, 0.45)
            for i in range(6):
                t = ((k + i*2) % 12)/12; x = sx + (cx - sx)*t; y = sy + (cy - sy)*t + 10*math.sin(i)
                d.ellipse([x-6, y-6, x+6, y+6], outline=INK, width=2)
        elif live: text(d, (cx, G-150), f'poison {8 - (k-12)//FPS}s', 22)
        else: cooldown(d, 12 + 8*FPS, 8, k)
    st['post'].append(draw)

specs = [('senpai2', 'Senpai', 'Pen stab  -  5 dmg, 3 s cooldown', 330, fx_senpai),
         ('catkid', 'Cat kid', 'Headbutt  -  15 dmg, hurts itself 2, 3 s cooldown', 320, fx_catkid),
         ('catcat2', 'Cat cat', 'Football  -  8 dmg, can miss, 5 s cooldown', 330, fx_catcat),
         ('poison', 'Poison cat', 'Poison cloud  -  3 dmg/s to rats inside, 8 s', 0, fx_poison)]
frames = []
for f in range(N):
    c = Image.new('RGBA', (880, 680), 'white'); d = ImageDraw.Draw(c); rnd.seed(1)
    text(d, (440, 25), 'EPIC CATS  -  ATTACKS', 36)
    for i, (n, t, s, rx, fx) in enumerate(specs):
        c.alpha_composite(panel2(f, n, t, s, rx, fx), (10 + (i % 2)*440, 50 + (i//2)*315))
    frames.append(c.convert('RGB').resize((704, 544), Image.LANCZOS))
pal = [fr.quantize(32, method=Image.Quantize.MEDIANCUT) for fr in frames]
pal[0].save(f'{OUT}/epic-attacks.gif', save_all=True, append_images=pal[1:], duration=1000//FPS, loop=0, optimize=True)
frames[5].save(f'{OUT}/epic-still.png')
print('ok')
