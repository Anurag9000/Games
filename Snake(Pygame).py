import pygame
import random
import sys
import time

WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

class SnakeGame:
    def __init__(self):
        self.snake = [(100, 100), (80, 100), (60, 100), (40, 100), (20, 100)]
        self.direction = "RIGHT"
        self.speed = 10
        self.game_running = True
        self.obstacles = []
        self.moving_obstacles = []
        self.foods = []
        self.time_elapsed = 0
        self.score = 0
        self.level = 1
        self.static_obstacle_interval = 5000
        self.moving_obstacle_interval = 7000
        self.food_interval = 15000
        self.last_static_obstacle_time = pygame.time.get_ticks()
        self.last_moving_obstacle_time = pygame.time.get_ticks()
        self.last_food_time = pygame.time.get_ticks()
        self.start_time = time.time()

    def random_position(self):
        while True:
            x = random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
            y = random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE
            pos = (x, y)
            if pos not in self.snake and pos not in self.obstacles and pos not in self.foods:
                return pos

    def change_direction(self, direction):
        opposites = {'UP':'DOWN', 'DOWN':'UP', 'LEFT':'RIGHT', 'RIGHT':'LEFT'}
        if direction != opposites.get(self.direction):
            self.direction = direction

    def move_snake(self):
        x, y = self.snake[0]
        if self.direction == 'UP':
            y -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            y += BLOCK_SIZE
        elif self.direction == 'LEFT':
            x -= BLOCK_SIZE
        elif self.direction == 'RIGHT':
            x += BLOCK_SIZE
        new_head = (x, y)
        if (x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or new_head in self.snake or new_head in self.obstacles):
            self.game_running = False
            return
        for obstacle in self.moving_obstacles:
            if new_head == obstacle['pos']:
                self.game_running = False
                return
        if new_head in self.foods:
            self.foods.remove(new_head)
            self.snake.insert(0, new_head)
            self.score += 1
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()

    def check_body_collision_with_moving_obstacles(self):
        for segment in self.snake:
            for obstacle in self.moving_obstacles:
                if segment == obstacle['pos']:
                    self.game_running = False
                    return

    def update_moving_obstacles(self):
        for obstacle in self.moving_obstacles:
            x, y = obstacle['pos']
            direction = obstacle['direction']
            if direction == 'UP':
                y -= BLOCK_SIZE
            elif direction == 'DOWN':
                y += BLOCK_SIZE
            elif direction == 'LEFT':
                x -= BLOCK_SIZE
            elif direction == 'RIGHT':
                x += BLOCK_SIZE
            if x < 0:
                x = WIDTH - BLOCK_SIZE
            elif x >= WIDTH:
                x = 0
            if y < 0:
                y = HEIGHT - BLOCK_SIZE
            elif y >= HEIGHT:
                y = 0
            obstacle['pos'] = (x, y)

    def draw_elements(self):
        screen.fill(BLACK)
        for x, y in self.snake:
            pygame.draw.rect(screen, GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        for x, y in self.obstacles:
            pygame.draw.rect(screen, RED, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        for food in self.foods:
            pygame.draw.rect(screen, BLUE, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
        for obstacle in self.moving_obstacles:
            x, y = obstacle['pos']
            pygame.draw.rect(screen, ORANGE, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        elapsed_time = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed_time, 60)
        timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (WIDTH - 150, 10))
        pygame.display.flip()

    def place_static_obstacle(self):
        if len(self.obstacles) < 15:
            pos = self.random_position()
            self.obstacles.append(pos)

    def place_moving_obstacle(self):
        if len(self.moving_obstacles) < 5:
            pos = self.random_position()
            direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            self.moving_obstacles.append({'pos': pos, 'direction': direction})

    def place_food(self):
        if len(self.foods) < 10:
            pos = self.random_position()
            self.foods.append(pos)

    def restart_game(self):
        self.snake = [(100, 100), (80, 100), (60, 100), (40, 100), (20, 100)]
        self.direction = "RIGHT"
        self.speed = 10
        self.game_running = True
        self.obstacles = []
        self.moving_obstacles = []
        self.foods = []
        self.time_elapsed = 0
        self.score = 0
        self.level = 1
        self.start_time = time.time()

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()
            if not self.game_running:
                font = pygame.font.Font(None, 72)
                game_over_text = font.render("Game Over! Press R to Restart", True, RED)
                text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(game_over_text, text_rect)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.restart_game()
                continue
            if current_time - self.last_static_obstacle_time > self.static_obstacle_interval:
                self.place_static_obstacle()
                self.last_static_obstacle_time = current_time
            if current_time - self.last_moving_obstacle_time > self.moving_obstacle_interval:
                self.place_moving_obstacle()
                self.last_moving_obstacle_time = current_time
            if current_time - self.last_food_time > self.food_interval:
                self.place_food()
                self.last_food_time = current_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_direction('UP')
                    elif event.key == pygame.K_DOWN:
                        self.change_direction('DOWN')
                    elif event.key == pygame.K_LEFT:
                        self.change_direction('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        self.change_direction('RIGHT')
            self.move_snake()
            self.update_moving_obstacles()
            self.check_body_collision_with_moving_obstacles()
            self.draw_elements()
            pygame.time.delay(100)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
