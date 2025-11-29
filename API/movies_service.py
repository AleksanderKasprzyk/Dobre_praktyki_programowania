import csv
from pathlib import Path
from movie import Movie, Link, Rating, Tag

DATA_DIR = Path(__file__).parent / "data"

def load_movies() -> list[dict]:
    movies_path = DATA_DIR / "movies.csv"
    movies: list[dict] = []

    with movies_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movie = Movie(
                movieId=row["movieId"],
                title=row["title"],
                genres=row["genres"])
            movies.append(movie.__dict__)

    return movies

def load_links() -> list[dict]:
    links_path = DATA_DIR / "links.csv"
    links: list[dict] = []

    with links_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            link = Link(
                movieId=row["movieId"],
                imdbId=row["imdbId"],
                tmdbId=row["tmdbId"])
            links.append(link.__dict__)

    return links

def load_ratings() -> list[dict]:
    ratings_path = DATA_DIR / "ratings.csv"
    ratings: list[dict] = []

    with ratings_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rating = Rating(
                userId=row["userId"],
                movieId=row["movieId"],
                rating=float(row["rating"]),
                timestamp=row["timestamp"])
            ratings.append(rating.__dict__)

    return ratings

def load_tags() -> list[dict]:
    tags_path = DATA_DIR / "tags.csv"
    tags: list[dict] = []

    with tags_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag = Tag(
                userId=row["userId"],
                movieId=row["movieId"],
                tag=row["tag"],
                timestamp=row["timestamp"])
            tags.append(tag.__dict__)

    return tags
