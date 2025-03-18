import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("ncaamb.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(tables)


# Query the team_stats table
cursor.execute("SELECT * FROM team_stats")

# Fetch all rows
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

# Close the connection
conn.close()
