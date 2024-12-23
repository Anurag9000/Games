import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
BLOCK_SIZE = SCREEN_WIDTH // 10
YELLOW = (255, 255, 102)
BLUE = (51, 153, 255)
RED = (204, 0, 0)
GREEN = (0, 204, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (255, 165, 0), (64, 224, 208)]
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snakes and Ladders")
font = pygame.font.SysFont(None, 24)
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

def roll_dice():
    return random.randint(1, 6)

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

def draw_board():
    for row in range(10):
        for col in range(10):
            x = col * BLOCK_SIZE
            y = (9 - row) * BLOCK_SIZE
            square_num = row * 10 + (col + 1) if row % 2 == 0 else row * 10 + (10 - col)
            color = YELLOW if (row + col) % 2 == 0 else BLUE
            pygame.draw.rect(screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
            text = font.render(str(square_num), True, BLACK)
            screen.blit(text, (x + 5, y + 5))
    for start, end in snakes.items():
        draw_snake_ladder(start, end, RED)
    for start, end in ladders.items():
        draw_snake_ladder(start, end, GREEN)

def draw_snake_ladder(start, end, color):
    start_x, start_y = get_position(start)
    end_x, end_y = get_position(end)
    pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 5)

def get_position(square):
    row, col = divmod(square - 1, 10)
    row = 9 - row
    col = col if (9 - row) % 2 == 0 else 9 - col
    x = col * BLOCK_SIZE + BLOCK_SIZE // 2
    y = row * BLOCK_SIZE + BLOCK_SIZE // 2
    return x, y

def draw_player(position, color):
    x, y = get_position(position)
    pygame.draw.circle(screen, color, (x, y), BLOCK_SIZE // 4)

def main():
    num_players = int(input("Enter the number of players (up to 6): "))
    num_players = min(num_players, 6)
    players = [Player(PLAYER_COLORS[i]) for i in range(num_players)]
    current_player_idx = 0
    dice_roll = 0

    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)
        draw_board()
        for i, player in enumerate(players):
            draw_player(player.position, player.color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    dice_roll = roll_dice()
                    print(f"Player {current_player_idx + 1} rolled a {dice_roll}")
                    players[current_player_idx].move(dice_roll)
                    if players[current_player_idx].position == 100:
                        print(f"Player {current_player_idx + 1} wins!")
                        pygame.quit()
                        sys.exit()
                    current_player_idx = (current_player_idx + 1) % num_players
        dice_text = font.render(f"Dice Roll: {dice_roll}", True, BLACK)
        screen.blit(dice_text, (10, SCREEN_HEIGHT - 30))
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
