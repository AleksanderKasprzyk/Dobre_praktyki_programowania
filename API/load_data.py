import csv
from pathlib import Path
from API.models_user import User
from API.database import SessionLocal
from API.models import Movie, Link, Rating, Tag
import bcrypt

DATA_DIR = Path(__file__).parent / "data"


def load_movies():
    session = SessionLocal()
    path = DATA_DIR / "movies.csv"

    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movie = Movie(
                movieId=row["movieId"],
                title=row["title"],
                genres=row["genres"])
            session.add(movie)

    session.commit()
    session.close()


def load_links():
    session = SessionLocal()
    path = DATA_DIR / "links.csv"

    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            link = Link(
                movieId=row["movieId"],
                imdbId=row["imdbId"],
                tmdbId=row["tmdbId"])
            session.add(link)

    session.commit()
    session.close()


def load_ratings():
    session = SessionLocal()
    path = DATA_DIR / "ratings.csv"

    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rating = Rating(
                userId=row["userId"],
                movieId=row["movieId"],
                rating=row["rating"],
                timestamp=row["timestamp"])
            session.add(rating)

    session.commit()
    session.close()


def load_tags():
    session = SessionLocal()
    path = DATA_DIR / "tags.csv"

    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag = Tag(
                userId=row["userId"],
                movieId=row["movieId"],
                tag=row["tag"],
                timestamp=row["timestamp"])
            session.add(tag)

    session.commit()
    session.close()

def load_users():
    session = SessionLocal()
    password = "secret123"
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user = User(username="testuser", password_hash=pw_hash, role="ROLE_USER")
    session.add(user)
    session.commit()
    session.close()
    print("Dodano użytkownika testowego")

if __name__ == "__main__":
    load_movies()
    load_links()
    load_ratings()
    load_tags()
    load_users()
    print("Załadowano dane do bazy!")
