{{
    config(
        materialized='incremental'
    )
}}


select
    amount / 100.0 AS amount,
    created,
    updated,
    settled,
    PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%E*SZ', created) AS transaction_timestamp,
    DATE(PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%E*SZ', created)) AS transaction_date,
    TIME(PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%E*SZ', created)) AS transaction_time,
    id,
    category,
    description,
    COALESCE(merchant,'-1') as merchant_id,
    notes,
    decline_reason,
    currency

from {{ source('monzo_data', 'raw_transactions') }}


{% if is_incremental() %}

    where created > (select max(created) from {{ this }} )

{% endif %}