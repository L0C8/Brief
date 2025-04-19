import tkinter as tk
import os
import json
import time
from scanner import scan_weather

class WeatherBox(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=240, height=120, highlightthickness=0)
        self.pack()

        current_hour = time.localtime().tm_hour
        if 5 <= current_hour < 15:
            self.gradient_start, self.gradient_end = "#4facfe", "#00f2fe"
            self.text_color = "black"
        elif 15 <= current_hour < 20:
            self.gradient_start, self.gradient_end = "#f9d423", "#ff4e50"
            self.text_color = "black"
        else:
            self.gradient_start, self.gradient_end = "#2c3e50", "#000000"
            self.text_color = "white"

        self.draw_gradient()
        self.display_weather()

    def draw_gradient(self):
        steps = 100
        for i in range(steps):
            r1, g1, b1 = self.winfo_rgb(self.gradient_start)
            r2, g2, b2 = self.winfo_rgb(self.gradient_end)
            r = int(r1 + (r2 - r1) * i / steps) >> 8
            g = int(g1 + (g2 - g1) * i / steps) >> 8
            b = int(b1 + (b2 - b1) * i / steps) >> 8
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            self.create_rectangle(0, i * 120 // steps, 240, (i + 1) * 120 // steps, outline="", fill=hex_color)

    def display_weather(self):
        self.weather_icon = tk.PhotoImage(file="assets/01d.png").subsample(2, 2)
        self.create_image(-5, -5, anchor="nw", image=self.weather_icon)

        weather = scan_weather()
        timestamp = "Unknown"
        if os.path.exists("data/cached_weather.json"):
            with open("data/cached_weather.json", "r") as f:
                cached = json.load(f)
                ts = cached.get("timestamp", None)
                if ts:
                    timestamp = time.strftime("%H:%M", time.localtime(ts))

        self.create_text(
            120, 60,
            text=weather,
            fill=self.text_color,
            font=("Helvetica", 10),
            justify="center",
            width=200
        )

        self.create_text(
            120, 105,
            text=f"Last updated: {timestamp}",
            fill=self.text_color,
            font=("Helvetica", 8)
        )
