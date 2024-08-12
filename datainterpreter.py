from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from datetime import datetime, timedelta
import os
import sys

# Set up logging to file
log_file = "D:/assignment/scraper_log.txt"
sys.stdout = open(log_file, 'w')
sys.stderr = sys.stdout

def log(message):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")
    sys.stdout.flush()

log("Script started")

# Initialize the WebDriver
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
driver.maximize_window()

log("WebDriver initialized")

# Define the URLs to scrape
urls = [
    "https://www.linkedin.com/jobs/search?location=India&geoId=102713980&f_C=1035&position=1&pageNum=0",
    "https://www.linkedin.com/jobs/search?keywords=&location=India&geoId=102713980&f_C=1441",  
    "https://www.linkedin.com/jobs/search?keywords=&location=India&geoId=102713980&f_TPR=r86400&f_C=1586&position=1&pageNum=0"
]

jobs = []

def wait_for_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        log(f"Element found: {value}")
        return element
    except TimeoutException:
        log(f"Timed out waiting for element: {value}")
        return None

def scrape_linkedin_jobs(url):
    log(f"Navigating to URL: {url}")
    driver.get(url)
    
    if not wait_for_element(driver, By.CLASS_NAME, "jobs-search__results-list"):
        log("Job results list not found. Skipping this URL.")
        return

    # Scroll down to load more jobs
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(5):  # Scroll 5 times
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        log(f"Scrolled {i+1} times.")

    # Log page source for debugging
    with open("D:/assignment/page_source.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    job_cards = soup.find_all('div', class_='base-card')
    if not job_cards:
        job_cards = soup.find_all('li', class_='jobs-search-results__list-item')
    
    log(f"Page source length: {len(driver.page_source)}")
    log(f"HTML snippet: {driver.page_source[:1000]}")  # Log the first 1000 characters


    for card in job_cards:
        try:
            company = card.find('h4', class_='base-search-card__subtitle').text.strip()
            title = card.find('h3', class_='base-search-card__title').text.strip()
            location = card.find('span', class_='job-search-card__location').text.strip()
            posted_on = card.find('time', class_='job-search-card__listdate')['datetime']
            job_link = card.find('a', class_='base-card__full-link')['href']
            job_id = job_link.split('/')[-2]
            
            job = {
                "company": company,
                "job_title": title,
                "linkedin_job_id": job_id,
                "location": location,
                "posted_on": posted_on,
                "posted_date": parse_date(posted_on),
                "Seniority level": None,
                "Employment type": None
            }
            jobs.append(job)
            log(f"Parsed job: {company} - {title} - {location}")
        except Exception as e:
            log(f"Error parsing job card: {str(e)}")

def parse_date(posted_on):
    try:
        return datetime.fromisoformat(posted_on.replace('Z', '+00:00')).strftime("%d-%m-%Y")
    except:
        return datetime.now().strftime("%d-%m-%Y")

# Scrape each URL
for url in urls:
    scrape_linkedin_jobs(url)

driver.quit()
log("WebDriver closed")

log(f"Total jobs scraped: {len(jobs)}")

if len(jobs) == 0:
    log("No jobs were scraped. Please check the scraping logic.")
else:
    # Convert to DataFrame
    df = pd.DataFrame(jobs)

    # Save to JSON and CSV
    json_file = "D:/assignment/linkedin_jobs.json"
    csv_file = "D:/assignment/linkedin_jobs.csv"
    
    df.to_json(json_file, orient="records", indent=4)
    df.to_csv(csv_file, index=False)
    
    # Verify that files are not empty
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            json_data = json.load(f)
            log(f"JSON file contains {len(json_data)} job records.")
    else:
        log(f"JSON file not found at {json_file}")
    
    if os.path.exists(csv_file):
        csv_df = pd.read_csv(csv_file)
        log(f"CSV file contains {len(csv_df)} job records.")
    else:
        log(f"CSV file not found at {csv_file}")
    
    log(f"Data scraping completed. Scraped {len(jobs)} jobs.")

# Print the first few jobs for verification
log("\nFirst few scraped jobs:")
log(json.dumps(jobs[:5], indent=2))

log("Script completed")
sys.stdout.close()
