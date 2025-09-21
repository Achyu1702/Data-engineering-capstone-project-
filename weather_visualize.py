# step 3: visualize 
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# 1. Connect to PostgreSQL
# ----------------------------
conn = psycopg2.connect(
    dbname="weather_db",
    user="postgres",
    password="Achyut@2006",  # <-- replace with your password
    host="localhost",
    port="5432"
)

# ----------------------------
# 2. Load Data into Pandas
# ----------------------------
query = "SELECT date_time, temperature, humidity, wind_speed, rainfall FROM weather_data WHERE city='Konkan Division' ORDER BY date_time;"
df = pd.read_sql(query, conn)
conn.close()

# Convert datetime
df['date_time'] = pd.to_datetime(df['date_time'])

# ----------------------------
# 3. Plot Graphs
# ----------------------------

# Temperature trend
plt.figure(figsize=(10,5))
plt.plot(df['date_time'], df['temperature'])
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.title("Temperature Trend - Last 30 Days (Konkan Division)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Humidity trend
plt.figure(figsize=(10,5))
plt.plot(df['date_time'], df['humidity'])
plt.xlabel("Date")
plt.ylabel("Humidity (%)")
plt.title("Humidity Trend - Last 30 Days")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Rainfall trend
plt.figure(figsize=(10,5))
plt.plot(df['date_time'], df['rainfall'])
plt.xlabel("Date")
plt.ylabel("Rainfall (mm)")
plt.title("Rainfall Trend - Last 30 Days")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
