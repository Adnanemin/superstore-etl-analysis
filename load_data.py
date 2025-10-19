#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mini Superstore ETL (CSV -> SQLite)
- pandas + sqlite3 only
- Robust CSV read, cleaning, normalized loads into: customers, products, orders, order_items
"""

import sqlite3
import pandas as pd

# --------------------------- CONFIG ---------------------------
DB_PATH = "superstore.db"
CSV_PATH = "data/superstore.csv"

VALID_SHIP_MODES = {"Standard Class", "First Class", "Second Class", "Same Day"}
TEXT_COLS = [
    "ship_mode", "customer_id", "customer_name", "segment", "country", "city",
    "state", "postal_code", "region", "product_id", "category", "sub_category", "product_name"
]
NUMERIC_COLS = ["quantity", "discount", "sales", "profit"]
DATE_COLS = ["order_date", "ship_date"]

RESET_DB = True

# ------------------------ HELPERS -----------------------------
def get_connection(db_path: str) -> sqlite3.Connection:
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA foreign_keys = ON;")
    return con

def read_csv_robust(path: str) -> pd.DataFrame:
    """Auto-detect delimiter; tolerate quoted commas."""
    return pd.read_csv(
        path,
        engine="python",
        sep=None,  # autodetect comma/semicolon/tab
        dtype={
            "Row ID": "Int64",
            "Order ID": "string",
            "Ship Mode": "string",
            "Customer ID": "string",
            "Customer Name": "string",
            "Segment": "string",
            "Country": "string",
            "City": "string",
            "State": "string",
            "Postal Code": "string",
            "Region": "string",
            "Product ID": "string",
            "Category": "string",
            "Sub-Category": "string",
            "Product Name": "string",
            "Profit": "string",
        },
        quotechar='"',
        escapechar='\\',
    )

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={
        "Row ID": "row_id",
        "Order ID": "order_id",
        "Order Date": "order_date",
        "Ship Date": "ship_date",
        "Ship Mode": "ship_mode",
        "Customer ID": "customer_id",
        "Customer Name": "customer_name",
        "Segment": "segment",
        "Country": "country",
        "City": "city",
        "State": "state",
        "Postal Code": "postal_code",
        "Region": "region",
        "Product ID": "product_id",
        "Category": "category",
        "Sub-Category": "sub_category",
        "Product Name": "product_name",
        "Sales": "sales",
        "Quantity": "quantity",
        "Discount": "discount",
        "Profit": "profit",
    })

def clean_text(df: pd.DataFrame) -> None:
    for c in [col for col in TEXT_COLS if col in df.columns]:
        df[c] = df[c].astype("string").str.strip()

def parse_dates(df: pd.DataFrame) -> None:
    for col in ["order_date", "ship_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce", format="%m/%d/%Y")
    sd, od = df["ship_date"], df["order_date"]
    df["ship_date"] = sd.where(sd.isna() | (sd >= od), od)

def normalize_numeric(df: pd.DataFrame) -> None:
    for col in [c for c in NUMERIC_COLS if c in df.columns]:
        df[col] = (
            df[col].astype("string")
            .str.strip()
            .str.replace("\u00a0", "", regex=False)  # non-breaking space
            .str.replace("%", "", regex=False)       # ignore '%'
            .str.replace(".", "", regex=False)       # thousands separator
            .str.replace(",", ".", regex=False)      # decimal comma -> dot
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

def apply_business_rules(df: pd.DataFrame) -> pd.DataFrame:
    # ship_mode normalization
    if "ship_mode" in df.columns:
        df["ship_mode"] = df["ship_mode"].where(df["ship_mode"].isin(VALID_SHIP_MODES), "Standard Class")
    # numeric guards
    df = df[df["quantity"].fillna(0) > 0]
    df = df[(df["discount"].fillna(-1) >= 0) & (df["discount"] <= 1)]
    df = df[df["sales"].fillna(-1) >= 0]
    # required keys
    df = df.dropna(subset=["order_id", "product_id", "customer_id", "order_date"])
    # convert datetimes to ISO; preserve NULLs for ship_date
    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
    ship_date_str = df["ship_date"].dt.strftime("%Y-%m-%d")
    df["ship_date"] = ship_date_str.mask(df["ship_date"].isna(), None)
    return df

def ensure_row_id(df: pd.DataFrame) -> None:
    if "row_id" not in df.columns or df["row_id"].isna().any() or df["row_id"].duplicated().any():
        df["row_id"] = pd.RangeIndex(1, len(df) + 1)

def to_sql_safe(df: pd.DataFrame, name: str, con: sqlite3.Connection) -> None:
    df.to_sql(name, con, if_exists="append", index=False, chunksize=1000, method=None)

def fk_checks(con: sqlite3.Connection) -> None:
    missing_orders = con.execute("""
        SELECT COUNT(*) FROM order_items oi
        LEFT JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_id IS NULL;
    """).fetchone()[0]
    missing_products = con.execute("""
        SELECT COUNT(*) FROM order_items oi
        LEFT JOIN products p ON oi.product_id = p.product_id
        WHERE p.product_id IS NULL;
    """).fetchone()[0]
    missing_customers = con.execute("""
        SELECT COUNT(*) FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL;
    """).fetchone()[0]
    print("Missing order_id in orders table: ", missing_orders)
    print("Missing product_id in products table: ", missing_products)
    print("Missing customer_id in orders table: ", missing_customers)

def print_counts(con: sqlite3.Connection) -> None:
    for t in ("customers", "products", "orders", "order_items"):
        total = con.execute(f"SELECT COUNT(*) FROM {t};").fetchone()[0]
        dist  = None
        if t == "customers":
            dist = con.execute("SELECT COUNT(DISTINCT customer_id) FROM customers;").fetchone()[0]
        elif t == "products":
            dist = con.execute("SELECT COUNT(DISTINCT product_id) FROM products;").fetchone()[0]
        elif t == "orders":
            dist = con.execute("SELECT COUNT(DISTINCT order_id) FROM orders;").fetchone()[0]
        elif t == "order_items":
            dist = con.execute("SELECT COUNT(DISTINCT row_id) FROM order_items;").fetchone()[0]
        print(f"{t:12s} total={total:,} distinct={dist:,}")

# -------------------------- PIPELINE -------------------------
def main():
    # read
    df = read_csv_robust(CSV_PATH)
    df = rename_columns(df)

    # clean
    clean_text(df)
    parse_dates(df)
    normalize_numeric(df)   # PATCH: profit dahil numeric dönüşüm burada
    df = apply_business_rules(df)

    # küçük bir görünürlük: CSV'de mükerrer row_id var mı?
    dup_row_id = df["row_id"].duplicated().sum() if "row_id" in df.columns else 0
    print("Duplicated row_id in CSV:", int(dup_row_id))

    ensure_row_id(df)

    # dims
    customers = (
        df[["customer_id", "customer_name", "segment", "country", "city", "state", "postal_code", "region"]]
        .drop_duplicates(subset=["customer_id"])
        .reset_index(drop=True)
    )
    products = (
        df[["product_id", "product_name", "category", "sub_category"]]
        .drop_duplicates(subset=["product_id"])
        .reset_index(drop=True)
    )
    orders = (
        df[["order_id", "order_date", "ship_date", "ship_mode", "customer_id"]]
        .drop_duplicates(subset=["order_id"])
        .reset_index(drop=True)
    )
    order_items = df[["row_id", "order_id", "product_id", "sales", "quantity", "discount", "profit"]].copy()

    # load
    with get_connection(DB_PATH) as con:
        if RESET_DB:
            # child -> parent order (FK'lere saygı)
            con.execute("DELETE FROM order_items;")
            con.execute("DELETE FROM orders;")
            con.execute("DELETE FROM products;")
            con.execute("DELETE FROM customers;")
            con.commit()

        to_sql_safe(customers, "customers", con)
        to_sql_safe(products, "products", con)
        to_sql_safe(orders, "orders", con)
        to_sql_safe(order_items, "order_items", con)

        print_counts(con)
        fk_checks(con)

    print("\n>> Data loading completed successfully.")

if __name__ == "__main__":
    main()