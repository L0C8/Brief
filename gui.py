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
        current_hour = time.localtime().tm_hour
        if 5 <= current_hour < 15:
            gradient_start, gradient_end = "#4facfe", "#00f2fe"  # morning/day
        elif 15 <= current_hour < 20:
            gradient_start, gradient_end = "#f9d423", "#ff4e50"  # sunset
        else:
            gradient_start, gradient_end = "#2c3e50", "#000000"  # night
        theme = get_current_theme()
        self.apply_theme(theme)

        self.weather_canvas = tk.Canvas(self, width=240, height=120, highlightthickness=0)
        self.weather_canvas.pack()
        self.draw_gradient(self.weather_canvas, gradient_start, gradient_end)

        self.weather_icon = tk.PhotoImage(file="assets/01d.png").subsample(2, 2)
        self.weather_canvas.create_image(0, 0, anchor="nw", image=self.weather_icon)

        weather = scan_weather()
        timestamp = "Unknown"
        if os.path.exists("data/cached_weather.json"):
            with open("data/cached_weather.json", "r") as f:
                cached = json.load(f)
                ts = cached.get("timestamp", None)
                if ts:
                    timestamp = time.strftime("%H:%M", time.localtime(ts))

        self.weather_canvas.create_text(
            120, 60,
            text=weather,
            fill=self.fg,
            font=("Helvetica", 10),
            justify="center",
            width=200
        )

        self.weather_canvas.create_text(
            120, 105,
            text=f"Last updated: {timestamp}",
            fill=self.fg,
            font=("Helvetica", 8)
        )

        self.update_widget_styles(theme)

    def draw_gradient(self, canvas, color1, color2):
        steps = 100
        for i in range(steps):
            r1, g1, b1 = self.winfo_rgb(color1)
            r2, g2, b2 = self.winfo_rgb(color2)
            r = int(r1 + (r2 - r1) * i / steps) >> 8
            g = int(g1 + (g2 - g1) * i / steps) >> 8
            b = int(b1 + (b2 - b1) * i / steps) >> 8
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_rectangle(0, i * 120 // steps, 240, (i + 1) * 120 // steps, outline="", fill=hex_color)

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