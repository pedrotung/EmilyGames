# Animated showcase of the Secret cats (Angel, Devil), same panel style as the other attack showcases.
import os, math
D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, 'mock_attacks_rare.py')).read().split('# Rizz cat:')[0])
N = 112  # 8 s loop
G = 250

def base(name, title, sub, draw):
    p = Image.new('RGBA', (PW, PH), 'white'); d = ImageDraw.Draw(p); rnd.seed(hash(name))
    line(d, [(10, G), (PW-10, G)], 3, 1)
    draw(p, d)
    text(d, (PW/2, 22), title, 30); text(d, (PW/2, 52), sub, 22); box(d, 2, 2, PW-3, PH-3, 3)
    return p

def poof(d, x, y, j):  # expanding puff circles where a rat vanished
    for i in range(6):
        a = i*math.pi/3; r = 8 + j*5
        d.ellipse([x + r*math.cos(a) - 7, y + r*math.sin(a) - 7, x + r*math.cos(a) + 7, y + r*math.sin(a) + 7], outline=INK, width=2)

# Angel cat: flies to the top, holy meow, hits every rat at once (-20). Second try: a boss zaps it mid-flight, it falls and starts again.
def angel(f):
    def draw(p, d):
        top = 150; ax = 105
        if f < 30: y = G - (G - top)*f/30; fly = True              # try 1: fly up
        elif f < 48: y = top; fly = True                            # blast
        elif f < 58: y = top + (G - top)*(f - 48)/10; fly = True    # glide down
        elif f < 62: y = G; fly = False
        elif f < 80: y = G - (G - top)*(f - 62)/30; fly = True      # try 2: fly up...
        elif f < 90: y0 = G - (G - top)*18/30; y = y0 + (G - y0)*((f - 80)/10)**2; fly = False  # ...zapped, falls
        else: y = G; fly = False
        hit_me = 79 <= f < 84
        im = spr('cat_angel', h=80, red=hit_me)
        if fly and f % 4 < 2: im = im.resize((im.width, int(im.height*0.9)))  # wing flap
        if fly and not hit_me:
            for i in range(3): d.line([(ax - 30 + i*30, y + 6), (ax - 30 + i*30, y + 16)], fill=INK, width=2)
        if 80 <= f < 90: im = im.rotate(-(f - 80)*8, expand=True, resample=Image.BICUBIC)
        put(p, im, ax, y)
        boss = f >= 62
        xs = [250, 320] + ([] if boss else [392])
        blast = 30 <= f < 44
        if blast:
            text(d, (ax + 120, top - 70), '~ MEOOOW ~', 28)
            for x in xs:  # holy light rays down to every rat
                for o in (-8, 0, 8): d.line([(ax + 40, top - 40), (x + o, G - 50)], fill=INK, width=1 if o else 3)
        for i, x in enumerate(xs):
            put(p, spr('rat_basic2', h=42, red=blast and f < 36), x, G)
            if blast: text(d, (x + 8, G - 64 - (f - 30)*3), '-30', 24)
        if 48 <= f < 62: text(d, (PW - 90, 92), 'cooldown 10s', 22)
        if boss:
            rx = 378; put(p, spr('rat_rainbow', h=70), rx, G)
            if 76 <= f < 82:  # rainbow lightning at the flying angel
                pts = [(rx - 20, G - 60)]; tx, ty = ax + 30, y - 40
                for i in range(1, 6): t = i/6; pts.append((pts[0][0] + (tx - pts[0][0])*t + (10 if i % 2 else -10), pts[0][1] + (ty - pts[0][1])*t))
                pts.append((tx, ty)); d.line(pts, fill=INK, width=6); d.line(pts, fill='white', width=2)
            if 80 <= f < 96: text(d, (ax + 70, 110), 'interrupted!', 28)
            if f >= 96: text(d, (ax + 70, G - 120), 'start again...', 26)
    return base('angel', 'Angel cat', 'Fly up, holy meow  -  30 dmg to ALL rats', draw)

# Devil cat: lunges and stabs with its trident. Any normal rat dies in one stab; a boss only takes 40.
def devil(f):
    c, k = f // 28, f % 28; rx = 320
    kind = lambda c: 'rat_queen' if c == 3 else 'rat_basic2'
    rh = lambda c: 80 if c == 3 else 44
    def draw(p, d):
        cx = 100 + (70*k/5 if k < 5 else 70*max(0, 1 - (k - 5)/5))
        put(p, spr('cat_devil', h=110), cx, G)
        stab = 4 <= k < 7
        if stab:  # stab sparks at the trident tips
            tx = cx - 151/2 + 151*0.95; ty = G - 100
            for i in range(4): a = -0.6 + i*0.4; d.line([(tx + 10*math.cos(a), ty + 10*math.sin(a)), (tx + 22*math.cos(a), ty + 22*math.sin(a))], fill=INK, width=2)
        boss = c == 3
        if boss or k < 5:
            put(p, spr(kind(c), h=rh(c), red=stab or (boss and 5 <= k < 8)), rx, G)
        elif k < 12:
            poof(d, rx, G - 22, k - 5); text(d, (rx, G - 90), 'defeated!', 26)
        else:  # next rat walks in from the right
            put(p, spr(kind(c + 1), h=rh(c + 1)), rx + (28 - k)*9, G)
        if boss and k >= 4: text(d, (rx + 10, G - 110 - min(k - 4, 8)*3), '-40', 28)
        if boss and k >= 10: text(d, (rx, G + 26), 'bosses survive', 20)
    return base('devil', 'Devil cat', 'Trident stab  -  kills any rat in 1 hit (not bosses)', draw)

frames = []
for f in range(N):
    c = Image.new('RGBA', (880, 680), 'white'); d = ImageDraw.Draw(c); rnd.seed(1)
    text(d, (440, 25), 'SECRET CATS  -  ATTACKS', 36)
    c.alpha_composite(angel(f), (10, 50)); c.alpha_composite(devil(f), (450, 50))
    box(d, 12, 367, 868, 668, 3)
    for j, t in enumerate(['Secret cats  -  6000 coins each, not in spins', 'Angel: flies up 3 s, then hits every rat on the field for 30', 'If a boss hits it in the air, it falls and must start again', 'Devil: front row, one stab defeats any normal rat', 'Bosses only take 40 per stab, 2 s cooldown']):
        text(d, (440, 410 + j*55), t, 32 if j == 0 else 26)
    frames.append(c.convert('RGB').resize((704, 544), Image.LANCZOS))
pal = [fr.quantize(32, method=Image.Quantize.MEDIANCUT) for fr in frames]
pal[0].save(f'{OUT}/secret-attacks.gif', save_all=True, append_images=pal[1:], duration=1000//FPS, loop=0, optimize=True)
for i in (36, 81, 100): frames[i].save(f'/tmp/claude-0/-home-claude/13041319-e160-5d00-9e6b-d3f686d8d6fe/scratchpad/secret-{i}.png')
print('ok')
