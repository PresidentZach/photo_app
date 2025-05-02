import sys
import os
import pytest
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

def test_calculate_date(photo_instance):
    """Test the date calculation method."""
    expected_date = datetime.now().strftime("%m-%d-%Y")
    assert photo_instance.date_created == expected_date

def test_insert_into_database(monkeypatch, photo_instance):
    """Test inserting a photo into the database."""
    def mock_insert(data):
        assert data["url"] == "http://example.com/photo.jpg"
        assert data["creator"] == "test_creator"
        assert data["tags"] == [1, 2, 3]
        assert data["is_favorited"] is False
        return {"id": 123}

    monkeypatch.setattr(photo_instance, "insert_into_database", mock_insert)
    result = photo_instance.insert_into_database()
    assert result["id"] == 123

def test_fetch_field(monkeypatch, photo_instance):
    """Test fetching a field from the database."""
    def mock_fetch_field(field_name):
        mock_data = {
            "url": "http://example.com/photo.jpg",
            "creator": "test_creator",
            "tags": [1, 2, 3],
            "is_favorited": False,
        }
        return mock_data.get(field_name)

    monkeypatch.setattr(photo_instance, "_fetch_field", mock_fetch_field)
    assert photo_instance.get_url() == "http://example.com/photo.jpg"
    assert photo_instance.get_creator() == "test_creator"
    assert photo_instance.get_tags# filepath: /Users/zach/Documents/coding_projects/photo_app/tests/test_photo.py
import pytest
from datetime import datetime
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

def test_calculate_date(photo_instance):
    """Test the date calculation method."""
    expected_date = datetime.now().strftime("%m-%d-%Y")
    assert photo_instance.date_created == expected_date

def test_insert_into_database(monkeypatch, photo_instance):
    """Test inserting a photo into the database."""
    def mock_insert(self):
        data = {
            "url": self.url,
            "creator": self.creator,
            "tags": self.tags,
            "is_favorited": self.is_favorited,
        }
        assert data["url"] == "http://example.com/photo.jpg"
        assert data["creator"] == "test_creator"
        assert data["tags"] == [1, 2, 3]
        assert data["is_favorited"] is False
        return {"id": 123}

    monkeypatch.setattr(Photo, "insert_into_database", mock_insert)
    result = photo_instance.insert_into_database()
    assert result["id"] == 123

def test_fetch_field(monkeypatch, photo_instance):
    """Test fetching a field from the database."""
    def mock_fetch_field(field_name):
        mock_data = {
            "url": "http://example.com/photo.jpg",
            "creator": "test_creator",
            "tags": [1, 2, 3],
            "is_favorited": False,
        }
        return mock_data.get(field_name)

    monkeypatch.setattr(photo_instance, "_fetch_field", mock_fetch_field)
    assert photo_instance.get_url() == "http://example.com/photo.jpg"
    assert photo_instance.get_creator() == "test_creator"
    assert photo_instance.get_tags