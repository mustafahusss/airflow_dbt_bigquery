{{
    config(
        materialized='incremental'
    )
}}


SELECT
    amount,
    created,
    transaction_timestamp,
    transaction_date,
    transaction_time,
    id as transaction_id,
    category,
    description,
    merchant_id as merchant_id,
    notes,
    decline_reason,
    updated,
    currency,

  CASE
        WHEN amount < 0 THEN 'IN'
        ELSE 'OUT'
    END AS transaction_type,
    EXTRACT(DAYOFWEEK FROM transaction_date) AS day_of_week

FROM {{ ref('stg_transactions') }}

{% if is_incremental() %}
    where updated > (select max(updated) from {{ this }})
{% endif %}

--Using {{ ref('stg_transactions') }} - This is dbt syntax that creates a dependency. dbt knows to run stg_transactions before fact_transactions