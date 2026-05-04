import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY',
        'dev-secret-key-change-this-in-production'
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = False

    DEBUG = os.environ.get("FLASK_DEBUG", "True") == "True"

    JSON_SORT_KEYS = False