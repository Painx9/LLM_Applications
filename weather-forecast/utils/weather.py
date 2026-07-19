import requests

def get_weather(city_name, owm_api_key):
    """
    Fetches real-time weather data using the OpenWeatherMap API.
    """
    # Using metric units for Celsius
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={owm_api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
        
    data = response.json()
    
    # Extracting standard fields from the JSON response
    weather_data = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "city": data["name"],
        "country": data["sys"]["country"]
    }
    
    return weather_data
