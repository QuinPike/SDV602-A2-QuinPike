from data.database_manager import DatabaseManager
from datetime import datetime
import config

class ChatMessage:

    def __init__(self, username, text, timestamp=None, session_id=None):
        self.username = username
        self.text = text
        self.session_id = session_id

        if timestamp is None:
            self.timestamp = datetime.now()
        else:
            self.timestamp = timestamp

        self.db = DatabaseManager.getInstance()

    def save(self):
        return self.db.insert_one(config.CHAT_MESSAGES_COLLECTION, {
            "username": self.username,
            "text": self.text,
            "timestamp": self.timestamp,
            "session_id": self.session_id
        })

    @classmethod
    def all(cls, session_id):
        db = DatabaseManager.getInstance()
        collection = db.get_collection(config.CHAT_MESSAGES_COLLECTION)

        messages = []

        documents = collection.find({
            "session_id": session_id
        }).sort("timestamp", 1)

        for document in documents:
            message = cls(
                document["username"],
                document["text"],
                document.get("timestamp"),
                document.get("session_id")
            )
            messages.append(message)

        return messages
