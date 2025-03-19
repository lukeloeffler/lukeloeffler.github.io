import sqlite3
import json

def sqlite_to_json(db_file, json_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            team_name AS "School", 
            rating as "Rating", 
            offensive_efficiency as "OE", 
            defensive_efficiency as "DE", 
            possessions as "POS", 
            games as "G", 
            wins as "W", 
            losses as "L", 
            win_pct AS "W-L%", 
            sos as "SOS", 
            points AS "Tm Pts", 
            opp_points AS "Opp Pts", 
            fg_made as "FG", 
            fg_attempted as "FGA", 
            fg_pct AS "FG%", 
            three_made AS "3P", 
            three_attempted as "3PA", 
            three_pct AS "3P%", 
            ft_made as "FT", 
            ft_attempted as "FTA", 
            ft_pct AS "FT%", 
            off_rebounds as "ORB", 
            total_rebounds as "TRB", 
            assists as "AST", 
            steals as "STL", 
            blocks as "BLK", 
            turnovers as "TOV", 
            personal_fouls as "PF", 
            ncaa_tournament as "MM" 
        FROM team_stats 
        ORDER BY rating DESC
    """)
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()

    data = []
    ranked_data = []
    for row in rows:
        data.append(dict(zip(columns, row)))

    # Add "Rank" based on rating
    rank = 1
    for item in data:
        item["Rank"] = rank
        ranked_data.append(item)
        rank += 1

    # Move "Rank" to the front of each dictionary
    for item in ranked_data:
        rank_val = item.pop("Rank")
        new_item = {"Rank": rank_val, **item} #create new item
        ranked_data[ranked_data.index(item)] = new_item #replace old item with new item

    with open(json_file, 'w') as f:
        json.dump(ranked_data, f, indent=4) #dump the ranked data.

sqlite_to_json('ncaamb.db', '2025team_stats.json')
print("Data exported to 2025team_stats.json")