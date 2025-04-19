import tkinter as tk
import time
from scanner import scan_news

class NewsBox(tk.Frame):
    def __init__(self, parent, bg_color="#ffffff", fg_color="#000000"):
        super().__init__(parent, width=240, height=240, bg=bg_color)
        self.pack_propagate(False)
        self.pack()

        self.bg_color = bg_color
        self.fg_color = fg_color

        self.headlines = scan_news()
        self.render_headlines()

    def render_headlines(self):
        title = tk.Label(self, text="Top News", bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 10, "bold"))
        title.pack(pady=(10, 5))

        for headline in self.headlines:
            lbl = tk.Label(self, text=f"• {headline}", bg=self.bg_color, fg=self.fg_color, wraplength=220, justify="left", anchor="w")
            lbl.pack(anchor="w", padx=10, pady=2)
