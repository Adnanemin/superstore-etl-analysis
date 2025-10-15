PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

--Creating "customers" Table
CREATE TABLE customers(
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    segment TEXT,
    country TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    region TEXT
);

--Creating "products" Table
CREATE TABLE products(
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    sub_category TEXT
);

--Creating "orders" Table
CREATE TABLE orders(
    order_id TEXT PRIMARY KEY,
    order_date TEXT NOT NULL, --ISO 8601 'YYYY-MM-DD'
    ship_date TEXT,
    ship_mode TEXT, 
    customer_id TEXT NOT NULL,
    CHECK (date(order_date) IS NOT NULL),
    CHECK (ship_date IS NULL OR date(ship_date) IS NOT NULL),
    CHECK (ship_date IS NULL OR date(ship_date) >= date(order_date)),
    CHECK(ship_mode IN ('Standard Class', 'First Class', 'Second Class', 'Same Day')),
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

--Creating "order_items" Table
CREATE TABLE order_items(
    row_id INTEGER PRIMARY KEY,
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    sales REAL NOT NULL,
    quantity INTEGER NOT NULL,
    discount REAL NOT NULL,
    profit REAL NOT NULL,
    CHECK (sales >= 0),
    FOREIGN KEY(order_id) REFERENCES orders(order_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(product_id) REFERENCES products(product_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CHECK (quantity > 0),
    CHECK (discount BETWEEN 0.0 AND 1.0)
);

--Indexes for common usable JOIN CLAUSES and FILTERS
CREATE INDEX IF NOT EXISTS idx_orders_order_date      ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_customer_id     ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_customers_region       ON customers(region);
CREATE INDEX IF NOT EXISTS idx_products_category_sub  ON products(category, sub_category);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id   ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_order_items_profit     ON order_items(profit);
CREATE INDEX IF NOT EXISTS idx_order_items_discount   ON order_items(discount);