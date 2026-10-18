# Animated mockup: team formation battle. Melee cats in the front line, ranged cats and Nurse behind,
# rats arrive in groups on several rows. Built from mock.py helpers and Jason's sprites.
import os, math
D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, 'mock.py')).read().split('# 1. Main page')[0])
OUT = os.path.join(D, '..', 'design', 'formation'); os.makedirs(OUT, exist_ok=True)
FPS = 14
ROWS = [340, 450, 560]            # ground line of each row, back to front
SCALE = {340: 0.82, 450: 0.92, 560: 1.02}

class Unit:
    def __init__(s, name, x, y, hp, h):
        s.name, s.x, s.y, s.hp, s.max = name, x, y, hp, hp
        sc = SCALE.get(y, 1); s.h = round(h*sc); s.im = spr(name, h=s.h); s.red = spr(name, h=s.h, red=True)
        s.flash = 0; s.cd = 0; s.lunge = 0; s.state = None; s.t = 0; s.target = None; s.flee = False

# Team of 5: melee in front (x 470), ranged + Nurse behind (x 240)
cats = {'cat': Unit('cat_cat', 480, 395, 100, 115), 'rizz': Unit('cat_rizz', 480, 560, 100, 115),
        'daisy': Unit('cat_daisy', 250, 340, 70, 125), 'water': Unit('cat_water', 250, 450, 70, 110),
        'nurse': Unit('cat_nurse', 250, 560, 70, 110)}
SCALE[395] = 0.87; cats['cat'] = Unit('cat_cat', 480, 395, 100, 115)
rats = []
waves = [(0, [(340, 'rat_basic'), (450, 'rat_ball'), (560, 'rat_basic')]),
         (25, [(395, 'rat_basic'), (500, 'rat_basic')]),
         (55, [(340, 'rat_ball'), (450, 'rat_basic'), (560, 'rat_ball')]),
         (90, [(395, 'rat_ball'), (500, 'rat_basic'), (560, 'rat_basic')])]
for y in (500,): SCALE[y] = 0.97
pops, shots, fans = [], [], []
nurse_left, coins_n = 1, 1265
script = {'tap1': None, 'heal': None}
frames = []

def alive_rats(): return [r for r in rats if r.hp > 0 and not r.flee]
def hit(u, n, tag=None):
    u.hp = max(0, u.hp - n); u.flash = 4
    pops[:] = [p for p in pops if p[4] is not u]  # one number per unit at a time
    pops.append([u.x + 20, u.y - u.h - 18, f'-{n}', 10, u])

end_at = None
for f in range(600):
    for t, group in waves:
        if t == f:
            for i, (y, n) in enumerate(group): rats.append(Unit(n, 1330 + i*40, y, 30 if n == 'rat_basic' else 45, 60))
    front = [cats['cat'], cats['rizz']]
    # rats walk left until they reach the front line (or the rat ahead in their row)
    for r in sorted(alive_rats(), key=lambda r: r.x):
        stop = 480 + 120
        ahead = [o for o in alive_rats() if o is not r and abs(o.y - r.y) < 30 and o.x < r.x]
        if ahead: stop = max(stop, max(o.x for o in ahead) + 110)
        if r.state != 'stared' and r.x > stop: r.x = max(stop, r.x - 8)
    for r in rats:
        if r.flee: r.x += 16
    for u in list(cats.values()) + rats: u.flash = max(0, u.flash-1); u.lunge = max(0, u.lunge-1); u.cd -= 1
    ar = alive_rats()
    near = lambda c: min(ar, key=lambda r: abs(r.x - c.x) + 2*abs(r.y - c.y)) if ar else None
    # front: Cat scratches the closest rat in reach
    c = cats['cat']; r = near(c)
    if r and r.x - c.x < 150 and abs(r.y - c.y) < 70 and c.cd <= 0: hit(r, 5); c.cd = 7; c.lunge = 3; c.target = r
    # front: Rizz stares at one rat for 4 s, then it runs away (counts as defeated)
    c = cats['rizz']
    if c.state is None:
        r = near(c)
        if r and r.x - c.x < 160 and abs(r.y - c.y) < 70: c.state, c.t, c.target = 'stare', 0, r; r.state = 'stared'
    elif c.state == 'stare':
        c.t += 1
        if c.target.hp <= 0: c.state = None
        elif c.t >= 4*FPS: c.target.flee = True; c.target.hp = 0; pops.append([c.target.x, c.target.y-90, 'ran away!', 16, None]); c.state = None
    # back: Daisy flings petals nonstop at the nearest rat
    c = cats['daisy']; r = near(c)
    if r and c.cd <= 0 and r.x < 1200: shots.append(['petal', c.x + 20, c.y - c.h + 15, r]); c.cd = 3
    # back: Water sprays a fan of straight lines, farther rats take less
    c = cats['water']; r = near(c)
    if r and c.cd <= 0 and r.x < 1150:
        mx, my = c.x + 15, c.y - c.h*0.57; ang = math.atan2(r.y - 25 - my, r.x - mx); fans.append([mx, my, ang, 6]); c.cd = FPS
        for o in ar:
            a2 = math.atan2(o.y - 25 - my, o.x - mx); dist = math.hypot(o.x - mx, o.y - my)
            if abs(a2 - ang) < 0.12 and dist < 900: hit(o, 6 if dist < 450 else 4 if dist < 650 else 2)
    # rats bite the front cats they touch
    for r in alive_rats():
        tgt = min(front, key=lambda c: abs(c.y - r.y))
        if r.x - tgt.x <= 125 and r.cd <= 0 and r.state != 'stared':
            hit(tgt, 6 if tgt is cats['cat'] else 2); r.cd = 10; r.lunge = 3
    for s in shots[:]:
        _, x, y, r = s; tx, ty = r.x - 20, r.y - 25; dx, dy = tx - x, ty - y; dd = math.hypot(dx, dy)
        if r.hp <= 0 or r.flee: shots.remove(s); continue
        if dd < 26: hit(r, 2); shots.remove(s)
        else: s[1] += dx/dd*26; s[2] += dy/dd*26
    for fn in fans[:]:
        fn[3] -= 1
        if fn[3] <= 0: fans.remove(fn)
    for r in rats:
        if r.hp <= 0 and not getattr(r, 'paid', 0): r.paid = 1; coins_n += 5
    # scripted taps: Cat gets low, player taps it, HEAL button on its head
    cc = cats['cat']
    if script['tap1'] is None and cc.hp <= 40: script['tap1'] = f
    if script['tap1'] is not None and script['heal'] is None and f == script['tap1'] + 14:
        script['heal'] = f; cc.hp = min(cc.max, cc.hp + cc.max//2); nurse_left = 0; pops.append([cc.x, cc.y - cc.h - 40, '+50% hp', 18, None])
    if script['heal'] is not None and cc.hp < 30: cc.hp = 30  # keep the demo cat alive

    # ---- draw
    cv = Image.new('RGBA', (W, H), 'white'); d = ImageDraw.Draw(cv); rnd.seed(f//3)
    top_bar(cv, d, f'{coins_n:,}'); text(d, (W/2, 40), 'LEVEL 3', 40)
    left = len(alive_rats()) + sum(len(g) for t, g in waves if t > f); text(d, (W/2, 85), f'Rats left: {left}', 26)
    c.alpha_composite if False else None
    cv.alpha_composite(spr('cat_nurse', h=44), (150, 80)); text(d, (225, 104), f'Heals left: {nurse_left}', 26, 'lm')
    # battlefield floor: back edge, front edge, faint row marks
    line(d, [(40, 285), (1240, 285)], 2, 1); line(d, [(10, 600), (1270, 600)], 4, 1.5)
    for y in (395, 505):
        for x in range(60, 1240, 160): line(d, [(x, y), (x + 50, y)], 2, 0.6)
    text(d, (480, 625), 'FRONT: melee', 24); text(d, (250, 625), 'BACK: ranged + Nurse', 24)
    units = [u for u in list(cats.values()) if True] + [r for r in rats if r.hp > 0 or r.flee]
    for u in sorted(units, key=lambda u: u.y):
        if u.flee and u.x > W + 80: continue
        is_cat = u in cats.values()
        dx = (8 if is_cat else -8) if u.lunge else 0
        im = u.red if u.flash else u.im
        if u.flee: im = u.im.transpose(Image.FLIP_LEFT_RIGHT)
        put(cv, im, u.x + dx, u.y)
        if not u.flee: hp_bar(d, u.x, u.y - u.h - 14, u.hp/u.max, 70 if is_cat else 50, 10 if is_cat else 8)
    # effects
    cc = cats['cat']
    if cc.lunge and cc.target and cc.target.hp > 0:
        r = cc.target
        for i in range(3): line(d, [(r.x - 30 + i*10, r.y - 50), (r.x - 42 + i*10, r.y - 15)], 3, 0.4)
    rz = cats['rizz']
    if rz.state == 'stare':
        r = rz.target; text(d, (r.x, r.y - 95), f'{4 - rz.t//FPS}', 30)
        if f % 10 < 5: text(d, (rz.x + 55, rz.y - rz.h + 10), '...', 30)
    for s in shots: d.ellipse([s[1]-9, s[2]-5, s[1]+9, s[2]+5], fill='white', outline=INK, width=2)
    for mx, my, ang, life in fans:
        L = 520
        for da in (-0.09, -0.03, 0.03, 0.09):
            a = ang + da
            for i in range(9):
                t0 = (i + (life % 2)*0.5)/9; t1 = t0 + 0.75/9
                if t1 > 1: continue
                p0 = (mx + L*t0*math.cos(a), my + L*t0*math.sin(a)); p1 = (mx + L*t1*math.cos(a), my + L*t1*math.sin(a))
                if p1[1] < 600: d.line([p0, p1], fill=INK, width=3)
    for p in pops[:]:
        text(d, (p[0], p[1]), p[2], 24); p[1] -= 2; p[3] -= 1
        if p[3] <= 0: pops.remove(p)
    def tap(x, y, k): circle(d, x, y, 30 - k*3, 3); d.ellipse([x-8, y-8, x+8, y+8], fill=INK)
    if script['tap1'] is not None and script['heal'] is None:
        k = f - script['tap1']; bx, by = cc.x, cc.y - cc.h - 5
        if k < 6: tap(cc.x, cc.y - 50, k)
        if k >= 4:
            box(d, bx-60, by-22, bx+60, by+22, 4, fill='white'); text(d, (bx+12, by), 'HEAL', 30)
            cv.alpha_composite(spr('cat_nurse', h=30), (round(bx-56), by-15))
            if k >= 10: tap(bx, by, k-10)
    if script['heal'] is not None and f - script['heal'] < 12:
        for i in range(5): a = i*1.3 + f*0.4; text(d, (cc.x + 55*math.cos(a), cc.y - 60 + 45*math.sin(a)), '+', 32)
    if left == 0:
        if end_at is None: end_at = f
        box(d, 390, 200, 890, 340, 5, fill='white'); text(d, (W/2, 250), 'LEVEL CLEAR!', 60)
        cv.alpha_composite(spr('cat_coin', h=40), (548, 285)); text(d, (600, 305), '+200 coins', 36, 'lm')
    text(d, (W/2, 680), 'Cats fight on their own.  Tap a hurt cat to use a Nurse heal.', 28)
    frames.append(cv.convert('RGB').resize((960, 540), Image.LANCZOS))
    if end_at is not None and f - end_at > 25: break

print('frames', len(frames), script)
pal = [fr.quantize(32, method=Image.Quantize.MEDIANCUT) for fr in frames]
pal[0].save(f'{OUT}/formation-battle.gif', save_all=True, append_images=pal[1:], duration=1000//FPS, loop=0, optimize=True)
for k in (60, (script['tap1'] or 0) + 8, len(frames) - 1): frames[min(k, len(frames)-1)].save(f'{OUT}/formation-{k}.png')
