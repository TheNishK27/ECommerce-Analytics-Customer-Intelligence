# E-Commerce Analytics & Customer Intelligence
## Key Business Insights

This document summarizes the main business findings from the Power BI dashboard built from the e-commerce analytics project.

---

## 1. Customer Retention Is the Biggest Opportunity

The customer segmentation analysis shows that **54.43% of customers are Recent One-Time customers**, while **40.21% are Lost / Dormant**. Only **2.97% are Loyal / Repeat** customers.

### Business interpretation
The customer base is heavily concentrated in one-time and inactive purchasing behavior. This suggests that improving repeat-purchase behavior is a major opportunity.

### Recommendation
Focus on customer retention strategies such as personalized recommendations, targeted follow-up campaigns, and re-engagement programs.

---

## 2. High-Value One-Time Customers Are an Important Opportunity

The High-Value One-Time cluster has an average monetary value of approximately **R$1,133**, compared with approximately **R$244 for Loyal / Repeat**, **R$114 for Lost / Dormant**, and **R$113 for Recent One-Time** customers.

### Business interpretation
A relatively small customer group generates substantially higher individual monetary value but has not developed repeat purchasing behavior.

### Recommendation
Prioritize this group for personalized re-engagement and VIP-style retention campaigns.

---

## 3. Health & Beauty Is the Leading Revenue Category

The Revenue by Product Category analysis places **Health & Beauty** as the highest revenue-generating category, followed by **Watches & Gifts**, **Bed, Bath & Table**, **Sports & Leisure**, and **Computers & Accessories**.

### Business interpretation
A relatively small set of categories contributes strongly to marketplace revenue.

### Recommendation
Use category-level performance when planning inventory, seller acquisition, promotions, and merchandising strategies.

---

## 4. Revenue Grew Significantly Over the Observed Period

The monthly revenue trend shows substantial growth from the early period of the dataset, reaching approximately **R$1 million or more per month during much of 2018**.

### Business interpretation
The marketplace experienced significant expansion in transaction activity and revenue over the observed period.

### Recommendation
Monitor whether future growth is sustained and investigate the drivers behind periods of acceleration or slowdown.

---

## 5. Delivery Performance Is Strong, but Late Orders Still Matter

The delivery analysis shows:

- **96K delivered orders**
- **12.56 average delivery days**
- **91.89% on-time delivery**
- **8.11% late delivery**

### Business interpretation
Most orders arrive on time, but approximately one out of every twelve delivered orders is late.

### Recommendation
Analyze late deliveries by seller, geography, category, and time period to identify operational bottlenecks.

---

## 6. Delivery Times Have a Long Right Tail

The Delivery Time Distribution shows that a large share of orders is concentrated in the lower delivery-time bins, while a smaller number of orders take substantially longer.

### Business interpretation
The average delivery time of 12.56 days does not fully describe the distribution. A small number of very long deliveries creates a long tail.

### Recommendation
Complement average delivery time with median and percentile metrics such as P75, P90, and P95.

---

## 7. Customer Reviews Are Concentrated at High Ratings

The review-score distribution shows a strong concentration of reviews at **5 stars**, followed by 4-star reviews. Lower scores occur much less frequently.

### Business interpretation
Overall customer feedback appears positive.

### Recommendation
Perform a separate analysis of 1- and 2-star reviews to identify recurring problems involving delivery, product quality, or seller performance.

---

## 8. Customer Behavior Is Highly Differentiated

The RFM analysis identifies four customer clusters:

- **Recent One-Time**
- **Lost / Dormant**
- **Loyal / Repeat**
- **High-Value One-Time**

The clusters differ substantially in recency and monetary value.

### Business interpretation
Customers should not be treated as a single homogeneous population. Different groups require different engagement strategies.

### Recommendation
Use RFM-based segmentation to personalize customer retention and marketing strategies.

---

## 9. Revenue and Seller/Product Performance Is Concentrated

The Top Products by Revenue and Top Sellers by Revenue analyses show that some products and sellers generate substantially more revenue than others.

### Business interpretation
Marketplace performance is influenced by a relatively smaller group of high-performing products and sellers.

### Recommendation
Monitor seller and product concentration and assess dependency on top contributors.

---

## 10. The Revenue Forecasting Model Has a Clear Limitation

The forecasting analysis uses a chronological holdout period to compare actual and predicted revenue. The model captured the historical upward trend but **overpredicted the later holdout months**, while actual revenue declined.

### Business interpretation
The simple trend-plus-seasonality model did not adapt well when the later revenue pattern changed.

### Recommendation
Improve the forecasting approach using richer time-series features, lag and rolling variables, or alternative forecasting models such as SARIMA, Prophet, or gradient-boosting approaches.

---

# Top 5 Interview Talking Points

If asked to summarize the project quickly, focus on these five findings:

1. **Retention:** 54.43% of customers are Recent One-Time and 40.21% are Lost / Dormant, while only 2.97% are Loyal / Repeat.
2. **High-value customers:** High-Value One-Time customers average approximately R$1,133 in monetary value.
3. **Category performance:** Health & Beauty is the leading revenue category.
4. **Delivery:** 91.89% of delivered orders are on time, with 8.11% late.
5. **Forecasting:** The trend-seasonality model overpredicted the later holdout period, showing the need for a more adaptive forecasting model.

---

## Important Analytical Notes

- Revenue represents transaction-level sales/revenue available in the dataset; the dataset does not contain an explicit cost-price field, so this analysis does **not** claim true profit.
- The forecasting chart represents **holdout validation**, not an unrestricted future forecast.
- Customer clustering is based on RFM features and K-Means clustering.
- Recommendations above are business interpretations of the dashboard findings, not direct measurements from the dataset.
