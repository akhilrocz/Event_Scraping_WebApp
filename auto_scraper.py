import schedule
import time
import os

def run_scraper():
    os.system("python scraper.py")

# Run scraper every 24 hours
schedule.every(24).hours.do(run_scraper)

while True:
    schedule.run_pending()
    time.sleep(60)  
