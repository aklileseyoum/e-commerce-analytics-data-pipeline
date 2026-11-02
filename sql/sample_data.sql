
INSERT INTO customers (name, email) VALUES
    ('Amina', 'amina@example.com'),
    ('Brian', 'brian@example.com'),
    ('Chloe', 'chloe@example.com');


INSERT INTO products (prod_name, price, metadata) VALUES
    ('Laptop',   550.00,  '{"color": "black", "size": "large"}'),
    ('Keyboard', 300.00,  '{"color": "pink", "size": "small"}'),
    ('Mouse',    120.00,  '{"speed": "fast"}'),
    ('Pen',      7.80, NULL);


INSERT INTO orders (customer_id, order_date) VALUES
    (1, '2026-10-28'),
    (1, '2026-10-30'),
    (2, '2026-10-29');


INSERT INTO order_items (product_id, order_id, quantity, unit_price) VALUES
    (1, 1, 2, 5.50),
    (1, 3, 2, 1.20),
    (2, 2, 1, 3.00),
    (3, 2, 1, 7.80),
    (3, 3, 2, 1.20);