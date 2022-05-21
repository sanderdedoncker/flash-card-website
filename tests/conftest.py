"""
Testing using pytest and pytest-cov

Extra info:
https://flask.palletsprojects.com/en/2.1.x/testing/
https://flask.palletsprojects.com/en/2.1.x/tutorial/tests/
https://testdriven.io/blog/flask-pytest/
https://stackoverflow.com/questions/46646603/generate-urls-for-flask-test-client-with-url-for-function
"""

import pytest

from application import create_app


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
