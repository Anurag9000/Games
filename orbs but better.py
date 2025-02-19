import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floating Orbs Simulation")

clock = pygame.time.Clock()

try:
    n_clusters = int(input("Enter number of clusters: "))
    k_orbs = int(input("Enter number of orbs per cluster: "))
except Exception as e:
    print("Invalid input, using defaults: n=3, k=10")
    n_clusters = 3
    k_orbs = 10

class Orb:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acc = pygame.math.Vector2(0, 0)
        self.size = 5

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

    def draw(self, surface, color):
        rect = pygame.Rect(int(self.pos.x), int(self.pos.y), self.size, self.size)
        pygame.draw.rect(surface, color, rect)

COLORS = [
    (255, 0, 0),    
    (0, 255, 0),    
    (0, 0, 255),    
    (255, 255, 0),  
    (255, 0, 255),  
    (0, 255, 255),  
    (128, 0, 0),
    (0, 128, 0),
    (0, 0, 128),
    (128, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (255, 165, 0),  
    (255, 20, 147), 
    (75, 0, 130),   
    (139, 69, 19),  
    (0, 100, 0),    
    (70, 130, 180), 
    (220, 20, 60),  
    (0, 191, 255)   
]

class Cluster:
    def __init__(self, orbs, type_index):
        self.orbs = orbs
        self.type = type_index
        self.color = COLORS[type_index]
        self.center = self.calculate_center()

    def calculate_center(self):
        center = pygame.math.Vector2(0, 0)
        for orb in self.orbs:
            center += orb.pos
        center /= len(self.orbs)
        return center

    def update_center(self):
        self.center = self.calculate_center()

clusters = []
type_counts = [n_clusters // 20] * 20
for i in range(n_clusters % 20):
    type_counts[i] += 1

for type_index in range(20):
    for _ in range(type_counts[type_index]):
        cluster_center = pygame.math.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        orbs = []
        for _ in range(k_orbs):
            offset = pygame.math.Vector2(random.uniform(-50, 50), random.uniform(-50, 50))
            orb = Orb(cluster_center.x + offset.x, cluster_center.y + offset.y)
            orbs.append(orb)
        clusters.append(Cluster(orbs, type_index))

cohesion_factor = 0.005
separation_factor = 0.05
separation_distance = 20

G_GRAVITY = 0.1
G_REPULSIVITY = 0.1

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for cluster in clusters:
        cluster.update_center()

    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            clusterA = clusters[i]
            clusterB = clusters[j]
            same_type = (clusterA.type == clusterB.type)
            constant = G_GRAVITY if same_type else G_REPULSIVITY

            for orb in clusterA.orbs:
                r_vec = clusterB.center - orb.pos
                r = r_vec.length() + 0.1
                force_magnitude = constant * (len(clusterB.orbs)) / (r ** 2)
                if same_type:
                    force = r_vec.normalize() * force_magnitude
                else:
                    force = -r_vec.normalize() * force_magnitude
                orb.apply_force(force)

            for orb in clusterB.orbs:
                r_vec = clusterA.center - orb.pos
                r = r_vec.length() + 0.1
                force_magnitude = constant * (len(clusterA.orbs)) / (r ** 2)
                if same_type:
                    force = r_vec.normalize() * force_magnitude
                else:
                    force = -r_vec.normalize() * force_magnitude
                orb.apply_force(force)

    for cluster in clusters:
        cluster_center = cluster.center
        for orb in cluster.orbs:
            cohesion_force = (cluster_center - orb.pos) * cohesion_factor

            separation_force = pygame.math.Vector2(0, 0)
            for other in cluster.orbs:
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
    for cluster in clusters:
        for orb in cluster.orbs:
            orb.draw(screen, cluster.color)

    pygame.display.flip()

pygame.quit()
sys.exit()
