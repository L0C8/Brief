import tkinter as tk
from tkinter import ttk
from themes import get_current_theme, list_themes, switch_to_theme

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

        self.dropdown_label = tk.Label(self, text="Select Theme:")
        self.dropdown_label.pack(pady=(20, 5))

        self.theme_var = tk.StringVar(value=self.theme_names[0])
        self.dropdown = ttk.Combobox(self, values=self.theme_names, textvariable=self.theme_var, state="readonly")
        self.dropdown.pack(pady=(0, 20))
        self.dropdown.bind("<<ComboboxSelected>>", self.on_theme_change)

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
        if hasattr(self, "dropdown_label"):
            self.dropdown_label.config(bg=theme["bg"], fg=theme["fg"])
        self.configure(bg=theme["bg"])

if __name__ == "__main__":
    app = BriefApp()
    app.mainloop()