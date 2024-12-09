import pytest
from flask import url_for
from app.modules.auth.services import AuthenticationService


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Verify user
        token = AuthenticationService().get_token_from_email("test@example.com")
        AuthenticationService().confirm_user_with_token(token)

    yield test_client

def test_login_success(test_client):
    response = test_client.post(
        "/login", data=dict(email="test@example.com", password="test1234"), follow_redirects=True
    )

    assert response.request.path != url_for("auth.login"), "Login was unsuccessful"

    test_client.get("/logout", follow_redirects=True)
