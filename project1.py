import streamlit as st
import requests
import os

def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY", "bf0edbee7f57e05a45282e906d848457")
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}&units=metric"
    
    try:
        response = requests.get(complete_url)
        response.raise_for_status()
        data = response.json()
        
        if data["cod"] != "404":
            main = data["main"]
            weather = data["weather"][0]
            
            weather_info = {
                "Temperature": f"{main['temp']}°C",
                "Pressure": f"{main['pressure']} hPa",
                "Humidity": f"{main['humidity']}%",
                "Description": weather["description"].capitalize()
            }
            return weather_info, None
        else:
            return None, "City Not Found!"
    except requests.exceptions.RequestException as e:
        return None, f"API request failed: {e}"

# Streamlit UI
st.title("🌍 OpenWeatherMap Real-Time Weather App")
st.write("Enter a city name to get the latest weather details.")

city_name = st.text_input("City Name", "Mumbai")

if st.button("Get Weather"):
    weather, error = get_weather(city_name)
    
    if error:
        st.error(error)
    else:
        st.subheader(f"Weather in {city_name}")
        st.metric("🌡 Temperature", weather["Temperature"])
        st.metric("🔵 Pressure", weather["Pressure"])
        st.metric("💧 Humidity", weather["Humidity"])
        st.write(f"**Condition:** {weather['Description']}")
