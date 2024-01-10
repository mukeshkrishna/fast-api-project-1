from app import schemas
import pytest
from jose import JWTError, jwt
from app.config import settings
from fastapi import Depends, status, HTTPException


def test_root(client):
    response = client.get("/")
    print(response.json().get('message'))
    assert response.json().get('message') == "Hello World!"
    assert response.status_code == 200


def test_create_user(client):
    response = client.post("/users/",
                           json = {"email": "mukesh5@gmail.com", "password": "password@123"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "mukesh5@gmail.com"
    assert response.status_code == 201


def test_login(client, test_user):
    response = client.post("/login", data={"username": test_user['email'],"password": test_user['password']})
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200