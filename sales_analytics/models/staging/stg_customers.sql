SELECT
    customer_id,
    customer_name,
    email,
    region,
    CAST(signup_date AS DATE) AS signup_date
FROM {{ source('dbt_project', 'raw_customers') }}