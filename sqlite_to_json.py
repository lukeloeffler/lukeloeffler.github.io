import sqlite3
import json

def sqlite_to_json(db_file, json_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM team_stats")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()

    data = []
    for row in rows:
        data.append(dict(zip(columns, row)))

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

sqlite_to_json('ncaamb.db', '2025team_stats.json')
print("Data exported to 2025team_stats.json")