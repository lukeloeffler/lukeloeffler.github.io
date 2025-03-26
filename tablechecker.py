import sqlite3

# # Connect to SQLite database
# conn = sqlite3.connect("ncaamb.db")
# cursor = conn.cursor()

# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = cursor.fetchall()
# print(tables)


# # Query the team_stats table
# cursor.execute("SELECT * FROM team_stats")

# # Fetch all rows
# rows = cursor.fetchall()

# # Print each row
# for row in rows:
#     print(row)

# # Close the connection
# conn.close()


conn = sqlite3.connect("mlb.db")
cursor = conn.cursor()

# Check if the table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='batting';")
table_exists = cursor.fetchone()

if table_exists:
    print("The 'batting' table exists in the mlb.db database.")
else:
    print("The 'batting' table does not exist in the mlb.db database.")

conn.close()
