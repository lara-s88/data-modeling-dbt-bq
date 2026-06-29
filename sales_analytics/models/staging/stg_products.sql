SELECT
    product_id,
    product_name,
    category,
    CAST(cost_price AS FLOAT64) AS cost_price
FROM {{ source('dbt_project', 'raw_products') }}