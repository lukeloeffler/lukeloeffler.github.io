import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import os

# Define the base URL once
BASE_URL = "https://www.sports-reference.com"
url = f"{BASE_URL}/cbb/schools/" 

print(f"Attempting to fetch data from: {url}")

try:
    response = requests.get(url, timeout=15)
    response.raise_for_status() # Raise an error for bad status codes (4xx or 5xx)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser") 

    # --- DEBUG STEP 1: Save the raw HTML to a file ---
    file_path = "raw_cbb_schools_html.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully saved raw HTML to: {os.path.abspath(file_path)}")

    # --- DEBUG STEP 2: Extract Comments and find the table ---
    target_id = 'NCAAM_schools' 
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    table_html = None
    
    print(f"\nFound {len(comments)} HTML comments. Searching for table ID '{target_id}'...")

    # Print the start of the first 5 comments for manual inspection
    for i, comment in enumerate(comments[:5]):
        print(f"\n--- Start of Comment {i+1} ---")
        print(comment.strip()[:500]) # Print first 500 characters
        print(f"--- End of Comment {i+1} ---")
        
        # Check if the table ID is present in the comment
        if f'<table class="sortable stats_table" id="{target_id}">' in comment:
            table_html = comment
            print(f"\n***SUCCESS: Found table ID '{target_id}' in Comment {i+1}***")
            break
        
    if table_html:
        # Re-parse the table HTML string that was inside the comment
        table_soup = BeautifulSoup(table_html, "html.parser")
        rows = table_soup.find("tbody").find_all("tr")
        print(f"\nSuccessfully parsed {len(rows)} rows from the table HTML.")
    else:
        # Fallback: Check if the table is loaded directly (unlikely)
        table_direct = soup.find("table", id=target_id)
        if table_direct and table_direct.find("tbody"):
            rows = table_direct.find("tbody").find_all("tr")
        else:
            print(f"\nERROR: Could not find the '{target_id}' table data in any comment or directly.")
            rows = []
            
except requests.exceptions.RequestException as e:
    print(f"\nERROR: Failed to fetch the URL. Check network connection or URL validity: {e}")
    rows = []
except AttributeError:
    # Handles error if find("tbody") fails after finding the comment but before finding rows
    print("\nERROR: Found the comment, but failed to parse the <tbody>. The table structure might be broken.")
    rows = []

# --- STEP 3: Collect Data (only runs if rows were found) ---
data = []

if rows:
    # The rest of your data collection logic goes here (omitted for brevity)
    # Since this is a debug script, we just confirm rows were found.
    # We will print a simple DataFrame to confirm success.
    for row in rows:
        school_name_td = row.find("td", {"data-stat": "school_name"})
        if school_name_td and school_name_td.find("a"): 
            team_name = school_name_td.find("a").text.strip()
            data.append({"school_name": team_name})
            
    team_info_table = pd.DataFrame(data)
    print("\n--- Output DataFrame Sample ---")
    print(team_info_table.head())
    
    # CRITICAL FOR POWER BI: Print the final DataFrame
    print(team_info_table)
else:
    team_info_table = pd.DataFrame()
    print("\n--- Output DataFrame Sample ---")
    print("Empty DataFrame - Data extraction failed.")
    print(team_info_table)