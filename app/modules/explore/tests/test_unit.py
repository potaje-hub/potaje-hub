import pytest
from unittest.mock import patch, MagicMock
from app.modules.explore.services import ExploreService
from app.modules.auth.models import User


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
    

@pytest.fixture
def explore_service():
    return ExploreService()


def test_get_all_by_num_of_models(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_get_all:
        mock_explore = [MagicMock(id=1), MagicMock(id=2), MagicMock(id=3), MagicMock(id=4)]
        mock_get_all.return_value = mock_explore

        result = explore_service.filter('', 'newest', 'any', 5, None, [])
        
        assert result == mock_explore
        assert len(result) == 4
        mock_get_all.assert_called_once_with('', 'newest', 'any', 5, None, [])
        
def test_get_all_by_num_of_features(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_get_all:
        mock_explore = [MagicMock(id=1), MagicMock(id=2), MagicMock(id=3), MagicMock(id=4)]
        mock_get_all.return_value = mock_explore

        result = explore_service.filter('', 'newest', 'any', None, 50, [])
        
        assert result == mock_explore
        assert len(result) == 4
        mock_get_all.assert_called_once_with('', 'newest', 'any', None, 50, [])
        
        
def test_get_all_by_num_of_features_and_models(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_get_all:
        mock_explore = [MagicMock(id=1), MagicMock(id=2), MagicMock(id=3), MagicMock(id=4)]
        mock_get_all.return_value = mock_explore

        result = explore_service.filter('', 'newest', 'any', 5, 50, [])
        
        assert result == mock_explore
        assert len(result) == 4
        mock_get_all.assert_called_once_with('', 'newest', 'any', 5, 50, [])  
        
# Negative cases     

def test_negative_get_all_by_num_of_models(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_get_all:
        mock_explore = []
        mock_get_all.return_value = mock_explore

        result = explore_service.filter('', 'newest', 'any', 2, None, [])
        
        assert result == mock_explore
        assert len(result) == 0
        mock_get_all.assert_called_once_with('', 'newest', 'any', 2, None, [])
        
def test_negative_get_all_by_num_of_features(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_get_all:
        mock_explore = []
        mock_get_all.return_value = mock_explore

        result = explore_service.filter('', 'newest', 'any', None, 31, [])
        
        assert result == mock_explore
        assert len(result) == 0
        mock_get_all.assert_called_once_with('', 'newest', 'any', None, 31, [])
        
        
def test_negative_get_all_by_num_of_features_and_models_wrong_models(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_get_all:
        mock_explore = []
        mock_get_all.return_value = mock_explore

        result = explore_service.filter('', 'newest', 'any', 3, 50, [])
        
        assert result == mock_explore
        assert len(result) == 0
        mock_get_all.assert_called_once_with('', 'newest', 'any', 3, 50, [])   
        
def test_negative_get_all_by_num_of_features_and_models_wrong_features(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_get_all:
        mock_explore = []
        mock_get_all.return_value = mock_explore

        result = explore_service.filter('', 'newest', 'any', 5, 23, [])
        
        assert result == mock_explore
        assert len(result) == 0
        mock_get_all.assert_called_once_with('', 'newest', 'any', 5, 23, [])