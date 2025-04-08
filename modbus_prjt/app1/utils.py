import requests
import os

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/onecall"

def get_forecast(lat=13.41, lon=122.56):  # Example: Philippines coords
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "current,minutely,hourly,alerts",
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        forecast = []

        for day in data.get('daily', [])[:7]:
            forecast.append({
                "date": day["dt"],
                "temperature": {
                    "min": day["temp"]["min"],
                    "max": day["temp"]["max"],
                },
                "rain": day.get("rain", 0),
                "weather": day["weather"][0]["description"].capitalize(),
                "icon": day["weather"][0]["icon"],
            })
        return forecast
    except Exception as e:
        print("Error:", e)
        return []
