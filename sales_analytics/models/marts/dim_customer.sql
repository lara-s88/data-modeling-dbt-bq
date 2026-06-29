SELECT
    customer_id,
    customer_name,
    email,
    region,
    signup_date
FROM {{ ref('stg_customers') }}