import streamlit as st
import openai
from openai import OpenAI
from utils.weather import get_weather

st.set_page_config(page_title="Weather AI Dashboard", layout="centered")

st.title("🌤️ AI Weather Assistant")

# Sidebar for credentials
with st.sidebar:
    st.header("API Settings")
    openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
    owm_api_key = st.text_input("Enter OpenWeatherMap API Key", type="password")
    st.info("Your keys are used securely only during this session.")

# Main interface
city = st.text_input("Enter city name", "Cottbus")

if st.button("Get Forecast"):
    if not openai_api_key or not owm_api_key:
        st.error("Please enter both the OpenAI and OpenWeatherMap API keys in the sidebar.")
    else:
        with st.spinner("Fetching weather from OpenWeatherMap..."):
            weather = get_weather(city, owm_api_key)
            
            if not weather:
                st.error("City not found or invalid OpenWeatherMap API key.")
            else:
                # Display metrics
                st.write(f"### Current conditions for {weather['city']}, {weather['country']}")
                col1, col2, col3 = st.columns(3)
                col1.metric("Temperature", f"{weather['temperature']}°C")
                col2.metric("Humidity", f"{weather['humidity']}%")
                col3.metric("Condition", weather['description'].title())
                
                # AI Analysis
                try:
                    with st.spinner("Generating AI insights..."):
                        client = OpenAI(api_key=openai_api_key)
                        prompt = f"The current weather in {weather['city']} is {weather['temperature']}°C with {weather['humidity']}% humidity and {weather['description']}. Give a short, helpful recommendation for the day."
                        
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        st.markdown("---")
                        st.markdown("### 🤖 AI Insight")
                        st.write(response.choices[0].message.content)

                # Catch OpenAI-specific errors gracefully
                except openai.RateLimitError:
                    st.error("⚠️ OpenAI Rate Limit Exceeded. Please ensure your API key has available credits.")
                except openai.AuthenticationError:
                    st.error("🔑 Invalid OpenAI API Key.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
