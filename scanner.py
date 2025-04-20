import requests
import os
import json
import time
from utils import get_api_key

WEATHER_CACHE_FILE = os.path.join("data", "cached_weather.json")
NEWS_CACHE_FILE = os.path.join("data", "cached_news.json")
IPINFO_CACHE_FILE = os.path.join("data", "cached_ipinfo.json")
WEATHER_CACHE_DURATION = 15 * 60  # 15 minutes
NEWS_CACHE_DURATION = 3 * 60 * 60  # 3 hours
IPINFO_CACHE_DURATION = 3 * 60 * 60  # 3 hours

def scan_ipinfo():
    if os.path.exists(IPINFO_CACHE_FILE):
        with open(IPINFO_CACHE_FILE, "r") as f:
            cached = json.load(f)
            if time.time() - cached.get("timestamp", 0) < IPINFO_CACHE_DURATION:
                return cached.get("geo", {})

    try:
        geo = requests.get("https://ipinfo.io/json").json()
        with open(IPINFO_CACHE_FILE, "w") as f:
            json.dump({"timestamp": time.time(), "geo": geo}, f)
        return geo
    except Exception as e:
        return {"error": str(e)}

def scan_weather(location=None):
    api_key = get_api_key("openweathermap")
    if not api_key:
        return "Missing API key."

    try:
        geo = scan_ipinfo()
        loc = geo.get("loc", "")
        city = geo.get("city", "Unknown")
        country = geo.get("country", "Unknown")

        if not loc:
            return "Could not determine location."

        lat, lon = loc.split(",")

        if os.path.exists(WEATHER_CACHE_FILE):
            with open(WEATHER_CACHE_FILE, "r") as f:
                cached = json.load(f)
                cached_loc = cached.get("location", "")
                if (
                    time.time() - cached.get("timestamp", 0) < WEATHER_CACHE_DURATION
                    and cached_loc == loc
                ):
                    return format_weather(cached["data"])

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") != 200:
            return f"Weather error: {data.get('message', 'unknown error')}"

        with open(WEATHER_CACHE_FILE, "w") as f:
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

def scan_news(category="general"):
    api_key = get_api_key("newsapi")
    if not api_key:
        return ["Missing NewsAPI key."]

    try:
        cache_key = f"{category.lower()}"
        if os.path.exists(NEWS_CACHE_FILE):
            with open(NEWS_CACHE_FILE, "r") as f:
                cached = json.load(f)
                cached_data = cached.get(cache_key, {})
                if time.time() - cached_data.get("timestamp", 0) < NEWS_CACHE_DURATION:
                    return cached_data.get("headlines", [])

        url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&pageSize=20&apiKey={api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            return [f"News error: {response.status_code}"]

        data = response.json()
        articles = data.get("articles", [])
        headlines = articles[:20]

        if os.path.exists(NEWS_CACHE_FILE):
            with open(NEWS_CACHE_FILE, "r") as f:
                cached = json.load(f)
        else:
            cached = {}

        cached[cache_key] = {"timestamp": time.time(), "headlines": headlines}

        with open(NEWS_CACHE_FILE, "w") as f:
            json.dump(cached, f)

        return headlines if headlines else ["No headlines found."]

    except Exception as e:
        return [f"News error: {e}"]