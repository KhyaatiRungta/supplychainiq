# Copyright (c) 2026 Khyaati Rungta. Licensed under the MIT Licence - see LICENSE.

"""Create the cleaned, analysis-ready CSV from the raw DataCo file.

Output: data/processed/cleaned_supply_chain.csv
"""

import csv
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw", "DataCoSupplyChainDataset.csv")
OUT = os.path.join(ROOT, "data", "processed", "cleaned_supply_chain.csv")
ENCODING = "latin-1"

TRIM_FIELDS = [
    "Category Name", "Department Name", "Order Region", "Order State", "Order City",
    "Order Country", "Customer Segment", "Shipping Mode", "Market", "Delivery Status",
    "Order Status", "Type", "Customer City", "Customer Country",
]


def parse_dt(value):
    value = value.strip()
    for fmt in ("%m/%d/%Y %H:%M", "%m/%d/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def norm(text):
    text = text.strip()
    while "  " in text:
        text = text.replace("  ", " ")
    return text


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(RAW, newline="", encoding=ENCODING) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    out_fields = [
        "Order ID", "Order Item ID", "Order Date", "Shipping Date", "Order Status",
        "Delivery Status", "Late Delivery Risk", "Eligible For Delivery KPI",
        "Late Delivery (KPI)", "Shipping Mode", "Scheduled Shipping Days",
        "Actual Shipping Days", "Shipping Delay Days", "Market", "Order Region",
        "Order Country", "Order City", "Customer Segment", "Department Name",
        "Category Name", "Product Name", "Product Status", "Sales", "Order Profit",
        "Order Item Quantity", "Order Item Discount", "Transaction Type",
        "Customer ID", "Product ID",
    ]

    written = 0
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(out_fields)
        for r in rows:
            order_dt = parse_dt(r["order date (DateOrders)"])
            ship_dt = parse_dt(r["shipping date (DateOrders)"])
            actual = float(r["Days for shipping (real)"])
            sched = float(r["Days for shipment (scheduled)"])
            delivery_status = norm(r["Delivery Status"])
            eligible = delivery_status != "Shipping canceled"
            late = delivery_status == "Late delivery"
            writer.writerow([
                r["Order Id"],
                r["Order Item Id"],
                order_dt.strftime("%Y-%m-%d %H:%M:%S") if order_dt else "",
                ship_dt.strftime("%Y-%m-%d %H:%M:%S") if ship_dt else "",
                norm(r["Order Status"]),
                delivery_status,
                int(float(r["Late_delivery_risk"])),
                int(eligible),
                int(late),
                norm(r["Shipping Mode"]),
                sched,
                actual,
                actual - sched,
                norm(r["Market"]),
                norm(r["Order Region"]),
                norm(r["Order Country"]),
                norm(r["Order City"]),
                norm(r["Customer Segment"]),
                norm(r["Department Name"]),
                norm(r["Category Name"]),
                r["Product Name"].strip(),
                int(float(r["Product Status"])),
                r["Sales"],
                r["Order Profit Per Order"],
                r["Order Item Quantity"],
                r["Order Item Discount"],
                norm(r["Type"]),
                r["Customer Id"],
                r["Product Card Id"],
            ])
            written += 1

    print(f"Wrote {written} rows to {OUT}")


if __name__ == "__main__":
    main()
