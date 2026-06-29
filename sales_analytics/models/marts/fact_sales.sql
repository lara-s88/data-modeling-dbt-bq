SELECT
    s.order_id,
    s.customer_id,
    s.product_id,
    s.order_date,
    s.quantity,
    s.amount,
    s.payment_method,
    s.amount AS revenue,
    ROUND(s.amount - p.cost_price, 2) AS profit
FROM {{ ref('stg_sales') }} s
LEFT JOIN {{ ref('stg_products') }} p
    ON s.product_id = p.product_id