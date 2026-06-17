import tkinter as tk
parchment = "#F4F1EA"
paper=  "#FFFFFF"
ink="#2C363F"
mutedSlate ="#7A7A7A"
sageGreen= "#6A8D73"
terracotta = "#C86A58"
colorBorder = "#E5E0D8"
highlight = "#EAE6DF"

fontHeader = ("Georgia",14)
fontNarrative=("Georgia", 11)
fontList = ("Arial", 10)
fontMath = ("Courier New", 12, "bold")
fontTimer= ("Courier New", 16, "bold")

def applyFlatBorder(master, bg_color=colorBorder):
    borderFrame = tk.Frame(master, bg=bg_color, padx=1,pady=1)
    return borderFrame