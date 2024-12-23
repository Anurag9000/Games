import tkinter as tk
import random
from time import time

WIDTH, HEIGHT = 800, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
BULLET_WIDTH, BULLET_HEIGHT = 10, 5
BULLET_SPEED = 5
FIRE_RATE = 0.5

player1_hp = 100
player2_hp = 100
player1_wins = 0
player2_wins = 0
player1_x, player1_y = 50, HEIGHT // 2 - PLAYER_HEIGHT // 2
player2_x, player2_y = WIDTH - 50 - PLAYER_WIDTH, HEIGHT // 2 - PLAYER_HEIGHT // 2
bullets_left = []
bullets_right = []

player1_last_fire = time()
player2_last_fire = time()

root = tk.Tk()
root.title("Shooter")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

player1_up = input("Enter the key to move Player 1 (left object) up: ").lower()
player1_down = input("Enter the key to move Player 1 (left object) down: ").lower()
player2_up = input("Enter the key to move Player 2 (right object) up: ").lower()
player2_down = input("Enter the key to move Player 2 (right object) down: ").lower()
player1_name = input("Enter Player 1's name: ")
player2_name = input("Enter Player 2's name: ")

keys_pressed = set()

def draw_objects():
    canvas.delete("all")
    canvas.create_rectangle(player1_x, player1_y, player1_x + PLAYER_WIDTH, player1_y + PLAYER_HEIGHT, fill="blue")
    canvas.create_rectangle(player2_x, player2_y, player2_x + PLAYER_WIDTH, player2_y + PLAYER_HEIGHT, fill="red")
    for bullet in bullets_left:
        canvas.create_rectangle(bullet[0], bullet[1], bullet[0] + BULLET_WIDTH, bullet[1] + BULLET_HEIGHT, fill="white")
    for bullet in bullets_right:
        canvas.create_rectangle(bullet[0], bullet[1], bullet[0] + BULLET_WIDTH, bullet[1] + BULLET_HEIGHT, fill="white")
    canvas.create_text(100, 20, text=f"{player1_name} HP: {player1_hp}", fill="white", font=("Arial", 16))
    canvas.create_text(700, 20, text=f"{player2_name} HP: {player2_hp}", fill="white", font=("Arial", 16))
    canvas.create_text(100, 50, text=f"Wins: {player1_wins}", fill="white", font=("Arial", 16))
    canvas.create_text(700, 50, text=f"Wins: {player2_wins}", fill="white", font=("Arial", 16))

def move_players():
    global player1_y, player2_y
    if player1_up in keys_pressed and player1_y > 0:
        player1_y -= 5
    if player1_down in keys_pressed and player1_y < HEIGHT - PLAYER_HEIGHT:
        player1_y += 5
    if player2_up in keys_pressed and player2_y > 0:
        player2_y -= 5
    if player2_down in keys_pressed and player2_y < HEIGHT - PLAYER_HEIGHT:
        player2_y += 5

def fire_bullets():
    global player1_last_fire, player2_last_fire
    current_time = time()
    if current_time - player1_last_fire > FIRE_RATE:
        bullets_left.append([player1_x + PLAYER_WIDTH, player1_y + PLAYER_HEIGHT // 2])
        player1_last_fire = current_time
    if current_time - player2_last_fire > FIRE_RATE:
        bullets_right.append([player2_x - BULLET_WIDTH, player2_y + PLAYER_HEIGHT // 2])
        player2_last_fire = current_time

def move_bullets():
    global bullets_left, bullets_right, player1_hp, player2_hp
    for bullet in bullets_left[:]:
        bullet[0] += BULLET_SPEED
        if bullet[0] > WIDTH:
            bullets_left.remove(bullet)
        elif player2_x < bullet[0] < player2_x + PLAYER_WIDTH and player2_y < bullet[1] < player2_y + PLAYER_HEIGHT:
            player2_hp -= 1
            bullets_left.remove(bullet)
    for bullet in bullets_right[:]:
        bullet[0] -= BULLET_SPEED
        if bullet[0] < 0:
            bullets_right.remove(bullet)
        elif player1_x < bullet[0] < player1_x + PLAYER_WIDTH and player1_y < bullet[1] < player1_y + PLAYER_HEIGHT:
            player1_hp -= 1
            bullets_right.remove(bullet)

def check_winner():
    global player1_hp, player2_hp, player1_wins, player2_wins, player1_hp, player2_hp
    if player1_hp <= 0:
        player2_wins += 1
        reset_game()
    elif player2_hp <= 0:
        player1_wins += 1
        reset_game()

def reset_game():
    global player1_hp, player2_hp, bullets_left, bullets_right
    player1_hp = 100
    player2_hp = 100
    bullets_left = []
    bullets_right = []

def key_press(event):
    keys_pressed.add(event.keysym.lower())

def key_release(event):
    keys_pressed.discard(event.keysym.lower())

def game_loop():
    move_players()
    fire_bullets()
    move_bullets()
    check_winner()
    draw_objects()
    root.after(16, game_loop)

canvas.bind_all("<KeyPress>", key_press)
canvas.bind_all("<KeyRelease>", key_release)
game_loop()
root.mainloop()
