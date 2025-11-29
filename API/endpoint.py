import csv
from pathlib import Path
from flask import Flask, jsonify
from movie import Movie
from movies_service import load_movies, load_links, load_ratings, load_tags


app = Flask(__name__)

class Movie:
    def __init__(self, movieId: str, title: str, genres: str):
        self.movieId = movieId
        self.title = title
        self.genres = genres

def load_movies() -> list[dict]:
    movies_path = Path(__file__).parent / "data" / "movies.csv"
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

@app.get("/hello")
def hello():
    return jsonify({"hello": "world"}), 200


@app.get("/movies")
def movies():
    data = load_movies()
    return jsonify(data), 200

@app.get("/hello")
def hello():
    return jsonify({"hello": "world"}), 200


@app.get("/movies")
def movies():
    data = load_movies()
    return jsonify(data), 200


@app.get("/links")
def links():
    data = load_links()
    return jsonify(data), 200


@app.get("/ratings")
def ratings():
    data = load_ratings()
    return jsonify(data), 200


@app.get("/tags")
def tags():
    data = load_tags()
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(debug=True)
