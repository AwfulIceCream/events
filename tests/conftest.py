import pytest
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app import create_app, db
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
