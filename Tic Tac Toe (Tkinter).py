import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.master.geometry("400x400")
        self.master.resizable(False, False)
        self.currentPlayer = "X"  # X always starts
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.createBoard()

    def createBoard(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    self.master,
                    text="",
                    font=("Arial", 24),
                    height=2,
                    width=5,
                    command=lambda r=row, c=col: self.makeMove(r, c)
                )
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def makeMove(self, row, col):
        if self.board[row][col] == "" and not self.checkWinner():
            self.board[row][col] = self.currentPlayer
            self.buttons[row][col].config(text=self.currentPlayer)

            if self.checkWinner():
                messagebox.showinfo("Game Over", f"Player {self.currentPlayer} wins!")
                self.resetBoard()
            elif self.isDraw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.resetBoard()
            else:
                self.currentPlayer = "O" if self.currentPlayer == "X" else "X"

    def checkWinner(self):
        for i in range(3):
            if all(self.board[i][j] == self.currentPlayer for j in range(3)) or \
               all(self.board[j][i] == self.currentPlayer for j in range(3)):
                return True
        if all(self.board[i][i] == self.currentPlayer for i in range(3)) or \
           all(self.board[i][2 - i] == self.currentPlayer for i in range(3)):
            return True
        return False

    def isDraw(self):
        return all(self.board[row][col] != "" for row in range(3) for col in range(3))

    def resetBoard(self):
        self.currentPlayer = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
