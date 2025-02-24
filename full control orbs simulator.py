import pygame
import sys
import random
import tkinter as tk

b_cohesion = 0.005 * 0.05
b_separation = 0.5 * 0.05
b_sepdist = 200 * 0.05
b_ggrav = 0.1 * 0.05
b_grep = 2 * 0.05
b_frot = 500 * 0.05
b_eradius = 200 * 0.05
b_speedlim = 4 * 0.05

root = tk.Tk()
root.geometry("400x600+0+0")
root.title("Adjustments")

cohesion_scale = tk.Scale(root, from_=0, to=100, orient="horizontal", resolution=0.1, label="Intercluster Cohesion", length=300)
cohesion_scale.set(1)
cohesion_scale.pack()

separation_scale = tk.Scale(root, from_=0, to=100, orient="horizontal", resolution=0.1, label="Intercluster Repulsion", length=300)
separation_scale.set(1)
separation_scale.pack()

sepdist_scale = tk.Scale(root, from_=0, to=100, orient="horizontal", resolution=0.1, label="Intercluster Repulsive Threshold", length=300)
sepdist_scale.set(1)
sepdist_scale.pack()

grav_scale = tk.Scale(root, from_=0, to=100, orient="horizontal", resolution=0.1, label="Intracluster Cohesion", length=300)
grav_scale.set(1)
grav_scale.pack()

repuls_scale = tk.Scale(root, from_=0, to=100, orient="horizontal", resolution=0.1, label="Intracluster Repulsion", length=300)
repuls_scale.set(1)
repuls_scale.pack()

frot_scale = tk.Scale(root, from_=0, to=100, orient="horizontal", resolution=0.1, label="Spin Force", length=300)
frot_scale.set(1)
frot_scale.pack()

eradius_scale = tk.Scale(root, from_=0, to=100, orient="horizontal", resolution=0.1, label="Effective Spin Radius", length=300)
eradius_scale.set(1)
eradius_scale.pack()

speedlim_scale = tk.Scale(root, from_=0, to=100, orient="horizontal", resolution=0.1, label="Velocity", length=300)
speedlim_scale.set(1)
speedlim_scale.pack()

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floating Orbs Simulation")
clock = pygame.time.Clock()

try:
    n_clusters = int(input("Enter number of clusters: "))
    k_orbs = int(input("Enter number of orbs per cluster: "))
except:
    n_clusters = 3
    k_orbs = 10

class Orb:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acc = pygame.math.Vector2(0, 0)
        self.size = 5

    def update(self, limit):
        self.vel += self.acc
        if self.vel.length() > limit:
            self.vel.scale_to_length(limit)
        self.pos += self.vel
        self.acc *= 0
        if self.pos.x < 0:
            self.pos.x += WIDTH
        if self.pos.x > WIDTH:
            self.pos.x -= WIDTH
        if self.pos.y < 0:
            self.pos.y += HEIGHT
        if self.pos.y > HEIGHT:
            self.pos.y -= HEIGHT

    def apply_force(self, f):
        self.acc += f

    def draw(self, surface, c):
        r = pygame.Rect(int(self.pos.x), int(self.pos.y), self.size, self.size)
        pygame.draw.rect(surface, c, r)

COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255),
    (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0), (128, 0, 128), (0, 128, 128),
    (255, 165, 0), (255, 20, 147), (75, 0, 130), (139, 69, 19), (0, 100, 0), (70, 130, 180),
    (220, 20, 60), (0, 191, 255)
]

class Cluster:
    def __init__(self, orbs, t):
        self.orbs = orbs
        self.type = t
        self.color = COLORS[t]
        self.center = self.calc_center()

    def calc_center(self):
        c = pygame.math.Vector2(0, 0)
        for o in self.orbs:
            c += o.pos
        c /= len(self.orbs)
        return c

    def update_center(self):
        self.center = self.calc_center()

clusters = []
tc = [n_clusters // 20] * 20

for i in range(n_clusters % 20):
    tc[i] += 1

for ti in range(20):
    for _ in range(tc[ti]):
        cc = pygame.math.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        orbs = []
        for _ in range(k_orbs):
            off = pygame.math.Vector2(random.uniform(-50, 50), random.uniform(-50, 50))
            o = Orb(cc.x + off.x, cc.y + off.y)
            orbs.append(o)
        clusters.append(Cluster(orbs, ti))

running = True

while running:
    root.update()

    ccohesion = b_cohesion * cohesion_scale.get()
    cseparation = b_separation * separation_scale.get()
    csepdist = b_sepdist * sepdist_scale.get()
    cggrav = b_ggrav * grav_scale.get()
    cgrep = b_grep * repuls_scale.get()
    cfrot = b_frot * frot_scale.get()
    ceradius = b_eradius * eradius_scale.get()
    cspeedlim = b_speedlim * speedlim_scale.get()

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    for c in clusters:
        c.update_center()

    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            a = clusters[i]
            b = clusters[j]
            same = (a.type == b.type)
            const = cggrav if same else cgrep
            for orb in a.orbs:
                rv = b.center - orb.pos
                r = rv.length() + 0.1
                fm = const * (len(b.orbs)) / (r ** 2)
                f = rv.normalize() * fm if same else -rv.normalize() * fm
                orb.apply_force(f)
            for orb in b.orbs:
                rv = a.center - orb.pos
                r = rv.length() + 0.1
                fm = const * (len(a.orbs)) / (r ** 2)
                f = rv.normalize() * fm if same else -rv.normalize() * fm
                orb.apply_force(f)

    mp = pygame.math.Vector2(pygame.mouse.get_pos())

    for c in clusters:
        cen = c.center
        for o in c.orbs:
            cf = (cen - o.pos) * ccohesion
            sf = pygame.math.Vector2(0, 0)
            for other in c.orbs:
                if other != o:
                    d = o.pos.distance_to(other.pos)
                    if d < csepdist and d > 0:
                        dif = o.pos - other.pos
                        dif /= d
                        sf += dif
            sf *= cseparation
            tf = cf + sf
            rv = o.pos - mp
            d = rv.length()
            if 1 < d < ceradius:
                t = pygame.math.Vector2(rv.y, -rv.x)
                t.normalize_ip()
                sp = t * (cfrot / (d * d))
                tf += sp
            o.apply_force(tf)
            o.update(cspeedlim)

    screen.fill((0, 0, 0))

    for c in clusters:
        for o in c.orbs:
            o.draw(screen, c.color)

    pygame.display.flip()

pygame.quit()
sys.exit()