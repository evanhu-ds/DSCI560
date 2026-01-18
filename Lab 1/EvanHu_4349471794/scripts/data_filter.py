# Import necessary libraries
from bs4 import BeautifulSoup
import csv
import os

raw_data = "../data/raw_data/web_data.html"
processed_dir = "../data/processed_data"

print("Starting data filtering ...")

# Ensure processed_data directory exists
os.makedirs(processed_dir, exist_ok=True)

# Read HTML file 
with open(raw_data, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

print("Filtering Market banner ...")
market_data = []
market_cards = soup.find_all('a', class_=lambda x: x and 'MarketCard-container' in str(x))

for card in market_cards:
    symbol = card.find(class_=lambda x: x and "MarketCard-symbol" in str(x))
    position = card.find(class_=lambda x: x and "MarketCard-stockPosition" in str(x))
    changes_pct = card.find(class_=lambda x: x and "MarketCard-changesPct" in str(x))

    market_data.append({
        "symbol": symbol.get_text(strip=True) if symbol else "",
        "stockPosition": position.get_text(strip=True) if position else "",
        "changesPct": changes_pct.get_text(strip=True) if changes_pct else ""
    })

print(f"Found {len(market_data)} market entries.")

# Save Market data to CSV
market_data_path = os.path.join(processed_dir, "market_data.csv")

print("Storing Market data into CSV ...")

with open(market_data_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(
        csvfile,
        fieldnames=["symbol", "stockPosition", "changesPct"]
    )
    writer.writeheader()
    writer.writerows(market_data)

print("market_data.csv created successfully.")

print("Filtering Latest News data...")

news_data = []

news_items = soup.find_all("li", class_=lambda x: x and "LatestNews-item" in str(x))

for item in news_items:
    timestamp_tag = item.find(class_=lambda x: x and 'LatestNews-timestamp' in str(x))
    title_tag = item.find(class_=lambda x: x and 'LatestNews-headline' in str(x))
    link_tag = item.find('a', class_=lambda x: x and 'LatestNews-headline' in str(x))
    
    timestamp = timestamp_tag.get_text(strip=True) if timestamp_tag else ""
    title = title_tag.get_text(strip=True) if title_tag else ""
    link = link_tag.get('href', "")
    
    # Remove timestamp from beginning of title (noticed redundancy by viewing CSV file)
    if title and timestamp and title.startswith(timestamp):
        title = title.replace(timestamp, "", 1).strip()
                
    news_data.append({
        "timestamp": timestamp,
        "title": title,
        "link": link
    })

print(f"Found {len(news_data)} news articles.")

# Save News Data CSV
news_csv_path = os.path.join(processed_dir, "news_data.csv")

print("Storing News data into CSV...")
with open(news_csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(
        csvfile,
        fieldnames=["timestamp", "title", "link"]
    )
    writer.writeheader()
    writer.writerows(news_data)

print("news_data.csv created successfully.")

print("Data filtering process completed.")