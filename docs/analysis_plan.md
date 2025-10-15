# Analysis Plan

This plan outlines how the Sample Superstore dataset will be analyzed to answer five key business questions.  
It defines the analytical approach, key metrics, and data validation steps. The actual SQL queries and Python code will be implemented later based on this roadmap.

---

## 0) Definitions and Assumptions
- **Profit Margin (%)** = Profit / Sales  
- **Month** = extracted from `Order Date` as `YYYY-MM`  
- **Discount Bands** (example thresholds):  
  - `0` → no discount  
  - `(0–0.10]` → low discount  
  - `(0.10–0.30]` → medium discount  
  - `>0.30` → high discount  
- **Record level:** each row represents a single order–product combination (from `order_items`).

---

## 1) Data Quality Checks
Before any analysis, perform quick validation steps:
- **Date consistency:** ensure `Ship Date` ≥ `Order Date`.  
- **Negative or invalid values:** check `Sales`, `Quantity`, `Discount`, `Profit` for anomalies.  
- **Geographic completeness:** confirm that `Country`, `Region`, `State`, `City` are not missing.  
- **Key uniqueness:** check for duplicate `order_id`, `customer_id`, and `product_id`.

> Any data issues will be documented in a short "Data Notes" section.

---

## Question 1 — Which are the top 5 most profitable products?
**Goal:** Identify products that generate the highest total profit.

**Steps**
1. Aggregate **SUM(Profit)** and **SUM(Sales)** by product.  
2. Optionally include `Quantity` or record count for robustness.  
3. Sort by total profit in descending order and select the **top 5**.  
4. Include a short commentary explaining possible reasons (e.g., high demand, premium pricing).

**Note**
- Watch out for one-off transactions that create abnormally high profits (outliers).

---

## Question 2 — How does the profit margin vary by Category and Region?
**Goal:** Understand how profitability differs across product categories and geographic regions.

**Steps**
1. Group by **Category** and **Region**.  
2. Compute `SUM(Sales)` and `SUM(Profit)`.  
3. Calculate **Profit Margin = SUM(Profit) / SUM(Sales)**.  
4. Visualize with a heatmap or pivot-style table showing both margin and volume.

**Note**
- Very low sales volumes may distort margin percentages; apply a minimum sales threshold (e.g., $1,000).

---

## Question 3 — Which customer segment has the highest return rate?
**Case A (if “Returns” sheet is available):**  
- Treat the “Returns” sheet as a separate table (`order_id` as reference).  
- Compute **Return Rate = returned orders / total orders**, grouped by customer segment.

**Case B (if “Returns” is not available):**  
- Use **Loss Rate** (orders with negative profit) as a proxy for returns.  
- Group by `Segment` and compute percentage of loss-making records.

**Steps (for Case B)**
1. Count total and loss-making records per segment.  
2. Calculate **Loss Ratio = (loss orders / total orders)**.  
3. Highlight segments with the highest ratios and suggest potential causes (e.g., discount abuse, product type).

---

## Question 4 — What is the monthly sales trend and is there any seasonality?
**Goal:** Identify sales and profit trends over time and detect seasonal patterns.

**Steps**
1. Extract `YYYY-MM` from `Order Date`.  
2. Aggregate **SUM(Sales)** and **SUM(Profit)** by month.  
3. Optionally apply a **3-month moving average** for smoother visualization.  
4. Identify months with peaks and drops, and suggest possible business reasons (e.g., holiday seasons, campaigns).

**Note**
- Handle incomplete months at dataset start/end carefully when interpreting trends.

---

## Question 5 — How does the discount rate affect profitability?
**Goal:** Examine how different discount levels impact profit and margin.

**Steps**
1. Categorize records into **discount bands** (0, low, medium, high).  
2. For each band, calculate average `Profit`, `Profit Margin`, and total `Sales`.  
3. Compare results visually (bar chart or grouped comparison).  
4. If necessary, further break down by `Category` or `Segment`.

**Note**
- Highlight combinations where high discounts lead to losses.

---

## Reporting Notes
- Provide concise comments for each finding: **why it matters** and **how it can guide decisions**.  
- When applicable, mention **data limitations** (e.g., small samples, missing geographic info).  
- Planned visuals:
  - Monthly trend → line chart  
  - Top 5 products → bar chart  
  - Category x Region → heatmap or pivot table  
  - Discount vs Profit → bar chart

---

## Deliverables (Based on This Plan)
- SQL queries → `sql/answers.sql`  
- EDA notebook → `notebooks/eda.ipynb`  
- Summary report → `reports/mini-report.md`  
- Optional: visual figures → `reports/figures/`

---

✅ This plan ensures that each business question is backed by a structured analytical path, making results easy to replicate, validate, and present.