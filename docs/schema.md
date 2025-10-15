# Database Schema Design

This schema is designed based on the **Sample Superstore dataset**.  
The goal is to organize the data into a clean relational structure for better query performance and clearer business insights.

---

## 🧱 customers
Stores customer and regional information.

| Column | Type | Description |
|--------|------|-------------|
| customer_id | TEXT | Unique identifier for each customer |
| customer_name | TEXT | Full name of the customer |
| segment | TEXT | Customer segment (e.g., Consumer, Corporate, Home Office) |
| country | TEXT | Country name |
| city | TEXT | City of the customer |
| state | TEXT | State or province |
| postal_code | TEXT | Postal or ZIP code |
| region | TEXT | Region (e.g., East, West, Central, South) |

**Primary Key:** `customer_id`

---

## 📦 products
Contains product information and its classification.

| Column | Type | Description |
|--------|------|-------------|
| product_id | TEXT | Unique identifier for each product |
| product_name | TEXT | Name of the product |
| category | TEXT | Product category (e.g., Furniture, Office Supplies) |
| sub_category | TEXT | Subdivision of the main category |

**Primary Key:** `product_id`

---

## 📄 orders
Holds order-level data such as dates and shipping mode.

| Column | Type | Description |
|--------|------|-------------|
| order_id | TEXT | Unique identifier for each order |
| order_date | DATE | Date when the order was placed |
| ship_date | DATE | Date when the order was shipped |
| ship_mode | TEXT | Shipping method used (e.g., Second Class, Standard Class) |

**Primary Key:** `order_id`

---

## 💰 order_items
Links each order to the products sold and contains financial metrics.

| Column | Type | Description |
|--------|------|-------------|
| row_id | INTEGER | Unique identifier for each row in the dataset |
| order_id | TEXT | Reference to the corresponding order |
| product_id | TEXT | Reference to the purchased product |
| sales | REAL | Total sales amount |
| quantity | INTEGER | Quantity of the product sold |
| discount | REAL | Discount applied to the sale (0–1 range) |
| profit | REAL | Profit gained from the sale |

**Primary Key:** `row_id`  
**Foreign Keys:**  
- `order_id` → orders(order_id)  
- `product_id` → products(product_id)

---

## 🔗 Relationships Overview

```text
customers ---< orders ---< order_items >--- products