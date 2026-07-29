import random
import pandas as pd
from faker import Faker
from datetime import date, timedelta

from config import RANDOM_SEED

random.seed(RANDOM_SEED)
fake = Faker("en_IN")
Faker.seed(RANDOM_SEED)

inventory = pd.read_csv("data_generation/Inventory Data.csv")
products = pd.read_csv("data_generation/Products Data.csv")
stores = pd.read_csv("data_generation/Store Data.csv")

MAX_SALES_PER_STORE = 120

used_sales_ids = set()
rows = []
sys_id = 1

def weighted_sale_date():
    year = date.today().year
    windows = [
        (date(year,1,1), date(year,8,31), 55),
        (date(year,9,1), date(year,9,30), 10),
        (date(year,10,1), date(year,10,31), 20),
        (date(year,11,1), date(year,11,30), 10),
        (date(year,12,1), date(year,12,31), 5),
    ]
    starts, ends, weights = zip(*windows)
    idx = random.choices(range(len(windows)), weights=weights, k=1)[0]
    start, end = starts[idx], ends[idx]
    return start + timedelta(days=random.randint(0,(end-start).days))

def choose_quantity(stock, category):
    if category in ["Mobile Phones", "Laptops"]:
        low, high = 1, 3
    elif category in ["Rice", "Flour", "Sugar"]:
        low, high = 2, 20
    else:
        low, high = 2, 35

    high = min(high, stock)

    if stock < low:
        return stock

    return random.randint(low, high)

def unique_sale_id():
    while True:
        sid=f"SALE{random.randint(100000,999999)}"
        if sid not in used_sales_ids:
            used_sales_ids.add(sid)
            return sid

inventory = inventory.copy()

for _, store in stores.iterrows():
    sales_count = random.randint(int(MAX_SALES_PER_STORE*0.7), MAX_SALES_PER_STORE)
    for _ in range(sales_count):
        available = inventory[inventory["CurrentStock"]>0]
        if available.empty:
            break
        inv = available.sample(1).iloc[0]
        idx = inv.name
        prod = products.loc[products["ProductID"]==inv["ProductID"]].iloc[0]
        sub = prod["SubCategory"]
        stock = max(0, int(inv["CurrentStock"]))

        qty = choose_quantity(stock, sub)

        inventory.at[idx,"CurrentStock"] -= qty

        sale_type = random.choices(
            ["Regular","Promotion","Clearance"],
            weights=[70,20,10],k=1
        )[0]

        if sale_type=="Regular":
            disc=random.choice([0,5])
        elif sale_type=="Promotion":
            disc=random.choice([10,15,20])
        else:
            disc=random.choice([25,30,40])

        returned = random.randint(1,max(1,qty//2)) if random.random()<0.05 else 0

        price = round(prod["SellingPrice"]*random.uniform(0.98,1.03),2)

        rows.append({
            "SalesSysID":f"SYSSALE{sys_id:07d}",
            "SalesID":unique_sale_id(),
            "SalesDate":weighted_sale_date(),
            "StoreID":store["StoreID"],
            "ProductID":prod["ProductID"],
            "QuantitySold":qty,
            "UnitSellingPrice":price,
            "DiscountPercentage":disc,
            "ReturnedQuantity":returned,
            "SaleType":sale_type
        })
        sys_id += 1

sales = pd.DataFrame(rows)
sales.to_csv("data_generation/Sales Data.csv", index=False)
print(sales.head())
print(f"Generated {len(sales)} sales records.")
