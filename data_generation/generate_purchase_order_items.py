import random
import pandas as pd

from config import RANDOM_SEED
random.seed(RANDOM_SEED)

purchase_orders = pd.read_csv(
    "data_generation/Purchase Order Header Data.csv"
)

supplier_products = pd.read_csv(
    "data_generation/Supplier Products Data.csv"
)

products = pd.read_csv(
    "data_generation/Products Data.csv"
)

rows = []
sys_id = 1
used_item_ids = set()

for _, po in purchase_orders.iterrows():
    purchase_order_id = po["PurchaseOrderID"]
    supplier_id = po["SupplierID"]

    supplier_catalog = supplier_products[
        supplier_products["SupplierID"] == supplier_id
    ]

    if len(supplier_catalog) == 0:
        continue
    
    num_items = random.randint(
        3,
        min(8, len(supplier_catalog))
    )

    selected_products = supplier_catalog.sample(
        n=num_items,
        replace=False,
        random_state=random.randint(1, 100000)
    )

    for _, item in selected_products.iterrows():
        product = products[
            products["ProductID"] == item["ProductID"]
        ].iloc[0]

        subcategory = product["SubCategory"]

        if subcategory in [
            "Mobile Phones",
            "Laptops"
        ]:
            quantity = random.randint(10, 40)

        elif subcategory in [
            "Rice",
            "Flour",
            "Sugar"
        ]:
            quantity = random.randint(300, 1500)

        else:
            quantity = random.randint(80, 500)

        if po["OrderStatus"] == "Delivered":
            scenario = random.choices(
                ["Full", "Minor", "Major"],
                weights=[75, 20, 5]
            )[0]

            if scenario == "Full":
                received_qty = quantity
            elif scenario == "Minor":
                received_qty = quantity - random.randint(
                    1,
                    max(1, int(quantity * 0.05))
                )
            else:
                received_qty = quantity - random.randint(
                    max(1, int(quantity * 0.06)),
                    max(2, int(quantity * 0.15))
                )
        else:
            received_qty = 0

        defect_rate = item["DefectRatePercentage"]

        expected_rejected = (
            received_qty * defect_rate / 100
        )

        rejected_qty = max(0, round(random.uniform(
                expected_rejected * 0.7,
                expected_rejected * 1.3
                )
            )
        )

        rejected_qty = min(
            rejected_qty,
            received_qty
        )

        accepted_qty = (
            received_qty - rejected_qty
        )

        if received_qty == 0:
            inspection_status = "Not Inspected"
        else:
            acceptance_rate = (
                accepted_qty / received_qty
            )

            if acceptance_rate == 1:
                inspection_status = "Passed"
            elif acceptance_rate >= 0.95:
                inspection_status = (
                    "Passed with Observations"
                )
            else:
                inspection_status = "Failed"
                
        quoted_cost = item["QuotedUnitCost"]

        total_item_cost = round(
            quantity * quoted_cost,
            2
        )
        
        line_amount_before_tax = round(
            quantity * quoted_cost,
            2
        )

        if subcategory in [
            "Mobile Phones",
            "Laptops"
        ]:
            tax_rate = 18
        elif subcategory in [
            "Rice",
            "Flour"
        ]:
            tax_rate = 5
        else:
            tax_rate = 12

        tax_amount = round(
            line_amount_before_tax * tax_rate / 100, 2
        )

        line_amount_after_tax = round(
            line_amount_before_tax + tax_amount, 2
        )

        while True:
            item_id = (
                f"POI{random.randint(100000,999999)}"
            )

            if item_id not in used_item_ids:
                used_item_ids.add(item_id)
                break
            
        rows.append({
            "PurchaseOrderItemSysID":
                f"SYSPOI{sys_id:07d}",
            "PurchaseOrderItemID":
                item_id,
            "PurchaseOrderID":
                purchase_order_id,
            "ProductID":
                item["ProductID"],
            "QuantityOrdered":
                quantity,
            "ReceivedQuantity":
                received_qty,
            "AcceptedQuantity":
                accepted_qty,
            "QuotedUnitCost":
                quoted_cost,
            "TotalItemCost":
                total_item_cost,
            "InspectionStatus":
                inspection_status,
            "LineAmountBeforeTax": 
                line_amount_before_tax,
            "TaxRate":
                tax_rate,
            "TaxAmount":
                tax_amount,
            "LineAmountAfterTax":
                line_amount_after_tax,
        })
        sys_id += 1

purchase_order_items = pd.DataFrame(rows)

purchase_order_items.to_csv(
    "data_generation/Purchase Order Items Data.csv",
    index=False
)

print(purchase_order_items.head())
print(f"\nGenerated {len(purchase_order_items)} purchase order items.")