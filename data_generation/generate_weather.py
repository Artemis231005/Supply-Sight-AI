import random
import pandas as pd
from datetime import timedelta

from config import RANDOM_SEED
random.seed(RANDOM_SEED)

START_DATE = "2023-01-01"
END_DATE = "2025-12-31"

CITY_DATA = [
    ("New Delhi", "Delhi", 15),
    ("Mumbai", "Maharashtra", 18),
    ("Bengaluru", "Karnataka", 15),
    ("Chennai", "Tamil Nadu", 12),
    ("Ahmedabad", "Gujarat", 10),
    ("Noida", "Uttar Pradesh", 10),
    ("Pune", "Maharashtra", 8),
    ("Ghaziabad", "Uttar Pradesh", 4),
    ("Lucknow", "Uttar Pradesh", 3),
    ("Kanpur", "Uttar Pradesh", 2),
    ("Nagpur", "Maharashtra", 1),
    ("Mangalore", "Karnataka", 1),
    ("Coimbatore", "Tamil Nadu", 1)
]

def generate_weather(city, month):
    climate = {
        "New Delhi": {
            "summer": (36, 46),
            "winter": (8, 20),
            "monsoon": (27, 36),
            "humidity": (35, 90),
            "rain_mult": 1.0
        },

        "Mumbai": {
            "summer": (30, 37),
            "winter": (20, 31),
            "monsoon": (25, 32),
            "humidity": (65, 98),
            "rain_mult": 2.0
        },

        "Bengaluru": {
            "summer": (27, 35),
            "winter": (15, 28),
            "monsoon": (21, 29),
            "humidity": (50, 92),
            "rain_mult": 1.2
        },

        "Chennai": {
            "summer": (33, 42),
            "winter": (21, 31),
            "monsoon": (25, 34),
            "humidity": (60, 95),
            "rain_mult": 1.5
        },

        "Ahmedabad": {
            "summer": (36, 46),
            "winter": (12, 28),
            "monsoon": (27, 36),
            "humidity": (35, 85),
            "rain_mult": 0.8
        },

        "Noida": {
            "summer": (36, 45),
            "winter": (8, 20),
            "monsoon": (27, 35),
            "humidity": (35, 90),
            "rain_mult": 1.0
        },

        "Pune": {
            "summer": (28, 37),
            "winter": (14, 27),
            "monsoon": (22, 30),
            "humidity": (50, 95),
            "rain_mult": 1.3
        },

        "Ghaziabad": {
            "summer": (36, 45),
            "winter": (8, 20),
            "monsoon": (27, 35),
            "humidity": (35, 90),
            "rain_mult": 1.0
        },

        "Lucknow": {
            "summer": (35, 44),
            "winter": (9, 22),
            "monsoon": (27, 35),
            "humidity": (40, 90),
            "rain_mult": 1.0
        },

        "Kanpur": {
            "summer": (36, 45),
            "winter": (8, 21),
            "monsoon": (27, 35),
            "humidity": (40, 90),
            "rain_mult": 1.0
        },

        "Nagpur": {
            "summer": (37, 47),
            "winter": (12, 28),
            "monsoon": (26, 34),
            "humidity": (35, 88),
            "rain_mult": 0.9
        },

        "Mangalore": {
            "summer": (29, 35),
            "winter": (20, 31),
            "monsoon": (23, 30),
            "humidity": (70, 99),
            "rain_mult": 2.5
        },

        "Coimbatore": {
            "summer": (29, 37),
            "winter": (18, 29),
            "monsoon": (22, 30),
            "humidity": (55, 92),
            "rain_mult": 1.3
        }
    }

    c = climate[city]
    humidity = random.randint(*c["humidity"])
    
    if month in [12, 1, 2]:
        temp = random.randint(*c["winter"])
        rainfall = random.choice([0]*10 + [2, 4])

        condition = random.choices(
            ["Sunny", "Cloudy", "Fog", "Rain"],
            weights=[60, 18, 17, 5]
        )[0]

    elif month in [3]:
        low = min(c["winter"][1], c["summer"][0])
        high = max(c["winter"][1], c["summer"][0])

        temp = random.randint(low, high)
        rainfall = random.choice([0]*8 + [3, 5, 8])

        condition = random.choices(
            ["Sunny", "Cloudy", "Rain"],
            weights=[70, 20, 10]
        )[0]

    elif month in [4, 5, 6]:
        temp = random.randint(*c["summer"])
        rainfall = int(random.randint(0, 10) * c["rain_mult"])

        condition = random.choices(
            ["Sunny", "Cloudy", "Heatwave"],
            weights=[72, 18, 10]
        )[0]

    elif month in [7, 8, 9]:
        temp = random.randint(*c["monsoon"])
        rainfall = int(random.randint(10, 90) * c["rain_mult"])

        condition = random.choices(
            ["Rain", "Heavy Rain", "Cloudy", "Storm"],
            weights=[42, 28, 20, 10]
        )[0]

    else:
        temp = random.randint(
            c["monsoon"][0]-2,
            c["monsoon"][1]
        )
        rainfall = int(random.randint(0, 20) * c["rain_mult"])

        condition = random.choices(
            ["Sunny", "Cloudy", "Rain"],
            weights=[60, 25, 15]
        )[0]

    if condition == "Storm":
        wind = random.randint(35, 60)
    elif condition == "Heavy Rain":
        wind = random.randint(20, 35)
    else:
        wind = random.randint(5, 20)

    if condition == "Storm":
        severity = "Severe"
    elif condition in ["Heavy Rain", "Heatwave"]:
        severity = "High"
    elif condition in ["Rain", "Fog"]:
        severity = "Moderate"
    else:
        severity = "Normal"

    return (
        temp,
        humidity,
        rainfall,
        wind,
        condition,
        severity
    )


dates = pd.date_range(START_DATE, END_DATE)
rows = []
sys_id = 1

for date in dates:
    for city, state, _ in CITY_DATA:
        (   temp,
            humidity,
            rainfall,
            wind,
            condition,
            severity
        ) = generate_weather(city, date.month)

        rows.append({
            "WeatherSysID":
                f"SYSWEA{sys_id:07d}",
            "WeatherID":
                f"WTH{random.randint(100000,999999)}",
            "City":
                city,
            "State":
                state,
            "Date":
                date.date(),
            "TemperatureC":
                temp,
            "HumidityPercent":
                humidity,
            "RainfallMM":
                rainfall,
            "WindSpeedKmph":
                wind,
            "WeatherCondition":
                condition,
            "WeatherSeverity":
                severity
        })
        sys_id += 1


weather = pd.DataFrame(rows)

weather.to_csv(
    "data_generation/Weather Data.csv",
    index=False
)

print(weather.head())
print(f"\nGenerated {len(weather):,} weather records.")