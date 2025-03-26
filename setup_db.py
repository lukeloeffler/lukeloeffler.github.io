import sqlite3

conn = sqlite3.connect("ncaamb.db")
cursor = conn.cursor()

# Create Games Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        team1_id INTEGER,
        team2_id INTEGER,
        score1 INTEGER,
        score2 INTEGER,
        location TEXT,
        FOREIGN KEY (team1_id) REFERENCES team_stats(id),
        FOREIGN KEY (team2_id) REFERENCES team_stats(id)
    )
''')

conn.commit()
conn.close()
print("NCAAMB Tables created successfully!")


conn = sqlite3.connect("mlb.db")
cursor = conn.cursor()

# Create batting Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS batting (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team TEXT UNIQUE,
        batters_count INTEGER,
        batters_age REAL,
        runs_game REAL,
        games INTEGER,
        plate_appearances INTEGER,
        at_bats INTEGER,
        runs INTEGER,
        hits INTEGER,  
        doubles INTEGER,
        triples INTEGER,
        home_runs INTEGER,
        runs_batted_in INTEGER,
        stolen_bases INTEGER,
        caught_stealing INTEGER,
        balls_walks_bases INTEGER,
        strikeouts INTEGER,
        batting_average REAL,
        on_base_pct REAL,
        slugging_pct REAL,
        on_base_slugging REAL,
        on_base_sligging_plus INTEGER,
        total bases INTEGER,
        left_on_base INTEGER
    )
''')

conn.commit()
conn.close()
print("MLB Tables created successfully!")