import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

# Add the token column
c.execute("ALTER TABLE users ADD COLUMN token TEXT")

conn.commit()
conn.close()
print("Column 'token' added successfully.")
