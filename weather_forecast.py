# step 4 ML 
import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# ----------------------------
# 1. Connect to PostgreSQL
# ----------------------------
conn = psycopg2.connect(
    dbname="weather_db",
    user="postgres",
    password="Achyut@2006",  # <-- replace with your actual password
    host="localhost",
    port="5432"
)

# ----------------------------
# 2. Load Data
# ----------------------------
query = "SELECT date_time, temperature FROM weather_data WHERE city='Konkan Division' ORDER BY date_time;"
df = pd.read_sql(query, conn)
conn.close()

df['date_time'] = pd.to_datetime(df['date_time'])
df['day'] = np.arange(len(df))  # convert date into numerical index

# ----------------------------
# 3. Train Linear Regression Model
# ----------------------------
X = df[['day']]
y = df['temperature']

model = LinearRegression()
model.fit(X, y)

# ----------------------------
# 4. Forecast Next 7 Days
# ----------------------------
future_days = np.arange(len(df), len(df)+7).reshape(-1, 1)
forecast = model.predict(future_days)

print("📈 7-Day Forecasted Temperatures:")
for i, temp in enumerate(forecast, 1):
    print(f"Day {i}: {temp:.2f} °C")

# ----------------------------
# 5. Plot Actual vs Forecast
# ----------------------------
plt.figure(figsize=(10,5))
plt.plot(df['date_time'], df['temperature'], label="Actual Temperature")
plt.plot(
    pd.date_range(df['date_time'].iloc[-1] + pd.Timedelta(hours=3), periods=7, freq='D'),
    forecast,
    label="Forecasted Temperature",
    linestyle="--",
    marker="o"
)
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.title("Temperature Forecast - Next 7 Days")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
