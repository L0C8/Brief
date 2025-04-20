import tkinter as tk

class SettingsPopup(tk.Toplevel):
    def __init__(self, parent, theme):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("520x480")
        self.configure(bg=theme["bg"])
        self.resizable(False, False)

        title = tk.Label(
            self,
            text="Settings",
            font=("Helvetica", 16, "bold"),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        title.pack(pady=20)

        self.theme = theme