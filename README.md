Event Scraping and Subscription System

A robust full-stack solution for automating the extraction of event data from Eventbrite, managing data persistence in MongoDB, and serving content via a high-performance FastAPI backend.

------------------------------
1. System Architecture
The application is composed of three core modules:

* Extraction Engine: A Selenium-based scraper that handles dynamic content loading and aggressive scrolling to capture comprehensive event listings.
* API Layer: A FastAPI implementation providing structured JSON endpoints for frontend consumption and user subscriptions.
* Automation Layer: A scheduling service that ensures the database remains synchronized with live web data.

------------------------------
2. Technical Stack

| Component | Technology |
|---|---|
| Language | Python 3.x |
| Scraping | Selenium, WebDriver Manager |
| Backend | FastAPI, Uvicorn |
| Database | MongoDB |
| Scheduling | Schedule Library |

------------------------------
## 3. Installation and Setup## Prerequisites

* Python 3.8+ installed
* MongoDB instance running locally
* Chrome Browser installed

Environment Configuration

   1. Clone the repository
   
   git clone <your-repo-url>
   cd Event_Scraping_WebApp
   
   2. Initialize Virtual Environment
   
   python -m venv .venv
   .\.venv\Scripts\activate
   
   3. Install Dependencies
   
   pip install fastapi uvicorn selenium pymongo webdriver-manager schedule pydantic
   
4. Operational Guide## Database Initialization
Execute the scraper manually to populate the initial event set:

python scraper.py

Server Deployment
Start the FastAPI development server:

uvicorn main:app --reload

5. API Reference## Get All Events

GET /events
Returns an array of event objects including titles, locations, and direct links.

Subscribe to Event
POST /subscribe
Accepts a JSON payload to link a user's email to a specific event ID.

{
  "email": "user@example.com",
  "event_id": "object_id_string"
}

6. Project Directory

Event_Scraping_WebApp/
├── main.py          # FastAPI Application
├── scraper.py       # Selenium Scraper Logic
├── scheduler.py     # Task Automation
└── .venv/           # Python Virtual Environment
