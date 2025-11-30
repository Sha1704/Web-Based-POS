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
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(category_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
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
    customer_email VARCHAR(100) NULL,
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

-- Transaction table
CREATE TABLE transaction (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_email VARCHAR(100),
    total DECIMAL(6,2) NOT NULL,
    tip_amount DECIMAL(5,2) DEFAULT 0,
    status ENUM('Active', 'Completed', 'Voided') DEFAULT 'Active',
    FOREIGN KEY (customer_email) REFERENCES customer(email)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Payment Method table (cash, card)
CREATE TABLE payment_method (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NULL,
    payment_type VARCHAR (30) NOT NULL, 
    amount DECIMAL (5,2) NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transaction(transaction_id)
);

-- category table
CREATE TABLE category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) UNIQUE NOT NULL
);

ALTER TABLE user
ADD COLUMN admin_code INT;
ALTER TABLE user
ADD COLUMN employee_code INT;
ALTER TABLE receipt
ADD COLUMN note VARCHAR(250);
ALTER TABLE inventory_item
ADD COLUMN tax_rate DECIMAL(10,2) DEFAULT 0.00;

-- add receipt_id to payment_method and link it to receipt
ALTER TABLE payment_method
ADD COLUMN receipt_id INT,
ADD FOREIGN KEY (receipt_id) REFERENCES receipt(receipt_id)
    ON DELETE CASCADE;

-- add receipt_id to transaction and link it to receipt as well
ALTER TABLE transaction
ADD COLUMN receipt_id INT,
ADD FOREIGN KEY (receipt_id) REFERENCES receipt(receipt_id)
    ON DELETE CASCADE;

-- Ratings table
-- (unique key to prevent duplicate ratings per customer per item)
CREATE TABLE item_rating(
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_email VARCHAR(100) NOT NULL,
    item_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review VARCHAR(250),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_email) REFERENCES customer(email)
        ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES inventory_item(item_id)
        ON DELETE CASCADE,
    UNIQUE KEY unique_rating (customer_email, item_id)
);

ALTER TABLE inventory_item
ADD COLUMN avg_rating DECIMAL(3,2) DEFAULT 0.0;