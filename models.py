from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    genre = Column(String)

class Venue(Base):
    __tablename__ = 'venues'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    bounding_box = Column(String)
    capacity = Column(Integer)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(DateTime)
    venue_id = Column(Integer, ForeignKey('venues.id'), nullable=False)
    venue = relationship('Venue', back_populates='events')
    artists = relationship('Artist', secondary='event_artist', back_populates='events')

event_artist = Table('event_artist', Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('artist_id', Integer, ForeignKey('artists.id'), primary_key=True)
)

Venue.events = relationship('Event', order_by=Event.id, back_populates='venue')
Artist.events = relationship('Event', secondary=event_artist, back_populates='artists')