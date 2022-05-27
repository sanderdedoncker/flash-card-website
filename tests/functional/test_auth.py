import pytest

from flask_login import current_user

from application.models import User


def test_registration(client, app, user):
    """
    GIVEN a Flask client with attached app and database
    WHEN registration link is opened
    THEN check if it is rendered correctly
    WHEN registration with existing email
    THEN check if registration fails
    WHEN registration with new email
    THEN check if registration was successful, and if user in database
    """
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b"register" in response.data
    assert b"form" in response.data

    response = client.post('/auth/register', data={'email': user.email,
                                                   'username': 'new_user',
                                                   'password': 'new_user',
                                                   'confirm_password': 'new_user'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'already registered' in response.data

    response = client.post('/auth/register', data={'email': 'new_user@a.b',
                                                   'username': 'new_user',
                                                   'password': 'new_user',
                                                   'confirm_password': 'new_user'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"successful" in response.data
    assert response.request.path == "/"

    with app.app_context():
        assert User.query.filter_by(email='new_user@a.b').one_or_none() is not None


@pytest.mark.parametrize(('username', 'email', 'password', 'confirm_password', 'message'), (
    ('', 'new_user@a.b', 'new_user', 'new_user', b'This field is required.'),
    ('new_user', '', 'new_user', 'new_user', b'This field is required.'),
    ('new_user', 'new_user@a.b', '', 'new_user', b'This field is required.'),
    ('new_user', 'new_user@a.b', 'new_user', '', b'This field is required.'),
    ('new_user', 'new_user', 'new_user', 'new_user', b'Invalid email address.'),
    ('new_user', 'new_user@a.b', 'new_user', 'nw_user', b'Passwords must match.'),
))
def test_registration_validate_input(client, username, email, password, confirm_password, message):
    """
    GIVEN a Flask client with attached app and database
    WHEN registration without name, email or password
    THEN check if registration fails
    WHEN registration with invalid email
    THEN check if registration fails
    WHEN registration with non-matching password
    THEN check if registration fails
    """
    response = client.post('/auth/register', data={'email': email,
                                                   'username': username,
                                                   'password': password,
                                                   'confirm_password': confirm_password}, follow_redirects=True)
    assert response.status_code == 200
    assert message in response.data
    assert response.request.path == "/auth/register"


def test_login(client, auth, user):
    """
    GIVEN a Flask client with attached app and database, and an existing user
    WHEN login link is opened
    THEN check if it is rendered correctly
    WHEN login with invalid credentials
    THEN check if login fails
    WHEN login with default credentials
    THEN check if login successful, and if the client can then access protected pages
    WHEN login again with default credentials
    THEN check if redirected to home
    """
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b"login" in response.data
    assert b"form" in response.data

    response = auth.login(email="new_user@a.b", password="new_user")
    assert response.status_code == 200
    assert b"nvalid" in response.data
    assert response.request.path == "/auth/login"

    response = auth.login()
    assert response.status_code == 200
    assert b"successful" in response.data
    assert response.request.path == "/"

    with client:
        response = client.get('auth/secret')
        assert response.status_code == 200
        assert b"secret" in response.data

        assert current_user == user
        assert current_user.is_authenticated
        assert not current_user.is_anonymous

    response = auth.login()
    assert response.status_code == 200
    assert b"already logged in" in response.data
    assert response.request.path == "/"


@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('', 'new_user', b'This field is required.'),
    ('new_user@a.b', '', b'This field is required.'),
    ('new_user', 'new_user', b'Invalid email address.'),
))
def test_login_validate_input(client, auth, email, password, message):
    """
    GIVEN a Flask client with attached app and database
    WHEN login without email or password
    THEN check if login fails
    WHEN login with invalid email
    THEN check if login fails
    """
    response = auth.login(email=email, password=password)
    assert response.status_code == 200
    assert message in response.data
    assert response.request.path == "/auth/login"


def test_logout(client, auth):
    """
    GIVEN a Flask client with attached app and database, and a valid login
    WHEN logout
    THEN check if logout is successful and if redirected to home page
    """
    auth.login()

    with client:
        response = auth.logout()
        assert response.status_code == 200
        assert b"logged out" in response.data

        assert not current_user.is_authenticated
        assert current_user.is_anonymous




