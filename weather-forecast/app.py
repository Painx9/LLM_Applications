import streamlit as st
from utils.weather import get_weather

st.set_page_config(page_title="Weather Dashboard", layout="centered")

st.title("🌤️ Live Weather Dashboard")

# Sidebar for credentials
with st.sidebar:
    st.header("API Settings")
    owm_api_key = st.text_input("Enter OpenWeatherMap API Key", type="password")
    st.info("Your key is used securely only during this session and is not stored.")

# Main interface
city = st.text_input("Enter city name", "Cottbus")

if st.button("Get Forecast"):
    if not owm_api_key:
        st.error("Please enter your OpenWeatherMap API key in the sidebar.")
    else:
        with st.spinner("Fetching weather from OpenWeatherMap..."):
            weather = get_weather(city, owm_api_key)
            
            if not weather:
                st.error("City not found or invalid OpenWeatherMap API key.")
            else:
                # Display metrics
                st.write(f"### Current conditions for {weather['city']}, {weather['country']}")
                
                # Visualizing data with columns
                col1, col2, col3 = st.columns(3)
                col1.metric("Temperature", f"{weather['temperature']}°C")
                col2.metric("Humidity", f"{weather['humidity']}%")
                col3.metric("Condition", weather['description'].title())
