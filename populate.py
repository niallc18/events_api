from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Venue, Artist, Event
import datetime

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def populate_database():
    session = SessionLocal()
    Base.metadata.create_all(engine) 

    # Create and add new objects
    venue = Venue(name="O2", bounding_box="10,5,8,1", capacity=80000)
    artist = Artist(name="Empire of the Sun", genre="Electronic")
    event_date = datetime.datetime.strptime("2022-01-01", "%Y-%m-%d").date()
    event = Event(name="Summer festival", date=event_date, venue=venue)
    event.artists.append(artist)
    
    session.add_all([venue, artist, event])
    session.commit()

    # Print the IDs of the created records
    print(f"Venue ID: {venue.id}")
    print(f"Artist ID: {artist.id}")
    print(f"Event ID: {event.id}")

    return session

def cleanup_database(session):
    # Drop all data and tables
    Base.metadata.drop_all(engine)
    session.close()
    print("Database reset.")

if __name__ == "__main__":
    session = populate_database()
    input("Press Enter to reset database...")  
    cleanup_database(session)