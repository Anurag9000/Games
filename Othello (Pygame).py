import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 640, 640
CELL_SIZE = WIDTH // 8
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

class Othello:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = "Black"
        self.running = True
        self.scores = {"Black": 2, "White": 2}
        self.init_pieces()

    def init_pieces(self):
        mid = len(self.board) // 2
        self.board[mid - 1][mid - 1] = "White"
        self.board[mid - 1][mid] = "Black"
        self.board[mid][mid - 1] = "Black"
        self.board[mid][mid] = "White"

    def draw_board(self, screen):
        screen.fill(GREEN)
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
                piece = self.board[row][col]
                if piece:
                    color = WHITE if piece == "White" else BLACK
                    pygame.draw.circle(
                        screen,
                        color,
                        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 3,
                    )
        score_text = FONT.render(f"White: {self.scores['White']}   Black: {self.scores['Black']}", True, WHITE)
        screen.blit(score_text, (20, 10))

    def is_valid_move(self, row, col, color):
        if self.board[row][col] is not None:
            return False
        opponent = "White" if color == "Black" else "Black"
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] is not None:
                if self.board[r][c] == opponent:
                    found_opponent = True
                elif self.board[r][c] == color:
                    if found_opponent:
                        return True
                    else:
                        break
                else:
                    break
                r += dr
                c += dc
        return False

    def get_valid_moves(self, color):
        return [(row, col) for row in range(8) for col in range(8) if self.is_valid_move(row, col, color)]

    def make_move(self, row, col, color):
        self.board[row][col] = color
        opponent = "White" if color == "Black" else "Black"
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] is not None:
                if self.board[r][c] == opponent:
                    pieces_to_flip.append((r, c))
                elif self.board[r][c] == color:
                    for rr, cc in pieces_to_flip:
                        self.board[rr][cc] = color
                    break
                else:
                    break
                r += dr
                c += dc
        self.update_scores()

    def update_scores(self):
        self.scores["Black"] = sum(row.count("Black") for row in self.board)
        self.scores["White"] = sum(row.count("White") for row in self.board)

    def check_game_over(self):
        if not self.get_valid_moves("Black") and not self.get_valid_moves("White"):
            winner = "Black" if self.scores["Black"] > self.scores["White"] else "White" if self.scores["White"] > self.scores["Black"] else "No one"
            return winner
        return None

    def reset_game(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = "Black"
        self.scores = {"Black": 2, "White": 2}
        self.init_pieces()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Othello")
    clock = pygame.time.Clock()
    game = Othello()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and game.running:
                x, y = pygame.mouse.get_pos()
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if (row, col) in game.get_valid_moves(game.current_player):
                    game.make_move(row, col, game.current_player)
                    game.current_player = "White" if game.current_player == "Black" else "Black"
                    if not game.get_valid_moves(game.current_player):
                        game.current_player = "White" if game.current_player == "Black" else "Black"
                        if not game.get_valid_moves(game.current_player):
                            game.running = False
            if event.type == pygame.KEYDOWN and not game.running:
                if event.key == pygame.K_r:
                    game.reset_game()
                    game.running = True
        screen.fill(GREEN)
        game.draw_board(screen)
        winner = game.check_game_over()
        if winner and not game.running:
            text = FONT.render(f"{winner} Won! Press R to Restart", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
