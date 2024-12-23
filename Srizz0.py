import tkinter as tk
from tkinter import ttk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def generate_wordcloud():
    text = text_input.get("1.0", tk.END).strip()
    bg_color = bg_color_var.get()
    cmap = cmap_var.get()
    if not text:
        return
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color=bg_color,
        colormap=cmap
    ).generate(text)
    root.destroy()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

root = tk.Tk()
root.title("WordCloud Generator")

text_label = tk.Label(root, text="Enter Text:")
text_label.pack()
text_input = tk.Text(root, height=10, width=50)
text_input.pack()

bg_color_var = tk.StringVar(value="white")
bg_color_label = tk.Label(root, text="Select Background Color:")
bg_color_label.pack()
colors = list(mcolors.CSS4_COLORS.keys())
bg_color_dropdown = ttk.Combobox(root, textvariable=bg_color_var, values=colors, state="readonly")
bg_color_dropdown.pack()

cmap_var = tk.StringVar(value="viridis")
cmap_label = tk.Label(root, text="Select Colormap:")
cmap_label.pack()
cmap_dropdown = ttk.Combobox(root, textvariable=cmap_var, values=plt.colormaps(), state="readonly")
cmap_dropdown.pack()

generate_button = tk.Button(root, text="Generate WordCloud", command=generate_wordcloud)
generate_button.pack()

root.mainloop()