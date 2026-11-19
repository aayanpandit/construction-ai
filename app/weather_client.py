"""Live weather from Open-Meteo (free, no API key)."""
import httpx
from .schemas import DayForecast, WeatherSnapshot

WMO = {0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast", 45: "Fog", 48: "Fog",
       51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle", 61: "Light rain", 63: "Rain", 65: "Heavy rain",
       71: "Light snow", 73: "Snow", 75: "Heavy snow", 80: "Rain showers", 81: "Rain showers",
       82: "Violent rain showers", 95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with hail"}


def get_weather(city: str) -> WeatherSnapshot:
    """Raises LookupError if the city is unknown, httpx.HTTPError on network problems."""
    with httpx.Client(timeout=10) as c:
        geo = c.get("https://geocoding-api.open-meteo.com/v1/search", params={"name": city, "count": 1}).json()
        if not geo.get("results"):
            raise LookupError(city)
        place = geo["results"][0]
        data = c.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude": place["latitude"], "longitude": place["longitude"], "timezone": "auto", "forecast_days": 3,
            "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
        }).json()
    cur, d = data["current"], data["daily"]
    forecast = [
        DayForecast(date=d["time"][i], condition=WMO.get(d["weather_code"][i], "Unknown"),
                    temp_max_c=d["temperature_2m_max"][i], temp_min_c=d["temperature_2m_min"][i],
                    precipitation_mm=d["precipitation_sum"][i] or 0, wind_max_kmh=d["wind_speed_10m_max"][i])
        for i in range(len(d["time"]))
    ]
    label = f"{place['name']}, {place.get('admin1', '')}".strip(", ")
    return WeatherSnapshot(
        city=label, temperature_c=cur["temperature_2m"], humidity_pct=cur["relative_humidity_2m"],
        wind_kmh=cur["wind_speed_10m"], precipitation_mm=cur["precipitation"],
        condition=WMO.get(cur["weather_code"], "Unknown"), forecast=forecast,
    )
