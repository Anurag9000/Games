import tkinter as tk
import random

WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
BLOCK_SIZE = 30
GRID_WIDTH = WINDOW_WIDTH // BLOCK_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // BLOCK_SIZE
COLORS = ["cyan", "blue", "orange", "yellow", "green", "red", "purple"]
SHAPES = [[[1, 1, 1, 1]], [[1, 1, 1], [0, 1, 0]], [[1, 1, 0], [0, 1, 1]], [[0, 1, 1], [1, 1, 0]], [[1, 1], [1, 1]], [[1, 1, 1], [1, 0, 0]], [[1, 1, 1], [0, 0, 1]]]

root = tk.Tk()
root.title("Tetris")
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
canvas.pack()
grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
score = 0
level = 1
fall_speed = 500

class Tetrimino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        rotated_shape = [list(row) for row in zip(*self.shape[::-1])]
        if not self.collides(rotated_shape):
            self.shape = rotated_shape
        else:
            if not self.collides(rotated_shape, x_offset=-1):
                self.x -= 1
                self.shape = rotated_shape
            elif not self.collides(rotated_shape, x_offset=1):
                self.x += 1
                self.shape = rotated_shape

    def collides(self, shape=None, x_offset=0, y_offset=0):
        shape = shape or self.shape
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    x = self.x + j + x_offset
                    y = self.y + i + y_offset
                    if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or (y >= 0 and grid[y][x]):
                        return True
        return False

    def lock(self):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    grid[self.y + i][self.x + j] = self.color

def check_lines():
    global score, level, fall_speed
    cleared_lines = 0
    for i in range(GRID_HEIGHT - 1, -1, -1):
        if all(grid[i]):
            del grid[i]
            grid.insert(0, [None for _ in range(GRID_WIDTH)])
            cleared_lines += 1
    score += cleared_lines ** 2
    if cleared_lines > 0:
        level += 1
        fall_speed = max(100, fall_speed - 20)

def draw_grid():
    canvas.delete("all")
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = grid[y][x]
            if color:
                canvas.create_rectangle(x * BLOCK_SIZE, y * BLOCK_SIZE, x * BLOCK_SIZE + BLOCK_SIZE, y * BLOCK_SIZE + BLOCK_SIZE, fill=color, outline="black")
    canvas.create_text(10, 10, anchor="nw", text=f"Score: {score}  Level: {level}", fill="white", font=("Arial", 16))

def draw_tetrimino(tetrimino):
    for i, row in enumerate(tetrimino.shape):
        for j, cell in enumerate(row):
            if cell:
                x = (tetrimino.x + j) * BLOCK_SIZE
                y = (tetrimino.y + i) * BLOCK_SIZE
                canvas.create_rectangle(x, y, x + BLOCK_SIZE, y + BLOCK_SIZE, fill=tetrimino.color, outline="black")

def game_loop():
    global tetrimino
    if not tetrimino.collides(y_offset=1):
        tetrimino.y += 1
    else:
        tetrimino.lock()
        check_lines()
        tetrimino = Tetrimino()
        if tetrimino.collides():
            canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="Game Over", fill="red", font=("Arial", 24))
            return
    draw_grid()
    draw_tetrimino(tetrimino)
    root.after(fall_speed, game_loop)

def move_left(event):
    if not tetrimino.collides(x_offset=-1):
        tetrimino.x -= 1
        draw_grid()
        draw_tetrimino(tetrimino)

def move_right(event):
    if not tetrimino.collides(x_offset=1):
        tetrimino.x += 1
        draw_grid()
        draw_tetrimino(tetrimino)

def move_down(event):
    if not tetrimino.collides(y_offset=1):
        tetrimino.y += 1
        draw_grid()
        draw_tetrimino(tetrimino)

def rotate(event):
    tetrimino.rotate()
    draw_grid()
    draw_tetrimino(tetrimino)

root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<Down>", move_down)
root.bind("<Up>", rotate)
tetrimino = Tetrimino()
game_loop()
root.mainloop()
