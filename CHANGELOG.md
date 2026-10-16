# Changelog

Notable changes to SupplyChainIQ are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Dates are the day the change was committed, not the day the underlying analysis
was performed.

## [Unreleased]

## [1.0.0] - 2026-10-15

First complete release of the analysis.

### Added

- `scripts/inspect_data.py` - profiles the raw DataCo extract: shape, column
  types, null counts and cardinality.
- `scripts/prepare_cleaned_data.py` - builds the analysed table from the raw
  CSV, dropping PII columns and deriving delivery KPI fields.
- `scripts/validate_data.py` - integrity checks over the cleaned table: row
  counts, referential consistency and confirmation that no PII survives.
- `scripts/build_excel_workbook.py` - generates
  `excel/supply_chain_analysis.xlsx` (Read Me, Data Dictionary, Cleaned Data,
  Delivery Analysis, Pivot Setup, KPI Summary).
- `powerbi/data_model.md` and `powerbi/dax/measures.dax` - documented star
  schema and the DAX measure layer.
- `powerbi/SupplyChainIQ.pbip` - Power BI Project opening the report and
  semantic model together in Power BI Desktop.
- `powerbi/SupplyChainIQ.SemanticModel/` - TMDL semantic model: `FactOrders`
  (30 columns loaded from the cleaned CSV in Power Query, 16 measures) plus
  `DimDate`, `DimShippingMode`, `DimGeography`, `DimProduct` and
  `DimCustomerSegment`, with 6 relationships matching `powerbi/data_model.md`.
- `powerbi/SupplyChainIQ.Report/` - PBIR report definition: 4 pages
  (Executive Overview, Shipping Performance, Geography and Product Analysis,
  Business Performance and Insights) with 30 visuals.
- `dashboard/index.html` - dependency-free single-file interactive dashboard
  with animated KPIs and charts.
- `docs/` - methodology, data dictionary, data quality report, dashboard
  design, relational model reference and business insights.
- `screenshots/dashboard.png` - rendered capture of the HTML dashboard.
- `requirements.txt`, `.gitattributes`, `.editorconfig`,
  `.github/workflows/ci.yml`, `CITATION.cff`, `docs/reproducibility.md`.
- MIT `LICENSE`, per the request recorded in `LICENSE-NOTES.md`.

### Notes

- The 91 MB raw CSV and the 46 MB cleaned CSV are gitignored. Download the raw
  file from Kaggle into `data/raw/` and regenerate the cleaned extract with
  `scripts/prepare_cleaned_data.py`.
- The Power BI `.pbix` is not committed (gitignored); the complete model
  specification is provided instead.
