# Animated showcase of the Legendary cats' attacks (GIF), same panel style as the other attack showcases.
import os, math
D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, 'mock_attacks_rare.py')).read().split('# Rizz cat:')[0])
N = 84  # 6 s loop
SIZE = {'fairy': 110, 'military': 100, 'witch': 120}
WITCH = spr('cat_witch', h=SIZE['witch'])
POTION = WITCH.crop((round(WITCH.width*0.81), round(WITCH.height*0.48), WITCH.width, round(WITCH.height*0.83)))

def panel3(f, name, title, sub, cx, fx):
    p = Image.new('RGBA', (PW, PH), 'white'); d = ImageDraw.Draw(p); rnd.seed(hash(name) + f//3)
    G = 250; line(d, [(10, G), (PW-10, G)], 3, 1)
    cat = spr('cat_'+name, h=SIZE[name])
    st = {'cx': cx, 'cy': 0, 'pre': [], 'post': []}
    fx(f, d, p, st, G, cat)
    for fn in st['pre']: fn()
    put(p, cat, st['cx'], G)
    for fn in st['post']: fn()
    text(d, (PW/2, 22), title, 30); text(d, (PW/2, 52), sub, 22); box(d, 2, 2, PW-3, PH-3, 3)
    return p

def rats_row(p, d, xs, hits, pops, h=42):
    for i, x in enumerate(xs):
        put(p, spr('rat_basic2', h=h, red=hits[i]), x, 250)
        if pops[i]: k, t = pops[i]; text(d, (x + 8, 250 - h - 22 - k*3), t, 24)

# Fairy cat: waves its wand, lightning strikes a rat from above, 10 dmg, 2 s cooldown (default)
def fx_fairy(f, d, p, st, G, cat):
    k = f % (2*FPS); rx = 320
    wx, wy = st['cx'] - cat.width/2 + cat.width*0.95, G + 4 - cat.height + cat.height*0.33
    def draw():
        if k < 6:  # wand sparkles
            for i in range(6):
                a = i*math.pi/3 + k*0.5; r = 8 + k*2
                d.line([(wx + r*math.cos(a), wy + r*math.sin(a)), (wx + (r+6)*math.cos(a), wy + (r+6)*math.sin(a))], fill=INK, width=2)
        strike = 6 <= k < 11
        if strike:  # zigzag bolt from the sky onto the rat
            pts = [(rx - 10, 75)]
            for i in range(1, 7): pts.append((rx - 10 + (14 if i % 2 else -14), 75 + i*(G - 40 - 75)/6))
            d.line(pts, fill=INK, width=7); d.line(pts, fill='white', width=3)
        rats_row(p, d, [rx], [strike and k < 9], [(k-6, '-10') if 6 <= k < 15 else None])
        if k >= 15: text(d, (PW-80, 92), 'cooldown 1s', 22)
    st['post'].append(draw)

# Military cat: fires its gun, quick bullets, 3 dmg each, 4 per second (default)
def fx_military(f, d, p, st, G, cat):
    k = f; rx = 350
    mx, my = st['cx'] - cat.width/2 + cat.width*0.99, G + 4 - cat.height + cat.height*0.37
    def draw():
        hit = False
        for s in range(0, N, 4):  # a bullet every 4 frames (~3.5 per second)
            t = (k - s)/4
            if 0 <= t <= 1:
                x = mx + (rx - 30 - mx)*t; y = my + (G - 30 - my)*t
                d.line([(x - 18, y - 18*(G-30-my)/(rx-30-mx)), (x, y)], fill=INK, width=6)
                if t > 0.75: hit = True
        if k % 4 == 0:  # muzzle flash
            for i in range(5): a = -0.8 + i*0.4; d.line([(mx + 6*math.cos(a), my + 6*math.sin(a)), (mx + 16*math.cos(a), my + 16*math.sin(a))], fill=INK, width=2)
        rats_row(p, d, [rx], [hit], [((k % 4), '-3')])
    st['post'].append(draw)

# Witch cat: throws a potion that smashes and splashes, 12 dmg to rats in the splash + slows them, 3 s cooldown (default)
def fx_witch(f, d, p, st, G, cat):
    k = f % (3*FPS); xs = [250, 320, 392]
    px0, py0 = st['cx'] - cat.width/2 + cat.width*0.9, G + 4 - cat.height + cat.height*0.65
    tx = 300
    def draw():
        splash = 10 <= k < 22
        if k < 10:  # potion flies in an arc, spinning
            t = k/10; x = px0 + (tx - px0)*t; y = py0 + (G - 30 - py0)*t - math.sin(t*math.pi)*70
            pot = POTION.rotate(-k*36, expand=True, resample=Image.BICUBIC); p.alpha_composite(pot, (round(x - pot.width/2), round(y - pot.height/2)))
        if splash:  # splash droplets + puddle outline
            j = k - 10
            for i in range(9):
                a = math.pi + i*math.pi/8; r = 12 + j*6
                x = tx + r*math.cos(a)*1.3; y = G - 30 + r*math.sin(a) + j*j*0.6
                d.ellipse([x-5, y-5, x+5, y+5], outline=INK, width=2)
            d.ellipse([tx - 70, G - 6, tx + 70, G + 8], outline=INK, width=2)
        inside = [abs(x - tx) < 60 for x in xs]
        rats_row(p, d, xs, [splash and inside[i] and k < 15 for i in range(3)], [((k-10), '-12') if splash and inside[i] else None for i in range(3)])
        if 14 <= k < 36:
            for i, x in enumerate(xs):
                if inside[i]: text(d, (x, G + 22), 'slowed', 18)
        if k >= 22: text(d, (PW-80, 92), f'cooldown {3 - (k-10)//FPS}s', 22)
    st['post'].append(draw)

specs = [('fairy', 'Fairy cat', 'Wand lightning  -  10 dmg, 2 s cooldown', 105, fx_fairy),
         ('military', 'Military cat', 'Shoots bullets  -  3 dmg each, rapid fire', 120, fx_military),
         ('witch', 'Witch cat', 'Potion splash  -  12 dmg + slow, 3 s cooldown', 90, fx_witch)]
frames = []
for f in range(N):
    c = Image.new('RGBA', (880, 680), 'white'); d = ImageDraw.Draw(c); rnd.seed(1)
    text(d, (440, 25), 'LEGENDARY CATS  -  ATTACKS', 36)
    for i, (n, t, s, cx, fx) in enumerate(specs):
        c.alpha_composite(panel3(f, n, t, s, cx, fx), (10 + (i % 2)*440, 50 + (i//2)*315))
    x6, y6 = 450, 365; box(d, x6+2, y6+2, x6+PW-3, y6+PH-3, 3)
    for j, t in enumerate(['Legendary cats', 'Strongest attacks, long range', 'All three stand in the back row', 'Rainbow Rat lightning: 8 dmg', '(Fairy cat lightning: 10 dmg)']):
        text(d, (x6+PW/2, y6+50+j*46), t, 32 if j == 0 else 24)
    frames.append(c.convert('RGB').resize((704, 544), Image.LANCZOS))
pal = [fr.quantize(32, method=Image.Quantize.MEDIANCUT) for fr in frames]
pal[0].save(f'{OUT}/legendary-attacks.gif', save_all=True, append_images=pal[1:], duration=1000//FPS, loop=0, optimize=True)
frames[8].save(f'{OUT}/legendary-still.png')
print('ok')
