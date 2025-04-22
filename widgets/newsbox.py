import tkinter as tk
import time
import webbrowser
import random
import os
import json

class NewsBox(tk.Frame):
    def __init__(self, parent, bg_color="#ffffff", fg_color="#000000"):
        super().__init__(parent, width=240, height=320, bg=bg_color)
        self.pack_propagate(False)
        self.pack()

        self.bg_color = bg_color
        self.fg_color = fg_color
        self.headlines = self.load_cached_headlines()

        self.render_headlines()

    def load_cached_headlines(self):
        from scanner import scan_news
        cache_path = "data/cached_news.json"
        cache_key = "gnews_top"
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                cached = json.load(f)
                data = cached.get(cache_key, {})
                if time.time() - data.get("timestamp", 0) < 3 * 60 * 60:
                    return data.get("headlines", [])
        return scan_news()

    def render_headlines(self):
        title = tk.Label(self, text="Top News", bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 10, "bold"))
        title.pack(pady=(10, 5))

        random.shuffle(self.headlines)
        for item in self.headlines[:5]:
            if isinstance(item, dict):
                text = item.get("title", "(untitled)")
                url = item.get("url", "")
                lbl = tk.Label(self, text=f"• {text}", bg=self.bg_color, fg=self.fg_color, wraplength=220, justify="left", anchor="w", cursor="hand2")
                lbl.pack(anchor="w", padx=10, pady=2)
                if url:
                    lbl.bind("<Button-1>", lambda e, link=url: webbrowser.open(link))
            else:
                lbl = tk.Label(self, text=f"• {item}", bg=self.bg_color, fg=self.fg_color, wraplength=220, justify="left", anchor="w")
                lbl.pack(anchor="w", padx=10, pady=2)
