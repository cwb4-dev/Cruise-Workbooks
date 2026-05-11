import urllib.request
import urllib.parse
import json

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Icy fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    77: "Snow grains",
    80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
}

RAINY_CODES = {51, 53, 55, 61, 63, 65, 71, 73, 75, 77, 80, 81, 82, 85, 86, 95, 96, 99}


def geocode(city):
    params = urllib.parse.urlencode({"name": city, "count": 1, "language": "en", "format": "json"})
    url = f"https://geocoding-api.open-meteo.com/v1/search?{params}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read())
    results = data.get("results")
    if not results:
        return None
    return results[0]


def get_weather(lat, lon):
    params = urllib.parse.urlencode({
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,weathercode",
        "temperature_unit": "celsius",
        "timezone": "auto",
    })
    url = f"https://api.open-meteo.com/v1/forecast?{params}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read())
    current = data["current"]
    return current["temperature_2m"], current["weathercode"]


def recommend(temp_c, weather_code):
    is_rainy = weather_code in RAINY_CODES
    if temp_c > 22 and not is_rainy:
        return "🌞 Lido Deck recommended"
    if temp_c < 18 or is_rainy:
        return "📚 Library recommended"
    return "☁️ Either works today"


def main():
    city = input("Enter city name: ").strip()
    if not city:
        print("No city entered.")
        return

    try:
        location = geocode(city)
    except Exception as e:
        print(f"Could not reach geocoding service: {e}")
        return

    if location is None:
        print(f"City '{city}' not found. Please check the spelling and try again.")
        return

    display_name = location.get("name", city)
    country = location.get("country", "")
    lat, lon = location["latitude"], location["longitude"]

    try:
        temp_c, weather_code = get_weather(lat, lon)
    except Exception as e:
        print(f"Could not fetch weather data: {e}")
        return

    temp_f = temp_c * 9 / 5 + 32
    condition = WEATHER_CODES.get(weather_code, f"Unknown (code {weather_code})")

    print(f"\nWeather for {display_name}{', ' + country if country else ''}:")
    print(f"  Temperature : {temp_c:.1f}°C / {temp_f:.1f}°F")
    print(f"  Condition   : {condition}")
    print(f"\n{recommend(temp_c, weather_code)}")


if __name__ == "__main__":
    main()
