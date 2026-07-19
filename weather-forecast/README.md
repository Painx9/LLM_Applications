# Live Weather Dashboard 🌤️

A secure, real-time weather application built with Streamlit. This dashboard fetches current weather metrics for any global city directly via the OpenWeatherMap API.

This project is part of a broader collection of Python applications.

## Project Overview

*   **Mission:** To provide a clean, lightweight interface for developers and users to check live global weather conditions securely using their own API credentials.
*   **Technologies Used:** Python, Streamlit (Frontend/UI), OpenWeatherMap API (Weather data generation), Requests, and Pandas.
*   **Project Detail:** A modular dashboard that fetches real-time weather metrics (temperature, humidity, atmospheric conditions) for any city without saving or logging user credentials.

## Key Features

*   **Real-Time Weather Data:** Fetches up-to-date weather metrics using the OpenWeatherMap API.
*   **User-Controlled Privacy:** Features a secure architecture where users provide their OpenWeatherMap API key directly within the app interface.
*   **Session Security:** API keys are used strictly in volatile memory during the active session and are never logged, stored, or saved in the repository.

## Prerequisites

*   Python 3.8 or higher
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

Enter your OpenWeatherMap API Key in the secure sidebar input fields.

Input the name of the city you want to check.

Click "Get Forecast" to retrieve the current weather metrics and the AI-generated recommendation.

Project Structure

```app.py```: The main Streamlit application containing the frontend UI and execution logic.

```utils/weather.py```: A helper module responsible for processing and fetching current weather data from the OpenWeatherMap API.

```requirements.txt```: The required Python packages for running the dashboard.

License

This project is licensed under the MIT License.
