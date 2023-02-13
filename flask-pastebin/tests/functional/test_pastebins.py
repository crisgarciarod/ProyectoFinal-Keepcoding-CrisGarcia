"""
This file contains the functional tests for the pastebin blueprint.
"""
from web.models import Pastebin


def test_home_page(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/" page is requested (GET)
    THEN check that the response code is valid
    """
    response = test_client.get("/")
    assert response.status_code == 200


def test_posting_pastebin(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/" page is posted to (POST)
    THEN check that the response is valid and pastebin is correctly created
    """
    response = test_client.post("/", data=dict(title="test title", content="test content",
                                syntax="text", expire_date=None, password=None), follow_redirects=True)

    assert response.status_code == 200

def test_pastebin_filter_by_id(init_database):
    """
    GIVEN a database access configured for testing
    WHEN Pastebin model is queried from DB
    THEN check that the Pastebin with given id exists already
    """
    assert Pastebin.query.filter_by(id=1).first()
    assert Pastebin.query.filter_by(id=2).first()
    assert not Pastebin.query.filter_by(id=3).first()


def test_accessing_pastebin(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/<link>" page is requested (GET)
    THEN check that the response code is valid and contains Pastebin
    """
    pastebin = Pastebin.query.filter_by(id=1).first()
    response = test_client.get("/" + pastebin.link)
    assert response.status_code == 200
    assert pastebin.content.encode() in response.data

    response = test_client.get("/test")
    assert response.status_code == 404


def test_accessing_pastebin_protected_with_password_with_cookie(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/<link>" page is requested (GET)
    THEN check that the response code is valid and set cookie to correct one with password to access page
    """
    pastebin = Pastebin.query.filter_by(id=2).first()
    response = test_client.get("/" + pastebin.link)

    assert response.status_code == 200
    assert b"This pastebin is private, please enter the password" in response.data
    assert not pastebin.content.encode() in response.data

    test_client.set_cookie("localhost", pastebin.link, pastebin.password)
    response = test_client.get("/" + pastebin.link)

    assert response.status_code == 200
    assert not b"This pastebin is private, please enter the password" in response.data
    assert pastebin.content.encode() in response.data


def test_accessing_raw_pastebin(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/raw/<link>" page is requested (GET)
    THEN check that the response code is valid and contains raw Pastebin
    """
    pastebin = Pastebin.query.filter_by(id=1).first()
    response = test_client.get("/raw/" + pastebin.link)
    assert response.status_code == 200
    assert pastebin.content.encode() in response.data

    response = test_client.get("/raw/test")
    assert response.status_code == 404


def test_accessing_raw_pastebin_protected_with_password(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/raw/<link>" page is requested (GET)
    THEN check that the response code is valid and returns 403 error
    """
    pastebin = Pastebin.query.filter_by(id=2).first()
    response = test_client.get("/raw/" + pastebin.link)

    assert response.status_code == 403
    assert not pastebin.content.encode() in response.data


def test_accessing_raw_pastebin_protected_with_password_with_cookie(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/raw/<link>" page is requested (GET)
    THEN check that the response code is valid and set cookie to correct one with password to access page
    """
    pastebin = Pastebin.query.filter_by(id=2).first()
    response = test_client.get("/raw/" + pastebin.link)

    assert response.status_code == 403
    assert not pastebin.content.encode() in response.data

    test_client.set_cookie("localhost", pastebin.link, pastebin.password)
    response = test_client.get("/raw/" + pastebin.link)

    assert response.status_code == 200
    assert pastebin.content.encode() in response.data


def test_download_pastebin(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/download/<link>" page is requested (GET)
    THEN check that the response code is valid and returns correct header
    """
    pastebin = Pastebin.query.filter_by(id=1).first()
    response = test_client.get("/download/" + pastebin.link)
    header = response.headers["Content-Disposition"]

    assert response.status_code == 200
    assert pastebin.content.encode() in response.data
    assert header
    assert "attachment" in header
    assert pastebin.link + ".txt" in header

    response = test_client.get("/download/test")
    assert response.status_code == 404


def test_download_pastebin_protected_with_password(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/download/<link>" page is requested (GET)
    THEN check that the response code is valid and returns error 403
    """
    pastebin = Pastebin.query.filter_by(id=2).first()
    response = test_client.get("/download/" + pastebin.link)

    assert response.status_code == 403
    assert not pastebin.content.encode() in response.data


def test_accessing_pastebin_protected_with_password_with_cookie(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/download/<link>" page is requested (GET)
    THEN check that the response code is valid and set cookie to correct one with password to access page
    """
    pastebin = Pastebin.query.filter_by(id=2).first()
    response = test_client.get("/download/" + pastebin.link)

    assert response.status_code == 403
    assert not pastebin.content.encode() in response.data

    test_client.set_cookie("localhost", pastebin.link, pastebin.password)
    response = test_client.get("/download/" + pastebin.link)
    header = response.headers["Content-Disposition"]

    assert response.status_code == 200
    assert pastebin.content.encode() in response.data
    assert header
    assert "attachment" in header
    assert pastebin.link + ".txt" in header


def test_delete_pastebin(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/delete/<link>" page is requested (GET)
    THEN check that the response is valid and returns error 403
    """
    pastebin = Pastebin.query.filter_by(id=1).first()
    response = test_client.get("/delete/" + pastebin.link)

    assert response.status_code == 403


def test_pastebin_get_public_pastebins(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN  the "/" page is requested (GET)
    THEN check that the get_public_pastebins function works correctly
    """
    pastebins = Pastebin.query.filter_by(password=None).all()[-10:]
    for pastebin in pastebins:
        assert pastebin

    assert len(pastebins) == 1
