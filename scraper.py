import time
import os
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["eventsdb"]
events_collection = db["events"]


URL = "https://www.eventbrite.com.au/d/australia--sydney/all-events/"


chrome_options = Options()
chrome_options.headless = False  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def scrape_events():
    print("🔍 Scraping Eventbrite...")

    
    driver.get(URL)

   
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "event-card"))
        )
    except:
        print("⚠️ No events found! The page structure might have changed.")
        driver.quit()
        return

    # ✅ Scroll Down Aggressively to Load More Events
    for _ in range(10):  # Scroll 10 times
        driver.execute_script("window.scrollBy(0, 2000);")  # Scroll down more
        time.sleep(2)  # Wait for content to load

    time.sleep(5)  # Extra wait for JavaScript content

    # ✅ Find all event containers
    events = driver.find_elements(By.CLASS_NAME, "event-card")

    if not events:
        print("⚠️ No events found on Eventbrite! Please check the page structure.")
        driver.quit()
        return

    events_collection.delete_many({})  # ✅ Clear old events
    scraped_events = []

    for event in events:
        try:
            # ✅ Extract event link
            link_element = event.find_element(By.TAG_NAME, "a")
            link = link_element.get_attribute("href")

            # ✅ Extract event title
            title_element = event.find_element(By.TAG_NAME, "h3")
            title = title_element.text.strip()

            # ✅ Extract event date (First `<p>` inside event)
            date_element = event.find_elements(By.TAG_NAME, "p")[0]
            date = date_element.text.strip() if date_element else "Unknown Date"

            # ✅ Extract event location (Second `<p>` inside event)
            location_element = event.find_elements(By.TAG_NAME, "p")[1]
            location = location_element.text.strip() if location_element else "Unknown Location"

            event_data = {
                "title": title,
                "date": date,
                "location": location,
                "description": "Event details on Eventbrite",
                "link": link,
            }
            scraped_events.append(event_data)

        except Exception as e:
            print(f"⚠️ Error parsing event: {e}")

    # ✅ Insert only if events are scraped
    if scraped_events:
        events_collection.insert_many(scraped_events)
        print(f"✅ {len(scraped_events)} events scraped successfully!")
    else:
        print("⚠️ No valid events were found.")

        
        # ✅ Check how many events exist in MongoDB
    events_count = events_collection.count_documents({})
    print(f"🛠️ Total Events in MongoDB: {events_count}")


    driver.quit()  # Close browser

if __name__ == "__main__":
    scrape_events()
