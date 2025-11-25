import sqlite3
from pathlib import Path

DB_PATH = Path ("DATA") / "intelligence_platform.db"
def connect_database(db_path=DB_PATH):
    """Connect to SQlite Database."""
    # ensure parent directory exists so sqlite can create the file
    db_dir = Path(db_path).parent
    try:
        db_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        # if directory creation fails, let sqlite raise a clear error
        pass
    return sqlite3.connect(str(db_path))



