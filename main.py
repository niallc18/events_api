import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Venue, Event, Artist
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic for request bodies
class VenueCreate(BaseModel):
    name: str
    bounding_box: str = None
    capacity: int = None

# Create a venue
@app.post("/venues/", status_code=status.HTTP_201_CREATED)
def create_venue(venue: VenueCreate, db: Session = Depends(get_db)):
    db_venue = Venue(name=venue.name, bounding_box=venue.bounding_box, capacity=venue.capacity)
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue

# Retrieve a venue
@app.get("/venues/{venue_id}")
def read_venue(venue_id: int, db: Session = Depends(get_db)):
    logging.info(f"Fetching venue with ID: {venue_id}")
    db_venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if db_venue is None:
        logging.warning(f"Venue with ID: {venue_id} not found")
        raise HTTPException(status_code=404, detail="Venue not found")
    return db_venue

# Retrieve all artists for an event
@app.get("/events/{event_id}/artists")
def read_artists_for_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event.artists