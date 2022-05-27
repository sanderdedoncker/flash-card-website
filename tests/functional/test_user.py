import pytest

from flask_login import current_user

from application.models import User, Card, Score


def test_profile(client, auth, user, admin):
    """
    GIVEN a Flask client with attached app and database
    WHEN user is not logged in
    THEN check if you get unauthorized error
    WHEN user (with card and scores) logs in and visits profile page
    THEN check if it is rendered correctly
    WHEN admin (without card and scores) logs in and visits profile page
    THEN check if it is rendered correctly
    """
    response = client.get('/user')
    assert response.status_code == 401

    auth.login()
    response = client.get('/user')
    assert response.status_code == 200
    assert str.encode(user.username) in response.data
    assert str.encode(user.email) in response.data
    assert str.encode(str(user.added_on.date()) if user.added_on else 'Unknown') in response.data
    assert b"Reviewable" in response.data
    assert b"Reviewed" in response.data

    auth.logout()
    auth.login(email=admin.email, password=admin.plain_password)
    response = client.get('/user')
    assert response.status_code == 200
    assert str.encode(admin.username) in response.data
    assert str.encode(admin.email) in response.data
    assert str.encode(str(admin.added_on.date()) if admin.added_on else 'Unknown') in response.data
    assert b"Reviewable" not in response.data
    assert b"Reviewed" not in response.data
    assert b"cards" in response.data


def test_edit_user(client, app, auth, user, admin):
    """
    GIVEN a Flask client with attached app and database
    WHEN user edit link is opened
    THEN check if you get unauthorized error
    WHEN user logs in and visits edit page
    THEN check if it is rendered correctly
    WHEN change to existing email
    THEN check if change fails
    WHEN change to valid new email, username
    THEN check if change was successful, and if user in database
    """
    response = client.get('/user/edit')
    assert response.status_code == 401

    auth.login()
    response = client.get('/user/edit')
    assert response.status_code == 200
    assert b"edit" in response.data
    assert b"form" in response.data

    response = client.post('/user/edit', data={'email': admin.email,
                                               'username': user.username}, follow_redirects=True)
    assert response.status_code == 200
    assert b'already registered' in response.data

    response = client.post('/user/edit', data={'email': 'new_user@a.b',
                                               'username': 'new_user'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"successful" in response.data
    assert response.request.path == "/user"

    with app.app_context():
        assert User.query.filter_by(email='new_user@a.b').filter_by(username='new_user').one_or_none() is not None


@pytest.mark.parametrize(('username', 'email', 'message'), (
    ('', 'new_user@a.b', b'This field is required.'),
    ('new_user', '', b'This field is required.'),
    ('new_user', 'new_user', b'Invalid email address.'),
))
def test_edit_user_validate_input(client, auth, username, email, message):
    """
    GIVEN a Flask client with attached app and database
    WHEN user edit without name or email
    THEN check if user edit fails
    WHEN user edit with invalid email
    THEN check if user edit fails
    """
    auth.login()
    response = client.post('/user/edit', data={'email': email,
                                               'username': username}, follow_redirects=True)
    assert response.status_code == 200
    assert message in response.data
    assert response.request.path == "/user/edit"


def test_reset_password(client, app, auth, user):
    """
    GIVEN a Flask client with attached app and database
    WHEN reset password link is opened
    THEN check if you get unauthorized error
    WHEN user logs in and visits reset password page
    THEN check if it is rendered correctly
    WHEN change to valid new password
    THEN check if change was successful, and in database
    """
    response = client.get('/user/reset_password')
    assert response.status_code == 401

    auth.login()
    response = client.get('/user/reset_password')
    assert response.status_code == 200
    assert b"password" in response.data
    assert b"form" in response.data

    response = client.post('/user/reset_password', data={'password': 'new',
                                                         'confirm_password': 'new'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"successful" in response.data
    assert response.request.path == "/user"

    with app.app_context():
        assert User.query.get(user.id).check_password('new')


@pytest.mark.parametrize(('password', 'confirm_password', 'message'), (
    ('', 'new_user', b'This field is required.'),
    ('new_user', '', b'This field is required.'),
    ('new_user', 'nw_user', b'Passwords must match.'),
))
def test_reset_password_validate_input(client, auth, password, confirm_password, message):
    """
    GIVEN a Flask client with attached app and database
    WHEN reset password without password
    THEN check if reset password fails
    WHEN reset password with non-matching password
    THEN check if reset password fails
    """
    auth.login()
    response = client.post('/user/reset_password', data={'password': password,
                                                         'confirm_password': confirm_password}, follow_redirects=True)
    assert response.status_code == 200
    assert message in response.data
    assert response.request.path == "/user/reset_password"


def test_delete_user(client, app, auth, user):
    """
    GIVEN a Flask client with attached app and database
    WHEN delete user link is opened
    THEN check if you get unauthorized error
    WHEN user logs in and visits delete user page
    THEN check if it is rendered correctly
    WHEN user is deleted
    THEN check if deletion was successful, and in database
    THEN check if user's cards and scores were deleted
    THEN check if user was logged out
    """
    response = client.get('/user/delete')
    assert response.status_code == 401

    auth.login()
    response = client.get('/user/delete')
    assert response.status_code == 200
    assert b"delete" in response.data
    assert b"user" in response.data

    response = client.post('/user/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b"successful" in response.data
    assert response.request.path == "/"

    with app.app_context():
        assert User.query.get(user.id) is None
        assert Card.query.filter_by(user_id=user.id).one_or_none() is None
        assert Score.query.filter_by(user_id=user.id).one_or_none() is None

    with client:
        client.get("/")
        assert not current_user.is_authenticated
        assert current_user.is_anonymous

    response = auth.login()
    assert b"nvalid" in response.data
