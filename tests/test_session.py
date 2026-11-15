from model.session import Session

def test_session_creation():
    """Test if creating a session works"""
    session = Session(
        name="Test Session",
        creator="Bob"
    )

    assert session.name == "Test Session"
    assert session.creator == "Bob"
    assert session.is_public is True
    assert session.members == ["Bob"]


def test_session_has_timestamp():
    """Testing if a session will have a timestamp"""
    session = Session(
        name="Test Session",
        creator="Bob"
    )

    assert session.timestamp is not None


def test_session_from_document():
    """Testing the actual session"""
    document = {
        "_id": "507f1f77bcf86cd799439011",
        "name": "Shared Session",
        "creator": "Bob",
        "is_public": True,
        "members": ["Bob", "Harry"],
        "timestamp": None
    }

    session = Session.from_document(document)

    assert session.name == "Shared Session"
    assert session.creator == "Bob"
    assert session.members == ["Bob", "Harry"]
    assert session.session_id == "507f1f77bcf86cd799439011"