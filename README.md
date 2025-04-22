# Brief

Brief is a minimalist desktop widget that displays real-time weather and news headlines in a compact format. It uses themed sections, cached API calls, and a lightweight interface built with tkinter.

Features:

Weather from OpenWeatherMap
Headlines via NewsAPI.org and gnews.io
Caching to reduce API load
Themes

# Dev Note
The program (as of app_07) works, but you need to add api keys (using the third x button on the gui) for [OpenWeatherMap](https://openweathermap.org/), [NewAPI](https://newsapi.org/), and [gnews.io](https://gnews.io/). Click apply once you've added the keys and reset the app. Currently the app will only get local news based on your IP address, if you're using a VPN it'll get news and weather for your location but use your system time for the hours (i'll change this later) 
