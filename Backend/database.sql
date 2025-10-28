DROP DATABASE IF EXISTS web_based_pos;
CREATE DATABASE web_based_pos;
USE web_based_pos;

-- User table
CREATE TABLE user (
    email VARCHAR(100) NOT NULL,
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

-- add security question and answer to user table
ALTER TABLE user
ADD COLUMN security_question VARCHAR(250) not Null;
ALTER TABLE user
ADD COLUMN security_answer VARCHAR(250) not Null;
