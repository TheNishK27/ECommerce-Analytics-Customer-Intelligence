import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# 2. POSTGRESQL CONNECTION
# ============================================================

connection_string = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(connection_string)

print("Connected to PostgreSQL!")


# ============================================================
# 3. LOAD MONTHLY SALES DATA
# ============================================================

monthly_sales = pd.read_sql(
    "SELECT * FROM analytics.v_monthly_sales",
    engine
)

# Convert month_year to datetime
monthly_sales["month_year"] = pd.to_datetime(
    monthly_sales["month_year"]
)

# Sort chronologically
monthly_sales = monthly_sales.sort_values(
    "month_year"
)


# ============================================================
# 4. CALCULATE MONTH-OVER-MONTH REVENUE GROWTH
# ============================================================

monthly_sales["previous_month_revenue"] = (
    monthly_sales["product_revenue"].shift(1)
)

monthly_sales["mom_growth_pct"] = (
    (
        monthly_sales["product_revenue"]
        - monthly_sales["previous_month_revenue"]
    )
    / monthly_sales["previous_month_revenue"]
) * 100


# ============================================================
# 5. DISPLAY MONTH-OVER-MONTH GROWTH
# ============================================================

print("\nMonth-over-Month Growth:")

print(
    monthly_sales[
        [
            "month_year",
            "product_revenue",
            "mom_growth_pct"
        ]
    ].head(15)
)


# ============================================================
# 6. CLEAN MOM DATA FOR ANALYSIS
# ============================================================

# Remove the first month because it has no previous month
growth_data = monthly_sales.dropna(
    subset=["mom_growth_pct"]
).copy()

# Ignore the very early months where revenue is extremely small
# This prevents unstable percentage growth from dominating the chart
growth_data = growth_data[
    growth_data["month_year"] >= "2017-02-01"
]


# ============================================================
# 7. FIND STRONGEST AND WEAKEST GROWTH MONTHS
# ============================================================

best_month = growth_data.loc[
    growth_data["mom_growth_pct"].idxmax()
]

worst_month = growth_data.loc[
    growth_data["mom_growth_pct"].idxmin()
]


print("\nStrongest Revenue Growth:")

print(
    best_month[
        [
            "month_year",
            "mom_growth_pct"
        ]
    ]
)


print("\nWeakest Revenue Growth:")

print(
    worst_month[
        [
            "month_year",
            "mom_growth_pct"
        ]
    ]
)


# ============================================================
# 8. DISPLAY MONTHLY SALES SUMMARY
# ============================================================

print("\nMonthly Sales:")

print(
    monthly_sales.head(10)
)


# ============================================================
# 9. REVENUE STATISTICS
# ============================================================

print("\nRevenue Statistics:")

print(
    monthly_sales["product_revenue"].describe()
)


# ============================================================
# 10. VISUALIZATION — MONTHLY REVENUE TREND
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["month_year"],
    monthly_sales["product_revenue"],
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ============================================================
# 11. VISUALIZATION — MONTH-OVER-MONTH GROWTH
# ============================================================

plt.figure(figsize=(12, 6))

plt.bar(
    growth_data["month_year"],
    growth_data["mom_growth_pct"]
)

plt.axhline(
    y=0,
    linewidth=1
)

plt.title("Month-over-Month Revenue Growth")
plt.xlabel("Month")
plt.ylabel("Growth (%)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================================
# 12. LOAD CUSTOMER RFM DATA
# ============================================================

rfm = pd.read_sql(
    "SELECT * FROM analytics.v_customer_rfm",
    engine
)

print("\nRFM Data:")
print(rfm.head())

print("\nRFM Shape:")
print(rfm.shape)

print("\nRFM Statistics:")

print(
    rfm[
        [
            "recency",
            "frequency",
            "monetary"
        ]
    ].describe()
)
# ============================================================
# 13. RFM DISTRIBUTIONS
# ============================================================

# -----------------------------
# Recency Distribution
# -----------------------------

plt.figure(figsize=(10, 6))

plt.hist(
    rfm["recency"],
    bins=30
)

plt.title("Customer Recency Distribution")
plt.xlabel("Recency (Days)")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.show()


# -----------------------------
# Frequency Distribution
# -----------------------------

plt.figure(figsize=(10, 6))

plt.hist(
    rfm["frequency"],
    bins=30
)

plt.title("Customer Frequency Distribution")
plt.xlabel("Number of Orders")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.show()


# -----------------------------
# Monetary Distribution
# -----------------------------

plt.figure(figsize=(10, 6))

plt.hist(
    rfm["monetary"],
    bins=30
)

plt.title("Customer Monetary Distribution")
plt.xlabel("Total Spending")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.show()

# ============================================================
# 14. PREPARE RFM DATA FOR MACHINE LEARNING
# ============================================================

from sklearn.preprocessing import StandardScaler


# Select RFM features
rfm_features = rfm[
    [
        "recency",
        "frequency",
        "monetary"
    ]
].copy()


# Check for missing values
print("\nMissing RFM Values:")
print(rfm_features.isnull().sum())


# Standardize the features
scaler = StandardScaler()

rfm_scaled = scaler.fit_transform(
    rfm_features
)


print("\nScaled RFM Data:")
print(rfm_scaled[:5])

# ============================================================
# 15. ELBOW METHOD FOR K-MEANS
# ============================================================

from sklearn.cluster import KMeans


inertia = []

# Test different numbers of clusters
for k in range(2, 11):

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    kmeans.fit(rfm_scaled)

    inertia.append(
        kmeans.inertia_
    )


# -----------------------------
# Plot Elbow Curve
# -----------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    range(2, 11),
    inertia,
    marker="o"
)

plt.title("Elbow Method for Optimal K")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")

plt.xticks(
    range(2, 11)
)

plt.tight_layout()
plt.show()

# ============================================================
# 16. K-MEANS CUSTOMER CLUSTERING
# ============================================================

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

# Assign each customer to a cluster
rfm["cluster"] = kmeans.fit_predict(rfm_scaled)

print("\nCluster Distribution:")
print(
    rfm["cluster"].value_counts().sort_index()
)

# ============================================================
# 17. PROFILE CUSTOMER CLUSTERS
# ============================================================

cluster_profile = (
    rfm
    .groupby("cluster")
    .agg(
        customers=("customer_unique_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean")
    )
    .round(2)
)

print("\nCustomer Cluster Profile:")
print(cluster_profile)

# ============================================================
# 18. DISPLAY CLUSTER PROFILE CLEARLY
# ============================================================

for cluster_id, row in cluster_profile.iterrows():

    print(f"\nCluster {cluster_id}")
    print(f"Customers: {row['customers']}")
    print(f"Average Recency: {row['avg_recency']} days")
    print(f"Average Frequency: {row['avg_frequency']} orders")
    print(f"Average Monetary: R$ {row['avg_monetary']}")

# ============================================================
# 19. ASSIGN BUSINESS SEGMENT NAMES
# ============================================================

cluster_labels = {
    0: "Lost / Dormant",
    1: "Loyal / Repeat",
    2: "High-Value One-Time",
    3: "Recent One-Time"
}

rfm["segment"] = rfm["cluster"].map(
    cluster_labels
)


print("\nCustomer Segment Distribution:")

print(
    rfm["segment"].value_counts()
)

# ============================================================
# 20. FINAL CUSTOMER SEGMENT PROFILE
# ============================================================

segment_profile = (
    rfm
    .groupby("segment")
    .agg(
        customers=("customer_unique_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean")
    )
    .round(2)
    .sort_values(
        "customers",
        ascending=False
    )
)

print("\nFinal Customer Segment Profile:")

print(segment_profile)

# ============================================================
# 21. CUSTOMER SEGMENT VISUALIZATION
# ============================================================

segment_counts = (
    rfm["segment"]
    .value_counts()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

plt.bar(
    segment_counts.index,
    segment_counts.values
)

plt.title("Customer Segments")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")

plt.xticks(rotation=30)

plt.tight_layout()
plt.show()

# ============================================================
# 22. PREPARE DATA FOR SALES FORECASTING
# ============================================================

forecast_data = monthly_sales[
    [
        "month_year",
        "product_revenue"
    ]
].copy()

# Sort by date
forecast_data = forecast_data.sort_values(
    "month_year"
)

# Create a sequential time index
forecast_data["time_index"] = range(
    len(forecast_data)
)

print("\nForecasting Dataset:")

print(
    forecast_data.head()
)

print("\nNumber of Months:")

print(
    len(forecast_data)
)

# ============================================================
# 23. TRAIN / TEST SPLIT FOR FORECASTING
# ============================================================

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


# Use the first 80% for training
split_index = int(
    len(forecast_data) * 0.8
)

train_data = forecast_data.iloc[
    :split_index
].copy()

test_data = forecast_data.iloc[
    split_index:
].copy()


print("\nTraining Period:")

print(
    train_data[
        ["month_year", "product_revenue"]
    ].iloc[[0, -1]]
)


print("\nTesting Period:")

print(
    test_data[
        ["month_year", "product_revenue"]
    ].iloc[[0, -1]]
)


# ============================================================
# 24. TRAIN LINEAR REGRESSION MODEL
# ============================================================

X_train = train_data[
    ["time_index"]
]

y_train = train_data[
    "product_revenue"
]

X_test = test_data[
    ["time_index"]
]

y_test = test_data[
    "product_revenue"
]


model = LinearRegression()

model.fit(
    X_train,
    y_train
)


# ============================================================
# 25. MAKE TEST PREDICTIONS
# ============================================================

test_data["predicted_revenue"] = model.predict(
    X_test
)


# ============================================================
# 26. MODEL EVALUATION
# ============================================================

mae = mean_absolute_error(
    y_test,
    test_data["predicted_revenue"]
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        test_data["predicted_revenue"]
    )
)


print("\nForecast Model Performance:")

print(f"MAE: R$ {mae:,.2f}")

print(f"RMSE: R$ {rmse:,.2f}")

# ============================================================
# 21. SEGMENT BUSINESS METRICS
# ============================================================

segment_summary = (
    rfm
    .groupby("segment")
    .agg(
        customers=("customer_unique_id", "count"),
        total_revenue=("monetary", "sum"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean")
    )
    .round(2)
)

# Customer percentage
segment_summary["customer_percentage"] = (
    segment_summary["customers"]
    / segment_summary["customers"].sum()
    * 100
).round(2)

# Revenue percentage
segment_summary["revenue_percentage"] = (
    segment_summary["total_revenue"]
    / segment_summary["total_revenue"].sum()
    * 100
).round(2)

# Sort by customer count
segment_summary = segment_summary.sort_values(
    "customers",
    ascending=False
)

print("\nSegment Business Summary:")
print(segment_summary)

# ============================================================
# 22. SAVE CUSTOMER SEGMENTS TO POSTGRESQL
# ============================================================

customer_segments = rfm[
    [
        "customer_unique_id",
        "recency",
        "frequency",
        "monetary",
        "cluster",
        "segment"
    ]
].copy()

customer_segments.to_sql(
    "customer_segments",
    engine,
    schema="analytics",
    if_exists="replace",
    index=False
)

print("\nCustomer segmentation saved to PostgreSQL!")

print(
    f"Customers saved: {len(customer_segments):,}"
)

# ============================================================
# 23. IMPROVED REVENUE FORECAST
# ============================================================

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Create month number
forecast_data["month"] = forecast_data["month_year"].dt.month

# Create seasonal features
forecast_data["month_sin"] = np.sin(
    2 * np.pi * forecast_data["month"] / 12
)

forecast_data["month_cos"] = np.cos(
    2 * np.pi * forecast_data["month"] / 12
)

# Features
X = forecast_data[
    [
        "time_index",
        "month_sin",
        "month_cos"
    ]
]

y = forecast_data["product_revenue"]

# Same 80/20 time-based split
split_index = int(len(forecast_data) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

# Train model
forecast_model = LinearRegression()

forecast_model.fit(X_train, y_train)

# Predictions
y_pred = forecast_model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)

rmse = np.sqrt(
    mean_squared_error(y_test, y_pred)
)

print("\nImproved Forecast Model")
print("-----------------------")
print(f"MAE:  R${mae:,.2f}")
print(f"RMSE: R${rmse:,.2f}")

# Actual vs predicted
forecast_results = forecast_data.iloc[split_index:].copy()

forecast_results["actual_revenue"] = y_test.values
forecast_results["predicted_revenue"] = y_pred

print("\nActual vs Predicted Revenue:")
print(
    forecast_results[
        [
            "month_year",
            "actual_revenue",
            "predicted_revenue"
        ]
    ]
)

# Plot
plt.figure(figsize=(12, 6))

plt.plot(
    forecast_results["month_year"],
    forecast_results["actual_revenue"],
    marker="o",
    label="Actual Revenue"
)

plt.plot(
    forecast_results["month_year"],
    forecast_results["predicted_revenue"],
    marker="o",
    label="Predicted Revenue"
)

plt.title("Actual vs Predicted Monthly Revenue")

plt.xlabel("Month")
plt.ylabel("Revenue (R$)")

plt.xticks(rotation=45)

plt.legend()

plt.tight_layout()

plt.show()

# ============================================================
# 24. SAVE FORECAST RESULTS TO POSTGRESQL
# ============================================================

forecast_output = forecast_results[
    [
        "month_year",
        "actual_revenue",
        "predicted_revenue"
    ]
].copy()

forecast_output.to_sql(
    "revenue_forecast",
    engine,
    schema="analytics",
    if_exists="replace",
    index=False
)

print("\nRevenue forecast saved to PostgreSQL!")

print(
    f"Forecast records saved: {len(forecast_output):,}"
)