import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
COLORS = [
    (0, 255, 255), (255, 165, 0), (0, 0, 255), (255, 255, 0),
    (0, 255, 0), (255, 0, 0), (128, 0, 128)
]
SHAPES = [
    [[1, 1, 1, 1]], [[1, 1, 1], [0, 1, 0]], [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]], [[1, 1], [1, 1]], [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

GRID_WIDTH, GRID_HEIGHT = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE
grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

class Tetrimino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def get_cells(self):
        cells = []
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    cells.append((self.x + j, self.y + i))
        return cells

    def collides(self, dx=0, dy=0):
        for x, y in self.get_cells():
            if x + dx < 0 or x + dx >= GRID_WIDTH or y + dy >= GRID_HEIGHT or grid[y + dy][x + dx] != BLACK:
                return True
        return False

    def lock(self):
        for x, y in self.get_cells():
            grid[y][x] = self.color

def check_lines():
    global grid
    full_lines = [i for i in range(GRID_HEIGHT) if all(grid[i][j] != BLACK for j in range(GRID_WIDTH))]
    for i in full_lines:
        del grid[i]
        grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
    return len(full_lines)

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, GREY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_tetrimino(tetrimino):
    for x, y in tetrimino.get_cells():
        pygame.draw.rect(screen, tetrimino.color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        pygame.draw.rect(screen, GREY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_score(score, level):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))

def main():
    clock = pygame.time.Clock()
    score = 0
    level = 1
    fall_time = 0
    fall_speed = 500
    tetrimino = Tetrimino()

    running = True
    while running:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time > fall_speed:
            fall_time = 0
            if not tetrimino.collides(dy=1):
                tetrimino.y += 1
            else:
                tetrimino.lock()
                lines_cleared = check_lines()
                score += lines_cleared * 10
                if lines_cleared > 0:
                    level += lines_cleared
                    fall_speed = max(100, fall_speed - 10)
                tetrimino = Tetrimino()
                if tetrimino.collides():
                    running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not tetrimino.collides(dx=-1):
                    tetrimino.x -= 1
                elif event.key == pygame.K_RIGHT and not tetrimino.collides(dx=1):
                    tetrimino.x += 1
                elif event.key == pygame.K_DOWN and not tetrimino.collides(dy=1):
                    tetrimino.y += 1
                elif event.key == pygame.K_UP:
                    tetrimino.rotate()
                    if tetrimino.collides():
                        for _ in range(3):
                            tetrimino.rotate()

        draw_grid()
        draw_tetrimino(tetrimino)
        draw_score(score, level)
        pygame.display.flip()

    pygame.quit()
    print("Game Over! Your Score:", score)

if __name__ == "__main__":
    main()
