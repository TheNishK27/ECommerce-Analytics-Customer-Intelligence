import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# --------------------------------------------------
# 2. Create PostgreSQL connection
# --------------------------------------------------

connection_url = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(connection_url)


# --------------------------------------------------
# 3. Locate CSV
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

csv_path = (
    BASE_DIR
    / "data"
    / "raw"
    / "olist_customers_dataset.csv"
)


# --------------------------------------------------
# 4. Read CSV
# --------------------------------------------------

df = pd.read_csv(csv_path)

print(f"CSV loaded successfully.")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")


# --------------------------------------------------
# 5. Load into PostgreSQL
# --------------------------------------------------

df.to_sql(
    "customers",
    engine,
    schema="raw",
    if_exists="replace",
    index=False
)

print("Customers table loaded successfully!")
print("Table: raw.customers")