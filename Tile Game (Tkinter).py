import tkinter as tk
import random

def generateBoard():
    numbers = list(range(1, 16))
    random.shuffle(numbers)
    numbers.append(0)
    return [numbers[i:i+4] for i in range(0, 16, 4)]

def drawBoard(board, canvas):
    canvas.delete("all")
    for i in range(4):
        for j in range(4):
            x0, y0 = j * 100, i * 100
            x1, y1 = x0 + 100, y0 + 100
            if board[i][j] != 0:
                canvas.create_rectangle(x0, y0, x1, y1, fill="lightgray", outline="black")
                canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(board[i][j]), font=("Helvetica", 32))
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")

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

def handleMouseClick(event, board, canvas, scoreLabel, score):
    row, col = event.y // 100, event.x // 100
    handleClick(board, row, col)
    if isSolved(board):
        score[0] += 1
        board[:] = generateBoard()
    drawBoard(board, canvas)
    scoreLabel.config(text=f"Score: {score[0]}")

def main():
    root = tk.Tk()
    root.title("Tile Game")

    board = generateBoard()
    score = [0]

    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()

    scoreLabel = tk.Label(root, text=f"Score: {score[0]}", font=("Helvetica", 16))
    scoreLabel.pack()

    canvas.bind("<Button-1>", lambda event: handleMouseClick(event, board, canvas, scoreLabel, score))

    drawBoard(board, canvas)

    root.mainloop()

if __name__ == "__main__":
    main()
