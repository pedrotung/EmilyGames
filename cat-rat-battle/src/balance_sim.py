# Rough balance simulation for Meow Brigade: auto battle in 0.1 s steps, prints how much team HP is left.
import random, sys, statistics
DT = 0.1
# cat: hp, dps (damage per second averaged over cooldown), role, special
CATS = {
 # Common: about 2 damage per second
 'cat':   dict(hp=100, dps=5/2, role='front'),
 'cool':  dict(hp=70, dps=5/2.5, role='back'),
 'bad':   dict(hp=70, dps=10/5, role='back'),
 'gent':  dict(hp=80, dps=6/3, role='back'),
 'daisy': dict(hp=60, dps=2/1, role='back'),
 'alert': dict(hp=80, dps=0, role='back', shield=True),
 # Rare: about 5, or a special
 'rizz':  dict(hp=130, dps=0, role='front', rizz=True),
 'bleh':  dict(hp=130, dps=0, role='front', bleh=True),
 'water': dict(hp=90, dps=4/1.5, role='back', splash=2),
 'ghost': dict(hp=130, dps=6, role='front', dodge=0.7),
 'nurse': dict(hp=90, dps=0, role='back', heal=True),
 # Epic: about 8
 'senpai': dict(hp=160, dps=8/1, role='front'),
 'catkid': dict(hp=160, dps=20/2.5 , role='front', selfhurt=2/2.5),
 'catcat': dict(hp=115, dps=22/2.5*0.9, role='back'),
 'poison': dict(hp=115, dps=4*8/12, role='back', splash=3),
 # Legendary: about 13
 'fairy':  dict(hp=140, dps=10/0.75, role='back'),
 'military': dict(hp=140, dps=3*4.5, role='back'),
 'witch':  dict(hp=140, dps=15/3, role='back', splash=3),
}
RATS = {'basic': dict(hp=20, dps=2), 'ball': dict(hp=30, dps=2, splash=2), 'spike': dict(hp=35, dps=3)}
BOSSES = {1: dict(hp=100, dps=5, summon=10), 2: dict(hp=150, dps=5, slam=(8, 6)), 3: dict(hp=200, dps=6, fakes=12),
          4: dict(hp=500, dps=12/4, back=12/4), 5: dict(hp=500, dps=9, heal=30)}
LEVELS = {1: ['basic']*6, 2: ['basic']*6+['ball']*3, 3: ['basic']*8+['ball']*4, 4: ['basic']*8+['ball']*6, 5: ['ball']*8+['spike']*6}
GAP = 3.5  # seconds between rats arriving
PER_CAT = 2  # how many rats can reach one front cat at the same time

def run(level, team, rat_mult=1.0, cat_mult=1.0, seed=0):
    rnd = random.Random(seed)
    cats = [dict(name=n, **CATS[n]) for n in team]
    for c in cats: c['hp'] *= cat_mult; c['max'] = c['hp']; c['cd'] = 0
    heals = sum(1 for c in cats if c.get('heal'))
    hpm = rat_mult * (1.1 ** (level-1))
    queue = [dict(kind=k, hp=RATS[k]['hp']*hpm, dps=RATS[k]['dps']*hpm, splash=RATS[k].get('splash', 1)) for k in LEVELS[level]]
    rnd.shuffle(queue)
    b = BOSSES[level]; boss = dict(kind='boss', hp=b['hp']*rat_mult, dps=b['dps']*rat_mult, splash=1, boss=True)
    t = 0; next_t = 0; field = []; boss_in = False; shield = 0; slam_t = 0; summon_t = 0
    while t < 400:
        if queue and t >= next_t: field.append(queue.pop(0)); next_t = t + GAP
        if not queue and not boss_in and not field: field.append(boss); boss_in = True
        alive = [c for c in cats if c['hp'] > 0]
        if not alive: return 0, t
        if boss_in and boss['hp'] <= 0 and not field: return sum(c['hp'] for c in cats)/sum(c['max'] for c in cats), t
        front = [c for c in alive if c['role'] == 'front'] or alive
        # cats attack
        for c in alive:
            if not field: break
            tgt = field[0]
            if c.get('rizz'):
                c['cd'] -= DT
                if c['cd'] <= 0:
                    nb = [r for r in field if not r.get('boss')]
                    if nb: nb[0]['hp'] = 0; c['cd'] = 4
            elif c.get('bleh'):
                c['cd'] -= DT
                if c['cd'] <= 0:
                    nb = [r for r in field if not r.get('boss')]
                    if nb: nb[0]['hp'] = 0
                    else: tgt['hp'] -= 30
                    c['cd'] = 8
            else:
                n = c.get('splash', 1)
                for r in field[:n]: r['hp'] -= c['dps']*DT
                if c.get('selfhurt'): c['hp'] -= c['selfhurt']*DT
        field = [r for r in field if r['hp'] > 0]
        # rats attack front cats, at most PER_CAT rats per front cat
        if shield > 0: shield -= DT
        attackers = field[:PER_CAT*len(front)]
        for i, r in enumerate(attackers):
            if shield > 0: break
            tgt = front[i % len(front)]
            dmg = r['dps']*DT
            if tgt.get('dodge') and rnd.random() < tgt['dodge']: dmg = 0
            tgt['hp'] -= dmg
            if r.get('splash', 1) > 1 and len(front) > 1: front[(i+1) % len(front)]['hp'] -= dmg
        if boss_in and boss['hp'] > 0:
            if b.get('back'):
                backs = [c for c in alive if c['role'] == 'back'] or alive
                rnd.choice(backs)['hp'] -= b['back']*DT
            if b.get('slam'):
                slam_t += DT
                if slam_t >= b['slam'][0]: slam_t = 0; [c.__setitem__('hp', c['hp'] - b['slam'][1]) for c in front]
            if b.get('summon'):
                summon_t += DT
                if summon_t >= b['summon']: summon_t = 0; field += [dict(kind='basic', hp=RATS['basic']['hp'], dps=RATS['basic']['dps'], splash=1) for _ in range(2)]
            if b.get('heal'): boss['hp'] += b['heal']/20*DT
            if any(c.get('shield') for c in alive) and rnd.random() < 0.08*DT/5*5: shield = 5
        # player taps Nurse heal when a cat falls under 30%
        for c in alive:
            if heals and c['hp'] < 0.3*c['max']: c['hp'] = min(c['max'], c['hp'] + c['max']/2); heals -= 1
        t += DT
    return 0, t

if __name__ == '__main__':
    teams = [(1, ['cat', 'cool', 'daisy']), (2, ['cat', 'bad', 'cool', 'daisy']), (3, ['cat', 'rizz', 'cool', 'daisy', 'nurse']),
             (4, ['cat', 'bleh', 'water', 'ghost', 'nurse']), (5, ['cat', 'bleh', 'water', 'ghost', 'nurse']),
             (5, ['catkid', 'bleh', 'water', 'ghost', 'nurse']), (5, ['catkid', 'senpai', 'bleh', 'poison', 'nurse']),
             (5, ['catkid', 'bleh', 'water', 'fairy', 'nurse']), (5, ['catkid', 'ghost', 'water', 'military', 'nurse'])]
    for lv, tm in teams:
        res = [run(lv, tm, seed=s) for s in range(30)]
        win = sum(1 for r, _ in res if r > 0)/len(res)
        left = statistics.mean(r for r, _ in res)
        print(f'L{lv} team {tm}: win {win:.0%}, team HP left {left:.0%}, time {statistics.mean(t for _, t in res):.0f}s')
    print('solo Cat on L1:', run(1, ['cat'])[0])
