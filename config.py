import os


class Config:
    API_TITLE = "Events REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_SECRET_KEY = "andrii"
    SECRET_KEY = "9c9c2ff463c47cea625cf6652b9b2043"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    JWT_SECRET_KEY = "andrii"
    SECRET_KEY = "9c9c2ff463c47cea625cf6652b9b2043"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
