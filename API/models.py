from sqlalchemy import Column, Integer, Float, String
from database import Base


class Movie(Base):
    __tablename__ = "movies"

    movieId = Column(Integer, primary_key=True)
    title = Column(String)
    genres = Column(String)

    def as_dict(self) -> dict:
        return {
            "movieId": self.movieId,
            "title": self.title,
            "genres": self.genres}

class Link(Base):
    __tablename__ = "links"

    movieId = Column(Integer, primary_key=True)
    imdbId = Column(String)
    tmdbId = Column(String)

    def as_dict(self) -> dict:
        return {
            "movieId": self.movieId,
            "imdbId": self.imdbId,
            "tmdbId": self.tmdbId}

class Rating(Base):
    __tablename__ = "ratings"

    userId = Column(Integer, primary_key=True)
    movieId = Column(Integer)
    rating = Column(Float)
    timestamp = Column(Integer)

    def as_dict(self) -> dict:
        return {
            "userId": self.userId,
            "movieId": self.movieId,
            "rating": self.rating,
            "timestamp": self.timestamp}

class Tag(Base):
    __tablename__ = "tags"

    userId = Column(Integer, primary_key=True)
    movieId = Column(Integer)
    tag = Column(String)
    timestamp = Column(Integer)

    def as_dict(self) -> dict:
        return {
            "userId": self.userId,
            "movieId": self.movieId,
            "tag": self.tag,
            "timestamp": self.timestamp}