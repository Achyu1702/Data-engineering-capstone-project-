# step 1 fetch weather data 

import requests
import datetime

# Your OpenWeatherMap API Key
API_KEY = "09bff7d03f3cb1ec8777627ac285380b"

# Location (Mumbai as example)
lat, lon = 19.076, 72.8777  

# API Endpoint (5-day forecast, every 3 hours)
url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

# Fetch Data
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    city_name = data['city']['name']
    
    print(f"✅ Weather data for: {city_name}\n")
    
    # Loop through forecast entries
    for entry in data['list'][:10]:  # printing only first 10 for now
        date_time = entry['dt_txt']
        temp = entry['main']['temp']
        humidity = entry['main']['humidity']
        wind_speed = entry['wind']['speed']
        rainfall = entry.get('rain', {}).get('3h', 0.0)  # some entries may not have rain
        
        print(f"Date: {date_time} | Temp: {temp}°C | Humidity: {humidity}% | "
              f"Wind: {wind_speed} m/s | Rain: {rainfall} mm")
else:
    print("❌ Failed to fetch data:", response.status_code)
