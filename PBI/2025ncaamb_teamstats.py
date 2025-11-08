import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL to scrape team stats
url = "https://www.sports-reference.com/cbb/seasons/men/2025-school-stats.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html5lib")

# Find all rows from url
rows = soup.find_all("tr")

# Function to calculate the rating
# def calculate_rating(oe, de, sos, oe_weight=0.35, de_weight=0.35, sos_weight=0.3):
#     """Calculates the overall team rating."""
#     rating = (oe_weight * oe) + (de_weight * (100 - de)) + (sos_weight * sos)
#     return round(rating, 2)

# Collect data in list of dicts
data = []

for row in rows:
    if 'over_header' in row.get('class', []) or 'thead' in row.get('class', []):
        continue
    try:
        school_name_td = row.find("td", {"data-stat": "school_name"})
        if school_name_td and school_name_td.find("a"):
            team_name = school_name_td.find("a").text.strip()
            games = int(row.find("td", {"data-stat": "g"}).text.strip())
            wins = int(row.find("td", {"data-stat": "wins"}).text.strip())
            losses = int(row.find("td", {"data-stat": "losses"}).text.strip())
            win_pct = round(float(row.find("td", {"data-stat": "win_loss_pct"}).text.strip()), 2)
            srs = round(float(row.find("td", {"data-stat": "srs"}).text.strip()), 2)
            sos = round(float(row.find("td", {"data-stat": "sos"}).text.strip()), 2)
            conf_wins = int(row.find("td", {"data-stat": "wins_conf"}).text.strip())
            conf_losses = int(row.find("td", {"data-stat": "losses_conf"}).text.strip())
            home_wins = int(row.find("td", {"data-stat": "wins_home"}).text.strip())
            home_losses = int(row.find("td", {"data-stat": "losses_home"}).text.strip())
            away_wins = int(row.find("td", {"data-stat": "wins_visitor"}).text.strip())
            away_losses = int(row.find("td", {"data-stat": "losses_visitor"}).text.strip())
            points = int(row.find("td", {"data-stat": "pts"}).text.strip())
            opp_points = int(row.find("td", {"data-stat": "opp_pts"}).text.strip())
            min_played = int(row.find("td", {"data-stat": "mp"}).text.strip())
            fg_made = int(row.find("td", {"data-stat": "fg"}).text.strip())
            fg_attempted = int(row.find("td", {"data-stat": "fga"}).text.strip())
            three_made = int(row.find("td", {"data-stat": "fg3"}).text.strip())
            three_attempted = int(row.find("td", {"data-stat": "fg3a"}).text.strip())
            ft_made = int(row.find("td", {"data-stat": "ft"}).text.strip())
            ft_attempted = int(row.find("td", {"data-stat": "fta"}).text.strip())
            off_rebounds = int(row.find("td", {"data-stat": "orb"}).text.strip())
            total_rebounds = int(row.find("td", {"data-stat": "trb"}).text.strip())
            assists = int(row.find("td", {"data-stat": "ast"}).text.strip())
            steals = int(row.find("td", {"data-stat": "stl"}).text.strip())
            blocks = int(row.find("td", {"data-stat": "blk"}).text.strip())
            turnovers = int(row.find("td", {"data-stat": "tov"}).text.strip())
            personal_fouls = int(row.find("td", {"data-stat": "pf"}).text.strip())
            ncaa_tournament = 1 if school_name_td.find("small") else 0

            # Derived metrics
            fg_pct = round((fg_made / fg_attempted) * 100, 2) if fg_attempted else 0
            three_pct = round((three_made / three_attempted) * 100, 2) if three_attempted else 0
            ft_pct = round((ft_made / ft_attempted) * 100, 2) if ft_attempted else 0
            # possessions = round(fg_attempted + 0.44 * ft_attempted - off_rebounds + turnovers, 2)
            # offensive_efficiency = round((points / possessions) * 100 if possessions else 0, 2)
            # defensive_efficiency = round((opp_points / possessions) * 100 if possessions else 0, 2)
            # rating = calculate_rating(offensive_efficiency, defensive_efficiency, sos)

            data.append({
                "team_name": team_name,
                "games": games,
                "wins": wins,
                "losses": losses,
                "win_pct": win_pct,
                "srs": srs,
                "sos": sos,
                "conf_wins": conf_wins,
                "conf_losses": conf_losses,
                "home_wins": home_wins,
                "home_losses": home_losses,
                "away_wins": away_wins,
                "away_losses": away_losses,
                "points": points,
                "opp_points": opp_points,
                "min_played": min_played,
                "fg_made": fg_made,
                "fg_attempted": fg_attempted,
                "fg_pct": fg_pct,
                "three_made": three_made,
                "three_attempted": three_attempted,
                "three_pct": three_pct,
                "ft_made": ft_made,
                "ft_attempted": ft_attempted,
                "ft_pct": ft_pct,
                "off_rebounds": off_rebounds,
                "total_rebounds": total_rebounds,
                "assists": assists,
                "steals": steals,
                "blocks": blocks,
                "turnovers": turnovers,
                "personal_fouls": personal_fouls,
                "ncaa_tournament": ncaa_tournament
            })
    except Exception:
        continue

# Convert list of dicts → pandas DataFrame
team_stats_2025 = pd.DataFrame(data)

# Output DataFrame to Power BI
team_stats_2025