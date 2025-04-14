import configparser
import os

THEME_FILE = os.path.join("data", "themes.ini")

def save_theme(name, theme_dict):
    config = configparser.ConfigParser()
    config.read(THEME_FILE)

    if name not in config.sections():
        config.add_section(name)

    for key, value in theme_dict.items():
        if key != "name":
            config.set(name, key, value)

    with open(THEME_FILE, "w") as configfile:
        config.write(configfile)

def delete_theme(name):
    config = configparser.ConfigParser()
    config.read(THEME_FILE)

    if name in config.sections():
        config.remove_section(name)

        with open(THEME_FILE, "w") as configfile:
            config.write(configfile)
        return True
    return False


def initialize_default_theme_file():
    if not os.path.exists(THEME_FILE):
        default_content = """
[Dark]
bg = #1e1e1e
fg = #e0e0e0
accent = #61dafb
button_bg = #333333
button_fg = #ffffff
headline = #dddddd

[Light]
bg = #ffffff
fg = #000000
accent = #007acc
button_bg = #f0f0f0
button_fg = #000000
headline = #222222

[CyberGreen]
bg = #0d0f0d
fg = #00ff9c
accent = #33ffcc
button_bg = #1e1e1e
button_fg = #00ff9c
headline = #00ffaa

[MidnightPurple]
bg = #1a1b41
fg = #e0e0f8
accent = #c084f5
button_bg = #292b5e
button_fg = #ffffff
headline = #e2c6ff

[SoftSunrise]
bg = #fff3e0
fg = #4e342e
accent = #ff8a65
button_bg = #ffe0b2
button_fg = #4e342e
headline = #bf360c
""".strip()

        with open(THEME_FILE, "w") as f:
            f.write(default_content)
        print("Default themes.ini created.")
