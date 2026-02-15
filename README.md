# 🏪 Mini Superstore Analytics

An end-to-end **retail analytics project** built with **Python and SQL**, based on the popular *Sample Superstore* dataset.  
This repository was created as a **personal learning project** to strengthen data cleaning, relational modeling, and EDA skills.

---

## 🎯 Project Overview
A complete **ETL → SQLite → EDA** workflow:
- Load CSV, clean & normalize with **pandas** (and simple **os** utilities)
- Persist to a relational **SQLite** schema
- Explore business questions and generate figures with **Matplotlib** & **Seaborn**

> ℹ️ **Note about the database file**
> This repo **does not include** `superstore.db` and **does not include** your local `venv/`.  
> Recreate the database locally by running `load_data.py` (instructions below).

---

## 🔍 Business Questions
1. Which are the **top 5 most profitable products**?  
2. How does **profit margin** vary by *Category* and *Region*?  
3. Which **customer segment** records the highest loss/return?  
4. What is the **yearly sales and profit trend**?  
5. How does the **discount rate** affect profitability?  

---

## 🧱 Database Schema
Four tables after normalization:

| Table | Description |
|---|---|
| `customers` | Customer details, location, segment |
| `products`  | Product info (category, sub-category) |
| `orders`    | Order metadata (dates, ship mode, customer) |
| `order_items` | Line-level metrics (quantity, sales, discount, profit) |

📄 Full schema: [`sql/create_tables.sql`](sql/create_tables.sql)

---

## ⚙️ Analytical Workflow
1. **ETL (Python):** read CSV → clean text/date/numeric fields → apply business rules → write to SQLite.  
2. **EDA (Notebook):** join tables into an analysis-ready `superstore` DataFrame → compute KPIs & answer questions.  
3. **Reporting:** export charts to `reports/figures/` for GitHub preview.

---

## 🖼️ Example Visuals
| Chart | Description |
|---|---|
| ![Top 5 Products](reports/figures/top5_products.png) | Top 5 Most Profitable Products |
| ![Category–Region Heatmap](reports/figures/category_region_heatmap.png) | Profit Margin by Category & Region |
| ![Yearly Trend](reports/figures/yearly_sales_profit_trend.png) | Yearly Sales & Profit Trend |
| ![Discount vs Profit](reports/figures/discount_vs_profit.png) | Impact of Discount Rate on Profitability |

---

## 📂 Project Structure
```
mini_superstore_analytics/
├── data/
│   └── superstore.csv
├── sql/
│   └── create_tables.sql
├── notebooks/
│   └── eda.ipynb
├── reports/
│   └── figures/
│       ├── yearly_sales_profit_trend.png
│       ├── top5_products.png
│       ├── category_region_heatmap.png
│       └── discount_vs_profit.png
├── load_data.py
├── requirements.txt
├── README.md
└── analysis_plan.md
```

---

## 🧩 Tools & Libraries
- **Python 3.10+**
- **SQLite 3**
- **pandas**
- **matplotlib**
- **seaborn**
- **os** (filesystem utilities)

---

## 🚀 How to Run (Reproducible Setup)

1) **Create a virtual environment & install deps**
```bash
python3 -m venv venv
source venv/bin/activate              # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2) **Create the SQLite schema**
```bash
sqlite3 superstore.db < sql/create_tables.sql
```

3) **Load data (CSV → SQLite)**
```bash
python load_data.py
```
> This will (re)generate `superstore.db` locally from `data/superstore.csv`.

4) **Open the EDA notebook**
```bash
jupyter notebook notebooks/eda.ipynb
```

---

## 📝 Git Hygiene (Recommended)
Add the following to `.gitignore` to keep the repo clean and small:
```
venv/
__pycache__/
*.sqlite
*.db
.DS_Store
```
> *We intentionally do **not** commit `venv/` and `superstore.db`.*

---

## 📊 Results (Summary of Insights)
### Top 5 Most Profitable Products
- The **most profitable products** are mainly high-value **copiers and electronics** (e.g., Canon and HP copiers).  
- These products generate significantly higher profits than the rest of the catalog.

---

### Yearly Sales and Profit Trend
- Both **sales** and **profits** show a clear **upward trend** over the years (2015–2017).  
- This suggests steady business growth and improving profitability over time.

---

### Discount vs Profit
- There’s a clear **negative relationship** between discount rate and profit.  
- Higher discounts often lead to **losses**, showing the importance of controlling discount policies.

---
---

## 📊 Overall Summary
The analysis highlights that:

- **Technology** and **Office Supplies** categories are the main profit drivers.  
- **High discounts** reduce profitability significantly.  
- **West** and **East** regions are the most profitable markets.  
- Profitability has **grown steadily over time**, indicating healthy business performance.

---

## 👤 Author
**Adnan Emin Nalçacı**  
📧 [adnanemin39@gmail.com](mailto:adnanemin39@gmail.com)  
🌐 [github.com/Adnanemin](https://github.com/Adnanemin)

---

## 🪪 License
This project is open-source under the **MIT License**.

---

### ✅ Notes
- This repository is for **educational and skill development** purposes.
- The Sample Superstore data is public/anonymized.
- Figures in `/reports/figures` are generated by the notebook.
