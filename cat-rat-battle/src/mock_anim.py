# Animated mockup (GIF) of the auto battle with the nurse heal, built from mock.py helpers and Jason's sprites.
import os, math
D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, 'mock.py')).read().split('# 1. Main page')[0])
OUT = os.path.join(D, '..', 'design', 'auto-battle'); os.makedirs(OUT, exist_ok=True)
G = 520

class U:
    def __init__(s, name, x, hp, side, h, dmg=0, rate=10, ranged=False):
        s.name, s.x, s.hp, s.max, s.side, s.h, s.dmg, s.rate, s.ranged = name, x, hp, hp, side, h, dmg, rate, ranged
        s.im = spr(name, h=h); s.red = spr(name, h=h, red=True); s.flash = 0; s.cd = rate; s.lunge = 0
    @property
    def w(s): return s.im.width

cats = [U('cat_cool', 700, 100, 'cat', 130, 8, 9), U('cat_cat', 520, 100, 'cat', 125, 5, 9),
        U('cat_nurse', 340, 80, 'cat', 115), U('cat_military', 130, 90, 'cat', 110, 4, 10, True)]
rats = []
spawns = [(0, 'rat_basic', 15), (10, 'rat_ball', 25), (22, 'rat_basic', 15), (34, 'rat_ball', 25), (46, 'rat_basic', 15),
          (58, 'rat_ball', 25), (72, 'rat_basic', 15), (84, 'rat_ball', 25), (96, 'rat_basic', 15)]
pops, bullets = [], []
nurse_left, coins_n = 1, 1265
script = {'tap1': None, 'heal': None, 'tap2': None}
frames = []

def front(lst, side):
    alive = [u for u in lst if u.hp > 0]
    if not alive: return None
    return max(alive, key=lambda u: u.x) if side == 'cat' else min(alive, key=lambda u: u.x)

def hit(u, n):
    u.hp = max(0, u.hp-n); u.flash = 5; pops.append([u.x, G-u.h-48, f'-{n} hp', 14])

for f in range(400):
    for t, n, hp in spawns:
        if t == f: rats.append(U(n, 1330, hp, 'rat', 72 if n == 'rat_basic' else 74, 10, 10))
    fc = front(cats, 'cat')
    # rats walk until touching the front cat or the rat ahead
    for r in sorted([r for r in rats if r.hp > 0], key=lambda r: r.x):
        ahead = [o for o in rats if o.hp > 0 and o.x < r.x]
        stop = (max(o.x for o in ahead) + 125) if ahead else (fc.x + fc.w/2 + r.w/2 - 10)
        if r.x > stop: r.x = max(stop, r.x-10)
    fr = front(rats, 'rat')
    for u in cats + rats:
        u.flash = max(0, u.flash-1); u.lunge = max(0, u.lunge-1); u.cd -= 1
    if fr and fc:
        touching = fr.x - fc.x <= fc.w/2 + fr.w/2
        for c in cats:
            if c.hp <= 0 or not c.dmg or c.cd > 0: continue
            if c is fc and touching: hit(fr, c.dmg); c.cd = c.rate; c.lunge = 4
            elif c.ranged and fr.x < 1150: bullets.append([c.x+60, G-75, fr]); c.cd = c.rate
        if touching and fr.cd <= 0:
            # rats only bite hard until the heal happens, so the clip shows both taps
            hit(fc, fr.dmg if script['heal'] is None or fc.hp > 35 else 2); fr.cd = fr.rate; fr.lunge = 4
    for b in bullets[:]:
        b[0] += 28
        if b[2].hp <= 0: bullets.remove(b)
        elif b[0] >= b[2].x - 20: hit(b[2], 3); bullets.remove(b)
    for r in rats:
        if r.hp <= 0 and not getattr(r, 'paid', 0): r.paid = 1; coins_n += 5
    # scripted taps
    cool = cats[0]
    if script['tap1'] is None and cool.hp <= 30: script['tap1'] = f
    if script['tap1'] is not None and script['heal'] is None and f == script['tap1'] + 14:
        script['heal'] = f; cool.hp = min(cool.max, cool.hp + cool.max//2); nurse_left = 0
        pops.append([cool.x, G-cool.h-50, '+50 hp', 18])
    if script['heal'] is not None and script['tap2'] is None and f >= script['heal'] + 20 and cool.hp <= 35: script['tap2'] = f

    if os.environ.get('DBG'):
        if f % 15 == 0: print(f, [u.hp for u in cats], [(round(r.x), r.hp) for r in rats if r.hp > 0])
        continue
    # ---- draw
    c = Image.new('RGBA', (W, H), 'white'); d = ImageDraw.Draw(c)
    rnd.seed(f//3)  # keep the hand-drawn wobble steady between frames
    top_bar(c, d, f'{coins_n:,}'); text(d, (W/2, 40), 'LEVEL 2', 40)
    left = sum(1 for r in rats if r.hp > 0) + sum(1 for t, *_ in spawns if t > f)
    text(d, (W/2, 85), f'Rats left: {left}', 26)
    ni = spr('cat_nurse', h=44); c.alpha_composite(ni, (150, 80)); text(d, (225, 104), f'Heals left: {nurse_left}', 26, 'lm')
    ground(d, G)
    for u in cats + rats:
        if u.hp <= 0: continue
        bob = abs(math.sin((f + u.x) / 3)) * 5 if u.side == 'rat' and u.x > (front(cats, 'cat').x + 150) else 0
        dx = (10 if u.side == 'cat' else -10) if u.lunge else 0
        im = u.red if u.flash else u.im
        put(c, im, u.x + dx, G - bob)
        hp_bar(d, u.x, G - u.h - 22, u.hp/u.max, 80 if u.side == 'cat' else 60, 12 if u.side == 'cat' else 9)
    for b in bullets: d.ellipse([b[0]-5, b[1]-5, b[0]+5, b[1]+5], fill=INK)
    for p in pops[:]:
        text(d, (p[0], p[1]), p[2], 30); p[1] -= 3; p[3] -= 1
        if p[3] <= 0: pops.remove(p)
    cool = cats[0]
    def tap(cx, cy, k):  # finger tap: shrinking ring + dot
        circle(d, cx, cy, 34 - k*3, 3); d.ellipse([cx-9, cy-9, cx+9, cy+9], fill=INK)
    if script['tap1'] is not None and script['heal'] is None:
        k = f - script['tap1']
        if k < 6: tap(cool.x, G-60, k)
        if k >= 4:  # heal button over the cat
            bx, by = cool.x, G - cool.h - 75
            box(d, bx-70, by-26, bx+70, by+26, 4, fill='white'); text(d, (bx+14, by), 'HEAL', 34)
            c.alpha_composite(spr('cat_nurse', h=34), (round(bx-64), by-17))
            if k >= 10: tap(bx, by, k-10)
    if script['heal'] is not None and f - script['heal'] < 12:
        for i in range(5):
            a = i*1.3 + f*0.4; text(d, (cool.x + 60*math.cos(a), G-70 + 50*math.sin(a) - (f-script['heal'])*3), '+', 36)
    if script['tap2'] is not None and f - script['tap2'] < 16:
        tap(cool.x, G-60, min(f - script['tap2'], 6)); box(d, cool.x-95, G-cool.h-135, cool.x+95, G-cool.h-90, 3, fill='white'); text(d, (cool.x, G - cool.h - 112), 'No heals left', 30)
    if left == 0:
        box(d, 390, 230, 890, 380, 5, fill='white'); text(d, (W/2, 285), 'LEVEL CLEAR!', 60)
        c.alpha_composite(spr('cat_coin', h=40), (548, 320)); text(d, (600, 340), '+100 coins', 36, 'lm')
    text(d, (W/2, 650), 'Cats fight on their own.  Tap a hurt cat to use a Nurse heal.', 30)
    frames.append(c.convert('RGB').resize((800, 450), Image.LANCZOS))
    if left == 0 and len([x for x in frames]) > f and f > 0:
        if not hasattr(U, 'end'): U.end = f
        if f - U.end > 30: break

print('frames', len(frames), script)
pal = [fr.quantize(32, method=Image.Quantize.MEDIANCUT) for fr in frames]
pal[0].save(f'{OUT}/auto-battle.gif', save_all=True, append_images=pal[1:], duration=60, loop=0, optimize=True)
for i, k in enumerate([script['tap1'] + 8, script['heal'] + 3, script['tap2'] + 4]):
    frames[k].save(f'{OUT}/still-{i+1}.png')
