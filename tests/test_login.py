from model.user import User
import pytest
import uuid

from data.user_repository import UserRepository

def test_user_creation():
    """Test creating a user."""

    user = User(
        name="Bob",
        password="Password123"
    )

    assert user.name == "Bob"
    assert user.password == "Password123"
    assert user.id is None


def test_user_with_id():
    """Test creating a user with an ID."""

    user = User(
        name="Bob",
        password="Password123",
        user_id="123"
    )

    assert user.id == "123"

def test_user_creation_with_same_name():
    """Test that duplicate usernames are rejected."""

    repository = UserRepository()

    username = f"TestUser_{uuid.uuid4().hex[:8]}"

    repository.create_user(username, "Password123")

    with pytest.raises(Exception, match="Username already taken"):
        repository.create_user(username, "Password456")