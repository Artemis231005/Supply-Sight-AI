import random
import pandas as pd
from faker import Faker

from config import NUM_WAREHOUSES, RANDOM_SEED

random.seed(RANDOM_SEED)
fake = Faker("en_IN")
Faker.seed(RANDOM_SEED)

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

WAREHOUSE_TYPES = [
    "National Distribution Center",
    "Regional Distribution Center",
    "Fulfillment Center"
]

NAME_PREFIXES = [
    "Apex", "Prime", "Velocity", "Horizon", "Pioneer",
    "Vertex", "Summit", "Elite", "Central", "North",
    "South", "East", "West", "Unity", "Nova",
    "Metro", "Global", "Rapid", "Blue", "Silver",
    "Golden", "Urban", "National", "Supreme", "Titan"
]

NAME_SUFFIXES = [
    "Logistics Park",
    "Distribution Hub",
    "Warehouse",
    "Supply Center",
    'Zone Center',
    "Storage Hub",
    "Inventory Center",
    "Logistics Center",
    "Distribution Park",
    "Operations Hub",
    "Supply Hub"
]
rows = []
used_warehouse_ids = set()

for i in range(1, NUM_WAREHOUSES + 1):
    while True:
        warehouse_id = f"WH{random.randint(100000,999999)}"

        if warehouse_id not in used_warehouse_ids:
            used_warehouse_ids.add(warehouse_id)
            break

    city, state, _ = random.choices(
        CITY_DATA,
        weights=[x[2] for x in CITY_DATA],
        k=1
    )[0]
    
    warehouse_name = (
        random.choice(NAME_PREFIXES)
        + " "
        + random.choice(NAME_SUFFIXES)
    )

    warehouse_type = random.choices(
        WAREHOUSE_TYPES,
        weights=[10, 45, 45]
    )[0]

    if warehouse_type == "National Distribution Center":
        capacity = random.randint(250000, 500000)
    elif warehouse_type == "Regional Distribution Center":
        capacity = random.randint(80000, 180000)
    else:
        capacity = random.randint(20000, 70000)

    active_status = random.choices(
        ["Active", "Inactive"],
        weights=[95, 5]
    )[0]
    
    operating_hours = random.choices(
        ["24x7", "Two Shifts", "Day Shift"],
        weights=[50, 30, 20]
    )[0]
    
    automation_level = random.choices(
        ["Manual", "Semi-Automated", "Automated"],
        weights=[25, 55, 20]
    )[0]

    rows.append({
        "WarehouseSysID": f"SYSWH{i:07d}",
        "WarehouseID": warehouse_id,
        "WarehouseName": warehouse_name,
        "WarehouseType": warehouse_type,
        "City": city,
        "State": state,
        "Manager": fake.name(),
        "Capacity": capacity,
        "OperatingHours": operating_hours,
        "AutomationLevel": automation_level,
        "ActiveStatus": active_status
    })

warehouses = pd.DataFrame(rows)

warehouses.to_csv(
    "data_generation/Warehouse Data.csv",
    index=False
)

print(warehouses.head())
print(f"\nGenerated {len(warehouses)} warehouse records")