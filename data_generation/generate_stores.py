import random
import pandas as pd
from faker import Faker

from config import NUM_STORES, RANDOM_SEED

random.seed(RANDOM_SEED)
fake = Faker("en_IN")
Faker.seed(RANDOM_SEED)

CITY_DATA = [
    ("New Delhi", "Delhi", 18),
    ("Mumbai", "Maharashtra", 20),
    ("Bengaluru", "Karnataka", 16),
    ("Chennai", "Tamil Nadu", 14),
    ("Ahmedabad", "Gujarat", 10),
    ("Noida", "Uttar Pradesh", 10),
    ("Pune", "Maharashtra", 8),
    ("Ghaziabad", "Uttar Pradesh", 6),
    ("Lucknow", "Uttar Pradesh", 5),
    ("Kanpur", "Uttar Pradesh", 4),
    ("Nagpur", "Maharashtra", 3),
    ("Mangalore", "Karnataka", 2),
    ("Coimbatore", "Tamil Nadu", 2),
    ("Surat", "Gujarat", 4)
]

STORE_TYPES = [
    "Hypermarket",
    "Supermarket",
    "Convenience Store"
]

NAME_PREFIXES = [
    "Fresh",
    "Daily",
    "Smart",
    "Urban",
    "Metro",
    "Value",
    "Prime",
    "Family",
    "Quick",
    "City",
    "Green",
    "Happy",
    "Elite",
    "Nova",
    "Big",
    "Reliance"
]

NAME_SUFFIXES = [
    "Mart",
    "Store",
    "Retail",
    "Market",
    "Outlet",
    "Superstore",
    "Bazaar"
]

STORE_LOCATION_TYPES = [
    "Mall",
    "High Street",
    "Commercial",
    "Residential",
    "Rural"
]

rows = []
used_store_ids = set()

for i in range(1, NUM_STORES + 1):

    while True:
        store_id = f"STR{random.randint(100000,999999)}"

        if store_id not in used_store_ids:
            used_store_ids.add(store_id)
            break

    city, state, _ = random.choices(
        CITY_DATA,
        weights=[x[2] for x in CITY_DATA],
        k=1
    )[0]

    store_name = (
        random.choice(NAME_PREFIXES)
        + " "
        + random.choice(NAME_SUFFIXES)
    )

    tier1_cities = [
        "Mumbai",
        "New Delhi",
        "Bengaluru",
        "Chennai"
    ]

    tier2_cities = [
        "Noida",
        "Pune",
        "Ahmedabad",
        "Ghaziabad"
    ]

    if city in tier1_cities:
        store_type = random.choices(
            STORE_TYPES,
            weights=[25, 55, 20]
        )[0]
    elif city in tier2_cities:
        store_type = random.choices(
            STORE_TYPES,
            weights=[10, 60, 30]
        )[0]
    else:
        store_type = random.choices(
            STORE_TYPES,
            weights=[5, 40, 55]
        )[0]

    if store_type == "Hypermarket":
        if city in tier1_cities:
            floor_area = random.randint(60000, 100000)
        else:
            floor_area = random.randint(45000, 70000)
    elif store_type == "Supermarket":
        if city in tier1_cities:
            floor_area = random.randint(18000, 35000)
        else:
            floor_area = random.randint(12000, 25000)
    else: 
        floor_area = random.randint(1500, 8000)
        
    if city in tier1_cities:
        store_location_type = random.choices(
            STORE_LOCATION_TYPES,
            weights=[30, 40, 15, 10, 5]
        )[0]
    elif city in tier2_cities:
        store_location_type = random.choices(
            STORE_LOCATION_TYPES,
            weights=[15, 35, 20, 20, 10]
        )[0]
    else:
        store_location_type = random.choices(
            STORE_LOCATION_TYPES,
            weights=[5, 15, 20, 35, 25]
        )[0]

    opening_year = random.randint(2000, 2025)
    active_status = random.choices(
        ["Active", "Inactive"],
        weights=[97, 3]
    )[0]

    rows.append({
        "StoreSysID": f"SYSST{i:07d}",
        "StoreID": store_id,
        "StoreName": store_name,
        "StoreType": store_type,
        "City": city,
        "State": state,
        "StoreLocationType": store_location_type,
        "Manager": fake.name(),
        "OpeningYear": opening_year,
        "FloorAreaSqFt": floor_area,
        "ActiveStatus": active_status
    })

stores = pd.DataFrame(rows)

stores.to_csv(
    "data_generation/Store Data.csv",
    index=False
)

print(stores.head())
print(f"\nGenerated {len(stores)} store records")