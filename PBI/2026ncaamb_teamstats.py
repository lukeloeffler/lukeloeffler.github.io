import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd

# URL to scrape team stats
url = "https://www.sports-reference.com/cbb/seasons/men/2026-school-stats.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser") 

# Find all rows from url
comments = soup.find_all(string=lambda text: isinstance(text, Comment))
table_html = None
target_id = 'all_NCAAM_schools'

for comment in comments:
    if f'id="{target_id}"' in comment:
        table_html = comment
        break

rows = []
if table_html:
    # Re-parse the table HTML string that was inside the comment
    table_soup = BeautifulSoup(table_html, "html.parser")
    tbody = table_soup.find("tbody")
    if tbody:
        rows = tbody.find_all("tr")
else:
    # Fallback: Check if the table is loaded directly
    table_direct = soup.find("table", id=target_id)
    if table_direct and table_direct.find("tbody"):
        rows = table_direct.find("tbody").find_all("tr")
    else:
        # If this message prints, the extraction logic failed.
        print(f"Could not find the '{target_id}' table data.")


# Collect data in list of dicts
data = []

if rows:
    for row in rows:
        if 'over_header' in row.get('class', []) or 'thead' in row.get('class', []) or not row.find("td", {"data-stat": "school_name"}):
            continue
            
        try:
            school_name_td = row.find("td", {"data-stat": "school_name"})
            # Ensure it's a valid team row (has a link)
            if school_name_td and school_name_td.find("a"): 
                team_name = school_name_td.find("a").text.strip()
                games = int(row.find("td", {"data-stat": "g"}).text.strip() or 0)
                wins = int(row.find("td", {"data-stat": "wins"}).text.strip() or 0)
                losses = int(row.find("td", {"data-stat": "losses"}).text.strip() or 0)
                win_pct = round(float(row.find("td", {"data-stat": "win_loss_pct"}).text.strip() or 0), 4)
                srs = round(float(row.find("td", {"data-stat": "srs"}).text.strip() or 0), 4)
                sos = round(float(row.find("td", {"data-stat": "sos"}).text.strip() or 0), 4)
                conf_wins = int(row.find("td", {"data-stat": "wins_conf"}).text.strip() or 0) 
                conf_losses = int(row.find("td", {"data-stat": "losses_conf"}).text.strip() or 0)
                home_wins = int(row.find("td", {"data-stat": "wins_home"}).text.strip() or 0)
                home_losses = int(row.find("td", {"data-stat": "losses_home"}).text.strip() or 0)
                away_wins = int(row.find("td", {"data-stat": "wins_visitor"}).text.strip() or 0)
                away_losses = int(row.find("td", {"data-stat": "losses_visitor"}).text.strip() or 0)
                points = int(row.find("td", {"data-stat": "pts"}).text.strip() or 0)
                opp_points = int(row.find("td", {"data-stat": "opp_pts"}).text.strip() or 0)
                min_played = int(row.find("td", {"data-stat": "mp"}).text.strip() or 0)
                fg_made = int(row.find("td", {"data-stat": "fg"}).text.strip() or 0)
                fg_attempted = int(row.find("td", {"data-stat": "fga"}).text.strip() or 1) # Use 1 to prevent ZeroDivisionError below
                three_made = int(row.find("td", {"data-stat": "fg3"}).text.strip() or 0)
                three_attempted = int(row.find("td", {"data-stat": "fg3a"}).text.strip() or 1) # Use 1 to prevent ZeroDivisionError below
                ft_made = int(row.find("td", {"data-stat": "ft"}).text.strip() or 0)
                ft_attempted = int(row.find("td", {"data-stat": "fta"}).text.strip() or 1) # Use 1 to prevent ZeroDivisionError below
                off_rebounds = int(row.find("td", {"data-stat": "orb"}).text.strip() or 0)
                total_rebounds = int(row.find("td", {"data-stat": "trb"}).text.strip() or 0)
                assists = int(row.find("td", {"data-stat": "ast"}).text.strip() or 0)
                steals = int(row.find("td", {"data-stat": "stl"}).text.strip() or 0)
                blocks = int(row.find("td", {"data-stat": "blk"}).text.strip() or 0)
                turnovers = int(row.find("td", {"data-stat": "tov"}).text.strip() or 0)
                personal_fouls = int(row.find("td", {"data-stat": "pf"}).text.strip() or 0)
                ncaa_tournament = 1 if school_name_td.find("small") else 0

                # Derived metrics
                fg_pct = round((fg_made / fg_attempted) * 100, 4)
                three_pct = round((three_made / three_attempted) * 100, 4)
                ft_pct = round((ft_made / ft_attempted) * 100, 4)

                data.append({
                    "team_name": team_name, "games": games, "wins": wins, "losses": losses, "win_pct": win_pct, 
                    "srs": srs, "sos": sos, "conf_wins": conf_wins, "conf_losses": conf_losses, 
                    "home_wins": home_wins, "home_losses": home_losses, "away_wins": away_wins, 
                    "away_losses": away_losses, "points": points, "opp_points": opp_points, 
                    "min_played": min_played, "fg_made": fg_made, "fg_attempted": fg_attempted, 
                    "fg_pct": fg_pct, "three_made": three_made, "three_attempted": three_attempted, 
                    "three_pct": three_pct, "ft_made": ft_made, "ft_attempted": ft_attempted, 
                    "ft_pct": ft_pct, "off_rebounds": off_rebounds, "total_rebounds": total_rebounds,
                    "assists": assists, "steals": steals, "blocks": blocks,
                    "turnovers": turnovers, "personal_fouls": personal_fouls,
                    "ncaa_tournament": ncaa_tournament
                })
        except Exception:
            # Catches any unexpected errors during data parsing for a specific row
            continue

# Convert list of dicts → pandas DataFrame
team_info = pd.DataFrame(data)