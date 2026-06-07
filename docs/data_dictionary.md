# Data Dictionary

## Customers

| Column        | Type    |
| ------------- | ------- |
| customer_id   | INT     |
| customer_name | VARCHAR |
| gender        | VARCHAR |
| city          | VARCHAR |
| state         | VARCHAR |

## Products

| Column       | Type    |
| ------------ | ------- |
| product_id   | INT     |
| product_name | VARCHAR |
| category     | VARCHAR |
| brand        | VARCHAR |
| price        | DECIMAL |

## Stores

| Column     | Type    |
| ---------- | ------- |
| store_id   | INT     |
| store_name | VARCHAR |
| city       | VARCHAR |
| state      | VARCHAR |

## Orders

| Column      | Type    |
| ----------- | ------- |
| order_id    | INT     |
| order_date  | DATE    |
| customer_id | INT     |
| product_id  | INT     |
| store_id    | INT     |
| quantity    | INT     |
| unit_price  | DECIMAL |
