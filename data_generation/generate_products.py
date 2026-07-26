import random
import pandas as pd
from faker import Faker
from config import NUM_PRODUCTS, RANDOM_SEED

random.seed(RANDOM_SEED)
fake = Faker("en_IN")
Faker.seed(RANDOM_SEED)

PRODUCTS = {
    "Electronics": {
        "Mobile Phones": {
            "Samsung": ["Galaxy S24", "Galaxy A55", "Galaxy S25", "Galaxy Z Flip 8"],
            "Apple": ["iPhone 15", "iPhone 15 Pro", "iPhone 16", "iPhone 16 Pro"],
            "OnePlus": ["OnePlus 12", "OnePlus Nord CE4", "OnePlus 15", "OnePlus Nord CE6"],
            "Redmi": ["Redmi Note 15", "Redmi Turbo 5"],
            "Motorola": ["Motorola Razr 60", "Motorola Edge 70", "Motorola G57"]
        },

        "Laptops": {
            "Dell": ["Inspiron", "XPS"],
            "HP": ["Pavilion", "Victus", "Envy", "Spectre"],
            "Lenovo": ["ThinkPad", "IdeaPad", "Legion"],
            "Apple": ["MacBook Air", "MacBook Pro"],
            "Asus": ["Vivobook", "Scar", "Zephyrus"]
        },
    },
        
    "Groceries": {
        "Rice": ["Basmati Rice", "Brown Rice", "Sona Masoori"],
        "Flour": ["Wheat Flour", "Multigrain Flour", "Gluten-Free Flour"],
        "Sugar": ["White Sugar", "Brown Sugar", "Organic Sugar"]
    },

    "Beverages": {
        "Tea": ["Masala Tea", "Green Tea", "Floral Tea","White Tea"],
        "Coffee": ["Instant Coffee", "Filter Coffee", "Vanilla Coffee", "Roasted Coffee"],
        "Juices": ["Orange Juice", "Apple Juice", "Mixed Fruit Juice", "Guava Juice"]
    }
}

ATTRIBUTES = {
    "Mobile Phones": {
        "Storage": ["128GB", "256GB", "512GB"],
        "RAM": ["4GB", "8GB", "12GB"],
        "Color": ["Black", "Blue", "Silver", "White", "Red"]
    },

    "Laptops": {
        "Storage": ["256GB", "512GB", "2TB"],
        "RAM": ["8GB", "16GB", "32GB"],
        "Color": ["Black", "Silver", "Blue", "White"]
    },

    "Rice": {
        "Weight": ["1kg", "5kg", "10kg"],
        "Package": ["Bag", "Premium Pack"]
    },

    "Flour": {
        "Weight": ["1kg", "5kg", "10kg"],
        "Package": ["Bag", "Premium Pack"]
    },

    "Sugar": {
        "Weight": ["1kg", "5kg"],
        "Package": ["Bag", "Premium Pack"]
    },

    "Tea": {
        "Weight": ["100g", "250g", "500g"],
        "Package": ["Box", "Pouch"]
    },

    "Coffee": {
        "Weight": ["100g", "200g", "500g"],
        "Package": ["Jar", "Pouch"]
    },

    "Juices": {
        "Weight": ["250ml", "500ml", "1L"],
        "Package": ["Bottle", "Carton"]
    }
}

PRICE_RANGE = {
    "Mobile Phones": (10000, 90000),
    "Laptops": (50000, 150000),

    "Rice": (80, 1200),
    "Flour": (40, 800),
    "Sugar": (30, 500),

    "Tea": (80, 1000),
    "Coffee": (200, 2500),
    "Juices": (40, 300)
}

FOOD_BRANDS = {
    "Rice": ["India Gate", "Fortune", "Daawat"],
    "Flour": ["Aashirvaad", "Fortune", "Patanjali"],
    "Sugar": ["Madhur", "Trust", "Organic India"],
    "Tea": ["Tata Tea", "Lipton", "Brooke Bond"],
    "Coffee": ["Nescafe", "Bru", "Continental"],
    "Juices": ["Real", "Tropicana", "B Natural"]
}


rows = []
used_product_ids = set()

for i in range(1, NUM_PRODUCTS + 1):
    category = random.choice(list(PRODUCTS.keys()))

    subcategory = random.choice(
        list(PRODUCTS[category].keys())
    )

    if category == "Electronics":

        brand = random.choice(
            list(PRODUCTS[category][subcategory].keys())
        )

        base_product = random.choice(
            PRODUCTS[category][subcategory][brand]
        )

        attrs = ATTRIBUTES[subcategory]

        storage = random.choice(attrs["Storage"])
        ram = random.choice(attrs["RAM"])
        color = random.choice(attrs["Color"])

        product_name = (
            f"{brand} "
            f"{base_product} "
            f"{storage} "
            f"{ram} "
            f"{color}"
        )

        shelf_life = None

    else:
        brand = random.choice(
            FOOD_BRANDS[subcategory]
        )

        base_product = random.choice(
            PRODUCTS[category][subcategory]
        )

        attrs = ATTRIBUTES[subcategory]

        weight = random.choice(attrs["Weight"])
        package = random.choice(attrs["Package"])

        product_name = (
            f"{brand} "
            f"{base_product} "
            f"{weight} "
            f"{package}"
        )

        if category == "Groceries":
            shelf_life = random.randint(180, 720)
        else:
            shelf_life = random.randint(90, 365)

    cost_low, cost_high = PRICE_RANGE[subcategory]
    
    unit_cost = round(random.uniform(cost_low, cost_high), 2)
    markup = random.uniform(1.15, 1.45)
    selling_price = round(unit_cost * markup, 2)

    while True:
        product_id = f"PROD{random.randint(100000, 999999)}"

        if product_id not in used_product_ids:
            used_product_ids.add(product_id)
            break

    rows.append({
        "ProductSysID": f"SYSP{i:07d}",
        "ProductID": product_id,        
        "ProductName": product_name,
        "Brand": brand,
        "Category": category,
        "SubCategory": subcategory,
        "UnitCost": unit_cost,
        "SellingPrice": selling_price,
        "ShelfLifeDays": shelf_life
    })

products = pd.DataFrame(rows)

products.to_csv(
    "data_generation/Products Data.csv",
    index=False
)

print(products.head())
print(f"\nGenerated {len(products)} products")