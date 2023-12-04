import pytest
from flask_jwt_extended import create_access_token

from app import create_app
from app.models import UserModel


def test_user_list(client, init_database):
    # Arrange
    access_token = create_access_token(identity=1, fresh=True)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Act
    response = client.get("/api/v1/users", headers=headers)

    # Assert
    assert response.status_code == 200
    users = UserModel.query.all()
    assert len(response.get_json()) == len(users)


def test_user_events(client, test_user):
    # Arrange
    access_token = create_access_token(identity=test_user.id, fresh=True)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Act
    response = client.get(f"/api/v1/users/{test_user.id}/events", headers=headers)

    # Assert
    assert response.status_code == 200
    assert len(response.get_json()) == len(test_user.attending)
