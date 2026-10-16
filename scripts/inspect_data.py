# Copyright (c) 2026 Khyaati Rungta. Licensed under the MIT Licence - see LICENSE.

"""Profile the raw DataCo supply chain dataset and write a basic report to stdout."""

import csv
import os
from collections import Counter, defaultdict
from datetime import datetime

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
RAW_FILE = os.path.join(RAW_DIR, "DataCoSupplyChainDataset.csv")
ENCODING = "latin-1"


def parse_dt(value):
    value = value.strip()
    for fmt in ("%m/%d/%Y %H:%M", "%m/%d/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def main():
    if not os.path.exists(RAW_FILE):
        print("Raw dataset not found at:", RAW_FILE)
        print("Place DataCoSupplyChainDataset.csv in data/raw/ and rerun.")
        return

    with open(RAW_FILE, newline="", encoding=ENCODING) as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        rows = list(reader)

    print("File:", os.path.basename(RAW_FILE))
    print("Encoding read as:", ENCODING)
    print("Row count (data):", len(rows))
    print("Column count:", len(header))
    print("\nColumns:")
    for i, name in enumerate(header, 1):
        print(f"{i:2d}. {name!r}")

    print("\nDistinct delivery statuses:", dict(Counter(r["Delivery Status"] for r in rows)))
    print("Distinct shipping modes:", dict(Counter(r["Shipping Mode"] for r in rows)))
    print("Distinct markets:", dict(Counter(r["Market"] for r in rows)))
    print("Distinct customer segments:", dict(Counter(r["Customer Segment"] for r in rows)))
    print("Distinct late-delivery risk:", dict(Counter(r["Late_delivery_risk"] for r in rows)))

    parsed = [parse_dt(r["order date (DateOrders)"]) for r in rows]
    ok = [d for d in parsed if d is not None]
    print("\nOrder date range:", min(ok), "to", max(ok), "| parsed rows:", len(ok), "of", len(rows))

    order_ids = {r["Order Id"] for r in rows}
    item_ids = {r["Order Item Id"] for r in rows}
    print("Distinct order IDs:", len(order_ids))
    print("Distinct order-item IDs:", len(item_ids))

    blanks = {name: sum(1 for r in rows if r.get(name, "").strip() == "") for name in header}
    print("\nColumns with blank values:")
    for name in header:
        if blanks[name]:
            print(f"  {name!r}: {blanks[name]}")


if __name__ == "__main__":
    main()
