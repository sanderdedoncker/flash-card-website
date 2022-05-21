from flask import url_for


def test_home_page_contents(client):
    """
    GIVEN a Flask client
    WHEN the "/" page is requested (GET)
    THEN check that the response is valid and the contents are rendered properly
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome!" in response.data


def test_home_page_methods(client):
    """
    GIVEN a Flask client
    WHEN the "/" page is requested with methods other than get
    THEN check that the methods are disallowed
    """
    response = client.post("/")
    assert response.status_code == 405
    response = client.put("/")
    assert response.status_code == 405
    response = client.patch("/")
    assert response.status_code == 405
    response = client.delete("/")
    assert response.status_code == 405
