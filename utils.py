import configparser
import os

THEME_FILE = os.path.join("data", "themes.ini")
USER_SETTINGS_FILE = os.path.join("data", "user_settings.ini")

# theme settings

def get_all_themes():
    config = configparser.ConfigParser()
    config.read(THEME_FILE)
    return [{**config[section], "name": section} for section in config.sections()]

def get_all_theme_names():
    config = configparser.ConfigParser()
    config.read(THEME_FILE)
    return config.sections()

def get_theme_by_name(name):
    config = configparser.ConfigParser()
    config.read(THEME_FILE)
    if name in config:
        return {**config[name], "name": name}
    return None

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

# weather settings

def get_icon_path_from_code(code, is_day=True):
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


# user settings

def initialize_user_settings():
    if not os.path.exists(USER_SETTINGS_FILE):
        default_content = """
[Preferences]
selected_theme = Dark
""".strip()

        with open(USER_SETTINGS_FILE, "w") as f:
            f.write(default_content)
        print("Default user_settings.ini created.")

def get_selected_theme():
    config = configparser.ConfigParser()
    config.read(USER_SETTINGS_FILE)
    return config.get("Preferences", "selected_theme", fallback="Dark")

def set_selected_theme(theme_name):
    config = configparser.ConfigParser()
    config.read(USER_SETTINGS_FILE)

    if not config.has_section("Preferences"):
        config.add_section("Preferences")

    config.set("Preferences", "selected_theme", theme_name)

    with open(USER_SETTINGS_FILE, "w") as f:
        config.write(f)

# api data (temp, only weather)

API_KEYS_FILE = os.path.join("data", "api_keys.ini")

def get_api_key(service_name):
    config = configparser.ConfigParser()
    config.read(API_KEYS_FILE)
    try:
        return config[service_name]["key"]
    except KeyError:
        return None