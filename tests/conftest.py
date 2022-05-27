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
from requests.auth import _basic_auth_str

from application import create_app, db
from application.models import User, Card, Score


@pytest.fixture(scope='function')
def admin():
    admin_user = User(
        id=0,
        username='admin',
        email='admin@a.b',
        admin=True,
        added_on=datetime.now()
    )
    admin_user.set_password('admin')
    admin_user.plain_password = 'admin'
    return admin_user


@pytest.fixture(scope='function')
def user():
    user = User(
        id=1,
        username='user',
        email='user@a.b',
        admin=False,
        added_on=datetime.now()
    )
    user.set_password('user')
    user.plain_password = 'user'
    return user


@pytest.fixture(scope='function')
def card():
    card = Card(
        id=0,
        front='card_front',
        back='card_back',
        private=True,
        added_on=datetime.now(),
        user_id=1
    )
    return card


@pytest.fixture(scope='function')
def score():
    score = Score(
        id=0,
        score=0,
        last_seen_on=datetime.now(),
        user_id=1,
        card_id=0
    )
    return score


@pytest.fixture
def app(admin, user, card, score):
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False,
    })
    with app.app_context():
        db.create_all()
        # If you don't set this, you cannot use 'detached' objects, see
        # https://stackoverflow.com/questions/58291247/using-objects-outside-of-the-sessions-scope-in-sqlalchemy
        # https://stackoverflow.com/questions/51446322/flask-sqlalchemy-set-expire-on-commit-false-only-for-current-session
        db.session().expire_on_commit = False
        db.session.add(admin)
        db.session.add(user)
        db.session.add(card)
        db.session.add(score)
        db.session.commit()

    yield app

    # SQLite in-memory db is destroyed once the session ends (after app is destroyed at the end of test fn),
    # so no db reset/cleanup needed


@pytest.fixture
def client(app):
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email='user@a.b', password='user'):  # credentials of the user fixture
        return self._client.post(
            '/auth/login',
            data={'email': email, 'password': password},
            follow_redirects=True
        )

    def logout(self):
        return self._client.get('/auth/logout', follow_redirects=True)

    def get_token(self, email='user@a.b', password='user'):  # credentials of the user fixture
        return self._client.post('/api/tokens', headers={
            "Authorization": _basic_auth_str(email, password),
        })

    def get_bearer_auth_header(self, email='user@a.b', password='user'): # credentials of the user fixture
        token = self.get_token(email=email, password=password).json.get("token", "")
        return {"Authorization": "Bearer " + token}

    def revoke_token(self, email='user@a.b', password='user'):  # credentials of the user fixture
        return self._client.delete('/api/tokens', headers=self.get_bearer_auth_header(email=email, password=password))


@pytest.fixture
def auth(client):
    return AuthActions(client)
