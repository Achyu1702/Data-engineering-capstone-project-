# 2nd step store weather data into postgresql 
import requests
import psycopg2
from psycopg2 import sql

# ----------------------------
# 1. API Setup
# ----------------------------
API_KEY = "09bff7d03f3cb1ec8777627ac285380b"
lat, lon = 19.076, 72.8777  # Mumbai
url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

# ----------------------------
# 2. PostgreSQL Connection
# ----------------------------
conn = psycopg2.connect(
    dbname="weather_db",   # your database name
    user="postgres",       # your username (default: postgres)
    password="Achyut@2006",  # <-- replace with your actual password
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# ----------------------------
# 3. Create Table (if not exists)
# ----------------------------
create_table_query = """
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    date_time TIMESTAMP,
    temperature FLOAT,
    humidity INT,
    wind_speed FLOAT,
    rainfall FLOAT
);
"""
cur.execute(create_table_query)
conn.commit()

# ----------------------------
# 4. Fetch Weather Data
# ----------------------------
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    city_name = data['city']['name']

    insert_query = """
    INSERT INTO weather_data (city, date_time, temperature, humidity, wind_speed, rainfall)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for entry in data['list']:
        dt = entry['dt_txt']
        temp = entry['main']['temp']
        humidity = entry['main']['humidity']
        wind = entry['wind']['speed']
        rain = entry.get('rain', {}).get('3h', 0.0)  # rainfall may not always be present

        cur.execute(insert_query, (city_name, dt, temp, humidity, wind, rain))

    conn.commit()
    print("✅ Weather data inserted successfully into PostgreSQL!")

else:
    print("❌ Failed to fetch data:", response.status_code)

# ----------------------------
# 5. Close Connection
# ----------------------------
cur.close()
conn.close()
