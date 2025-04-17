import os
import json
import time
import tkinter as tk
from tkinter import ttk
from themes import get_current_theme, list_themes, switch_to_theme
from scanner import scan_weather

class BriefApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Brief")
        self.geometry("240x500")
        self.resizable(False, False)
        self.theme_names = list_themes()
        self.build_ui()

    def build_ui(self):
        theme = get_current_theme()
        self.apply_theme(theme)

        weather = scan_weather()
        timestamp = "Unknown"
        if os.path.exists("data/cached_weather.json"):
            with open("data/cached_weather.json", "r") as f:
                cached = json.load(f)
                ts = cached.get("timestamp", None)
                if ts:
                    timestamp = time.strftime("%H:%M", time.localtime(ts))

        self.weather_label = tk.Label(
            self,
            text=weather,
            bg=self.bg,
            fg=self.fg,
            wraplength=200,
            justify="center"
        )
        self.weather_label.pack(pady=(30, 5))

        self.timestamp_label = tk.Label(
            self,
            text=f"Last updated: {timestamp}",
            bg=self.bg,
            fg=self.fg,
            font=("Helvetica", 8)
        )
        self.timestamp_label.pack(pady=(0, 20))

        self.update_widget_styles(theme)


    def on_theme_change(self, event):
        selected_name = self.theme_var.get()
        index = self.theme_names.index(selected_name)
        theme = switch_to_theme(index)
        self.apply_theme(theme)

    def apply_theme(self, theme):
        self.bg = theme["bg"]
        self.fg = theme["fg"]
        self.configure(bg=self.bg)
        self.update_widget_styles(theme)

    def update_widget_styles(self, theme):
        self.configure(bg=theme["bg"])

if __name__ == "__main__":
    app = BriefApp()
    app.mainloop()
