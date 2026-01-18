from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import time

url = "https://www.cnbc.com/world/?region=world"

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up browser
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

# Open page
driver.get(url)

# Wait for content to load
time.sleep(5)

WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='MarketCard-container']")))

# Get fully rendered HTML
html = driver.page_source
driver.quit()

# Parse with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Create directory 
os.makedirs("../data/raw_data", exist_ok=True)

# Save HTML
with open("../data/raw_data/web_data.html", "w", encoding="utf-8") as file:
    file.write(soup.prettify())

print("Rendered page saved to raw_data/web_data.html")
