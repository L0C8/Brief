import tkinter as tk

class Toolbar(tk.Frame):
    def __init__(self, parent, bg_color="#ffffff", fg_color="#000000"):
        super().__init__(parent, bg=bg_color)
        self.pack(fill="x", pady=(5, 0))

        self.bg_color = bg_color
        self.fg_color = fg_color

        self.create_buttons()

    def create_buttons(self):
        for i in range(3):
            if i == 0:
                btn = tk.Button(
                    self,
                    text="X",
                    width=2,
                    bg=self.bg_color,
                    fg=self.fg_color,
                    relief="flat",
                    font=("Helvetica", 8),
                    command=self.open_settings
                )
            else:
                btn = tk.Button(
                    self,
                    text="X",
                    width=2,
                    bg=self.bg_color,
                    fg=self.fg_color,
                    relief="flat",
                    font=("Helvetica", 8)
                )
            btn.pack(side="left", padx=5)

    def open_settings(self):
        from popups.popup_settings import SettingsPopup
        SettingsPopup(self, {"bg": self.bg_color, "fg": self.fg_color})