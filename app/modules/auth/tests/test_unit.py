import pytest
from flask import url_for

from app.modules.auth.services import AuthenticationService
from app.modules.auth.repositories import UserRepository
from app.modules.profile.repositories import UserProfileRepository


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        pass

    yield test_client


def test_login_success(test_client):
    response = test_client.post(
        "/login", data=dict(email="test@example.com", password="test1234"), follow_redirects=True
    )

    assert response.request.path != url_for("auth.login"), "Login was unsuccessful"

    test_client.get("/logout", follow_redirects=True)


def test_login_unsuccessful_bad_email(test_client):
    response = test_client.post(
        "/login", data=dict(email="bademail@example.com", password="test1234"), follow_redirects=True
    )

    assert response.request.path == url_for("auth.login"), "Login was unsuccessful"

    test_client.get("/logout", follow_redirects=True)


def test_login_unsuccessful_bad_password(test_client):
    response = test_client.post(
        "/login", data=dict(email="test@example.com", password="basspassword"), follow_redirects=True
    )

    assert response.request.path == url_for("auth.login"), "Login was unsuccessful"

    test_client.get("/logout", follow_redirects=True)


def test_signup_user_no_name(test_client):
    response = test_client.post(
        "/signup", data=dict(surname="Foo", email="test@example.com", password="test1234"), follow_redirects=True
    )
    assert response.request.path == url_for("auth.show_signup_form"), "Signup was unsuccessful"
    assert b"This field is required" in response.data, response.data


def test_signup_user_unsuccessful(test_client):
    email = "test@example.com"
    response = test_client.post(
        "/signup", data=dict(name="Test", surname="Foo", email=email, password="test1234"), follow_redirects=True
    )
    assert response.request.path == url_for("auth.show_signup_form"), "Signup was unsuccessful"
    assert f"Email {email} in use".encode("utf-8") in response.data


def test_signup_user_successful(test_client):
    response = test_client.post(
        "/signup",
        data=dict(name="Foo", surname="Example", email="foo@example.com", password="foo1234"),
        follow_redirects=True,
    )
    assert response.request.path == url_for("auth.login"), "Signup was unsuccessful"


def test_service_create_with_profie_success(clean_database):
    data = {
        "name": "Test",
        "surname": "Foo",
        "email": "service_test1@example.com",
        "password": "test1234"
    }
    data_developer1 = {
        "name": "Test",
        "surname": "Foo",
        "email": "service_test2@example.com",
        "password": "test1234",
        "developer": True,
        "github_user": "github_user_test"
    }
    data_developer2 = {
        "name": "Test",
        "surname": "Foo",
        "email": "service_test3@example.com",
        "password": "test1234",
        "developer": False,
        "github_user": ""
    }

    AuthenticationService().create_with_profile(**data)
    AuthenticationService().create_with_profile(**data_developer1)
    AuthenticationService().create_with_profile(**data_developer2)

    assert UserRepository().count() == 3
    assert UserProfileRepository().count() == 3


def test_service_create_with_profile_fail_no_email(clean_database):
    data = {
        "name": "Test",
        "surname": "Foo",
        "email": "",
        "password": "1234"
    }

    with pytest.raises(ValueError, match="Email is required."):
        AuthenticationService().create_with_profile(**data)

    assert UserRepository().count() == 0
    assert UserProfileRepository().count() == 0


def test_service_create_with_profile_fail_no_password(clean_database):
    data = {
        "name": "Test",
        "surname": "Foo",
        "email": "test4@example.com",
        "password": ""
    }

    with pytest.raises(ValueError, match="Password is required."):
        AuthenticationService().create_with_profile(**data)

    assert UserRepository().count() == 0
    assert UserProfileRepository().count() == 0


def test_service_create_with_profile_fail_developer_without_github_user(clean_database):
    data_developer1 = {
        "name": "Test",
        "surname": "Foo",
        "email": "test5@example.com",
        "password": "1234",
        "developer": True,
        "github_user": ""
    }
    data_developer2 = {
        "name": "Test",
        "surname": "Foo",
        "email": "test6@example.com",
        "password": "1234",
        "developer": True
    }
    data_developer3 = {
        "name": "Test",
        "surname": "Foo",
        "email": "service_test7@example.com",
        "password": "test1234",
        "developer": False
    }

    with pytest.raises(ValueError, match="For a developer a Github User is required."):
        AuthenticationService().create_with_profile(**data_developer1)
        AuthenticationService().create_with_profile(**data_developer2)
        AuthenticationService().create_with_profile(**data_developer3)

    assert UserRepository().count() == 0
    assert UserProfileRepository().count() == 0


def test_service_create_with_profile_fail_github_user_without_developer(clean_database):
    data_developer1 = {
        "name": "Test",
        "surname": "Foo",
        "email": "test8@example.com",
        "password": "1234",
        "developer": False,
        "github_user": "github_user_test"
    }
    data_developer2 = {
        "name": "Test",
        "surname": "Foo",
        "email": "test9@example.com",
        "password": "1234",
        "github_user": "github_user_test"
    }
    data_developer3 = {
        "name": "Test",
        "surname": "Foo",
        "email": "test10@example.com",
        "password": "1234",
        "github_user": ""
    }

    with pytest.raises(ValueError, match="Github User should not be provided if not a developer."):
        AuthenticationService().create_with_profile(**data_developer1)
        AuthenticationService().create_with_profile(**data_developer2)
        AuthenticationService().create_with_profile(**data_developer3)

    assert UserRepository().count() == 0
    assert UserProfileRepository().count() == 0
