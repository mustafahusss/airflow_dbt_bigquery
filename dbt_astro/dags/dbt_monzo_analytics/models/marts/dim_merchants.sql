{{
    config(
        materialized='incremental',
        unique_key='merchant_id',
        incremental_strategy='merge'
    )
}}

SELECT
    merchant_id,
    description,
    category,
    transaction_timestamp
FROM (
    SELECT
        merchant_id,
        description,
        category,
        transaction_timestamp,
        ROW_NUMBER() OVER (PARTITION BY merchant_id ORDER BY transaction_timestamp DESC) as rank
    FROM {{ ref('stg_transactions') }}
    
    {% if is_incremental() %}
        WHERE transaction_timestamp > (SELECT MAX(transaction_timestamp) FROM {{ this }})
    {% endif %}
)
WHERE rank = 1
  AND merchant_id != '-1'