<!-- Copyright (c) 2026 Khyaati Rungta. Licensed under the MIT Licence - see LICENSE. -->

# Reproducibility

Everything in this repository can be regenerated from the raw DataCo extract.
This page lists the exact order, what each step produces, and how to confirm
the output is correct.

## Prerequisites

- Python 3.9 or newer (the scripts use `csv`, `os`, `datetime` and `collections`
  from the standard library)
- `openpyxl`, declared in `requirements.txt`

```bash
python -m pip install -r requirements.txt
```

## Pipeline

Run these from the repository root, in order.

| Step | Command | Output | Notes |
| --- | --- | --- | --- |
| 1. Profile | `python scripts/inspect_data.py` | Console report | Shape, null counts, cardinality. Read this before changing anything. |
| 2. Clean | `python scripts/prepare_cleaned_data.py` | `data/processed/cleaned_supply_chain.csv` | Drops PII columns, derives delivery KPI fields. |
| 3. Validate | `python scripts/validate_data.py` | Console pass/fail | Row counts, KPI integrity, PII exclusion. |
| 4. Build workbook | `python scripts/build_excel_workbook.py` | `excel/supply_chain_analysis.xlsx` | Six sheets; the Cleaned Data sheet is an Excel Table named `CleanedData`. |

The interactive dashboard (`dashboard/index.html`) is hand-authored HTML with
the validated aggregates inlined. It has no build step and no dependencies -
open the file directly in a browser.

The Power BI model has no scripted build. Follow `docs/dashboard_design.md`
for the layout and load `powerbi/dax/measures.dax` for the measure layer.

## Expected validation results

These are the figures the validated cleaned extract produces. If `validate_data.py`
reports materially different numbers, the raw input is not the DataCo extract
this analysis was built on.

| Measure | Value |
| --- | --- |
| Order-item rows | 180,519 |
| Original columns | 53 |
| Distinct orders | 65,752 |
| Distinct customers | 20,652 |
| Distinct products | 118 |
| Period covered | 2015-01 to 2018-01 |
| Late delivery rate | 57.29% |
| Total sales | 36.8M USD |
| Order profit margin | 10.78% |

## Data provenance and licensing

The raw dataset is **not** redistributed here - it is gitignored on purpose.
Download it from Kaggle and keep it in `data/raw/`. See `LICENSE-NOTES.md` for
the attribution and reuse conditions that apply to the source data, and
`CITATION.cff` for how to cite this repository.

## Continuous integration

`.github/workflows/ci.yml` runs on every push and pull request. It
byte-compiles all scripts, parses each one with `ast` to surface the
third-party import set, and fails the build if any CSV extract has been
committed. It does not run the cleaning pipeline, because the raw data is not
in the repository.

## Determinism

The cleaning and validation scripts read the CSV with the standard library and
perform no randomised or time-dependent computation, so a given raw input
always produces byte-identical output. The workbook build stamps the
generation date in the Read Me sheet, so the `.xlsx` differs between runs in
that cell only.
