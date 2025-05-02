import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app.classes.photo import Photo

@pytest.fixture
def photo_instance():
    """Fixture to create a Photo instance for testing."""
    return Photo(url="http://example.com/photo.jpg", creator="test_creator", tags=[1, 2, 3])

def test_photo_initialization(photo_instance):
    """Test the initialization of the Photo class."""
    assert photo_instance.url == "http://example.com/photo.jpg"
    assert photo_instance.creator == "test_creator"
    assert photo_instance.tags == [1, 2, 3]
    assert photo_instance.is_favorited is False
    assert photo_instance.id == -1