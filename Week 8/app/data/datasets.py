import pandas as pd
from .db import connect_database
from pathlib import Path

def load_csv_to_table(csv_path: Path, table_name: str):
    """Load a CSV file into a specified database table."""
    csv_full_path = Path(csv_path)
    if not csv_full_path.exists():
        print(f"CSV file {csv_path} does not exist.")
        return 0
    
    conn = connect_database()
    try:
        df = pd.read_csv(csv_full_path)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Loaded {len(df)} records into table '{table_name}' from '{csv_path}'.")
        return len(df)
    except Exception as e:
        print(f"Error loading CSV to table: {e}")
        return 0
    finally:
        conn.close()
    