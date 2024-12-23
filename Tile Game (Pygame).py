import pygame
import random

def generateBoard():
    numbers = list(range(1, 16))
    random.shuffle(numbers)
    numbers.append(0)
    return [numbers[i:i+4] for i in range(0, 16, 4)]

def drawBoard(board, screen, font):
    screen.fill((255, 255, 255))
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                pygame.draw.rect(screen, (200, 200, 200), (j * 100, i * 100, 100, 100))
                numSurface = font.render(str(board[i][j]), True, (0, 0, 0))
                screen.blit(numSurface, (j * 100 + 35, i * 100 + 35))
            pygame.draw.rect(screen, (0, 0, 0), (j * 100, i * 100, 100, 100), 2)

def findEmptyTile(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return i, j

def isSolved(board):
    sequence = [board[i][j] for i in range(4) for j in range(4)]
    return sequence[:-1] == list(range(1, 16)) and sequence[-1] == 0

def handleClick(board, row, col):
    emptyRow, emptyCol = findEmptyTile(board)
    if (row == emptyRow and abs(col - emptyCol) == 1) or (col == emptyCol and abs(row - emptyRow) == 1):
        board[emptyRow][emptyCol], board[row][col] = board[row][col], board[emptyRow][emptyCol]

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Tile Game")
    font = pygame.font.Font(None, 50)
    clock = pygame.time.Clock()

    board = generateBoard()
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // 100, x // 100
                handleClick(board, row, col)
                if isSolved(board):
                    score += 1
                    board = generateBoard()

        drawBoard(board, screen, font)
        scoreSurface = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(scoreSurface, (10, 360))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
