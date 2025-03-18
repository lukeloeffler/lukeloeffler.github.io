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

# ONLY USE TO RESET TABLE: cursor.execute("DROP TABLE IF EXISTS team_stats")

# Create TeamStats Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS team_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT UNIQUE,
    games INTEGER,
    wins INTEGER,
    losses INTEGER,
    win_pct FLOAT,
    conf_wins INTEGER,
    conf_losses INTEGER,
    home_wins INTEGER,
    home_losses INTEGER,
    away_wins INTEGER,
    away_losses INTEGER,
    points INTEGER,
    opp_points INTEGER,
    fg_made INTEGER,
    fg_attempted INTEGER,
    three_made INTEGER,
    three_attempted INTEGER,
    ft_made INTEGER,
    ft_attempted INTEGER,
    off_rebounds INTEGER,
    total_rebounds INTEGER,
    assists INTEGER,
    steals INTEGER,
    blocks INTEGER,
    turnovers INTEGER,
    personal_fouls INTEGER,
    FOREIGN KEY (team_name) REFERENCES teams(name)
)
''')

conn.commit()
conn.close()
print("Tables created successfully!")
