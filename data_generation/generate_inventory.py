import random
import pandas as pd
from faker import Faker

from config import RANDOM_SEED

random.seed(RANDOM_SEED)
fake = Faker("en_IN")
Faker.seed(RANDOM_SEED)

purchase_orders = pd.read_csv(
    "data_generation/Purchase Order Header Data.csv"
)

purchase_order_items = pd.read_csv(
    "data_generation/Purchase Order Items Data.csv"
)

products = pd.read_csv(
    "data_generation/Products Data.csv"
)

rows = []
used_inventory_ids = set()
sys_id = 1

merged = purchase_order_items.merge(
    purchase_orders[[
        "PurchaseOrderID",
        "WarehouseID",
        "ExpectedDeliveryDate",
        "OrderStatus"
    ]],
    on="PurchaseOrderID",
    how="inner"

)

merged = merged[
    merged["OrderStatus"] == "Delivered"
]

inventory = merged.groupby(["WarehouseID", "ProductID"], as_index=False).agg({
    "AcceptedQuantity":"sum",
    "ExpectedDeliveryDate":"max"
})

for _, row in inventory.iterrows():
    while True:
        inventory_id = (
            f"INV{random.randint(100000,999999)}"
        )
        if inventory_id not in used_inventory_ids:
            used_inventory_ids.add(inventory_id)
            break

    product = products[
        products["ProductID"] == row["ProductID"]
    ].iloc[0]

    subcategory = product["SubCategory"]

    accepted = int(row["AcceptedQuantity"])

    if subcategory in [
        "Mobile Phones",
        "Laptops"
    ]:
        issued = random.randint(
            int(accepted*0.15),
            int(accepted*0.75)
        )
        reorder_level = random.randint(15, 40)
        
    elif subcategory in [
        "Rice",
        "Flour",
        "Sugar"
    ]:
        issued = random.randint(
            int(accepted*0.30),
            int(accepted*0.90)
        )
        reorder_level = random.randint(300, 900)

    else:
        issued = random.randint(
            int(accepted*0.25),
            int(accepted*0.85)
        )
        reorder_level = random.randint(80, 250)

    target_condition = random.choices(
        ["Low Stock", "Normal", "Slow Moving", "Overstocked"],
        weights=[25, 35, 25, 15]
    )[0]

    if target_condition == "Low Stock":
        current_stock = random.randint(
            max(0, int(reorder_level * 0.3)),
            reorder_level
        )

    elif target_condition == "Normal":
        current_stock = random.randint(
            reorder_level + 1,
            int(reorder_level * 3)
        )

    elif target_condition == "Slow Moving":
        current_stock = random.randint(
            int(reorder_level * 2),
            int(reorder_level * 5)
        )

    else:  
        current_stock = random.randint(
            int(reorder_level * 5) + 1,
            int(reorder_level * 8)
        )

    current_stock = min(current_stock, accepted)

    reserved_stock = random.randint(0,
        min(
            current_stock,
            max(1, int(current_stock*0.30))
        )
    )
    
    condition = target_condition

    last_restock = pd.to_datetime(
        row["ExpectedDeliveryDate"]
    ).date()

    last_issued = fake.date_between(
        start_date=last_restock,
        end_date="today"
    )

    rows.append({
        "InventorySysID":
            f"SYSINV{sys_id:07d}",
        "InventoryID":
            inventory_id,
        "WarehouseID":
            row["WarehouseID"],
        "ProductID":
            row["ProductID"],
        "CurrentStock":
            current_stock,
        "ReservedStock":
            reserved_stock,
        "ReorderLevel":
            reorder_level,
        "LastRestockedDate":
            last_restock,
        "LastIssuedDate":
            last_issued,
        "InventoryCondition":
            condition
    })
    sys_id += 1

inventory_df = pd.DataFrame(rows)

inventory_df.to_csv(
    "data_generation/Inventory Data.csv",
    index=False
)

print(inventory_df.head())
print(f"\nGenerated {len(inventory_df)} inventory records.")