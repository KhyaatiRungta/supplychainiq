# Dashboard design (SupplyChainIQ)

Power BI file name: `SupplyChainIQ.pbix` (build in Power BI Desktop following this spec).  
Colour palette: light background, dark navy headings, teal/blue accents, amber/red warnings.

## Intended model

- Fact: `FactOrders` (order-item grain).
- Dimensions: `DimDate`, `DimShippingMode`, `DimGeography`, `DimProduct`, `DimCustomerSegment`.
- Active date: `FactOrders[OrderDate]` -> `DimDate[Date]`.
- Date table marked as a date table; month names sorted by month number.
- Single-direction relationships (dimensions -> fact).

## Page 1 - Executive Overview

KPI cards: Distinct Orders; Eligible Delivery Records; Late Delivery Rate; Average Actual Shipping Days; Average Shipping Delay; Total Sales.

Visuals:
1. Monthly order volume and late-delivery trend (line/area).
2. Late Delivery Rate by Shipping Mode (bar, sorted descending).
3. Delivery Status distribution (donut).
4. Late Delivery Rate by Region (bar or matrix, top 8 and bottom 8).
Slicers: Date (OrderDate), Shipping Mode, Market, Category.

## Page 2 - Shipping Performance

1. Actual vs scheduled shipping days by Shipping Mode (clustered bar).
2. Late Delivery Rate by Shipping Mode.
3. Late Delivery Rate by Region.
4. Delay distribution (histogram grouped by delay buckets -3..+4).
5. Detail table: Shipping Mode, eligible items, scheduled days, actual days, late rate.
Slicers + cross-filtering + tooltips (eligible record count + metric definition).

## Page 3 - Geography and Product

1. Late Delivery Rate by Order Region.
2. Order volume by Market.
3. Late Delivery Rate and Sales by Category (scatter or matrix).
4. Sales and Order Profit by Category (bar, top 10).
5. Shipping-mode composition by Region (stacked bar).
Use bar chart instead of map (fields are region/country, not lat/long in the published model).

## Page 4 - Business Performance and Insights

1. Sales trend over time.
2. Order profit by category (or department).
3. Late rate vs profit margin by category/region (scatter, descriptive only).
4. Product category performance matrix.
5. Text box: four key findings + recommended follow-up investigations.

## Formatting rules

- Percentages as %; money as USD with 0 or 2 decimals; counts with thousands separators.
- Dynamic titles on category/region visuals where helpful.
- Reset Filters button via bookmarks if feasible.
- No customer-level PII on any page.
