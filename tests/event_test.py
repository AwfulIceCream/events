from datetime import datetime

from flask_jwt_extended import create_access_token

from app.models import EventModel


def test_event_resource(client, test_user, init_database):
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
    response = client.get(f"/events/{new_event.id}", headers=headers)

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


def test_attend_event_resource(client, test_user, init_database):
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
    response = client.post(f"/events/{new_event.id}/attend/{test_user.id}", headers=headers)

    # Assert
    assert response.status_code == 200
    event = db.session.get(EventModel, new_event.id)
    assert test_user in event.attendees


def test_event_attendees_resource(client, test_user, init_database):
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
    response = client.get(f"/events/{new_event.id}/attendees", headers=headers)

    # Assert
    assert response.status_code == 200
    event = db.session.get(EventModel, new_event.id)
    assert len(response.get_json()) == len(event.attendees)
