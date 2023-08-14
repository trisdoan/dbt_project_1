-- create a commerce schema
CREATE SCHEMA warehouse;

-- Use commerce schema
SET
    search_path TO warehouse;

CREATE TABLE customers (
    customer_id INTEGER,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    state_code VARCHAR(2),
    datetime_created VARCHAR(100),
    datetime_updated VARCHAR(100)
);

CREATE TABLE orders (
    order_id VARCHAR(50),
    customer_id INTEGER,
    item_id VARCHAR(50),
    item_name VARCHAR(150),
    delivered_on VARCHAR(50),
    order_status VARCHAR(15)
);

CREATE TABLE state (
    state_identifier VARCHAR(10),
    state_code VARCHAR(5000),
    state_name VARCHAR(5000)
);
COPY warehouse.state(state_identifier, state_code, state_name)
FROM '/input_data/state.csv' DELIMITER ',' CSV HEADER;