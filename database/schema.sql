CREATE DATABASE IF NOT EXISTS sanchay;

USE sanchay;

CREATE TABLE dim_payment_category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE dim_payment_mode (
    mode_id INT AUTO_INCREMENT PRIMARY KEY,
    mode_name VARCHAR(10) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE dim_bill_category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE dim_bill_payment_mode (
    mode_id INT AUTO_INCREMENT PRIMARY KEY,
    mode_name VARCHAR(10) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE fact_income (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    payment_date DATE NOT NULL,
    payment_category_id INT NOT NULL,
    payment_payee_name VARCHAR(100),
    payment_amt DECIMAL(12,2) NOT NULL,
    payment_mode_id INT NOT NULL,
    payment_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_income_category
        FOREIGN KEY (payment_category_id)
        REFERENCES dim_payment_category(category_id),

    CONSTRAINT fk_income_payment_mode
        FOREIGN KEY (payment_mode_id)
        REFERENCES dim_payment_mode(mode_id)
);

CREATE TABLE fact_spending (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    bill_date DATE NOT NULL,
    bill_category_id INT NOT NULL,
    bill_issuer_name VARCHAR(150),
    bill_amount DECIMAL(12,2) NOT NULL,
    bill_reference VARCHAR(100),
    bill_payment_mode_id INT NOT NULL,
    bill_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_bill_category
        FOREIGN KEY (bill_category_id)
        REFERENCES dim_bill_category(category_id),

    CONSTRAINT fk_bill_payment_mode
        FOREIGN KEY (bill_payment_mode_id)
        REFERENCES dim_bill_payment_mode(mode_id)
);