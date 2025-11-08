# import requests
# from bs4 import BeautifulSoup, Comment
# import pandas as pd
# import math

# url = "https://www.sports-reference.com/cbb/seasons/men/2026-school-stats.html"
# resp = requests.get(url)
# html = resp.text
# soup = BeautifulSoup(html, "html5lib")

# # helper parsers
# def parse_int(td):
#     try:
#         s = td.text.strip()
#         if s == "" or s.upper() == "DUMMY":
#             return None
#         # sometimes they use "iz" classes but text may be empty
#         return int(float(s))  # handles "0" or "0.0"
#     except Exception:
#         return None

# def parse_float(td, percent=False, keep_fraction=False):
#     """Parse numeric strings robustly.
#     - percent=True: convert .468 or 0.468 -> 46.8
#     - keep_fraction=True: keep as fraction (0.468) rather than percent
#     """
#     try:
#         s = td.text.strip()
#         if s == "" or s.upper() == "DUMMY":
#             return None
#         # remove commas
#         s = s.replace(",", "")
#         # handle values like ".468"
#         if s.startswith("."):
#             val = float(s)
#         else:
#             val = float(s)
#         if percent:
#             # if already looks like a fraction (<=1), convert to percent
#             if 0 <= val <= 1 and not keep_fraction:
#                 return round(val * 100, 2)
#             else:
#                 # it's already expressed (like "46.8"), keep as-is
#                 return round(val, 2)
#         else:
#             return round(val, 3) if (abs(val) < 10 and "." in s) else int(val) if val.is_integer() else round(val, 3)
#     except Exception:
#         return None

# # find table: prefer live table id="school-stats", fallback to commented block
# table = soup.find("table", {"id": "school-stats"})
# if table is None:
#     # search comments for the table markup
#     comments = soup.find_all(string=lambda text: isinstance(text, Comment))
#     for c in comments:
#         if "school-stats" in c:
#             table = BeautifulSoup(c, "html5lib").find("table", {"id": "school-stats"})
#             if table:
#                 break

# if table is None:
#     raise RuntimeError("Couldn't find table with id='school-stats' on page. Inspect response.text to confirm layout.")

# rows = table.find_all("tr")

# data = []
# for row in rows:
#     # skip header/over_header rows
#     if 'over_header' in row.get('class', []) or 'thead' in row.get('class', []):
#         continue
#     # make sure it's a data row (has school_name)
#     school_name_td = row.find("td", {"data-stat": "school_name"})
#     if not school_name_td or not school_name_td.find("a"):
#         continue
#     try:
#         team_name = school_name_td.find("a").text.strip()
#         # numeric fields (use parse_int/parse_float)
#         games = parse_int(row.find("td", {"data-stat": "g"}))
#         wins = parse_int(row.find("td", {"data-stat": "wins"}))
#         losses = parse_int(row.find("td", {"data-stat": "losses"}))
#         win_pct = parse_float(row.find("td", {"data-stat": "win_loss_pct"}), percent=False, keep_fraction=True)  # keep as fraction (1.000 -> 1.0)
#         srs = parse_float(row.find("td", {"data-stat": "srs"}), percent=False)
#         sos = parse_float(row.find("td", {"data-stat": "sos"}), percent=False)

#         conf_wins = parse_int(row.find("td", {"data-stat": "wins_conf"}))
#         conf_losses = parse_int(row.find("td", {"data-stat": "losses_conf"}))
#         home_wins = parse_int(row.find("td", {"data-stat": "wins_home"}))
#         home_losses = parse_int(row.find("td", {"data-stat": "losses_home"}))
#         away_wins = parse_int(row.find("td", {"data-stat": "wins_visitor"}))
#         away_losses = parse_int(row.find("td", {"data-stat": "losses_visitor"}))

#         points = parse_int(row.find("td", {"data-stat": "pts"}))
#         opp_points = parse_int(row.find("td", {"data-stat": "opp_pts"}))
#         min_played = parse_int(row.find("td", {"data-stat": "mp"}))

#         fg_made = parse_int(row.find("td", {"data-stat": "fg"}))
#         fg_attempted = parse_int(row.find("td", {"data-stat": "fga"}))
#         fg_pct = parse_float(row.find("td", {"data-stat": "fg_pct"}), percent=True)   # .468 -> 46.8

#         three_made = parse_int(row.find("td", {"data-stat": "fg3"}))
#         three_attempted = parse_int(row.find("td", {"data-stat": "fg3a"}))
#         three_pct = parse_float(row.find("td", {"data-stat": "fg3_pct"}), percent=True)

#         ft_made = parse_int(row.find("td", {"data-stat": "ft"}))
#         ft_attempted = parse_int(row.find("td", {"data-stat": "fta"}))
#         ft_pct = parse_float(row.find("td", {"data-stat": "ft_pct"}), percent=True)

#         off_rebounds = parse_int(row.find("td", {"data-stat": "orb"}))
#         total_rebounds = parse_int(row.find("td", {"data-stat": "trb"}))
#         assists = parse_int(row.find("td", {"data-stat": "ast"}))
#         steals = parse_int(row.find("td", {"data-stat": "stl"}))
#         blocks = parse_int(row.find("td", {"data-stat": "blk"}))
#         turnovers = parse_int(row.find("td", {"data-stat": "tov"}))
#         personal_fouls = parse_int(row.find("td", {"data-stat": "pf"}))
#         ncaa_tournament = 1 if school_name_td.find("small") else 0

#         data.append({
#             "team_name": team_name,
#             "games": games,
#             "wins": wins,
#             "losses": losses,
#             "win_pct_fraction": win_pct,   # fraction like 1.0 ; you can convert to percent if preferred
#             "srs": srs,
#             "sos": sos,
#             "conf_wins": conf_wins,
#             "conf_losses": conf_losses,
#             "home_wins": home_wins,
#             "home_losses": home_losses,
#             "away_wins": away_wins,
#             "away_losses": away_losses,
#             "points": points,
#             "opp_points": opp_points,
#             "min_played": min_played,
#             "fg_made": fg_made,
#             "fg_attempted": fg_attempted,
#             "fg_pct": fg_pct,
#             "three_made": three_made,
#             "three_attempted": three_attempted,
#             "three_pct": three_pct,
#             "ft_made": ft_made,
#             "ft_attempted": ft_attempted,
#             "ft_pct": ft_pct,
#             "off_rebounds": off_rebounds,
#             "total_rebounds": total_rebounds,
#             "assists": assists,
#             "steals": steals,
#             "blocks": blocks,
#             "turnovers": turnovers,
#             "personal_fouls": personal_fouls,
#             "ncaa_tournament": ncaa_tournament
#         })
#     except Exception:
#         # skip malformed rows but continue scraping others
#         continue

# team_stats_2026 = pd.DataFrame(data)

# # optional: convert win fraction to percent column if you prefer
# if not team_stats_2026.empty and "win_pct_fraction" in team_stats_2026.columns:
#     team_stats_2026["win_pct_percent"] = team_stats_2026["win_pct_fraction"].apply(
#         lambda x: round(x * 100, 2) if (x is not None and x <= 1) else (round(x,2) if isinstance(x, (int,float)) else None)
#     )

# # show top rows (Power BI will read the DataFrame when this script is used there)
# print(team_stats_2026.head())




import requests
from bs4 import BeautifulSoup, Comment

url = "https://www.sports-reference.com/cbb/seasons/men/2026-school-stats.html"
html = requests.get(url).text
soup = BeautifulSoup(html, "html5lib")

# Print out the first ~2000 characters so we can view structure
print(html[:2000])
# You can also search for “<table” or “data‑stat=” in the code
for table in soup.find_all("table"):
    print("Found table with id=", table.get("id"), "class=", table.get("class"))
