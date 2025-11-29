import csv
from pathlib import Path
from movie import Movie

DATA_DIR = Path(__file__).parent / "data"


def load_movies_from_csv(filename: str = "movies.csv") -> list[dict]:
    movies_path = DATA_DIR / filename
    movies: list[dict] = []

    with movies_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            movie = Movie(
                movie_id=row["movieId"],
                title=row["title"],
                genres=row["genres"])
            movies.append(movie.__dict__)

    return movies
