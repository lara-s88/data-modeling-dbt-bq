SELECT
    order_id,
    customer_id,
    product_id,
    CAST(order_date AS DATE) AS order_date,
    CAST(quantity AS INT64) AS quantity,
    CAST(amount AS FLOAT64) AS amount,
    payment_method
FROM {{ source('dbt_project', 'raw_sales') }}