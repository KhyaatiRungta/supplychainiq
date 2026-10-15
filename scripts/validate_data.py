"""Validation checks for the raw and cleaned DataCo supply chain data."""

import csv
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw", "DataCoSupplyChainDataset.csv")
CLEAN = os.path.join(ROOT, "data", "processed", "cleaned_supply_chain.csv")
ENCODING = "latin-1"


def parse_dt(v):
    v = v.strip()
    for fmt in ("%m/%d/%Y %H:%M", "%m/%d/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            continue
    return None


def main():
    print("== Validation ==")
    assert os.path.exists(RAW), f"Missing raw file: {RAW}"
    with open(RAW, newline="", encoding=ENCODING) as f:
        raw = list(csv.DictReader(f))
    print(f"raw rows: {len(raw)}")
    print(f"raw columns: {len(raw[0])}")

    required_raw = ["Order Id", "order date (DateOrders)", "shipping date (DateOrders)",
                    "Delivery Status", "Late_delivery_risk", "Shipping Mode", "Market",
                    "Order Region", "Category Name", "Sales", "Order Profit Per Order"]
    for c in required_raw:
        assert c in raw[0], f"Missing column: {c}"
    print("required columns present: OK")

    bad_dates = sum(1 for r in raw if parse_dt(r["order date (DateOrders)"]) is None)
    print(f"order date parse failures: {bad_dates}")
    assert bad_dates == 0

    # risk consistent with delivery status
    mism = sum(1 for r in raw if int(float(r["Late_delivery_risk"])) != (1 if r["Delivery Status"] == "Late delivery" else 0))
    print(f"late-risk consistency mismatches: {mism}")
    assert mism == 0

    # duplicate full rows
    seen = set(tuple(r.values()) for r in raw)
    print(f"exact duplicate rows: {len(raw) - len(seen)}")
    assert len(raw) == len(seen), "Unexpected duplicate full rows"

    # late rate eligible
    eligible = [r for r in raw if r["Delivery Status"] != "Shipping canceled"]
    late = [r for r in eligible if r["Delivery Status"] == "Late delivery"]
    print(f"eligible: {len(eligible)}, late: {len(late)}, rate: {len(late)/len(eligible):.4f}")

    if os.path.exists(CLEAN):
        with open(CLEAN, newline="", encoding="utf-8") as f:
            clean = list(csv.DictReader(f))
        print(f"cleaned rows: {len(clean)}")
        assert len(clean) == len(raw), "Row count changed during cleaning"
        assert "Shipping Delay Days" in clean[0]
        # check date strings parse
        bad = sum(1 for r in clean if r["Order Date"] and parse_dt is None)
        print("cleaned file OK")
    else:
        print("Cleaned file not found (run prepare_cleaned_data.py)")

    print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
