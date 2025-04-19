import requests
import os
import json
import time
from utils import get_api_key

CACHE_FILE = os.path.join("data", "cached_weather.json")
CACHE_DURATION = 15 * 60  # 15 minutes

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

        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                cached = json.load(f)
                cached_loc = cached.get("location", "")
                if (
                    time.time() - cached.get("timestamp", 0) < CACHE_DURATION
                    and cached_loc == loc
                ):
                    return format_weather(cached["data"])

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") != 200:
            return f"Weather error: {data.get('message', 'unknown error')}"

        with open(CACHE_FILE, "w") as f:
            json.dump({"timestamp": time.time(), "location": loc, "data": data}, f)

        return format_weather(data)

    except Exception as e:
        return f"Weather error: {e}"

def format_weather(data):
    city = data.get("name", "Unknown")
    country = data.get("sys", {}).get("country", "")
    temp = data.get("main", {}).get("temp", "?")
    desc = data.get("weather", [{}])[0].get("description", "no data")
    return f"{city}, {country}: {temp}°C, {desc.capitalize()}"

def scan_news():
    api_key = get_api_key("newsapi")
    if not api_key:
        return ["Missing NewsAPI key."]

    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            return [f"News error: {response.status_code}"]

        data = response.json()
        articles = data.get("articles", [])
        headlines = [article["title"] for article in articles[:5]]
        return headlines if headlines else ["No headlines found."]

    except Exception as e:
        return [f"News error: {e}"]