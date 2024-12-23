import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk

class CursiveTextApp:
    def __init__(self, root, selectedFontPath):
        self.root = root
        self.root.title("The Srizzing App")
        self.root.attributes('-fullscreen', True)
        self.selectedFontPath = selectedFontPath
        self.label = tk.Label(root, text="Enter Text Below:", font=("Arial", 18))
        self.label.pack(pady=10)
        inputFrame = tk.Frame(root)
        inputFrame.pack(pady=10, fill="x", expand=True)
        self.textInput = tk.Text(inputFrame, font=("Arial", 16), width=80, height=10, wrap="word")
        self.textInput.pack(side="left", fill="both", expand=True)
        self.textInput.bind("<KeyRelease>", self.convertToCursive)
        inputScrollbar = ttk.Scrollbar(inputFrame, orient="vertical", command=self.textInput.yview)
        inputScrollbar.pack(side="right", fill="y")
        self.textInput.config(yscrollcommand=inputScrollbar.set)
        canvasFrame = tk.Frame(root)
        canvasFrame.pack(pady=20, fill="both", expand=True)
        self.canvas = tk.Canvas(canvasFrame, width=1200, height=600, bg="white", scrollregion=(0, 0, 2000, 2000))
        self.canvas.pack(side="left", fill="both", expand=True)
        canvasScrollbar = ttk.Scrollbar(canvasFrame, orient="vertical", command=self.canvas.yview)
        canvasScrollbar.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=canvasScrollbar.set)

    def convertToCursive(self, event):
        userInput = self.textInput.get("1.0", tk.END).strip()
        if userInput:
            self.renderCursiveText(userInput)

    def renderCursiveText(self, text):
        try:
            font = ImageFont.truetype(self.selectedFontPath, 40)
        except OSError:
            font = ImageFont.load_default()
        image = Image.new("RGB", (2000, 2000), "white")
        draw = ImageDraw.Draw(image)
        draw.multiline_text((10, 50), text, font=font, fill="blue", spacing=10)
        imageTk = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        self.canvas.image = imageTk
        self.canvas.create_image(0, 0, anchor="nw", image=imageTk)

if __name__ == "__main__":
    fontPaths = {
        1: ("Segoe Print", "C:/Windows/Fonts/segoepr.ttf"),
        2: ("Algerian", "C:/Windows/Fonts/ALGER.TTF"),
        3: ("Bradley Hand ITC", "C:/Windows/Fonts/BRADHITC.TTF"),
        4: ("Broadway", "C:/Windows/Fonts/BROADW.TTF"),
        5: ("Brush Script", "C:/Windows/Fonts/BRUSHSCI.TTF"),
        6: ("Chiller", "C:/Windows/Fonts/CHILLER.TTF"),
        7: ("Edwardian Script", "C:/Windows/Fonts/EDWARDS.TTF"),
        8: ("Freestyle Script", "C:/Windows/Fonts/FREESCPT.TTF"),
        9: ("Gabriola", "C:/Windows/Fonts/GABRIOLA.TTF"),
        10: ("Gigi", "C:/Windows/Fonts/GIGI.TTF"),
        11: ("Harlow Solid", "C:/Windows/Fonts/HARLOWSI.TTF"),
        12: ("Harrington", "C:/Windows/Fonts/HARNGTON.TTF"),
        13: ("Jokerman", "C:/Windows/Fonts/JOKERMAN.TTF"),
        14: ("Kunstler Script", "C:/Windows/Fonts/KUNSTLER.TTF"),
        15: ("Lucida Handwriting", "C:/Windows/Fonts/LHANDW.TTF"),
        16: ("Magneto", "C:/Windows/Fonts/MAGNETOB.TTF"),
        17: ("Niagara Engraved", "C:/Windows/Fonts/NIAGENG.TTF"),
        18: ("Parchment", "C:/Windows/Fonts/PARCH.TTF"),
        19: ("Rage Italic", "C:/Windows/Fonts/RAGE.TTF"),
        20: ("Ravie", "C:/Windows/Fonts/RAVIE.TTF"),
        21: ("Segoe Script", "C:/Windows/Fonts/SEGOESC.TTF"),
        22: ("Tempus Sans", "C:/Windows/Fonts/TEMPSITC.TTF"),
        23: ("Viner Hand", "C:/Windows/Fonts/VINERITC.TTF"),
        24: ("Vivaldi", "C:/Windows/Fonts/VIVALDII.TTF"),
        25: ("Vladimir Script", "C:/Windows/Fonts/VLADIMIR.TTF")
    }

    print("Available Fonts:")
    for number, (name, _) in fontPaths.items():
        print(f"{number}: {name}")

    while True:
        try:
            choice = int(input("Enter the number of your desired font: "))
            if choice in fontPaths:
                selectedFontPath = fontPaths[choice][1]
                break
            else:
                print("Invalid selection. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    root = tk.Tk()
    app = CursiveTextApp(root, selectedFontPath)
    root.mainloop()