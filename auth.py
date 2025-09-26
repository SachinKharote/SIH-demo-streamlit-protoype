# auth.py
import sqlite3
import hashlib
import secrets
from db_setup import init_db

# Ensure database is ready
init_db()

# -------------------------
# Helper functions
# -------------------------

def hash_password(password):
    """Return SHA256 hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# -------------------------
# User functions
# -------------------------

def create_user(name, email, password):
    if not is_valid_email(email):
        return False, "Invalid email format"

    token = secrets.token_hex(16)  # random token for email verification/reset

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (name, email, password, token) VALUES (?, ?, ?, ?)",
            (name, email, hash_password(password), token)
        )
        conn.commit()
        return True, "User created successfully"
    except sqlite3.IntegrityError:
        # Happens if email already exists
        return False, "Email already registered"
    finally:
        conn.close()

def login_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()

    if not row:
        return False, "User not found"

    stored_password = row[0]
    if stored_password == hash_password(password):
        return True, "Login successful"
    else:
        return False, "Incorrect password"
