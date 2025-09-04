import os
import requests
from typing import Literal
from pydantic import BaseModel, Field
from langchain.tools import tool


OPENWEATHER_BASE_GEOCODE = "https://api.openweathermap.org/geo/1.0/direct"
OPENWEATHER_ONECALL = "https://api.openweathermap.org/data/3.0/onecall"


class WeatherArgs(BaseModel):
    """ Weather lookup by place, name and day offset """
    location: str = Field(
        ...,
        description="City name, state code (only for the US) and country "
                    "code divided by comma. Please use ISO 3166 country codes."
    )
    days_ahead: int = Field(0, ge=0, le=8, description="0=today, 1=tomorrow...")
    units: Literal["metric", "imperial"] = Field("metric", description="Units for temperature/wind")


def _geocode(q: str, api_key: str):
    """ Geocodes a place name to lat/lon using OpenWeatherMap Geocoding API. """
    resp = requests.get(OPENWEATHER_BASE_GEOCODE, params={"q": q, "limit": 1, "appid": api_key}, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        raise ValueError(f"Could not geocode '{q}'. Try a more specific place.")
    top = data[0]
    return {"name": top.get("name"), "lat": top["lat"], "lon": top["lon"], "country": top.get("country"), "state": top.get("state")}


def _onecall(lat: float, lon: float, units: str, api_key: str):
    """ Fetches weather data for given lat/lon using OpenWeatherMap One Call API. """
    params = {"lat": lat, "lon": lon, "units": units, "exclude": "minutely,alerts", "appid": api_key}
    resp = requests.get(OPENWEATHER_ONECALL, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


@tool("get_weather", args_schema=WeatherArgs)
def get_weather(location: str, days_ahead: int = 0, units: str = "metric"):
    """
    Fetches current conditions and the days_ahead day's daily forecast for a location.
    Returns a concise dict for easy, readable use in answers.
    """
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY not set.")
    try:
        geo = _geocode(location, api_key)
        data = _onecall(geo["lat"], geo["lon"], units, api_key)
        current = data.get("current", {})
        daily = data.get("daily", [])
        day = daily[min(days_ahead, len(daily)-1)] if daily else {}

        def _desc(w):
            try:
                return w["weather"][0]["description"]
            except Exception as ex:
                print(ex)
                return None

        summary = {
            "place": {
                "name": geo.get("name"),
                "country": geo.get("country"),
                "state": geo.get("state"),
                "lat": geo["lat"],
                "lon": geo["lon"],
            },
            "units": units,
            "current": {
                "temp": current.get("temp"),
                "feels_like": current.get("feels_like"),
                "humidity": current.get("humidity"),
                "wind_speed": current.get("wind_speed"),
                "description": _desc(current),
            },
            "selected_day": {
                "index": days_ahead,
                "min": day.get("temp", {}).get("min"),
                "max": day.get("temp", {}).get("max"),
                "pop": day.get("pop"),
                "uvi": day.get("uvi"),
                "description": _desc(day),
            },
        }
        return summary
    except requests.HTTPError as e:
        return {"error": f"OpenWeather HTTP error: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"Weather tool failed: {e}"}
