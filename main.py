import os
from utils import initialize_default_theme_file, initialize_user_settings
from gui import BriefApp

os.makedirs("data", exist_ok=True)
initialize_default_theme_file()
initialize_user_settings()

if __name__ == "__main__":
    app = BriefApp()
    app.mainloop()