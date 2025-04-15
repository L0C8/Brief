import requests
from utils import get_api_key

def scan_weather(location=None):
    api_key = get_api_key("openweathermap")
    if not api_key:
        return "Missing API key."

    try:
        geo = requests.get("https://ipinfo.io/json").json()
        loc = geo.get("loc", "")
        city = geo.get("city", "Unknown")
        country = geo.get("country", "Unknown")

        if not loc:
            return "Could not determine location."

        lat, lon = loc.split(",")

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") != 200:
            return f"Weather error: {data.get('message', 'unknown error')}"

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        return f"{city}, {country}: {temp}°C, {desc.capitalize()}"

    except Exception as e:
        return f"Weather error: {e}"