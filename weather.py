# weather.py

import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city_name: str):
    """
    Fetch live weather data for a given city using OpenWeather API.
    Returns a dictionary with temperature, humidity, rainfall, and description.
    """
    if not API_KEY:
        raise ValueError("API Key not found. Please set OPENWEATHER_API_KEY in .env file.")

    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code != 200:
            return {"error": data.get("message", "Failed to fetch weather")}

        weather_info = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "rainfall": data.get("rain", {}).get("1h", 0),  # rainfall in mm (last 1 hour if available)
            "description": data["weather"][0]["description"]
        }

        return weather_info

    except requests.RequestException as e:
        return {"error": str(e)}
