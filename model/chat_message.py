from data.database_manager import DatabaseManager


class ChatMessage:
    # Make a collection variable 
    COLLECTION = "messages"

    def __init__(self, username, text, timestamp=None):
        self.username = username
        self.text = text
        self.timestamp = timestamp

    def save(self):
        db = DatabaseManager.getInstance()

        document = {
            "username": self.username,
            "text": self.text,
            "timestamp": self.timestamp
        }

        db.insert_one(self.COLLECTION, document)

    @classmethod
    def all(cls):
        db = DatabaseManager.getInstance()
        collection = db.get_collection(cls.COLLECTION)

        documents = collection.find().sort("_id", 1)

        messages = []

        for document in documents:
            message = cls(
                username=document["username"],
                text=document["text"],
                timestamp=document.get("timestamp")
            )
            messages.append(message)

        return messages