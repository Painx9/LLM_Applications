import requests
import streamlit as st

def get_weather(city_name, owm_api_key):
    """
    Fetches real-time weather data and logs API errors directly to the console/UI.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={owm_api_key}&units=metric"
    response = requests.get(url)
    
    # If it fails, let's look under the hood
    if response.status_code != 200:
        error_details = response.json()
        # This will print the exact reason in your terminal console
        print(f"--- API ERROR ({response.status_code}) ---")
        print(f"Message from OpenWeatherMap: {error_details.get('message')}")
        print("---------------------------------------")
        
        # This will also show a small warning banner in your Streamlit app
        st.warning(f"API Code {response.status_code}: {error_details.get('message')}")
        return None
        
    data = response.json()
    
    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "city": data["name"],
        "country": data["sys"]["country"]
    }
