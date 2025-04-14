import os
from utils import initialize_default_theme_file
# from gui import BriefApp

os.makedirs("data", exist_ok=True)
initialize_default_theme_file()

# if __name__ == "__main__":
    # app = BriefApp()
    # app.mainloop()