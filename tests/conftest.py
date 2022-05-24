"""
Testing using pytest and pytest-cov

Extra info:
https://flask.palletsprojects.com/en/2.1.x/testing/
https://flask.palletsprojects.com/en/2.1.x/tutorial/tests/
https://testdriven.io/blog/flask-pytest/
https://stackoverflow.com/questions/46646603/generate-urls-for-flask-test-client-with-url-for-function
"""

import pytest
from datetime import datetime

from application import create_app
from application.models import User, Card, Score


@pytest.fixture()
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def admin():
    admin_user = User(
        id=0,
        username='admin',
        email='admin@a.b',
        admin=True,
        added_on=datetime.now()
    )
    admin_user.set_password('admin')
    return admin_user


@pytest.fixture(scope='module')
def user():
    user = User(
        id=1,
        username='user',
        email='user@a.b',
        admin=False,
        added_on=datetime.now()
    )
    user.set_password('user')
    return user


@pytest.fixture(scope='function')
def card():
    card = Card(
        id=0,
        front='card_front',
        back='card_back',
        private=True,
        added_on=datetime.now(),
    )
    return card


@pytest.fixture(scope='function')
def score():
    score = Score(
        id=0,
        score=0,
        last_seen_on=datetime.now(),
    )
    return score
