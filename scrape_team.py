import requests
from bs4 import BeautifulSoup
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("ncaamb.db")
cursor = conn.cursor()

# URL to scrape (this is just an example, update with the correct URL)
url = 'https://www.example.com/ncaamb-teams'  # Change this to your actual data source URL
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Example: Find all team names and conference (you'll need to adjust based on the website structure)
teams = soup.find_all('div', class_='team-info')  # Update this based on actual HTML structure

for team in teams:
    name = team.find('span', class_='team-name').text  # Adjust based on actual HTML structure
    conference = team.find('span', class_='team-conference').text  # Adjust based on actual HTML structure
    rating = float(team.find('span', class_='team-rating').text)  # Adjust based on actual HTML structure

    # Insert into database
    cursor.execute('''
    INSERT OR IGNORE INTO teams (name, conference, rating) 
    VALUES (?, ?, ?)''', (name, conference, rating))

# Commit changes and close connection
conn.commit()
conn.close()

print("Teams data scraped and inserted into database!")
