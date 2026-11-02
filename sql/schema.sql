
CREATE TABLE customers (
    id    INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name  TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);


CREATE TABLE orders (
    id           INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(id),
    order_date   DATE NOT NULL
);


CREATE TABLE products (
    id        INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    prod_name TEXT NOT NULL,
    price     NUMERIC(10,2) NOT NULL CHECK(price > 0),
    metadata  JSONB
);


CREATE TABLE order_items (
    product_id INT NOT NULL REFERENCES products(id),
    order_id   INT NOT NULL REFERENCES orders(id),
    quantity   INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price > 0),
    PRIMARY KEY (order_id, product_id)
);