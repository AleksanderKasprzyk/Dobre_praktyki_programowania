from flask import Flask, jsonify
from database import SessionLocal
from models import Movie, Link, Rating, Tag


app = Flask(__name__)

def row_to_dict(obj) -> dict:
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}

@app.get("/hello")
def hello():
    return jsonify({"hello": "world"}), 200

@app.get("/movies")
def get_movies():
    session = SessionLocal()
    try:
        movies = session.query(Movie).all()
        data = [row_to_dict(m) for m in movies]
        return jsonify(data), 200
    finally:
        session.close()

@app.get("/links")
def get_links():
    session = SessionLocal()
    try:
        links = session.query(Link).all()
        data = [row_to_dict(l) for l in links]
        return jsonify(data), 200
    finally:
        session.close()

@app.get("/ratings")
def get_ratings():
    session = SessionLocal()
    try:
        ratings = session.query(Rating).all()
        data = [row_to_dict(r) for r in ratings]
        return jsonify(data), 200
    finally:
        session.close()

@app.get("/tags")
def get_tags():
    session = SessionLocal()
    try:
        tags = session.query(Tag).all()
        data = [row_to_dict(t) for t in tags]
        return jsonify(data), 200
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)
