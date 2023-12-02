from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import decode_token

from app.models import UserModel


def test_register(client, init_database):
    new_user = {
        "email": "test@example.com",
        "password": "password",
        "name": "Test User"
    }

    response = client.post("/auth/register", json=new_user)

    assert response.status_code == 201
    assert response.get_json() == {"message": "User created successfully."}
    user = UserModel.query.filter_by(email=new_user["email"]).first()
    assert user is not None
    assert user.name == new_user["name"]
    assert pbkdf2_sha256.verify(new_user["password"], user.password)


def test_login(client, test_user):
    login_credentials = {
        "email": test_user.email,
        "password": "password"
    }

    # Act
    response = client.post("/auth/login", json=login_credentials)

    # Assert
    assert response.status_code == 200
    access_token = response.get_json()["access_token"]
    decoded_token = decode_token(access_token)
    assert decoded_token["sub"] == test_user.id
