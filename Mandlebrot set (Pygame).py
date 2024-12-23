import pygame

pygame.init()
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mandelbrot Set")

def mandelbrot(c, max_iter):
    z = 0
    for i in range(max_iter):
        if abs(z) > 2:
            return i
        z = z*z + c
    return max_iter

max_iter = 100
zoom = 200
x_offset = -WIDTH // 2
y_offset = -HEIGHT // 2
center_x, center_y = -0.5, 0

def screen_to_complex(x, y):
    real = (x + x_offset) / zoom + center_x
    imag = (y + y_offset) / zoom + center_y
    return complex(real, imag)

def get_color(iteration, max_iter):
    if iteration == max_iter:
        return (0, 0, 0)
    color = int(255 * iteration / max_iter)
    return (color, color // 2, color // 3)

def render():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            c = screen_to_complex(x, y)
            iteration = mandelbrot(c, max_iter)
            color = get_color(iteration, max_iter)
            screen.set_at((x, y), color)

running = True
render()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()