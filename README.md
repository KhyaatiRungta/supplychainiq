# SupplyChainIQ - Healthcare-Oriented Supply Chain Analytics

A portfolio-ready, end-to-end supply chain analytics project built on the real
**DataCo SMART Supply Chain** dataset. It demonstrates data inspection and cleaning,
KPI engineering, Excel analytics, a documented Power BI data model and DAX measures,
and evidence-backed business findings.

> Scope note: this is a general retail/e-commerce supply chain dataset. It is not MSD
> data and contains no pharmaceutical shipments. It is presented as a supply chain
> analytics case study with relevance to healthcare operations analytics.

## Business problem

Supply chain teams need to know how reliably orders are fulfilled, whether actual
shipping times meet scheduled commitments, and which shipping modes, regions,
categories or periods are associated with poor performance.

Question set: see `docs/business_insights.md` and `docs/dashboard_design.md`.

## Dataset

- DataCo SMART Supply Chain for Big Data Analysis
- Kaggle: https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis
- Data dictionary (source): `data/raw/DescriptionDataCoSupplyChain.csv`
- Profile: 180,519 order-item rows, 53 original columns, 2015-01 to 2018-01,
  65,752 distinct orders, 20,652 distinct customers, 118 distinct products.

The raw CSV (91 MB) is gitignored. Download it into `data/raw/`.

## Tools

Microsoft Excel, Power BI Desktop, Power Query, DAX, Git/GitHub (Python with pandas
optional; this build used the standard library plus openpyxl).

## Repository structure

    supplychainiq/
    ├── README.md
    ├── LICENSE-NOTES.md
    ├── .gitignore
    ├── data/raw/README.md
    ├── data/processed/README.md
    ├── excel/supply_chain_analysis.xlsx
    ├── powerbi/dax/measures.dax
    ├── scripts/inspect_data.py
    ├── scripts/validate_data.py
    ├── scripts/prepare_cleaned_data.py
    ├── docs/data_dictionary.md
    ├── docs/data_quality_report.md
    ├── docs/dashboard_design.md
    ├── docs/business_insights.md
    ├── docs/methodology.md
    └── screenshots/README.md

## Setup

1. Download `DataCoSupplyChainDataset.csv` and `DescriptionDataCoSupplyChain.csv`
   from Kaggle into `data/raw/`.
2. Run `python3 scripts/prepare_cleaned_data.py` to build the cleaned CSV.
3. Run `python3 scripts/validate_data.py` to check integrity.
4. Open `excel/supply_chain_analysis.xlsx` (already contains the cleaned table
   and validated summaries).

For Power BI, build the model following `docs/dashboard_design.md` and load the
measures from `powerbi/dax/measures.dax`.

## Workbook

Sheets: Read Me, Data Dictionary, Cleaned Data (Excel Table `CleanedData`),
Delivery Analysis, Pivot Setup, KPI Summary.

## KPIs

Distinct Orders; Order Items; Eligible Delivery Records; Late Delivery Records;
Late Delivery Rate (57.29%); On-Time Delivery Rate; Average Actual/Scheduled
Shipping Days; Average Shipping Delay; Total Sales (36.8M USD); Total Order Profit
(4.0M USD); Order Profit Margin (10.78%); Sales per Order.

## Dashboard pages (Power BI spec)

1. Executive Overview
2. Shipping Performance
3. Geography and Product Analysis
4. Business Performance and Insights

Full layout: `docs/dashboard_design.md`.

## Headline findings

1. 57.29% of eligible order items are delivered late.
2. First Class has a 100.00% late rate against a one-day promise; Standard Class
   has the best late rate (39.77%) at the largest volume.
3. Markets (56.8-57.7%) and regions (51.6-60.2%) are nearly level; mode policy
   explains more than geography.
4. Monthly late rate is stable around 57% with no seasonal spike.
5. Product categories and customer segments barely move the late rate (52.7-62.6%).
6. Total sales 36.8M USD; weighted margin 10.78%.

Full treatment: `docs/business_insights.md`.

## Limitations

- No genuine supplier/master data; no supplier scorecard or freight costs.
- No cause is claimed from correlation.
- No prediction model; descriptive analytics only.
- Live Power BI PBIX and Excel PivotTable objects were not generated
  programmatically in this environment; the complete specification is provided
  instead (see `docs/dashboard_design.md` and the `Pivot Setup` sheet).

## Reproducibility

See `docs/methodology.md`. Scripts are standard-library Python plus openpyxl
(already installed).

## Screenshots

Add high-quality exports of all four dashboard pages here once the PBIX is built.
