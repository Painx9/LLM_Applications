import streamlit as st
from openai import OpenAI
from utils.weather import get_weather

st.set_page_config(page_title="Weather AI Dashboard", layout="centered")

st.title("🌤️ AI Weather Assistant")

# Sidebar for credentials
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    st.info("Your key is used only for this session.")

city = st.text_input("Enter city name", "Cottbus")

if st.button("Get Forecast"):
    if not api_key:
        st.error("Please enter an OpenAI API key in the sidebar.")
    else:
        with st.spinner("Fetching weather..."):
            weather = get_weather(city)
            
            if not weather:
                st.error("City not found.")
            else:
                # Display metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Temp", f"{weather['temperature_2m']}°C")
                col2.metric("Humidity", f"{weather['relative_humidity_2m']}%")
                col3.metric("Rain", f"{weather['precipitation']}mm")
                
                # AI Analysis
                client = OpenAI(api_key=api_key)
                prompt = f"The current weather in {city} is {weather['temperature_2m']}°C with {weather['relative_humidity_2m']}% humidity. Give a short, helpful recommendation for the day."
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown("### 🤖 AI Insight")
                st.write(response.choices[0].message.content)
