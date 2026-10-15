# Relational model reference (from the DataCo supply chain database-design project)

Source: https://github.com/adamchua97/dataco-supply-chain-database-design (Phase 1, GBA 6220, Cal Poly Pomona).

The DataCo dataset can also be modelled as a normalised relational schema with 11 entities.
Our Power BI model is deliberately denormalised into a star schema, but this reference documents
the underlying entities, keys and business rules used for validation.

## Entities (11)

| Type | Entity | Grain |
|---|---|---|
| Core | CUSTOMER | one per customer |
| Core | PRODUCT | one per product |
| Core | ORDER | one per order (65,752 distinct) |
| Core | ORDER_LOCATION | destination location |
| Junction | LINE | one per order item (180,519) |
| Weak | SHIPMENT | one per order (1:1 with ORDER) |
| Lookup | DEPARTMENT | 11 departments |
| Lookup | CATEGORY | 50 categories |
| Lookup | SHIPPING_MODE | 4 modes |
| Lookup | PAYMENT_TYPE | 4 types (Type) |
| Lookup | MARKET | 5 markets |

## Relationships and cardinality

- CUSTOMER 1:M ORDER
- ORDER 1:M LINE
- PRODUCT 1:M LINE
- DEPARTMENT 1:M CATEGORY
- CATEGORY 1:M PRODUCT
- ORDER 1:1 SHIPMENT (enforced by UNIQUE on `SHIPMENT.ORDER_ID`)
- SHIPPING_MODE 1:M ORDER
- PAYMENT_TYPE 1:M ORDER
- MARKET 1:M ORDER_LOCATION
- ORDER_LOCATION 1:M ORDER

## Design decisions

- Surrogate (AUTO_INCREMENT) keys for `SHIPMENT`, `SHIPPING_MODE`, `PAYMENT_TYPE`, `MARKET`, `ORDER_LOCATION` (no natural key in the source).
- `SHIPMENT.ORDER_ID` has a UNIQUE constraint to guarantee one shipment per order (weak entity).
- Two ambiguous/duplicate financial columns were removed from the physical model to avoid conflicting sources of truth:
  - `Sales per customer` (unreliable aggregate; excluded here too).
  - `Order Item Total` (equals Sales less discount; redundant once Sales and Discount coexist).
- Money stored as `DECIMAL(10,2)`; ratios `DECIMAL(5,4)`; ZIP codes `VARCHAR(10)` to keep leading zeros; binary flags `TINYINT(1)`; dates `DATETIME`.
- Standardised a geographic field mixed with Spanish-language values into English (mirrors our whitespace/label normalisation).

## How this informs the SupplyChainIQ star schema

- LINE is the `FactOrders` fact grain; PRODUCT/DEPARTMENT/CATEGORY roll into `DimProduct`;
  MARKET/ORDER_LOCATION roll into `DimGeography`; SHIPPING_MODE/PAYMENT_TYPE roll into
  `DimShippingMode`/a transaction-type attribute; CUSTOMER/ORDER attributes are kept only for
  aggregation (segment), never for PII.
- The 1:1 SHIPMENT relationship justifies a single set of shipping attributes on the fact row
  (actual days, scheduled days, shipping date) rather than a separate shipment fact.
- Derived-value elimination justifies computing `Order Profit Margin` as TotalProfit / TotalSales
  instead of averaging row-level ratios.

## Business rules referenced

- Valid value sets: Delivery Status = {Advance shipping, Late delivery, Shipping on time, Shipping canceled};
  Shipping Mode = {Standard Class, First Class, Second Class, Same Day};
  Customer Segment = {Consumer, Corporate, Home Office};
  Market = {Africa, Europe, LATAM, Pacific Asia, USCA};
  Product Status = 0 (available) / 1 (unavailable) — 0 in every source row.
- `Late_delivery_risk` = 1 iff Delivery Status = "Late delivery" (verified on all 180,519 rows).
- Order Item Profit Ratio is a per-item ratio; the weighted margin is Total Profit / Total Sales.

Business-rules and data-dictionary PDFs: see the linked repository.
