import sqlite3

# Connect to a new database (or recreate)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    age INTEGER,
    password TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("✅ users.db created and table `users` added successfully.")
