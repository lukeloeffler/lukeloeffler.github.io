import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd

# URL to scrape team stats
url = "https://www.sports-reference.com/cbb/schools/#site_menu_link"

# URL to grab logo page
base_url = "https://www.sports-reference.com"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser") 

# Find all rows from url
comments = soup.find_all(string=lambda text: isinstance(text, Comment))
table_html = None
target_id = 'NCAAM_schools'

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
            
            anchor_tag = school_name_td.find("a")
            # Find the anchor tag

            if school_name_td and school_name_td.find("a") and anchor_tag: 
                school_name = school_name_td.find("a").text.strip()

                url_relative = anchor_tag['href']
                url_full = base_url + url_relative

                location = (row.find("td", {"data-stat": "location"}).text.strip() or "null")
                year_min = int(row.find("td", {"data-stat": "year_min"}).text.strip() or 0)
                year_max = int(row.find("td", {"data-stat": "year_max"}).text.strip() or 0)
                years = int(row.find("td", {"data-stat": "years"}).text.strip() or 0)                                
                games = int(row.find("td", {"data-stat": "g"}).text.strip() or 0)
                wins = int(row.find("td", {"data-stat": "wins"}).text.strip() or 0)
                losses = int(row.find("td", {"data-stat": "losses"}).text.strip() or 0)
                win_pct = round(float(row.find("td", {"data-stat": "win_loss_pct"}).text.strip() or 0), 4)
                srs = round(float(row.find("td", {"data-stat": "srs"}).text.strip() or 0), 4)
                sos = round(float(row.find("td", {"data-stat": "sos"}).text.strip() or 0), 4)
                ncaa_count = int(row.find("td", {"data-stat": "ncaa_count"}).text.strip() or 0)
                ncaa_final_four = int(row.find("td", {"data-stat": "ncaa_final_four_count"}).text.strip() or 0)                
                ncaa_champ = int(row.find("td", {"data-stat": "ncaa_champ_count"}).text.strip() or 0)

                data.append({
                    "school_name": school_name, "url": url_full, "location": location, "year_min": year_min, "year_max": year_max, 
                    "years": years, "games": games, "wins": wins, "losses": losses, "win_pct": win_pct, "srs": srs, 
                    "sos": sos, "ncaa_count": ncaa_count, "ncaa_final_four": ncaa_final_four, "ncaa_champ": ncaa_champ
                })
        except Exception:
            # Catches any unexpected errors during data parsing for a specific row
            continue

# Convert list of dicts → pandas DataFrame
team_info = pd.DataFrame(data)