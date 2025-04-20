import os
import json
import time
import tkinter as tk
from tkinter import ttk
from themes import get_current_theme, list_themes, switch_to_theme
from widgets.weatherbox import WeatherBox
from widgets.newsbox import NewsBox

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

        from widgets.toolbar import Toolbar
        self.toolbar = Toolbar(self, bg_color=self.bg, fg_color=self.fg)

        self.weather_box = WeatherBox(self)
        self.news_box = NewsBox(self, bg_color=self.bg, fg_color=self.fg)

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

