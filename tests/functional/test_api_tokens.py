from application.models import User


def test_get_token(client, app, auth, user):
    """
    GIVEN a Flask client with attached app and database
    WHEN token is requested with invalid credentials
    THEN check if error is returned
    WHEN user is queried with invalid token
    THEN check if none is returned
    WHEN token is requested with valid credentials
    THEN check if token is returned, valid and in db
    WHEN token is requested with same credentials immediately after
    THEN check if same token is returned
    """
    response = auth.get_token(email="new_user@a.b",
                              password="new_user")
    assert response.status_code == 401

    with app.app_context():
        assert User.check_token("") is None

    response = auth.get_token()
    assert response.status_code == 200
    assert "token" in response.json
    token = response.json["token"]
    with app.app_context():
        assert User.check_token(token) == user

    assert auth.get_token().json["token"] == token


def test_revoke_token(client, app, auth):
    """
    GIVEN a Flask client with attached app and database
    WHEN non-existing token is revoked
    THEN check if error is returned
    WHEN token is requested with valid credentials and token is revoked with same credentials
    THEN check if token becomes invalid
    """
    response = auth.revoke_token(email="user@a.b",
                                 password="wrong")
    assert response.status_code == 401

    token = auth.get_token().json["token"]
    with app.app_context():
        assert User.check_token(token) is not None
    response = auth.revoke_token()
    assert response.status_code == 204
    with app.app_context():
        assert User.check_token(token) is None

