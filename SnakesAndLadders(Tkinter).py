import tkinter as tk
import random

BLOCK_SIZE = 60
BOARD_SIZE = 10
WINDOW_SIZE = BLOCK_SIZE * BOARD_SIZE
PLAYER_COLORS = ["red", "green", "blue", "purple", "orange", "cyan"]
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

class Player:
    def __init__(self, color):
        self.color = color
        self.position = 1
    def move(self, steps):
        self.position += steps
        if self.position > 100:
            self.position = 100 - (self.position - 100)
        if self.position in snakes:
            self.position = snakes[self.position]
        elif self.position in ladders:
            self.position = ladders[self.position]

def draw_board(canvas):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x1 = col * BLOCK_SIZE
            y1 = (BOARD_SIZE - row - 1) * BLOCK_SIZE
            x2 = x1 + BLOCK_SIZE
            y2 = y1 + BLOCK_SIZE
            square_num = row * BOARD_SIZE + (col + 1) if row % 2 == 0 else row * BOARD_SIZE + (BOARD_SIZE - col)
            color = "yellow" if (row + col) % 2 == 0 else "blue"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            canvas.create_text(x1 + 10, y1 + 10, text=str(square_num), anchor="nw")
    for start, end in snakes.items():
        draw_snake_ladder(canvas, start, end, "red")
    for start, end in ladders.items():
        draw_snake_ladder(canvas, start, end, "green")

def draw_snake_ladder(canvas, start, end, color):
    x1, y1 = get_position(start)
    x2, y2 = get_position(end)
    canvas.create_line(x1, y1, x2, y2, fill=color, width=3)

def get_position(square):
    row, col = divmod(square - 1, BOARD_SIZE)
    row = BOARD_SIZE - row - 1
    col = col if (BOARD_SIZE - row - 1) % 2 == 0 else BOARD_SIZE - col - 1
    x = col * BLOCK_SIZE + BLOCK_SIZE // 2
    y = row * BLOCK_SIZE + BLOCK_SIZE // 2
    return x, y

def draw_player(canvas, position, color):
    x, y = get_position(position)
    canvas.create_oval(x - BLOCK_SIZE // 4, y - BLOCK_SIZE // 4, x + BLOCK_SIZE // 4, y + BLOCK_SIZE // 4, fill=color, tags="player")

def roll_dice():
    return random.randint(1, 6)

def start_game(canvas, player_entry, dice_label, result_label, roll_button):
    num_players = min(int(player_entry.get()), 6)
    players = [Player(PLAYER_COLORS[i]) for i in range(num_players)]
    current_player_idx = 0

    def roll():
        nonlocal current_player_idx
        dice_roll = roll_dice()
        dice_label.config(text=f"Dice Roll: {dice_roll}")
        players[current_player_idx].move(dice_roll)
        if players[current_player_idx].position == 100:
            result_label.config(text=f"Player {current_player_idx + 1} wins!")
            roll_button.config(state=tk.DISABLED)
        current_player_idx = (current_player_idx + 1) % num_players
        update_board()

    def update_board():
        canvas.delete("player")
        for i, player in enumerate(players):
            draw_player(canvas, player.position, player.color)

    roll_button.config(state=tk.NORMAL, command=roll)
    result_label.config(text="")
    update_board()

def main():
    root = tk.Tk()
    root.title("Snakes and Ladders")
    canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE, bg="white")
    canvas.pack()
    draw_board(canvas)
    control_frame = tk.Frame(root)
    control_frame.pack()
    tk.Label(control_frame, text="Number of Players (up to 6):").grid(row=0, column=0)
    player_entry = tk.Entry(control_frame)
    player_entry.grid(row=0, column=1)
    dice_label = tk.Label(root, text="Dice Roll: ")
    dice_label.pack()
    result_label = tk.Label(root, text="")
    result_label.pack()
    roll_button = tk.Button(root, text="Roll Dice", state=tk.DISABLED)
    roll_button.pack()
    start_button = tk.Button(control_frame, text="Start Game", command=lambda: start_game(canvas, player_entry, dice_label, result_label, roll_button))
    start_button.grid(row=0, column=2)
    root.mainloop()

main()
