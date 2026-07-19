import requests

def get_weather(city_name):
    # 1. Get coordinates for the city
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    geo_res = requests.get(geo_url).json()
    
    if "results" not in geo_res:
        return None
    
    data = geo_res["results"][0]
    lat, lon = data["latitude"], data["longitude"]
    
    # 2. Get weather forecast
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,weather_code"
    response = requests.get(weather_url).json()
    return response["current"]
