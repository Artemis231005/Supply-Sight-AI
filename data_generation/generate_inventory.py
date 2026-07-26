import random
import pandas as pd
from faker import Faker

from config import NUM_UNIQUE_SUPPLIERS, RANDOM_SEED

random.seed(RANDOM_SEED)
fake = Faker("en_IN")
Faker.seed(RANDOM_SEED)

CATEGORIES = [
    "Electronics",
    "Groceries",
    "Beverages"
]

STATES = {
    "Delhi": ["New Delhi"],
    
    "Uttar Pradesh": [
        "Noida",
        "Ghaziabad",
        "Lucknow",
        "Kanpur"
    ],

    "Maharashtra": [
        "Mumbai",
        "Pune",
        "Nagpur"
    ],

    "Karnataka": [
        "Bengaluru",
        "Mangalore"
    ],

    "Tamil Nadu": [
        "Chennai",
        "Coimbatore"
    ],

    "Gujarat": [
        "Ahmedabad",
        "Surat"
    ]
}

rows = []
used_supplier_ids = set()
sys_id = 1

NAME_SUFFIXES = [
    "Traders",
    "Distributors",
    "Enterprises",
    "Wholesale",
    "Supplies",
    "Industries"
]

for i in range(NUM_UNIQUE_SUPPLIERS):

    while True:
        supplier_id = f"SUP{random.randint(100000,999999)}"

        if supplier_id not in used_supplier_ids:
            used_supplier_ids.add(supplier_id)
            break

    supplier_name = (
        fake.last_name() +
        " " +
        fake.last_name() +
        " " +
        random.choice(NAME_SUFFIXES)
    )

    state = random.choice(list(STATES.keys()))
    city = random.choice(STATES[state])

    phone = fake.phone_number()
    email = fake.company_email()

    supplier_size = random.choices(
        ["Small", "Medium", "Large"],
        weights=[50, 35, 15]
    )[0]

    if supplier_size == "Large":

        supplier_tier = random.choices(
            ["Tier 1", "Tier 2", "Tier 3"],
            weights=[75, 20, 5]
        )[0]

    elif supplier_size == "Medium":

        supplier_tier = random.choices(
            ["Tier 1", "Tier 2", "Tier 3"],
            weights=[20, 60, 20]
        )[0]

    else:   

        supplier_tier = random.choices(
            ["Tier 1", "Tier 2", "Tier 3"],
            weights=[5, 30, 65]
        )[0]

    if supplier_tier == "Tier 1":

        rating = round(
            random.uniform(4.2, 5.0),
            1
        )

    elif supplier_tier == "Tier 2":

        rating = round(
            random.uniform(3.4, 4.7),
            1
        )

    else:   

        rating = round(
            random.uniform(2.3, 4.2),
            1
        )

    active_status = random.choices(
        ["Active", "Inactive"],
        weights=[93, 7]
    )[0]

    supplier_categories = random.sample(
        CATEGORIES,
        random.randint(1, 3)
    )

    for category in supplier_categories:

        rows.append({

            "SupplierSysID": f"SYSSUP{sys_id:07d}",

            "SupplierID": supplier_id,

            "SupplierName": supplier_name,

            "Category": category,

            "Phone": phone,

            "Email": email,

            "City": city,

            "State": state,

            "SupplierSize": supplier_size,

            "SupplierTier": supplier_tier,

            "Rating": rating,

            "ActiveStatus": active_status

        })

        sys_id += 1

suppliers = pd.DataFrame(rows)

suppliers.to_csv(
    "data_generation/Supplier Data.csv",
    index=False
)

print(suppliers.head())
print(f"\nGenerated {len(suppliers)} supplier records")