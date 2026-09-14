-- Delivery performance analysis

SELECT
    order_id,
    order_delivered_customer_date -
    order_purchase_timestamp AS delivery_days
FROM orders;