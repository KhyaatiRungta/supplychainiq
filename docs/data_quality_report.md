<!-- Copyright (c) 2026 Khyaati Rungta. Licensed under the MIT Licence - see LICENSE. -->

# Data quality report

## Source

- File: `DataCoSupplyChainDataset.csv` (+ `DescriptionDataCoSupplyChain.csv`)
- Primary source dataset: DataCo SMART Supply Chain for Big Data Analysis.
- Kaggle: https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis
- Original publication (Mendeley Data): https://data.mendeley.com/datasets/8gx2fvg2k6/5
- Mirror used for this build: https://github.com/YvMohsin/DataCo-SMART-SUPPLY-CHAIN-FOR-BIG-DATA-ANALYSIS
- Encoding read as Latin-1 (single-byte accented characters such as "Rajasthan"; CSV uses LF line endings).
- Rows: **180,519** order-item records (+ 1 header).
- Columns: **53**.
- Order date range: **2015-01-01** to **2018-01-31**.
- Shipping date range: 2015-01-03 to 2018-02-06.

## Missing values

| Field | Blank rows |
|---|---|
| Product Description | 180,519 (entirely empty - excluded) |
| Order Zipcode | 155,679 (mostly blank outside USCA - excluded) |
| Customer Zipcode | 3 |
| Customer Lname | 8 |
| (all others) | 0 |

Customer-facing fields are masked in source (`Customer Email`, `Customer Password` = `XXXXXXXXX`). They are excluded from all analytical outputs.

## Duplicates

- No exact duplicate rows (180,519 unique full rows).
- The source is at order-item grain; `Order Item Id` is unique. `Order Id` is not unique (180,519 rows / 65,752 distinct orders; mean 2.75 items per order).
- Duplicate order IDs are therefore legitimate line items, not data errors, and are not removed.
- `Order Customer Id` matches `Customer Id`.

## Date and numeric validation

- All 180,519 `order date` values parsed with `%m/%d/%Y %H:%M`.
- All 180,519 `shipping date` values parsed with the same pattern.
- `Days for shipping (real)` is an integer 0-6 and exactly matches `(shipping date - order date)` (0-day or 0.5-day rounding only).
- `Days for shipment (scheduled)` is 0, 1, 2 or 4 and is a fixed function of `Shipping Mode`.

## Delivery status

| Delivery Status | Rows |
|---|---|
| Late delivery | 98,977 |
| Advance shipping | 41,592 |
| Shipping on time | 32,196 |
| Shipping canceled | 7,754 |

`Late_delivery_risk` exactly equals 1 when Delivery Status = 'Late delivery' (0 mismatches across 180,519 rows).

## Cleaning decisions

1. Preserved the untouched source copy in `data/raw/`.
2. Read with Latin-1 encoding (verified readable; text remains intact).
3. Trimmed leading/trailing whitespace in categorical labels and collapsed repeated internal spaces (e.g. "Health and Beauty ", "South of  USA ").
4. Parsed dates to date/time types using an explicit format.
5. Standardised field names to PascalCase-ish readable names for the analytical model.
6. Added three derived flags/columns: `IsEligibleDelivery` (DeliveryStatus <> 'Shipping canceled'), `IsLateDelivery` (DeliveryStatus = 'Late delivery'), `ShippingDelayDays` (actual - scheduled).
7. Excluded personal, location, redundant and empty columns from the cleaned dataset (29 columns retained).
8. Did not replace missing values with zeros or arbitrary dates; blanks retained where source was blank (none affect required KPIs).
9. Row counts reconciled: raw 180,519 = cleaned 180,519 (+ header).

## Known limitations

- The dataset is a general retail/e-commerce supply chain; it is **not** an MSD, pharmaceutical, or healthcare logistics dataset. Findings are presented as a supply chain analytics case study only.
- There is no genuine supplier master data; no supplier scorecard or procurement cost analysis was attempted.
- `First Class` has a scheduled window of 1 day and an actual duration of 2 days in every row, so its 100% late rate reflects the tight service-level target at least as much as service quality. Actual delivery (2 days) is still faster than Standard Class (~4 days).
- `Order Zipcode` is mostly blank and is not used for geography (use Market / Order Region instead).
- `Sales per customer` does not reconcile to the sum of the `Sales` field and is excluded.
- Financial values (`Order Profit`) are stored at order-item grain but vary per item within an order; profit margin is computed as a weighted ratio, not by averaging row ratios.
- Order volume is ~5,000 rows/month for 2015-09/2017 and then falls to ~2,000/month for Oct-2017 to Jan-2018; treat late-2017 trends with appropriate caution.
- Month and regional differences in late-delivery rate are modest (about 52% to 61%); the largest single driver is the shipping-mode service level.
