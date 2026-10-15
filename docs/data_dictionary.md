# Data dictionary

Source: `DescriptionDataCoSupplySupplyChain.csv` (DataCo SMART Supply Chain).  
Raw schema: 53 columns, 180,519 order-item rows.  
Cleaned grain: order-item (one row per order item).

## Privacy exclusions (not used in any public output)

- Customer Email, Customer Fname, Customer Lname, Customer Password, Customer Street, Customer City, Customer State, Customer Zipcode, Customer Country.
- Latitude / Longitude (location-level detail).
- Product Description (empty in source), Product Image (URL).
- Benefit per order (duplicate of Order Profit Per Order), Order Item Total (derived), Product Price (reference only), Product Category Id / Department Id (redundant), Sales per customer (unreliable aggregate), Order Item Profit Ratio and Order Item Discount Rate (source-side ratios; weighted ratios are computed in DAX).

## Cleaned fact-table fields (`FactOrders`)

| Cleaned field | Source field(s) | Meaning | Type |
|---|---|---|---|
| OrderID | Order Id | Order identifier | Integer |
| OrderItemID | Order Item Id | Order-item identifier (unique in source) | Integer |
| OrderDate | order date (DateOrders) | Date/time the order was placed | Date/Time |
| ShippingDate | shipping date (DateOrders) | Date/time the item was shipped | Date/Time |
| OrderStatus | Order Status | Order lifecycle status | Text |
| DeliveryStatus | Delivery Status | Advance shipping / Late delivery / Shipping on time / Shipping canceled | Text |
| LateDeliveryRisk | Late_delivery_risk | Source late flag (1 = late); equals DeliveryStatus = 'Late delivery' | 0/1 |
| IsEligibleDelivery | derived | 1 when DeliveryStatus <> 'Shipping canceled' | 0/1 |
| IsLateDelivery | derived | 1 when DeliveryStatus = 'Late delivery' | 0/1 |
| ShippingMode | Shipping Mode | Standard/First/Second/Same Day | Text |
| ScheduledShippingDays | Days for shipment (scheduled) | Scheduled delivery days by mode | Integer |
| ActualShippingDays | Days for shipping (real) | Actual delivery days | Integer |
| ShippingDelayDays | derived | Actual - scheduled (positive = slower) | Decimal |
| Market | Market | Africa / Europe / LATAM / Pacific Asia / USCA | Text |
| OrderRegion | Order Region | Destination region (23 values) | Text |
| OrderCountry | Order Country | Destination country | Text |
| OrderCity | Order City | Destination city | Text |
| CustomerSegment | Customer Segment | Consumer / Corporate / Home Office | Text |
| DepartmentName | Department Name | Department (11 values) | Text |
| CategoryName | Category Name | Product category (50 values) | Text |
| ProductName | Product Name | Product name | Text |
| ProductStatus | Product Status | 0 = available, 1 = unavailable (all 0 in source) | 0/1 |
| Sales | Sales | Source sales value (= unit price x quantity) | Decimal (USD) |
| OrderProfit | Order Profit Per Order | Profit contribution (order-item grain) | Decimal (USD) |
| Quantity | Order Item Quantity | Units | Integer |
| Discount | Order Item Discount | Discount value | Decimal |
| TransactionType | Type | DEBIT / TRANSFER / PAYMENT / CASH | Text |
| CustomerID | Customer Id | Customer identifier (aggregation only) | Integer |
| ProductID | Product Card Id / Order Item Cardprod Id | Product identifier | Integer |

## Dimensions (Power BI)

- `DimDate` - Date, Year, Quarter, Month number, Month name, YearMonth
- `DimShippingMode` - ShippingMode, ScheduledDays
- `DimGeography` - Market, OrderRegion (OrderCountry/OrderCity available if needed)
- `DimProduct` - ProductID, ProductName, CategoryName, DepartmentName
- `DimCustomerSegment` - CustomerSegment

No supplier dimension is created: the source has no genuine supplier master data.
