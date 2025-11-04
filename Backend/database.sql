DROP DATABASE IF EXISTS web_based_pos;
CREATE DATABASE web_based_pos;
USE web_based_pos;

-- User table
CREATE TABLE user (
    email VARCHAR(100) NOT NULL,
    customer_id INT,
    password_hash VARCHAR(250) NOT NULL,
    user_type ENUM('Employee', 'Admin', 'Customer') NOT NULL,
    PRIMARY KEY (email)
);

-- Inventory Item table
CREATE TABLE inventory_item (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL,
    category VARCHAR(50) NOT NULL
);

-- Customer table
CREATE TABLE customer (
    email VARCHAR(100) NOT NULL,
    points INT DEFAULT 0,
    PRIMARY KEY (email),
    FOREIGN KEY (email) REFERENCES user(email)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE receipt (
    receipt_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_email VARCHAR(100),
    total_amount DECIMAL(10,2) DEFAULT 0,
    amount_due DECIMAL(10,2) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_email) REFERENCES customer(email)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE receipt_item (
    item_line_id INT AUTO_INCREMENT PRIMARY KEY,
    receipt_id INT,
    item_id INT,
    quantity INT NOT NULL DEFAULT 1,
    item_price DECIMAL(10,2) NOT NULL,
    item_tax DECIMAL(4,2) DEFAULT 0,
    FOREIGN KEY (receipt_id) REFERENCES receipt(receipt_id)
        ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES inventory_item(item_id)
        ON DELETE CASCADE
);

-- steps to add to receipt

-- create an empyt receipt for example
-- INSERT INTO receipt (customer_email, total_amount, amount_due)
-- VALUES ('customer@example.com', 7.00, 7.00);

-- add items to receipt_item for example
-- INSERT INTO receipt_item (receipt_id, item_id, quantity, item_price)
-- VALUES (1, 1, 2, 1.50), (1, 2, 1, 4.00);


-- add security question and answer to user table
ALTER TABLE user
ADD COLUMN security_question VARCHAR(250) not Null;
ALTER TABLE user
ADD COLUMN security_answer VARCHAR(250) not Null;
ALTER TABLE user
ADD COLUMN admin_code INT;
ALTER TABLE user
ADD COLUMN employee_code INT;
ALTER TABLE receipt
ADD COLUMN note VARCHAR(250);