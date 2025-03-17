import sqlite3

conn = sqlite3.connect("ncaamb.db")
cursor = conn.cursor()

# Create Games Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    team1 TEXT,
    team2 TEXT,
    score1 INTEGER,
    score2 INTEGER,
    location TEXT
)
''')

# Create Teams Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    rating FLOAT,
    conference TEXT
)
''')

conn.commit()
conn.close()
print("Tables created successfully!")
