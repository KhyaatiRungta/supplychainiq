# Copyright (c) 2026 Khyaati Rungta. Licensed under the MIT Licence - see LICENSE.

import csv, os, datetime, collections
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw", "DataCoSupplyChainDataset.csv")
CLEANED = os.path.join(ROOT, "data", "processed", "cleaned_supply_chain.csv")
OUT = os.path.join(ROOT, "excel", "supply_chain_analysis.xlsx")

NAVY = "1F3864"
TEAL = "0F766E"
LIGHT = "F2F5F9"
GREY = "D9D9D9"
WARN = "C00000"

thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = Workbook()

def style_header(ws, row=1, ncols=None):
    if ncols is None:
        ncols = ws.max_column
    for c in range(1, ncols+1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(bold=True, color="FFFFFF", size=10)
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER

def title_block(ws, title, subtitle=None):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=14, color=NAVY)
    r = 2
    if subtitle:
        ws.cell(row=r, column=1, value=subtitle).font = Font(italic=True, size=10, color="404040")
        r += 1
    return r + 1

def autosize(ws, max_width=42):
    for col in ws.columns:
        length = 0
        letter = col[0].column_letter
        for cell in col:
            if cell.value is not None:
                l = len(str(cell.value))
                if l > length:
                    length = l
        ws.column_dimensions[letter].width = min(max(length+2, 10), max_width)

# ============================================================
# Sheet 1: Read Me
# ============================================================
ws = wb.active
ws.title = "Read Me"
ws.sheet_properties.tabColor = NAVY
r = title_block(ws, "SupplyChainIQ - Excel Analytics Workbook", "Healthcare-oriented supply chain analytics case study (general supply chain data)")
lines = [
    ("Project", "SupplyChainIQ - Healthcare-Oriented Supply Chain Analytics"),
    ("Purpose", "Analyse delivery reliability, shipping performance, geography, products and profitability using the real DataCo SMART Supply Chain dataset."),
    ("Dataset", "DataCo SMART Supply Chain for Big Data Analysis (Kaggle / Mendeley Data)."),
    ("Source URL", "https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis"),
    ("Attribution", "Fabian Constante et al.; use must follow the source licence. Source data is not committed to the repository."),
    ("Workbook grain", "Order-item level. Each row in 'Cleaned Data' is one order item. Distinct orders are counted separately."),
    ("Scope note", "This is a general retail/e-commerce supply chain dataset, not MSD data and not pharmaceutical shipments. It is used as a portfolio case study relevant to healthcare operations analytics."),
    ("How to use", "1) Inspect 'Data Dictionary'. 2) Filter 'Cleaned Data'. 3) Review 'Delivery Analysis' and 'KPI Summary'. 4) Build PivotTables from the 'CleanedData' Excel Table (see 'Pivot Setup')."),
    ("Key KPI", "Late Delivery Rate = late eligible items / eligible delivery items (excludes 'Shipping canceled')."),
    ("Known limit", "No live PivotTable objects were embedded programmatically. Create them in Excel via Insert > PivotTable from the CleanedData table."),
]
start = r
for label, value in lines:
    ws.cell(row=r, column=1, value=label).font = Font(bold=True, color=NAVY)
    ws.cell(row=r, column=2, value=value).alignment = Alignment(wrap_text=True, vertical="top")
    r += 1
ws.column_dimensions["A"].width = 22
ws.column_dimensions["B"].width = 110

# ============================================================
# Sheet 2: Data Dictionary (from description file + mapping)
# ============================================================
ddesc = {}
try:
    with open(os.path.join(ROOT, "data", "raw", "DescriptionDataCoSupplyChain.csv"), newline="", encoding="latin-1") as f:
        for row in csv.DictReader(f):
            ddesc[row["FIELDS"].strip()] = row["DESCRIPTION"].strip().lstrip(":").strip()
except Exception:
    pass

clean_map = {
    "Type": ("Transaction Type", "Cleaned"),
    "Days for shipping (real)": ("Actual Shipping Days", "Cleaned"),
    "Days for shipment (scheduled)": ("Scheduled Shipping Days", "Cleaned"),
    "Benefit per order": ("Order Profit (derived duplicate removed)", "Not retained (duplicate of Order Profit Per Order)"),
    "Sales per customer": ("(not retained)", "Not retained (unreliable customer aggregate)"),
    "Delivery Status": ("Delivery Status", "Cleaned"),
    "Late_delivery_risk": ("Late Delivery Risk", "Cleaned"),
    "Category Id": ("(not retained)", "Not retained (redundant with Product Category)"),
    "Category Name": ("Category Name", "Cleaned; whitespace trimmed"),
    "Customer City": ("(not retained)", "Excluded (customer-level detail)"),
    "Customer Country": ("(not retained)", "Excluded (customer-level detail)"),
    "Customer Email": ("(not retained)", "Excluded (PII, masked)"),
    "Customer Fname": ("(not retained)", "Excluded (PII)"),
    "Customer Id": ("Customer ID", "Cleaned"),
    "Customer Lname": ("(not retained)", "Excluded (PII)"),
    "Customer Password": ("(not retained)", "Excluded (PII, masked)"),
    "Customer Segment": ("Customer Segment", "Cleaned"),
    "Customer State": ("(not retained)", "Excluded (customer/store-level detail)"),
    "Customer Street": ("(not retained)", "Excluded (PII)"),
    "Customer Zipcode": ("(not retained)", "Excluded (PII)"),
    "Department Id": ("(not retained)", "Not retained (redundant with name)"),
    "Department Name": ("Department Name", "Cleaned; whitespace trimmed"),
    "Latitude": ("(not retained)", "Excluded (location-level detail)"),
    "Longitude": ("(not retained)", "Excluded (location-level detail)"),
    "Market": ("Market", "Cleaned"),
    "Order City": ("Order City", "Cleaned"),
    "Order Country": ("Order Country", "Cleaned"),
    "Order Customer Id": ("Customer ID (duplicate)", "Not retained (duplicate key)"),
    "order date (DateOrders)": ("Order Date", "Cleaned; parsed to date/time"),
    "Order Id": ("Order ID", "Cleaned"),
    "Order Item Cardprod Id": ("Product ID", "Cleaned"),
    "Order Item Discount": ("Order Item Discount", "Cleaned"),
    "Order Item Discount Rate": ("(not retained)", "Not retained (derivable)"),
    "Order Item Id": ("Order Item ID", "Cleaned"),
    "Order Item Product Price": ("(not retained)", "Not retained (reference price)"),
    "Order Item Profit Ratio": ("(not retained)", "Not retained (source ratio not weighted)"),
    "Order Item Quantity": ("Order Item Quantity", "Cleaned"),
    "Sales": ("Sales", "Cleaned; validated as unit price x quantity"),
    "Order Item Total": ("(not retained)", "Not retained (equals Sales less discount)"),
    "Order Profit Per Order": ("Order Profit", "Cleaned; renamed for grain clarity"),
    "Order Region": ("Order Region", "Cleaned; whitespace normalised"),
    "Order State": ("(not retained)", "Not retained (region-level reporting used)"),
    "Order Status": ("Order Status", "Cleaned"),
    "Order Zipcode": ("(not retained)", "Not retained (mostly blank outside USCA)"),
    "Product Card Id": ("Product ID (duplicate)", "Not retained (duplicate key)"),
    "Product Category Id": ("(not retained)", "Not retained (redundant with name)"),
    "Product Description": ("(not retained)", "Excluded (empty in source)"),
    "Product Image": ("(not retained)", "Excluded (URL, not needed)"),
    "Product Name": ("Product Name", "Cleaned; trailing space removed"),
    "Product Price": ("(not retained)", "Not retained (reference only)"),
    "Product Status": ("Product Status", "Cleaned (0=available)"),
    "shipping date (DateOrders)": ("Shipping Date", "Cleaned; parsed to date/time"),
    "Shipping Mode": ("Shipping Mode", "Cleaned"),
}

type_map = {
    "Type": "Text", "Days for shipping (real)": "Integer", "Days for shipment (scheduled)": "Integer",
    "Benefit per order": "Decimal", "Sales per customer": "Decimal", "Delivery Status": "Text",
    "Late_delivery_risk": "Integer (0/1)", "Category Id": "Integer", "Category Name": "Text",
    "Customer City": "Text", "Customer Country": "Text", "Customer Email": "Text",
    "Customer Fname": "Text", "Customer Id": "Integer", "Customer Lname": "Text",
    "Customer Password": "Text", "Customer Segment": "Text", "Customer State": "Text",
    "Customer Street": "Text", "Customer Zipcode": "Text", "Department Id": "Integer",
    "Department Name": "Text", "Latitude": "Decimal", "Longitude": "Decimal",
    "Market": "Text", "Order City": "Text", "Order Country": "Text", "Order Customer Id": "Integer",
    "order date (DateOrders)": "Date/Time", "Order Id": "Integer", "Order Item Cardprod Id": "Integer",
    "Order Item Discount": "Decimal", "Order Item Discount Rate": "Decimal", "Order Item Id": "Integer",
    "Order Item Product Price": "Decimal", "Order Item Profit Ratio": "Decimal",
    "Order Item Quantity": "Integer", "Sales": "Decimal", "Order Item Total": "Decimal",
    "Order Profit Per Order": "Decimal", "Order Region": "Text", "Order State": "Text",
    "Order Status": "Text", "Order Zipcode": "Text", "Product Card Id": "Integer",
    "Product Category Id": "Integer", "Product Description": "Text", "Product Image": "Text",
    "Product Name": "Text", "Product Price": "Decimal", "Product Status": "Integer (0/1)",
    "shipping date (DateOrders)": "Date/Time", "Shipping Mode": "Text",
}

with open(os.path.join(RAW, "..", "DescriptionDataCoSupplyChain.csv") if False else os.path.join(ROOT,"data","raw","DescriptionDataCoSupplyChain.csv"), newline="", encoding="latin-1") as f:
    desc_rows = list(csv.DictReader(f))

# fix field name keys (description file has trailing spaces)
ws = wb.create_sheet("Data Dictionary")
ws.sheet_properties.tabColor = TEAL
headers = ["Original Field", "Cleaned Field", "Description (source)", "Data Type", "Example Value (actual)", "Used In Analysis?", "Privacy / Quality Notes"]
ws.append(headers)
style_header(ws, 1, len(headers))

# extract example values from raw
import itertools
example_cache = {}
raw_head = list(csv.DictReader(open(os.path.join(ROOT,"data","raw","DataCoSupplyChainDataset.csv"), newline="", encoding="latin-1")))
for src in clean_map.keys():
    vals = [r[src].strip() for r in raw_head[:200] if r[src].strip() != ""]
    example_cache[src] = vals[0] if vals else ""

for d in desc_rows:
    src = d["FIELDS"].strip()
    desc = d["DESCRIPTION"].strip().lstrip(":").strip()
    clean_field, note = clean_map.get(src, ("(not reviewed)", "Not reviewed"))
    used = "No" if clean_field.startswith("(") else "Yes"
    if src in ("Customer Email","Customer Fname","Customer Lname","Customer Password","Customer Street","Customer Zipcode","Product Description","Product Image"):
        used = "No (excluded)"
    ex = example_cache.get(src, "")
    if len(ex) > 40:
        ex = ex[:37] + "..."
    ws.append([src, clean_field, desc, type_map.get(src, "Text"), ex, used, note])

# append cleaned calculated columns
calc_rows = [
    ("(calculated)", "Eligible For Delivery KPI", "Eligible record flag: Delivery Status != 'Shipping canceled'.", "Integer (0/1)", "1", "Yes", "Derived in cleaning."),
    ("(calculated)", "Late Delivery (KPI)", "Late flag: Delivery Status == 'Late delivery'.", "Integer (0/1)", "1", "Yes", "Derived in cleaning."),
    ("(calculated)", "Shipping Delay Days", "Actual Shipping Days - Scheduled Shipping Days.", "Decimal", "1.0", "Yes", "Derived in cleaning."),
]
for r in calc_rows:
    ws.append(list(r))

autosize(ws, 46)
ws.freeze_panes = "A2"
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    row[2].alignment = Alignment(wrap_text=True)
    row[6].alignment = Alignment(wrap_text=True)

# ============================================================
# Sheet 3: Cleaned Data
# ============================================================
ws = wb.create_sheet("Cleaned Data")
ws.sheet_properties.tabColor = "7F7F7F"
with open(CLEANED, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    ws.append(header)
    style_header(ws, 1, len(header))
    count = 0
    for row in reader:
        # convert known columns for Excel types
        out = list(row)
        # date columns 3 and 4 -> datetime
        for idx in (2, 3):
            val = out[idx]
            if val:
                try:
                    out[idx] = datetime.datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    pass
        # numeric
        for idx in (11, 12, 13, 23, 24, 25, 6, 7, 8):
            val = out[idx]
            if val not in ("", None):
                try:
                    out[idx] = float(val) if "." in str(val) else int(val)
                except Exception:
                    pass
        ws.append(out)
        count += 1
        if count >= 180519:
            pass
print("cleaned rows written to workbook:", count)

date_fmt = "yyyy-mm-dd hh:mm"
ws.cell(row=1, column=3).number_format = date_fmt
ws.cell(row=1, column=4).number_format = date_fmt
for r in range(2, ws.max_row+1):
    ws.cell(row=r, column=3).number_format = date_fmt
    ws.cell(row=r, column=4).number_format = date_fmt
    for c in (11,12,13):
        ws.cell(row=r, column=c+1).number_format = "0.00"
    ws.cell(row=r, column=22).number_format = "$#,##0.00"
    ws.cell(row=r, column=23).number_format = "$#,##0.00"
    ws.cell(row=r, column=25).number_format = "0.00"
    ws.cell(row=r, column=16).number_format = "0"
    ws.cell(row=r, column=17).number_format = "0.00%"

tab = Table(displayName="CleanedData", ref=f"A1:{get_column_letter(len(header))}{ws.max_row}")
style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                      showLastColumn=False, showRowStripes=True, showColumnStripes=False)
tab.tableStyleInfo = style
ws.add_table(tab)
ws.freeze_panes = "C2"
autosize(ws, 24)

# ============================================================
# Save computed summary values (from full cleaned data)
# ============================================================
def load_cleaned():
    rows = []
    with open(CLEANED, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        for r in rd:
            rows.append(r)
    return rows
CROWS = load_cleaned()
for r in CROWS:
    r["Sales"] = float(r["Sales"])
    r["Order Profit"] = float(r["Order Profit"])
    r["Scheduled Shipping Days"] = float(r["Scheduled Shipping Days"])
    r["Actual Shipping Days"] = float(r["Actual Shipping Days"])
    r["Shipping Delay Days"] = float(r["Shipping Delay Days"])
    r["Eligible"] = r["Eligible For Delivery KPI"] == "1"
    r["Late"] = r["Late Delivery (KPI)"] == "1"
ELIG = [r for r in CROWS if r["Eligible"]]
LATE = [r for r in ELIG if r["Late"]]

def is_cancelled(r): return r["Delivery Status"] == "Shipping canceled"

total_rows = len(CROWS)
eligible_n = len(ELIG)
late_n = len(LATE)
distinct_orders = len({r["Order ID"] for r in CROWS})
distinct_orders_elig = len({r["Order ID"] for r in ELIG})
total_sales = sum(r["Sales"] for r in CROWS)
total_profit = sum(r["Order Profit"] for r in CROWS)
margin = total_profit / total_sales
avg_actual = sum(r["Actual Shipping Days"] for r in ELIG)/eligible_n
avg_sched = sum(r["Scheduled Shipping Days"] for r in ELIG)/eligible_n
avg_delay = sum(r["Shipping Delay Days"] for r in ELIG)/eligible_n
late_rate = late_n / eligible_n
ontime_rate = 1 - late_rate

# mode summary
modes = {}
for r in ELIG:
    m = r["Shipping Mode"]
    d = modes.setdefault(m, {"n":0,"late":0,"real":0.0,"sched":0.0,"delay":0.0,"sales":0.0,"profit":0.0})
    d["n"] += 1
    if r["Late"]: d["late"] += 1
    d["real"] += r["Actual Shipping Days"]
    d["sched"] += r["Scheduled Shipping Days"]
    d["delay"] += r["Shipping Delay Days"]
    d["sales"] += r["Sales"]
    d["profit"] += r["Order Profit"]
mode_order = ["Same Day","First Class","Second Class","Standard Class"]

# market summary
markets = {}
for r in ELIG:
    m = r["Market"]
    d = markets.setdefault(m, {"n":0,"late":0,"real":0.0,"sales":0.0})
    d["n"] += 1
    if r["Late"]: d["late"] += 1
    d["real"] += r["Actual Shipping Days"]
    d["sales"] += r["Sales"]

# region summary (n>=500)
regions = {}
for r in ELIG:
    reg = r["Order Region"]
    d = regions.setdefault(reg, {"n":0,"late":0})
    d["n"] += 1
    if r["Late"]: d["late"] += 1
reg_list = sorted([(reg,d["n"],100*d["late"]/d["n"]) for reg,d in regions.items() if d["n"]>=500], key=lambda x:-x[2])

# category summary (top sales)
cats = {}
for r in ELIG:
    c = r["Category Name"]
    d = cats.setdefault(c, {"n":0,"late":0,"sales":0.0,"profit":0.0})
    d["n"] += 1
    if r["Late"]: d["late"] += 1
    d["sales"] += r["Sales"]
    d["profit"] += r["Order Profit"]
cat_list = sorted(cats.items(), key=lambda kv:-kv[1]["sales"])[:12]

# segment summary
segs = {}
for r in ELIG:
    s = r["Customer Segment"]
    d = segs.setdefault(s, {"n":0,"late":0,"sales":0.0,"profit":0.0})
    d["n"] += 1
    if r["Late"]: d["late"] += 1
    d["sales"] += r["Sales"]
    d["profit"] += r["Order Profit"]

# monthly count + late (last 4 months lower)
import collections
months = collections.OrderedDict()
for r in ELIG:
    ym = r["Order Date"][:7]
    d = months.setdefault(ym, {"n":0,"late":0})
    d["n"] += 1
    if r["Late"]: d["late"] += 1
month_rows = list(months.items())

# ============================================================
# Sheet 4: Delivery Analysis (static summaries with formulas note)
# ============================================================
ws = wb.create_sheet("Delivery Analysis")
ws.sheet_properties.tabColor = "C00000"
r = title_block(ws, "Delivery performance summaries", "Values calculated from the full 180,519-row source. Shipping mode drives most of the late-delivery variation.")
# KPI table top
ws.cell(row=r, column=1, value="Core delivery KPIs").font = Font(bold=True, color=NAVY)
r += 1
kpi_header = ["KPI", "Value", "Definition"]
ws.append([])  # placeholder skip handling manually
# build manually
row0 = r
hdrs = ["KPI", "Value", "Definition"]
for i,h in enumerate(hdrs):
    ws.cell(row=row0, column=1+i, value=h)
style_header(ws, row0, 3)
r = row0 + 1
kpi_rows = [
    ("Total order items (fact rows)", total_rows, "#,##0", "Rows in the source at order-item grain."),
    ("Distinct orders", distinct_orders, "#,##0", "Distinct Order ID values."),
    ("Eligible delivery items", eligible_n, "#,##0", "Excludes 'Shipping canceled'."),
    ("Late delivery items", late_n, "#,##0", "Delivery Status = 'Late delivery'."),
    ("Late delivery rate", late_rate, "0.00%", "Late eligible items / eligible delivery items."),
    ("On-time delivery rate", ontime_rate, "0.00%", "1 - late delivery rate (eligible items)."),
    ("Average actual shipping days", avg_actual, "0.00", "Eligible items only."),
    ("Average scheduled shipping days", avg_sched, "0.00", "Eligible items only."),
    ("Average shipping delay (days)", avg_delay, "0.00", "Actual minus scheduled; positive = slower than schedule."),
    ("Total sales (USD)", total_sales, "$#,##0", "Sum of the source Sales field."),
    ("Total order profit (USD)", total_profit, "$#,##0", "Sum of 'Order Profit Per Order'."),
    ("Order profit margin (weighted)", margin, "0.0%", "Total profit / total sales (weighted)."),
]
for name, val, fmt, defin in kpi_rows:
    ws.cell(row=r, column=1, value=name)
    c = ws.cell(row=r, column=2, value=val); c.number_format = fmt
    ws.cell(row=r, column=3, value=defin).alignment = Alignment(wrap_text=True)
    r += 1
ws.column_dimensions["A"].width = 36
ws.column_dimensions["B"].width = 18
ws.column_dimensions["C"].width = 52

# shipping mode table
r += 1
ws.cell(row=r, column=1, value="Delivery performance by shipping mode (eligible items)").font = Font(bold=True, color=NAVY)
r += 1
mhdr = ["Shipping Mode", "Eligible Items", "Late Items", "Late Rate", "Avg Actual Days", "Avg Scheduled Days", "Avg Delay", "Sales (USD)"]
for i,h in enumerate(mhdr):
    ws.cell(row=r, column=1+i, value=h)
style_header(ws, r, len(mhdr))
mhdr_row = r
r += 1
for mode in mode_order:
    d = modes[mode]
    ws.cell(row=r, column=1, value=mode)
    ws.cell(row=r, column=2, value=d["n"]).number_format = "#,##0"
    ws.cell(row=r, column=3, value=d["late"]).number_format = "#,##0"
    c = ws.cell(row=r, column=4, value=d["late"]/d["n"]); c.number_format = "0.00%"
    ws.cell(row=r, column=5, value=d["real"]/d["n"]).number_format = "0.00"
    ws.cell(row=r, column=6, value=d["sched"]/d["n"]).number_format = "0.00"
    ws.cell(row=r, column=7, value=d["delay"]/d["n"]).number_format = "0.00"
    ws.cell(row=r, column=8, value=d["sales"]).number_format = "$#,##0"
    r += 1
# total row
ws.cell(row=r, column=1, value="Total").font = Font(bold=True)
ws.cell(row=r, column=2, value=eligible_n).number_format = "#,##0"
ws.cell(row=r, column=3, value=late_n).number_format = "#,##0"
ws.cell(row=r, column=4, value=late_rate).number_format = "0.00%"
ws.cell(row=r, column=5, value=avg_actual).number_format = "0.00"
ws.cell(row=r, column=6, value=avg_sched).number_format = "0.00"
ws.cell(row=r, column=7, value=avg_delay).number_format = "0.00"
ws.cell(row=r, column=8, value=sum(d["sales"] for d in modes.values())).number_format = "$#,##0"
for c in range(1, len(mhdr)+1):
    ws.cell(row=r, column=c).font = Font(bold=True)
    ws.cell(row=r, column=c).fill = PatternFill("solid", fgColor=LIGHT)
r += 2

# market table
ws.cell(row=r, column=1, value="Delivery performance by market (eligible items)").font = Font(bold=True, color=NAVY)
r += 1
for i,h in enumerate(["Market", "Eligible Items", "Late Items", "Late Rate", "Avg Actual Days", "Sales (USD)"]):
    ws.cell(row=r, column=1+i, value=h)
style_header(ws, r, 6)
r += 1
for market in sorted(markets.keys()):
    d = markets[market]
    ws.cell(row=r, column=1, value=market)
    ws.cell(row=r, column=2, value=d["n"]).number_format = "#,##0"
    ws.cell(row=r, column=3, value=d["late"]).number_format = "#,##0"
    ws.cell(row=r, column=4, value=d["late"]/d["n"]).number_format = "0.00%"
    ws.cell(row=r, column=5, value=d["real"]/d["n"]).number_format = "0.00"
    ws.cell(row=r, column=6, value=d["sales"]).number_format = "$#,##0"
    r += 1
r += 1

# region extremes
ws.cell(row=r, column=1, value="Regions with the highest late-delivery rates (eligible items, n>=500)").font = Font(bold=True, color=NAVY)
r += 1
for i,h in enumerate(["Order Region", "Eligible Items", "Late Rate"]):
    ws.cell(row=r, column=1+i, value=h)
style_header(ws, r, 3)
r += 1
for reg, n, rate in reg_list[:8]:
    ws.cell(row=r, column=1, value=reg)
    ws.cell(row=r, column=2, value=n).number_format = "#,##0"
    ws.cell(row=r, column=3, value=rate/100).number_format = "0.00%"
    r += 1
r += 1
ws.cell(row=r, column=1, value="Regions with the lowest late-delivery rates (eligible items, n>=500)").font = Font(bold=True, color=NAVY)
r += 1
for i,h in enumerate(["Order Region", "Eligible Items", "Late Rate"]):
    ws.cell(row=r, column=1+i, value=h)
style_header(ws, r, 3)
r += 1
for reg, n, rate in sorted(reg_list, key=lambda x:x[2])[:8]:
    ws.cell(row=r, column=1, value=reg)
    ws.cell(row=r, column=2, value=n).number_format = "#,##0"
    ws.cell(row=r, column=3, value=rate/100).number_format = "0.00%"
    r += 1
r += 1

# segment
ws.cell(row=r, column=1, value="Customer segment performance (eligible items)").font = Font(bold=True, color=NAVY)
r += 1
for i,h in enumerate(["Customer Segment", "Eligible Items", "Late Rate", "Sales (USD)", "Profit Margin (weighted)"]):
    ws.cell(row=r, column=1+i, value=h)
style_header(ws, r, 5)
r += 1
for seg in sorted(segs.keys()):
    d = segs[seg]
    ws.cell(row=r, column=1, value=seg)
    ws.cell(row=r, column=2, value=d["n"]).number_format = "#,##0"
    ws.cell(row=r, column=3, value=d["late"]/d["n"]).number_format = "0.00%"
    ws.cell(row=r, column=4, value=d["sales"]).number_format = "$#,##0"
    ws.cell(row=r, column=5, value=d["profit"]/d["sales"]).number_format = "0.0%"
    r += 1
r += 1
ws.cell(row=r, column=1, value="Department late-delivery rates (eligible items)").font = Font(bold=True, color=NAVY)
r += 1
deps = {}
for rr in ELIG:
    dep = rr["Department Name"]
    d = deps.setdefault(dep, {"n":0,"late":0,"sales":0.0,"profit":0.0})
    d["n"] += 1
    if rr["Late"]: d["late"] += 1
    d["sales"] += rr["Sales"]
    d["profit"] += rr["Order Profit"]
for i,h in enumerate(["Department", "Eligible Items", "Late Rate", "Sales (USD)", "Profit Margin (weighted)"]):
    ws.cell(row=r, column=1+i, value=h)
style_header(ws, r, 5)
r += 1
for dep, d in sorted(deps.items(), key=lambda kv:-kv[1]["sales"]):
    ws.cell(row=r, column=1, value=dep)
    ws.cell(row=r, column=2, value=d["n"]).number_format = "#,##0"
    ws.cell(row=r, column=3, value=d["late"]/d["n"]).number_format = "0.00%"
    ws.cell(row=r, column=4, value=d["sales"]).number_format = "$#,##0"
    ws.cell(row=r, column=5, value=d["profit"]/d["sales"]).number_format = "0.0%"
    r += 1

# ============================================================
# Sheet 5: PivotTables (precomputed + setup guide)
# ============================================================
ws = wb.create_sheet("Pivot Setup")
ws.sheet_properties.tabColor = "7F6000"
ws["A1"] = "How to create the required PivotTables"
ws["A1"].font = Font(bold=True, size=14, color=NAVY)
notes = [
    "The cleaned data is stored in the Excel Table 'CleanedData' on the 'Cleaned Data' sheet (order-item grain).",
    "In Excel: Insert > PivotTable > From Table/Range, source = CleanedData.",
    "Recommended layouts:",
    "1) Shipping mode performance: Rows=Shipping Mode; Values=Late items (count), Eligible items (count), Late rate (average of 'Late Delivery (KPI)'? no - build calc field), Avg Actual, Avg Scheduled.",
    "2) Regional delivery performance: Rows=Order Region (filter by Market); Values=Eligible items, Late rate, Sales.",
    "3) Monthly delivery trends: Rows=Order Date grouped by Year+Month; Values=Eligible items, Late items, Late rate.",
    "4) Product category performance: Rows=Category Name (filter by Department Name); Values=Eligible items, Late rate, Sales, Order Profit.",
    "5) Sales and order-profit analysis: Rows=Customer Segment; Values=Sales (sum), Order Profit (sum), Profit margin (calculated).",
    "Tip: Latency/late rate should be added as a calculated field = 'Late Delivery (KPI)' average, or a DAX-ish field via Value Field Settings.",
]
rr = 3
for n in notes:
    ws.cell(row=rr, column=1, value=n).alignment = Alignment(wrap_text=True)
    rr += 1
ws.column_dimensions["A"].width = 150

# ============================================================
# Sheet 6: KPI Summary
# ============================================================
ws = wb.create_sheet("KPI Summary")
ws.sheet_properties.tabColor = "0F766E"
r = title_block(ws, "Validated KPI summary", "Denominators and eligibility follow the documented rules.")
hdrs = ["KPI", "Value", "Denominator / eligibility", "Notes"]
for i,h in enumerate(hdrs):
    ws.cell(row=r, column=1+i, value=h)
style_header(ws, r, len(hdrs))
r += 1
summary = [
    ("Distinct Orders", distinct_orders, "All records", "DISTINCTCOUNT(Order ID). Not equal to row count."),
    ("Order Items", total_rows, "All records", "Fact rows at order-item grain."),
    ("Eligible Delivery Records", eligible_n, "Delivery Status <> 'Shipping canceled'", "Delivered-items denominator."),
    ("Late Delivery Records", late_n, "Delivery Status = 'Late delivery'", "Numerator for the rate."),
    ("Late Delivery Rate", late_rate, f"Late / Eligible = {late_n}/{eligible_n}", "Primary reliability KPI."),
    ("On-Time Delivery Rate", ontime_rate, f"(Eligible-Late)/Eligible", "Complement of late rate."),
    ("Average Actual Shipping Days", avg_actual, "Eligible items", "Source 'Days for shipping (real)'."),
    ("Average Scheduled Shipping Days", avg_sched, "Eligible items", "Source 'Days for shipment (scheduled)'."),
    ("Average Shipping Delay", avg_delay, "Eligible items", "Actual minus scheduled. Positive = slower."),
    ("Total Sales (USD)", total_sales, "All records", "Sum of source Sales field."),
    ("Total Order Profit (USD)", total_profit, "All records", "Sum of Order Profit (line grain)."),
    ("Order Profit Margin (weighted)", margin, "Profit / Sales", "Weighted; not an average of ratios."),
    ("Sales per Order (USD)", total_sales/distinct_orders, "Sales / distinct orders", "Descriptive ratio."),
]
for name, val, den, note in summary:
    ws.cell(row=r, column=1, value=name)
    c = ws.cell(row=r, column=2, value=val)
    if "Rate" in name or "Margin" in name:
        c.number_format = "0.00%" if "Rate" in name or "Margin" in name else "0.00"
    elif "Days" in name or "Delay" in name:
        c.number_format = "0.00"
    elif "USD" in name or "Sales" in name or "Profit" in name:
        c.number_format = "$#,##0.00" if abs(val) < 100000 else "$#,##0"
    else:
        c.number_format = "#,##0"
    ws.cell(row=r, column=3, value=den)
    ws.cell(row=r, column=4, value=note).alignment = Alignment(wrap_text=True)
    r += 1
ws.column_dimensions["A"].width = 34
ws.column_dimensions["B"].width = 18
ws.column_dimensions["C"].width = 40
ws.column_dimensions["D"].width = 52
ws.freeze_panes = "A4"

# remove empty default? keep
wb.save(OUT)
print("Saved", OUT)
