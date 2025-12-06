import pytest
import bcrypt

from API.endpoint import app
from API.database import SessionLocal
from API.models_user import User


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_users():
    session = SessionLocal()
    session.query(User).delete()
    session.commit()
    session.close()


ADMIN = {
    "username": "admin",
    "password": "admin123",
    "role": "ROLE_ADMIN",}


def test_create_user_success(client):
    resp = client.post("/users", json=ADMIN)
    assert resp.status_code == 201

    data = resp.get_json()
    assert data["username"] == "admin"
    assert data["role"] == "ROLE_ADMIN"


def test_create_user_existingusername(client):
    client.post("/users", json=ADMIN)

    resp = client.post("/users", json=ADMIN)
    assert resp.status_code == 400

    data = resp.get_json()
    assert "error" in data


def test_login_success(client):
    client.post("/users", json=ADMIN)

    resp = client.post("/login", json={
        "username": "admin",
        "password": "admin123",})

    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data
    assert data["type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/users", json=ADMIN)

    resp = client.post("/login", json={
        "username": "admin",
        "password": "zlehaslo",})

    assert resp.status_code == 401
    data = resp.get_json()
    assert "error" in data

def create_user_and_token(client, username: str, password: str, role: str):
    resp = client.post("/users", json={
        "username": username,
        "password": password,
        "role": role,})
    assert resp.status_code in (200, 201)

    resp = client.post("/login", json={
        "username": username,
        "password": password,})
    assert resp.status_code == 200
    data = resp.get_json()
    token = data["access_token"]
    return token

#test_delete_tag_without_token_returns_401
def test_delete_tag_without_token401(client):
    resp = client.delete("/tags/1")
    assert resp.status_code == 401

def test_delete_tag_userforbidden(client):
    password = "user123"
    token = create_user_and_token(
        client,
        username="normal_user",
        password=password,
        role="ROLE_USER",)

    resp = client.delete(
        "/tags/1",
        headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 403

def test_delete_tag_adminallowed(client):
    password = "admin123"
    token = create_user_and_token(
        client,
        username="super_admin",
        password=password,
        role="ROLE_ADMIN",)

    resp = client.delete(
        "/tags/1",
        headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code in (200, 404)
