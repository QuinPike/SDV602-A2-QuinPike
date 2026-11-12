from data.database_manager import DatabaseManager
from datetime import datetime, timezone
from bson import ObjectId


class Session:

    COLLECTION = "sessions"

    def __init__(self, name, creator, is_public=True,
                 session_id=None, members=None, timestamp=None):

        self.name = name
        self.creator = creator
        self.is_public = is_public
        self.session_id = session_id
        self.members = members or [creator]
        self.timestamp = timestamp or datetime.now(timezone.utc)

    def save(self):
        db = DatabaseManager.getInstance()

        document = {
            "name": self.name,
            "creator": self.creator,
            "is_public": self.is_public,
            "members": self.members,
            "timestamp": self.timestamp
        }

        result = db.insert_one(self.COLLECTION, document)

        self.session_id = str(result)

        return self

    ## Factory Method to take the database record and convert it to the python object
    @classmethod
    def from_document(cls, document):
        return cls(
            name=document["name"],
            creator=document["creator"],
            is_public=document["is_public"],
            session_id=str(document["_id"]),
            members=document.get("members", []),
            timestamp=document.get("timestamp")
        )