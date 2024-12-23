import tkinter as tk
from tkinter import messagebox


class Othello:
    def __init__(self, master):
        self.master = master
        self.master.title("Othello")
        self.master.geometry("640x640")
        self.master.resizable(False, False)

        self.boardSize = 8
        self.cellSize = 640 // self.boardSize
        self.board = [[None for _ in range(self.boardSize)] for _ in range(self.boardSize)]
        self.currentPlayer = "Black"

        self.canvas = tk.Canvas(self.master, width=640, height=640, bg="green")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handleClick)
        self.master.bind("r", self.restartGame)

        self.createBoard()
        self.initializePieces()

        self.scoreLabel = tk.Label(
            self.master, text="White: 2   Black: 2", font=("Arial", 16), bg="green", fg="white"
        )
        self.scoreLabel.place(x=400, y=10)

    def createBoard(self):
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                x1 = col * self.cellSize
                y1 = row * self.cellSize
                x2 = x1 + self.cellSize
                y2 = y1 + self.cellSize
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

    def initializePieces(self):
        mid = self.boardSize // 2
        self.placePiece(mid - 1, mid - 1, "White")
        self.placePiece(mid - 1, mid, "Black")
        self.placePiece(mid, mid - 1, "Black")
        self.placePiece(mid, mid, "White")

    def placePiece(self, row, col, color):
        x1 = col * self.cellSize + self.cellSize // 4
        y1 = row * self.cellSize + self.cellSize // 4
        x2 = x1 + self.cellSize // 2
        y2 = y1 + self.cellSize // 2
        self.board[row][col] = self.canvas.create_oval(x1, y1, x2, y2, fill=color)

    def handleClick(self, event):
        col = event.x // self.cellSize
        row = event.y // self.cellSize
        if self.isValidMove(row, col, self.currentPlayer):
            self.makeMove(row, col, self.currentPlayer)
            self.updateScores()
            self.currentPlayer = "White" if self.currentPlayer == "Black" else "Black"
            if not self.hasValidMove(self.currentPlayer):
                self.currentPlayer = "White" if self.currentPlayer == "Black" else "Black"
                if not self.hasValidMove(self.currentPlayer):
                    self.endGame()

    def isValidMove(self, row, col, color):
        if self.board[row][col] is not None:
            return False
        opponent = "White" if color == "Black" else "Black"
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            foundOpponent = False
            while 0 <= r < self.boardSize and 0 <= c < self.boardSize and self.board[r][c] is not None:
                pieceColor = self.canvas.itemcget(self.board[r][c], "fill")
                if pieceColor == opponent:
                    foundOpponent = True
                elif pieceColor == color:
                    if foundOpponent:
                        return True
                    else:
                        break
                else:
                    break
                r += dr
                c += dc
        return False

    def makeMove(self, row, col, color):
        self.placePiece(row, col, color)
        opponent = "White" if color == "Black" else "Black"
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            piecesToFlip = []
            while 0 <= r < self.boardSize and 0 <= c < self.boardSize and self.board[r][c] is not None:
                pieceColor = self.canvas.itemcget(self.board[r][c], "fill")
                if pieceColor == opponent:
                    piecesToFlip.append((r, c))
                elif pieceColor == color:
                    for rr, cc in piecesToFlip:
                        self.canvas.itemconfig(self.board[rr][cc], fill=color)
                    break
                else:
                    break
                r += dr
                c += dc

    def hasValidMove(self, color):
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if self.isValidMove(row, col, color):
                    return True
        return False

    def updateScores(self):
        blackCount = sum(
            self.canvas.itemcget(self.board[row][col], "fill") == "Black"
            for row in range(self.boardSize)
            for col in range(self.boardSize)
            if self.board[row][col] is not None
        )
        whiteCount = sum(
            self.canvas.itemcget(self.board[row][col], "fill") == "White"
            for row in range(self.boardSize)
            for col in range(self.boardSize)
            if self.board[row][col] is not None
        )
        self.scoreLabel.config(text=f"White: {whiteCount}   Black: {blackCount}")

    def endGame(self):
        blackCount = sum(
            self.canvas.itemcget(self.board[row][col], "fill") == "Black"
            for row in range(self.boardSize)
            for col in range(self.boardSize)
            if self.board[row][col] is not None
        )
        whiteCount = sum(
            self.canvas.itemcget(self.board[row][col], "fill") == "White"
            for row in range(self.boardSize)
            for col in range(self.boardSize)
            if self.board[row][col] is not None
        )
        winner = "Black" if blackCount > whiteCount else "White" if whiteCount > blackCount else "No one"
        self.canvas.delete("all")
        self.canvas.create_text(
            320,
            320,
            text=f"{winner} Won\nPress R to Restart",
            fill="white",
            font=("Arial", 24),
        )

    def restartGame(self, event):
        self.board = [[None for _ in range(self.boardSize)] for _ in range(self.boardSize)]
        self.currentPlayer = "Black"
        self.canvas.delete("all")
        self.createBoard()
        self.initializePieces()
        self.updateScores()


if __name__ == "__main__":
    root = tk.Tk()
    game = Othello(root)
    root.mainloop()
