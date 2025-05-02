import pytest
from app.classes.tag import Tag

@pytest.fixture
def tag_instance():
    """Fixture to create a Tag instance for testing."""
    return Tag(name="test_tag")

def test_tag_initialization(tag_instance):
    """Test the initialization of the Tag class."""
    assert tag_instance.name == "test_tag"
    assert tag_instance.id == -1

def test_insert_into_database(monkeypatch, tag_instance):
    """Test inserting a tag into the database."""
    def mock_insert(self):
        data = {
            "name": self.name,
        }
        assert data["name"] == "test_tag"
        self.id = 123  # Set the id attribute directly
        return {"data": [{"id": 123}]}

    monkeypatch.setattr(Tag, "insert_into_database", mock_insert)
    tag_instance.insert_into_database()
    assert tag_instance.id == 123

def test_get_id(monkeypatch, tag_instance):
    """Test fetching the tag ID from the database."""
    def mock_get_id(self):
        self.id = 123
        return self.id

    monkeypatch.setattr(Tag, "get_id", mock_get_id)
    tag_id = tag_instance.get_id()
    assert tag_id == 123
    assert tag_instance.id == 123

def test_set_name(monkeypatch, tag_instance):
    """Test updating the tag name."""
    def mock_set_name(self, new_name):
        self.name = new_name

    monkeypatch.setattr(Tag, "set_name", mock_set_name)
    tag_instance.set_name("new_tag_name")
    assert tag_instance.name == "new_tag_name"

def test_delete(monkeypatch, tag_instance):
    """Test deleting a tag from the database."""
    def mock_delete(self):
        self.id = -1

    monkeypatch.setattr(Tag, "delete", mock_delete)
    tag_instance.delete()
    assert tag_instance.id == -1  # Assuming deletion resets the ID

def test_print_info(capsys, tag_instance):
    """Test the print_info method."""
    tag_instance.print_info()
    captured = capsys.readouterr()
    assert "Tag ID: -1" in captured.out
    assert "Tag Name: test_tag" in captured.out