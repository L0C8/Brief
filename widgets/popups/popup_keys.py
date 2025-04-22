import tkinter as tk
import configparser
import os

API_KEYS_FILE = os.path.join("data", "api_keys.ini")

class APIKeyPopup(tk.Toplevel):
    def __init__(self, parent, theme):
        super().__init__(parent)
        self.title("API Keys")
        self.geometry("520x480")
        self.configure(bg=theme["bg"])
        self.resizable(False, False)

        self.theme = theme
        self.entries = {}

        self.create_widgets()
        self.load_keys()

    def create_widgets(self):
        labels = ["openweathermap", "newsapi", "gnews"]

        for idx, label in enumerate(labels):
            tk.Label(
                self,
                text=label,
                font=("Helvetica", 10),
                bg=self.theme["bg"],
                fg=self.theme["fg"]
            ).place(x=40, y=40 + idx * 60)

            entry = tk.Entry(self, width=50, bg=self.theme["bg"], fg=self.theme["fg"], insertbackground=self.theme["fg"])
            entry.place(x=180, y=40 + idx * 60)
            self.entries[label] = entry

        self.cancel_button = tk.Button(
            self, text="Cancel", width=10,
            command=self.destroy,
            bg=self.theme["bg"], fg=self.theme["fg"]
        )
        self.cancel_button.place(x=300, y=420)

        self.apply_button = tk.Button(
            self, text="Apply", width=10,
            command=self.save_keys,
            bg=self.theme["bg"], fg=self.theme["fg"]
        )
        self.apply_button.place(x=400, y=420)

    def load_keys(self):
        config = configparser.ConfigParser()
        config.read(API_KEYS_FILE)
        for label in self.entries:
            if label in config and "key" in config[label]:
                self.entries[label].insert(0, config[label]["key"])

    def save_keys(self):
        config = configparser.ConfigParser()
        for label, entry in self.entries.items():
            config[label] = {"key": entry.get()}

        with open(API_KEYS_FILE, "w") as f:
            config.write(f)

        self.destroy()
