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
