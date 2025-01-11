import tkinter as tk
import random
from tkinter import messagebox

class ColorGame:
    def __init__(self, root, color_diff_factor):
        self.root = root
        self.root.title("Color Game")

        self.score = 0
        self.grid_size = 4
        self.color_diff = 255
        self.color_diff_factor = color_diff_factor
        self.current_odd_square = None

        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack(anchor="nw", padx=10, pady=5)

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.generate_new_round()

    def generate_new_round(self):
        self.canvas.delete("all")
        base_color = self.get_random_color()
        odd_color = self.get_odd_color(base_color)

        self.odd_square_index = random.randint(0, self.grid_size ** 2 - 1)
        self.squares = []

        square_size = 400 // self.grid_size

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = odd_color if len(self.squares) == self.odd_square_index else base_color
                square_id = self.canvas.create_rectangle(
                    j * square_size,
                    i * square_size,
                    (j + 1) * square_size,
                    (i + 1) * square_size,
                    fill=color,
                    outline="white"
                )
                self.squares.append(square_id)
                self.canvas.tag_bind(square_id, "<Button-1>", self.handle_square_click)

    def get_random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    def get_odd_color(self, base_color):
        r_base, g_base, b_base = int(base_color[1:3], 16), int(base_color[3:5], 16), int(base_color[5:7], 16)

        r_odd = max(0, min(255, r_base + random.choice([-1, 1]) * self.color_diff))
        g_odd = max(0, min(255, g_base + random.choice([-1, 1]) * self.color_diff))
        b_odd = max(0, min(255, b_base + random.choice([-1, 1]) * self.color_diff))

        return f"#{r_odd:02x}{g_odd:02x}{b_odd:02x}"

    def handle_square_click(self, event):
        clicked_square = self.canvas.find_closest(event.x, event.y)[0]
        if clicked_square == self.squares[self.odd_square_index]:
            self.current_odd_square = self.odd_square_index
            self.check_answer()
        else:
            messagebox.showinfo("Game Over", f"Wrong answer! Final score: {self.score}")
            self.root.quit()

    def check_answer(self):
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")
        self.color_diff = max(1, int(self.color_diff * self.color_diff_factor))
        self.generate_new_round()

def show_level_selection():
    def start_game(factor):
        level_selection.destroy()
        root = tk.Tk()
        game = ColorGame(root, factor)
        root.mainloop()

    level_selection = tk.Tk()
    level_selection.title("Select Level")

    title_label = tk.Label(level_selection, text="Pick your poison", font=("Arial", 20, "bold"))
    title_label.pack(pady=10)

    levels = [
        ("Training Grounds", 99 / 100),
        ("Cakewalk", 90 / 100),
        ("Warm-Up", 80 / 100),
        ("Rookie", 70 / 100),
        ("Try-Hard", 60 / 100),
        ("Sweat Mode", 50 / 100),
        ("Challenge Accepted", 40 / 100),
        ("Hardcore", 30 / 100),
        ("Nightmare", 20 / 100),
        ("Immortal Legend", 10 / 100)
    ]

    for level_name, factor in levels:
        button = tk.Button(level_selection, text=level_name, command=lambda f=factor: start_game(f))
        button.pack(pady=5)

    level_selection.mainloop()

if __name__ == "__main__":
    show_level_selection()
