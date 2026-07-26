import random
import pandas as pd
from config import RANDOM_SEED

random.seed(RANDOM_SEED)

products = pd.read_csv("data_generation/Products Data.csv")
suppliers = pd.read_csv("data_generation/Supplier Data.csv")

rows = []
sys_id = 1

for _, supplier in suppliers.iterrows():

    supplier_id = supplier["SupplierID"]
    supplier_size = supplier["SupplierSize"]
    supplier_tier = supplier["SupplierTier"]
    category = supplier["Category"]

    category_products = products[
        products["Category"] == category
    ]
    
    available_subcategories = category_products[
        "SubCategory"
    ].unique()

    primary_subcategory = random.choice(
        available_subcategories
    )

    primary_products = category_products[
        category_products["SubCategory"] == primary_subcategory
    ]

    secondary_products = category_products[
        category_products["SubCategory"] != primary_subcategory
    ]

    total_products = len(category_products)

    if supplier_size == "Large":
        percent = random.uniform(0.12, 0.18)
    elif supplier_size == "Medium":
        percent = random.uniform(0.07, 0.12)
    else:
        percent = random.uniform(0.03, 0.07)

    num_products = max(
        5,
        int(total_products * percent)
    )

    primary_count = min(
        int(num_products * 0.8),
        len(primary_products)
    )

    secondary_count = min(
        num_products - primary_count,
        len(secondary_products)
    )

    sampled_products = pd.concat([

        primary_products.sample(
            n=primary_count,
            random_state=random.randint(1, 100000)
        ),

        secondary_products.sample(
            n=secondary_count,
            random_state=random.randint(1, 100000)
        )

    ])

    for _, product in sampled_products.iterrows():
        subcategory = product["SubCategory"]
        
        if subcategory in ["Mobile Phones", "Laptops"]:
            lead_time = random.randint(15, 40)
        elif subcategory in ["Rice", "Flour", "Sugar"]:
            lead_time = random.randint(2, 10)
        else:
            lead_time = random.randint(3, 12)


        if supplier_tier == "Tier 1":
            lead_time = max(
                1,
                lead_time - random.randint(0, 3)
            )
        elif supplier_tier == "Tier 3":
            lead_time += random.randint(2, 7)


        if subcategory in ["Mobile Phones", "Laptops"]:
            if supplier_size == "Large":
                moq = random.randint(80, 150)
            elif supplier_size == "Medium":
                moq = random.randint(40, 100)
            else:
                moq = random.randint(20, 60)
                
        elif subcategory in ["Rice", "Flour", "Sugar"]:
            if supplier_size == "Large":
                moq = random.randint(500, 1200)
            elif supplier_size == "Medium":
                moq = random.randint(250, 700)
            else:
                moq = random.randint(100, 400)
                
        else:
            if supplier_size == "Large":
                moq = random.randint(250, 700)
            elif supplier_size == "Medium":
                moq = random.randint(100, 400)
            else:
                moq = random.randint(50, 200)

        if supplier_tier == "Tier 1":
            multiplier = random.uniform(0.99, 1.05)
        elif supplier_tier == "Tier 2":
            multiplier = random.uniform(0.96, 1.02)
        else:
            multiplier = random.uniform(0.90, 0.98)

        quoted_cost = round(
            product["UnitCost"] * multiplier,
            2
        )
        
        if supplier_tier == "Tier 1":
            defect_rate = round(
                random.uniform(0.2, 1.2),
                2
            )
        elif supplier_tier == "Tier 2":
            defect_rate = round(
                random.uniform(0.8, 3.0),
                2
            )
        else:
            defect_rate = round(
                random.uniform(2.5, 7.5),
                2
            )

        rows.append({
        "SupplierProductSysID":
            f"SYSSP{sys_id:07d}",
        "SupplierID":
            supplier_id,
        "ProductID":
            product["ProductID"],
        "LeadTimeDays":
            lead_time,
        "MinimumOrderQty":
            moq,
        "QuotedUnitCost":
            quoted_cost,
        "DefectRatePercentage":
            defect_rate
    })

        sys_id += 1

supplier_products = pd.DataFrame(rows)

supplier_products.to_csv(
    "data_generation/Supplier Products Data.csv",
    index=False
)

print(supplier_products.head())
print(
    f"\nGenerated {len(supplier_products)} supplier product records"
)