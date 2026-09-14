-- Customer analytics views

-- RFM customer analysis
-- Customer segmentation features:
-- Recency
-- Frequency
-- Monetary value

SELECT
    customer_id,
    MAX(order_purchase_timestamp) AS last_purchase,
    COUNT(order_id) AS total_orders,
    SUM(payment_value) AS monetary_value
FROM orders
GROUP BY customer_id;