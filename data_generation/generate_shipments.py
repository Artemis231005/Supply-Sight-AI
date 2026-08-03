import random
import pandas as pd
from datetime import timedelta

from config import RANDOM_SEED

random.seed(RANDOM_SEED)

po = pd.read_csv("data_generation/Purchase Order Header Data.csv")
suppliers = pd.read_csv("data_generation/Supplier Data.csv")
warehouses = pd.read_csv("data_generation/Warehouse Data.csv")
weather = pd.read_csv("data_generation/Weather Data.csv")

weather["Date"] = pd.to_datetime(weather["Date"])
po["OrderDate"] = pd.to_datetime(po["OrderDate"])
po["ExpectedDeliveryDate"] = pd.to_datetime(po["ExpectedDeliveryDate"])

suppliers = suppliers.drop_duplicates(subset="SupplierID")
supplier_lookup = suppliers.set_index("SupplierID").to_dict("index")
warehouse_lookup = warehouses.set_index("WarehouseID").to_dict("index")

CITY_DISTANCE = {
    ("New Delhi","Noida"):25,
    ("New Delhi","Ghaziabad"):20,
    ("New Delhi","Lucknow"):555,
    ("New Delhi","Kanpur"):440,
    ("New Delhi","Mumbai"):1410,
    ("New Delhi","Ahmedabad"):930,
    ("New Delhi","Pune"):1460,
    ("New Delhi","Bengaluru"):2150,
    ("New Delhi","Chennai"):2180,
    ("New Delhi","Nagpur"):1080,
    ("New Delhi","Mangalore"):2250,
    ("New Delhi","Coimbatore"):2420,

    ("Mumbai","Pune"):150,
    ("Mumbai","Ahmedabad"):530,
    ("Mumbai","Nagpur"):840,
    ("Mumbai","Bengaluru"):980,
    ("Mumbai","Chennai"):1330,
    ("Mumbai","Mangalore"):715,
    ("Mumbai","Coimbatore"):1190,

    ("Bengaluru","Chennai"):345,
    ("Bengaluru","Mangalore"):350,
    ("Bengaluru","Coimbatore"):365,

    ("Chennai","Coimbatore"):500,
    ("Lucknow","Kanpur"):95,
    ("Ahmedabad","Pune"):660,
    ("Pune","Nagpur"):720
}

def get_distance(city1, city2):
    if city1 == city2:
        return random.randint(15,40)

    if (city1,city2) in CITY_DISTANCE:
        return CITY_DISTANCE[(city1,city2)]

    if (city2,city1) in CITY_DISTANCE:
        return CITY_DISTANCE[(city2,city1)]

    return random.randint(300,1800)

CARRIERS = [
    "Blue Dart",
    "Delhivery",
    "DHL",
    "FedEx",
    "Ecom Express",
    "Shadowfax"
]

def transport_mode(distance):
    if distance < 450:
        return "Road"

    if random.random() < 0.10:
        return "Rail"

    return "Road"

def freight_cost(distance, mode):
    if mode == "Road":
        rate = random.uniform(22,27)
    else:
        rate = random.uniform(15,19)
        
    return round(distance * rate,2)

def transit_days(distance, mode):
    if mode == "Road":
        if distance < 150:
            return random.randint(1,2)
        elif distance < 600:
            return random.randint(2,4)
        elif distance < 1200:
            return random.randint(4,6)
        else:
            return random.randint(6,9)

    else:
        if distance < 600:
            return random.randint(2,4)
        elif distance < 1200:
            return random.randint(4,6)
        else:
            return random.randint(5,8)

def weather_severity(city, date):
    row = weather[
        (weather["City"] == city) &
        (weather["Date"] == date)
    ]

    if len(row) == 0:
        return "Normal"
    
    return row.iloc[0]["WeatherSeverity"]

def delay_days(severity):
    if severity == "Normal":
        return random.choices(
            [0,1],
            weights=[95,5]
        )[0]

    elif severity == "Moderate":
        return random.choices(
            [0,1,2],
            weights=[70,20,10]
        )[0]

    elif severity == "High":
        return random.choices(
            [1,2,3],
            weights=[40,40,20]
        )[0]

    else:
        return random.randint(2,5)


def tracking():
    return "TRK" + str(random.randint(100000000,999999999))


rows = []
sys_id = 1
today = pd.Timestamp.today().normalize()

for _, order in po.iterrows():
    supplier = supplier_lookup[order["SupplierID"]]
    warehouse = warehouse_lookup[order["WarehouseID"]]

    supplier_city = supplier["City"]
    warehouse_city = warehouse["City"]

    distance = get_distance(
        supplier_city,
        warehouse_city
    )

    mode = transport_mode(distance)

    shipment_date = order["OrderDate"] + timedelta(
        days=random.randint(0, 2)
    )

    transit = transit_days(distance, mode)

    severity = weather_severity(
        warehouse_city,
        shipment_date.normalize()
    )

    delay = delay_days(severity)
    expected_delivery = order["ExpectedDeliveryDate"]
    actual_delivery = expected_delivery + timedelta(days=delay)

    if shipment_date > today:
        status = "Scheduled"
    elif actual_delivery > today:
        status = "In Transit"
    elif delay > 0:
        status = "Delayed"
    else:
        status = "Delivered"

    rows.append({
        "ShipmentSysID":
            f"SYSSHP{sys_id:07d}",
        "ShipmentID":
            f"SHP{sys_id:07d}",
        "PurchaseOrderID":
            order["PurchaseOrderID"],
        "SupplierID":
            order["SupplierID"],
        "WarehouseID":
            order["WarehouseID"],
        "ShipmentDate":
            shipment_date.date(),
        "ExpectedDeliveryDate":
            expected_delivery.date(),
        "ActualDeliveryDate":
            actual_delivery.date(),
        "Carrier":
            random.choice(CARRIERS),
        "TransportMode":
            mode,
        "TrackingNumber":
            tracking(),
        "DistanceKM":
            distance,
        "TransitDays":
            transit,
        "DelayDays":
            delay,
        "ShipmentStatus":
            status,
        "FreightCost":
            freight_cost(distance, mode)
    })

    sys_id += 1

shipments = pd.DataFrame(rows)

shipments.to_csv(
    "data_generation/Shipment Data.csv",
    index=False
)

print(shipments.head())
print(f"\nGenerated {len(shipments):,} shipment records.")