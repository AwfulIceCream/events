from flask_jwt_extended import create_access_token

from app.models import UserModel


def test_get_all_users(client, init_database):
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


def test_get_user_events(client, test_user):
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


def test_get_user_by_id(client, test_user):
    # Arrange
    access_token = create_access_token(identity=test_user.id, fresh=True)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Act
    response = client.get(f"/api/v1/users/{test_user.id}", headers=headers)

    # Assert
    assert response.status_code == 200
    assert response.get_json()['id'] == test_user.id


def test_update_user_by_id(client, test_user):
    # Arrange
    access_token = create_access_token(identity=test_user.id, fresh=True)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    user_data = {
        'name': 'new_username'
    }

    # Act
    response = client.put(f"/api/v1/users/{test_user.id}", headers=headers, json=user_data)

    # Assert
    assert response.status_code == 200
    assert response.get_json()['name'] == 'new_username'


def test_delete_user_by_id(client, test_user):
    # Arrange
    access_token = create_access_token(identity=test_user.id, fresh=True)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Act
    response = client.delete(f"/api/v1/users/{test_user.id}", headers=headers)

    # Assert
    assert response.status_code == 204
    assert UserModel.query.get(test_user.id) is None
