import pandas as pd
from .db import connect_database

def load_csv_to_table(csv_path, table_name):
    """Load a CSV file into a specified database table."""
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"CSV file {csv_path} not found.")
        return 0
    except pd.errors.EmptyDataError:
        print(f"CSV file {csv_path} is empty.")
        return 0
    except Exception as e:
        print(f"Error reading CSV file {csv_path}: {e}")
        return 0

    conn = connect_database()
    try:
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Loaded {len(df)} records into table '{table_name}' from '{csv_path}'.")
        return len(df)
    except Exception as e:
        print(f"Error loading CSV to table: {e}")
        return 0
    finally:
        conn.close()
