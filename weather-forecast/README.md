# Weather Forecast Dashboard 🌤️

An AI-powered weather forecasting application built with Streamlit and OpenAI. This project allows users to retrieve real-time weather data for any city and receive personalized, context-aware activity recommendations based on the current forecast.

This project is part of a broader collection of LLM applications.

## Key Features

*   **Real-Time Weather Data:** Fetches up-to-date weather metrics (temperature, humidity, precipitation) using the free Open-Meteo API.
*   **AI-Powered Insights:** Utilizes OpenAI's GPT models to provide human-readable advice and recommendations based on local weather conditions.
*   **User-Controlled Privacy (BYOK):** Features a "Bring Your Own Key" architecture. Users provide their OpenAI API key directly within the app interface.
*   **Session Security:** API keys are used strictly in volatile memory during the active session and are never logged, stored, or saved in the repository.

## Prerequisites

*   Python 3.8 or higher
*   An active [OpenAI API Key](https://platform.openai.com/api-keys)

## Setup & Installation

**1. Navigate to the project directory**
Ensure you are in the specific folder for this project:
```bash
cd weather-forecast
```
2. Install required dependencies
It is recommended to use a virtual environment, but you can install the dependencies directly via:
```bash
pip install -r requirements.txt
```
Usage
1. Launch the Streamlit application
Start the local server by running:
```bash
streamlit run app.py
```
2. Interact with the Dashboard

Open the local URL provided in your terminal (usually http://localhost:8501).

Enter your OpenAI API Key in the secure sidebar input field.

Input the name of the city you want to check.

Click "Get Forecast" to retrieve the current weather metrics and the AI-generated recommendation.

Project Structure

```app.py```: The main Streamlit application containing the frontend UI and execution logic.

```utils/weather.py```: A helper module responsible for geocoding and fetching weather data from the Open-Meteo API.

```requirements.txt```: The required Python packages for running the dashboard.

## License

This project is licensed under the MIT License.
