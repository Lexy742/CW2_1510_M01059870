from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents 
from app.data.datasets import load_csv_to_table 
from pathlib import Path 

def main():
    print("=" * 60)
    print("Week 8: Database Integration and User Management")
    print("=" * 60)
    
    #1. Setup Database
    print("Setting up the database...")
    conn = connect_database()
    create_all_tables(conn)
    conn.close()
    
    #2. Migrate users from file
    migrate_users_from_file()
    
    #Load CSV files
    load_csv_to_table(Path("DATA") / "cyber_incidents.csv", "cyber_incidents")
    load_csv_to_table(Path("DATA") / "it_tickets.csv", "it_tickets")
    load_csv_to_table(Path("DATA") / "datasets_metadata.csv", "datasets_metadata")
    print("Database setup and data loading complete.")
    
    #3. Test Authentication
    success, msg = register_user("lexy", "SecurePass123", "analyst")
    print(msg)
    
    success, msg = login_user("lexy", "SecurePass123")
    print(msg)
    
    #4. Test CRUD
    incident_id = insert_incident("2025-01-15", "Phishing", "High", "Open", "Phishing email reported", "lexy")
    print(f"Inserted incident with ID: {incident_id}")
    incidents_df = get_all_incidents()
    print("All Incidents:")
    print(incidents_df.head())
    
    
    

if __name__ == "__main__":
    main()


