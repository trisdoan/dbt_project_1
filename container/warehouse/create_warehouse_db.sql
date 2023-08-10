CREATE TABLE customers (
    customer_id INTEGER,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    state_code VARCHAR(2),
    datetime_created VARCHAR(100),
    datetime_updated VARCHAR(100),
    datetime_inserted TIMESTAMP not null default CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id VARCHAR(50),
    customer_id INTEGER,
    item_id VARCHAR(50),
    item_name VARCHAR(150),
    delivered_on VARCHAR(50)
);