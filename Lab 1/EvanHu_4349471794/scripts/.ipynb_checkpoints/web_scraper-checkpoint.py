import requests
from bs4 import BeautifulSoup
import os

url = "https://www.cnbc.com/world/?region=world"

# Add browser-like headers
headers = {'User-Agent': 'Mozilla/5.0'}

# Send request to target URL
response = requests.get(url, headers=headers)

# Status code of 200 is a successful request
if response.status_code == 200:
    # Use BeautifulSoup's HTML parser
    soup = BeautifulSoup(response.text, "html.parser")

    # Ensure directory to store web data exists
    os.makedirs("../data/raw_data", exist_ok=True)

    # Save HTML file
    file_path = "../data/raw_data/web_data.html"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    
    print("Web scraping successful! Saved collected data.")

# Otherwise request is unsuccessful 
else:
    print("Web scraping unsuccessful.")