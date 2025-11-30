from flask import Flask, jsonify, request
from database import SessionLocal
from models import Movie, Link, Rating, Tag

app = Flask(__name__)

def to_dict(obj) -> dict:
    if hasattr(obj, "as_dict"):
        return obj.as_dict()
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}

@app.get("/hello")
def hello():
    return jsonify({"hello": "world"}), 200

@app.get("/movies")
def get_movies():
    session = SessionLocal()
    try:
        movies = session.query(Movie).all()
        return jsonify([m.as_dict() for m in movies]), 200
    finally:
        session.close()


@app.get("/movies/<int:movie_id>")
def get_movie(movie_id: int):
    session = SessionLocal()
    try:
        movie = session.query(Movie).get(movie_id)
        if movie is None:
            return jsonify({"error": "Movie not found"}), 404
        return jsonify(movie.as_dict()), 200
    finally:
        session.close()

@app.post("/movies")
def create_movie():
    session = SessionLocal()
    data = request.json or {}

    movie = Movie(
        movieId=data.get("movieId"),
        title=data.get("title"),
        genres=data.get("genres"))

    session.add(movie)
    session.commit()
    session.refresh(movie)

    session.close()
    return jsonify(movie.as_dict()), 201


@app.put("/movies/<int:movie_id>")
def update_movie(movie_id: int):
    session = SessionLocal()
    data = request.json or {}

    movie = session.query(Movie).get(movie_id)
    if movie is None:
        session.close()
        return jsonify({"error": "Movie not found"}), 404

    movie.title = data.get("title", movie.title)
    movie.genres = data.get("genres", movie.genres)

    session.commit()
    session.refresh(movie)
    session.close()

    return jsonify(movie.as_dict()), 200


@app.delete("/movies/<int:movie_id>")
def delete_movie(movie_id: int):
    session = SessionLocal()
    movie = session.query(Movie).get(movie_id)

    if movie is None:
        session.close()
        return jsonify({"error": "Movie not found"}), 404

    session.delete(movie)
    session.commit()
    session.close()

    return jsonify({"status": "deleted"}), 200

@app.get("/links")
def get_links():
    session = SessionLocal()
    try:
        links = session.query(Link).all()
        return jsonify([l.as_dict() for l in links]), 200
    finally:
        session.close()

@app.get("/links/<int:movie_id>")
def get_link(movie_id: int):
    session = SessionLocal()
    try:
        link = session.query(Link).get(movie_id)
        if link is None:
            return jsonify({"error": "Link not found"}), 404
        return jsonify(link.as_dict()), 200
    finally:
        session.close()


@app.post("/links")
def create_link():
    session = SessionLocal()
    data = request.json or {}

    link = Link(
        movieId=data.get("movieId"),
        imdbId=data.get("imdbId"),
        tmdbId=data.get("tmdbId"))

    session.add(link)
    session.commit()
    session.refresh(link)
    session.close()

    return jsonify(link.as_dict()), 201

@app.put("/links/<int:movie_id>")
def update_link(movie_id: int):
    session = SessionLocal()
    data = request.json or {}

    link = session.query(Link).get(movie_id)
    if link is None:
        session.close()
        return jsonify({"error": "Link not found"}), 404

    link.imdbId = data.get("imdbId", link.imdbId)
    link.tmdbId = data.get("tmdbId", link.tmdbId)

    session.commit()
    session.refresh(link)
    session.close()

    return jsonify(link.as_dict()), 200

@app.delete("/links/<int:movie_id>")
def delete_link(movie_id: int):
    session = SessionLocal()
    link = session.query(Link).get(movie_id)
    if link is None:
        session.close()
        return jsonify({"error": "Link not found"}), 404

    session.delete(link)
    session.commit()
    session.close()

    return jsonify({"status": "deleted"}), 200

@app.get("/ratings")
def get_ratings():
    session = SessionLocal()
    try:
        ratings = session.query(Rating).all()
        return jsonify([r.as_dict() for r in ratings]), 200
    finally:
        session.close()

@app.get("/ratings/<int:user_id>")
def get_rating(user_id: int):
    session = SessionLocal()
    try:
        rating_obj = session.query(Rating).filter_by(userId=user_id).first()
        if rating_obj is None:
            return jsonify({"error": "Rating not found"}), 404
        return jsonify(rating_obj.as_dict()), 200
    finally:
        session.close()

@app.post("/ratings")
def create_rating():
    session = SessionLocal()
    data = request.json or {}
    user_id = data.get("userId")

    try:
        existing = session.query(Rating).filter_by(userId=user_id).first()
        if existing:
            existing.movieId = data.get("movieId", existing.movieId)
            existing.rating = data.get("rating", existing.rating)
            existing.timestamp = data.get("timestamp", existing.timestamp)
            session.commit()
            session.refresh(existing)
            return jsonify(existing.as_dict()), 201

        rating_obj = Rating(
            userId=user_id,
            movieId=data.get("movieId"),
            rating=data.get("rating"),
            timestamp=data.get("timestamp"))
        session.add(rating_obj)
        session.commit()
        session.refresh(rating_obj)
        return jsonify(rating_obj.as_dict()), 201
    finally:
        session.close()

@app.put("/ratings/<int:user_id>")
def update_rating(user_id: int):
    session = SessionLocal()
    data = request.json or {}

    try:
        rating_obj = session.query(Rating).filter_by(userId=user_id).first()
        if rating_obj is None:
            return jsonify({"error": "Rating not found"}), 404

        rating_obj.movieId = data.get("movieId", rating_obj.movieId)
        rating_obj.rating = data.get("rating", rating_obj.rating)
        rating_obj.timestamp = data.get("timestamp", rating_obj.timestamp)

        session.commit()
        session.refresh(rating_obj)
        return jsonify(rating_obj.as_dict()), 200
    finally:
        session.close()

@app.delete("/ratings/<int:user_id>")
def delete_rating(user_id: int):
    session = SessionLocal()
    try:
        rating_obj = session.query(Rating).filter_by(userId=user_id).first()
        if rating_obj is None:
            return jsonify({"error": "Rating not found"}), 404

        session.delete(rating_obj)
        session.commit()
        return jsonify({"status": "deleted"}), 200
    finally:
        session.close()

@app.get("/tags")
def get_tags():
    session = SessionLocal()
    try:
        tags = session.query(Tag).all()
        return jsonify([t.as_dict() for t in tags]), 200
    finally:
        session.close()

@app.get("/tags/<int:user_id>")
def get_tag(user_id: int):
    session = SessionLocal()
    try:
        tag_obj = session.query(Tag).filter_by(userId=user_id).first()
        if tag_obj is None:
            return jsonify({"error": "Tag not found"}), 404
        return jsonify(tag_obj.as_dict()), 200
    finally:
        session.close()


@app.post("/tags")
def create_tag():
    session = SessionLocal()
    data = request.json or {}
    user_id = data.get("userId")

    try:
        existing = session.query(Tag).filter_by(userId=user_id).first()
        if existing:
            existing.movieId = data.get("movieId", existing.movieId)
            existing.tag = data.get("tag", existing.tag)
            existing.timestamp = data.get("timestamp", existing.timestamp)
            session.commit()
            session.refresh(existing)
            return jsonify(existing.as_dict()), 201

        tag_obj = Tag(
            userId=user_id,
            movieId=data.get("movieId"),
            tag=data.get("tag"),
            timestamp=data.get("timestamp"),
        )
        session.add(tag_obj)
        session.commit()
        session.refresh(tag_obj)
        return jsonify(tag_obj.as_dict()), 201
    finally:
        session.close()


@app.put("/tags/<int:user_id>")
def update_tag(user_id: int):
    session = SessionLocal()
    data = request.json or {}

    try:
        tag_obj = session.query(Tag).filter_by(userId=user_id).first()
        if tag_obj is None:
            return jsonify({"error": "Tag not found"}), 404

        tag_obj.movieId = data.get("movieId", tag_obj.movieId)
        tag_obj.tag = data.get("tag", tag_obj.tag)
        tag_obj.timestamp = data.get("timestamp", tag_obj.timestamp)

        session.commit()
        session.refresh(tag_obj)
        return jsonify(tag_obj.as_dict()), 200
    finally:
        session.close()

@app.delete("/tags/<int:user_id>")
def delete_tag(user_id: int):
    session = SessionLocal()
    try:
        tag_obj = session.query(Tag).filter_by(userId=user_id).first()
        if tag_obj is None:
            return jsonify({"error": "Tag not found"}), 404

        session.delete(tag_obj)
        session.commit()
        return jsonify({"status": "deleted"}), 200
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)
