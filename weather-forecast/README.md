# OpenWeather AI Dashboard 🌤️

An AI-powered weather forecasting application built with Streamlit and OpenAI. This project allows users to retrieve real-time weather data for any city via OpenWeatherMap and receive personalized, context-aware activity recommendations based on the current forecast.

This project is part of a broader collection of LLM applications.

## Project Overview

*   **Mission:** It eliminates the need for developers to host expensive API keys or manage user data by allowing users to securely bring their own OpenAI and OpenWeatherMap API keys to get instant, AI-interpreted local weather insights.
*   **Technologies Used:** Python, Streamlit (Frontend/UI), OpenAI API (LLM Analysis), OpenWeatherMap API (Weather data generation), Requests, and Pandas.
*   **Project Detail:** A lightweight, modular dashboard that fetches real-time weather metrics (temperature, humidity, atmospheric conditions) for any global city and uses GPT models to generate personalized, human-readable activity recommendations for the day.

## Key Features

*   **Real-Time Weather Data:** Fetches up-to-date weather metrics (temperature, humidity, condition summaries) using the OpenWeatherMap API.
*   **AI-Powered Insights:** Utilizes OpenAI's GPT models to provide human-readable advice and recommendations based on local weather conditions.
*   **User-Controlled Privacy (BYOK):** Features a "Bring Your Own Key" architecture. Users securely provide both their OpenAI and OpenWeatherMap API keys directly within the app interface.
*   **Session Security:** API keys are used strictly in volatile memory during the active session and are never logged, stored, or saved in the repository.

## Prerequisites

*   Python 3.8 or higher
*   An active [OpenAI API Key](https://platform.openai.com/api-keys)
*   An active [OpenWeatherMap API Key](https://home.openweathermap.org/users/sign_up)

## Setup & Installation

**1. Navigate to the project directory**
Ensure you are in the specific folder for this project:
```bash
cd weather-forecast
```
2. Install required dependencies
It is recommended to use a virtual environment, but you can install the dependencies directly via:

```Bash
pip install -r requirements.txt
```
Usage
1. Launch the Streamlit application
Start the local server by running:

```Bash
streamlit run app.py
```
2. Interact with the Dashboard

Open the local URL provided in your terminal (usually http://localhost:8501).

Enter your OpenAI API Key and OpenWeatherMap API Key in the secure sidebar input fields.

Input the name of the city you want to check.

Click "Get Forecast" to retrieve the current weather metrics and the AI-generated recommendation.

Project Structure

```app.py```: The main Streamlit application containing the frontend UI and execution logic.

```utils/weather.py```: A helper module responsible for processing and fetching current weather data from the OpenWeatherMap API.

```requirements.txt```: The required Python packages for running the dashboard.

License

This project is licensed under the MIT License.
