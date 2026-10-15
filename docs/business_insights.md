# Business insights

All figures below come from the validated DataCo dataset (180,519 order-item rows; 172,765 eligible delivery records).  
Eligible records exclude `Delivery Status = 'Shipping canceled'` (7,754 rows).

## Finding 1 - Roughly six in ten eligible items are delivered late

- Metric: Late Delivery Rate
- Value: 57.29% (98,977 of 172,765)
- Baseline: On-time delivery 42.71% (73,788 items: 41,592 advance + 32,196 on time)
- Evidence: `Late_delivery_risk` exactly matches "Late delivery" status across all rows.
- Interpretation: Late delivery is the modal outcome in this dataset, not an exception. Anyone tracking a 90% on-time target would find a large gap to close.
- Next step: Break the 57.29% down by shipping mode before assigning accountability (see Finding 2).
- Limitation: "Late" means "later than the scheduled window"; it does not imply the customer missed a hard appointment.

## Finding 2 - First Class posts a 100% late rate because its service level is one day

- Metric: Late Delivery Rate by Shipping Mode
- Values:
  - First Class: 100.00% (26,513 / 26,513), scheduled 1 day, actual 2 days, avg delay +1.0
  - Second Class: 79.83% (26,987 / 33,806), scheduled 2 days, actual ~3.99 days
  - Same Day: 47.93% (4,454 / 9,293), scheduled 0 days, actual ~0.48 days
  - Standard Class: 39.77% (41,023 / 103,153), scheduled 4 days, actual ~3.99 days, avg delay -0.01
- Comparison: Standard Class has the best late rate and the largest volume (103,153 eligible items).
- Interpretation: Much of the "lateness" is a function of how aggressive the scheduled window is, not of slower physical transit. First Class is fastest in absolute days (2) but always misses a 1-day promise. Standard Class meets/exceeds a 4-day promise.
- Next step: Compare transit times within each mode, and recalibrate First Class/Second Class service promises rather than assuming warehouse or carrier failure.
- Limitation: Mode is a business-decision field in this data, not a measured transit process; no causal claim can be made about why a mode is slow.

## Finding 3 - Markets and regions are surprisingly even; mode usage explains most of the spread

- Metric: Late Delivery Rate by Market and Order Region
- Markets: Africa 56.84%, Europe 57.69%, LATAM 56.87%, Pacific Asia 57.38%, USCA 57.41% (all within about one point).
- Regions (n >= 500): Canada lowest at 51.60% (n=907); Central Africa highest at 60.15% (n=1,616); all 23 regions fall between 51.6% and 60.2%.
- Evidence: shipping-mode mix is nearly identical across high- and low-late regions (e.g. Standard Class ~59-60% of eligible items).
- Interpretation: Geography adds less signal than the service-level design. Network-wide actions (mode policy, promise windows) would help more than region-specific fixes.
- Next step: Investigate the low-volume Canada lane and a handful of niche categories if region-specific action is still wanted.
- Limitation: regional differences are statistically small; do not build region-specific SLAs on n < few-hundred subsets.

## Finding 4 - Late-delivery performance is stable across the 37 months covered

- Metric: Late Delivery Rate by Year-Month
- Values: monthly late rate stays between about 55.8% and 58.7% across 2015-01 to 2018-01 (e.g. 56.3% in 2015-01, 58.7% in 2018-01).
- Seasonal pattern: by calendar month, rates range 56.7% (April, July) to 58.0% (August), a spread of roughly 1.3 points - effectively flat.
- Volume: about 5,000 order items per month through 2017-09, then about 2,000 per month from 2017-10 to 2018-01.
- Interpretation: this is a structural (policy) problem, not a peak-season problem. There is no obvious seasonal spike to plan around.
- Next step: Focus improvement programmes on process/marketing rather than capacity surge plans.
- Limitation: the late-2017 drop in volume may reflect partial data coverage rather than a business event; trends should be verified before acting.

## Finding 5 - Product categories vary in late rate and profitability, mostly independently

- Metric: Late rate, sales and margin by category
- Sales concentration: Fishing 6.64M, Cleats 4.24M, Camping & Hiking 3.95M, Cardio Equipment 3.53M (USD).
- Late-rate range by category (n >= 300): 52.71% (Computers) to 62.61% (Lacrosse); 47 of 50 categories sit between 55% and 61%.
- Profit margin range (categories with >= 100k USD sales): 8.95% (Health and Beauty) to 13.62% (Women's Clothing); dataset-wide weighted margin 10.78%.
- Customer segments: Consumer 57.31% late, 10.86% margin; Corporate 57.08%, 10.81%; Home Office 57.59%, 10.67% - segments are effectively identical on reliability.
- Interpretation: category/segment identity is a weaker performance signal than shipping-mode choice in this data.
- Next step: prioritise high-sales categories and worst-margin categories (Health and Beauty, Shop by Sport) for promotional/cost review; keep reliability work separate.
- Limitation: late rate and profit margin are reported on the same items but no causal direction is claimed (correlation only).

## Finding 6 - Financial totals (for KPI context)

- Total sales: 36,784,735 USD.
- Total order profit: 3,966,903 USD.
- Weighted order-profit margin: 10.78%.
- Sales per order: 559.45 USD (65,752 distinct orders).
- Profit margin by mode: First Class 11.40%, Standard 10.78%, Second 10.54%, Same Day 10.47% - minor; despite the higher late rate of Second Class and First Class, margin does not collapse.

## Suggested four follow-up investigations (not findings)

1. Effective transit days within each shipping mode (to separate carrier delay from promise design).
2. The 7,754 'Shipping canceled' records - customer/order status reasons and revenue at risk.
3. Categories/departments below 10% margin; whether discounting or freight accruals explain the gap.
4. Customer-experience cost of 'Advance shipping' (receiving 41,592 items earlier than promised).
