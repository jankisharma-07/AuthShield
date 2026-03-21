import sqlite3

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    status TEXT,
    ip TEXT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

conn.commit()

# Default user
cursor.execute("INSERT OR IGNORE INTO users VALUES ('admin','Admin@123')")
conn.commit()