import pytest
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app, get_db
from models import Base, Venue, Artist, Event


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    _client = TestClient(app)
    yield _client
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def session():
    connection = engine.connect()
    transaction = connection.begin()
    db_session = TestingSessionLocal(bind=connection)
    yield db_session
    db_session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def populate_db(session):
    venue = Venue(name="O2", bounding_box="10,5,8,1", capacity=80000)
    artist = Artist(name="Empire of the Sun", genre="Electronic")
    event_date = datetime.datetime.strptime("2022-01-01", "%Y-%m-%d").date()
    event = Event(name="Summer festival", date=event_date, venue=venue)
    event.artists.append(artist)
    session.add_all([venue, artist, event])
    session.commit()
    return venue, artist, event

# Dependency override for the database
@pytest.fixture(autouse=True)
def override_dependency(request):
    app.dependency_overrides[get_db] = lambda: request.getfixturevalue('session')

def test_create_venue(client):
    response = client.post("/venues/", json={"name": "Cardiff", "bounding_box": "10,10,10,10", "capacity": 30000})
    assert response.status_code == 201
    assert response.json()["name"] == "Cardiff"

def test_read_venue(client, populate_db):
    venue, _, _ = populate_db
    response = client.get(f"/venues/{venue.id}")
    assert response.status_code == 200, f"Failed to find venue with ID: {venue.id}"

def test_read_artists_for_event(client, populate_db):
    _, _, event = populate_db
    response = client.get(f"/events/{event.id}/artists")
    assert response.status_code == 200, f"Failed to find event with ID: {event.id}"