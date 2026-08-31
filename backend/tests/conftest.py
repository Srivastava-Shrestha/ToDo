import pytest
from app import create_app
from app.extensions import db


@pytest.fixture()
def app():
    application = create_app("testing")
    yield application
    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_headers(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Shrestha Srivastava",
            "email": "shrestha@example.com",
            "password": "Password123!",
        },
    )
    token = response.get_json()["token"]
    return {"Authentication-Token": token}
