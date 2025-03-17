import sqlite3

conn = sqlite3.connect("ncaamb.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Existing tables:", tables)

conn.close()

conn.execute('PRAGMA database_list;')