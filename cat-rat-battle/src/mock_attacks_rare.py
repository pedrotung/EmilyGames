# Animated showcase of the Rare cats' abilities (GIF), same style as mock_attacks.py.
import os, math
D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, 'mock_attacks.py')).read().split('specs = [')[0])
FPS = 14; N = 120  # ~8.5 s loop so Bleh's 8 s cooldown fits

def panel2(f, name, title, sub, rx, fx):
    p = Image.new('RGBA', (PW, PH), 'white'); d = ImageDraw.Draw(p); rnd.seed(hash(name) + f//3)
    G = 250; line(d, [(10, G), (PW-10, G)], 3, 1)
    cat = spr('cat_'+name, h=90 if name == 'ghost' else 120)
    st = {'cx': 90, 'cy': 0, 'rx': rx, 'red': False, 'rat': 'rat_basic', 'rat_s': 1.0, 'flip': False, 'hit': None, 'pre': [], 'post': []}
    fx(f, d, p, st, G, cat)
    for fn in st['pre']: fn()
    if not st.get('hide_cat'): put(p, cat, st['cx'], G + st['cy'])
    if st['rat']:
        r = spr(st['rat'], h=max(4, int(60*st['rat_s'])), red=st['red'], flip=st['flip']); put(p, r, st['rx'], G)
    for fn in st['post']: fn()
    if st['hit']: k, txt = st['hit']; text(d, (st.get('hx', st['rx']), G-80-k*3), txt, 28)
    text(d, (PW/2, 22), title, 30); text(d, (PW/2, 52), sub, 22); box(d, 2, 2, PW-3, PH-3, 3)
    return p

def at(cat, st, G, fx_, fy): return st['cx'] - cat.width/2 + cat.width*fx_, G + st['cy'] + 4 - cat.height + cat.height*fy

# Rizz cat: walks up to a rat, stands there 4 s, the rat runs away (counts as defeated)
def fx_rizz(f, d, p, st, G, cat):
    k = f % N; rx = 320
    if k < 14: st['cx'] = 90 + (rx-130-90)*k/14
    else: st['cx'] = rx-130
    if 14 <= k < 70:
        sec = 4 - (k-14)//FPS; text(d, (rx, G-95), f'{sec}', 34)
        if k % 10 < 5: text(d, (rx+40, G-70), '...', 30)
    if k >= 70:
        st['flip'] = True; st['rx'] = rx + (k-70)*12
        text(d, (PW/2, 100), 'Ran away = defeated!', 26)
        for i in range(3): line(d, [(st['rx']-60-i*8, G-20-i*12), (st['rx']-90-i*8, G-20-i*12)], 2, 0)
    if st['rx'] > PW + 60: st['rat'] = None

# Water: straight lines of water fan out from the mouth at a small angle; farther rats take less damage. 1 s cooldown
def fx_water(f, d, p, st, G, cat):
    k = f % FPS; x0, y0 = at(cat, st, G, 0.6, 0.43)
    rats = [(215, '-6'), (295, '-4'), (375, '-2')]; st['rat'] = None
    def beam():
        if k < 7:
            reach = min(1, (k+1)/3); L = (PW - 8 - x0)*reach
            base = math.atan2((G-12) - y0, PW - 8 - x0)
            for j, da in enumerate([-0.11, -0.04, 0.03, 0.10]):  # 4 straight water lines, small fan
                a = base + da; x1, y1 = x0 + L*math.cos(a)/math.cos(da), y0 + L*math.sin(a)/math.cos(da)
                n = 9  # gaps that travel outward so the lines read as flowing water
                for i in range(n):
                    t0 = (i + (k % 2)*0.5)/n; t1 = t0 + 0.8/n
                    if t1 > 1 or y0+(y1-y0)*t1 > G-4: continue  # stop at the ground
                    d.line([(x0+(x1-x0)*t0, y0+(y1-y0)*t0), (x0+(x1-x0)*t1, y0+(y1-y0)*t1)], fill=INK, width=4 if j in (1, 2) else 3)
        for i, (rx, dmg) in enumerate(rats):
            hit = 1 <= k < 7 and x0 + (PW-x0)*min(1, (k+1)/3) >= rx-25
            put(p, spr('rat_basic', h=46, red=hit and k < 5), rx, G)
            if 3 <= k < 10: text(d, (rx, G-70-(k-3)*3), dmg, 24 - i*2)
        if k >= 8: text(d, (PW/2, 92), 'cooldown 1s', 22)
    st['post'].append(beam)

# Bleh: shoots out its own tongue like a frog, pulls the rat in, chews and swallows it; 8 s cooldown
BLEH = Image.open(f'{A}/cat_bleh.png').convert('RGBA')
TONGUE = BLEH.crop((105, 64, 131, 119)).rotate(90, expand=True)  # his drawn tongue, now pointing right
BLEH_NT = BLEH.copy(); ImageDraw.Draw(BLEH_NT).rectangle([105, 67, 130, 118], fill='white')  # same cat, tongue tucked in
def bleh_img(tongue_len=0, mouth=0, squash=1.0, lump=None, tail=None):
    W0, H0 = BLEH.size; im = Image.new('RGBA', (W0 + 260, H0)); base = BLEH if (tongue_len == 0 and mouth == 0 and lump is None and tail is None) else BLEH_NT
    if squash != 1.0:
        b2 = base.resize((round(W0*squash), H0)); im.alpha_composite(b2, (round((W0-b2.width)/2), 0))
    else: im.alpha_composite(base, (0, 0))
    dd = ImageDraw.Draw(im); mx, my = 118, 74
    if mouth: dd.ellipse([mx-9*mouth, my-7*mouth, mx+9*mouth, my+7*mouth], fill=INK)
    if tongue_len > 0:
        tw = TONGUE.width; cut_ = 14
        mid = TONGUE.crop((cut_, 0, tw-22, TONGUE.height)).resize((max(1, round(tongue_len)), TONGUE.height))
        im.alpha_composite(TONGUE.crop((0, 0, cut_, TONGUE.height)), (mx-4, my-TONGUE.height//2))
        im.alpha_composite(mid, (mx-4+cut_, my-TONGUE.height//2))
        im.alpha_composite(TONGUE.crop((tw-22, 0, tw, TONGUE.height)), (mx-4+cut_+mid.width, my-TONGUE.height//2))
    if tail is not None:  # rat tail wiggling out of the mouth while chewing
        dd.line([(mx+4, my+2), (mx+18, my-6+tail), (mx+30, my-10-tail)], fill=INK, width=4)
    if lump is not None:
        dd.ellipse([mx-10, lump-9, mx+10, lump+9], outline=INK, width=4)
    return im

def fx_bleh(f, d, p, st, G, cat):
    k = f % N; rx = 300; sc = 120/BLEH.height; cx = 90; st['hide_cat'] = True
    left = cx - BLEH.width*sc/2; mouth_x = left + 118*sc; tip_max = (rx-40-mouth_x)/sc - 32
    args = {}
    if k < 3: args = dict(mouth=k/3)
    elif k < 9: args = dict(mouth=1, tongue_len=tip_max*(k-2)/6)
    elif k < 17:
        t = (k-9)/8; args = dict(mouth=1, tongue_len=tip_max*(1-t)); st['rx'] = rx - (rx-mouth_x)*t; st['rat_s'] = max(0.25, 1-t*0.75)
    elif k < 45:  # chewing
        j = (k-17) % 6; args = dict(mouth=0.4 if j < 3 else 0.9, squash=1.07 if j < 3 else 0.97, tail=(4 if j < 3 else -4) if k < 33 else None)
        st['rat'] = None; text(d, (cx+40, G-150), 'chew  chew', 26)
    elif k < 60:  # swallow: lump slides down the body
        args = dict(mouth=0.2 if k < 48 else 0, lump=74 + (k-45)*4); st['rat'] = None
        if k >= 50: text(d, (cx+40, G-150), 'GULP!', 32)
    else: st['rat'] = None
    if k >= 17:
        text(d, (PW-75, 92), f'cooldown {max(0, 8 - (k-17)//FPS)}s', 22)
        if k >= 70: st['rat'] = 'rat_basic'; st['rx'] = max(rx, PW + 40 - (k-70)*5); st['rat_s'] = 1
    img = bleh_img(**args); img = img.resize((round(img.width*sc), round(img.height*sc)), Image.LANCZOS)
    st['pre'].append(lambda: p.alpha_composite(img, (round(left), round(G + 4 - img.height))))

# Ghost cat: flies fast (rats mostly miss), pokes 1 dmg rapidly; 4 clones for 5 s that attack too, each on a different rat
def fx_ghost(f, d, p, st, G, cat):
    k = f % N; st['rat'] = None; st['hide_cat'] = True
    rats = [150, 205, 260, 315, 370]
    cloning = 40 <= k < 40 + 5*FPS
    g0 = spr('cat_ghost', h=62); gc = spr('cat_ghost', h=62); gc.putalpha(gc.getchannel('A').point(lambda a: int(a*0.55)))
    def draw():
        n = 5 if cloning else 1
        for i, rx in enumerate(rats):
            hit = i < n and (f + i) % 3 == 0
            put(p, spr('rat_basic', h=30, red=hit), rx, G)
            if i < n and (f + i) % 3 < 2: text(d, (rx+12, G-42-((f+i) % 3)*4), '-1', 20)
        for i in range(n):  # each ghost hovers over its own rat, darting in to poke
            rx = rats[i]; gx = rx - 10 + 12*math.sin(f*1.1 + i*1.7); gy = G - 45 - (i % 2)*55 + 8*math.sin(f*1.6 + i)
            im = g0 if i == 0 else gc
            p.alpha_composite(im, (round(gx-im.width/2), round(gy-im.height)))
        if f % 20 < 6: text(d, (rats[0]-40, G-12), 'miss!', 20)
        if cloning: text(d, (PW-80, 92), f'4 clones  {5 - (k-40)//FPS}s', 22)
        else: text(d, (PW-80, 92), 'clones in ' + (f'{(40-k)//FPS + 1}s' if k < 40 else 'cooldown'), 22)
    st['post'].append(draw)

# Nurse: tap a hurt cat, HEAL button appears on it, restores half its HP, once per battle
def fx_nurse(f, d, p, st, G, cat):
    k = f % N; st['cx'] = 60; rx = 330; st['rx'] = rx
    friend = spr('cat_cat', h=110); fx_ = 220
    hp = 1.0 - min(k, 50)/50*0.75
    if k >= 62: hp = min(1.0, 0.25 + 0.5) - max(0, k-62)/60*0.4
    def draw():
        put(p, spr('cat_cat', h=110, red=(k % 10 < 3 and k < 100)), fx_, G); hp_bar(d, fx_, G-150, hp, 80, 12) if not 50 <= k < 62 else None
        text(d, (PW-90, 92), f'Heals left: {1 if k < 62 else 0}', 22)
        def tap(x, y, j): circle(d, x, y, 30-j*3, 3); d.ellipse([x-8, y-8, x+8, y+8], fill=INK)
        if 50 <= k < 62:
            bx, by = fx_, G-125
            box(d, bx-55, by-20, bx+55, by+20, 3, fill='white'); text(d, (bx, by), 'HEAL', 28)
            tap(fx_, G-50, min(k-50, 6)) if k < 56 else tap(bx, by, k-56)
        if 62 <= k < 75:
            text(d, (fx_, G-165-(k-62)*2), '+50% hp', 26)
            for i in range(4): a = i*1.6+k*0.5; text(d, (fx_+45*math.cos(a), G-60+35*math.sin(a)), '+', 30)
        if 95 <= k < 112:
            tap(fx_, G-50, min(k-95, 6)); box(d, fx_-80, G-190, fx_+80, G-152, 3, fill='white'); text(d, (fx_, G-171), 'No heals left', 22)
    st['post'].append(draw)
    if k % 10 < 3: st['hit'] = (k % 10, '-5')

specs = [('rizz', 'Rizz cat', 'Stares 4 s, then the rat runs away', 320, fx_rizz),
         ('water', 'Water', 'Water fan, weaker farther away, 1 s cooldown', 300, fx_water),
         ('bleh', 'Bleh', 'Tongue grabs a rat, chews, swallows. 8 s cooldown', 300, fx_bleh),
         ('ghost', 'Ghost cat', '1 dmg pokes, hard to hit, 4 clones that fight too', 320, fx_ghost),
         ('nurse', 'Nurse', 'Tap a hurt cat to heal it, once per battle', 330, fx_nurse)]
frames = []
for f in range(N):
    c = Image.new('RGBA', (1300, 680), 'white'); d = ImageDraw.Draw(c); rnd.seed(1)
    text(d, (650, 25), 'RARE CATS  -  ABILITIES', 36)
    for i, (n, t, s, rx, fx) in enumerate(specs):
        c.alpha_composite(panel2(f, n, t, s, rx, fx), (10 + (i % 3)*430, 50 + (i//3)*310))
    x6, y6 = 10 + 2*430, 50 + 310; box(d, x6+2, y6+2, x6+PW-3, y6+PH-3, 3)
    for j, t in enumerate(['Team rules', 'Up to 5 cats on the field', 'Same cat can be taken more than once', '5 Ghost cats x (1 + 4 clones)', '= 25 ghosts on the field!']):
        text(d, (x6+PW/2, y6+50+j*48), t, 34 if j == 0 else 26)
    frames.append(c.convert('RGB').resize((1040, 544), Image.LANCZOS))
pal = [fr.quantize(32, method=Image.Quantize.MEDIANCUT) for fr in frames]
pal[0].save(f'{OUT}/rare-attacks.gif', save_all=True, append_images=pal[1:], duration=1000//FPS, loop=0, optimize=True)
for i in (5, 12, 25, 50, 58): frames[i].save(f'{OUT}/rare-still-{i}.png')
print('ok')
