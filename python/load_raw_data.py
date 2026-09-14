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
# 3. Locate raw data folder
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"


# --------------------------------------------------
# 4. Load every CSV
# --------------------------------------------------

csv_files = sorted(DATA_DIR.glob("*.csv"))

print(f"Found {len(csv_files)} CSV files.\n")


for csv_file in csv_files:

    print("=" * 60)
    print(f"Loading: {csv_file.name}")

    # Read CSV
    df = pd.read_csv(csv_file)

    # Convert filename to PostgreSQL table name
    table_name = csv_file.stem.replace("olist_", "").replace("_dataset", "")

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    # Load into PostgreSQL
    df.to_sql(
        table_name,
        engine,
        schema="raw",
        if_exists="replace",
        index=False
    )

    print(f"Loaded → raw.{table_name}")


print("\nAll datasets loaded successfully!")