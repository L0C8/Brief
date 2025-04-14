import configparser
import os

THEME_FILE = os.path.join("data", "themes.ini")

available_themes = []
current_theme = {}
theme_names = []

def load_themes():
    global available_themes, current_theme, theme_names
    config = configparser.ConfigParser()
    config.read(THEME_FILE)

    available_themes.clear()
    theme_names.clear()

    for section in config.sections():
        theme = {key: value for key, value in config[section].items()}
        theme["name"] = section
        available_themes.append(theme)
        theme_names.append(section)

    if available_themes:
        set_theme_by_name(theme_names[0])

def set_theme_by_name(name):
    global current_theme
    for theme in available_themes:
        if theme["name"].lower() == name.lower():
            current_theme = theme
            return

def toggle_theme():
    global current_theme
    if not available_themes:
        return
    index = available_themes.index(current_theme)
    current_theme = available_themes[(index + 1) % len(available_themes)]

load_themes()
