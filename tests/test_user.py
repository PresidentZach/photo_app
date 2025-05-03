import pytest
from app.classes.user import User
from app.classes.photo import Photo

@pytest.fixture
def user_instance():
    """Fixture to create a User instance for testing."""
    return User()

def test_signup(monkeypatch, user_instance):
    """Test the signup method."""
    def mock_sign_up(data):
        assert data["email"] == "test@example.com"
        assert data["password"] == "password123"
        return True

    monkeypatch.setattr("app.supabase_client.supabase.auth.sign_up", mock_sign_up)
    result = user_instance.signup(email="test@example.com", password="password123")
    assert result is True

def test_signout(monkeypatch, user_instance):
    """Test the signout method."""
    def mock_sign_out():
        return True

    monkeypatch.setattr("app.supabase_client.supabase.auth.sign_out", mock_sign_out)
    result = user_instance.signout()
    assert result is True

def test_get_id(monkeypatch, user_instance):
    """Test the get_id method."""
    def mock_get_user():
        class MockUser:
            id = "mock_user_id"
        return type("Response", (), {"user": MockUser()})

    monkeypatch.setattr("app.supabase_client.supabase.auth.get_user", mock_get_user)
    result = user_instance.get_id()
    assert result == "mock_user_id"

def test_get_email(monkeypatch, user_instance):
    """Test the get_email method."""
    def mock_get_user():
        class MockUser:
            email = "test@example.com"
        return type("Response", (), {"user": MockUser()})

    monkeypatch.setattr("app.supabase_client.supabase.auth.get_user", mock_get_user)
    result = user_instance.get_email()
    assert result == "test@example.com"

def test_get_photo_list(user_instance):
    """Test the get_photo_list method."""
    user_instance.global_user_photo_list = [Photo(url="http://example.com/photo.jpg", creator="mock_user", tags=[1])]
    photo_list = user_instance.get_photo_list()
    assert len(photo_list) == 1
    assert photo_list[0].url == "http://example.com/photo.jpg"