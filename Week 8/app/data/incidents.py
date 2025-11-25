import pandas as pd
from .db import connect_database

def insert_incident(data, incident_type, severity, status, description, reported_by=None):
    """Insert a new incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO cyber_incidents (data, incident_type, severity, status, description, reported_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (data, incident_type, severity, status, description, reported_by)
    )
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents():
    """Get all incidencts as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY id DESC", conn)
    conn.close()
    return df

def update_incident_status(incident_id, new_status):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE cyber_incidents SET status = ? WHERE id = ?", (new_status, incident_id))
    conn.commit()
    conn.close()
    
def delete_incident(incident_id):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
    conn.close()

