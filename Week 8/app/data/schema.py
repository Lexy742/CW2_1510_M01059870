def create_users_table(conn):
    """Create users table"""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL UNIQUE,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    
def create_cyber_incidents_table(conn):
    """Create cyber_incidents table"""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            incident_type TEXT,
            severity TEXT,
            status TEXT,
            description TEXT,
            reported_by TEXT,
            reported_at TEXT,
            FOREIGN KEY (reported_by) REFERENCES users(username)
        )
    ''')
    conn.commit()
    
def create_datasets_metadata_table(conn):
    """Create datasets_metadata table"""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL,
            source TEXT,
            size_mb REAL,
            num_records INTEGER,
            last_updated TEXT
        )
    ''')
    conn.commit()
    
def create_it_tickets_table(conn):
    """Create it_tickets table"""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            ticket_id TEXT UNIQUE,
            priority TEXT,
            status TEXT,
            assigned_to TEXT,
            created_date TEXT
        )
    ''')
    conn.commit()
    
def create_all_tables(conn):
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    print("All tables created successfully.")
    