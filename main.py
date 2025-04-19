import os
from utils import initialize_default_theme_file, initialize_user_settings
from gui import BriefApp
from scanner import scan_news

os.makedirs("data", exist_ok=True)
initialize_default_theme_file()
initialize_user_settings()

# Test NewsAPI
# headlines = scan_news()
# print("Top Headlines:")
# for headline in headlines:
#     print(f"• {headline}")

if __name__ == "__main__":
    app = BriefApp()
    app.mainloop()