-- Sales analytics views

SELECT
    DATE_TRUNC('month', order_purchase_timestamp) AS month,
    SUM(payment_value) AS revenue,
    COUNT(order_id) AS orders
FROM orders
GROUP BY 1
ORDER BY 1;