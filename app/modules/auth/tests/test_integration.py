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