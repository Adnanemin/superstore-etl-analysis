PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- Customers
CREATE TABLE customers (
    customer_id   TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    segment       TEXT NOT NULL,
    country       TEXT NOT NULL,
    city          TEXT NOT NULL,
    state         TEXT NOT NULL,
    postal_code   TEXT NOT NULL,
    region        TEXT NOT NULL
);

-- Products
CREATE TABLE products (
    product_id   TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category     TEXT NOT NULL,
    sub_category TEXT NOT NULL
);

-- Orders
CREATE TABLE orders (
    order_id    TEXT PRIMARY KEY,
    order_date  TEXT NOT NULL, -- ISO 8601 'YYYY-MM-DD'
    ship_date   TEXT,
    ship_mode   TEXT NOT NULL,
    customer_id TEXT NOT NULL,

    CHECK (date(order_date) IS NOT NULL),
    CHECK (ship_date IS NULL OR date(ship_date) IS NOT NULL),
    CHECK (ship_date IS NULL OR date(ship_date) >= date(order_date)),
    CHECK (ship_mode IN ('Standard Class','First Class','Second Class','Same Day')),

    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Order items
CREATE TABLE order_items (
    row_id     INTEGER PRIMARY KEY,
    order_id   TEXT NOT NULL,
    product_id TEXT NOT NULL,
    sales      REAL NOT NULL,
    quantity   INTEGER NOT NULL,
    discount   REAL NOT NULL,
    profit     REAL NOT NULL,

    CHECK (sales >= 0),
    CHECK (quantity > 0),
    CHECK (discount BETWEEN 0.0 AND 1.0),

    FOREIGN KEY(order_id)  REFERENCES orders(order_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(product_id) REFERENCES products(product_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Indexes (practical set)
CREATE INDEX IF NOT EXISTS idx_orders_order_date      ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_customer_id     ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_customers_region       ON customers(region);
CREATE INDEX IF NOT EXISTS idx_products_category_sub  ON products(category, sub_category);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id   ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);