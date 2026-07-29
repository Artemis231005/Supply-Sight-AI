import random
import pandas as pd
from faker import Faker
from datetime import timedelta, date

from config import NUM_PURCHASE_ORDERS, RANDOM_SEED

random.seed(RANDOM_SEED)
fake = Faker("en_IN")
Faker.seed(RANDOM_SEED)

suppliers = pd.read_csv("data_generation/Supplier Data.csv")
supplier_products = pd.read_csv("data_generation/Supplier Products Data.csv")
warehouses = pd.read_csv("data_generation/Warehouse Data.csv")

used_po_ids = set()
rows = []

today = date.today()

for i in range(1, NUM_PURCHASE_ORDERS + 1):
    while True:
        po_id = f"PO{random.randint(100000,999999)}"

        if po_id not in used_po_ids:
            used_po_ids.add(po_id)
            break

    supplier = suppliers.sample(1).iloc[0]

    supplier_id = supplier["SupplierID"]
    category = supplier["Category"]

    if category == "Electronics":
        eligible = warehouses[
            warehouses["WarehouseType"].isin([
                "National Distribution Center",
                "Regional Distribution Center"
            ])
        ]

    elif category == "Groceries":
        eligible = warehouses[
            warehouses["WarehouseType"].isin([
                "Regional Distribution Center",
                "Fulfillment Center"
            ])
        ]

    else:
        eligible = warehouses[
            warehouses["WarehouseType"] == "Fulfillment Center"
        ]

    warehouse = eligible.sample(1).iloc[0]

    warehouse_id = warehouse["WarehouseID"]

    lead_time = round(

        supplier_products[
            supplier_products["SupplierID"] == supplier_id
        ]["LeadTimeDays"].mean()

    )

    order_date = fake.date_between(
        start_date="-1y",
        end_date="today"
    )

    expected_delivery = (
        order_date +
        timedelta(days=int(lead_time))
    )

    if expected_delivery < today:
        order_status = random.choices(
            ["Delivered", "Delayed"],
            weights=[90, 10]
        )[0]
    elif order_date <= today:
        order_status = random.choices(
            ["In Transit", "Processing"],
            weights=[75, 25]
        )[0]
    else:
        order_status = "Scheduled"

    if random.random() < 0.04:
        order_status = "Cancelled"

    if order_status == "Delivered":
        payment_status = random.choices(
            ["Paid", "Pending"],
            weights=[95, 5]
        )[0]
    elif order_status == "Cancelled":
        payment_status = "Cancelled"
    else:
        payment_status = "Pending"
        
    rows.append({
        "PurchaseOrderSysID":
            f"SYSPO{i:07d}",
        "PurchaseOrderID":
            po_id,
        "SupplierID":
            supplier_id,
        "WarehouseID":
            warehouse_id,
        "OrderDate":
            order_date,
        "ExpectedDeliveryDate":
            expected_delivery,
        "OrderStatus":
            order_status,
        "PaymentStatus":
            payment_status
    })

purchase_orders = pd.DataFrame(rows)

purchase_orders.to_csv(
    "data_generation/Purchase Order Header Data.csv",
    index=False
)

print(purchase_orders.head())
print(
    f"\nGenerated {len(purchase_orders)} purchase orders."
)