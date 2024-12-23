import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
CELL_SIZE = WIDTH // 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
FONT = pygame.font.Font(None, 100)

class TicTacToe:
    def __init__(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.currentPlayer = "X"
        self.running = True

    def drawBoard(self):
        screen.fill(WHITE)
        for i in range(1, 3):
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == "X":
                    self.drawX(row, col)
                elif self.board[row][col] == "O":
                    self.drawO(row, col)

    def drawX(self, row, col):
        x, y = col * CELL_SIZE, row * CELL_SIZE
        pygame.draw.line(screen, BLUE, (x + 50, y + 50), (x + CELL_SIZE - 50, y + CELL_SIZE - 50), LINE_WIDTH)
        pygame.draw.line(screen, BLUE, (x + CELL_SIZE - 50, y + 50), (x + 50, y + CELL_SIZE - 50), LINE_WIDTH)

    def drawO(self, row, col):
        x, y = col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, RED, (x, y), CELL_SIZE // 2 - 50, LINE_WIDTH)

    def makeMove(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.currentPlayer
            if self.checkWinner():
                self.displayMessage(f"Player {self.currentPlayer} Wins!")
                self.resetGame()
            elif self.isDraw():
                self.displayMessage("It's a Draw!")
                self.resetGame()
            else:
                self.currentPlayer = "O" if self.currentPlayer == "X" else "X"

    def checkWinner(self):
        for i in range(3):
            if all(self.board[i][j] == self.currentPlayer for j in range(3)) or all(self.board[j][i] == self.currentPlayer for j in range(3)):
                return True
        if all(self.board[i][i] == self.currentPlayer for i in range(3)) or all(self.board[i][2 - i] == self.currentPlayer for i in range(3)):
            return True
        return False

    def isDraw(self):
        return all(self.board[row][col] != "" for row in range(3) for col in range(3))

    def displayMessage(self, message):
        screen.fill(WHITE)
        text = FONT.render(message, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

    def resetGame(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.currentPlayer = "X"

    def getCell(self, pos):
        x, y = pos
        return y // CELL_SIZE, x // CELL_SIZE

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and self.running:
                    row, col = self.getCell(pygame.mouse.get_pos())
                    self.makeMove(row, col)
            self.drawBoard()
            pygame.display.flip()

game = TicTacToe()
game.run()
pygame.quit()
sys.exit()
