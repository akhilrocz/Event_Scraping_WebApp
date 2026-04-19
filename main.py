from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from bson.objectid import ObjectId
import os


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")


client = MongoClient(MONGO_URI)
db = client["eventsdb"]
events_collection = db["events"]
subscriptions_collection = db["subscriptions"]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EventOut(BaseModel):
    id: str
    title: str
    date: str
    location: str
    description: str
    link: str

class EmailInput(BaseModel):
    email: str
    event_id: str


@app.get("/events", response_model=list[EventOut])
def get_events():
    try:
        events = list(events_collection.find({}, {"_id": 1, "title": 1, "date": 1, "location": 1, "description": 1, "link": 1}))
        if not events:
            raise HTTPException(status_code=404, detail="No events found in MongoDB.")
        return [{"id": str(event["_id"]), **event} for event in events]
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/subscribe")
def subscribe(email_data: EmailInput):
    try:
       
        print(f"🔍 Checking event ID: {email_data.event_id}")

       
        try:
            event_object_id = ObjectId(email_data.event_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid event ID format.")

        
        event = events_collection.find_one({"_id": event_object_id})
        
        if not event:
            raise HTTPException(status_code=404, detail=f"Event with ID {email_data.event_id} not found")

      
        subscriptions_collection.insert_one(
            {"email": email_data.email, "event_id": email_data.event_id}
        )

        return {"message": "Subscription successful!"}

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



@app.get("/")
def root():
    return {"message": "Event Scraper API is running!"}
