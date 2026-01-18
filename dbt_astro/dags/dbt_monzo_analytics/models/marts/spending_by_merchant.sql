{{
    config(
        materialized='incremental',
        unique_key=['category', 'merchant_id', 'year', 'month']
    )
}}

SELECT
    category,
    merchant_id,
    MAX(updated) AS updated,
    EXTRACT(YEAR FROM transaction_date) AS year,
    EXTRACT(MONTH FROM transaction_date) AS month,
    SUM(amount) AS total_spent,
    COUNT(*) AS transaction_count,
    AVG(amount) AS avg_transaction_amount
FROM {{ ref('fact_transactions') }}

GROUP BY
    category,
    merchant_id,
    year,
    month