from datetime import datetime

from flask_jwt_extended import create_access_token

from app.models import EventModel


def test_event_get_all(client, test_user, init_database):
    # Arrange
    access_token = create_access_token(identity=test_user.id, fresh=True)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    new_event = EventModel(
        title="Event Title",
        description="Event Description",
        date=datetime.strptime("2023-12-01T13:25:38", "%Y-%m-%dT%H:%M:%S"),
        creator=test_user
    )

    db = init_database
    db.session.add(new_event)
    db.session.commit()

    # Act
    response = client.get(f"/api/v1/events/{new_event.id}", headers=headers)

    # Assert
    assert response.status_code == 200
    event_dict = {column.name: getattr(new_event, column.name) for column in new_event.__table__.columns}
    event_dict["date"] = event_dict["date"].strftime("%Y-%m-%d %H:%M:%S")
    assert response.get_json() == event_dict


# def test_event_resource(client, test_user, init_database):
#     # Arrange
#     access_token = create_access_token(identity=test_user.id, fresh=True)
#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }
#
#     new_event = EventModel(
#         title="Event Title",
#         description="Event Description",
#         date=datetime.strptime("2023-12-01T13:25:38", "%Y-%m-%dT%H:%M:%S"),
#         creator=test_user
#     )
#
#     db = init_database
#     db.session.add(new_event)
#     db.session.commit()
#
#     # Act
#     response = client.get(f"/events/{new_event.id}", headers=headers)
#
#     # Assert
#     assert response.status_code == 200
#     event_dict = {column.name: getattr(new_event, column.name) for column in new_event.__table__.columns}
#     event_dict["date"] = event_dict["date"].strftime("%Y-%m-%d %H:%M:%S")
#     assert response.get_json() == event_dict

def test_get_event_by_id(client, test_event, init_database):
    # Arrange
    access_token = create_access_token(identity=1, fresh=True)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Act
    response = client.get(f"/api/v1/events/{test_event.id}", headers=headers)

    # Assert
    assert response.status_code == 200
    assert response.get_json()['id'] == test_event.id


def test_add_event(client, test_user, init_database):
    # Arrange
    access_token = create_access_token(identity=test_user.id, fresh=True)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    event_data = {
        'title': 'Event Title',
        'description': 'Event Description',
        'date': '2023-12-01T13:25:38'
    }

    # Act
    response = client.post("/api/v1/events", headers=headers, json=event_data)

    # Assert
    assert response.status_code == 201
    assert response.get_json()['title'] == 'Event Title'
    assert response.get_json()['description'] == 'Event Description'


def test_update_event_by_id(client, test_event, init_database):
    # Arrange
    access_token = create_access_token(identity=test_event.creator.id, fresh=True)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    event_data = {
        'title': 'New Event Title',
        'description': 'New Event Description'
    }

    # Act
    response = client.put(f"/api/v1/events/{test_event.id}", headers=headers, json=event_data)

    # Assert
    assert response.status_code == 200
    assert response.get_json()['title'] == 'New Event Title'
    assert response.get_json()['description'] == 'New Event Description'


def test_delete_event_by_id(client, test_event, init_database):
    # Arrange
    access_token = create_access_token(identity=test_event.creator.id, fresh=True)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Act
    response = client.delete(f"/api/v1/events/{test_event.id}", headers=headers)

    # Assert
    assert response.status_code == 204
    assert EventModel.query.get(test_event.id) is None


def test_attend_event(client, test_user, init_database):
    # Arrange
    access_token = create_access_token(identity=test_user.id, fresh=True)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    new_event = EventModel(
        title="Event Title",
        description="Event Description",
        date=datetime.strptime("2023-12-01T13:25:38", "%Y-%m-%dT%H:%M:%S"),
        creator=test_user
    )

    db = init_database
    db.session.add(new_event)
    db.session.commit()

    # Act
    response = client.post(f"/api/v1/events/{new_event.id}/attend/{test_user.id}", headers=headers)

    # Assert
    assert response.status_code == 200
    event = db.session.get(EventModel, new_event.id)
    assert test_user in event.attendees


def test_event_attendees(client, test_user, init_database):
    # Arrange
    access_token = create_access_token(identity=test_user.id, fresh=True)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    new_event = EventModel(
        title="Event Title",
        description="Event Description",
        date=datetime.strptime("2023-12-01T13:25:38", "%Y-%m-%dT%H:%M:%S")
    )

    db = init_database
    db.session.add(new_event)
    db.session.commit()

    # Act
    response = client.get(f"/api/v1/events/{new_event.id}/attendees", headers=headers)

    # Assert
    assert response.status_code == 200
    event = db.session.get(EventModel, new_event.id)
    assert len(response.get_json()) == len(event.attendees)
