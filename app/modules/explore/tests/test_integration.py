import pytest
import json


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        pass

    yield test_client


def test_get_datasests(test_client):
    """
    Test retrieving filtered datasets via POST request.
    """

    # Filter datasets
    response = test_client.post('/explore', data=json.dumps({
        'number_of_features': '',
        'number_of_models': '5',
        'publication_type': 'any',
        'query': '',
        'sorting': 'newest'
    }), content_type='application/json', follow_redirects=True)
    assert response.status_code == 200
    response_data = response.get_json()
    print(response_data)
