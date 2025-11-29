from sqlalchemy import Column, Integer, Float, String
from database import Base


class Movie(Base):
    __tablename__ = "movies"

    movieId = Column(Integer, primary_key=True)
    title = Column(String)
    genres = Column(String)


class Link(Base):
    __tablename__ = "links"

    movieId = Column(Integer, primary_key=True)
    imdbId = Column(String)
    tmdbId = Column(String)


class Rating(Base):
    __tablename__ = "ratings"

    userId = Column(Integer, primary_key=True)
    movieId = Column(Integer)
    rating = Column(Float)
    timestamp = Column(Integer)


class Tag(Base):
    __tablename__ = "tags"

    userId = Column(Integer, primary_key=True)
    movieId = Column(Integer)
    tag = Column(String)
    timestamp = Column(Integer)
