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
        icon_path = "assets/01d.png"
        weather = scan_weather()
        timestamp = "Unknown"

        if os.path.exists("data/cached_weather.json"):
            with open("data/cached_weather.json", "r") as f:
                cached = json.load(f)
                code = cached.get("data", {}).get("weather", [{}])[0].get("id", 800)
                ts = cached.get("timestamp", None)
                if ts:
                    timestamp = time.strftime("%H:%M", time.localtime(ts))
                hour = time.localtime().tm_hour
                is_day = 5 <= hour < 20
                icon_path = self.get_gpx(code, is_day)

        self.weather_icon = tk.PhotoImage(file=icon_path).subsample(2, 2)
        self.create_image(-5, -5, anchor="nw", image=self.weather_icon)

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

    def get_gpx(self, code, is_day=True):
        suf = "d" if is_day else "n"
        if 200 <= code < 300:
            return f"assets/11{suf}.png"  # Thunderstorm
        elif 300 <= code < 400:
            return f"assets/09{suf}.png"  # Drizzle
        elif 500 <= code < 505:
            return f"assets/10{suf}.png"  # Light to moderate rain
        elif code == 511:
            return f"assets/13{suf}.png"  # Freezing rain
        elif 520 <= code < 600:
            return f"assets/09{suf}.png"  # Shower rain
        elif 600 <= code < 700:
            return f"assets/13{suf}.png"  # Snow
        elif 700 <= code < 800:
            return f"assets/50{suf}.png"  # Atmosphere
        elif code == 800:
            return f"assets/01{suf}.png"  # Clear
        elif code == 801:
            return f"assets/02{suf}.png"  # Few clouds
        elif code == 802:
            return f"assets/03{suf}.png"  # Scattered clouds
        elif code in [803, 804]:
            return f"assets/04{suf}.png"  # Broken/overcast clouds
        else:
            return f"assets/01{suf}.png"  # Fallback: Clear