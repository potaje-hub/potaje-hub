import pytest
from app import create_app


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()
    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


def test_download_all_dataset_not_logged_in(test_client):
    response = test_client.get("/dataset/download_all", follow_redirects=False)
    assert response.status_code == 302, "Expected 302 Redirect when not logged in"
    assert "/login" in response.headers["Location"], "Expected redirect to login page"


def test_download_all_dataset_logged_in(test_client):
    login_response = test_client.post("/login", data=dict(
        username="testuser",
        password="testpassword"
    ), follow_redirects=True)
    assert login_response.status_code == 200, "Login failed"

    response = test_client.get("/dataset/download_all", follow_redirects=True)
    assert response.status_code == 200, "Download all datasets was successful"

    test_client.get("/logout", follow_redirects=True)
