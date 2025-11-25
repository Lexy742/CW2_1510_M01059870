import bcrypt
from pathlib import Path
from typing import Optional
from ..data.db import connect_database
from ..data.users import get_user_by_username, insert_user
from ..data.schema import create_users_table

def register_user(username, password, role='user'):
    """Register new user with hashing password."""
    if get_user_by_username(username):
        return False, "Username already exists"

    # Hash the password
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Insert the new user into the database
    insert_user(username, password_hash.decode('utf-8'), role)
    return True, f"User '{username}' registered."
    
def login_user(username, password):
    """Authenticate."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found"
    
    #Verify password
    stored_password_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
        return True, "Login successful!"
    return False, "Incorrect password."

def migrate_users_from_file(filepath: Optional[str] = None):
    """Migrate users from text file to database.

    Behavior:
    - If `filepath` is provided, use it.
    - Otherwise prefer `DATA/users.txt`, then fall back to `users.txt` at repo root.
    """
    # ensure tables exist before migrating
    conn = connect_database()
    create_users_table(conn)
    conn.close()

    candidates = []
    if filepath:
        candidates.append(Path(filepath))
    else:
        candidates.append(Path("DATA") / "users.txt")
        candidates.append(Path("users.txt"))

    chosen = None
    for p in candidates:
        if p.exists():
            chosen = p
            break

    if chosen is None:
        raise FileNotFoundError(f"No users file found in: {[str(p) for p in candidates]}")

    with open(chosen, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            parts = [p.strip() for p in line.strip().split(',')]
            if len(parts) < 2:
                print(f"Skipping malformed line: {line.strip()}")
                continue
            username = parts[0]
            password = parts[1]
            role = parts[2] if len(parts) > 2 else 'user'
            success, msg = register_user(username, password, role)
            if not success:
                print(f"Skipping user {username}: {msg}")
    print(f"User migration completed from {chosen}.")
          
    
  

