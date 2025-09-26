# db_setup.py
import sqlite3

def init_db():
    """Create users table if missing, safely add token column"""
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            token TEXT
        )
    """)

    # Ensure 'token' column exists (safe for existing tables)
    try:
        c.execute("ALTER TABLE users ADD COLUMN token TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists

    conn.commit()
    conn.close()
