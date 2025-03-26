import sqlite3

# Connect to SQLite (creates ncaamb.db if it doesn't exist)
conn = sqlite3.connect("ncaamb.db")
cursor = conn.cursor()

print("Database created successfully!")

conn.close()

conn = sqlite3.connect("mlb.db")
cursor = conn.cursor()

print("Database created successfully!")

conn.close()