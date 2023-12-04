from datetime import datetime

import pytest
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app import create_app, db
from app.models import EventModel
from app.models.user import UserModel
from config import TestingConfig


@pytest.fixture(scope='module')
def app():
    app = create_app(config_class=TestingConfig)
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def init_database():
    db.create_all()  # Create database tables
    yield db  # This allows tests to run with the initialized database
    db.drop_all()  # Drop all tables after the tests are done


@pytest.fixture(scope='module')
def test_user(init_database):
    user = UserModel(email="teest@example.com", name="test", password=pbkdf2_sha256.hash("password"))
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope='module')
def test_event(init_database, test_user):
    event = EventModel(
        title="Event Title",
        description="Event Description",
        date=datetime.strptime("2023-12-01T13:25:38", "%Y-%m-%dT%H:%M:%S"),
        creator=test_user
    )
    db.session.add(event)
    db.session.commit()
    return event
