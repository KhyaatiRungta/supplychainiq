# Power BI data model ( SupplyChainIQ )

## Fact table: `FactOrders` (order-item grain)

Source: `data/processed/cleaned_supply_chain.csv` (29 columns). Measures are populated as
per `powerbi/dax/measures.dax`. Column names are PascalCase versions of the cleaned fields
(e.g. `OrderID`, `OrderDate`, `ShippingMode`, `Sales`, `OrderProfit`, `ActualShippingDays`,
`ScheduledShippingDays`, `ShippingDelayDays`, `DeliveryStatus`, `IsEligibleDelivery`,
`IsLateDelivery`, `CustomerSegment`, `CategoryName`, `DepartmentName`, `Market`,
`OrderRegion`, `ProductName`, `ProductID`, `ProductStatus`, `TransactionType`,
`Quantity`, `Discount`, `OrderStatus`, `ShippingDate`, `OrderCity`, `OrderCountry`,
`CustomerID`, `OrderItemID`, `LateDeliveryRisk`).

## Dimensions

| Dimension | Key / fields | Notes |
|---|---|---|
| DimDate | Date (PK), Year, Quarter, MonthNumber, MonthName, YearMonth | Mark as date table; active on FactOrders[OrderDate] |
| DimShippingMode | ShippingMode (PK), ScheduledDays | ScheduledDays = max/one value per mode |
| DimGeography | GeographyKey (Market & OrderRegion), Market, OrderRegion | Avoid many-to-many on country/city |
| DimProduct | ProductID (PK), ProductName, CategoryName, DepartmentName | Product-level ref only |
| DimCustomerSegment | CustomerSegment (PK) | |

## Relationships

- DimDate[Date] 1:* FactOrders[OrderDate] (active)
- DimDate[Date] 1:* FactOrders[ShippingDate] (inactive, for shipping-date analysis)
- DimShippingMode[ShippingMode] 1:* FactOrders[ShippingMode]
- DimGeography[GeographyKey] 1:* FactOrders (Market + OrderRegion concatenation key)
- DimProduct[ProductID] 1:* FactOrders[ProductID]
- DimCustomerSegment[CustomerSegment] 1:* FactOrders[CustomerSegment]
- Single direction (dimensions filter fact). No many-to-many.

## Data types / quality

- Date columns as date/time.
- Numeric measures as decimal/whole.
- Category fields trimmed (no trailing/extra spaces).
- DimDate month name sorted by MonthNumber.
- No customer-level PII in the model (no name/address/email/password/zip).
