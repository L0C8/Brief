from utils import (
    get_all_themes,
    get_theme_by_name,
    get_all_theme_names,
    get_selected_theme,
    set_selected_theme
)

def get_current_theme():
    theme_name = get_selected_theme()
    return get_theme_by_name(theme_name)

def list_themes():
    return get_all_theme_names()

def switch_to_theme(index=None):
    themes = get_all_theme_names()
    current = get_selected_theme()

    if current not in themes:
        current = themes[0]

    if index is None:
        current_index = themes.index(current)
        index = (current_index + 1) % len(themes)

    selected = themes[index % len(themes)]
    set_selected_theme(selected)
    return get_theme_by_name(selected)