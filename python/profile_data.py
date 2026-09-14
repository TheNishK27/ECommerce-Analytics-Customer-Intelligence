from pathlib import Path
import pandas as pd


# Location of our raw datasets
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def profile_dataset(file_path):
    """Print basic information about a CSV dataset."""

    df = pd.read_csv(file_path)

    print("=" * 70)
    print(f"FILE: {file_path.name}")
    print("=" * 70)

    print(f"Rows       : {df.shape[0]:,}")
    print(f"Columns    : {df.shape[1]}")

    print("\nColumns:")
    print(list(df.columns))

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\n")


def main():
    csv_files = sorted(DATA_DIR.glob("*.csv"))

    print(f"Found {len(csv_files)} CSV files.\n")

    for file_path in csv_files:
        profile_dataset(file_path)


if __name__ == "__main__":
    main()