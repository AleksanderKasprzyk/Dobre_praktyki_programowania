import pytest
from endpoint import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_movies_list(client):
    resp = client.get("/movies")
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_single_movie_existing(client):
    resp = client.get("/movies")
    movies = resp.get_json()
    movie_id = movies[0]["movieId"]

    resp = client.get(f"/movies/{movie_id}")
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["movieId"] == movie_id


def test_get_single_movie_not_found(client):
    resp = client.get("/movies/999999999")
    assert resp.status_code == 404


def test_create_movie(client):
    new_movie = {
        "movieId": 999998,
        "title": "Test Movie",
        "genres": "Test|Movie"}

    resp = client.post("/movies", json=new_movie)
    assert resp.status_code == 201

    data = resp.get_json()
    assert data["movieId"] == new_movie["movieId"]
    assert data["title"] == new_movie["title"]

    client.delete(f"/movies/{new_movie['movieId']}")


def test_update_movie(client):
    movie = {
        "movieId": 999997,
        "title": "To be updated",
        "genres": "Old"}
    client.post("/movies", json=movie)
    update_data = {"title": "Updated title"}
    resp = client.put(f"/movies/{movie['movieId']}", json=update_data)
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["title"] == "Updated title"
    client.delete(f"/movies/{movie['movieId']}")


def test_delete_movie(client):
    movie = {
        "movieId": 999996,
        "title": "To be deleted",
        "genres": "Delete"}
    client.post("/movies", json=movie)

    resp = client.delete(f"/movies/{movie['movieId']}")
    assert resp.status_code == 200

    resp = client.get(f"/movies/{movie['movieId']}")
    assert resp.status_code == 404

def test_get_links_list(client):
    resp = client.get("/links")
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, list)


def test_get_single_link_existing(client):
    resp = client.get("/links")
    links = resp.get_json()
    assert len(links) > 0

    movie_id = links[0]["movieId"]

    resp = client.get(f"/links/{movie_id}")
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["movieId"] == movie_id

def test_get_single_link_not_found(client):
    resp = client.get("/links/999999999")
    assert resp.status_code == 404

def test_create_link(client):
    new_link = {
        "movieId": 998001,
        "imdbId": "tt9980010",
        "tmdbId": "998001"}

    resp = client.post("/links", json=new_link)
    assert resp.status_code == 201

    data = resp.get_json()
    assert data["movieId"] == new_link["movieId"]

    client.delete(f"/links/{new_link['movieId']}")


def test_update_link(client):
    link = {
        "movieId": 998002,
        "imdbId": "tt_old",
        "tmdbId": "old"}
    client.post("/links", json=link)

    update_data = {"imdbId": "tt_new"}

    resp = client.put(f"/links/{link['movieId']}", json=update_data)
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["imdbId"] == "tt_new"

    client.delete(f"/links/{link['movieId']}")


def test_delete_link(client):
    link = {
        "movieId": 998003,
        "imdbId": "tt_del",
        "tmdbId": "del"}
    client.post("/links", json=link)

    resp = client.delete(f"/links/{link['movieId']}")
    assert resp.status_code == 200

    resp = client.get(f"/links/{link['movieId']}")
    assert resp.status_code == 404

def test_get_ratings_list(client):
    resp = client.get("/ratings")
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, list)


def test_get_single_rating_existing(client):
    resp = client.get("/ratings")
    ratings = resp.get_json()
    assert len(ratings) > 0

    user_id = ratings[0]["userId"]

    resp = client.get(f"/ratings/{user_id}")
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["userId"] == user_id


def test_get_single_rating_not_found(client):
    resp = client.get("/ratings/999999999")
    assert resp.status_code == 404


def test_create_rating(client):
    new_rating = {
        "userId": 997001,
        "movieId": 1,
        "rating": 4.5,
        "timestamp": 1234567890}

    resp = client.post("/ratings", json=new_rating)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["userId"] == new_rating["userId"]
    client.delete(f"/ratings/{new_rating['userId']}")


def test_update_rating(client):
    rating = {
        "userId": 997002,
        "movieId": 1,
        "rating": 3.0,
        "timestamp": 1111111111}
    client.post("/ratings", json=rating)

    update_data = {"rating": 5.0}
    resp = client.put(f"/ratings/{rating['userId']}", json=update_data)
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["rating"] == 5.0
    client.delete(f"/ratings/{rating['userId']}")


def test_delete_rating(client):
    rating = {
        "userId": 997003,
        "movieId": 1,
        "rating": 2.0,
        "timestamp": 2222222222}
    client.post("/ratings", json=rating)

    resp = client.delete(f"/ratings/{rating['userId']}")
    assert resp.status_code == 200

    resp = client.get(f"/ratings/{rating['userId']}")
    assert resp.status_code == 404

def test_get_tags_list(client):
    resp = client.get("/tags")
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, list)


def test_get_single_tag_existing(client):
    resp = client.get("/tags")
    tags = resp.get_json()
    assert len(tags) > 0

    user_id = tags[0]["userId"]

    resp = client.get(f"/tags/{user_id}")
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["userId"] == user_id


def test_get_single_tag_not_found(client):
    resp = client.get("/tags/999999999")
    assert resp.status_code == 404


def test_create_tag(client):
    new_tag = {
        "userId": 996001,
        "movieId": 1,
        "tag": "test-tag",
        "timestamp": 3333333333}

    resp = client.post("/tags", json=new_tag)
    assert resp.status_code == 201

    data = resp.get_json()
    assert data["userId"] == new_tag["userId"]

    client.delete(f"/tags/{new_tag['userId']}")


def test_update_tag(client):
    tag = {
        "userId": 996002,
        "movieId": 1,
        "tag": "old-tag",
        "timestamp": 4444444444}
    client.post("/tags", json=tag)

    update_data = {"tag": "new-tag"}

    resp = client.put(f"/tags/{tag['userId']}", json=update_data)
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["tag"] == "new-tag"

    client.delete(f"/tags/{tag['userId']}")


def test_delete_tag(client):
    tag = {
        "userId": 996003,
        "movieId": 1,
        "tag": "delete-me",
        "timestamp": 5555555555}
    client.post("/tags", json=tag)

    resp = client.delete(f"/tags/{tag['userId']}")
    assert resp.status_code == 200

    resp = client.get(f"/tags/{tag['userId']}")
    assert resp.status_code == 404
