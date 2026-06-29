SELECT
    product_id,
    product_name,
    category,
    cost_price
FROM {{ ref('stg_products') }}