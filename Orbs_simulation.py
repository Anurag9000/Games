import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbs Simulation")
clock = pygame.time.Clock()

try:
    n_clusters = int(input("Enter number of clusters: "))
    k_orbs = int(input("Enter number of orbs per cluster: "))
except Exception as e:
    print("Invalid input, using defaults: n=3, k=10")
    n_clusters = 3
    k_orbs = 10

class Orb:
    def __init__(self, x, y, color):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acc = pygame.math.Vector2(0, 0)
        self.size = 5
        self.color = color
    def update(self):
        self.vel += self.acc
        speed_limit = 4
        if self.vel.length() > speed_limit:
            self.vel.scale_to_length(speed_limit)
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
    def apply_force(self, force):
        self.acc += force
    def draw(self, surface):
        rect = pygame.Rect(int(self.pos.x), int(self.pos.y), self.size, self.size)
        pygame.draw.rect(surface, self.color, rect)

clusters = []
for i in range(n_clusters):
    cluster_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    cluster_center = pygame.math.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
    orbs = []
    for j in range(k_orbs):
        offset = pygame.math.Vector2(random.uniform(-50, 50), random.uniform(-50, 50))
        orb = Orb(cluster_center.x + offset.x, cluster_center.y + offset.y, cluster_color)
        orbs.append(orb)
    clusters.append(orbs)

cohesion_factor = 0.005
separation_factor = 0.05
separation_distance = 20

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for orbs in clusters:
        cluster_center = pygame.math.Vector2(0, 0)
        for orb in orbs:
            cluster_center += orb.pos
        cluster_center /= len(orbs)
        for orb in orbs:
            cohesion_force = (cluster_center - orb.pos) * cohesion_factor
            separation_force = pygame.math.Vector2(0, 0)
            for other in orbs:
                if other != orb:
                    distance = orb.pos.distance_to(other.pos)
                    if distance < separation_distance and distance > 0:
                        diff = orb.pos - other.pos
                        diff /= distance
                        separation_force += diff
            separation_force *= separation_factor
            total_force = cohesion_force + separation_force
            orb.apply_force(total_force)
            orb.update()
    screen.fill((0, 0, 0))
    for orbs in clusters:
        for orb in orbs:
            orb.draw(screen)
    pygame.display.flip()
pygame.quit()
sys.exit()
