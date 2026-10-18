# Animated showcase of the rats' attacks (rats-plan.md), from mock.py helpers and Jason's sprites.
import os, math
D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, 'mock.py')).read().split('# 1. Main page')[0])
OUT = os.path.join(D, '..', 'design', 'rats'); os.makedirs(OUT, exist_ok=True)
FPS = 14; N = 112; PW, PH = 420, 300; G = 262
_cache = {}
def S(name, h, red=False, flip=False):
    k = (name, h, red, flip)
    if k not in _cache: _cache[k] = spr(name, h=h, red=red, flip=flip)
    return _cache[k]

def pop(d, x, y, txt, k): text(d, (x, y - k*3), txt, 24)

def base(title, sub, f, seed):
    p = Image.new('RGBA', (PW, PH), 'white'); d = ImageDraw.Draw(p); rnd.seed(seed + f//3)
    line(d, [(10, G), (PW-10, G)], 3, 1)
    text(d, (PW/2, 22), title, 30); text(d, (PW/2, 52), sub, 21)
    return p, d

def cat_at(p, x, y, red=False, name='cat_cat', h=80): put(p, S(name, h, red), x, y)

def bite(d, x, y):  # teeth marks
    for i in range(3): line(d, [(x-10+i*10, y-8), (x-6+i*10, y+4)], 3, 0)

# 1 Basic rat: bites the cat in front, 3 dmg every second
def basic(f):
    p, d = base('Basic rat', 'Bites  -  3 dmg, 1 per second', f, 1); k = f % FPS
    lunge = 10 if k < 3 else 0
    cat_at(p, 120, G, red=2 <= k < 5); put(p, S('rat_basic', 60), 250 - lunge, G)
    if 1 <= k < 4: bite(d, 165, G-40)
    if 2 <= k < 10: pop(d, 120, G-100, '-3', k-2)
    return p

# 2 Ball rat: swings its tail ball over and hits 2 neighbouring front cats, 6 dmg every 1.5 s
def ball(f):
    p, d = base('Ball rat', 'Tail ball smash  -  6 dmg to 2 cats, 1.5 s', f, 2); k = f % 21
    hit = 8 <= k < 12
    cat_at(p, 110, G-55, red=hit, h=70); cat_at(p, 140, G, red=hit, h=80)
    rat = S('rat_ball', 66); put(p, rat, 290, G)
    tx, ty = 290 + rat.width/2 - 8, G - rat.height + 8  # tail ball rest position
    if k < 8: t = k/8; bx = tx + (180 - tx)*t; by = ty - 110*math.sin(t*math.pi) + (G-80-ty)*t
    elif k < 14: bx, by = 180, G-80
    else: t = (k-14)/7; bx = 180 + (tx-180)*t; by = G-80 + (ty-(G-80))*t
    line(d, [(tx-10, ty+6), (bx, by)], 3, 0.5); d.ellipse([bx-9, by-9, bx+9, by+9], fill=INK)
    if hit:
        for i in range(6): a = i*math.pi/3; d.line([(bx+14*math.cos(a), by+14*math.sin(a)), (bx+24*math.cos(a), by+24*math.sin(a))], fill=INK, width=3)
    if 8 <= k < 16: pop(d, 70, G-150, '-6', k-8); pop(d, 190, G-110, '-6', k-8)
    return p

# 3 Spike rat: charges with its nose spike (first hit 20), then stabs 10 every 2 s
def spike(f):
    p, d = base('Spike rat', 'Charge 20 dmg, then stabs 10 every 2 s', f, 3); k = f % N
    if k < 12: x = 420 - k*14
    else: x = 252 - (8 if (k-12) % 28 < 3 else 0)
    first = 10 <= k < 14; stab = k >= 12 and 1 <= (k-12) % 28 < 4 and k > 30
    cat_at(p, 120, G, red=first or stab); put(p, S('rat_spike', 54), x, G)
    if k < 12:
        for i in range(3): line(d, [(x+60+i*12, G-30+i*10), (x+100+i*12, G-30+i*10)], 2, 0)
        text(d, (x, G-80), 'CHARGE!', 26)
    if 11 <= k < 20: pop(d, 120, G-100, '-20', k-11)
    if k > 30 and 1 <= (k-12) % 28 < 9: pop(d, 120, G-100, '-10', (k-12) % 28 - 1)
    return p

# 4 Rat Queen (L1 boss): bites 8, every 10 s calls 2 Basic rats
def queen(f):
    p, d = base('Rat Queen  (Level 1 boss, 150 hp)', 'Bites 8 dmg; calls 2 Basic rats every 10 s', f, 4); k = f % N
    lunge = 10 if k % FPS < 3 else 0
    cat_at(p, 90, G, red=2 <= k % FPS < 5); put(p, S('rat_queen', 100), 250 - lunge, G)
    if 2 <= k % FPS < 10: pop(d, 90, G-100, '-8', k % FPS - 2)
    if k >= 50:
        for i, (rx, ry) in enumerate([(360, G), (330, G-70)]):
            if k < 58:
                r = (k-50)*4
                for j in range(8): a = j*math.pi/4; d.line([(rx+r*math.cos(a), ry-25+r*math.sin(a)), (rx+(r+8)*math.cos(a), ry-25+(r+8)*math.sin(a))], fill=INK, width=2)
            put(p, S('rat_basic', 44), rx - max(0, k-58)*1.5, ry)
        if k < 70: text(d, (300, 95), 'Come, my rats!', 24)
    return p

# 5 Legged Rat (L2 boss): stomps 10; every 8 s jumps and slams the whole front row for 12
def legged(f):
    p, d = base('Legged Rat  (Level 2 boss, 300 hp)', 'Jump slam: 12 dmg to the whole front row', f, 5); k = f % 56
    if 20 <= k < 34: t = (k-20)/14; dy = -110*math.sin(t*math.pi)
    else: dy = 0
    slam = 34 <= k < 40
    sx = (3 if k % 2 else -3) if slam else 0
    for i, y in enumerate([G-70, G-35, G]): cat_at(p, 70 + i*35 + sx, y, red=slam, h=62)
    put(p, S('rat_legged', 130), 280 + sx, G + dy)
    if slam:
        r = (k-34)*14
        for side in (-1, 1): d.arc([280 - 40 - r, G-12, 280 + 40 + r, G+12], 160 if side < 0 else 0, 200 if side < 0 else 20, fill=INK, width=3)
        line(d, [(150, G-4), (210, G-4)], 3, 2)
    if 34 <= k < 44:
        for i, y in enumerate([G-70, G-35, G]): pop(d, 70 + i*35 + 30, y-70, '-12', k-34)
    if k < 20 and k % FPS < 3: text(d, (200, G-60), '-10', 22)
    if 14 <= k < 22: text(d, (300, 95), 'STOMP!', 28)
    return p

# 6 Clone Rat (L3 boss): every 12 s makes 2 fake clones that vanish after one hit
def clone(f):
    p, d = base('Clone Rat  (Level 3 boss, 350 hp)', '2 fake clones soak up attacks, 1 hit pops them', f, 6); k = f % N
    cat_at(p, 70, G, h=80)
    put(p, S('rat_clone', 90), 330, G)
    fakes = [(220, G-55), (235, G)]
    for i, (fx_, fy) in enumerate(fakes):
        born = 20 + i*6; dead = 60 + i*25
        if born <= k < born + 6:
            r = (k-born)*5
            for j in range(8): a = j*math.pi/4; d.line([(fx_+r*math.cos(a), fy-40+r*math.sin(a)), (fx_+(r+8)*math.cos(a), fy-40+(r+8)*math.sin(a))], fill=INK, width=2)
        if born + 3 <= k < dead: put(p, S('rat_clone', 80), fx_, fy)
        if dead - 6 <= k < dead:  # cat scratches the fake
            for j in range(3): line(d, [(fx_-25+j*10, fy-50), (fx_-35+j*10, fy-20)], 3, 0)
        if dead <= k < dead + 10: text(d, (fx_, fy-90-(k-dead)*2), 'fake! poof', 22)
    return p

# 7 Long Rat (L4 boss): long neck reaches over the front row to bite a back-row cat, 12 every 4 s
LONG = spr('rat_long', h=185)
def long_(f):
    p, d = base('Long Rat  (Level 4 boss, 500 hp)', 'Long neck bites the back row, 12 dmg / 4 s', f, 7); k = f % 56
    cat_at(p, 105, G, name='cat_nurse', h=78); cat_at(p, 215, G, name='cat_cat', h=80)
    if k < 14: ang = 0
    elif k < 22: ang = (k-14)/8*40
    elif k < 32: ang = 40
    elif k < 40: ang = 40 - (k-32)/8*40
    else: ang = 0
    im = LONG.rotate(ang, expand=True, resample=Image.BICUBIC)
    # keep the foot planted at the same spot
    fx_, fy = 345 - 45*ang/40, G  # steps forward as it leans in
    rad = math.radians(ang); w, h = LONG.size
    cx, cy = w*0.8, h  # pivot in sprite coords
    # expand=True recentres; find where the pivot lands by rotating a marker image
    mk = Image.new('L', LONG.size); ImageDraw.Draw(mk).ellipse([cx-3, cy-6, cx+3, cy], fill=255)
    mk = mk.rotate(ang, expand=True); bb = mk.getbbox()
    px, py = (bb[0]+bb[2])/2, bb[3]
    p.alpha_composite(im, (round(fx_ - px), round(fy - py)))
    red = 22 <= k < 28
    if red:
        p.alpha_composite(S('cat_nurse', 78, True), (round(105 - S('cat_nurse', 78).width/2), G + 4 - 78))
        bite(d, 120, G-70)
    if 22 <= k < 32: pop(d, 60, G-110, '-12', k-22)
    return p

# 8 Rainbow Rat (L5 boss): changes colour every 5 s, each colour a different move
def tint(im, rgb):
    im = im.copy(); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and max(r, g, b) - min(r, g, b) > 50: px[x, y] = (*rgb, a)
    return im
RB = spr('rat_rainbow', h=120)
PHASES = [('RED: fire breath', (235, 60, 50)), ('YELLOW: lightning', (245, 200, 40)), ('GREEN: heals +30', (70, 200, 70)), ('BLUE: 3 s immune', (60, 120, 230))]
RBT = [tint(RB, c) for _, c in PHASES]
def rainbow(f):
    p, d = base('Rainbow Rat  (Level 5 boss, 600 hp)', 'Changes colour every 5 s, each colour a new move', f, 8)
    ph = (f // 28) % 4; k = f % 28
    for i, y in enumerate([G-60, G]): cat_at(p, 80 + i*30, y, red=(ph == 0 and 8 <= k < 20) or (ph == 1 and i == 1 and 10 <= k < 16), h=66)
    p.alpha_composite(RBT[ph], (round(300 - RB.width/2), G + 4 - RB.height))
    text(d, (PW/2, 90), PHASES[ph][0], 26)
    mx, my = 300 - RB.width/2 + 10, G - 70
    if ph == 0 and 6 <= k < 20:  # black-and-white flame lines from its mouth
        for j in range(5):
            a = math.pi + (j-2)*0.13; L = 90 + 40*((k + j) % 3)
            pts = [(mx + L*t*math.cos(a) + 6*math.sin(t*12 + k), my + L*t*math.sin(a) + 6*math.cos(t*12 + k)) for t in [i/8 for i in range(9)]]
            d.line(pts, fill=INK, width=3)
        if k >= 10: pop(d, 90, G-130, '-15', k-10)
    if ph == 1 and 8 <= k < 16:  # zigzag bolt onto one cat
        x0, y0 = 120, 100; pts = [(x0, y0)]
        for i in range(1, 6): pts.append((x0 + (12 if i % 2 else -12), y0 + i*(G-60-y0)/5))
        d.line(pts, fill=INK, width=5); pop(d, 140, G-90, '-8', k-8)
    if ph == 2 and 4 <= k < 20:
        for i in range(5): a = i*1.25 + k*0.3; text(d, (300 + 70*math.cos(a), G-60 + 40*math.sin(a) - k*1.5), '+', 30)
        text(d, (300, G-150), '+30', 26)
    if ph == 3:
        r = 82 + (k % 3)
        d.ellipse([300-r, G-60-r*0.9, 300+r, G-60+r*0.9], outline=INK, width=3)
        if 10 <= k < 18: text(d, (215, G-120), 'immune!', 24)
    return p

panels = [basic, ball, spike, queen, legged, clone, long_, rainbow]
frames = []
for f in range(N):
    c = Image.new('RGBA', (1300, 1000), 'white'); d = ImageDraw.Draw(c); rnd.seed(9)
    text(d, (650, 25), 'RATS  -  ATTACKS', 36)
    for i, fn in enumerate(panels):
        pp = fn(f); box(ImageDraw.Draw(pp), 2, 2, PW-3, PH-3, 3)
        c.alpha_composite(pp, (10 + (i % 3)*430, 50 + (i//3)*315))
    x6, y6 = 10 + 2*430, 50 + 2*315; box(d, x6+2, y6+2, x6+PW-3, y6+PH-3, 3)
    for j, t in enumerate(['Rat rules', 'Rats hit the FRONT row first', 'Back row only when front is empty', 'Long Rat can reach the back row', '+10% hp and damage each level']):
        text(d, (x6+PW/2, y6+50+j*48), t, 32 if j == 0 else 24)
    frames.append(c.convert('RGB').resize((975, 750), Image.LANCZOS))
pal = [fr.quantize(48, method=Image.Quantize.MEDIANCUT) for fr in frames]
pal[0].save(f'{OUT}/rat-attacks.gif', save_all=True, append_images=pal[1:], duration=1000//FPS, loop=0, optimize=True)
for i in (10, 36, 62): frames[i].save(f'{OUT}/rat-still-{i}.png')
print('ok')
