

-- 1. Foodtrucks
CREATE TABLE foodtrucks (
    foodtruck_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cuisine_type VARCHAR(50),
    city VARCHAR(50)
);

-- 2. Products 
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    foodtruck_id INT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2),
    stock INT,
    FOREIGN KEY (foodtruck_id) REFERENCES foodtrucks(foodtruck_id)
);

-- 3. Orders
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    foodtruck_id INT,
    order_date DATETIME,
    status VARCHAR(20),
    total DECIMAL(10,2),
    FOREIGN KEY (foodtruck_id) REFERENCES foodtrucks(foodtruck_id)
);

-- 4. Locations
CREATE TABLE locations (
    location_id INT PRIMARY KEY,
    foodtruck_id INT,
    location_date DATE,
    zone VARCHAR(50),
    FOREIGN KEY (foodtruck_id) REFERENCES foodtrucks(foodtruck_id)
);

-- 5. Order_items
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

select * from order_items;

INSERT INTO order_items (order_item_id, order_id, product_id, quantity) 
VALUES (1, 1001, 101, 1);

-- Verificar EXACTAMENTE qué hay en orders
SELECT * FROM orders WHERE order_id = 1001;

DELETE FROM orders;
INSERT INTO orders (order_id, foodtruck_id, order_date, status, total) VALUES 
(1001, 1, '2023-09-01', 'entregado', 90),
(1002, 2, '2023-09-01', 'pendiente', 100);

-- Forzar commit de la transacción
COMMIT;

-- Verificar que realmente existe
SELECT * FROM orders WHERE order_id = 1001;

-- Intentar la inserción de nuevo
INSERT INTO order_items_2 (order_item_id, order_id, product_id, quantity) 
VALUES (1, 1001, 101, 1);

CREATE TABLE order_items_2 (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT, 
    quantity INT
    -- Sin foreign keys por ahora
);

select * from order_items_2;