import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

player1_hp = 100
player2_hp = 100
player1_wins = 0
player2_wins = 0
bullet_speed = 5
fire_rate = 30

object_width, object_height = 50, 50
bullet_width, bullet_height = 10, 5

player1_x, player1_y = 50, HEIGHT // 2 - object_height // 2
player2_x, player2_y = WIDTH - 50 - object_width, HEIGHT // 2 - object_height // 2

bullets_left = []
bullets_right = []

game_started = False
player1_last_fire = pygame.time.get_ticks()
player2_last_fire = pygame.time.get_ticks()

player1_up = input("Enter the key to move Player 1 (left object) up: ").lower()
player1_down = input("Enter the key to move Player 1 (left object) down: ").lower()
player2_up = input("Enter the key to move Player 2 (right object) up: ").lower()
player2_down = input("Enter the key to move Player 2 (right object) down: ").lower()

player1_name = input("Enter Player 1's name: ")
player2_name = input("Enter Player 2's name: ")

def reset_game():
    global player1_hp, player2_hp, bullets_left, bullets_right, fire_rate, game_started, player1_last_fire, player2_last_fire
    player1_hp = 100
    player2_hp = 100
    bullets_left = []
    bullets_right = []
    fire_rate = 30
    game_started = False
    player1_last_fire = pygame.time.get_ticks()
    player2_last_fire = pygame.time.get_ticks()

running = True
winner_message = "Press SPACE or ENTER to start the game."

while running:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                game_started = True

    if not game_started:
        start_text = font.render(winner_message, True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        clock.tick(60)
        continue

    if keys[getattr(pygame, f"K_{player1_up}")] and player1_y > 0:
        player1_y -= 5
    if keys[getattr(pygame, f"K_{player1_down}")] and player1_y < HEIGHT - object_height:
        player1_y += 5

    if keys[getattr(pygame, f"K_{player2_up}")] and player2_y > 0:
        player2_y -= 5
    if keys[getattr(pygame, f"K_{player2_down}")] and player2_y < HEIGHT - object_height:
        player2_y += 5

    current_time = pygame.time.get_ticks()
    if current_time - player1_last_fire >= fire_rate:
        bullets_left.append([player1_x + object_width, player1_y + object_height // 2 - bullet_height // 2])
        player1_last_fire = current_time

    if current_time - player2_last_fire >= fire_rate:
        bullets_right.append([player2_x - bullet_width, player2_y + object_height // 2 - bullet_height // 2])
        player2_last_fire = current_time

    for bullet in bullets_left[:]:
        bullet[0] += bullet_speed
        if bullet[0] > WIDTH:
            bullets_left.remove(bullet)

    for bullet in bullets_right[:]:
        bullet[0] -= bullet_speed
        if bullet[0] < 0:
            bullets_right.remove(bullet)

    for bullet in bullets_left[:]:
        if player2_x < bullet[0] < player2_x + object_width and player2_y < bullet[1] < player2_y + object_height:
            player2_hp -= 1
            bullets_left.remove(bullet)

    for bullet in bullets_right[:]:
        if player1_x < bullet[0] < player1_x + object_width and player1_y < bullet[1] < player1_y + object_height:
            player1_hp -= 1
            bullets_right.remove(bullet)

    fire_rate = max(5, fire_rate - 0.01)

    pygame.draw.rect(screen, BLUE, (player1_x, player1_y, object_width, object_height))
    pygame.draw.rect(screen, RED, (player2_x, player2_y, object_width, object_height))

    for bullet in bullets_left:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))

    for bullet in bullets_right:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))

    hp_text = font.render(f"{player1_name} HP: {player1_hp}   {player2_name} HP: {player2_hp}", True, WHITE)
    win_text = font.render(f"{player1_name} Wins: {player1_wins}   {player2_name} Wins: {player2_wins}", True, WHITE)
    screen.blit(hp_text, (20, 20))
    screen.blit(win_text, (WIDTH - 300, 20))

    if player1_hp <= 0 or player2_hp <= 0:
        if player1_hp <= 0:
            player2_wins += 1
            winner_message = f"{player2_name} wins this round! Press 'R' to restart."
        else:
            player1_wins += 1
            winner_message = f"{player1_name} wins this round! Press 'R' to restart."

        game_over_text = font.render(winner_message, True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    reset_game()
                    waiting = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
