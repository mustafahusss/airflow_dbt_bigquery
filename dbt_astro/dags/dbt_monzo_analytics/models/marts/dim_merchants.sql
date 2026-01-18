SELECT DISTINCT
    merchant_id,
    description,
    category

FROM {{ ref('stg_transactions') }}